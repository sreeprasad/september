# Phase 1: Yutori Navigator Integration

**Duration:** ~1 hour
**Priority:** Critical (Foundation layer)
**Judge Focus:** Dhruv Batra (Yutori - $3,500 prize)

---

## Overview

Yutori Navigator is the entry point of the pipeline. It handles intelligent web browsing, visiting LinkedIn profiles, and making autonomous decisions about which data matters most.

## Tool Information

### What is Yutori Navigator?

- **State-of-the-art web agent** that autonomously navigates websites on its own cloud browser
- **Powered by Yutori n1** - a pixels-to-actions LLM trained via mid-training, supervised fine-tuning, and reinforcement learning
- **Performance**: 78.7% success rate on Online-Mind2Web, 83.4% on Navi-Bench
- **Speed**: 3.3x faster than Claude 4.5, 2.7x faster than Gemini 2.5

### Key Capabilities

- Checking availability, comparing prices, filling forms
- Making reservations, ordering food, completing purchases
- **Most relevant for us**: Intelligent content prioritization and decision-making

### Resources

- **API Documentation**: https://yutori.com/api
- **GitHub (Navi-Bench)**: https://github.com/yutori-ai/navi-bench
- **Blog**: https://yutori.com/blog/introducing-navigator

---

## Implementation Steps

### Step 1.1: API Setup & Authentication

```bash
# Install dependencies (likely Python SDK)
pip install yutori  # or npm install @yutori/navigator
```

**Tasks:**
1. Obtain API key from Yutori developer portal
2. Set up environment variables for credentials
3. Create a configuration file for Navigator settings

```python
# config/yutori_config.py
import os

YUTORI_CONFIG = {
    "api_key": os.getenv("YUTORI_API_KEY"),
    "browser_mode": "cloud",  # Use cloud browser
    "timeout": 60,  # 60 second timeout
    "decision_mode": "intelligent"  # Enable intelligent prioritization
}
```

### Step 1.2: LinkedIn Profile Browsing Agent

**Objective:** Create an agent that visits a LinkedIn profile and extracts relevant information with intelligent prioritization.

```python
# agents/linkedin_browser.py

class LinkedInBrowserAgent:
    """
    Agent that uses Yutori Navigator to browse LinkedIn profiles
    and make intelligent decisions about what content matters.
    """

    def __init__(self, navigator_client):
        self.navigator = navigator_client

    async def browse_profile(self, linkedin_url: str) -> dict:
        """
        Browse a LinkedIn profile and return prioritized data.

        The agent will:
        1. Visit the profile page
        2. Scroll through posts and activity
        3. DECIDE which posts reveal personality (not just recent)
        4. Visit company page if relevant
        5. Return structured data with prioritization metadata
        """
        pass

    async def analyze_posts(self, profile_data: dict) -> list:
        """
        Analyze posts and determine which reveal meaningful insights.

        Decision criteria:
        - Engagement level (comments, likes)
        - Topic relevance to professional identity
        - Recency vs. significance trade-off
        - Sentiment and passion indicators
        """
        pass
```

### Step 1.3: Company Research Module

**Objective:** Autonomously research the person's company and decide what information is most relevant.

```python
# agents/company_researcher.py

class CompanyResearcher:
    """
    Uses Navigator to research company context and make
    intelligent decisions about relevance.
    """

    async def research_company(self, company_name: str, person_role: str) -> dict:
        """
        Research company and prioritize information based on context.

        Decision Logic:
        - For executives: Focus on funding news, strategic moves
        - For engineers: Focus on tech stack, product launches
        - For sales: Focus on competitors, market position
        """
        sources_to_check = [
            "crunchbase",
            "company_website",
            "recent_news",
            "linkedin_company_page"
        ]
        pass
```

### Step 1.4: Decision Engine Integration

**This is the KEY differentiator for Dhruv Batra's judging criteria.**

```python
# agents/decision_engine.py

class NavigatorDecisionEngine:
    """
    The intelligence layer that makes Navigator stand out.

    Instead of scraping everything, we DECIDE what matters.
    """

    def prioritize_data_points(self, raw_data: dict) -> dict:
        """
        From 47 data points, surface the 5 most relevant.

        Criteria:
        1. Relevance to first meeting context
        2. Uniqueness (not generic job title info)
        3. Conversation potential (can spark discussion)
        4. Recency balanced with significance
        5. Emotional/passion indicators
        """
        pass

    def generate_reasoning(self, decisions: list) -> list:
        """
        Generate explanations for why each data point was selected.

        Example output:
        "Selected 'AI Ethics' post because:
         - 3x more engagement than average posts
         - Aligns with their recent conference talk
         - Provides unique conversation opener"
        """
        pass
```

---

## Data Schema

### Input
```json
{
    "linkedin_url": "https://linkedin.com/in/username",
    "meeting_context": "first meeting, potential partnership",
    "user_goal": "understand their priorities"
}
```

### Output (to Phase 2)
```json
{
    "profile": {
        "name": "string",
        "headline": "string",
        "current_role": "string",
        "company": "string",
        "location": "string",
        "connections": "number"
    },
    "posts": [
        {
            "content": "string",
            "date": "ISO date",
            "engagement": {"likes": 0, "comments": 0},
            "priority_score": 0.95,
            "priority_reason": "string"
        }
    ],
    "company_context": {
        "name": "string",
        "industry": "string",
        "funding": {"stage": "string", "amount": "string"},
        "recent_news": [],
        "competitors": []
    },
    "decision_metadata": {
        "total_data_points_found": 47,
        "data_points_surfaced": 5,
        "decision_rationale": []
    }
}
```

---

## Demo Script Points (for Dhruv)

During the demo, narrate:

1. **"Navigator is browsing..."** - Show the agent visiting the profile
2. **"It found 12 posts but it's prioritizing..."** - Highlight intelligent filtering
3. **"It decided this person cares about [topic]..."** - Show decision reasoning
4. **"Now checking Crunchbase... deciding if funding news matters"** - Show context-aware decisions

**Key Demo Moment:**
> "The agent found 47 data points but surfaced these 5 because they're most relevant for a first meeting."

---

## Error Handling & Fallbacks

### LinkedIn Blocks Navigator
```python
async def handle_linkedin_block(self):
    """
    Fallback if LinkedIn blocks the agent.

    Strategy:
    1. Try with different browser fingerprint
    2. Use cached data if available
    3. Pivot to company-only research
    4. Alert user and offer alternative input
    """
    pass
```

### Rate Limiting
- Implement exponential backoff
- Cache results for repeated lookups
- Queue requests if hitting limits

---

## Testing Checklist

- [ ] API connection successful
- [ ] Can browse public LinkedIn profiles
- [ ] Post prioritization logic works
- [ ] Company research returns relevant data
- [ ] Decision engine produces reasoning
- [ ] Output schema matches Phase 2 input requirements
- [ ] Handles errors gracefully
- [ ] Response time under 30 seconds

---

## Files to Create

```
src/
├── agents/
│   ├── __init__.py
│   ├── linkedin_browser.py
│   ├── company_researcher.py
│   └── decision_engine.py
├── config/
│   └── yutori_config.py
└── schemas/
    └── navigator_output.py
```

---

## Success Criteria

1. **Functional**: Successfully browse LinkedIn and extract profile data
2. **Intelligent**: Demonstrate prioritization (not just scraping)
3. **Fast**: Complete in under 30 seconds
4. **Explainable**: Generate reasoning for decisions
5. **Demo-ready**: Clear visual indicators of agent activity
