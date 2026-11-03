# Implementation teardowns of the Cerebral Valley x Anthropic "Built with Opus 4.6" and "Built with Opus 4.7" winners, and what we can reuse for a Meta-model build

Scope note for the report writer. I read the winners' GitHub repos through `gh api`, raw files and tarball snapshots (no code was run), plus the official winner pages, the Cerebral Valley gallery pages, the YouTube metadata for each demo video, and the builders' own logs (CrossBeam `progress.md`, PostVisit `BUILD-LOG.md`, MedKit `docs/evolution.md` and `spec.md`, ARIA `docs/ARIA_PRD.md`). All counts marked "counted" were computed by me from the GitHub API on Nov 3 2026, at the commit closest to each event's deadline where that was possible: Feb 16 2026 20:00 UTC for Opus 4.6 (deadline was 3:00 PM EST) and Apr 27 2026 for Opus 4.7. Test counts are `it(`/`test(` calls in TS/JS plus `def test_` in Python. LOC is raw line count of .ts/.tsx/.js/.py/.c/.rs files excluding node_modules/vendor, so it includes tests and data files. I could not watch the videos or pull their captions (YouTube caption endpoints returned nothing), so "what the video showed" comes from the builders' own written beat sheets, shot lists and video descriptions; it is marked as planned/declared, not verified.

