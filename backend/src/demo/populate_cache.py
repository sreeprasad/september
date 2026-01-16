import asyncio
import json
import os
import sys

# Ensure we can import from src
# Add backend directory to path (parent of src)
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_path)

from src.demo.cache_manager import CacheManager

def populate_cache():
    print("--- Populating Demo Cache ---")
    cache_manager = CacheManager()
    
    # Profile 1: Executive (Dhruv Batra)
    dhruv_data = {
        "person": {
            "name": "Dhruv Batra",
            "role": "Founder & CEO",
            "company": "Yutori",
            "professional_identity": "AI Visionary & Entrepreneur",
            "photo_url": "https://media.licdn.com/dms/image/v2/D5603AQHZq7q8q8q8qA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1700000000000?e=1700000000&v=beta&t=xxxxxxxx" # Placeholder
        },
        "themes": {
            "primary": "Autonomous Agents",
            "secondary": ["Web Navigation", "AI Research"],
            "frequency_breakdown": {
                "Autonomous Agents": 0.50,
                "Web Navigation": 0.30,
                "AI Research": 0.20
            }
        },
        "talking_points": [
            {
                "point": "Discuss the future of web agents",
                "context": "Aligns with Yutori's mission",
                "why_selected": "Core business focus"
            },
            {
                "point": "Scaling reinforcement learning",
                "context": "Technical challenge relevant to Navigator",
                "why_selected": "Recent technical posts"
            },
            {
                "point": "Partnership opportunities for agent ecosystem",
                "context": "Strategic growth area",
                "why_selected": "Executive priority"
            }
        ],
        "key_insights": [
            {"insight": "Heavily focused on 'pixels to actions' paradigm", "confidence": 0.95}
        ],
        "reasoning_chain": [
            {"decision": "Selected 'Web Agents' as primary theme", "reason": "90% of content relates to Navigator", "confidence": 0.99}
        ],
        "mock_conversations": {
            "likely_questions": [
                {
                    "question": "How does your solution handle dynamic DOM changes?",
                    "why_likely": "Core technical challenge for Yutori",
                    "response_strategy": "Explain our adaptive selectors..."
                }
            ],
            "pitch_simulation": [],
            "conversation_scenarios": {}
        },
        "company_context": {
            "name": "Yutori",
            "recent_developments": ["Launched Navigator", "Seed Funding"],
            "relevance_score": 0.99
        },
        "sentiment": {
            "communication_style": "Visionary and technical",
            "passion_topics": ["AGI", "Browser Automation"]
        }
    }
    
    # Profile 2: Engineer (Backup)
    engineer_data = {
        "person": {
            "name": "Alex Chen",
            "role": "Senior Staff Engineer",
            "company": "Anthropic",
            "professional_identity": "Systems Architect",
            "photo_url": ""
        },
        "themes": {
            "primary": "System Design",
            "secondary": ["Rust", "Distributed Systems"],
            "frequency_breakdown": {
                "System Design": 0.40,
                "Rust": 0.35,
                "Distributed Systems": 0.25
            }
        },
        "talking_points": [
            {"point": "Optimizing inference latency", "context": "Relevant to recent work", "why_selected": "Technical depth"},
            {"point": "Rust vs C++ for ML infra", "context": "Ongoing debate", "why_selected": "High engagement topic"},
            {"point": "Scaling reliable systems", "context": "Core responsibility", "why_selected": "Role alignment"}
        ],
        "mock_conversations": {
            "likely_questions": [
                {"question": "What are your p99 latency requirements?", "why_likely": "Focus on performance", "response_strategy": "Provide specific benchmarks..."}
            ],
            "pitch_simulation": [],
            "conversation_scenarios": {}
        },
        "company_context": {
            "name": "Anthropic",
            "recent_developments": ["Claude 3.5 Sonnet Release"],
            "relevance_score": 0.90
        },
        "sentiment": {
            "communication_style": "Precise and data-driven",
            "passion_topics": ["Reliability", "Performance"]
        }
    }

    # Save to cache
    print("Caching Dhruv Batra...")
    cache_manager.save_to_cache("https://linkedin.com/in/dhruvbatra", dhruv_data)
    
    print("Caching Alex Chen (Backup)...")
    cache_manager.save_to_cache("https://linkedin.com/in/alexc", engineer_data)
    
    print("SUCCESS: Demo cache populated.")

if __name__ == "__main__":
    populate_cache()
