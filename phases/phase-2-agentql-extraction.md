# Phase 2: TinyFish AgentQL Extraction

**Duration:** ~1 hour
**Priority:** Critical (Data transformation layer)
**Judge Focus:** Homer W. (TinyFish - Head of Product)

---

## Overview

AgentQL transforms raw web data into semantically understood, structured JSON. It's not just parsing HTML—it's understanding intent and extracting themes.

## Tool Information

### What is AgentQL?

- **Suite of tools** for connecting AI to the web
- **Natural language queries** to pinpoint data and elements on any web page
- **Self-healing selectors** that work across similar sites and adapt to UI changes
- **AI-powered alternative** to fragile XPath and DOM/CSS selectors

### Key Features

- Semantic/natural language queries
- Structured data extraction to JSON
- Theme identification
- Sentiment analysis
- Works with authenticated and dynamically generated content

### Resources

- **Main Site**: https://www.agentql.com
- **GitHub**: https://github.com/tinyfish-io/agentql
- **Python SDK**: `pip install agentql`
- **JavaScript SDK**: `npm install agentql`
- **MCP Server**: https://playbooks.com/mcp/tinyfish-agentql

---

## Implementation Steps

### Step 2.1: SDK Installation & Setup

```bash
# Python
pip install agentql playwright
playwright install  # Install browser binaries

# Or JavaScript
npm install agentql playwright
```

**Configuration:**
```python
# config/agentql_config.py
import os

AGENTQL_CONFIG = {
    "api_key": os.getenv("AGENTQL_API_KEY"),
    "extraction_mode": "semantic",  # Use semantic extraction
    "output_format": "json",
    "include_confidence_scores": True
}
```

### Step 2.2: Semantic Profile Extractor

**Objective:** Extract structured data from raw Navigator output using semantic understanding.

```python
# extractors/profile_extractor.py
from agentql import AgentQL

class SemanticProfileExtractor:
    """
    Uses AgentQL to semantically extract and structure profile data.

    Key differentiator: Understanding INTENT, not just text.
    """

    def __init__(self):
        self.ql = AgentQL()

    async def extract_profile_themes(self, raw_posts: list) -> dict:
        """
        Extract themes from posts using semantic analysis.

        Example output:
        {
            "primary_theme": "developer experience",
            "theme_frequency": {"devex": 0.45, "ai": 0.30, "leadership": 0.25},
            "professional_identity": "Developer advocate focused on DX"
        }
        """
        query = """
        Analyze these posts and extract:
        - Primary professional themes
        - Recurring topics and their frequency
        - Professional identity beyond job title
        - Passion indicators
        """
        pass

    async def extract_sentiment_patterns(self, posts: list) -> dict:
        """
        Understand sentiment and emotional patterns.

        Output:
        {
            "overall_sentiment": "positive",
            "passion_topics": ["open source", "mentorship"],
            "concerns": ["tech debt", "burnout"],
            "communication_style": "direct and technical"
        }
        """
        pass
```

### Step 2.3: Theme Identification Engine

**This is the KEY differentiator for Homer's judging criteria.**

```python
# extractors/theme_engine.py

class ThemeIdentificationEngine:
    """
    Goes beyond text parsing to identify meaningful themes.

    Demo point: "This person posts about developer experience
    3x more than anything else"
    """

    def identify_themes(self, content: list) -> dict:
        """
        Identify and rank themes from content.

        Uses AgentQL's semantic understanding to:
        1. Cluster related topics
        2. Calculate frequency ratios
        3. Identify passion vs. obligation posts
        4. Extract professional identity markers
        """
        pass

    def generate_theme_insights(self, themes: dict) -> list:
        """
        Generate human-readable insights from themes.

        Example:
        "This person's professional identity is centered on
        developer advocacy, not their job title. They post about
        developer experience 3x more than anything else."
        """
        pass
```

### Step 2.4: Structured Data Transformer

