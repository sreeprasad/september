import requests
import json
import time
import sys

def verify_cached_end_to_end():
    print("--- Running Cached End-to-End Verification ---")
    
    base_url = "http://localhost:8000/api/briefing"
    
    # Use cached profile URL
    target_url = "https://linkedin.com/in/dhruvbatra"
    
    print(f"\n[Step 1] Requesting Cached Profile: {target_url}")
    start_time = time.time()
    try:
        response = requests.post(f"{base_url}/generate", json={
            "linkedin_url": target_url,
            "meeting_context": "Demo Run"
        })
        
        if response.status_code == 200:
            data = response.json()
            duration = time.time() - start_time
            print(f"SUCCESS: Cache hit returned in {duration:.2f}s")
            
            # Verify it matches our cached data structure
            if data.get("person", {}).get("name") == "Dhruv Batra":
                print("Verification: Correct profile returned (Dhruv Batra)")
            else:
                print(f"FAILURE: Unexpected profile: {data.get('person', {}).get('name')}")
                
            print(f"Themes: {list(data.get('themes', {}).get('frequency_breakdown', {}).keys())}")
        else:
            print(f"FAILURE: Request failed (Status {response.status_code})")
            print(response.text)
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("FAILURE: Connection refused. Is the API server running?")
        sys.exit(1)

    # 2. Download PDF
    print("\n[Step 2] Downloading PDF for Cached Profile...")
    try:
        download_response = requests.post(f"{base_url}/download", json={
            "briefing_id": "dhruv_id" 
        })
        
        if download_response.status_code == 200:
            content_length = len(download_response.content)
            print(f"SUCCESS: PDF downloaded ({content_length} bytes)")
            
            with open("dhruv_briefing.pdf", "wb") as f:
                f.write(download_response.content)
            print("Saved to dhruv_briefing.pdf")
        else:
            print(f"FAILURE: Download failed (Status {download_response.status_code})")
            
    except Exception as e:
        print(f"FAILURE: Download error: {e}")

if __name__ == "__main__":
    verify_cached_end_to_end()
