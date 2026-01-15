from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Engagement(BaseModel):
    likes: int
    comments: int

class Post(BaseModel):
    content: str
    date: str
    engagement: Engagement
    priority_score: float
    priority_reason: str

class Profile(BaseModel):
    name: str
    headline: str
    current_role: str
    company: str
    location: str
    connections: Optional[int] = None

class Funding(BaseModel):
    stage: Optional[str] = None
    amount: Optional[str] = None

class CompanyContext(BaseModel):
    name: str
    industry: Optional[str] = None
    funding: Optional[Funding] = None
    recent_news: List[str] = []
    competitors: List[str] = []

class DecisionMetadata(BaseModel):
    total_data_points_found: int
    data_points_surfaced: int
    decision_rationale: List[str]

class NavigatorOutput(BaseModel):
    profile: Profile
    posts: List[Post]
    company_context: CompanyContext
    decision_metadata: DecisionMetadata
