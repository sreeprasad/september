"""
Task 3: Test Claude Compliance Analysis
Run with: uv run python test_compliance.py <transcript_file>
Or: uv run python test_compliance.py (uses sample transcript)
"""

import sys
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

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

SAMPLE_TRANSCRIPT = """
Agent: Hello, thanks for calling ABC Financial Services, my name is Mike. How can I help you today?

Customer: Hi, I'm calling about my account balance.

Agent: Sure, I can help with that. What's your account number?

Customer: It's 4521-8890.

Agent: Great, I see your account here. Your current balance is $2,450.

Customer: Oh that seems high. I thought I paid last month.

Agent: Look, I'm going to be honest with you - if you don't pay this TODAY, we're going to have to send this to collections and that will DESTROY your credit score. You really need to act now. I can take a payment right now over the phone.

Customer: I... I don't know, I need to check with my husband first.

Agent: Trust me, you don't have time for that. Every day you wait, the interest is piling up. I've seen people lose their homes over this. Let me just get your card number and we can take care of this right now before it's too late.

Customer: Actually, can you remove me from your call list? I don't want any more calls.

Agent: Sure, but let's just finish this payment first. What's your card number?

Customer: No, I said I want to be removed from your list.

Agent: I'll make a note, but seriously, about that payment...
"""


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


def analyze_compliance(transcript: str) -> dict:
    """Analyze a transcript for compliance violations using Claude."""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    
    client = Anthropic(api_key=api_key)
    
    print("🔍 Analyzing transcript for compliance violations...")
    print("⏳ Processing with Claude...")
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": COMPLIANCE_PROMPT.format(transcript=transcript)
            }
        ]
    )
    
    response_text = message.content[0].text
    return parse_json_response(response_text)


def print_results(result: dict):
    """Pretty print the compliance analysis results."""
    
    print("\n" + "=" * 60)
    print("📋 COMPLIANCE ANALYSIS REPORT")
    print("=" * 60)
    
    risk_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "NONE": "✅"}
    
    print(f"\n🎯 Risk Level: {risk_emoji.get(result['risk_level'], '❓')} {result['risk_level']}")
    print(f"📊 Total Violations: {result['total_violations']}")
    print(f"\n💬 Summary: {result['summary']}")
    
    if result['violations']:
        print("\n" + "-" * 60)
        print("⚠️  VIOLATIONS FOUND:")
        print("-" * 60)
        
        for i, v in enumerate(result['violations'], 1):
            severity_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            print(f"\n{i}. [{severity_emoji.get(v['severity'], '❓')} {v['severity']}] {v['rule_code']}")
            print(f"   Quote: \"{v['quote']}\"")
            print(f"   Issue: {v['explanation']}")
            print(f"   Fix: {v['suggestion']}")
    
    if result.get('compliant_areas'):
        print("\n" + "-" * 60)
        print("✅ COMPLIANT AREAS:")
        print("-" * 60)
        for area in result['compliant_areas']:
            print(f"   • {area}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        transcript_path = sys.argv[1]
        if not os.path.exists(transcript_path):
            print(f"❌ File not found: {transcript_path}")
            sys.exit(1)
        with open(transcript_path, "r") as f:
            transcript = f.read()
        print(f"📁 Using transcript from: {transcript_path}")
    else:
        transcript = SAMPLE_TRANSCRIPT
        print("📝 Using sample transcript (run with file path for custom transcript)")
    
    try:
        result = analyze_compliance(transcript)
        print_results(result)
        
        output_file = "compliance_results.json"
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Results saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
