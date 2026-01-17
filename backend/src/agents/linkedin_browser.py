import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright
import agentql
from .decision_engine import NavigatorDecisionEngine
import os

class LinkedInBrowserAgent:
    """
    Agent that uses Playwright + AgentQL to browse LinkedIn profiles
    and make intelligent decisions about what content matters.
    """

    def __init__(self, api_key: str):
        # Ensure API key is set for AgentQL
        if api_key and not os.getenv("AGENTQL_API_KEY"):
             os.environ["AGENTQL_API_KEY"] = api_key
        
        self.decision_engine = NavigatorDecisionEngine()

    async def browse_profile(self, linkedin_url: str, meeting_context: str) -> Dict[str, Any]:
        """
        Browse a LinkedIn profile and return prioritized data.
        """
        print(f"Browsing profile: {linkedin_url} with context: {meeting_context}")
        
        raw_profile = {}
        raw_posts = []

        try:
            async with async_playwright() as p:
                # Launch browser (headless=True for backend)
                browser = await p.chromium.launch(headless=True)
                
                # Load auth state if available
                auth_path = os.path.join(os.path.dirname(__file__), "../../data/cache/auth_state.json")
                if os.path.exists(auth_path):
                    print(f"Loading auth state from {auth_path}")
                    context = await browser.new_context(storage_state=auth_path)
                else:
                    print("No auth state found. Proceeding as guest (likely limited).")
                    context = await browser.new_context(
                         user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    )

                page = await context.new_page()
                
                # Wrap page with AgentQL
                page = await agentql.wrap_async(page)
                
                await page.goto(linkedin_url)
                # Wait for some content to load
                await page.wait_for_timeout(5000) 
                
                # Attempt Playwright scraping first (or in parallel) as requested
                print("Attempting deep scraping with Playwright...")
                playwright_data = await self._scrape_profile_playwright(page)
                
                # Define AgentQL Query
                QUERY = """
                {
                    profile {
                        name
                        headline
                        current_role
                        company
                        location
                        connections
                    }
                    posts[] {
                        content
                        date
                        engagement {
                            likes
                            comments
                        }
                    }
                }
                """
                
                # Execute Query
                response = None
                try:
                    response = await page.query_data(QUERY)
                except Exception as q_err:
                    print(f"AgentQL query error: {q_err}")
                
                ql_profile = {}
                ql_posts = []

                if response:
                    ql_profile = response.get("profile", {}) or {}
                    ql_posts = response.get("posts", []) or []

                    # Sanitize connections count
                    if "connections" in ql_profile and isinstance(ql_profile["connections"], str):
                        try:
                            # Extract numbers from string like "500+" -> 500
                            import re
                            nums = re.findall(r'\d+', ql_profile["connections"])
                            if nums:
                                ql_profile["connections"] = int(nums[0])
                            else:
                                ql_profile["connections"] = 0
                        except:
                            ql_profile["connections"] = 0
                
                # Merge Data: Prefer Playwright for details, AgentQL for structure if needed
                # For now, we overlay Playwright data on top of AgentQL data
                raw_profile = {**ql_profile, **playwright_data.get("profile", {})}
                
                # Merge posts: simple concatenation for now, could be smarter deduplication
                raw_posts = ql_posts + playwright_data.get("posts", [])

                await browser.close()
                
        except Exception as e:
            # If we fail (e.g. no AgentQL key or browser issue), we return empty to avoid breaking pipeline completely
            # but we are NOT falling back to mock data.
            print(f"Error browsing LinkedIn: {e}")
            return {"error": str(e), "profile": {}, "posts": [], "decision_metadata": {}}

        # Intelligent Filtering
        prioritized_posts = self.decision_engine.prioritize_data_points(raw_posts, meeting_context)
        decision_rationale = self.decision_engine.generate_reasoning(prioritized_posts)
        
        result = {
            "profile": raw_profile,
            "posts": prioritized_posts,
            "decision_metadata": {
                "total_data_points_found": len(raw_posts),
                "data_points_surfaced": len(prioritized_posts),
                "decision_rationale": decision_rationale
            }
        }

        return result

    async def _scrape_profile_playwright(self, page) -> Dict[str, Any]:
        """
        Deep extraction using Playwright selectors.
        """
        data = {"profile": {}, "posts": []}
        try:
            # --- Basic Info ---
            # Name
            name_el = await page.query_selector("h1.text-heading-xlarge")
            if name_el:
                data["profile"]["name"] = await name_el.inner_text()
            
            # Headline
            headline_el = await page.query_selector("div.text-body-medium")
            if headline_el:
                 data["profile"]["headline"] = await headline_el.inner_text()

            # Location
            loc_el = await page.query_selector("span.text-body-small.inline.t-black--light.break-words")
            if loc_el:
                data["profile"]["location"] = (await loc_el.inner_text()).strip()

            # About
            about_el = await page.query_selector("section#about div.inline-show-more-text span[aria-hidden='true']")
            if about_el:
                data["profile"]["about"] = await about_el.inner_text()

            # --- Experience ---
            # This is complex as classes are dynamic or nested. 
            # We look for the Experience section and iterate list items.
            # Simplified approach: Look for company names in experience section
            # (This is a robust effort, selectors might need maintenance)
            
            # --- Posts (Recent Activity) ---
            # Often in a separate tab or section "Activity"
            # We try to find feed updates if visible on main profile
            posts = await page.query_selector_all("div.feed-shared-update-v2")
            for post in posts:
                content_el = await post.query_selector("div.feed-shared-update-v2__description span[dir='ltr']")
                if content_el:
                    text = await content_el.inner_text()
                    data["posts"].append({
                        "content": text,
                        "date": "Recent", # Hard to parse relative time easily without more logic
                        "engagement": {"likes": 0, "comments": 0} # Placeholder
                    })
                    
        except Exception as e:
            print(f"Playwright scraping error: {e}")
            
        return data
