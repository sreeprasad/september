from typing import Dict, Any

class QuestionTemplates:
    """
    Templates for generating relevant questions by person type.
    """

    QUESTION_FRAMEWORKS = {
        "executive": {
            "categories": ["strategic_impact", "roi", "team_resources", "timeline"],
            "style": "high-level, outcome-focused",
            "typical_concerns": ["budget", "team capacity", "strategic fit"]
        },
        "engineer": {
            "categories": ["technical_architecture", "scalability", "integration", "maintenance"],
            "style": "detailed, specific examples",
            "typical_concerns": ["tech debt", "complexity", "team expertise"]
        },
        "investor": {
            "categories": ["market_size", "traction", "team", "competition", "unit_economics"],
            "style": "metrics-driven, thesis-validation",
            "typical_concerns": ["defensibility", "growth rate", "capital efficiency"]
        },
        "designer": {
            "categories": ["user_research", "design_process", "iteration", "metrics"],
            "style": "user-centric, process-oriented",
            "typical_concerns": ["user needs", "design debt", "team collaboration"]
        }
    }

    def get_question_framework(self, person_type: str, themes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get question generation framework based on person type and themes.
        """
        base_framework = self.QUESTION_FRAMEWORKS.get(
            person_type,
            self.QUESTION_FRAMEWORKS["executive"]
        )

        # In a real app, we would customize based on themes here
        # For now, return the base framework
        return base_framework