Event basics used below:
- Opus 4.6 ran Feb 10–16 2026. Submissions were a ≤3-minute video, an open-source repo and a 100–200-word summary. Rules required "New Work Only" and "fully open source". Stage-1 rubric: Impact 25%, Opus 4.6 Use 25%, Depth & Execution 20%, Demo 30% — [rules copy in CrossBeam repo](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/docs/hackathon/hackathon-rules.md)
- Opus 4.7 ran Apr 21–26 2026 per [GIGAZINE](https://gigazine.net/gsc_news/en/20260425-anthropic-hackathon/) and the [Wrench Board video description](https://www.youtube.com/watch?v=OZ2D_p82z6w). The Virtual Puppet Theater README banner says "April 21–28" ([README](https://github.com/rhmoller/virtual-puppet-theater)), which probably includes judging (inference). ARIA's PRD copies the 4.7 rubric as **Impact 30%, Demo 25%, Opus 4.7 Use 25%, Depth & Execution 20%** ([ARIA PRD §6](https://github.com/zestones/Aria/blob/main/docs/ARIA_PRD.md)). That is exactly Meta's weighting. I found no official copy of the 4.7 rules to confirm it; a search turned up only the 4.6 rubric ([HF mirror of 4.6 rules](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/docs/hackathon-rules.md)).

## Q1. What concrete architecture did each winner use, and how much of it was built during the event?

### Takeaway
Every placed project was a **multi-stage pipeline around a deterministic, non-LLM core**: a CBA engine, a C/WASM sequencer, a circuit simulator, TimescaleDB thresholds, a curated guideline registry or drug APIs. Each pipeline gave the model 3–6 distinct roles (vision extraction, planning, tool-using agent, grader, narrator), often routed across model tiers, and each showed the agent working live in the UI. Repo history shows the code was written during the event week: first commits fall on kickoff day, and there were 12 to 373 commits by the deadline. The exceptions are Wrench Board, whose public history was rewritten in June, and MedKit, which was squashed to a single commit.

### Cited Findings

#### Opus 4.6 — 1st: CrossBeam (Mike Brown, personal-injury lawyer)
- **Repo and license:** [mikeOnBreeze/cc-crossbeam](https://github.com/mikeOnBreeze/cc-crossbeam), **MIT**. Created Feb 11 2026; 297 stars. The README says "This repository is the hackathon snapshot, not the current product" — [README](https://github.com/mikeOnBreeze/cc-crossbeam)
- **Depth (counted):** 63 commits at the deadline (71 now). 752 files at the deadline, but ~440 of them are vendored or authored skill files under `.claude/skills` and `adu-skill-development/skill`. 84 app code files, ~361 KB. 11 layered pipeline test scripts: `test-l0-smoke`, `test-l0c-smoke-city`, `test-l1-skill-invoke`, `test-l1c-skill-read`, `test-l2-subagent-bash`, `test-l3-mini-pipeline`, `test-l3b/c/d`, `test-l4-full-pipeline`, `test-l4c-full-review`. Plus 5 test-plan docs under `docs/testing/` (~180 KB) — [agents-crossbeam/src/tests](https://github.com/mikeOnBreeze/cc-crossbeam/tree/main/agents-crossbeam/src/tests)
- **Architecture:** Next.js 16 / React 19 / shadcn front end → Express 5 orchestrator on Cloud Run → each job in an isolated Vercel Sandbox running the Claude Agent SDK `claude_code` preset plus skills → Supabase (Postgres, Realtime, Storage). Cloud Run was chosen because "Agent runs take 10-30 minutes" and serverless functions time out at 60–300 s — [README](https://github.com/mikeOnBreeze/cc-crossbeam)
- **How the model was used:**
  - **Skills, not prompts.** A California ADU skill has 28 reference files: the 54-page HCD handbook, Gov Code §§66310-66342, a decision-tree router and a thresholds table. Other skills cover corrections interpretation, three-mode city research (WebSearch → WebFetch → browser fallback) and ops — [README](https://github.com/mikeOnBreeze/cc-crossbeam). The gallery summary says 13 custom skills "all running concurrently" — [CV gallery #54](https://cerebralvalley.ai/e/claude-code-hackathon/hackathon/gallery/54)
  - **A 4-phase flow writes 8 JSON artifacts to a session dir:** `corrections_parsed.json` → `sheet-manifest.json` → `state_law_findings.json` / `city_discovery.json` / `sheet_observations.json` / `city_research_findings.json` → `corrections_categorized.json` + `contractor_questions.json`. Then Skill 2 writes `response_letter.md`, `professional_scope.md`, `corrections_report.md` and `sheet_annotations.json`. `verify.ts` detects which phases completed from which files exist — [corrections-analysis.ts](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/agents-crossbeam/src/flows/corrections-analysis.ts); [verify.ts](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/agents-crossbeam/src/utils/verify.ts)
  - **Vision via subagents:** PDF → PNG per page, with each page sent to a vision subagent "in batches of 3 subagents". A manifest maps PDF pages to sheet labels (A3, S1, E2), because corrections letters cite sheet labels, not page numbers — [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **What was hard and how he solved it** (all from [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)):
  - **Extraction accuracy vs. time.** "85% accuracy: 10–15 minutes for a 26-page binder… 95% accuracy: 35 minutes". He pivoted to a "targeted page viewer" that reads the corrections letter first and opens only the ~6 relevant sheets.
  - **Browser tools were too slow** for city websites. Replaced with web search, direct fetch, then explore subagents on specific URLs.
  - **Subagents "stepping on each other".** Moved to "file-based coordination": each subagent writes its own output file and the lead agent reads them. Added "mandatory subagent rules to prevent context window blowout".
  - **Sandbox limits.** The 4 GB Vercel Sandbox couldn't run pdftoppm on 7,400-px pages, so extraction moved to Cloud Run. Cloud Run's timeout was raised to 60 min. PDF generation was dropped and the agent "ends at markdown".
  - **Pre-baking for speed.** City research and the binder manifest were pre-loaded for onboarded cities.
- **Operational numbers:** "City review: 16 minutes, $8.69. Contractor analysis: 11 minutes, $4.46. Contractor response: 6 minutes, $1.46. Full contractor E2E: 17 minutes, $5.92" — [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **Demo mode** — [app-mode.ts](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/frontend/lib/app-mode.ts); [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md); [seed-demo-outputs.mjs](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/scripts/seed-demo-outputs.mjs):
  - `AppMode = 'dev-test' | 'judge-demo' | 'real'`, with pinned `SHOWCASE_*_OUTPUT_ID`s for "the best curated run for each flow".
  - A DevTools scrubber steps through agent states with scripted data.
  - 45 minutes before the deadline he realized the judge demo only showed finished output: "It looks like I faked the output." He added "Showcase + Run Live dual-button mode" and reset-before-run in "8 commits in 12 minutes".
  - Demo data is seeded from real session runs.
- **Video:** 180 s ([YouTube](https://www.youtube.com/watch?v=jHwBkFSvyk0)). It took a whole day, in a separate repo. It includes interviews with the Mayor of Buena Park ("the 'impact' angle for the judges (25% of the score)") and the contractor whose letter inspired the project; screen recordings of the deployed app; Remotion-animated shots (hero, architecture diagram, contractor flow, agent-working animation, blueprint pan, "Accuracy + logo bumper"); and licensed music, cut in Premiere — [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **Landing page for judges:** at ~3–4 AM on deadline day he rewrote it as a "technical deep-dive": a 4-step pipeline diagram, "28 Files, Not One Prompt", "One Page Per Subagent", "480 Cities, 3 Research Modes", "Why Three Layers", a stats strip, and a working / in-progress / roadmap status board — [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **README structure:** what it is now (with traction: Laguna Beach 12-month agreement approved Aug 4 2026; Buena Park PreCheck launched Oct 5 2026) → "History: hackathon" → pointer to the `progress.md` voice log → problem → three flows → architecture diagram plus a "why this architecture" list → skills-first design → tech-stack table → project tree → run locally → test-data attribution → license — [README](https://github.com/mikeOnBreeze/cc-crossbeam)

#### Opus 4.6 — 2nd: Elisa (Jon McBee, software engineer)
- **Repo and license:** [zoidbergclawd/elisa](https://github.com/zoidbergclawd/elisa), **MIT**. First commit Feb 10 17:57 UTC — [commits](https://github.com/zoidbergclawd/elisa/commits/main)
- **Depth (counted at deadline commit 1581b128):** 85 commits (331 now); 291 files; 112 test files; **1,521 test cases**; **39,586 LOC**. This matches the official "76 commits, more than 39,000 lines of code, and more than 1,500 tests" — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon). My count is 85 commits against their 76, probably because of the submission timestamp (inference). The same blog says "Built in 30 hours" but quotes Jon saying "only six days"; the commits span Feb 10–16.
- **Architecture:** Electron shell → React 19 + Vite + Blockly SPA ↔ REST + WebSocket ↔ Express 5 server. The 4-phase pipeline is plan → execute → test → deploy. A **meta-planner** turns a Zod-validated `NuggetSpec` into a task DAG. Up to **3 agents run in parallel via a streaming `Promise.race` pool**. Each agent is an isolated Agent SDK `query()`. There is no database (in-memory state with JSON persistence), a per-session git repo, a test runner, ESP32 flashing, a teaching engine, and a narrator on Haiku — [README](https://github.com/zoidbergclawd/elisa)
- **How the model was used:**
  - **Meta-planner:** the plan is parsed from JSON (fences stripped) with one retry, then validated. It must have `tasks`, a non-empty array, unique ids, and `dependencies` on every task — [metaPlanner.ts](https://github.com/zoidbergclawd/elisa/blob/main/backend/src/services/metaPlanner.ts)
  - **Agent runner:** `maxTurns = 25`, `permissionMode: 'bypassPermissions'`, and per-task `total_cost_usd` and input/output tokens captured — [agentRunner.ts](https://github.com/zoidbergclawd/elisa/blob/main/backend/src/services/agentRunner.ts)
- **Trace UI (MIT, React):**
  - `MissionControl/`: TaskDAG, CommsFeed, MetricsPanel, NarratorFeed, MinionSquadPanel
  - `BottomBar/`: GitTimeline, TestResults, ProgressPanel, TeachingSidebar, BoardOutput
  - Each component has a `.test.tsx` — [frontend/src/components](https://github.com/zoidbergclawd/elisa/tree/main/frontend/src/components)
- **Build timeline from commit messages:**
  - A PRD day plan: "Scaffold Day 1 skeleton" (Feb 10), "Implement Day 2: meta-planner, task DAG", "Day 3: full orchestration loop, git integration, test infrastructure", "Day 4: teaching layer, test visualization, comms feed, token metrics", "Day 5: hardware integration".
  - "Rewrite backend from Python/FastAPI to TypeScript/Express" (Feb 11 03:36 UTC) and "Migrate from CLI subprocess to Claude Agent SDK" (Feb 11 23:29 UTC) — [commits](https://github.com/zoidbergclawd/elisa/commits/main)
- **Video:** 176 s. "a demo and explanation of what the Elisa project is, why I built it, and how it is already being used today" (his daughter's science-fair use) — [YouTube](https://www.youtube.com/watch?v=rsUaz_QAK6o); [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)
- **README structure:** logo, badges (MIT, React, TS, CI) and demo GIF → what it is → download → dev quickstart → features → a "primitive → AI engineering concept" table → ASCII architecture → project tree → docs index → env-var table → license — [README](https://github.com/zoidbergclawd/elisa)

#### Opus 4.6 — 3rd: PostVisit.ai (Michał Nedoszytko, cardiologist)
- **Repo and license:** the GitHub link given on the gallery page, `github.com/mnedoszytko/postvisit` ([CV gallery #81](https://cerebralvalley.ai/e/claude-code-hackathon/hackathon/gallery/81)), now returns 404. An **MIT-licensed** mirror ("Migrated from GitHub") exists at [huggingface.co/datasets/introvoyz041/postvisit](https://huggingface.co/datasets/introvoyz041/postvisit). Its LICENSE reads "Copyright (c) 2026 PostVisit.ai". The mirror is third-party, so treat it with care.
- **Depth:** "349 commits in 7 days"; "262 feature tests covering all API modules with 797 assertions… with mocked AI services"; Claude Code ran as "multiple parallel instances" — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md); [BUILD-LOG (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
- **Architecture:** Laravel 12 (PHP 8.4) + Vue 3/Tailwind SPA, PostgreSQL 17 (UUID, jsonb, FHIR-aligned), SSE streaming, Sanctum auth. Prompts are versioned as files in `prompts/` — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
- **How the model was used** — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md):
  - "Reverse AI Scribe" with audio chunking for 30+ min visits
  - "8-layer context assembly … Typical: 60K-180K tokens" using the 1M context
  - An agentic tool loop with 5 medical tools (RxNorm interactions, OpenFDA/DailyMed, lab reference ranges, guideline search, adverse events)
  - Per-subsystem extended-thinking budgets of 1K–16K
  - Prompt caching with a "78% reduction in input token costs"
  - "Plan-Execute-Verify" clinical reasoning
  - Thinking-backed escalation detection
- **3-tier comparison, shown live in the demo.** A toggle switches between "Good (Sonnet)", "Better (Opus)" and "Opus 4.6 (Full)" (thinking budget 0 / 16K / 34K, guidelines none / none / full-text PMC). "Switching tiers in real-time during the demo shows the progressive improvement" — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
- **Hard problems:**
  - He found a buffering bug in the Anthropic PHP SDK and "Built a raw cURL streaming layer".
  - Hospital testing (with consent) surfaced long-recording loss (fixed with chunking) and an iPhone sleeping mid-recording (fixed with the Wake Lock API).
  - Demo rate limiting was "too aggressive".
  - Sources: [README](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md); [BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
- **Demo mode:** a "multi-scenario demo engine" with 12 clinical scenarios; `POST /api/v1/demo/start` with no auth; a `DemoSeeder`; and a 10-endpoint Demo API (start, status, reset, simulate alerts, switch role). The live site auto-authenticates — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
- **Video:** 179 s ([YouTube](https://youtu.be/V29UCOii2jE)). It includes footage filmed in a real hospital with consenting patients. "The demo video was the single biggest time sink of the project"; he re-recorded "because the UI kept evolving" — [BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)

#### Opus 4.6 — Keep Thinking: TARA (Kyeyune Kazibwe, transport engineer, Uganda)
- **Repo and license:** [Kye256/tara-transport-assessment](https://github.com/Kye256/tara-transport-assessment), **MIT**
- **Depth (counted):** 49 commits at the deadline (54 now; first "Initial commit" Feb 11); 80 files; 37 code files, ~476 KB. One validator script, "12 checks on GeoJSON output" — [video/test_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py). Commit messages track it: "Fix video pipeline: 11/11 validator checks passing" → "Video pipeline: 12/12 validator passing" — [commits](https://github.com/Kye256/tara-transport-assessment/commits/main)
- **Architecture:**
  - Python Dash app (7-step wizard), dash-leaflet, Plotly, FPDF2
  - `agent/orchestrator.py` ("Agent loop with tool_use"), `tools.py`, `prompts.py`
  - `engine/`: cba.py (NPV, EIRR, BCR, FYRR), traffic, sensitivity, equity, deterioration
  - `video/`: frames, GPS matching, vision assessment, condition map, interventions
  - A local DB of 738 Uganda roads
  - Source: [README](https://github.com/Kye256/tara-transport-assessment)
- **How the model was used (vision)** — [vision_assess.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/vision_assess.py):
  - One Opus call per frame, with a "Respond ONLY with valid JSON" prompt. The prompt embeds the schema (surface_type, condition_class, iri_estimate, distress_types, plus an activity_profile of people, vehicles, facilities and NMT).
  - Markdown fences are regex-stripped; there are 2 attempts, then a `DEFAULT_ASSESSMENT` fallback.
  - `assess_frame_mock()` is a deterministic cycling mock "for reproducible testing without API".
  - Frames are selected by **GPS distance** (`interval_meters=25` default), not time — [video_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/video_pipeline.py)
- **Cache and demo mode:** cache path = md5(`video_path:gpx_path:interval`), with base64 images stripped before caching. Three cached pipeline JSONs (4–5 MB each) ship in `data/videos/*/cache/`, so "Anthropic API key (optional — cached demo data included)" — [video_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/video_pipeline.py); [README](https://github.com/Kye256/tara-transport-assessment)
- **Build process:** `docs/` holds ~20 Claude Code build prompts (`TARA_VIDEO_BUILD_PROMPT.md`, `TARA_EQUITY_BUILD_PROMPT.md`, `TARA_UX_AUDIT_PROMPT.md`, `TARA_PDF_FIX_PROMPT.md` …), plus `AUDIT_REPORT.md` and `UX_AUDIT.md` — [docs/](https://github.com/Kye256/tara-transport-assessment/tree/main/docs). The README says "Multi-agent development with hooks for autonomous operation" — [README](https://github.com/Kye256/tara-transport-assessment)
- **Video:** 180 s, "dashcam footage → condition assessment → economic analysis → equity scoring → PDF report", tested on real footage near Kampala — [README](https://github.com/Kye256/tara-transport-assessment); [YouTube](https://www.youtube.com/watch?v=GFCrXehS1DE)
- **README structure:** winner badge → tagline ("A $56 dashcam doing the job of an $800,000 survey van") → video thumbnail → 2×2 screenshot grid → what it does → problem ($181B/yr need; "80% of projects fail at feasibility") → a "How Claude Opus 4.6 Is Used" bullet list → quickstart (works without an API key) → tech-stack table → project tree → author → license — [README](https://github.com/Kye256/tara-transport-assessment)

#### Opus 4.6 — Creative Exploration: Conductr (Asep Bagja Priandana)
- **Repo and license:** [nanassound/conductr](https://github.com/nanassound/conductr), **Apache-2.0**. 12 commits (Feb 11–14); no test cases found (counted). "~4,800 LOC" (1,134 lines of C + 3,656 of JS) — [README](https://github.com/nanassound/conductr)
- **Architecture: three timescales.**
  - A C → WASM engine at "~15 ms per step"
  - A JS performance analyzer "every ~4 seconds"
  - The Opus director "every ~8 seconds" (or immediately on a voice/text command)
  - "The engine never waits for Opus. Opus shapes the next phrase, not the current note"
  - The director returns JSON: `musical_intent`, `params`, `transition`, `suggestion`
  - It keeps the last 10 exchanges as history
  - A "fallback rule-based director" runs when the API is unavailable
  - Timing uses a Web Worker clock
  - Source: [README](https://github.com/nanassound/conductr)
- **Video:** 179 s, "I Built an AI Band That Plays With You in Real Time" — [YouTube](https://www.youtube.com/watch?v=X6CqJoyj0kI)

#### Opus 4.7 — 1st: MedKit (Bedirhan Keskin, physician turned engineer)
- **Repo and license:** [bedriyan/medkit-app](https://github.com/bedriyan/medkit-app). **No OSS license:** "Private — hackathon submission. Not licensed for redistribution" — [README](https://github.com/bedriyan/medkit-app)
- **Depth (counted):** **1 commit** (squashed, Apr 26 2026), so the in-event timeline can't be verified from git. 110 files; 18 TS test cases + 22 Python test functions; ~31.6K LOC, of which one file is a 393 KB patient-data module. The README says "Built in three days".
- **Architecture** — [README](https://github.com/bedriyan/medkit-app):
  - React 18 + Vite + Three.js (`@react-three/fiber`)
  - LiveKit WebRTC
  - A Python `livekit-agents` voice worker (Deepgram Nova-3 STT → Claude Haiku 4.5 → Cartesia Sonic-2 TTS)
  - A FastAPI backend acting as a Managed Agents proxy and LiveKit JWT mint
  - An attending grader on **Opus 4.7 as a Managed Agent** (`medkit-attending`)
  - Model routing: Haiku for the patient persona ("fast, cheap"), Opus for grading ("precision matters")
- **How the model was used:**
  - **Custom tools rendered as UI cards:** `render_vitals_chart`, `render_bed_map`, `render_triage_badge`, `render_patient_timeline`, `render_case_evaluation`, a write tool `flag_critical_finding` behind an approve/decline dialog, and `lookup_ehr_history` through a credential vault — [customTools.ts](https://github.com/bedriyan/medkit-app/blob/main/src/agents/customTools.ts); [docs/evolution.md](https://github.com/bedriyan/medkit-app/blob/main/docs/evolution.md)
  - **Card contracts are Zod-defined** "so the attending agent can't silently emit a malformed card at demo time" — [docs/evolution.md](https://github.com/bedriyan/medkit-app/blob/main/docs/evolution.md)
  - **Citations come from a curated registry**, not generated, "so it can't invent guidance" — [CV gallery #28](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/28)
  - **A second, separate Opus path:** `POST /agent/triage/classify` for one-shot ESI triage ("two distinct Opus code paths") — [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md)
- **Verification:**
  - `npm run verify` checks "deterministic invariants over src/data/*" (data-integrity, rubric-smoke, triage-priority, three-scene)
  - `npm run test` covers custom tools and loop commands
  - A `/loop 20m /medkit-verify-simulation` long-running verifier
  - Sources: [README](https://github.com/bedriyan/medkit-app); [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md)
- **Prize-targeting artifacts:**
  - `docs/evolution.md`, an "Idea evolution log … Kept for the 'Keep Thinking' submission prize — judges want to see that the idea moved"
  - A spec table titled "What wins prizes here", mapping each rubric criterion to a feature
  - Sources: [evolution.md](https://github.com/bedriyan/medkit-app/blob/main/docs/evolution.md); [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md)
- **Video (planned):** a **90-second beat sheet** — [medkit-demo-video skill](https://github.com/bedriyan/medkit-app/blob/main/.claude/skills/medkit-demo-video.md); [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md):
  1. Patient walks in (8 s)
  2. Voice conversation with waveform and transcript (20 s)
  3. Order tests and see results (15 s)
  4. The Managed Agent renders a triage-badge card in real time (15 s; "the most valuable shot")
  5. Agent grades the diagnosis (12 s)
  6. A `/loop` verification log rolls by (5 s)
  7. Title card (5 s)

  The video was planned in Remotion with design tokens extracted from the running app. The gallery's video ID 6bN6hnx-A2A returned no player data when I fetched it, so its actual length and order are unverified.

#### Opus 4.7 — 2nd: Wrench Board (Alexis Chapellier, microsoldering technician)
- **Repo and license:** [Junkz3/wrench-board](https://github.com/Junkz3/wrench-board). **Proprietary source-available license** ("All rights reserved"; view, clone, run for personal or evaluation use, and use as an internal repair tool), **not OSS** — [LICENSE](https://github.com/Junkz3/wrench-board/blob/main/LICENSE)
- **How much is hackathon code:** the repo was created Apr 21, but the public history starts with "Initial public commit" on Jun 7 2026 (16 commits) — [commits](https://github.com/Junkz3/wrench-board/commits/main). The current README already says "powered by Claude Opus 4.8". **The current code is post-event.** Current main (counted): 820 files, 2,245 Python test functions (the README claims "2 600+ fast tests"), ~148K LOC, 44 custom tools. At submission time the video description says "29 agent tools" and "Built solo in 5 days … (April 21–26, 2026)" — [YouTube](https://www.youtube.com/watch?v=OZ2D_p82z6w)
- **Architecture (current)** — [README](https://github.com/Junkz3/wrench-board):
  - FastAPI + native WebSocket + Pydantic v2; vanilla JS + D3 + Three.js boardview; 16 boardview parsers
  - **Knowledge Factory:** 4 personas (Scout, Registry, Writers, Auditor); the 3 Writers run in parallel and "share a cache-warmed prefix"
  - **Schematic ingestion:** vision page by page → a queryable `ElectricalGraph`
  - **Diagnostic agent:** a Managed Agent with 4-store layered memory that "pilots the boardview" through `bv_*` tools
  - **Deterministic core:** `simulator.py` and `hypothesize.py` (1- and 2-fault candidates "ranked by F1 against the observation"; "Neither calls an LLM at runtime")
  - **Two interchangeable runtimes** (Managed vs direct Messages API) behind an identical WS protocol
  - **Model tiers:** Opus (heavy), Sonnet (routine), Haiku (classifier, narrator)
- **Anti-hallucination (two layers):** tools return `{found: false, closest_matches: [...]}`, and `sanitize.py` regex-scans outbound text (`\b[A-Z]{1,3}\d{1,4}\b`) and wraps unverified refdes as `⟨?U999⟩` — [README](https://github.com/Junkz3/wrench-board); [sanitize.py](https://github.com/Junkz3/wrench-board/blob/main/api/agent/sanitize.py)
- **Process:** prototyped in Claude Design. Each domain (design, schematic ingestion, boardview, diagnostic agent) got a spec, then a plan. Claude Code multi-agent mode ran "five or six agents in parallel", with Superpowers skills for brainstorm-then-plan — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **Video:** 160 s — [YouTube](https://www.youtube.com/watch?v=OZ2D_p82z6w). Alexis says he knew it worked when the boardview would "light up step by step" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)

#### Opus 4.7 — 3rd: Maieutic (Paula Vásquez-Henríquez, CS lecturer)
- **Repo:** the gallery lists [github.com/pauvasquezh/maieutic](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/58); it now returns 404 (checked via GitHub API). There is no license or code to read.
- **Architecture** — [maieutic.dev](https://maieutic.dev/); [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon):
  - A Monaco editor with autocomplete off
  - A spec gate: the editor stays locked until Opus's clarifying questions produce an implementable spec
  - Chat answers reference questions but counters reasoning questions with questions
  - "Intent-Diff Review" classifies each spec↔code divergence as drift, revision or bug
  - An instructor dashboard with one-sentence summaries per student and cohort analysis
  - A per-student model with predicted answers
- **Process:** "Two days were spent on the design spec and technical spec before any code was written" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **Demo:** a scripted version of the spec gate built from real session transcripts at demo.maieutic.dev — [maieutic.dev](https://maieutic.dev/). Video 171 s — [YouTube](https://www.youtube.com/watch?v=IJ9FyX2xwWA)

#### Opus 4.7 — Most Creative: Virtual Puppet Theater (Rene Hangstrup Møller)
- **Repo and license:** [rhmoller/virtual-puppet-theater](https://github.com/rhmoller/virtual-puppet-theater), **MIT**. A `hackathon-release` branch "preserves the exact code submitted" — [README](https://github.com/rhmoller/virtual-puppet-theater)
- **Depth (counted, hackathon-release):** 79 commits; ~8.7K LOC TypeScript; 42 test cases (e.g. `server/limits.test.ts`, `session.test.ts`, `brain.test.ts`)
- **Architecture:** Bun + Vite + TS (strict); MediaPipe hands (WASM); three.js at 60 fps; Web Speech API for STT; ElevenLabs TTS with browser-synthesis fallback; a WebSocket "brain" server calling Opus 4.7 — [README](https://github.com/rhmoller/virtual-puppet-theater); [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **How the model was used:**
  - "two Claudes work in parallel": a conversation Claude performs the character, and a separate Opus 4.7 "designs each novel prop on the fly from a tight set of THREE.js primitives"
  - "Asked again, it pops in instantly from cache" — [submission-summary.md](https://github.com/rhmoller/virtual-puppet-theater/blob/main/docs/specs/submission-summary.md)
  - The cache is an in-process `Map` keyed by a normalized description hash, plus a prompt-cached long prefix — [server/asset-generator.ts](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/asset-generator.ts)
  - Abuse limits: `SESSION_RATE_LIMIT_PER_MIN = 8` — [server/limits.ts](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/limits.ts)
  - Spatial reasoning was refined through a "screenshot-based feedback loop" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **Video:** 167 s ([YouTube](https://www.youtube.com/watch?v=qLuGU4PQNss)), made "with Claude and Hyperframes". He advises reserving "that entire last day just for producing the demo" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)

#### Opus 4.7 — Keep Thinking: MaestrIA (Benjamin Torralbo, 20, no prior programming)
- **Repo:** the gallery lists `github.com/Benjxyg/MaestrIA` ([CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194)); it now returns 404. There is no code to read.
- **Architecture** — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon); [CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194):
  - Photo + voice (Chilean Spanish) + location in
  - Opus "streams its reasoning over the photos with animated bounding boxes"
  - A structured diagnosis out (problem, material, severity 1–5, budget, time)
  - A "simulated committee of trades that debate on screen"
  - A managed agent checks material prices against Chilean retail
  - A second agent drafts a WhatsApp message
  - A map of nearby maestros
  - A JSON knowledge file injected into every diagnosis: 17 rules, 7 native woods, 16 dialect terms, 19 benchmark prices, 9 common mistakes
  - Security: input sanitization against prompt injection, rate limiting, origin validation, "Zod schemas as the single source of truth"
- **Video:** 182 s — [YouTube](https://www.youtube.com/watch?v=rkH4AjoTL5Q)

#### Opus 4.7 — Best Use of Managed Agents: ARIA (Idriss Benguezzou and Adam Hnaien)
- **Repo and license:** [zestones/Aria](https://github.com/zestones/Aria). **No LICENSE file** (the GitHub license API returns 404), so by default all rights are reserved (inference).
- **Depth (counted):** **373 commits by Apr 27** (377 total; 61 on Apr 24 alone). At snapshot 08d03cd: 112 TS test cases + 230 Python test functions, ~47K LOC. CI badge — [commits](https://github.com/zestones/Aria/commits/main); [README](https://github.com/zestones/Aria)
- **Architecture** — [README](https://github.com/zestones/Aria):
  - Docker Compose: TimescaleDB + migrations + **4 simulator containers** (1 Hz) + FastAPI backend + React/Vite/TanStack front end
  - 5 agents: KB Builder (PDF vision + 4 calibration questions), Sentinel, Investigator (Opus 4.7 extended thinking; writes and runs Python in a sandboxed container), Work Order Generator, Q&A (hands off to the Investigator)
  - A **FastMCP server with 16 read + 1 write tools as "the agents' only path to data"**
  - The Investigator on Managed Agents with hosted MCP; everything else on the Messages API
- **Trace UI:**
  - The "Agent Inspector" is a bottom drawer exposing the "thinking stream, tool calls, raw event IO, and a Memory stub derived from read-style tool calls" — [AgentInspector.tsx](https://github.com/zestones/Aria/blob/main/frontend/src/features/agents/AgentInspector.tsx)
  - The Activity Feed renders delegations "as a visible sub-turn" via `agent_handoff` + child `agent_start`/`agent_end` frames — [handoff.py](https://github.com/zestones/Aria/blob/main/backend/agents/investigator/handoff.py)
  - The WS event vocabulary I found in the code: `agent_start`, `agent_end`, `agent_handoff`, `tool_call_started`, `tool_call_completed`, `thinking_delta`
- **Demo mode:** "`SIMULATOR_MODE=demo`. Compresses a seventy-two-hour failure scenario into roughly four minutes wall-clock", and "Demo endpoints inject scenario spikes on cue" (`/api/v1/demo/trigger-memory-scene`) — [README](https://github.com/zestones/Aria); [backend/main.py](https://github.com/zestones/Aria/blob/main/backend/main.py)
- **Video (planned in PRD):**
  - 0:00 problem plus a "chiffre choc" (shock number)
  - 0:30 upload a real manufacturer PDF
  - 1:00 live threshold extraction ("on voit Opus 4.7 travailler")
  - 1:45 operator dialogue
  - 2:15 simulated anomaly → diagnosis + automatic work order
  - 2:45 impact line ("6 mois et 100k€ … 10 minutes")

  Sources: [ARIA PRD §7](https://github.com/zestones/Aria/blob/main/docs/ARIA_PRD.md). The actual video is 180 s — [YouTube](https://www.youtube.com/watch?v=Hen24w2Jyz4)
- **Process:** "Day two was spent planning on a GitHub Project board, scoping milestones, issues, and acceptance criteria". Claude Code wrote "about 80% of the raw lines" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)

### Inferences
- **Deterministic core.** The common architecture is "LLM does perception and judgment, deterministic code does computation and verification." TARA (CBA engine), Conductr (C engine), Wrench Board (simulator/hypothesizer), ARIA (simulators, thresholds, MCP) and MedKit (curated guideline registry, deterministic verify) all keep the numbers outside the model. For us, SAM 3.1 masks and tracks, or a geometric/audio controller, should play that role, with Spark judging on top.
- **Visible agent work.** Every 4.7 winner made the agent's work visible on screen in real time: the boardview lighting up, streamed bounding boxes, render-tool cards, the Agent Inspector, a trades committee debate. The judges' "Demo" criterion seems to reward watching the agent think, not just seeing the output.
- **Model-tier routing.** Wrench, MedKit, ARIA, Elisa and PostVisit each used 2–3 model tiers, which looks like a depth signal. The Meta analog is Glimmer or Spark at low effort for the fast loop, and Spark at medium/high effort or Wonder for the deep pass.
- **Event-week builds.** The 4.6 repos (and ARIA/VPT for 4.7) show first commits on kickoff day and dense commit histories. That makes "built during the event" checkable by judges. A squashed single commit (MedKit) did not prevent 1st place, though.

### Gaps
- I could not watch any demo video or retrieve captions, so the actual shot order is unverified. I used declared beat sheets and descriptions instead. MedKit's video (6bN6hnx-A2A) returned no metadata.
- MaestrIA, Maieutic and the original PostVisit repos are gone from GitHub. PostVisit is readable only through an unofficial MIT mirror.
- Wrench Board's hackathon-era code is not public; the history was rewritten Jun 7 2026. Its in-event depth (beyond "29 agent tools", 5 days, solo) can't be measured.
- I found no official Opus 4.7 rules page; the 30/25/25/20 weights come from one builder's PRD.

## Q2. What evaluation or measured number did each winner show, and how was it computed?

### Takeaway
Only two winners shipped a formal accuracy eval. **MaestrIA** ran a blind expert-agreement test (12 real cases × 9 dimensions, with an ablation from 74% to 81%). **Wrench Board** built a frozen, provenance-checked oracle benchmark (23 + 15 scenarios). The rest proved depth with **engineering numbers**: test counts (Elisa 1,521; PostVisit 262/797 assertions; ARIA 342), pipeline validators (TARA 12/12), per-run time and cost (CrossBeam), cost reductions (PostVisit −78% tokens), throughput claims ("weeks → 5 hours"; "a dozen cases an hour") or a live ablation (PostVisit's tier toggle).

### Cited Findings
- **MaestrIA (the template eval):**
  - Benjamin's father, a master carpenter, diagnosed 12 real photos by audio, without seeing the AI output.
  - The AI was scored on 9 dimensions, "including pathology, material, workdays, CLP cost, severity, and honesty under uncertainty"; agreement was 81%.
  - Before the father's interview went into the knowledge base it was 74%. "The model and prompt were unchanged", so he attributes the 7 points to the expert input — [CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194)
  - Ground truth was recorded by his father — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
  - The video description: "He diagnosed 12 real photos by audio, blind to the AI … The +7 points are his" — [YouTube](https://www.youtube.com/watch?v=rkH4AjoTL5Q)
  - His own verdict: building the "auditable 9-dimension eval against 12 real cases" was the most important thing he did; the eval, "not my intuition, told me what was working" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
  - The official site says only "81% agreement with a Maestro Mayor on 12 real photos (automated eval)" — [maestriachile.cl](https://maestriachile.cl/). That suggests the comparison was scored automatically, probably by an LLM judge per dimension (inference; the scoring code is not public).
- **Wrench Board benchmark:**
  - `benchmark/scenarios.jsonl` (23 lines) and `agent_scenarios.jsonl` (15 lines) are a "Frozen oracle".
  - The **provenance contract**: every scenario must carry a `source_url`, a verbatim `source_quote` of 50+ characters and a local `source_archive`, or "Scenarios missing any of these three are rejected at load time". The rule is "Never refresh just to 'match what the simulator now does'".
  - Sources: [benchmark/README.md](https://github.com/Junkz3/wrench-board/blob/main/benchmark/README.md); [scenarios.jsonl](https://github.com/Junkz3/wrench-board/blob/main/benchmark/scenarios.jsonl)
  - Each scenario gives a cause (refdes and mode) plus `expected_dead_rails` and `expected_dead_components`, scored by `evaluator.compute_score`. Entries are stamped `generated_by: "alex+sonnet-bootstrap"`, `generated_at: 2026-04-24`, `validated_by_human: true` — an LLM drafted them during the event week and a human validated them — [scenarios.jsonl](https://github.com/Junkz3/wrench-board/blob/main/benchmark/scenarios.jsonl); [scoring.py](https://github.com/Junkz3/wrench-board/blob/main/api/pipeline/bench_generator/scoring.py)
  - Today's README adds `make eval-all` across 4 eval surfaces (simulator, pipeline, vision, agent) with "cross-skill regression detection", plus 10 deterministic invariants, plus overnight "evolve" loops that keep or revert patches against the oracle — [README](https://github.com/Junkz3/wrench-board). The current README doesn't say whether these existed at submission.
- **CrossBeam:**
  - **Accuracy:** vision extraction was "~85%" in 10–15 min vs "95%+" in 35 min per 26-page binder. The log doesn't say how accuracy was measured; manual comparison is likely (inference).
  - **Per-run time and cost:** city review 16 min / $8.69, contractor E2E 17 min / $5.92.
  - **Source:** [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
  - **Impact stats** used in the pitch: >90% first-submission rejection, ~6-month delays, $30K delay cost, Buena Park ~120 permits in 2024 vs 8,900 needed by 2029 — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)
- **Elisa:** 1,521 test cases and 39,586 LOC at the deadline (counted; official figures "1,500+", "39,000+") — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon); [repo](https://github.com/zoidbergclawd/elisa)
- **PostVisit:**
  - 262 tests / 797 assertions, with AI mocked
  - "78% reduction in input token costs" from prompt caching
  - Context sizes of "60K-180K tokens"
  - A live 3-tier comparison in the demo
  - Source: [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
- **TARA:**
  - A 12-check GeoJSON validator (continuity, section count, intervention checks …) — [test_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py)
  - The claim "This process used to take weeks. TARA does it in five hours"; traditional studies cost "$1–4 million and take nine to 14 months" — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)
- **MedKit:**
  - Throughput claim: "about a dozen cases an hour", each with a cited debrief — [CV gallery #28](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/28)
  - Deterministic data-integrity and rubric-smoke suites, which "run in under two seconds without network access" — [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md)
  - Traction: three medical faculties and a pharma company planning pilots — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **ARIA:** 342 tests (counted). Onboarding takes "<15 minutes" vs a "6 months / €50k–€500k" status quo — [README](https://github.com/zestones/Aria); [ARIA PRD](https://github.com/zestones/Aria/blob/main/docs/ARIA_PRD.md)
- **Conductr:** the latency claim ("15 ms per step"; "musically invisible") stands in for a metric; it has no tests — [README](https://github.com/nanassound/conductr)
- **Virtual Puppet Theater:** "my son's giggle at the responses was really the only user validation I needed" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)

### Inferences
- **Ablation, not a bare accuracy figure.** The strongest eval story was "the same model, plus domain knowledge X, improves the score by N points against a human expert." For Meta's 25% tooling criterion, the analogous demo is "Spark alone vs SAM 3.1 + Spark", or "with vs without Muse-Image-forged examples", measured on 12–30 held-out items with a human-labeled truth set.
- **Provenance.** Wrench Board's contract (an external source and a verbatim quote for every oracle item) is a cheap defense against the "you generated your own test set" critique. That matters for Defect Forge, where Muse Image creates the data (inference).
- **Tests are not required, but they help.** Conductr won a special prize with no tests, and MedKit won 1st with ~40. Elisa got 2nd as the "depth" story, with its test count named in the official write-up.

### Gaps
- MaestrIA's scoring code, per-dimension rubric text and judging method (human vs LLM judge) are not public.
- CrossBeam's 85%/95% accuracy figures have no stated method.
- None of the 4.6 winners reported a held-out accuracy number.

## Q3. Which repos have permissive licenses, and which components could we adapt for a Meta-model pipeline (OpenAI-compatible API)?

### Takeaway
Five winners are reusable as code: **CrossBeam (MIT), Elisa (MIT), TARA (MIT), Virtual Puppet Theater (MIT) and Conductr (Apache-2.0)**, plus PostVisit through an MIT mirror. **MedKit (not licensed), Wrench Board (proprietary source-available) and ARIA (no license)** can only be studied as patterns. The most portable pieces are the demo-mode/showcase system, the trace panels, the cache-plus-mock pattern, the validators and the planner validation. Agent runtimes built on the Claude Agent SDK or Managed Agents do not port to an OpenAI-compatible endpoint and would need re-wiring (inference).

### Cited Findings

#### License table

| Winner | License | Reusable as code? |
|---|---|---|
| CrossBeam | MIT ([LICENSE](https://github.com/mikeOnBreeze/cc-crossbeam)) | Yes |
| Elisa | MIT ([README](https://github.com/zoidbergclawd/elisa)) | Yes |
| TARA | MIT ([README](https://github.com/Kye256/tara-transport-assessment)) | Yes |
| Virtual Puppet Theater | MIT ([README](https://github.com/rhmoller/virtual-puppet-theater)) | Yes |
| Conductr | Apache-2.0 (GitHub license API) | Yes |
| PostVisit | MIT via third-party HF mirror ([dataset](https://huggingface.co/datasets/introvoyz041/postvisit)) | Only via the mirror |
| MedKit | "Not licensed for redistribution" ([README](https://github.com/bedriyan/medkit-app)) | Pattern only |
| Wrench Board | Proprietary source-available ([LICENSE](https://github.com/Junkz3/wrench-board/blob/main/LICENSE)) | Pattern only |
| ARIA | No license file | Pattern only |
| Maieutic, MaestrIA | Repos removed | No |

#### Components worth lifting (MIT/Apache), with the Meta-port note
- **Demo-mode / showcase system** (CrossBeam, MIT). `app-mode.ts` defines three modes (`dev-test`, `judge-demo`, `real`) and pinned `SHOWCASE_*_OUTPUT_ID`s. `seed-demo-outputs.mjs` seeds from real runs. The "Showcase + Run Live" dual button resets the project before a live run. It is pure front-end/Supabase code and model-agnostic — [app-mode.ts](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/frontend/lib/app-mode.ts); [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **Layered pipeline test ladder plus phase detection** (CrossBeam, MIT). L0 smoke → L1 skill invoke → L2 subagent → L3 mini pipeline → L4 full pipeline, plus `verify.ts` (expected files present → phases completed). The structure ports directly; the bodies call the Agent SDK — [tests](https://github.com/mikeOnBreeze/cc-crossbeam/tree/main/agents-crossbeam/src/tests); [verify.ts](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/agents-crossbeam/src/utils/verify.ts)
- **Trace / call-log panels** (Elisa, MIT, React 19 + TS with tests): `TaskDAG`, `CommsFeed`, `MetricsPanel` (cost and tokens per task, from `total_cost_usd`/`usage`), `NarratorFeed`, `TestResults`, `GitTimeline` — [MissionControl](https://github.com/zoidbergclawd/elisa/tree/main/frontend/src/components/MissionControl); [agentRunner.ts](https://github.com/zoidbergclawd/elisa/blob/main/backend/src/services/agentRunner.ts)
- **Task-DAG planner validation** (Elisa, MIT). Parse JSON → one retry → validate `tasks`/ids/`dependencies`. This ports to Spark with `text.format` JSON-schema structured output, which removes the fence-stripping (inference) — [metaPlanner.ts](https://github.com/zoidbergclawd/elisa/blob/main/backend/src/services/metaPlanner.ts)
- **Per-frame vision assessor** (TARA, MIT, Python). JSON-schema prompt, 2 attempts, safe default, deterministic mock, frame selection by GPS distance, md5 input-keyed cache with base64 stripped, and shipped cache JSON so the app runs with no API key. Port it by swapping `anthropic.messages.create` for an OpenAI-SDK call to `https://api.meta.ai/v1` with an image data URI and a JSON schema (inference) — [vision_assess.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/vision_assess.py); [video_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/video_pipeline.py)
- **Output validator script** (TARA, MIT): N named checks on the final GeoJSON with pass/fail printout ("12/12") — [test_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py)
- **Generation cache plus rate limits** (VPT, MIT). An in-process `Map` keyed by a normalized description hash, a stable long prompt prefix, and `limits.ts` (pure-logic per-session rate limits) with tests — [asset-generator.ts](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/asset-generator.ts); [limits.ts](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/limits.ts)
- **Non-blocking multi-timescale control loop plus rule-based fallback** (Conductr, Apache-2.0). Fast deterministic engine (15 ms), feature analyzer (~4 s), LLM director (~8 s) returning a JSON params/transition object, with a fallback director when the API fails — [README](https://github.com/nanassound/conductr)
- **Demo scenario engine** (PostVisit, MIT mirror, PHP/Laravel): `/demo/start`, reset, simulate alerts, 12 scenarios, a live tier-comparison toggle — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)

#### Patterns to re-implement (license-restricted code)
- **Agent event protocol plus inspector drawer** (ARIA): `agent_start`/`agent_end`/`agent_handoff`/`tool_call_started`/`tool_call_completed`/`thinking_delta` over WebSocket, rendered as an Activity Feed plus an Inspector with thinking, tool, raw-IO and memory tabs — [AgentInspector.tsx](https://github.com/zestones/Aria/blob/main/frontend/src/features/agents/AgentInspector.tsx); [handoff.py](https://github.com/zestones/Aria/blob/main/backend/agents/investigator/handoff.py)
- **Demo time-compression plus trigger endpoints** (ARIA): a 72-hour failure compressed to ~4 min, and on-cue scenario injection — [README](https://github.com/zestones/Aria)
- **Frozen oracle with a provenance contract** (Wrench Board) — [benchmark/README.md](https://github.com/Junkz3/wrench-board/blob/main/benchmark/README.md)
- **Tool-grounded anti-hallucination** (Wrench Board): `{found:false, closest_matches}` plus an outbound regex sanitizer — [sanitize.py](https://github.com/Junkz3/wrench-board/blob/main/api/agent/sanitize.py)
- **Model renders UI through tools** (MedKit): `render_*` tools with Zod contracts, plus an approve/decline permission gate on write tools — [customTools.ts](https://github.com/bedriyan/medkit-app/blob/main/src/agents/customTools.ts); [evolution.md](https://github.com/bedriyan/medkit-app/blob/main/docs/evolution.md)

### Inferences
- **Map to our three ideas.** ✓✓ = strong fit; ✓ = helpful; — = little use.

  | Reusable component (license) | Defect Forge | DemoScribe | Find-and-Guide |
  |---|---|---|---|
  | CrossBeam demo-mode + Showcase/Run-Live (MIT) | ✓✓ pinned best run plus live run | ✓✓ | ✓ live mic/camera demo needs a fallback |
  | CrossBeam L0–L4 test ladder + phase verify (MIT) | ✓✓ forge → SAM → Spark stages | ✓✓ track → segment → label stages | ✓ |
  | Elisa MissionControl / MetricsPanel trace UI (MIT) | ✓✓ call log with model ID, latency, cost | ✓✓ | ✓ |
  | Elisa DAG planner validation (MIT) | ✓ | ✓✓ subtask graph from a robot video | — |
  | TARA per-frame JSON assessor + md5 cache + mock (MIT) | ✓✓ per-image Spark inspection | ✓✓ per-keyframe Spark labels; cache SAM tracks per video | ✓ |
  | TARA N-check output validator (MIT) | ✓ label/mask consistency checks | ✓✓ track continuity, label coverage, temporal order | ✓ |
  | VPT description-hash generation cache + rate limits (MIT) | ✓✓ cache Muse Image forgeries (150 RPM limit) | — | ✓ |
  | Conductr multi-timescale loop + fallback (Apache-2.0) | — | — | ✓✓ SAM/audio loop at frame rate; Spark re-plans every few seconds; rule-based fallback |
  | PostVisit tier toggle (MIT mirror) | ✓✓ live "Spark only vs SAM + Spark" ablation | ✓✓ reasoning-effort low vs high | ✓ |
  | Wrench Board frozen oracle + provenance (pattern) | ✓✓ answers "you graded your own synthetic data" | ✓ human-annotated subtask boundaries | ✓ |
  | Wrench Board sanitizer (pattern) | ✓✓ never report a defect without a SAM mask behind it | ✓ only label frames with a track | — |
  | ARIA event protocol + inspector (pattern) | ✓ | ✓✓ multi-stage visible pipeline | ✓ |
  | ARIA demo time-compression (pattern) | — | ✓ replay long robot videos fast | ✓ scripted scenario triggers |
  | MaestrIA blind-expert ablation eval (pattern) | ✓✓ | ✓✓ | ✓ success rate / time-to-grasp with vs without guidance |

- **Porting cost.** Agent-SDK-dependent code (CrossBeam's `query()` flows, Elisa's agentRunner, MedKit/Wrench/ARIA Managed Agents) won't run against Meta's API. For a 31-hour build, the portable value is in the UI, demo modes, caches, validators and schemas, not in the agent runtimes.

### Gaps
- I didn't check per-file license headers or third-party asset licenses inside the MIT repos (e.g. CrossBeam bundles Anthropic's document-skills scripts under `.claude/skills/`, which may carry their own terms).
- The PostVisit mirror is not the author's official distribution.

## Q4. What do the winners' own write-ups, posts or interviews say about why they won and how they used parallel coding agents?

### Takeaway
The winners and commentators attribute the wins to **domain expertise plus a real problem with real artifacts**. Most winners describe a **spec/plan-first, parallel-session workflow**: one Claude Code session or worktree per subsystem, 3–6 at once, with CLAUDE.md or spec files keeping them coherent. Several deliberately engineered their submission to the rubric: a "What wins prizes here" table, a judge-facing landing page, an idea-evolution log, stakeholder interviews.

### Cited Findings
- **Why they won (official framing):**
  - Jason Bigman (Anthropic) framed the winners as "the people closest to a problem" finally building the solution themselves — [EdTech Innovation Hub](https://www.edtechinnovationhub.com/news/a-doctor-a-carpenter-and-a-teacher-win-anthropics-global-opus-47-hackathon)
  - "Four out of five winners were not professional developers" (4.6) — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)
- **Why they won (commentator view):** Dexter Hadley: "expertise trumps coding"; CrossBeam "works because Mr. Brown understands building permit laws". The same piece criticizes the demos as "merely a theoretical proof", lacking evidence they'd hold up six months later, with auditability not a priority — [GIGAZINE](https://gigazine.net/gsc_news/en/20260425-anthropic-hackathon/)
- **MedKit:**
  - He ran four separate Claude Code sessions (voice engine, content generation, 3D game layer, core app) "to keep each context clean", working "almost entirely by voice" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
  - His log shows he re-pitched from game to "training simulator" because "Judges grading Impact will weigh a training tool higher than a game"
  - He added the Managed Agent attending specifically because "The $5k Managed Agents special prize is specifically for using the new API primitives"
  - Source for both: [docs/evolution.md](https://github.com/bedriyan/medkit-app/blob/main/docs/evolution.md)
- **Wrench Board:** a Claude Design prototype → one spec and plan per domain → "five or six agents in parallel during debugging, with one dedicated agent per domain" → Superpowers skills for brainstorm-then-plan → "Bet on Opus 4.7's visual schematic understanding" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **PostVisit:** "Up to 4-5 agents working simultaneously on separate modules (backend + frontend + docs)", each "in its own git worktree" on a Hetzner VPS. The VPS kept agents working through an 11-hour flight with unstable Wi-Fi — [BUILD-LOG (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
- **Elisa:** Jon's later talk covers keeping Claude Code coherent "at ~10k lines/day" through "CLAUDE.md at every directory level" ("a system prompt for the codebase") and "a staleness table so docs never rot". He "rewrote the entire backend in one evening", which matches the Feb 11 "Rewrite backend from Python/FastAPI to TypeScript/Express" commit — [Code with Claude session](https://claude.com/code-with-claude/session/sf-ext-coherence-at-claude-code-speed); [commits](https://github.com/zoidbergclawd/elisa/commits/main)
- **CrossBeam:**
  - "I didn't even read a line of code"; Claude wrote the tests — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)
  - He kept voice logs.
  - He wrapped the built-in Claude Code guide agent in a skill ("Would have saved a ton of time").
  - He asked organizers "deploy or polish?" and learned "They want deployment."
  - On the speakers' advice ("develop for future models"), he left the slow 95%-accurate extraction skill in place.
  - He rewrote the landing page because "Judges don't care about that. They want to see the architecture."
  - At the end he ran "Claude Code and Cursor both going".
  - Source for the last five items: [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
- **ARIA:** "One day of planning let us spend the rest of the week executing, not improvising"; "you can't prompt your way to knowing what a maintenance technician actually looks at" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **Maieutic:** two days of design and technical spec before any code — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
- **TARA:** roughly 20 feature-by-feature build prompts checked into `docs/` (video, equity, UX, PDF fixes, audits) — [docs/](https://github.com/Kye256/tara-transport-assessment/tree/main/docs). That suggests each sub-feature was handed to Claude Code as a written spec (inference).
- **Virtual Puppet Theater:** "Claude handled concept discussion, planning, and code writing. Rene handled direction, architecture, review, and decisions" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)

### Inferences
- **Parallel sessions split by subsystem.** The repeatable recipe is 3–6 parallel Claude Code sessions or worktrees, each owning one subsystem with its own spec/CLAUDE.md, plus one human acting as architect and integrator. For us: (1) the SAM 3.1 track/mask service, (2) the Spark agent and eval harness, (3) the front end with the trace panel and demo mode, and (4) Muse Image generation or the audio-cue engine, depending on the idea.
- **Design to the rubric.** Rubric-mapping documents (MedKit's prize table, ARIA's criteria table) and judge-facing artifacts (CrossBeam's technical landing page, MedKit's evolution log) are cheap and were used by at least three winners. It looks like deliberate design-to-rubric pays off.

### Gaps
- I found no first-person interview with the judges (Boris Cherny, Cat Wu) explaining their picks. GIGAZINE confirms none was quoted.
- I found no posts by Benjamin Torralbo or Paula Vásquez-Henríquez beyond the official pages.

## Q5 (synthesis). What "depth bar" did the winners clear?

### Takeaway
The bar is roughly: a **3–6-stage pipeline on real domain inputs**, with **≥2 distinct model roles or tiers**, a **deterministic engine or validator the model can't fool**, **live visible agent activity**, a **demo mode that never fails**, and **one checkable proof** (a test suite in the hundreds or thousands, a validator at N/N, or a blind expert-agreement number with an ablation). Raw volume ranges widely: 12 commits / 4.8K LOC (Conductr, special prize) up to 349–373 commits (PostVisit, ARIA).

### Cited Findings
- **Commits by deadline (counted unless noted):**
  - Conductr 12
  - TARA 49
  - CrossBeam 63
  - VPT 79
  - Elisa 85
  - PostVisit 349 (self-reported) — [BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
  - ARIA 373
  - MedKit 1 (squashed)
- **Tests:**
  - Elisa 1,521
  - ARIA 342
  - PostVisit 262 (797 assertions) — [README](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
  - VPT 42
  - MedKit 40
  - CrossBeam 11 layered pipeline scripts
  - TARA one 12-check validator
  - Conductr 0
  - Wrench Board 2,245 today, but not measurable at submission
- **Real inputs:**
  - CrossBeam used real Placentia and Long Beach permit sets, with permission — [README](https://github.com/mikeOnBreeze/cc-crossbeam)
  - TARA used real dashcam footage of Kira–Matugga and Kasangati–Matugga — [Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon); [repo cache dirs](https://github.com/Kye256/tara-transport-assessment/tree/main/data/videos)
  - Wrench Board used the MNT Reform open-hardware board — [scenarios.jsonl](https://github.com/Junkz3/wrench-board/blob/main/benchmark/scenarios.jsonl)
  - PostVisit tested in a real hospital — [BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
  - MaestrIA used 12 real photos — [CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194)
- **Multiple model paths:**
  - MedKit: Haiku persona + Opus Managed Agent grader + Opus triage endpoint — [spec.md](https://github.com/bedriyan/medkit-app/blob/main/spec.md)
  - Wrench Board: Opus/Sonnet/Haiku tiers — [README](https://github.com/Junkz3/wrench-board)
  - VPT: conversation Claude + Opus prop designer — [submission-summary.md](https://github.com/rhmoller/virtual-puppet-theater/blob/main/docs/specs/submission-summary.md)
  - ARIA: Managed Agent Investigator + Messages-API agents — [README](https://github.com/zestones/Aria)
  - Elisa: Opus agents + Haiku narrator — [README](https://github.com/zoidbergclawd/elisa)
- **Grounding and anti-fabrication:**
  - MedKit's curated citation registry — [CV gallery #28](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/28)
  - Wrench Board's refdes sanitizer — [sanitize.py](https://github.com/Junkz3/wrench-board/blob/main/api/agent/sanitize.py)
  - ARIA's MCP as the "only path to data" — [README](https://github.com/zestones/Aria)
  - CrossBeam's 28-file statute skill — [README](https://github.com/mikeOnBreeze/cc-crossbeam)

### Inferences
- **A depth bar for our 31 hours:**
  1. Chain ≥3 Meta models, each with a distinct job (e.g. Muse Image generates, SAM 3.1 grounds, Spark judges/plans; add Glimmer for a fast tier if time allows).
  2. Put a deterministic checker between models (mask-IoU, track continuity, a geometric hand-to-object controller).
  3. Ship a trace panel and a demo mode.
  4. Produce one ablation number on 12–30 human-labeled real items.
  5. Write ~50–150 fast tests with the models mocked. That is achievable with parallel sessions and clears the 4.7 winners' typical range without chasing Elisa's 1,500.
- **Quality over volume.** Volume alone does not win. ARIA's 373 commits won a special prize, not a top-3 place. CrossBeam won 1st with 63 commits, because the domain problem, real artifacts and visible multi-agent work carried it.

### Gaps
- There is no judge-side scoring data, so the relative weight of depth signals is inferred from outcomes only.

## Q6 (synthesis). What video and README structure do the winners share?

### Takeaway
Videos ran **160–182 s** (the cap was 3:00). The declared structure is: **problem with a shock number → upload a real artifact → watch the agent work (with the newest-model capability on screen) → a human-in-the-loop moment → professional output → impact or traction close**. Builders consistently report the video as the **biggest time sink** and reserve the last day for it. READMEs follow **hero/video → problem with numbers → what it does → architecture diagram → "How [model] is used" table → stack table → quickstart that runs on cached/demo data → project tree → tests → license**, often with a build log.

### Cited Findings
- **Video lengths** (from YouTube metadata):
  - CrossBeam 180 s — [YouTube](https://www.youtube.com/watch?v=jHwBkFSvyk0)
  - Elisa 176 s — [YouTube](https://www.youtube.com/watch?v=rsUaz_QAK6o)
  - PostVisit 179 s — [YouTube](https://youtu.be/V29UCOii2jE)
  - TARA 180 s — [YouTube](https://www.youtube.com/watch?v=GFCrXehS1DE)
  - Conductr 179 s — [YouTube](https://www.youtube.com/watch?v=X6CqJoyj0kI)
  - Wrench Board 160 s — [YouTube](https://www.youtube.com/watch?v=OZ2D_p82z6w)
  - Maieutic 171 s — [YouTube](https://www.youtube.com/watch?v=IJ9FyX2xwWA)
  - VPT 167 s — [YouTube](https://www.youtube.com/watch?v=qLuGU4PQNss)
  - MaestrIA 182 s — [YouTube](https://www.youtube.com/watch?v=rkH4AjoTL5Q)
  - ARIA 180 s — [YouTube](https://www.youtube.com/watch?v=Hen24w2Jyz4)
- **Declared beat sheets:**
  - ARIA: 0:00 problem + shock number → 0:30 real PDF upload → 1:00 live extraction "(on voit Opus 4.7 travailler)" → 1:45 operator dialogue → 2:15 anomaly → diagnosis + work order → 2:45 impact line — [ARIA PRD §7](https://github.com/zestones/Aria/blob/main/docs/ARIA_PRD.md)
  - MedKit's 90-s plan names its "most valuable shot": the agent rendering a custom-tool card in real time — [medkit-demo-video skill](https://github.com/bedriyan/medkit-app/blob/main/.claude/skills/medkit-demo-video.md)
  - TARA's flow: "dashcam footage → condition assessment → economic analysis → equity scoring → PDF report" — [README](https://github.com/Kye256/tara-transport-assessment)
- **Production methods:**
  - CrossBeam: stakeholder interviews (mayor, contractor), Remotion-animated architecture and agent-working shots, Premiere, a whole day of work — [progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)
  - MedKit: Remotion composited over design tokens extracted from the app; narration recorded separately "so you can re-record without re-rendering visuals" — [medkit-demo-video skill](https://github.com/bedriyan/medkit-app/blob/main/.claude/skills/medkit-demo-video.md)
  - VPT: "Claude and Hyperframes", plus "reserving that entire last day just for producing the demo" — [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)
  - PostVisit: "the single biggest time sink"; re-recorded as the UI changed — [BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)
- **README patterns:**
  - TARA: badge → tagline → video thumbnail → screenshot grid → "How Claude Opus 4.6 Is Used" → quickstart "optional — cached demo data included" — [README](https://github.com/Kye256/tara-transport-assessment)
  - PostVisit: test badge (262 passed) → build-log link → "Built with Opus 4.6" feature→usage table → healthcare design → license-tracked stack table — [README (mirror)](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/README.md)
  - ARIA: mermaid agent diagram → 3-command quickstart → seeded users → "How it runs" → stack → layout → docs index — [README](https://github.com/zestones/Aria)
  - Wrench Board: video link + "try it online" → what it is → why it exists (personal story) → how it works → "Under the hood" → anti-hallucination section — [README](https://github.com/Junkz3/wrench-board)
  - Build logs: CrossBeam `progress.md`, PostVisit `BUILD-LOG.md`, MedKit `docs/evolution.md`

### Inferences
- **Our video template:** a 0:00–0:20 hook with a real stakeholder or real footage and a number; 0:20–0:40 the real input; 0:40–1:50 the live pipeline with the trace panel visible and the SAM/Muse capability shown in close-up; 1:50–2:20 a human-in-the-loop moment or ablation; 2:20–2:50 the eval number and output artifact; 2:50–3:00 close. Record narration separately. Lock the UI before shooting (PostVisit's lesson).
- **README:** put a "How Meta models are used" table (model ID → role → why it's needed) near the top. Make the quickstart default to cached outputs, with a live path behind an env var (TARA's pattern).

### Gaps
- Shot-by-shot content of the actual videos is unverified.

## Q7 (synthesis). Which of their tricks transfer most directly to Defect Forge, DemoScribe and Find-and-Guide?

### Takeaway
**DemoScribe** maps most directly onto proven winner code. TARA's per-frame JSON vision pipeline with cache, mock and validator is MIT, and CrossBeam's file-based staged artifacts and Elisa's DAG planner and trace UI are MIT too. **Defect Forge** gets the strongest *eval story*: MaestrIA's ablation plus Wrench Board's provenance oracle, with VPT's generation cache for Muse Image. **Find-and-Guide** maps onto Conductr's "engine never waits for the model" loop (Apache-2.0) and VPT's real-time webcam stack (MIT). It has the least reusable eval machinery and the highest live-demo risk.

### Cited Findings
- **TARA's video→frames→per-frame JSON→segments→validator→report flow** is structurally the DemoScribe pipeline (video → SAM tracks → Spark subtask/failure labels → validated timeline) — [video_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/video_pipeline.py); [test_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py)
- **Conductr's three-timescale design**, where the model "shapes the next phrase, not the current note" and a rule-based fallback runs "when the API is unavailable", matches a guidance loop. Audio cues have to update at frame rate from tracking while the planner runs asynchronously — [README](https://github.com/nanassound/conductr)
- **VPT's real-time webcam + MediaPipe + WebSocket brain + TTS fallback stack** is a working reference for a browser camera/voice loop (MIT) — [README](https://github.com/rhmoller/virtual-puppet-theater)
- **Generated-data credibility:**
  - VPT caches generated assets by description hash — [asset-generator.ts](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/asset-generator.ts)
  - Wrench Board requires an external source for every oracle item — [benchmark/README.md](https://github.com/Junkz3/wrench-board/blob/main/benchmark/README.md)
  - MaestrIA measured against a blind human expert — [CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194)

### Inferences
- **Defect Forge:**
  - Reuse TARA's assessor/cache/mock and VPT's generation cache.
  - Implement a Wrench-style provenance rule: the eval set must be real defect photos (public datasets or our own), never Muse-Image forgeries.
  - Report a MaestrIA-style ablation: Spark zero-shot vs Spark plus forged-and-SAM-labeled few-shot examples, scored on the real set.
  - Add a Wrench-style sanitizer so every reported defect must reference a SAM mask ID.
- **DemoScribe:**
  - Reuse TARA's pipeline shape and validator, Elisa's DAG validation for subtask graphs, and CrossBeam's file-per-stage artifacts and phase detection.
  - Use the ARIA event protocol for a visible multi-stage trace, and PostVisit's tier toggle (reasoning effort, or with/without SAM tracks) as the live ablation.
- **Find-and-Guide:**
  - Reuse Conductr's loop architecture and fallback director, VPT's browser real-time stack and limits, and CrossBeam's Showcase/Run-Live split.
  - A live camera demo is the riskiest of the three under "holds up live", so a recorded showcase path is mandatory.
  - The eval would be task success and time-to-touch over ~10–20 trials, with vs without guidance (MaestrIA-style ablation adapted).

### Gaps
- None of the winners used segmentation models or audio-guidance loops, so the Find-and-Guide and SAM-specific parts are extrapolations, not precedents.
