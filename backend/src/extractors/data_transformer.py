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
        if raw_extraction is None:
            raw_extraction = {}

        # Constructing the dictionary as per the plan's requirement
        # Helper for safe access
        def safe_get(d, keys, default=None):
            if d is None: return default
            for k in keys:
                if d and isinstance(d, dict):
                    d = d.get(k)
                else:
                    return default
            return d if d is not None else default

        output = {
            "person": {
                "name": safe_get(raw_extraction, ["person", "name"], ""),
                "role": safe_get(raw_extraction, ["person", "role"], ""),
                "company": safe_get(raw_extraction, ["person", "company"], ""),
                "professional_identity": safe_get(raw_extraction, ["person", "professional_identity"], ""), 
                "career_trajectory": safe_get(raw_extraction, ["person", "career_trajectory"], "")
            },
            "themes": {
                "primary": safe_get(raw_extraction, ["themes", "primary"], ""),
                "secondary": safe_get(raw_extraction, ["themes", "secondary"], []),
                "frequency_breakdown": safe_get(raw_extraction, ["themes", "frequency_breakdown"], {}),
            },
            "sentiment": {
                "overall": safe_get(raw_extraction, ["sentiment", "overall"], ""),
                "passion_topics": safe_get(raw_extraction, ["sentiment", "passion_topics"], []),
                "concerns": safe_get(raw_extraction, ["sentiment", "concerns"], []),
                "communication_style": safe_get(raw_extraction, ["sentiment", "communication_style"], ""),
            },
            "insights": safe_get(raw_extraction, ["insights"], []),
            "company_context": {
                "name": safe_get(raw_extraction, ["company_context", "name"], ""),
                "relevance_score": safe_get(raw_extraction, ["company_context", "relevance_score"], 0.0),
                "key_facts": safe_get(raw_extraction, ["company_context", "key_facts"], []),
                "recent_developments": safe_get(raw_extraction, ["company_context", "recent_developments"], []),
            },
            "extraction_metadata": {
                "confidence_score": safe_get(raw_extraction, ["extraction_metadata", "confidence_score"], 0.0),
                "data_quality": safe_get(raw_extraction, ["extraction_metadata", "data_quality"], ""),
                "extraction_time": safe_get(raw_extraction, ["extraction_metadata", "extraction_time"], ""),
            }
        }
        
        # Optional: Validate with Pydantic model
        # validated_output = ExtractionOutput(**output)
        # return validated_output.model_dump()
        
        return output
