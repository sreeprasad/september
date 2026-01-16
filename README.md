<div align="center">

# <img src="https://img.icons8.com/?id=pKq5yp4WmXN0&format=png&size=48" alt="BriefMe" width="40"/> BriefMe

### AI-Powered Research & Briefing Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Next.js-14-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/FastAPI-0.68+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/AI-AgentQL-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">
</p>

<p align="center">
  <strong>Automated research, synthesis, and briefing generation.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a>
</p>

---

</div>

## <img src="https://img.icons8.com/?size=32&id=60003&format=png" alt="Features"/> Features

<table>
<tr>
<td width="50%">

### <img src="https://img.icons8.com/?id=9inONWn9EvfI&format=png&size=24" alt="Research"/> **Deep Research Agents**
Autonomous agents that browse LinkedIn, Twitter, and company websites to gather comprehensive intelligence.

</td>
<td width="50%">

### <img src="https://img.icons8.com/?id=14748&format=png&size=24" alt="Synthesis"/> **Adaptive Synthesis**
Intelligent pipeline that synthesizes raw data into structured insights, themes, and strategic talking points.

</td>
</tr>
<tr>
<td width="50%">

### <img src="https://img.icons8.com/?id=16239&format=png&size=24" alt="Compliance"/> **Compliance Analysis**
Analyzes call transcripts for regulatory violations using Claude and ElevenLabs speech-to-text.

</td>
<td width="50%">

### <img src="https://img.icons8.com/?id=63251&format=png&size=24" alt="Dashboard"/> **Interactive Dashboard**
Modern Next.js frontend for visualizing profiles, themes, and generating PDF briefings on demand.

</td>
</tr>
<tr>
<td width="50%">

### <img src="https://img.icons8.com/?id=13724&format=png&size=24" alt="Fabricate"/> **Scenario Fabrication**
Generates mock conversations, pitch simulations, and likely questions to prepare you for meetings.

</td>
<td width="50%">

### <img src="https://img.icons8.com/?size=24&id=60677&format=png" alt="PDF"/> **PDF Generation**
Automatically creates professional PDF briefings ready for download and offline use.

</td>
</tr>
</table>

---

## <img src="https://img.icons8.com/?size=32&id=2081&format=png" alt="Architecture"/> Architecture

<div align="center">

```mermaid
graph TD
    %% Users and Frontend
    User([User]) <-->|Interacts| Frontend[Next.js Frontend]
    
    subgraph "Frontend Layer"
        Frontend -->|Upload/Analyze| AnalyzePage[Analyze Page]
        Frontend -->|Input URL| HomePage[Home Page]
        Frontend -->|Generate PDF| PDFRequest[PDF Request]
    end

    %% Backend Connection
    Frontend <-->|REST API| Backend[FastAPI Server]

    subgraph "Backend Services"
        Backend -->|Orchestrates| Pipeline[Research Pipeline]
        
        %% Phase 1: Research
        subgraph "Phase 1: Research Agents"
            Pipeline -->|Browses| LinkedIn[LinkedIn Browser]
            Pipeline -->|Browses| Twitter[Twitter Browser]
            Pipeline -->|Research| Company[Company Researcher]
            
            LinkedIn <-->|AgentQL| Web1[LinkedIn]
            Twitter <-->|AgentQL| Web2[Twitter/X]
            Company <-->|AgentQL| Web3[Company Sites]
        end

        %% Phase 2: Extraction
        subgraph "Phase 2: Extraction & Analysis"
            LinkedIn & Twitter & Company --> RawData[Raw HTML/Text]
            RawData --> Extractor[Semantic Extractor]
            RawData --> ThemeEngine[Theme Engine]
            
            Extractor -->|Extracts| StructuredData[Structured Profile]
            ThemeEngine -->|Identifies| Themes[Key Themes]
            
            StructuredData & Themes --> Transformer[Data Transformer]
        end

        %% Phase 3: Synthesis
        subgraph "Phase 3: Synthesis"
            Transformer --> SynthesisPipe[Adaptive Synthesis Pipeline]
            SynthesisPipe --> Classifier[Person Classifier]
            SynthesisPipe --> Reasoning[Reasoning Chain]
            
            Classifier & Reasoning --> Insights[Strategic Insights]
        end

        %% Phase 4: Fabrication
        subgraph "Phase 4: Fabrication"
            Insights --> Fabricate[Conversation Engine]
            Fabricate --> MockGen[Mock Conversation Gen]
            Fabricate --> Coach[Response Coach]
            Fabricate --> Scenarios[Scenario Builder]
            
            MockGen & Coach & Scenarios --> SimData[Simulation Data]
        end
        
        %% Phase 5: Visualization & Output
        subgraph "Phase 5: Output"
            SimData --> Visual[Visual Generators]
            Visual --> HTMLGen[HTML Generator]
            Visual --> PDFGen[PDF Generator]
            
            PDFGen -->|Returns| PDFFile[Briefing PDF]
        end

        %% Compliance Module (Separate Flow)
        subgraph "Compliance Module"
            Backend -->|Audio/Text| Transcribe[ElevenLabs STT]
            Transcribe -->|Transcript| Analyzer[Compliance Analyzer]
            Analyzer <-->|Prompt| Claude[Anthropic Claude]
        end
    end

    %% Data Return
    Visual -->|JSON/PDF| Backend
    Backend -->|Response| Frontend
```

