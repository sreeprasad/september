# Phase 5: Tonic Fabricate Mock Conversations

**Duration:** ~30 minutes
**Priority:** High (Novel feature)
**Judge Focus:** Karl Hanson (Tonic.AI - Co-Founder)

---

## Overview

Tonic Fabricate generates mock conversation scenarios—preparing you not just with information, but with actual conversation practice. This is the novel use case that will impress Karl: Fabricate for contextual prep, not just test data.

## Tool Information

### What is Tonic Fabricate?

- **AI-powered synthetic data generation** platform
- **Natural language interface** - describe what you need in plain English
- **Hyper-realistic data** in under 5 minutes
- **Multiple output formats** - databases, CSVs, PDFs, DOCX, emails

### Key Features

- Fabricate Data Agent for chat-based data generation
- Relational data with referential integrity
- Domain-specific realistic data
- Integration with CI/CD pipelines
- Free tier available

### Recent Updates (2025)

- **November 2025**: Launched Fabricate Data Agent
- **April 2025**: Tonic.ai acquired Fabricate (from Mockaroo)
- Showcased at AWS re:Invent 2025

### Resources

- **Main Site**: https://www.tonic.ai/products/fabricate
- **Blog**: https://www.tonic.ai/blog/hyper-realistic-synthetic-data-via-agentic-ai-has-arrived-meet-the-fabricate-data-agent
- **Webinar**: https://www.tonic.ai/webinars/introducing-fabricate-data-agent-the-ai-agent-for-synthetic-data-generation

---

## Implementation Steps

### Step 5.1: Fabricate Setup

```bash
# Access Fabricate via web interface or API
# Sign up at tonic.ai/products/fabricate
```

**API Configuration:**
```python
# config/fabricate_config.py
import os

FABRICATE_CONFIG = {
    "api_key": os.getenv("TONIC_FABRICATE_API_KEY"),
    "endpoint": "https://api.tonic.ai/fabricate",
    "output_format": "json",
    "generation_mode": "contextual"  # Our novel use case
}
```

### Step 5.2: Mock Conversation Generator

**This is the KEY differentiator for Karl Hanson's judging criteria.**

```python
# fabricate/conversation_generator.py

class MockConversationGenerator:
    """
    Uses Fabricate to generate contextual mock conversations.

    Novel use case: Not generating test data, but generating
    conversation PREPARATION based on real profile intelligence.
    """

    def __init__(self, fabricate_client):
        self.fabricate = fabricate_client

    async def generate_likely_questions(
        self,
        profile_data: dict,
        meeting_context: str
    ) -> list:
        """
        Generate questions the person is likely to ask.

        Based on:
        - Their interests and themes
        - Their communication style
        - The meeting context
        - Their role and seniority
        """

        prompt = f"""
        Generate 3-5 questions that this person is likely to ask
        based on their profile.

        Person: {profile_data['name']}
        Role: {profile_data['role']}
        Interests: {profile_data['themes']['passion_topics']}
        Communication Style: {profile_data['sentiment']['communication_style']}
        Meeting Context: {meeting_context}

        For each question, include:
        - The question itself
        - Why they would ask this (based on their profile)
        - A suggested response strategy
        - Follow-up questions they might have
        """

        return await self.fabricate.generate(prompt)

    async def generate_pitch_simulation(
        self,
        profile_data: dict,
        your_pitch: str
    ) -> list:
        """
        Generate a simulated back-and-forth conversation.

        "Here's a simulated back-and-forth if you pitch them X"
        """

        prompt = f"""
        Simulate a conversation where you pitch this person.

        Person Profile:
        - Name: {profile_data['name']}
        - Role: {profile_data['role']}
        - Interests: {profile_data['themes']}
        - Style: {profile_data['sentiment']['communication_style']}

        Your Pitch: {your_pitch}

        Generate a realistic 4-6 exchange conversation showing:
        - How they would respond to the pitch
        - Follow-up questions based on their interests
        - Potential objections based on their background
        - How the conversation might naturally evolve
        """

        return await self.fabricate.generate(prompt)
```

### Step 5.3: Question Types by Person Type

```python
# fabricate/question_templates.py

class QuestionTemplates:
    """
    Templates for generating relevant questions by person type.
    """

    QUESTION_FRAMEWORKS = {
        "executive": {
            "categories": ["strategic_impact", "roi", "team_resources", "timeline"],
            "style": "high-level, outcome-focused",
            "typical_concerns": ["budget", "team capacity", "strategic fit"]
        },
        "engineer": {
            "categories": ["technical_architecture", "scalability", "integration", "maintenance"],
            "style": "detailed, specific examples",
            "typical_concerns": ["tech debt", "complexity", "team expertise"]
        },
        "investor": {
            "categories": ["market_size", "traction", "team", "competition", "unit_economics"],
            "style": "metrics-driven, thesis-validation",
            "typical_concerns": ["defensibility", "growth rate", "capital efficiency"]
        },
        "designer": {
            "categories": ["user_research", "design_process", "iteration", "metrics"],
            "style": "user-centric, process-oriented",
            "typical_concerns": ["user needs", "design debt", "team collaboration"]
        }
    }

    def get_question_framework(self, person_type: str, themes: dict) -> dict:
        """
        Get question generation framework based on person type and themes.
        """
        base_framework = self.QUESTION_FRAMEWORKS.get(
            person_type,
            self.QUESTION_FRAMEWORKS["executive"]
        )

        # Customize based on their specific themes
        customized = self._customize_for_themes(base_framework, themes)

        return customized
```

