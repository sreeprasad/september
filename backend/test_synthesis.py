import asyncio
import json
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.synthesis.adaptive_pipeline import AdaptiveSynthesisPipeline

async def verify_synthesis():
    print("--- Testing Adaptive Synthesis Pipeline ---")
    
    pipeline = AdaptiveSynthesisPipeline()
    
    # Mock data simulating input from Phase 2
    mock_input_executive = {
        "person": {
            "name": "Jane Doe",
            "role": "Chief Technology Officer",
            "company": "TechCorp"
        },
        "themes": {
            "primary": "AI Strategy",
            "secondary": ["Digital Transformation", "Cloud Infrastructure"],
            "frequency_breakdown": {}
        }
    }
    
    mock_input_engineer = {
        "person": {
            "name": "John Smith",
            "role": "Senior Software Engineer",
            "company": "DevTools Inc"
        },
        "themes": {
            "primary": "Rust Programming",
            "secondary": ["WebAssembly", "Performance Optimization"],
            "frequency_breakdown": {}
        }
    }
    
    context = "introductory partnership meeting"
    
    print("\n[Test Case 1: Executive]")
    result_exec = await pipeline.synthesize(mock_input_executive, context)
    print(f"Detected Type: {result_exec['person_type']}")
    print(f"Focus Areas: {result_exec['synthesis_config']['focus_areas']}")
    print(f"Talking Points: {len(result_exec['talking_points'])}")
    print(f"Reasoning Chain: {len(result_exec['reasoning_chain'])}")
    
    print("\n[Test Case 2: Engineer]")
    result_eng = await pipeline.synthesize(mock_input_engineer, context)
    print(f"Detected Type: {result_eng['person_type']}")
    print(f"Focus Areas: {result_eng['synthesis_config']['focus_areas']}")
    
    # Validation
    if result_exec['person_type'] == 'executive' and result_eng['person_type'] == 'engineer':
        print("\nSUCCESS: Classification working correctly.")
    else:
        print("\nFAILURE: Classification mismatch.")
        
    if len(result_exec['talking_points']) > 0 and len(result_exec['reasoning_chain']) > 0:
         print("SUCCESS: Content generation working.")
    else:
         print("FAILURE: Content generation empty.")

if __name__ == "__main__":
    asyncio.run(verify_synthesis())
