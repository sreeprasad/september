import asyncio
import os
import json
from src.config.yutori_config import YUTORI_CONFIG
from src.agents.linkedin_browser import LinkedInBrowserAgent
from src.agents.yutori_researcher import YutoriResearcher
from src.agents.twitter_browser import TwitterBrowserAgent
from src.schemas.navigator_output import NavigatorOutput

async def main():
    print("--- Yutori Navigator Agent Starting ---")
    
    # Configuration
    api_key = YUTORI_CONFIG["api_key"]
    # if not api_key:
    #     print("Warning: YUTORI_API_KEY not set. Using mock mode.")
    #     api_key = "mock_key"
        
    # Input
    target_url = "https://www.linkedin.com/in/sreeprasadatrit/"
    twitter_target_url = "https://twitter.com/sreeprasadatrit" # Example fallback/additional source
    meeting_context = "first meeting, potential technical partnership"
    print(f"Target: {target_url}")
    print(f"Twitter Target: {twitter_target_url}")
    print(f"Context: {meeting_context}")
    print("-" * 30)

    # Initialize Agents
    browser = LinkedInBrowserAgent(api_key=api_key)
    twitter_browser = TwitterBrowserAgent(api_key=api_key)
    # Replaced CompanyResearcher with YutoriResearcher for deep agentic research
    researcher = YutoriResearcher(api_key=api_key)
    
    # Step 1: Browse Profile
    print("\n[1/3] Browsing Profile...")
    profile_data = await browser.browse_profile(target_url, meeting_context)
    
    # Step 1.5: Browse Twitter
    print("\n[1.5/3] Browsing Twitter...")
    twitter_posts = await twitter_browser.browse_tweets(twitter_target_url)
    if twitter_posts:
        print(f"Found {len(twitter_posts)} tweets. Merging into profile data.")
        # We append raw tweets. Note: They won't have 'priority_score' from the LinkedIn decision engine,
        # but the sanitize function in step 3 handles missing fields.
        if "posts" in profile_data:
            profile_data["posts"].extend(twitter_posts)
        else:
            profile_data["posts"] = twitter_posts
    else:
        print("No tweets found.")

    # Step 2: Research Company
    print("\n[2/3] Researching Company...")
    company_name = profile_data["profile"].get("company")
    role = profile_data["profile"].get("current_role")
    
    if not company_name:
        print("Warning: Could not extract company name from profile. Using 'Unknown'.")
        company_name = "Unknown"
        
    company_data = await researcher.research_company(company_name, role)
    
    # Step 3: Synthesis & Output
    print("\n[3/3] Synthesizing Final Output...")
    
    # Helper to parse connections
    def parse_connections(val):
        if isinstance(val, int): return val
        if isinstance(val, str):
            digits = "".join(filter(str.isdigit, val))
            return int(digits) if digits else 0
        return 0
        
    # Helper to sanitize posts
    def sanitize_post(post):
        engagement = post.get("engagement", {}) or {}
        
        def safe_int(v):
            if isinstance(v, int): return v
            if isinstance(v, str) and v.isdigit(): return int(v)
            return 0
            
        return {
            "content": post.get("content") or "",
            "date": post.get("date") or "Unknown Date",
            "engagement": {
                "likes": safe_int(engagement.get("likes")),
                "comments": safe_int(engagement.get("comments"))
            },
            "priority_score": post.get("priority_score", 0.0),
            "priority_reason": post.get("priority_reason", "No reason provided")
        }

    # Ensure profile has required fields for schema validation
    # If the Playwright scrape found extra fields (like 'about'), we want to keep them if the schema allows.
    # However, NavigatorOutput schema might need updating to accept them. 
    # For now, we fit into the existing schema, but print the extra data for verification.
    if "about" in profile_data["profile"]:
        print(f"\n[Info] Extracted About section (length {len(profile_data['profile']['about'])}): {profile_data['profile']['about'][:50]}...")
    
    profile_safe = {
        "name": profile_data["profile"].get("name") or "Unknown Candidate",
        "headline": profile_data["profile"].get("headline") or "Professional",
        "current_role": profile_data["profile"].get("current_role") or "Unknown Role",
        "company": profile_data["profile"].get("company") or "Unknown Company",
        "location": profile_data["profile"].get("location") or "Unknown Location",
        "connections": parse_connections(profile_data["profile"].get("connections"))
    }
    
    posts_safe = [sanitize_post(p) for p in profile_data["posts"]]

    final_output = {
        "profile": profile_safe,
        "posts": posts_safe,
        "company_context": company_data,
        "decision_metadata": profile_data["decision_metadata"]
    }
    
    # Validate with Pydantic
    try:
        validated_output = NavigatorOutput(**final_output)
        print("\nSUCCESS: Output validated against schema.")
        print(json.dumps(validated_output.model_dump(), indent=2))
        
        # Save to file for next phase
        with open("phase1_output.json", "w") as f:
            json.dump(validated_output.model_dump(), f, indent=2)
            print("\nOutput saved to phase1_output.json")
            
    except Exception as e:
        print(f"\nERROR: Validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
