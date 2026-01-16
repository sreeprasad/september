from typing import List, Dict, Any

class ResponseCoach:
    """
    Generate suggested responses and coaching tips.
    """

    async def generate_response_strategies(
        self,
        questions: List[Dict[str, Any]],
        profile_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        For each likely question, generate response strategies.
        """
        strategies = []

        for question in questions:
            strategy = {
                "question": question["question"],
                "response_framework": "Acknowledge -> Bridge -> Pivot",
                "emphasize": ["Value", "Alignment"],
                "avoid": ["Defensiveness", "Over-promising"],
                "pivot_options": ["Let's discuss the long-term view", "Have you seen our case studies?"],
                "follow_up_prepared": ["Does that address your concern?", "What are your thoughts on that approach?"]
            }
            strategies.append(strategy)

        return strategies
