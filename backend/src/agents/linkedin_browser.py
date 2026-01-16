import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright
import agentql
from .decision_engine import NavigatorDecisionEngine
import os
import json

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
                # Create context with a user agent to avoid immediate blocking
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Wrap page with AgentQL
                page = await agentql.wrap_async(page)
                
                await page.goto(linkedin_url)
                # Wait for some content to load
                await page.wait_for_timeout(5000) 
                
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
                response = await page.query_data(QUERY)
                
                if response:
                    raw_profile = response.get("profile", {}) or {}
                    raw_posts = response.get("posts", []) or []

                    # Sanitize connections count
                    if "connections" in raw_profile and isinstance(raw_profile["connections"], str):
                        try:
                            # Extract numbers from string like "500+" -> 500
                            import re
                            nums = re.findall(r'\d+', raw_profile["connections"])
                            if nums:
                                raw_profile["connections"] = int(nums[0])
                            else:
                                raw_profile["connections"] = 0
                        except:
                            raw_profile["connections"] = 0
                else:
                    pass

                await browser.close()
                
        except Exception as e:
            # If we fail (e.g. no AgentQL key or browser issue), we return empty to avoid breaking pipeline completely
            # but we are NOT falling back to mock data.
            print(f"Error browsing LinkedIn: {e}")

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
