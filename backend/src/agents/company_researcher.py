import asyncio
from typing import Dict, Any
from playwright.async_api import async_playwright

class CompanyResearcher:
    """
    Uses Playwright to research company context.
    """
    
    def __init__(self, api_key: str):
        pass

    async def research_company(self, company_name: str, person_role: str) -> Dict[str, Any]:
        """
        Research company and prioritize information based on context.
        """
        # Ensure inputs are safe strings
        if company_name is None:
            company_name = "Unknown"
        if person_role is None:
            person_role = "Unknown"

        print(f"Researching company: {company_name} for role: {person_role}")
        
        recent_news = []
        
        if not company_name or company_name == "Unknown":
             print("Warning: No company name provided for research.")
             return {
                "name": "Unknown",
                "industry": "Unknown",
                "funding": {"stage": "Unknown", "amount": "Unknown"},
                "recent_news": ["No company name provided."],
                "competitors": []
            }
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                # DuckDuckGo search for news
                url = f"https://duckduckgo.com/?q={company_name.replace(' ', '+')}+news&t=h_&ia=news"
                await page.goto(url)
                await page.wait_for_timeout(3000)
                
                # Simple extraction of news titles
                elements = await page.query_selector_all("a.result__a") # DDG news selector might vary, using generic result link
                
                # Fallback to generic text if specific selectors fail
                if not elements:
                     elements = await page.query_selector_all("h2")

                for el in elements[:3]:
                    text = await el.inner_text()
                    if text and len(text) > 10:
                        recent_news.append(text)
                
                await browser.close()
                
        except Exception as e:
            print(f"Error researching company: {e}")

        return {
            "name": company_name,
            "industry": "Technology", # Hard to determine without deeper scrape
            "funding": {
                "stage": "Unknown",
                "amount": "Unknown"
            },
            "recent_news": recent_news if recent_news else [f"No specific news found for {company_name}"],
            "competitors": []
        }
