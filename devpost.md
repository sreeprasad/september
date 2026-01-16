# BriefMe: Your AI Chief of Staff for Meeting Prep

> **Elevator Pitch**
> BriefMe is your autonomous AI research agent. It scrapes the web, synthesizes deep insights, and generates strategic briefings to help you master every meeting.

## <img src="https://img.icons8.com/?id=rXb5QD2dsojX&format=png&size=32" alt="Inspiration"/> Inspiration
We've all been there—scrambling five minutes before a crucial meeting, trying to look up the person's LinkedIn, scan their company's latest news, and figure out a decent icebreaker. Thorough research takes hours, but in a fast-paced world, we often only have minutes. We asked ourselves: **What if you had an AI Chief of Staff who could do the deep dive for you?** 

We wanted to build a tool that doesn't just "summarize" data but actually *researches* like a human analyst—browsing profiles, connecting dots between disparate sources, and even helping you practice the conversation beforehand.

## <img src="https://img.icons8.com/?id=15175&format=png&size=32" alt="What it does"/> What it does
BriefMe is an autonomous research and briefing agent that automates the entire pre-meeting workflow.

*   **Deep Research:** Autonomous agents browse LinkedIn, Twitter, and company websites to gather comprehensive intelligence on people and organizations.
*   **Adaptive Synthesis:** It doesn't just dump data; it synthesizes raw information into structured insights, identifying key themes, shared interests, and strategic talking points.
*   **Scenario Fabrication:** It helps you practice. BriefMe generates mock conversations, likely objections, and simulates the meeting so you can rehearse your pitch.
*   **Compliance Guardrails:** It analyzes past call transcripts (via ElevenLabs and Claude) to ensure your interactions remain compliant with regulations.
*   **Professional Deliverables:** Generates a beautiful, downloadable PDF briefing and presents a rich interactive dashboard for immediate consumption.

## <img src="https://img.icons8.com/?id=12205&format=png&size=32" alt="How we built it"/> How we built it
We built BriefMe using a modern, agentic architecture orchestrated by a **Python FastAPI** backend. Here is how we leveraged our key technologies:

### <img src="https://img.icons8.com/?id=9inONWn9EvfI&format=png&size=24" alt="Yutori"/> Intelligent Browsing with Yutori Navigator
We used **Yutori Navigator** to power our browsing agents, but we went beyond simple scraping. Instead of just visiting a URL, our agents use Yutori's decision-making capabilities to *prioritize* information. 
*   **Novel Use Case:** The agent doesn't just grab the last 5 posts. It analyzes engagement and content to decide *which* posts reveal the person's true professional identity, ignoring generic company reposts.

### <img src="https://img.icons8.com/?id=11973&format=png&size=24" alt="AgentQL"/> Semantic Extraction with TinyFish AgentQL
Traditional selectors break whenever a website updates. We used **TinyFish AgentQL** to query data semantically.
*   **Novel Use Case:** We used AgentQL's self-healing selectors to build a "Theme Engine." By querying for *intent* rather than just DOM elements, we could extract abstract concepts like "Passion Topics" and "Communication Style" directly from raw profile data.

### <img src="https://img.icons8.com/?id=63251&format=png&size=24" alt="Retool"/> Visual Intelligence with Retool
We built our entire frontend dashboard in **Retool** to create a professional, interactive experience in record time.
*   **Novel Use Case:** We implemented a "Why Panel" (Reasoning Transparency). When the AI suggests a talking point, users can click to see the exact reasoning chain and evidence source, building trust in the agent's output.

### <img src="https://img.icons8.com/?id=13724&format=png&size=24" alt="Tonic"/> Role-Play Simulation with Tonic Fabricate
Most people use **Tonic Fabricate** for test data. We used it to generate *preparation scenarios*.
*   **Novel Use Case:** We feed the synthesized profile intelligence into Fabricate to generate a "Mock Conversation." The AI simulates the person you're about to meet—mimicking their tone and interests—allowing you to role-play your pitch before the actual meeting.

