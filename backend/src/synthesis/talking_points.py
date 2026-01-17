from typing import List, Dict, Any

class TalkingPointsGenerator:
    """
    Generate contextual, personalized talking points using LLM.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def generate(self, themes: Dict[str, Any], person_type: str, context: str, profile_name: str = "Candidate") -> List[Dict[str, Any]]:
        """
        Generate 3 talking points with reasoning.
        """
        talking_points = []
        
        theme_list = []
        if isinstance(themes, dict):
             # Handle structure from ThemeIdentificationEngine
             theme_list.append(themes.get("primary"))
             theme_list.extend(themes.get("secondary", []))
        
        # Limit to top 3 unique themes, filtering None
        top_themes = [t for t in theme_list if t][:3]
        themes_str = ", ".join([str(t) for t in top_themes])

        if not self.llm_client:
             # Fallback
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

        # LLM Generation
        prompt = f"""
        Generate 3 strategic talking points for a meeting with {profile_name}.
        Meeting Context: {context}
        Person Archetype: {person_type}
        Identified Themes in their content: {themes_str}

        For each talking point, provide:
        1. The Point (Actionable topic)
        2. Context (Why it matters)
        3. Why Selected (Connection to their profile)
        4. Conversation Opener (A natural question/statement)
        5. Expected Reaction (How they might respond)

        Return valid JSON:
        [
            {{
                "point": "...",
                "context": "...",
                "why_selected": "...",
                "conversation_opener": "...",
                "expected_reaction": "..."
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
            import json
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                 response_text = response_text.split("```")[1].split("```")[0]
            talking_points = json.loads(response_text)
        except Exception as e:
            print(f"Error generating talking points: {e}")
            # Fallback
            for i, theme in enumerate(top_themes):
                point = {
                    "point": f"Discuss perspectives on {theme}",
                    "context": "Key area of interest.",
                    "why_selected": "High engagement topic.",
                    "conversation_opener": f"What's your take on {theme}?",
                    "expected_reaction": "Engagement.",
                }
                talking_points.append(point)

        return talking_points


    def adapt_to_person_type(self, points: List[Dict[str, Any]], person_type: str) -> List[Dict[str, Any]]:
        """
        Adjust talking points based on person type.
        """
        # Placeholder for further adaptation logic
        return points