```python
# extractors/data_transformer.py

class StructuredDataTransformer:
    """
    Transform extracted data into clean JSON for downstream processing.
    """

    def transform_to_briefing_format(self, raw_extraction: dict) -> dict:
        """
        Transform semantic extraction into briefing-ready format.

        Input: Raw AgentQL extraction
        Output: Clean JSON matching Cline synthesis requirements
        """
        return {
            "person": {
                "name": "",
                "role": "",
                "company": "",
                "professional_identity": "",  # Beyond job title
            },
            "themes": {
                "primary": "",
                "secondary": [],
                "frequency_breakdown": {},
            },
            "sentiment": {
                "overall": "",
                "passion_topics": [],
                "communication_style": "",
            },
            "company_context": {
                "relevance_score": 0.0,
                "key_facts": [],
                "recent_developments": [],
            },
            "extraction_metadata": {
                "confidence_score": 0.0,
                "data_quality": "",
                "extraction_time": "",
            }
        }
```

---

## AgentQL Query Examples

### Profile Theme Query
```
{
    profile_themes[] {
        topic_name
        frequency_score
        example_posts[]
        sentiment_indicator
    }
}
```

### Semantic Post Analysis
```
{
    posts[] {
        content
        primary_topic
        engagement_quality  # Not just numbers, but quality
        passion_indicator   # High/Medium/Low
        relevance_to_identity
    }
}
```

### Company Context Query
```
{
    company {
        core_business
        recent_news[] {
            headline
            relevance_to_person
            date
        }
        market_position
        key_differentiators[]
    }
}
```

---

## Data Schema

### Input (from Phase 1)
```json
{
    "profile": { ... },
    "posts": [ ... ],
    "company_context": { ... },
    "decision_metadata": { ... }
}
```

### Output (to Phase 4 - Cline)
```json
{
    "person": {
        "name": "string",
        "role": "string",
        "company": "string",
        "professional_identity": "Developer advocate who prioritizes DX",
        "career_trajectory": "IC → Lead → VP path"
    },
    "themes": {
        "primary": "developer experience",
        "secondary": ["AI/ML", "open source", "mentorship"],
        "frequency_breakdown": {
            "developer experience": 0.45,
            "AI/ML": 0.30,
            "open source": 0.15,
            "mentorship": 0.10
        }
    },
    "sentiment": {
        "overall": "positive-enthusiastic",
        "passion_topics": ["open source contributions", "junior dev mentorship"],
        "concerns": ["technical debt", "meeting overload"],
        "communication_style": "direct, technical, uses examples"
    },
    "insights": [
        {
            "insight": "Posts about devex 3x more than role suggests",
            "confidence": 0.92,
            "evidence": ["post_id_1", "post_id_2"]
        }
    ],
    "company_context": {
        "name": "string",
        "relevance_score": 0.85,
        "key_facts": [],
        "recent_developments": []
    }
}
```

---

## Demo Script Points (for Homer)

During the demo, highlight:

1. **"AgentQL isn't parsing HTML—it's understanding intent"**
2. **"It identified that this person's professional identity is centered on developer advocacy, not their job title"**
3. **"This person posts about developer experience 3x more than anything else"**
4. **"Semantic extraction, not just text pulling"**

**Key Demo Moment:**
> Show the theme frequency breakdown: "Look—their job title says 'VP of Engineering' but their posts reveal they're really a developer advocate at heart."

---

## MCP Server Integration (Optional Enhancement)

If time permits, integrate the AgentQL MCP server for enhanced capabilities:

```bash
# Install MCP server
npx @anthropic-ai/mcp-cli install tinyfish-agentql
```

This allows:
- Real-time debugging of queries
- Enhanced extraction capabilities
- Direct integration with AI assistants

---

## Testing Checklist

- [ ] AgentQL SDK installed and authenticated
- [ ] Can extract themes from sample posts
- [ ] Theme frequency calculation is accurate
- [ ] Sentiment analysis produces meaningful results
- [ ] Output schema matches Phase 4 input requirements
- [ ] Extraction completes in under 15 seconds
- [ ] Confidence scores are included
- [ ] Edge cases handled (empty posts, private profiles)

---

## Files to Create

```
src/
├── extractors/
│   ├── __init__.py
│   ├── profile_extractor.py
│   ├── theme_engine.py
│   └── data_transformer.py
├── queries/
│   ├── profile_themes.aql
│   ├── post_analysis.aql
│   └── company_context.aql
└── schemas/
    └── extraction_output.py
```

---

## Success Criteria

1. **Semantic**: Extract meaning, not just text
2. **Thematic**: Identify and rank themes accurately
3. **Insightful**: Generate "aha" moments (3x frequency insight)
4. **Structured**: Clean JSON output for downstream
5. **Fast**: Under 15 seconds extraction time
6. **Confident**: Include confidence scores for transparency
