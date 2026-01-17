import json
from typing import Dict, Any, List
from .person_classifier import PersonTypeClassifier
from .talking_points import TalkingPointsGenerator
from .reasoning_chain import ReasoningChainGenerator

class AdaptiveSynthesisPipeline:
    """
    Dynamically generates synthesis logic based on person type.
    """

    def __init__(self, llm_client=None):
        self.classifier = PersonTypeClassifier()
        self.tp_generator = TalkingPointsGenerator(llm_client=llm_client)
        self.reasoning_generator = ReasoningChainGenerator()

    async def synthesize(self, extracted_data: Dict[str, Any], meeting_context: str) -> Dict[str, Any]:
        """
        Run adaptive synthesis pipeline.
        """
        if extracted_data is None:
            extracted_data = {}
        if meeting_context is None:
            meeting_context = "General meeting"

        # Step 1: Classify Person Type
        # We need to flatten the extracted data structure a bit or pass the relevant parts
        # extracted_data structure from Phase 2: { "person": {...}, "themes": {...}, ... }
        profile_data = extracted_data.get("person", {})
        person_type = self.classifier.classify(profile_data)
        
        # Get synthesis config (focus areas, style)
        config = self.classifier.get_synthesis_config(person_type)
        
        # Step 2: Generate Talking Points
        themes = extracted_data.get("themes", {})
        talking_points = await self.tp_generator.generate(themes, person_type, meeting_context, profile_name=profile_data.get("name", "Candidate"))
        
        # Step 3: Generate Reasoning Chain
        reasoning_chain = self.reasoning_generator.generate_chain(talking_points)
        
        # Step 4: Construct Output
        result = {
            "person_type": person_type,
            "synthesis_config": {
                "focus_areas": config["focus"],
                "talking_point_style": config["talking_point_style"]
            },
            "talking_points": talking_points,
            "key_insights": extracted_data.get("insights", []),
            "reasoning_chain": reasoning_chain,
            "briefing_summary": f"Briefing prepared for {profile_data.get('name')} ({person_type}). Focus on {', '.join(config['focus'])}."
        }
        
        return result
