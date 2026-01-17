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
        
        raw_tweets = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                
                # Load auth state if available
                auth_path = os.path.join(os.path.dirname(__file__), "../../data/cache/auth_state.json")
                if os.path.exists(auth_path):
                    print(f"Loading auth state from {auth_path}")
                    context = await browser.new_context(storage_state=auth_path)
                else:
                    print("No auth state found. Proceeding as guest.")
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
                
                response = None
                try:
                    response = await page.query_data(QUERY)
                except Exception as query_error:
                    print(f"AgentQL query failed: {query_error}")

                if response and response.get("tweets"):
                    tweets_data = response.get("tweets", [])
                    
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
                
                # Fallback if AgentQL returns nothing
                if not raw_tweets:
                    print("AgentQL returned no tweets. Attempting Playwright fallback...")
                    raw_tweets = await self._scrape_tweets_fallback(page)
                
                await browser.close()

        except Exception as e:
            print(f"Error browsing Twitter: {e}")
            pass
            
        return raw_tweets

    async def _scrape_tweets_fallback(self, page) -> List[Dict[str, Any]]:
        """
        Fallback scraping method using standard Playwright selectors.
        """
        tweets = []
        try:
            # Select all tweet articles
            # Twitter uses <article data-testid="tweet">
            tweet_elements = await page.query_selector_all('article[data-testid="tweet"]')
            
            for tweet_el in tweet_elements:
                try:
                    # Extract Text
                    text_el = await tweet_el.query_selector('[data-testid="tweetText"]')
                    text = await text_el.inner_text() if text_el else ""
                    
                    # Extract Date
                    time_el = await tweet_el.query_selector('time')
                    date = await time_el.get_attribute('datetime') if time_el else "Unknown Date"
                    
                    # Extract Metrics
                    # Note: These selectors are based on data-testids which are generally stable but can change
                    like_el = await tweet_el.query_selector('[data-testid="like"]')
                    like_label = await like_el.get_attribute('aria-label') if like_el else ""
                    # Parse likes from aria-label (e.g., "100 Likes") or inner text if available
                    # For simplicity, we might just try to get the text number if visible
                    
                    # Alternative: get text content of the group
                    likes = 0
                    if like_el:
                        like_text = await like_el.inner_text()
                        if like_text and like_text.strip().isdigit():
                            likes = int(like_text.strip())
                            
                    reply_el = await tweet_el.query_selector('[data-testid="reply"]')
                    replies = 0
                    if reply_el:
                         reply_text = await reply_el.inner_text()
                         if reply_text and reply_text.strip().isdigit():
                             replies = int(reply_text.strip())

                    tweets.append({
                        "content": text,
                        "date": date,
                        "engagement": {
                            "likes": likes,
                            "comments": replies
                        },
                        "source": "twitter"
                    })
                except Exception as el_e:
                    continue
                    
        except Exception as e:
            print(f"Fallback scraping failed: {e}")
            
        return tweets
