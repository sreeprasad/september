from typing import List, Dict, Any

class MockConversationGenerator:
    """
    Uses Fabricate to generate contextual mock conversations.
    Novel use case: Not generating test data, but generating
    conversation PREPARATION based on real profile intelligence.
    """

    def __init__(self, fabricate_client=None):
        self.fabricate = fabricate_client

    async def generate_likely_questions(
        self,
        profile_data: Dict[str, Any],
        meeting_context: str
    ) -> List[Dict[str, Any]]:
        """
        Generate questions the person is likely to ask.
        """
        # In a real implementation, we would call the Fabricate API.
        # For this demo, we mock the response based on inputs.
        
        name = profile_data.get('name', 'They')
        role = profile_data.get('role', 'Professional')
        
        # Simple template-based generation based on context
        questions = [
            {
                "question": f"Given your work in {meeting_context}, how do you see this aligning with our roadmap?",
                "why_likely": f"As a {role}, {name} focuses on strategic alignment.",
                "response_strategy": "Highlight shared goals and long-term vision.",
                "follow_up_questions": ["What are the key milestones?", "How do we measure success?"]
            },
            {
                "question": "What are the technical challenges you anticipate?",
                "why_likely": "Based on their technical background.",
                "response_strategy": "Be transparent about risks but have mitigation plans ready.",
                "follow_up_questions": ["Have you considered scaling issues?", "What about security compliance?"]
            },
            {
                "question": "How does this compare to existing solutions in the market?",
                "why_likely": "Standard due diligence question.",
                "response_strategy": "Focus on unique value proposition and specific differentiators.",
                "follow_up_questions": ["Who do you see as the main competitor?", "What is your moat?"]
            }
        ]
        return questions

    async def generate_pitch_simulation(
        self,
        profile_data: Dict[str, Any],
        your_pitch: str
    ) -> List[Dict[str, Any]]:
        """
        Generate a simulated back-and-forth conversation.
        """
        name = profile_data.get('name', 'Partner')
        
        simulation = [
            {
                "speaker": "You",
                "message": your_pitch,
                "context": "Opening pitch"
            },
            {
                "speaker": name,
                "message": "That sounds interesting. How does it specifically address [Specific Pain Point]?",
                "context": "Probing for relevance"
            },
            {
                "speaker": "You",
                "message": "It addresses [Specific Pain Point] by [Solution Mechanism].",
                "context": "Direct answer"
            },
            {
                "speaker": name,
                "message": "I see. And what kind of resources would be required on our end?",
                "context": "Evaluating feasibility"
            },
             {
                "speaker": "You",
                "message": "Minimal resources. We handle the heavy lifting via...",
                "context": "Reassurance"
            }
        ]
        return simulation
