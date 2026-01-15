# Phase 4: Cline Adaptive Synthesis

**Duration:** ~30-45 minutes
**Priority:** High (Intelligence layer)
**Judge Focus:** Juan Pablo (Cline), Gagan Bhat (Anthropic - reasoning quality)

---

## Overview

Cline handles the synthesis logic—taking structured data from AgentQL and generating personalized talking points, insights, and reasoning chains. The key differentiator: Cline dynamically adapts the synthesis pipeline based on person type.

## Tool Information

### What is Cline?

- **Open-source AI coding agent** with Plan/Act modes
- **MCP integration** for extending capabilities with custom tools
- **4M+ developers** trust it worldwide
- **Dynamic tool creation** - can create and install tools tailored to workflows

### Key Features

- Model Context Protocol (MCP) integration
- Custom tool creation via natural language
- Memory and context management across sessions
- Orchestration of complex multi-tool workflows
- Enterprise-ready with security controls

### Resources

- **Main Site**: https://cline.bot
- **GitHub**: https://github.com/cline/cline
- **MCP Documentation**: https://cline.bot/tag/mcp
- **Developer Guide**: https://cline.bot/blog/the-developers-guide-to-mcp-from-basics-to-advanced-workflows

---

## Implementation Steps

### Step 4.1: Cline MCP Server Setup

**Create custom MCP server for Brief Me synthesis:**

```bash
# Using Cline to create the MCP server
# In VS Code with Cline extension:
"Create an MCP server that synthesizes meeting briefings from structured profile data"
```

**Manual setup alternative:**

```javascript
// mcp-servers/briefing-synthesis/index.js
import { MCPServer } from '@anthropic-ai/mcp';

const server = new MCPServer({
  name: 'briefing-synthesis',
  version: '1.0.0',
  tools: [
    {
      name: 'synthesize_briefing',
      description: 'Generate personalized briefing from profile data',
      inputSchema: {
        type: 'object',
        properties: {
          profile_data: { type: 'object' },
          person_type: { type: 'string' },
          meeting_context: { type: 'string' }
        }
      }
    },
    {
      name: 'generate_talking_points',
      description: 'Create contextual talking points',
      inputSchema: {
        type: 'object',
        properties: {
          themes: { type: 'object' },
          person_type: { type: 'string' }
        }
      }
    }
  ]
});
```

### Step 4.2: Person Type Classification

**This is the KEY differentiator for Juan Pablo's judging criteria.**

```python
# synthesis/person_classifier.py

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

    def classify(self, profile_data: dict) -> str:
        """
        Classify person type based on role, themes, and content.

        Uses signals like:
        - Job title keywords
        - Post content themes
        - Engagement patterns
        - Company type
        """
        pass

    def get_synthesis_config(self, person_type: str) -> dict:
        """
        Return synthesis configuration for person type.
        """
        return self.PERSON_TYPES.get(person_type, self.PERSON_TYPES["executive"])
```

### Step 4.3: Adaptive Synthesis Pipeline

```python
# synthesis/adaptive_pipeline.py

class AdaptiveSynthesisPipeline:
    """
    Dynamically generates synthesis logic based on person type.

    This is where Cline shines—different synthesis for a CTO vs. a designer.
    """

    def __init__(self, llm_client, person_type: str):
        self.llm = llm_client
        self.person_type = person_type
        self.config = PersonTypeClassifier.PERSON_TYPES[person_type]

    async def synthesize(self, extracted_data: dict) -> dict:
        """
        Run adaptive synthesis pipeline.

        Pipeline varies by person type:
        - Executive: Focus on strategic implications
        - Engineer: Focus on technical depth
        - Designer: Focus on UX and visual thinking
        """

        # Step 1: Generate person-specific prompt
        synthesis_prompt = self._build_adaptive_prompt(extracted_data)

        # Step 2: Run synthesis with adapted parameters
        result = await self.llm.complete(synthesis_prompt)

        # Step 3: Post-process based on person type
        return self._post_process(result)

    def _build_adaptive_prompt(self, data: dict) -> str:
        """
        Build synthesis prompt adapted to person type.
        """
        base_prompt = f"""
        Analyze this person's profile and generate a meeting briefing.

        Person Type: {self.person_type}
        Focus Areas: {self.config['focus']}
        Talking Point Style: {self.config['talking_point_style']}

        Profile Data:
        {json.dumps(data, indent=2)}

        Generate:
        1. 3 talking points tailored to their {self.person_type} perspective
        2. Key insights about what they care about
        3. Reasoning for each recommendation
        """
        return base_prompt
```

### Step 4.4: Talking Points Generator

```python
# synthesis/talking_points.py

class TalkingPointsGenerator:
    """
    Generate contextual, personalized talking points.
    """

    async def generate(self, themes: dict, person_type: str, context: str) -> list:
        """
        Generate 3 talking points with reasoning.

        Each talking point includes:
        - The point itself
        - Why it was selected
        - How to naturally bring it up
        - Expected response/reaction
        """

        talking_points = []

        for theme in themes['top_themes'][:3]:
            point = {
                "point": "",
                "context": "",
                "why_selected": "",
                "conversation_opener": "",
                "expected_reaction": "",
                "follow_up_questions": []
            }
            talking_points.append(point)

        return talking_points

    def adapt_to_person_type(self, points: list, person_type: str) -> list:
        """
        Adjust talking points based on person type.

        For executives: Frame around business impact
        For engineers: Include technical specifics
        For designers: Connect to user outcomes
        """
        pass
```