### Step 5.4: Conversation Scenario Builder

```python
# fabricate/scenario_builder.py

class ConversationScenarioBuilder:
    """
    Build complete conversation scenarios for different contexts.
    """

    async def build_scenarios(
        self,
        profile_data: dict,
        meeting_contexts: list = None
    ) -> dict:
        """
        Build multiple conversation scenarios.

        Default contexts:
        - First meeting introduction
        - Pitching your product/idea
        - Asking for advice/mentorship
        - Partnership discussion
        """

        contexts = meeting_contexts or [
            "first_meeting",
            "pitch",
            "advice_seeking",
            "partnership"
        ]

        scenarios = {}

        for context in contexts:
            scenario = await self._build_single_scenario(profile_data, context)
            scenarios[context] = scenario

        return scenarios

    async def _build_single_scenario(
        self,
        profile_data: dict,
        context: str
    ) -> dict:
        """
        Build a single conversation scenario.

        Returns:
        {
            "context": "first_meeting",
            "likely_opener": "How they might start the conversation",
            "questions_they_might_ask": [],
            "topics_to_avoid": [],
            "topics_to_lean_into": [],
            "sample_dialogue": []
        }
        """
        pass
```

### Step 5.5: Response Coach

```python
# fabricate/response_coach.py

class ResponseCoach:
    """
    Generate suggested responses and coaching tips.
    """

    async def generate_response_strategies(
        self,
        questions: list,
        profile_data: dict
    ) -> list:
        """
        For each likely question, generate response strategies.

        Each strategy includes:
        - Suggested response framework
        - What to emphasize (based on their interests)
        - What to avoid
        - How to pivot if needed
        """

        strategies = []

        for question in questions:
            strategy = {
                "question": question["question"],
                "response_framework": self._generate_framework(question, profile_data),
                "emphasize": self._what_to_emphasize(question, profile_data),
                "avoid": self._what_to_avoid(question, profile_data),
                "pivot_options": self._generate_pivots(question, profile_data),
                "follow_up_prepared": self._prepare_follow_ups(question)
            }
            strategies.append(strategy)

        return strategies
```

---

## Data Schema

### Input (from Phase 4)
```json
{
  "person_type": "executive",
  "talking_points": [...],
  "key_insights": [...],
  "profile_data": {
    "name": "string",
    "role": "string",
    "themes": {...},
    "sentiment": {...}
  }
}
```

### Output (to Phase 3 - Dashboard)
```json
{
  "mock_conversations": {
    "likely_questions": [
      {
        "question": "What's your approach to AI governance?",
        "why_likely": "Posted about AI ethics 5 times recently",
        "response_strategy": {
          "framework": "Acknowledge concern, share your principles, give example",
          "emphasize": ["transparency", "human oversight"],
          "avoid": ["dismissing concerns", "overly technical jargon"],
          "sample_response": "Great question..."
        }
      }
    ],
    "pitch_simulation": [
      {
        "speaker": "them",
        "message": "Tell me about what you're working on",
        "context": "Standard opener"
      },
      {
        "speaker": "you",
        "message": "We're building...",
        "context": "Lead with their interest area"
      },
      {
        "speaker": "them",
        "message": "How does that handle [their concern]?",
        "context": "Based on their posting about this topic"
      }
    ],
    "conversation_scenarios": {
      "first_meeting": {...},
      "pitch": {...},
      "advice_seeking": {...}
    }
  }
}
```

---

## Demo Script Points (for Karl)

During the demo, highlight:

1. **"Fabricate isn't just generating test data—it's generating preparation"**
2. **"Contextual mock conversations based on real profile intelligence"**
3. **Show the questions**: "Based on their interests, here are 3 likely questions they'll ask you"
4. **Show the simulation**: "Here's a simulated back-and-forth if you pitch them X"

**Key Demo Moment:**
> "Karl, watch this—Fabricate just generated a mock conversation based on your profile. It predicted you might ask about data quality because of your Tonic background. Here's how I'd respond."

**Bold Move (if confident):**
> Use Karl's actual profile to generate mock questions, then show him the output live.

---

## Integration Points

### With Cline (Phase 4)
- Receive person type classification
- Use talking points as conversation anchors
- Leverage reasoning chain for question context

### With Retool (Phase 3)
- Display questions in expandable cards
- Show pitch simulation as chat-style interface
- Allow scenario switching via tabs

---

## Testing Checklist

- [ ] Fabricate API connection works
- [ ] Questions generated are relevant to profile
- [ ] Pitch simulation feels realistic
- [ ] Response strategies are actionable
- [ ] Output matches dashboard expectations
- [ ] Generation completes in under 20 seconds
- [ ] Different outputs for different person types

---

## Files to Create

```
src/
├── fabricate/
│   ├── __init__.py
│   ├── conversation_generator.py
│   ├── question_templates.py
│   ├── scenario_builder.py
│   └── response_coach.py
├── config/
│   └── fabricate_config.py
└── schemas/
    └── mock_conversation_output.py
```

---

## Success Criteria

1. **Novel**: Clearly different from typical Fabricate use cases
2. **Relevant**: Questions match profile themes
3. **Actionable**: Response strategies are useful
4. **Realistic**: Simulations feel like real conversations
5. **Fast**: Generation under 20 seconds
6. **Demo-worthy**: Impressive enough to stand out to Karl
