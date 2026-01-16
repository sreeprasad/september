# Brief Me: Implementation Phases

This folder contains detailed phase-by-phase implementation plans for the Brief Me hackathon project.

## Phase Overview

| Phase | Tool | Duration | Priority | Judge Focus |
|-------|------|----------|----------|-------------|
| [Phase 1](./phase-1-yutori-navigator.md) | Yutori Navigator | ~1 hour | Critical | Dhruv Batra ($3,500) |
| [Phase 2](./phase-2-agentql-extraction.md) | TinyFish AgentQL | ~1 hour | Critical | Homer W. |
| [Phase 3](./phase-3-retool-dashboard.md) | Retool | ~1 hour | Critical | All judges, Gagan Bhat |
| [Phase 4](./phase-4-cline-synthesis.md) | Cline + LLM | ~30-45 min | High | Juan Pablo, Gagan Bhat |
| [Phase 5](./phase-5-tonic-fabricate.md) | Tonic Fabricate | ~30 min | High | Karl Hanson |
| [Phase 6](./phase-6-freepik-visual.md) | Freepik API | ~30 min | Medium | All judges |
| [Phase 7](./phase-7-polish-demo.md) | Polish & Demo | ~30-60 min | Critical | All judges |

**Total Build Time:** ~5.5 hours

---

## Data Flow Architecture

```
LinkedIn URL
     │
     ▼
┌─────────────────┐
│  PHASE 1        │
│  Yutori         │──► Intelligent browsing + decision-making
│  Navigator      │
└────────┬────────┘
         │ Raw filtered data
         ▼
┌─────────────────┐
│  PHASE 2        │
│  TinyFish       │──► Semantic extraction + theme identification
│  AgentQL        │
└────────┬────────┘
         │ Clean JSON
         ▼
┌─────────────────┐
│  PHASE 4        │
│  Cline +        │──► Adaptive synthesis + reasoning chain
│  LLM            │
└────────┬────────┘
         │ Structured briefing
         ▼
┌─────────────────┐
│  PHASE 5        │
│  Tonic          │──► Mock conversations + Q&A scenarios
│  Fabricate      │
└────────┬────────┘
         │ Full briefing
         ▼
┌─────────────────┐
│  PHASE 3        │
│  Retool         │──► Dashboard display + "Why" panel
│  Dashboard      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PHASE 6        │
│  Freepik        │──► Visual one-pager PDF
│  API            │
└─────────────────┘
```

---

## Tool Resources Quick Reference

| Tool | Documentation | SDK |
|------|--------------|-----|
| Yutori Navigator | [yutori.com/api](https://yutori.com/api) | Python/JS |
| TinyFish AgentQL | [agentql.com](https://www.agentql.com) | `pip install agentql` |
| Retool | [retool.com](https://retool.com) | Web-based |
| Cline | [cline.bot](https://cline.bot) | VS Code Extension |
| Tonic Fabricate | [tonic.ai/fabricate](https://www.tonic.ai/products/fabricate) | Web/API |
| Freepik | [freepik.com/api](https://www.freepik.com/api) | REST API |

---

## Key Differentiators by Judge

| Judge | Company | What to Demonstrate |
|-------|---------|---------------------|
| **Dhruv Batra** | Yutori | Navigator deciding what matters, not just scraping |
| **Karl Hanson** | Tonic.AI | Fabricate for contextual prep, not just test data |
| **Homer W.** | TinyFish | Semantic theme extraction, professional identity insights |
| **Simon Tiu** | Vertex VC | $3B TAM, better than ZoomInfo/Apollo |
| **Gagan Bhat** | Anthropic | Reasoning transparency, "Why" panel |
| **Juan Pablo** | Cline | Dynamic pipeline adaptation by person type |

---

## Demo Script Summary

1. **Hook (0:15):** "Every person has walked into a meeting underprepared..."
2. **Agent Running (0:45):** Narrate Navigator decisions live
3. **Dashboard (0:30):** Highlight themes, reasoning chain
4. **Mock Conversations (0:30):** Show Fabricate output
5. **PDF Generation (0:30):** "Shareable, send before any meeting"
6. **Architecture (0:30):** Name all 6 tools
7. **Close (0:15):** One-liner pitch

**Total: 3 minutes**

---

## Quick Start

1. Read phases in order (1 → 7)
2. Set up API keys for all tools
3. Follow implementation steps in each phase
4. Test end-to-end after each phase
5. Record backup videos before demo
6. Practice demo script with timer

Good luck!
