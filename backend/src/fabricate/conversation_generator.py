from typing import List, Dict, Any

class MockConversationGenerator:
    """
    Uses Fabricate to generate contextual mock conversations.
    Novel use case: Not generating test data, but generating
    conversation PREPARATION based on real profile intelligence.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def generate_likely_questions(
        self,
        profile_data: Dict[str, Any],
        meeting_context: str
    ) -> List[Dict[str, Any]]:
        """
        Generate questions the person is likely to ask using LLM.
        """
        name = profile_data.get('name', 'They')
        role = profile_data.get('role', 'Professional')
        company = profile_data.get('company', 'their company')
        
        if not self.llm_client:
            # Fallback to templates if no LLM client
            return [
                {
                    "question": f"Given your work in {meeting_context}, how do you see this aligning with our roadmap?",
                    "why_likely": f"As a {role}, {name} focuses on strategic alignment.",
                    "response_strategy": "Highlight shared goals and long-term vision.",
                    "follow_up_questions": ["What are the key milestones?", "How do we measure success?"]
                }
            ]

        prompt = f"""
        You are an expert negotiation coach. Based on the following profile, generate 3 likely questions this person would ask in a "{meeting_context}" meeting.

        Profile:
        Name: {name}
        Role: {role}
        Company: {company}
        Professional Identity: {profile_data.get('professional_identity', 'Unknown')}
        
        Return valid JSON in this format:
        [
            {{
                "question": "The question",
                "why_likely": "Reasoning based on their role/background",
                "response_strategy": "Brief strategy tip",
                "follow_up_questions": ["Follow up 1", "Follow up 2"]
            }}
        ]
        """

        try:
            message = self.llm_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text
            # Simple JSON parsing (in production, use robust parser)
            import json
            
            # extract json part if wrapped in code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                 response_text = response_text.split("```")[1].split("```")[0]
                 
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating questions with LLM: {e}")
            # Fallback
            return [
                {
                    "question": f"Can you tell me more about your proposal for {company}?",
                    "why_likely": "Standard opening question.",
                    "response_strategy": "Focus on value.",
                    "follow_up_questions": []
                }
            ]

    async def generate_pitch_simulation(
        self,
        profile_data: Dict[str, Any],
        your_pitch: str
    ) -> List[Dict[str, Any]]:
        """
        Generate a simulated back-and-forth conversation using LLM.
        """
        name = profile_data.get('name', 'Partner')
        role = profile_data.get('role', 'Professional')
        
        if not self.llm_client:
             # Fallback
             return []

        prompt = f"""
        Simulate a realistic dialogue between "You" (the pitcher) and "{name}" ({role}).
        The pitch starts with: "{your_pitch}"
        
        Generate a 4-turn exchange (2 responses each).
        
        Return valid JSON:
        [
            {{"speaker": "You", "message": "...", "context": "..."}},
            {{"speaker": "{name}", "message": "...", "context": "..."}}
        ]
        """
        
        try:
            message = self.llm_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = message.content[0].text
            import json
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                 response_text = response_text.split("```")[1].split("```")[0]
            return json.loads(response_text)
        except Exception as e:
             print(f"Error generating simulation: {e}")
             return []

