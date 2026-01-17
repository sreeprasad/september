import requests
import json
import time
import sys

def verify_end_to_end():
    print("--- Running End-to-End Verification ---")
    
    base_url = "http://localhost:8000/api/briefing"
    
    # 1. Generate Briefing
    print("\n[Step 1] Generating Briefing...")
    start_time = time.time()
    try:
        response = requests.post(f"{base_url}/generate", json={
            "linkedin_url": "https://www.linkedin.com/in/sreeprasadatrit/",
            "twitter_url": "https://twitter.com/janedoe",
            "meeting_context": "End-to-end test run"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Generation complete in {time.time() - start_time:.2f}s")
            print(f"Person: {data.get('person', {}).get('name')}")
            print(f"Themes: {list(data.get('themes', {}).get('frequency_breakdown', {}).keys())}")
            print(f"Talking Points: {len(data.get('talking_points', []))}")
            print(f"Mock Scenarios: {len(data.get('mock_conversations', {}).get('conversation_scenarios', {}))}")
        else:
            print(f"FAILURE: Generation failed (Status {response.status_code})")
            print(response.text)
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("FAILURE: Connection refused. Is the API server running?")
        sys.exit(1)

    # 2. Download PDF
    print("\n[Step 2] Downloading PDF...")
    start_time = time.time()
    try:
        # In a real scenario, we'd pass the ID from step 1
        download_response = requests.post(f"{base_url}/download", json={
            "briefing_id": "test_id",
            "linkedin_url": "https://www.linkedin.com/in/sreeprasadatrit/"
        })
        
        if download_response.status_code == 200:
            content_length = len(download_response.content)
            print(f"SUCCESS: PDF downloaded in {time.time() - start_time:.2f}s ({content_length} bytes)")
            
            with open("e2e_result.pdf", "wb") as f:
                f.write(download_response.content)
            print("Saved to e2e_result.pdf")
        else:
            print(f"FAILURE: Download failed (Status {download_response.status_code})")
            
    except Exception as e:
        print(f"FAILURE: Download error: {e}")

if __name__ == "__main__":
    verify_end_to_end()
