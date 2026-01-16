from typing import Dict, Any, List

class ConversationScenarioBuilder:
    """
    Build complete conversation scenarios for different contexts.
    """

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
        Build a single conversation scenario.
        """
        name = profile_data.get('name', 'They')
        
        # Mocking scenario data
        return {
            "context": context,
            "likely_opener": f"Thanks for meeting. I'm interested to hear about your work in {context}.",
            "questions_they_might_ask": [
                "Can you elaborate on your experience?",
                "How does this apply to our current situation?"
            ],
            "topics_to_avoid": ["Internal politics", "Competitor pricing"],
            "topics_to_lean_into": ["Innovation", "Efficiency"],
            "sample_dialogue": [
                {"speaker": "You", "message": "Hi, thanks for the time."},
                {"speaker": name, "message": "Glad to meet you. What's on your mind?"}
            ]
        }
