import asyncio
import os
import json
import sys

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.yutori_config import YUTORI_CONFIG
from src.agents.linkedin_browser import LinkedInBrowserAgent
from src.agents.company_researcher import CompanyResearcher
from src.agents.twitter_browser import TwitterBrowserAgent
from src.extractors.profile_extractor import SemanticProfileExtractor
from src.extractors.theme_engine import ThemeIdentificationEngine
from src.extractors.data_transformer import StructuredDataTransformer

async def main():
    print("--- Orchestrator Pipeline Test (Phase 1 + Phase 2) ---")
    
    # --- PHASE 1: Yutori Navigator ---
    print("\n=== PHASE 1: Yutori Navigator ===")
    
    api_key = YUTORI_CONFIG.get("api_key", "mock_key")
    target_url = "https://www.linkedin.com/in/sreeprasadatrit/"
    twitter_url = "https://twitter.com/sreeprasad" # Mock URL for testing
    meeting_context = "first meeting, potential technical partnership"
    
    browser = LinkedInBrowserAgent(api_key=api_key)
    twitter_browser = TwitterBrowserAgent(api_key=api_key)
    researcher = CompanyResearcher(api_key=api_key)
    
    print(f"Browsing: {target_url}")
    profile_data = await browser.browse_profile(target_url, meeting_context)
    
    # Twitter extraction
    print(f"Browsing Twitter: {twitter_url}")
    twitter_posts = await twitter_browser.browse_tweets(twitter_url)
    profile_data["posts"].extend(twitter_posts)
    
    company_name = profile_data["profile"]["company"]
    role = profile_data["profile"]["current_role"]
    print(f"Researching: {company_name}")
    company_data = await researcher.research_company(company_name, role)
    
    phase1_output = {
        "profile": profile_data["profile"],
        "posts": profile_data["posts"],
        "company_context": company_data,
        "decision_metadata": profile_data["decision_metadata"]
    }
    
    print("Phase 1 Complete. Output keys:", phase1_output.keys())
    
    # --- PHASE 2: AgentQL Extraction ---
    print("\n=== PHASE 2: AgentQL Extraction ===")
    
    extractor = SemanticProfileExtractor()
    theme_engine = ThemeIdentificationEngine()
    transformer = StructuredDataTransformer()
    
    print("Extracting themes...")
    themes = await extractor.extract_profile_themes(phase1_output["posts"])
    
    print("Analyzing sentiment...")
    sentiment = await extractor.extract_sentiment_patterns(phase1_output["posts"])
    
    print("Identifying deep themes...")
    theme_insights = theme_engine.identify_themes(phase1_output["posts"])
    insights = theme_engine.generate_theme_insights(theme_insights)
    
    # Construct intermediate extraction object
    raw_extraction = {
        "person": {
            "name": phase1_output["profile"]["name"],
            "role": phase1_output["profile"]["current_role"],
            "company": phase1_output["profile"]["company"],
            "professional_identity": themes.get("professional_identity", ""),
            "career_trajectory": "IC -> Lead -> CTO" # Mocked for now as it's not in extraction output
        },
        "themes": theme_insights,
        "sentiment": sentiment,
        "insights": insights,
        "company_context": {
            "name": phase1_output["company_context"]["name"],
            "relevance_score": 0.85, # Mocked
            "key_facts": phase1_output["company_context"]["recent_news"],
            "recent_developments": phase1_output["company_context"]["recent_news"]
        },
        "extraction_metadata": {
            "confidence_score": 0.95,
            "data_quality": "high",
            "extraction_time": "1.2s"
        }
    }
    
    print("Transforming to final format...")
    final_output = transformer.transform_to_briefing_format(raw_extraction)
    
    print("\n=== FINAL PIPELINE OUTPUT ===")
    print(json.dumps(final_output, indent=2))
    
    # Save to file
    with open("pipeline_output.json", "w") as f:
        json.dump(final_output, f, indent=2)
    print("\nSaved to pipeline_output.json")

if __name__ == "__main__":
    asyncio.run(main())
