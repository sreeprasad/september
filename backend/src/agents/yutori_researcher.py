import asyncio
import os
import json
import requests
import time
from typing import Dict, Any, List
from yutori import YutoriClient

class YutoriResearcher:
    """
    Agent that uses Yutori to perform deep research on companies and people.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        if not self.api_key:
            print("Warning: YUTORI_API_KEY not set for YutoriResearcher.")
            
        try:
            self.client = YutoriClient(api_key=self.api_key)
        except Exception as e:
            print(f"Failed to initialize YutoriClient: {e}")
            self.client = None

    async def research_company(self, company_name: str, person_role: str) -> Dict[str, Any]:
        """
        Research company and generate talking points using Yutori.
        """
        if not self.client:
            return self._fallback_response(company_name)

        print(f"Initiating Yutori research for {company_name}...")

        prompt = (
            f"Research the company '{company_name}'. "
            f"Find 3 recent news items (last 30 days) or key developments. "
            f"Identify the company's industry, funding stage (if applicable), and main competitors. "
            f"Also, considering the role '{person_role}', suggest 2 strategic talking points "
            f"for a meeting. "
            f"Return the result as a JSON object with keys: 'name', 'industry', 'funding', 'recent_news' (list), 'competitors' (list), 'talking_points' (list)."
        )

        try:
            # 1. Start Task
            payload = {
                "task": prompt,
                "start_url": "https://www.google.com" # Start at Google for broad research
            }
            
            initial_response = self.client.agent_run(payload)
            task_id = initial_response.get("task_id")
            
            if not task_id:
                print("Error: No task_id returned from Yutori.")
                return self._fallback_response(company_name)

            print(f"Yutori Task Started: {task_id}")
            print(f"Monitor at: {initial_response.get('view_url')}")

            # 2. Poll for Result
            # We'll poll for up to 90 seconds (Yutori tasks can take time)
            base_url = self.client.base_url
            headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
            
            for _ in range(45): # 45 * 2s = 90s
                # Note: In a production async app, we should use aiohttp or run in executor to avoid blocking
                # For this script, blocking is acceptable or we can use asyncio.sleep
                await asyncio.sleep(2)
                
                resp = requests.get(f"{base_url}/browsing/tasks/{task_id}", headers=headers)
                
                if resp.status_code != 200:
                    continue
                    
                task_data = resp.json()
                status = task_data.get("status")
                
                if status == "completed":
                    print("Yutori research completed.")
                    return self._parse_result(task_data, company_name)
                elif status == "failed":
                    print(f"Yutori task failed: {task_data.get('error')}")
                    return self._fallback_response(company_name)
            
            print("Yutori task timed out.")
            return self._fallback_response(company_name)

        except Exception as e:
            print(f"Error during Yutori research: {e}")
            return self._fallback_response(company_name)

    def _parse_result(self, task_data: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """
        Extract the JSON result from the task output.
        """
        # The result might be in 'output', 'result', or 'artifacts'. 
        # Inspecting the test run would help, but assuming 'result' or 'output' text.
        # Often agents return a final text answer.
        
        output_text = task_data.get("output", "") or task_data.get("result", "")
        
        # Try to parse JSON from text
        try:
            # simple json extraction
            if "```json" in output_text:
                json_str = output_text.split("```json")[1].split("```")[0]
            elif "{" in output_text:
                start = output_text.find("{")
                end = output_text.rfind("}") + 1
                json_str = output_text[start:end]
            else:
                json_str = output_text

            data = json.loads(json_str)
            # Ensure keys exist
            return {
                "name": data.get("name", company_name),
                "industry": data.get("industry", "Unknown"),
                "funding": data.get("funding", {"stage": "Unknown", "amount": "Unknown"}),
                "recent_news": data.get("recent_news", []),
                "competitors": data.get("competitors", []),
                # Extra fields
                "talking_points": data.get("talking_points", [])
            }
        except Exception:
            print("Failed to parse JSON from Yutori output. Returning raw text as news.")
            return {
                "name": company_name,
                "industry": "Unknown",
                "funding": {"stage": "Unknown", "amount": "Unknown"},
                "recent_news": [output_text[:500]] if output_text else ["No data returned."],
                "competitors": []
            }

    def _fallback_response(self, company_name: str) -> Dict[str, Any]:
        return {
            "name": company_name,
            "industry": "Unknown",
            "funding": {"stage": "Unknown", "amount": "Unknown"},
            "recent_news": ["Yutori research unavailable."],
            "competitors": []
        }