### <img src="https://img.icons8.com/?id=114320&format=png&size=24" alt="Freepik"/> Professional Output with Freepik
To make the briefing shareable, we use **Freepik's API** to generate a polished one-pager.
*   **Novel Use Case:** We use Freepik to enhance profile photos and generate custom thematic icons for the PDF, turning raw text data into a visually stunning document you can take offline.

### <img src="https://img.icons8.com/?id=2081&format=png&size=24" alt="Architecture"/> Architecture

![Architecture Diagram](https://mermaid.ink/img/Z3JhcGggVEQKICAgICUlIFVzZXJzIGFuZCBGcm9udGVuZAogICAgVXNlcihbVXNlcl0pIDwtLT58SW50ZXJhY3RzfCBGcm9udGVuZFtOZXh0LmpzIEZyb250ZW5kXQogICAgCiAgICBzdWJncmFwaCAiRnJvbnRlbmQgTGF5ZXIiCiAgICAgICAgRnJvbnRlbmQgLS0+fFVwbG9hZC9BbmFseXplfCBBbmFseXplUGFnZVtBbmFseXplIFBhZ2VdCiAgICAgICAgRnJvbnRlbmQgLS0+fElucHV0IFVSTHwgSG9tZVBhZ2VbSG9tZSBQYWdlXQogICAgICAgIEZyb250ZW5kIC0tPnxHZW5lcmF0ZSBQREZ8IFBERlJlcXVlc3RbUERGIFJlcXVlc3RdCiAgICBlbmQKCiAgICAlJSBCYWNrZW5kIENvbm5lY3Rpb24KICAgIEZyb250ZW5kIDwtLT58UkVTVCBBUEl8IEJhY2tlbmRbRmFzdEFQSSBTZXJ2ZXJdCgogICAgc3ViZ3JhcGggIkJhY2tlbmQgU2VydmljZXMiCiAgICAgICAgQmFja2VuZCAtLT58T3JjaGVzdHJhdGVzfCBQaXBlbGluZVtSZXNlYXJjaCBQaXBlbGluZV0KICAgICAgICAKICAgICAgICAlJSBQaGFzZSAxOiBSZXNlYXJjaAogICAgICAgIHN1YmdyYXBoICJQaGFzZSAxOiBSZXNlYXJjaCBBZ2VudHMiCiAgICAgICAgICAgIFBpcGVsaW5lIC0tPnxCcm93c2VzfCBMaW5rZWRJbltMaW5rZWRJbiBCcm93c2VyXQogICAgICAgICAgICBQaXBlbGluZSAtLT58QnJvd3Nlc3wgVHdpdHRlcltUd2l0dGVyIEJyb3dzZXJdCiAgICAgICAgICAgIFBpcGVsaW5lIC0tPnxSZXNlYXJjaHwgQ29tcGFueVtDb21wYW55IFJlc2VhcmNoZXJdCiAgICAgICAgICAgIAogICAgICAgICAgICBMaW5rZWRJbiA8LS0+fEFnZW50UUx8IFdlYjFbTGlua2VkSW5dCiAgICAgICAgICAgIFR3aXR0ZXIgPC0tPnxBZ2VudFFMfCBXZWIyW1R3aXR0ZXIvWF0KICAgICAgICAgICAgQ29tcGFueSA8LS0+fEFnZW50UUx8IFdlYjNbQ29tcGFueSBTaXRlc10KICAgICAgICBlbmQKCiAgICAgICAgJSUgUGhhc2UgMjogRXh0cmFjdGlvbgogICAgICAgIHN1YmdyYXBoICJQaGFzZSAyOiBFeHRyYWN0aW9uICYgQW5hbHlzaXMiCiAgICAgICAgICAgIExpbmtlZEluICYgVHdpdHRlciAmIENvbXBhbnkgLS0+IFJhd0RhdGFbUmF3IEhUTUwvVGV4dF0KICAgICAgICAgICAgUmF3RGF0YSAtLT4gRXh0cmFjdG9yW1NlbWFudGljIEV4dHJhY3Rvcl0KICAgICAgICAgICAgUmF3RGF0YSAtLT4gVGhlbWVFbmdpbmVbVGhlbWUgRW5naW5lXQogICAgICAgICAgICAKICAgICAgICAgICAgRXh0cmFjdG9yIC0tPnxFeHRyYWN0c3wgU3RydWN0dXJlZERhdGFbU3RydWN0dXJlZCBQcm9maWxlXQogICAgICAgICAgICBUaGVtZUVuZ2luZSAtLT58SWRlbnRpZmllc3wgVGhlbWVzW0tleSBUaGVtZXNdCiAgICAgICAgICAgIAogICAgICAgICAgICBTdHJ1Y3R1cmVkRGF0YSAmIFRoZW1lcyAtLT4gVHJhbnNmb3JtZXJbRGF0YSBUcmFuc2Zvcm1lcl0KICAgICAgICBlbmQKCiAgICAgICAgJSUgUGhhc2UgMzogU3ludGhlc2lzCiAgICAgICAgc3ViZ3JhcGggIlBoYXNlIDM6IFN5bnRoZXNpcyIKICAgICAgICAgICAgVHJhbnNmb3JtZXIgLS0+IFN5bnRoZXNpc1BpcGVbQWRhcHRpdmUgU3ludGhlc2lzIFBpcGVsaW5lXQogICAgICAgICAgICBTeW50aGVzaXNQaXBlIC0tPiBDbGFzc2lmaWVyW1BlcnNvbiBDbGFzc2lmaWVyXQogICAgICAgICAgICBTeW50aGVzaXNQaXBlIC0tPiBSZWFzb25pbmdbUmVhc29uaW5nIENoYWluXQogICAgICAgICAgICAKICAgICAgICAgICAgQ2xhc3NpZmllciAmIFJlYXNvbmluZyAtLT4gSW5zaWdodHNbU3RyYXRlZ2ljIEluc2lnaHRzXQogICAgICAgIGVuZAoKICAgICAgICAlJSBQaGFzZSA0OiBGYWJyaWNhdGlvbgogICAgICAgIHN1YmdyYXBoICJQaGFzZSA0OiBGYWJyaWNhdGlvbiIKICAgICAgICAgICAgSW5zaWdodHMgLS0+IEZhYnJpY2F0ZVtDb252ZXJzYXRpb24gRW5naW5lXQogICAgICAgICAgICBGYWJyaWNhdGUgLS0+IE1vY2tHZW5bTW9jayBDb252ZXJzYXRpb24gR2VuXQogICAgICAgICAgICBGYWJyaWNhdGUgLS0+IENvYWNoW1Jlc3BvbnNlIENvYWNoXQogICAgICAgICAgICBGYWJyaWNhdGUgLS0+IFNjZW5hcmlvc1tTY2VuYXJpbyBCdWlsZGVyXQogICAgICAgICAgICAKICAgICAgICAgICAgTW9ja0dlbiAmIENvYWNoICYgU2NlbmFyaW9zIC0tPiBTaW1EYXRhW1NpbXVsYXRpb24gRGF0YV0KICAgICAgICBlbmQKICAgICAgICAKICAgICAgICAlJSBQaGFzZSA1OiBWaXN1YWxpemF0aW9uICYgT3V0cHV0CiAgICAgICAgc3ViZ3JhcGggIlBoYXNlIDU6IE91dHB1dCIKICAgICAgICAgICAgU2ltRGF0YSAtLT4gVmlzdWFsW1Zpc3VhbCBHZW5lcmF0b3JzXQogICAgICAgICAgICBWaXN1YWwgLS0+IEhUTUxHZW5bSFRNTCBHZW5lcmF0b3JdCiAgICAgICAgICAgIFZpc3VhbCAtLT4gUERGR2VuW1BERiBHZW5lcmF0b3JdCiAgICAgICAgICAgIAogICAgICAgICAgICBQREZHZW4gLS0+fFJldHVybnN8IFBERkZpbGVbQnJpZWZpbmcgUERGXQogICAgICAgIGVuZAoKICAgICAgICAlJSBDb21wbGlhbmNlIE1vZHVsZSAoU2VwYXJhdGUgRmxvdykKICAgICAgICBzdWJncmFwaCAiQ29tcGxpYW5jZSBNb2R1bGUiCiAgICAgICAgICAgIEJhY2tlbmQgLS0+fEF1ZGlvL1RleHR8IFRyYW5zY3JpYmVbRWxldmVuTGFicyBTVFRdCiAgICAgICAgICAgIFRyYW5zY3JpYmUgLS0+fFRyYW5zY3JpcHR8IEFuYWx5emVyW0NvbXBsaWFuY2UgQW5hbHl6ZXJdCiAgICAgICAgICAgIEFuYWx5emVyIDwtLT58UHJvbXB0fCBDbGF1ZGVbQW50aHJvcGljIENsYXVkZV0KICAgICAgICBlbmQKICAgIGVuZAoKICAgICUlIERhdGEgUmV0dXJuCiAgICBWaXN1YWwgLS0+fEpTT04vUERGfCBCYWNrZW5kCiAgICBCYWNrZW5kIC0tPnxSZXNwb25zZXwgRnJvbnRlbmQK)

## <img src="https://img.icons8.com/?id=KarJz0n4bZSj&format=png&size=32" alt="Challenges"/> Challenges we ran into
*   **Data Noise:** The internet is noisy. Early versions of our agents grabbed too much irrelevant text. We had to refine our `extraction_output` schemas and use our custom "Theme Engines" to filter for signal over noise.
*   **Agent Reliability:** Dynamic websites change often. Traditional scraping broke constantly. Switching to an AI-powered query language (AgentQL) was a game-changer but required us to rethink how we structure our data queries.
*   **Pipeline Latency:** Chaining multiple AI calls (Research -> Extract -> Synthesize -> Fabricate) can be slow. We had to optimize the async flows in our FastAPI backend to ensure the user wasn't waiting forever for their briefing.

## <img src="https://img.icons8.com/?id=16951&format=png&size=32" alt="Accomplishments"/> Accomplishments that we're proud of
*   **The "Scenario Builder":** We're particularly proud of the fabrication module. Seeing the AI generate a realistic role-play script based on a person's actual tweets and LinkedIn history feels like magic.
*   **Seamless PDF Generation:** Generating a professional-grade PDF dynamically from the analyzed data was a tricky engineering hurdle that adds immense real-world value.
*   **End-to-End Automation:** Going from a single name or URL to a comprehensive dossier without human intervention is a massive productivity unlock.

## <img src="https://img.icons8.com/?id=14748&format=png&size=32" alt="Learnings"/> What we learned
*   **Structured Data is King:** LLMs are great at text, but software needs structure. Forcing our agents to adhere to strict Pydantic models (Schemas) was crucial for building a reliable application.
*   **Context Windows Matter:** We learned how to efficiently manage context when passing data between the researcher agents and the synthesis engine to avoid "forgetting" key details or hallucinating.

## <img src="https://img.icons8.com/?id=ZAtOouDQCiIu&format=png&size=32" alt="Next Steps"/> What's next for BriefMe
*   **Calendar Integration:** Automatically triggering research 24 hours before every meeting on your Google Calendar.
*   **Real-time Coaching:** A live "copilot" mode that listens during the meeting and nudges you with facts or compliance warnings in real-time.
*   **CRM Sync:** Pushing the synthesized insights directly into Salesforce or HubSpot to keep client records updated automatically.

## <img src="https://img.icons8.com/?id=59881&format=png&size=32" alt="GitHub"/> Try it out
Check out the source code and contribute: [GitHub Repository](https://github.com/sreeprasad/september)
