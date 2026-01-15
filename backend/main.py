import asyncio
import os
import json
from src.config.yutori_config import YUTORI_CONFIG
from src.agents.linkedin_browser import LinkedInBrowserAgent
from src.agents.company_researcher import CompanyResearcher
from src.schemas.navigator_output import NavigatorOutput

async def main():
    print("--- Yutori Navigator Agent Starting ---")
    
    # Configuration
    api_key = YUTORI_CONFIG["api_key"]
    # if not api_key:
    #     print("Warning: YUTORI_API_KEY not set. Using mock mode.")
    #     api_key = "mock_key"
        
    # Input
    target_url = "https://linkedin.com/in/janedoe"
    meeting_context = "first meeting, potential technical partnership"
    print(f"Target: {target_url}")
    print(f"Context: {meeting_context}")
    print("-" * 30)

    # Initialize Agents
    browser = LinkedInBrowserAgent(api_key=api_key)
    researcher = CompanyResearcher(api_key=api_key)
    
    # Step 1: Browse Profile
    print("\n[1/3] Browsing Profile...")
    profile_data = await browser.browse_profile(target_url, meeting_context)
    
    # Step 2: Research Company
    print("\n[2/3] Researching Company...")
    company_name = profile_data["profile"]["company"]
    role = profile_data["profile"]["current_role"]
    company_data = await researcher.research_company(company_name, role)
    
    # Step 3: Synthesis & Output
    print("\n[3/3] Synthesizing Final Output...")
    
    final_output = {
        "profile": profile_data["profile"],
        "posts": profile_data["posts"],
        "company_context": company_data,
        "decision_metadata": profile_data["decision_metadata"]
    }
    
    # Validate with Pydantic
    try:
        validated_output = NavigatorOutput(**final_output)
        print("\nSUCCESS: Output validated against schema.")
        print(json.dumps(validated_output.dict(), indent=2))
        
        # Save to file for next phase
        with open("phase1_output.json", "w") as f:
            json.dump(validated_output.dict(), f, indent=2)
            print("\nOutput saved to phase1_output.json")
            
    except Exception as e:
        print(f"\nERROR: Validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
