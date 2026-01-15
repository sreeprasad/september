from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Person(BaseModel):
    name: str = Field(..., description="Full name of the person")
    role: str = Field(..., description="Current job title or role")
    company: str = Field(..., description="Current company")
    professional_identity: str = Field(..., description="Professional identity beyond job title (e.g. 'Developer advocate who prioritizes DX')")
    career_trajectory: Optional[str] = Field(None, description="Brief summary of career path (e.g. 'IC -> Lead -> VP path')")

class Themes(BaseModel):
    primary: str = Field(..., description="The most dominant professional theme")
    secondary: List[str] = Field(default_factory=list, description="Secondary themes")
    frequency_breakdown: Dict[str, float] = Field(default_factory=dict, description="Frequency ratio of each theme (0.0 to 1.0)")

class Sentiment(BaseModel):
    overall: str = Field(..., description="Overall sentiment/tone (e.g. 'positive-enthusiastic')")
    passion_topics: List[str] = Field(default_factory=list, description="Topics the person seems passionate about")
    concerns: List[str] = Field(default_factory=list, description="Topics expressed with concern or frustration")
    communication_style: str = Field(..., description="Description of communication style (e.g. 'direct, technical')")

class Insight(BaseModel):
    insight: str = Field(..., description="Key insight about the person")
    confidence: float = Field(..., description="Confidence score for this insight (0.0 to 1.0)")
    evidence: List[str] = Field(default_factory=list, description="IDs or snippets of posts supporting this insight")

class CompanyContext(BaseModel):
    name: str = Field(..., description="Company name")
    relevance_score: float = Field(..., description="Relevance of company to the user's goals (0.0 to 1.0)")
    key_facts: List[str] = Field(default_factory=list, description="Key facts about the company")
    recent_developments: List[str] = Field(default_factory=list, description="Recent news or developments")

class ExtractionMetadata(BaseModel):
    confidence_score: float = Field(..., description="Overall extraction confidence")
    data_quality: str = Field(..., description="Assessment of input data quality")
    extraction_time: str = Field(..., description="Time taken for extraction")

class ExtractionOutput(BaseModel):
    person: Person
    themes: Themes
    sentiment: Sentiment
    insights: List[Insight] = Field(default_factory=list)
    company_context: Optional[CompanyContext] = None
    extraction_metadata: Optional[ExtractionMetadata] = None
