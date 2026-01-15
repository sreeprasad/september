from typing import Dict, Any, List
from ..schemas.extraction_output import ExtractionOutput

class StructuredDataTransformer:
    """
    Transform extracted data into clean JSON for downstream processing.
    """

    def transform_to_briefing_format(self, raw_extraction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform semantic extraction into briefing-ready format.

        Input: Raw AgentQL extraction
        Output: Clean JSON matching Cline synthesis requirements
        """
        # This implementation assumes raw_extraction contains keys that map to our desired output.
        # In a real scenario, this would map the AgentQL response structure to our schema.
        
        # Constructing the dictionary as per the plan's requirement
        output = {
            "person": {
                "name": raw_extraction.get("person", {}).get("name", ""),
                "role": raw_extraction.get("person", {}).get("role", ""),
                "company": raw_extraction.get("person", {}).get("company", ""),
                "professional_identity": raw_extraction.get("person", {}).get("professional_identity", ""), 
                "career_trajectory": raw_extraction.get("person", {}).get("career_trajectory", "")
            },
            "themes": {
                "primary": raw_extraction.get("themes", {}).get("primary", ""),
                "secondary": raw_extraction.get("themes", {}).get("secondary", []),
                "frequency_breakdown": raw_extraction.get("themes", {}).get("frequency_breakdown", {}),
            },
            "sentiment": {
                "overall": raw_extraction.get("sentiment", {}).get("overall", ""),
                "passion_topics": raw_extraction.get("sentiment", {}).get("passion_topics", []),
                "concerns": raw_extraction.get("sentiment", {}).get("concerns", []),
                "communication_style": raw_extraction.get("sentiment", {}).get("communication_style", ""),
            },
            "insights": raw_extraction.get("insights", []),
            "company_context": {
                "name": raw_extraction.get("company_context", {}).get("name", ""),
                "relevance_score": raw_extraction.get("company_context", {}).get("relevance_score", 0.0),
                "key_facts": raw_extraction.get("company_context", {}).get("key_facts", []),
                "recent_developments": raw_extraction.get("company_context", {}).get("recent_developments", []),
            },
            "extraction_metadata": {
                "confidence_score": raw_extraction.get("extraction_metadata", {}).get("confidence_score", 0.0),
                "data_quality": raw_extraction.get("extraction_metadata", {}).get("data_quality", ""),
                "extraction_time": raw_extraction.get("extraction_metadata", {}).get("extraction_time", ""),
            }
        }
        
        # Optional: Validate with Pydantic model
        # validated_output = ExtractionOutput(**output)
        # return validated_output.model_dump()
        
        return output
