from typing import List, Dict, Any

class TalkingPointsGenerator:
    """
    Generate contextual, personalized talking points.
    """

    async def generate(self, themes: Dict[str, Any], person_type: str, context: str) -> List[Dict[str, Any]]:
        """
        Generate 3 talking points with reasoning.
        """
        talking_points = []
        
        # We'll use the themes identified in Phase 2
        # In a real implementation with LLM, we would generate these dynamically
        # For now, we'll template them based on the themes and person type
        
        theme_list = []
        if isinstance(themes, dict):
             # Handle structure from ThemeIdentificationEngine
             # Structure: { "primary": "...", "secondary": [...], "frequency_breakdown": {...} }
             theme_list.append(themes.get("primary"))
             theme_list.extend(themes.get("secondary", []))
        
        # Limit to top 3 unique themes, filtering None
        top_themes = [t for t in theme_list if t][:3]
        
        for i, theme in enumerate(top_themes):
            point = {
                "point": f"Discuss approach to {theme}",
                "context": f"Relevant to their interest in {theme} and your meeting about {context}",
                "why_selected": f"High engagement topic for this {person_type}",
                "conversation_opener": f"I noticed you've been writing a lot about {theme} lately...",
                "expected_reaction": "Likely to share strong opinions and recent experiences",
            }
            talking_points.append(point)
            
        return talking_points

    def adapt_to_person_type(self, points: List[Dict[str, Any]], person_type: str) -> List[Dict[str, Any]]:
        """
        Adjust talking points based on person type.
        """
        # Placeholder for further adaptation logic
        return points
