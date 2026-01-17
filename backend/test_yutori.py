import asyncio
import os
import json
import requests
import time
from yutori import YutoriClient
from dotenv import load_dotenv

load_dotenv()

async def test_yutori():
    print("Testing Yutori SDK...")
    
    api_key = os.getenv("YUTORI_API_KEY")
    if not api_key:
        print("Error: YUTORI_API_KEY not found in environment.")
        return

    client = YutoriClient(api_key=api_key)
    
    # Simple research prompt
    prompt = "Research the latest news about OpenAI and summarize 2 key recent events."
    
    print(f"Sending prompt: {prompt}")
    
    try:
        # Attempt 1: agent_run (Browsing)
        # This endpoint queues a task on Yutori's cloud browser.
        payload = {
            "task": prompt,
            "start_url": "https://www.google.com" 
        }
        
        print("Starting agent_run task...")
        result = client.agent_run(payload)
        print("Task created:", json.dumps(result, indent=2))
        
        task_id = result.get("task_id")
        if task_id:
            print(f"Polling task {task_id}...")
            # Guessing endpoint: GET /v1/browsing/tasks/{task_id}
            # The base URL is likely the same as client.base_url
            base_url = client.base_url # e.g., https://api.yutori.com/v1
            
            headers = {"x-api-key": api_key, "Content-Type": "application/json"}
            
            for _ in range(10): # Poll for a bit
                resp = requests.get(f"{base_url}/browsing/tasks/{task_id}", headers=headers)
                if resp.status_code == 200:
                    task_data = resp.json()
                    status = task_data.get("status")
                    print(f"Status: {status}")
                    
                    if status in ["completed", "success"]:
                        print("Task finished!")
                        print(json.dumps(task_data, indent=2))
                        break
                    elif status == "failed":
                        print("Task failed!")
                        print(json.dumps(task_data, indent=2))
                        break
                else:
                    print(f"Poll failed: {resp.status_code} - {resp.text}")
                
                time.sleep(2)
        
    except Exception as e:
        print(f"Error calling Yutori: {e}")

if __name__ == "__main__":
    asyncio.run(test_yutori())