### Step 4.5: Reasoning Chain Generator

**For Gagan Bhat (Anthropic) - Explainable AI**

```python
# synthesis/reasoning_chain.py

class ReasoningChainGenerator:
    """
    Generate transparent reasoning for all decisions.

    Key for Anthropic judge: Show WHY, not just WHAT.
    """

    def generate_chain(self, decisions: list) -> list:
        """
        For each decision, generate:
        - What was decided
        - Why it was chosen
        - What evidence supports it
        - What alternatives were considered
        - Confidence level
        """

        reasoning_chain = []

        for decision in decisions:
            chain_item = {
                "decision": decision["what"],
                "reason": self._generate_reason(decision),
                "evidence": self._gather_evidence(decision),
                "alternatives_considered": self._list_alternatives(decision),
                "confidence": self._calculate_confidence(decision),
                "explanation_for_user": self._humanize_explanation(decision)
            }
            reasoning_chain.append(chain_item)

        return reasoning_chain

    def _humanize_explanation(self, decision: dict) -> str:
        """
        Create human-readable explanation.

        Example:
        "I chose to highlight their interest in AI ethics because:
         - They posted about it 5 times in the last 3 months
         - Each post had 3x their average engagement
         - It aligns with your stated meeting goal of discussing AI strategy"
        """
        pass
```

### Step 4.6: MCP Tool Integration

```python
# synthesis/mcp_integration.py

class ClineMCPIntegration:
    """
    Integrate with Cline's MCP for dynamic tool creation.
    """

    async def create_synthesis_tool(self, person_type: str):
        """
        Dynamically create synthesis tool via Cline.

        Instead of hardcoding synthesis logic, have Cline
        generate it based on person type.
        """

        tool_prompt = f"""
        Create an MCP tool that synthesizes meeting briefings for {person_type}s.

        The tool should:
        1. Accept profile data and themes as input
        2. Generate talking points appropriate for a {person_type}
        3. Include reasoning for each recommendation
        4. Output structured JSON

        Focus areas for {person_type}: {PERSON_TYPES[person_type]['focus']}
        """

        # Cline creates the tool dynamically
        pass
```

---

## Data Schema

### Input (from Phase 2)
```json
{
  "person": {
    "name": "string",
    "role": "string",
    "company": "string",
    "professional_identity": "string"
  },
  "themes": {
    "primary": "string",
    "secondary": ["string"],
    "frequency_breakdown": {}
  },
  "sentiment": {
    "overall": "string",
    "passion_topics": [],
    "communication_style": "string"
  }
}
```

### Output (to Phase 5 - Fabricate)
```json
{
  "person_type": "executive",
  "synthesis_config": {
    "focus_areas": [],
    "talking_point_style": "string"
  },
  "talking_points": [
    {
      "point": "string",
      "context": "string",
      "why_selected": "string",
      "conversation_opener": "string",
      "expected_reaction": "string"
    }
  ],
  "key_insights": [
    {
      "insight": "string",
      "confidence": 0.92,
      "evidence": []
    }
  ],
  "reasoning_chain": [
    {
      "decision": "string",
      "reason": "string",
      "evidence": "string",
      "confidence": 0.95
    }
  ],
  "briefing_summary": "string"
}
```

---

## Demo Script Points (for Juan Pablo)

During the demo, highlight:

1. **"Cline isn't just writing code—it's adapting the analysis pipeline to the person type"**
2. **"Different synthesis for a CTO vs. a designer"**
3. **Show the person type classification**: "Detected: Executive → Focusing on strategic implications"
4. **Show adaptive output**: "For engineers, we'd show technical depth instead"

**Key Demo Moment:**
> "Watch how the talking points change when we classify someone as an engineer vs. an executive. The synthesis pipeline adapts dynamically."

---

## Testing Checklist

- [ ] Person type classification works accurately
- [ ] Different outputs for different person types
- [ ] Talking points are relevant and actionable
- [ ] Reasoning chain is clear and transparent
- [ ] Output schema matches Phase 5 requirements
- [ ] Synthesis completes in under 10 seconds
- [ ] MCP integration functional (if time permits)

---

## Files to Create

```
src/
├── synthesis/
│   ├── __init__.py
│   ├── person_classifier.py
│   ├── adaptive_pipeline.py
│   ├── talking_points.py
│   ├── reasoning_chain.py
│   └── mcp_integration.py
├── mcp-servers/
│   └── briefing-synthesis/
│       ├── index.js
│       ├── package.json
│       └── tools/
│           ├── synthesize.js
│           └── classify.js
└── prompts/
    ├── executive_synthesis.txt
    ├── engineer_synthesis.txt
    └── designer_synthesis.txt
```

---

## Success Criteria

1. **Adaptive**: Different outputs for different person types
2. **Intelligent**: Talking points feel personalized, not generic
3. **Transparent**: Clear reasoning for all decisions
4. **Fast**: Synthesis under 10 seconds
5. **Dynamic**: Pipeline adapts based on classification
6. **Demo-ready**: Clear visual difference between person types
