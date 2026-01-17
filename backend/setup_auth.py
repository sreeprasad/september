import asyncio
import os
from playwright.async_api import async_playwright

AUTH_STATE_PATH = os.path.join(os.path.dirname(__file__), "data/cache/auth_state.json")

async def setup_auth():
    print("--- Authentication Setup Wizard ---")
    print("This script will launch a browser for you to log in to your accounts.")
    print("Please log in to LinkedIn and Twitter/X.")
    print("Once logged in, press Enter in this terminal to save the session state.")
    
    # Ensure cache directory exists
    os.makedirs(os.path.dirname(AUTH_STATE_PATH), exist_ok=True)

    async with async_playwright() as p:
        # Launch headed browser so user can interact
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        # Open tabs for convenience
        page_li = await context.new_page()
        await page_li.goto("https://www.linkedin.com/login")
        
        page_tw = await context.new_page()
        await page_tw.goto("https://twitter.com/i/flow/login")
        
        print("\nBrowser launched!")
        input("Press Enter here after you have successfully logged in to both sites...")
        
        # Save storage state (cookies, localStorage, etc.)
        await context.storage_state(path=AUTH_STATE_PATH)
        print(f"\nAuthentication state saved to: {AUTH_STATE_PATH}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(setup_auth())
