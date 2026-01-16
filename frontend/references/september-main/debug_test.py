import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

msg = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=2000,
    messages=[{'role': 'user', 'content': '''Analyze this transcript for compliance. Return ONLY JSON.
    
Transcript: Agent says "Pay now or your credit is destroyed"

Return format:
{"total_violations": 1, "risk_level": "HIGH", "violations": [{"rule_code": "TEST", "severity": "HIGH", "quote": "quote", "explanation": "why", "suggestion": "fix"}], "compliant_areas": [], "summary": "summary"}'''}]
)

print('Raw response:')
print(repr(msg.content[0].text))
