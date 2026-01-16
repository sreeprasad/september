# Implementation Steps: Brief Me

## 💡 Recommendation: Web App vs. Retool
**Suggestion:** Build a **Next.js (React) Web App** instead of Retool.

**Why?**
1.  **"Real Product" Feel:** You are pitching a "ZoomInfo killer" ($3B TAM), not an internal tool. A custom UI looks like a polished SaaS product.
2.  **Visual Control:** Essential for the "Visual One-Pager" and the "Decision Transparency" panels (impressing Gagan).
3.  **Demo Impact:** Easier to implement a slick "Progress Bar" that narrates the agent's actions ("Now analyzing sentiment...", "Found 3 relevant posts...") which is key to the "Autonomy" score.

**Demo Strategy:**
*   **Split Screen:** 
    *   **Left (User View):** The polished Web App. Clean, simple.
    *   **Right (Agent View):** A scrolling terminal or log window showing Yutori/TinyFish's raw "thoughts" and decisions (Matrix style). This proves it's real and autonomous.

---

## ⏱️ Short Plans (Hour-by-Hour)

### Phase 1: Infrastructure & "The Eyes" (Hour 0-1.5)
**Goal:** Can we visit a URL and get raw HTML/Screenshots?
1.  **Setup:** Initialize Next.js project (frontend) and a Python/Node backend (agent).
2.  **Yutori Integration:**
    *   Implement `browse_profile(url)`: Use Yutori to navigate to LinkedIn.
    *   Implement `scroll_and_capture()`: Ensure dynamic content loads.
    *   *Win Condition:* A script that takes a URL and saves the page content/screenshot locally.

### Phase 2: "The Brain" - Extraction & Meaning (Hour 1.5-3)
**Goal:** Turn raw pixels into structured insight.
1.  **TinyFish Integration:**
    *   Feed Yutori's output to TinyFish.
    *   Create `extract_profile_data()`: Name, Role, Company, History.
    *   Create `analyze_posts()`: Extract themes (e.g., "AI Ethics", "Developer Exp") and sentiment.
2.  **Logic & Decisions (The "Judge Pleaser"):**
    *   Write the selection logic: "If posts > 5, select top 3 by engagement" OR "If Engineer, prioritize GitHub links."
    *   *Win Condition:* JSON object with cleaned profile data and "Identified Themes".

### Phase 3: "The Prep" - Synthesis & Simulation (Hour 3-4)
**Goal:** Generate the talking points and mock conversations.
1.  **Cline Integration:**
    *   Prompt: "Given [JSON Data], generate 3 talking points for a [Meeting Type] meeting."
    *   *Crucial:* Dynamic prompt generation based on role (CTO vs. VC).
2.  **Tonic Fabricate:**
    *   Prompt: "Generate a mock dialogue between User and [Profile Name] about [Theme]."
    *   *Win Condition:* Final JSON containing Profile, Talking Points, and Mock Q&A.

### Phase 4: "The Face" - UI & One-Pager (Hour 4-5)
**Goal:** Make it look beautiful and downloadable.
1.  **Frontend Build:**
    *   Input field (centered, big).
    *   **Live Status Component:** Shows "Browsing...", "Reasoning...", "Generating..." updates.
    *   **Dashboard View:** Cards for "Who", "What they care about", "Talking Points".
2.  **Freepik Integration:**
    *   Map the Final JSON to a visual template.
    *   Generate the image/PDF.
    *   Add "Download PDF" button.

### Phase 5: Polish & Rehearsal (Hour 5-5.5)
1.  **Error Handling:** What if LinkedIn blocks? (Switch to Backup Mode: Company Search).
2.  **Latency Masking:** Add engaging "loading facts" or live logs if it takes >30s.
3.  **Demo Practice:** Time the "Hands up" intro and the specific call-outs to judges.
