from typing import Dict, Any, List

class ConversationScenarioBuilder:
    """
    Build complete conversation scenarios for different contexts.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def build_scenarios(
        self,
        profile_data: Dict[str, Any],
        meeting_contexts: List[str] = None
    ) -> Dict[str, Any]:
        """
        Build multiple conversation scenarios.
        """
        contexts = meeting_contexts or [
            "first_meeting",
            "pitch",
            "advice_seeking",
            "partnership"
        ]

        scenarios = {}

        for context in contexts:
            scenario = await self._build_single_scenario(profile_data, context)
            scenarios[context] = scenario

        return scenarios

    async def _build_single_scenario(
        self,
        profile_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """
        Build a single conversation scenario using LLM.
        """
        name = profile_data.get('name', 'They')
        role = profile_data.get('role', 'Professional')
        company = profile_data.get('company', 'their company')
        
        if not self.llm_client:
            # Fallback
            return {
                "context": context,
                "likely_opener": f"Thanks for meeting. I'm interested to hear about your work in {context}.",
                "questions_they_might_ask": ["Can you elaborate?", "How does this apply to us?"],
                "topics_to_avoid": ["Politics", "Competitors"],
                "topics_to_lean_into": ["Innovation", "Efficiency"],
                "sample_dialogue": [
                    {"speaker": "You", "message": "Hi, thanks for the time."},
                    {"speaker": name, "message": "Glad to meet you."}
                ]
            }

        prompt = f"""
        Generate a conversation scenario for a "{context}" meeting with:
        Name: {name}
        Role: {role}
        Company: {company}
        
        Return valid JSON:
        {{
            "context": "{context}",
            "likely_opener": "A good opening line for You",
            "questions_they_might_ask": ["Q1", "Q2"],
            "topics_to_avoid": ["Topic 1", "Topic 2"],
            "topics_to_lean_into": ["Topic 1", "Topic 2"],
            "sample_dialogue": [
                {{"speaker": "You", "message": "..."}},
                {{"speaker": "{name}", "message": "..."}}
            ]
        }}
        """

        try:
            message = self.llm_client.messages.create(
                model="claude-sonnet-4-5",
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
            print(f"Error generating scenario: {e}")
            return {
                "context": context,
                "likely_opener": "Hello.",
                "questions_they_might_ask": [],
                "topics_to_avoid": [],
                "topics_to_lean_into": [],
                "sample_dialogue": []
            }

