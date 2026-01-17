import asyncio
import os
from src.agents.twitter_browser import TwitterBrowserAgent
from dotenv import load_dotenv

load_dotenv()

async def test_twitter_agent():
    print("Testing TwitterBrowserAgent...")
    
    # Use a mock key if not set, as we want to test fallback mostly if AgentQL is missing or fails
    api_key = os.getenv("AGENTQL_API_KEY", "mock_key")
    agent = TwitterBrowserAgent(api_key=api_key)
    
    # Target a profile. Using a generic one or the one from main
    # Note: Twitter scraping is hard without login. Expecting potentially empty results or errors,
    # but the goal is to verify the code runs and attempts fallback.
    target_url = "https://twitter.com/Twitter" 
    
    print(f"Browsing {target_url}...")
    tweets = await agent.browse_tweets(target_url)
    
    print("-" * 30)
    print(f"Result: Found {len(tweets)} tweets.")
    for t in tweets[:3]:
        print(f"- {t.get('date')}: {t.get('content')[:50]}...")
    print("-" * 30)

    if not tweets:
        print("Note: No tweets found. This might be due to Twitter login walls or anti-scraping.")
        print("However, if the fallback logic executed without crashing, the test is partial success.")

if __name__ == "__main__":
    asyncio.run(test_twitter_agent())
