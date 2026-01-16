import asyncio
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.fabricate.conversation_generator import MockConversationGenerator
from src.fabricate.response_coach import ResponseCoach
from src.fabricate.scenario_builder import ConversationScenarioBuilder

async def verify_fabricate():
    print("--- Testing Tonic Fabricate Mock Generation ---")

    mock_generator = MockConversationGenerator()
    response_coach = ResponseCoach()
    scenario_builder = ConversationScenarioBuilder()

    profile_data = {
        "name": "Jane Doe",
        "role": "CTO",
        "themes": {"passion_topics": ["AI", "Security"]}
    }
    context = "introductory meeting"

    print("\n[Test 1: Likely Questions]")
    questions = await mock_generator.generate_likely_questions(profile_data, context)
    print(f"Generated {len(questions)} questions.")
    print(f"First question: {questions[0]['question']}")

    print("\n[Test 2: Response Coaching]")
    strategies = await response_coach.generate_response_strategies(questions, profile_data)
    print(f"Generated {len(strategies)} strategies.")
    print(f"Strategy for Q1: {strategies[0]['response_framework']}")

    print("\n[Test 3: Pitch Simulation]")
    simulation = await mock_generator.generate_pitch_simulation(profile_data, "My Pitch")
    print(f"Generated {len(simulation)} messages.")

    print("\n[Test 4: Scenario Builder]")
    scenarios = await scenario_builder.build_scenarios(profile_data)
    print(f"Generated {len(scenarios)} scenarios: {list(scenarios.keys())}")
    
    if len(questions) > 0 and len(strategies) > 0 and len(scenarios) > 0:
        print("\nSUCCESS: Fabricate mock generation working correctly.")
    else:
        print("\nFAILURE: Missing data in generation.")

if __name__ == "__main__":
    asyncio.run(verify_fabricate())
