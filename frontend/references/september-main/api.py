"""
Voice Compliance Copilot - FastAPI Backend
Run with: uv run uvicorn api:app --reload --port 8000
"""

import os
import json
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from anthropic import Anthropic

load_dotenv()

app = FastAPI(title="Voice Compliance Copilot API")


# Allow Retool to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


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


class TranscriptRequest(BaseModel):
    transcript: str


class AnalyzeResponse(BaseModel):
    total_violations: int
    risk_level: str
    violations: list
    compliant_areas: list
    summary: str


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
    return {"status": "ok", "service": "Voice Compliance Copilot API"}


@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe an audio file using ElevenLabs Speech-to-Text."""
    
    if not os.getenv("ELEVENLABS_API_KEY"):
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not configured")
    
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
    import base64
    
    # Decode base64 to file
    audio_data = base64.b64decode(request.audio_base64)
    suffix = request.filename.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name
    
    # Transcribe
    with open(tmp_path, "rb") as audio_file:
        result = elevenlabs_client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",
            language_code="en"
        )
    os.unlink(tmp_path)
    transcript = result.text
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": COMPLIANCE_PROMPT.format(transcript=transcript)}]
    )
    
    response_text = message.content[0].text
    compliance_result = parse_json_response(response_text)
    
    return {**compliance_result, "transcript": transcript}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_compliance(request: TranscriptRequest):
    """Analyze a transcript for compliance violations using Claude."""
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not configured")
    
    try:
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
        
        return AnalyzeResponse(**result)
    
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


from fastapi import Form

@app.post("/analyze-audio-form")
async def analyze_audio_form(audio_base64: str = Form(...), filename: str = Form(...)):
    """Analyze audio from form data."""
    import base64
    
    # Decode base64 to file
    audio_data = base64.b64decode(audio_base64)
    suffix = filename.split('.')[-1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(audio_data)
        tmp_path = tmp.name
    
    # Transcribe
    with open(tmp_path, "rb") as audio_file:
        result = elevenlabs_client.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",
            language_code="en"
        )
    os.unlink(tmp_path)
    
    # Analyze
    transcript = result.text
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": COMPLIANCE_PROMPT.format(transcript=transcript)}]
    )
    
    response_text = message.content[0].text
    compliance_result = parse_json_response(response_text)

    print("returning reponse ")
    
    return {**compliance_result, "transcript": transcript}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
