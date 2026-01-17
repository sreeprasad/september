from typing import List, Dict, Any
from .tonic_client import FabricateClient

class MockConversationGenerator:
    """
    Uses Fabricate to generate contextual mock conversations.
    Novel use case: Not generating test data, but generating
    conversation PREPARATION based on real profile intelligence.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.fabricate_client = FabricateClient()

    async def generate_likely_questions(
        self,
        profile_data: Dict[str, Any],
        meeting_context: str
    ) -> List[Dict[str, Any]]:
        """
        Generate questions the person is likely to ask using Tonic Fabricate or LLM fallback.
        """
        name = profile_data.get('name', 'They')
        role = profile_data.get('role', 'Professional')
        company = profile_data.get('company', 'their company')
        
        # Try Tonic Fabricate first
        prompt = f"""
        Generate 3 likely questions this person would ask in a "{meeting_context}" meeting.
        
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
        
        fabricate_result = self.fabricate_client.generate(prompt)

        # #region agent log
        import json, time
        try:
            with open("/Users/nihalnihalani/Desktop/Github/Orchestrator/.cursor/debug.log", "a") as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"verify-sponsors","hypothesisId":"tonic-fallback","timestamp":int(time.time()*1000),"message":"Questions: Tonic vs Fallback","data":{"fabricate_success": bool(fabricate_result)}})+"\n")
        except: pass
        # #endregion

        if fabricate_result:
            # Tonic might return a list directly or a wrapped response depending on API
            # Assuming client returns list based on our implementation
            if isinstance(fabricate_result, list):
                return fabricate_result
            elif isinstance(fabricate_result, dict) and "data" in fabricate_result:
                 return fabricate_result["data"]
                 
        # Fallback to LLM if Fabricate fails or is not configured
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
        Generate a simulated back-and-forth conversation using Tonic Fabricate or LLM fallback.
        """
        name = profile_data.get('name', 'Partner')
        role = profile_data.get('role', 'Professional')
        
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
        
        # Try Tonic Fabricate first
        fabricate_result = self.fabricate_client.generate(prompt)

        # #region agent log
        import json, time
        try:
            with open("/Users/nihalnihalani/Desktop/Github/Orchestrator/.cursor/debug.log", "a") as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"verify-sponsors","hypothesisId":"tonic-fallback","timestamp":int(time.time()*1000),"message":"Pitch: Tonic vs Fallback","data":{"fabricate_success": bool(fabricate_result)}})+"\n")
        except: pass
        # #endregion

        if fabricate_result:
             if isinstance(fabricate_result, list):
                return fabricate_result
             elif isinstance(fabricate_result, dict) and "data" in fabricate_result:
                 return fabricate_result["data"]

        # Fallback to LLM
        if not self.llm_client:
             # Fallback
             return [
                {
                    "speaker": "You",
                    "message": your_pitch,
                    "context": "Opening pitch"
                },
                {
                    "speaker": name,
                    "message": "That sounds interesting. How does it specifically address our current challenges?",
                    "context": "Probing for relevance"
                },
                {
                    "speaker": "You",
                    "message": "It addresses them by streamlining your workflow and providing actionable insights.",
                    "context": "Direct answer"
                },
                {
                    "speaker": name,
                    "message": "I see. And what kind of resources would be required on our end?",
                    "context": "Evaluating feasibility"
                }
            ]
        
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

