from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import json
import tempfile
import base64

# Import pipeline components
from src.config.yutori_config import YUTORI_CONFIG
from src.agents.linkedin_browser import LinkedInBrowserAgent
from src.agents.twitter_browser import TwitterBrowserAgent
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
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from anthropic import Anthropic

from src.demo.cache_manager import CacheManager

load_dotenv()

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache_manager = CacheManager()
print(f"DEBUG: Cache directory is {os.path.abspath(cache_manager.cache_dir)}")

# Initialize clients for Call Analyzer
try:
    elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
except Exception as e:
    print(f"Warning: Failed to initialize ElevenLabs client: {e}")
    elevenlabs_client = None

try:
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
except Exception as e:
    print(f"Warning: Failed to initialize Anthropic client: {e}")
    anthropic_client = None

COMPLIANCE_PROMPT = """You are a compliance analyst reviewing call center transcripts for regulatory violations.

Analyze the following transcript and identify any compliance violations.

Check for these specific rules:
1. RECORDING_DISCLOSURE - Agent must inform caller they are being recorded at the start
2. IDENTITY_VERIFICATION - Agent must verify caller's identity before sharing sensitive info
3. NO_PRESSURE_TACTICS - Agent cannot use high-pressure sales language or create false urgency
4. ACCURATE_INFORMATION - Agent cannot make false claims or promises
5. OPT_OUT_RESPECT - Agent must respect do-not-call or opt-out requests

For each violation found, provide:
- rule_code: The rule that was violated
- severity: "HIGH", "MEDIUM", or "LOW"
- quote: The exact quote from the transcript showing the violation
- explanation: Why this is a violation
- suggestion: How the agent should have handled it

Respond ONLY with valid JSON in this format:
{{
    "total_violations": <number>,
    "risk_level": "HIGH" | "MEDIUM" | "LOW" | "NONE",
    "violations": [
        {{
            "rule_code": "RULE_CODE",
            "severity": "HIGH",
            "quote": "exact quote from transcript",
            "explanation": "why this violates the rule",
            "suggestion": "what the agent should have said instead"
        }}
    ],
    "compliant_areas": ["list of rules that were followed correctly"],
    "summary": "One sentence summary of the call's compliance status"
}}

TRANSCRIPT:
{transcript}
"""

class BriefingRequest(BaseModel):
    linkedin_url: str
    twitter_url: Optional[str] = None
    meeting_context: str

class DownloadRequest(BaseModel):
    briefing_id: str
    linkedin_url: Optional[str] = None

class TranscriptRequest(BaseModel):
    transcript: str

class AnalyzeResponse(BaseModel):
    total_violations: int
    risk_level: str
    violations: list
    compliant_areas: list
    summary: str
    transcript: Optional[str] = None

class TranscribeResponse(BaseModel):
    transcript: str

class Base64AudioRequest(BaseModel):
    audio_base64: str
    filename: str

def parse_json_response(response_text: str) -> dict:
    """Parse JSON from Claude's response, handling markdown code blocks."""
    cleaned = response_text.strip()
    
    lines = cleaned.split('\n')
    if lines[0].startswith('```'):
        lines = lines[1:]
    if lines[-1].strip() == '```':
        lines = lines[:-1]
    
    cleaned = '\n'.join(lines).strip()
    return json.loads(cleaned)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "BriefMe Intelligence Suite API"}