</div>

### Directory Structure

```
BriefMe/
├── 🐍 backend/                 # Python FastAPI Backend
│   ├── 🤖 src/agents/          # Research agents (LinkedIn, Twitter)
│   ├── 🧠 src/synthesis/       # Synthesis and reasoning pipelines
│   ├── 📝 src/extractors/      # Data extraction and transformation
│   ├── 💬 src/fabricate/       # Conversation simulation
│   └── 🎨 src/visual/          # PDF and HTML generation
├── ⚛️ frontend/                # Next.js Frontend
│   ├── 🧩 components/          # React components
│   └── 📄 app/                 # Next.js pages and routes
└── 📄 README.md                # This file
```

---

## <img src="https://img.icons8.com/?size=32&id=59881&format=png" alt="Installation"/> Installation

### Prerequisites

<table>
<tr>
<td>

**<img src="https://img.icons8.com/?size=20&id=13441&format=png" alt="Python"/> Python**
```
Python 3.8+
```

</td>
<td>

**<img src="https://img.icons8.com/?size=20&id=54087&format=png" alt="Node"/> Node.js**
```
Node.js 18+
```

</td>
<td>

**<img src="https://img.icons8.com/?size=20&id=37410&format=png" alt="Keys"/> API Keys**
```
Yutori, ElevenLabs, Anthropic
```

</td>
</tr>
</table>

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

---

## <img src="https://img.icons8.com/?size=32&id=24880&format=png" alt="Usage"/> Usage

### <img src="https://img.icons8.com/?id=13051&format=png&size=24" alt="Server"/> Running the API Server

Start the FastAPI backend to handle requests:

```bash
# From the backend directory
python api_server.py
```
The server will start at `http://localhost:8000`.

### <img src="https://img.icons8.com/?id=63251&format=png&size=24" alt="Web"/> Running the Frontend

Start the Next.js development server:

```bash
# From the frontend directory
npm run dev
```
Open `http://localhost:3000` to access the BriefMe dashboard.

### <img src="https://img.icons8.com/?size=24&id=60677&format=png" alt="CLI"/> CLI Usage

You can also run the research pipeline directly from the CLI:

```bash
# From the backend directory
python main.py
```

---

<div align="center">

### <img src="https://img.icons8.com/?size=24&id=59799&format=png" alt="Love"/> Built for Intelligence

<p>
  <img src="https://img.shields.io/badge/Made_with-❤️-red?style=for-the-badge" alt="Made with Love">
  <img src="https://img.shields.io/badge/Powered_by-Yutori-blue?style=for-the-badge" alt="Powered by Yutori">
</p>

**[⬆ Back to Top](#-briefme)**

</div>
