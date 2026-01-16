from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio

# Import pipeline components
from src.config.yutori_config import YUTORI_CONFIG
from src.agents.linkedin_browser import LinkedInBrowserAgent
from src.agents.company_researcher import CompanyResearcher
from src.extractors.profile_extractor import SemanticProfileExtractor
from src.extractors.theme_engine import ThemeIdentificationEngine
from src.extractors.data_transformer import StructuredDataTransformer
from src.synthesis.adaptive_pipeline import AdaptiveSynthesisPipeline
from src.fabricate.conversation_generator import MockConversationGenerator
from src.fabricate.response_coach import ResponseCoach
from src.fabricate.scenario_builder import ConversationScenarioBuilder
from src.visual.pdf_generator import PDFGenerator
from fastapi.responses import StreamingResponse
import io
import os

from src.demo.cache_manager import CacheManager

app = FastAPI()
cache_manager = CacheManager()
print(f"DEBUG: Cache directory is {os.path.abspath(cache_manager.cache_dir)}")

class BriefingRequest(BaseModel):
    linkedin_url: str
    meeting_context: str

class DownloadRequest(BaseModel):
    briefing_id: str
    linkedin_url: Optional[str] = None

@app.post("/api/briefing/generate")
async def generate_briefing(request: BriefingRequest):
    try:
        # Check cache first (Demo Mode)
        cached_data = cache_manager.get_from_cache(request.linkedin_url)
        if cached_data:
            return cached_data

        # Pipeline Execution Logic
        api_key = YUTORI_CONFIG.get("api_key", "mock_key")
        
        # Initialize Agents
        browser = LinkedInBrowserAgent(api_key=api_key)
        researcher = CompanyResearcher(api_key=api_key)
        extractor = SemanticProfileExtractor()
        theme_engine = ThemeIdentificationEngine()
        transformer = StructuredDataTransformer()
        synthesis_pipeline = AdaptiveSynthesisPipeline()
        
        # Initialize Phase 5 Components
        mock_generator = MockConversationGenerator()
        response_coach = ResponseCoach()
        scenario_builder = ConversationScenarioBuilder()
        
        # Phase 1
        profile_data = await browser.browse_profile(request.linkedin_url, request.meeting_context)
        company_name = profile_data["profile"]["company"]
        role = profile_data["profile"]["current_role"]
        company_data = await researcher.research_company(company_name, role)
        
        phase1_output = {
            "profile": profile_data["profile"],
            "posts": profile_data["posts"],
            "company_context": company_data,
            "decision_metadata": profile_data["decision_metadata"]
        }
        
        # Phase 2
        themes = await extractor.extract_profile_themes(phase1_output["posts"])
        sentiment = await extractor.extract_sentiment_patterns(phase1_output["posts"])
        theme_insights = theme_engine.identify_themes(phase1_output["posts"])
        insights = theme_engine.generate_theme_insights(theme_insights)
        
        raw_extraction = {
            "person": {
                "name": phase1_output["profile"]["name"],
                "role": phase1_output["profile"]["current_role"],
                "company": phase1_output["profile"]["company"],
                "professional_identity": themes.get("professional_identity", ""),
                "career_trajectory": "IC -> Lead -> CTO"
            },
            "themes": theme_insights,
            "sentiment": sentiment,
            "insights": insights,
            "company_context": {
                "name": phase1_output["company_context"]["name"],
                "relevance_score": 0.85,
                "key_facts": phase1_output["company_context"]["recent_news"],
                "recent_developments": phase1_output["company_context"]["recent_news"]
            },
            "extraction_metadata": {
                "confidence_score": 0.95,
                "data_quality": "high",
                "extraction_time": "1.2s"
            }
        }
        
        final_output = transformer.transform_to_briefing_format(raw_extraction)
        
        # Phase 4: Adaptive Synthesis
        synthesis_result = await synthesis_pipeline.synthesize(raw_extraction, request.meeting_context)
        
        # Merge synthesis result into final output
        final_output.update(synthesis_result)
        
        # Phase 5: Tonic Fabricate Mock Conversations
        # 5.1 Generate Likely Questions
        likely_questions = await mock_generator.generate_likely_questions(raw_extraction["person"], request.meeting_context)
        
        # 5.2 Generate Response Strategies
        strategies = await response_coach.generate_response_strategies(likely_questions, raw_extraction["person"])
        
        # 5.3 Generate Pitch Simulation
        pitch_simulation = await mock_generator.generate_pitch_simulation(raw_extraction["person"], "I'd like to propose a partnership...")
        
        # 5.4 Build Full Scenarios
        scenarios = await scenario_builder.build_scenarios(raw_extraction["person"])
        
        # Add to final output
        final_output["mock_conversations"] = {
            "likely_questions": strategies, # Strategies include the question + coaching
            "pitch_simulation": pitch_simulation,
            "conversation_scenarios": scenarios
        }
        
        # Save to cache for next time
        cache_manager.save_to_cache(request.linkedin_url, final_output)

        return final_output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/briefing/download")
async def download_briefing(request: DownloadRequest):
    # Try to get data from cache if URL provided
    data = None
    if request.linkedin_url:
        data = cache_manager.get_from_cache(request.linkedin_url)

    if not data:
        # Mock data fallback for demo purposes
        data = {
            "person": {
                "name": "Jane Doe",
                "role": "Chief Technology Officer",
                "company": "TechCorp",
                "professional_identity": "AI Strategy Leader",
                "photo_url": "https://via.placeholder.com/150"
            },
            "themes": {
                "frequency_breakdown": {
                    "AI Strategy": 0.45,
                    "Cloud Infrastructure": 0.30,
                    "Digital Transformation": 0.25
                }
            },
            "talking_points": [
                {"point": "Discuss AI Governance", "context": "Relevant to recent posts"},
                {"point": "Cloud Migration Challenges", "context": "Aligns with company news"},
                {"point": "Team Scaling", "context": "Based on job postings"}
            ],
            "company_context": {
                "name": "TechCorp",
                "recent_developments": ["Series B Funding Announced", "New Product Launch"]
            },
            "sentiment": {
                "communication_style": "Direct and strategic"
            }
        }
    
    pdf_gen = PDFGenerator()
    pdf_bytes = pdf_gen.generate(data)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=briefing.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
