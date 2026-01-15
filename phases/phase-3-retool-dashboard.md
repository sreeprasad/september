# Phase 3: Retool Dashboard Setup

**Duration:** ~1 hour
**Priority:** Critical (Presentation layer)
**Judge Focus:** All judges (Visual impact), Gagan Bhat (Anthropic - "Why" panel)

---

## Overview

Retool is the visual layer that brings everything together. It displays the briefing, shows reasoning transparency, and hosts the mock conversation panel.

## Tool Information

### What is Retool?

- **Fastest way to build internal tools** with drag-and-drop GUI
- **Connects to any database or API** (REST, GraphQL, SQL)
- **100+ pre-built UI components** (tables, charts, buttons, text)
- **AI-native building blocks** for intelligent behavior
- **Enterprise-grade security** with granular permissions

### Key Features

- Real-time data binding
- Custom JavaScript/Python transforms
- Responsive design
- REST API integration
- Custom components support

### Resources

- **Main Site**: https://retool.com
- **Documentation**: https://docs.retool.com
- **Templates**: https://retool.com/templates
- **API Dashboard Template**: https://retool.com/templates/api-dashboard

---

## Implementation Steps

### Step 3.1: Retool App Setup

**Create new Retool application:**
1. Sign up/login at retool.com
2. Create new app: "Brief Me Dashboard"
3. Set up API resources for backend connection

```javascript
// Retool Resource Configuration
{
  "name": "BriefMeAPI",
  "type": "REST API",
  "baseUrl": "{{YOUR_BACKEND_URL}}",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer {{API_KEY}}"
  }
}
```

### Step 3.2: Dashboard Layout Design

**Layout Components:**

```
┌─────────────────────────────────────────────────────────────┐
│  BRIEF ME - Meeting Briefing Dashboard                      │
├─────────────────────────────────────────────────────────────┤
│  [LinkedIn URL Input]                    [Generate Button]  │
├──────────────────────┬──────────────────────────────────────┤
│                      │                                      │
│   PROFILE CARD       │     INSIGHTS PANEL                   │
│   ┌─────────────┐    │     ┌────────────────────────────┐  │
│   │  Photo      │    │     │ Theme Analysis             │  │
│   │  Name       │    │     │ • Primary: DevEx (45%)     │  │
│   │  Role       │    │     │ • AI/ML (30%)              │  │
│   │  Company    │    │     │ • Open Source (15%)        │  │
│   └─────────────┘    │     └────────────────────────────┘  │
│                      │                                      │
├──────────────────────┼──────────────────────────────────────┤
│                      │                                      │
│   TALKING POINTS     │     WHY PANEL (for Anthropic)       │
│   ┌─────────────┐    │     ┌────────────────────────────┐  │
│   │ 1. Topic A  │    │     │ "Selected because..."      │  │
│   │ 2. Topic B  │    │     │ Reasoning chain visible    │  │
│   │ 3. Topic C  │    │     │ Decision transparency      │  │
│   └─────────────┘    │     └────────────────────────────┘  │
│                      │                                      │
├──────────────────────┴──────────────────────────────────────┤
│                                                             │
│   MOCK CONVERSATIONS (for Tonic)                            │
│   ┌─────────────────────────────────────────────────────┐  │
│   │ Q: "What's your take on AI in developer tools?"      │  │
│   │ A: [Suggested response based on their interests]     │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  [Download PDF One-Pager]                    [Share Link]   │
└─────────────────────────────────────────────────────────────┘
```

### Step 3.3: Component Implementation

#### Profile Card Component

```javascript
// Retool Component: Profile Card
{
  "type": "container",
  "components": [
    {
      "type": "image",
      "source": "{{briefingData.person.photo_url}}",
      "style": { "borderRadius": "50%", "width": "100px" }
    },
    {
      "type": "text",
      "value": "{{briefingData.person.name}}",
      "style": { "fontSize": "24px", "fontWeight": "bold" }
    },
    {
      "type": "text",
      "value": "{{briefingData.person.role}} at {{briefingData.person.company}}"
    },
    {
      "type": "text",
      "value": "{{briefingData.person.professional_identity}}",
      "style": { "fontStyle": "italic", "color": "#666" }
    }
  ]
}
```

#### Theme Analysis Chart

```javascript
// Retool Component: Theme Pie Chart
{
  "type": "chart",
  "chartType": "pie",
  "data": "{{briefingData.themes.frequency_breakdown}}",
  "title": "Topic Distribution",
  "colors": ["#4F46E5", "#10B981", "#F59E0B", "#EF4444"]
}
```

#### Talking Points List

```javascript
// Retool Component: Talking Points
{
  "type": "listView",
  "data": "{{briefingData.talking_points}}",
  "itemTemplate": {
    "type": "container",
    "components": [
      {
        "type": "text",
        "value": "{{item.point}}",
        "style": { "fontWeight": "bold" }
      },
      {
        "type": "text",
        "value": "{{item.context}}",
        "style": { "fontSize": "12px", "color": "#666" }
      }
    ]
  }
}
```

### Step 3.4: "Why" Panel (Anthropic Focus)

**This is the KEY differentiator for Gagan Bhat's judging criteria.**

```javascript
// Retool Component: Reasoning Panel
{
  "type": "container",
  "title": "Why These Insights?",
  "components": [
    {
      "type": "text",
      "value": "Reasoning Transparency",
      "style": { "fontSize": "18px", "fontWeight": "bold" }
    },
    {
      "type": "listView",
      "data": "{{briefingData.reasoning_chain}}",
      "itemTemplate": {
        "type": "container",
        "components": [
          {
            "type": "text",
            "value": "{{item.decision}}",
            "style": { "fontWeight": "bold" }
          },
          {
            "type": "text",
            "value": "Because: {{item.reason}}"
          },
          {
            "type": "text",
            "value": "Evidence: {{item.evidence}}",
            "style": { "fontSize": "11px", "color": "#888" }
          }
        ]
      }
    }
  ]
}
```

