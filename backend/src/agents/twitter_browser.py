import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright
import agentql
import os

class TwitterBrowserAgent:
    """
    Agent that uses Playwright + AgentQL to browse Twitter/X profiles
    and extract recent tweets for sentiment analysis.
    """

    def __init__(self, api_key: str):
        # Ensure API key is set for AgentQL
        if api_key and not os.getenv("AGENTQL_API_KEY"):
             os.environ["AGENTQL_API_KEY"] = api_key
        
    async def browse_tweets(self, twitter_url: str) -> List[Dict[str, Any]]:
        """
        Browse a Twitter/X profile and return recent tweets.
        """
        print(f"Browsing Twitter profile: {twitter_url}")
        
        raw_tweets = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Use a user agent to mimic a real browser to avoid instant login walls if possible
                context = await browser.new_context(
                     user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                page = await agentql.wrap_async(page)
                
                await page.goto(twitter_url)
                await page.wait_for_timeout(5000)
                
                # Scroll a bit to trigger lazy loading
                await page.evaluate("window.scrollTo(0, 1000)")
                await page.wait_for_timeout(2000)

                # AgentQL Query for Tweets
                QUERY = """
                {
                    tweets[] {
                        text_content
                        date
                        metrics {
                            likes
                            retweets
                            replies
                        }
                    }
                }
                """
                
                print("Executing AgentQL query on Twitter...")
                response = await page.query_data(QUERY)
                
                if response:
                    tweets_data = response.get("tweets", []) or []
                    print(f"Found {len(tweets_data)} tweets")
                    
                    # Normalize to match the 'posts' structure expected by extractors
                    for t in tweets_data:
                        raw_tweets.append({
                            "content": t.get("text_content"),
                            "date": t.get("date"),
                            "engagement": {
                                "likes": t.get("metrics", {}).get("likes", 0),
                                "comments": t.get("metrics", {}).get("replies", 0) # Mapping replies to comments
                            },
                            "source": "twitter"
                        })
                else:
                    print("No tweets extracted.")
                
                await browser.close()

        except Exception as e:
            print(f"Error browsing Twitter: {e}")
            
        return raw_tweets