@app.post("/api/briefing/generate")
async def generate_briefing(request: BriefingRequest):
    try:
        # Check cache first (Demo Mode)
        # Note: Cache key currently only uses LinkedIn URL. 
        # For simplicity, we keep it that way, assuming LinkedIn is the primary key.
        cached_data = cache_manager.get_from_cache(request.linkedin_url)
        if cached_data:
            return cached_data

        # Pipeline Execution Logic
        api_key = YUTORI_CONFIG.get("api_key", "mock_key")
        
        # Initialize Agents
        browser = LinkedInBrowserAgent(api_key=api_key)
        twitter_browser = TwitterBrowserAgent(api_key=api_key)
        researcher = CompanyResearcher(api_key=api_key)
        extractor = SemanticProfileExtractor()
        theme_engine = ThemeIdentificationEngine()
        transformer = StructuredDataTransformer()
        synthesis_pipeline = AdaptiveSynthesisPipeline(llm_client=anthropic_client)
        
        # Initialize Phase 5 Components
        # Pass the initialized Anthropic client to the generators
        mock_generator = MockConversationGenerator(llm_client=anthropic_client)
        response_coach = ResponseCoach(llm_client=anthropic_client)
        scenario_builder = ConversationScenarioBuilder(llm_client=anthropic_client)
        
        # Phase 1: LinkedIn Browsing
        profile_data = await browser.browse_profile(request.linkedin_url, request.meeting_context)
        
        if not profile_data.get("profile"):
             raise Exception("Failed to extract profile data. Please check the URL or try again later.")
        
        # Phase 1.5: Twitter Browsing (Optional)
        twitter_posts = []
        if request.twitter_url:
            twitter_posts = await twitter_browser.browse_tweets(request.twitter_url)
            # Combine LinkedIn posts and Tweets for analysis
            profile_data["posts"].extend(twitter_posts)

        company_name = profile_data["profile"].get("company", "Unknown")
        role = profile_data["profile"].get("current_role", "Unknown")
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
                "name": phase1_output["profile"].get("name"),
                "role": phase1_output["profile"].get("current_role"),
                "company": phase1_output["profile"].get("company"),
                "professional_identity": themes.get("professional_identity", ""),
                "career_trajectory": "IC -> Lead -> CTO" # Still somewhat mocked unless we extract history
            },
            "themes": theme_insights,
            "sentiment": sentiment,
            "insights": insights,
            "company_context": {
                "name": phase1_output["company_context"].get("name"),
                "relevance_score": 0.85,
                "key_facts": phase1_output["company_context"].get("recent_news", []),
                "recent_developments": phase1_output["company_context"].get("recent_news", [])
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
        raise HTTPException(status_code=404, detail="Briefing not found. Please generate it first.")
    
    pdf_gen = PDFGenerator()
    pdf_bytes = pdf_gen.generate(data)
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=briefing.pdf"}
    )

# --- Call Analyzer Endpoints ---

@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe an audio file using ElevenLabs Speech-to-Text."""
    
    if not elevenlabs_client:
        raise HTTPException(status_code=500, detail="ElevenLabs client not initialized")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Transcribe with ElevenLabs
        with open(tmp_path, "rb") as audio_file:
            result = elevenlabs_client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                language_code="en"
            )
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return TranscribeResponse(transcript=result.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-audio-base64")
async def analyze_audio_base64(request: Base64AudioRequest):
    """Analyze audio from base64 data."""
    if not elevenlabs_client:
        raise HTTPException(status_code=500, detail="ElevenLabs client not initialized")
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic client not initialized")

    # Decode base64 to file
    audio_data = base64.b64decode(request.audio_base64)
    suffix = request.filename.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name
    
    try:
        # Transcribe
        with open(tmp_path, "rb") as audio_file:
            result = elevenlabs_client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                language_code="en"
            )
        transcript = result.text
        
        # Analyze
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5", 
            max_tokens=2000,
            messages=[{"role": "user", "content": COMPLIANCE_PROMPT.format(transcript=transcript)}]
        )
        
        response_text = message.content[0].text
        compliance_result = parse_json_response(response_text)
        
        return {**compliance_result, "transcript": transcript}
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_compliance(request: TranscriptRequest):
    """Analyze a transcript for compliance violations using Claude."""
    
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic client not initialized")
    
    try:
        # Note: Model name updated to a more standard one if the previous was hypothetical
        # Reverting to what was in the source file: claude-sonnet-4-5
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5", 
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": COMPLIANCE_PROMPT.format(transcript=request.transcript)
                }
            ]
        )
        
        response_text = message.content[0].text
        result = parse_json_response(response_text)
        
        return AnalyzeResponse(**result, transcript=request.transcript)
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Claude response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-audio", response_model=AnalyzeResponse)
async def analyze_audio(file: UploadFile = File(...)):
    """Full pipeline: Transcribe audio and analyze for compliance in one call."""
    
    # First transcribe
    transcribe_result = await transcribe_audio(file)
    
    # Then analyze
    analyze_result = await analyze_compliance(TranscriptRequest(transcript=transcribe_result.transcript))
    
    return analyze_result

@app.post("/analyze-audio-form")
async def analyze_audio_form(audio_base64: str = Form(...), filename: str = Form(...)):
    """Analyze audio from form data."""
    if not elevenlabs_client:
        raise HTTPException(status_code=500, detail="ElevenLabs client not initialized")
    if not anthropic_client:
        raise HTTPException(status_code=500, detail="Anthropic client not initialized")

    # Decode base64 to file
    try:
        audio_data = base64.b64decode(audio_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 data: {e}")

    suffix = filename.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name
    
    try:
        # Transcribe
        with open(tmp_path, "rb") as audio_file:
            result = elevenlabs_client.speech_to_text.convert(
                file=audio_file,
                model_id="scribe_v1",
                language_code="en"
            )
        transcript = result.text
        
        # Analyze
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-5", 
            max_tokens=2000,
            messages=[{"role": "user", "content": COMPLIANCE_PROMPT.format(transcript=transcript)}]
        )
        
        response_text = message.content[0].text
        compliance_result = parse_json_response(response_text)
        
        return {**compliance_result, "transcript": transcript}
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)