**Example "Why" Panel Content:**
```json
{
  "reasoning_chain": [
    {
      "decision": "Selected 'AI Ethics' as talking point #1",
      "reason": "3x engagement on this topic vs. others",
      "evidence": "Posts from Jan-Mar 2024 averaged 450 reactions"
    },
    {
      "decision": "Prioritized recent funding news",
      "reason": "Person is executive - funding context relevant",
      "evidence": "Series B announced 2 weeks ago"
    }
  ]
}
```

### Step 3.5: Mock Conversations Panel

```javascript
// Retool Component: Mock Conversations
{
  "type": "container",
  "title": "Conversation Scenarios",
  "components": [
    {
      "type": "tabs",
      "tabs": [
        {
          "label": "Likely Questions",
          "content": {
            "type": "listView",
            "data": "{{briefingData.mock_conversations.likely_questions}}"
          }
        },
        {
          "label": "Pitch Simulation",
          "content": {
            "type": "chatWidget",
            "messages": "{{briefingData.mock_conversations.pitch_simulation}}"
          }
        }
      ]
    }
  ]
}
```

### Step 3.6: API Integration

```javascript
// Retool Query: Generate Briefing
{
  "name": "generateBriefing",
  "type": "REST API",
  "resource": "BriefMeAPI",
  "method": "POST",
  "endpoint": "/api/briefing/generate",
  "body": {
    "linkedin_url": "{{linkedinUrlInput.value}}",
    "meeting_context": "{{meetingContextSelect.value}}"
  },
  "onSuccess": [
    "briefingData.setValue(generateBriefing.data)",
    "utils.showNotification({ message: 'Briefing generated!' })"
  ]
}
```

### Step 3.7: Loading States & Animations

```javascript
// Loading State Configuration
{
  "loadingState": {
    "type": "container",
    "visible": "{{generateBriefing.isLoading}}",
    "components": [
      {
        "type": "spinner",
        "size": "large"
      },
      {
        "type": "text",
        "value": "{{loadingMessage.value}}",
        "style": { "textAlign": "center" }
      }
    ]
  }
}

// Dynamic loading messages (updated via backend events)
const loadingMessages = [
  "Navigator is browsing the profile...",
  "Deciding which posts reveal personality...",
  "Analyzing themes and sentiment...",
  "Generating talking points...",
  "Creating mock conversations...",
  "Almost ready!"
];
```

---

## Data Schema

### Expected Input (from Backend)
```json
{
  "person": {
    "name": "string",
    "photo_url": "string",
    "role": "string",
    "company": "string",
    "professional_identity": "string",
    "location": "string"
  },
  "themes": {
    "primary": "string",
    "secondary": ["string"],
    "frequency_breakdown": {
      "topic": 0.45
    }
  },
  "talking_points": [
    {
      "point": "string",
      "context": "string",
      "why_selected": "string"
    }
  ],
  "reasoning_chain": [
    {
      "decision": "string",
      "reason": "string",
      "evidence": "string"
    }
  ],
  "mock_conversations": {
    "likely_questions": [
      {
        "question": "string",
        "suggested_response": "string",
        "context": "string"
      }
    ],
    "pitch_simulation": [
      {
        "role": "them|you",
        "message": "string"
      }
    ]
  },
  "company_context": {
    "recent_news": [],
    "funding": {},
    "competitors": []
  }
}
```

---

## Demo Script Points

During the demo, highlight:

1. **Clean, professional interface** - First impression matters
2. **Real-time population** - Show data appearing as agent works
3. **"Why" panel** - Click to expand reasoning (for Gagan)
4. **Theme visualization** - Pie chart shows clear distribution
5. **Mock conversations tab** - Show prepared scenarios

**Key Demo Moment:**
> Click the "Why" panel: "Here's the reasoning chain—why each insight was selected. Full transparency into the agent's decision-making."

---

## Responsive Design

Ensure dashboard works on:
- Desktop (primary demo target)
- Tablet (backup presentation)
- Mobile (shareable link use case)

```javascript
// Responsive breakpoints
{
  "desktop": { "columns": 12, "gutters": 24 },
  "tablet": { "columns": 8, "gutters": 16 },
  "mobile": { "columns": 4, "gutters": 12 }
}
```

---

## Testing Checklist

- [ ] Dashboard loads without errors
- [ ] LinkedIn URL input works
- [ ] Generate button triggers API call
- [ ] Profile card displays correctly
- [ ] Theme chart renders accurately
- [ ] Talking points list populates
- [ ] "Why" panel shows reasoning
- [ ] Mock conversations display properly
- [ ] Loading states work smoothly
- [ ] PDF download button functional
- [ ] Responsive on different screens

---

## Files/Assets to Create

```
retool/
├── BriefMeDashboard.json     # Exported Retool app
├── components/
│   ├── ProfileCard.json
│   ├── ThemeChart.json
│   ├── TalkingPoints.json
│   ├── WhyPanel.json
│   └── MockConversations.json
├── queries/
│   ├── generateBriefing.json
│   └── downloadPDF.json
└── styles/
    └── theme.json
```

---

## Success Criteria

1. **Visual Impact**: Professional, polished appearance
2. **Functional**: All components work correctly
3. **Transparent**: "Why" panel shows clear reasoning
4. **Fast**: UI responds quickly to data updates
5. **Demo-ready**: Smooth flow for live presentation
6. **Intuitive**: Self-explanatory interface
