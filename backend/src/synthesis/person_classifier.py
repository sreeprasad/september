from typing import Dict, Any

class PersonTypeClassifier:
    """
    Classify person type to adapt synthesis pipeline.
    
    Cline doesn't just write code—it adapts the analysis 
    pipeline to the person type.
    """

    PERSON_TYPES = {
        "executive": {
            "focus": ["strategy", "business_impact", "leadership"],
            "talking_point_style": "high-level, outcome-focused",
            "mock_conversation_depth": "strategic"
        },
        "engineer": {
            "focus": ["technical_depth", "architecture", "tools"],
            "talking_point_style": "technical, specific examples",
            "mock_conversation_depth": "detailed implementation"
        },
        "designer": {
            "focus": ["user_experience", "aesthetics", "process"],
            "talking_point_style": "visual, user-centric",
            "mock_conversation_depth": "design rationale"
        },
        "founder": {
            "focus": ["vision", "traction", "team"],
            "talking_point_style": "story-driven, ambitious",
            "mock_conversation_depth": "vision and execution"
        },
        "investor": {
            "focus": ["market_size", "differentiation", "team"],
            "talking_point_style": "metrics-driven, thesis-aligned",
            "mock_conversation_depth": "due diligence"
        }
    }

    def classify(self, profile_data: Dict[str, Any]) -> str:
        """
        Classify person type based on role, themes, and content.
        """
        if profile_data is None:
            profile_data = {}

        role = profile_data.get("role", "")
        if role is None:
            role = ""
        role = role.lower()
        
        company_context = profile_data.get("company_context", {})
        
        # Heuristic based classification
        if any(keyword in role for keyword in ["ceo", "cto", "cpo", "vp", "director", "head of", "chief"]):
            return "executive"
        elif any(keyword in role for keyword in ["engineer", "developer", "architect", "programmer"]):
            return "engineer"
        elif any(keyword in role for keyword in ["designer", "ux", "ui", "creative", "artist"]):
            return "designer"
        elif any(keyword in role for keyword in ["founder", "co-founder", "owner"]):
            return "founder"
        elif any(keyword in role for keyword in ["investor", "partner", "vc", "angel"]):
            return "investor"
            
        # Default fallback
        return "executive"

    def get_synthesis_config(self, person_type: str) -> Dict[str, Any]:
        """
        Return synthesis configuration for person type.
        """
        return self.PERSON_TYPES.get(person_type, self.PERSON_TYPES["executive"])
