# Handoff: Defect Forge for the Meta Global AI Developer Hackathon

Start here. This file is the plan as decided after two rounds of research. The full reasoning, sources and code patterns are in [`reports/`](reports/), and the raw research notes are in [`research_notes/`](research_notes/).

**Status (Wed Nov 4, 02:10 IST):** research done, idea chosen, **gate tests passed (GREEN), and the headline has changed.** Read [`docs/gate-results.md`](docs/gate-results.md) first.

- Muse Image forges convincing holes and prints (cracks are plausible).
- The deterministic compositor keeps every pixel outside the defect byte-identical.
- SAM 3.1 box-prompt masks reach a median IoU of 0.867.
- **Muse Spark already inspects hazelnuts perfectly zero-shot (20/20)**, so "forged examples improve recall" is dead.
- The new headline is the **detection-threshold curve**: forge a defect, shrink or fade it with OpenCV, and find where the inspector stops seeing it. That curve already falls off cleanly (holes at 12% opacity: 0/5 detected).

No product code yet; the next step is the build (Step 2). Test scripts are in [`spikes/`](spikes/).

## Deadlines

| Event | IST | ET | UTC |
|---|---|---|---|
| Submission deadline (hard) | **Thu Nov 5, 07:30** | Wed Nov 4, 21:00 | Thu Nov 5, 02:00 |
| Target submit time (3 h buffer) | Thu Nov 5, 04:30 | Wed Nov 4, 18:00 | Wed Nov 4, 23:00 |
| Code freeze | Wed Nov 4, 23:30 | Wed Nov 4, 13:00 | Wed Nov 4, 18:00 |
| Office hours (ask the open questions) | Wed Nov 4, 20:30–21:30 | Wed Nov 4, 10:00–11:00 | Wed Nov 4, 15:00–16:00 |
| Judging / live final for the top 5 per track | Nov 5–9 / Nov 9 | Nov 4–8 / Nov 9 | |

The plan in the report assumes a 00:45 IST start. Shift each row by however late you actually start, and cut nice-to-haves first. **Never cut the code freeze, the video block or the submission buffer.**

## The decision

**Build Defect Forge, refined into a spec-driven defect test suite.**

> Before your line has produced a single defect, Defect Forge forges the defects your spec describes, labels them to the pixel, and shows which ones your inspector would miss. The same forgeries, shown in context, teach a Meta inspector.

- **Track:** Indie. **Theme:** Push the Frontier. **Team:** 2 people.
- **Loop:** Muse Spark turns the spec into a defect taxonomy, Muse Image forges each defect onto a photo of a good part, deterministic OpenCV code aligns and composites the edit, SAM 3.1 labels the defect to the pixel, and Muse Spark critiques realism and inspects real parts.
- **Benchmark:** the MVTec AD **hazelnut** category (full test split).
- **Live demo:** real hazelnuts you damage at home, shot with a phone or webcam.

Verdicts on the three candidates (details in [`reports/Meta hackathon build feasibility.md`](reports/Meta%20hackathon%20build%20feasibility.md)):

| Idea | Verdict | Why |
|---|---|---|
| **Defect Forge** | **GO, gated on the tests below** | No visible competitor forges defects with Muse Image. Fits a computer-vision and labeling team, needs only a phone and webcam, and API cost stays under $30 |
| DemoScribe (robot video labeling) | Pivot only | Crowded: winnow (263 commits), GlassBox, DemoDoctor, and MimicAnno from a Gemma 4 Good 1st place. No robot-learning background on the team |
| Find-and-Guide (blind object finding) | NO-GO | Netra (3rd at Gemini 3) and shipped products already do it. No blind tester, no Meta text-to-speech under the runtime rule, unmeasured latency |

## Rules that can disqualify us

1. **Every model called at runtime must be a Meta model.** Organizers tightened this on Nov 1 and Nov 2. No OpenAI, Claude, Gemini, Whisper, ElevenLabs, Llama (Llama does *not* count), embeddings, CLIP, LPIPS, rembg, MediaPipe, YOLO or any local neural net. OpenCV, NumPy and SciPy are classical code and are fine. Coding tools (Claude Code, Codex) are fine.
2. **The README must state which Meta models run and where.**
3. **Model API Terms §10.1(ix)** bars using outputs to train models that compete with Meta. Frame the forged set as **evaluation data and in-context examples for a Meta inspector**, which the Terms explicitly allow. **Do not train any detector on the forgeries.**
4. **MVTec AD is CC BY-NC-SA.** Ship a download script and never commit MVTec images. Build the video and all DEMO_MODE fixtures from **our own hazelnut photos**.
5. **Submission:** a video of 3 minutes or less with live Meta calls visible, a **public** GitHub repo that runs from its README, the Cerebral Valley form listing **every teammate**, and an X post link for Most Viral.
6. **The video shows only work built during the event.** Commit early and often; a dense commit history is evidence of that.
7. **Demo mode is allowed** only if the repo still runs live by default and the README explains demo mode.
8. **Avoid the anti-projects:** no Streamlit, and the dashboard must not be the main feature.

## Step 0: setup

- **API key:** get a Meta Model API key from dev.meta.ai and put it in `.env` as `MODEL_API_KEY=...` (copy `.env.example`). **Never commit `.env`.** Rate limits are per team, not per key, so both builders share one budget.
- **Clone path:** clone to a path without spaces (e.g. `D:\dev\meta-ai-hackathon`), because some tooling breaks on spaces.
- **Toolchain:** Python 3.12 and Node 20. On Windows, call `.venv\Scripts\python` directly to avoid PowerShell execution-policy issues.
- **Phone camera:** it needs HTTPS. Use `cloudflared tunnel --url http://localhost:5173`. The laptop webcam works on `localhost` without HTTPS.

## Step 1: gate tests (DONE, GREEN; see [`docs/gate-results.md`](docs/gate-results.md))

These tests ran on Wed Nov 4, 01:20–02:10 IST, for about $1.27. The plan below is kept for reference; the results and plan changes are in the results doc.

| # | Owner | Test | Pass | If it fails |
|---|---|---|---|---|
| T0 | A | Claim the credits, create a key, call `/v1/models`, read the `x-ratelimit-remaining-*` headers. B starts the MVTec hazelnut download (588 MB) | The key works on `muse-spark-1.3`, `muse-image-1.0` and `sam-3.1` | Report it at dev.meta.ai/support; use the other person's key meanwhile |
| T1 | A | One `/v1/images/edits` call on a 512 px crop of a train/good hazelnut. Try `reasoning_strength` low vs high, with tools on vs off. Log latency, returned size and drift after alignment | Low strength with tools off returns in under ~60 s, and the diff isolates a compact region | If it's slow but works, batch overnight. If the safety filter blocks "crack", rephrase ("a split", "a small hole") |
| T2 | A | 3 defect types (hole, crack, print) × 5 samples × 2 prompt styles: (a) text naming the location at the crop centre; (b) a red outline drawn on the crop, with "paint the defect inside the red outline, then remove the outline". Plus one whole-image control. Composite all of them | Composited results look plausible | Switch to the outline style or to whole-image edits |
| T3 | B | SAM 3.1 box prompts on 10 real test defects, using the ground-truth boxes, scored by IoU against the GT masks. Then the concept prompt "hazelnut" for the part mask | Median IoU ≥ 0.5, and a clean part mask | Pad boxes 20–50%, or crop and upsample. Fall back to diff masks as labels |
| T4 | B | 20 test images (10 good, 10 defective): zero-shot vs 4 real held-out defect examples in context. Validate the JSON schema and the 0–1000 box parsing | Zero-shot balanced accuracy between 55% and 90%, and the real examples add ≥5 points of recall | Make label quality and realism the headline instead |
| T5 | B, then A | B blind-rates 10 forged and 10 real crops in random order. The Spark critic scores the same forgeries | ≥2 defect types with ≥3 of 5 rated realistic, and the critic agrees on ≥4 of 5 | See the gate outcomes |

**Gate outcomes:**

- **Green:** ≥2 defect types pass T5 and the T3 median IoU is ≥ 0.5. Build the full plan.
- **Amber:** only one type passes. Narrow to it, and spend at most 1 hour trying MVTec `bottle` or `metal_nut`.
- **Red:** nothing passes. Pivot within an hour to a narrow DemoScribe: a robot-episode grader benchmarked on the RoboReward test split (200 H.264 clips, about 120 MB, CC-BY-4.0, published MAE 0.691–1.485). About 60% of the infrastructure carries over.

## Step 2: build

Full details are in the feasibility report sections **"Build a three-model loop around a deterministic OpenCV core"** (architecture, exact API call patterns, gotchas, code to reuse) and **"Scope for two people and thirty hours"** (must, nice and cut, plus the hour-by-hour plan for Person A and Person B).

**Ownership:**

- **Person A (forge + UI):** the Meta client layer (retry, cost ledger, replay), the forge core, labeling, the critic, the validators, the batch runner, the React UI, DEMO_MODE, the Live Inspect page and the hero shot.
- **Person B (eval + data + rig + docs):** the Spark inspector, the eval harness, the SAM IoU checks, the blind realism page, the hazelnut rig, the home photo set, the tests, the README and the friction log.

**Cut entirely:**

- the Muse Wonder planner and Glimmer/Spark Open
- training any detector
- TTS and voice
- glasses, Quest and robot hardware
- auth and databases
- a public live backend
- all DemoScribe and Find-and-Guide features

**Target layout** (the repo root is this folder; build into these subfolders):

```
README.md  EVAL.md  THIRD_PARTY.md  .env.example  .gitattributes  .gitignore
docs/        architecture.png  friction-log.md  build-log.md  results/*.json
backend/app/ main.py (FastAPI, SSE /events)  routes/
  meta/      client.py  spark.py  muse_image.py  sam.py  retry.py  ledger.py  replay.py
  forge/     taxonomy.py  locate.py  crop.py  composite.py  label.py  critic.py  validators.py  batch.py
  inspect/   inspector.py  sanitize.py
  export/    coco.py
eval/        download_mvtec.py  split.py  run_eval.py  metrics.py  realism_test/  home_set/
frontend/    Vite + React + TS + Tailwind: Forge, Dataset, Eval, LiveInspect pages
fixtures/    demo runs recorded on our own hazelnut photos only
tests/       pytest with a recorded transport
scripts/     setup.ps1  setup.sh  dev.ps1  dev.sh  tunnel.ps1
```

## Step 3: prove it

> **Updated after the gate tests:** the headline is now the **detection-threshold curve**, and the C0–C3 table below is only a supporting row, because zero-shot Spark was already 20/20.
>
> - For each defect type, sweep forged severity (size ×1.0/0.6/0.35/0.2, opacity 1.0/0.5/0.25/0.12) and report detection per cell with Wilson CIs, plus specificity on good parts.
> - Validate the curve with **real drilled hazelnuts** at 2–3 bit sizes.
>
> See `spikes/t6_severity.py` and [`docs/gate-results.md`](docs/gate-results.md).

**Pre-register the eval** in `EVAL.md` and commit it *before* running it. Use the full MVTec hazelnut test split, with four conditions run twice each:

| Condition | What the inspector sees |
|---|---|
| C0 | Spec text only |
| C1 | Spec + 2 good images (controls for extra images) |
| C2 | Spec + 2 good + 8 forged defects (the treatment) |
| C3 | Spec + 2 good + 8 real defects (the upper bound) |

- **Metrics:** recall, specificity, balanced accuracy, per-type recall and box hit rate, with Wilson 95% confidence intervals and an exact McNemar test of C2 vs C1.
- **Fallback headlines** if C2 doesn't beat C1:
  - SAM 3.1 mask IoU against real ground-truth masks
  - a blind realism test (real vs forged crops, 5–10 raters)
  - cost and time per labeled sample
- **Choose the headline from the data** around 17:30 IST, and report a null result honestly.

## Step 4: video, X post, submission

See the feasibility report sections **"A 2:50 video that shows live calls, then a twelve-item submission check"** and **"Aim bonuses at Creative Build; treat Most Viral as a quiz"**.

- **Video:** open on *generation* (the forged defect grid), not inspection, so it doesn't look like another inspector.
- **Related work:** the README must cite Walkdown (a rival entry that uses Muse Image for false-alarm negatives) and AnomalyAgent.
- **Bonus targets:**
  - **Best Creative Build** (Muse Image)
  - **Most Viral**: post a "which crack is real?" quiz on X, since comments count

## Questions to ask the organizers (Discord #questions and office hours)

1. Can one project win a track prize and a bonus prize?
2. Does evaluation-only use of Muse Image outputs (test suite plus in-context examples, no training) satisfy Model API Terms §10.1(ix)?

## Still unverified (check during the gate tests)

- Muse Image latency, output size and realism on small defects
- SAM 3.1 latency and IoU on small defects
- the exact `meta_sam_parser` import names (check against the cookbook's `sam_preview.py`)
- whether a flat four-integer box schema works in strict mode
- the hazelnut test-split counts (confirm after download)
- the bonus prize amounts, which appear only in participant copies of the Participant Guide

## Decisions the repo owner still has to make

- **Make the repo public** before submitting. It is private for now, and the submission requires a public repo that opens logged-out.
- **License:** the report suggests MIT. If you copy MIT or Apache code, keep its license text in `THIRD_PARTY.md`.
- **Research notes in the public repo:** decide whether `reports/` and `research_notes/` stay in once it goes public. They include competitor analysis.

## Document map

| File | What's in it |
|---|---|
| [`reports/Meta hackathon build feasibility.md`](reports/Meta%20hackathon%20build%20feasibility.md) | **The build plan.** Verdicts, gate tests, architecture, exact API calls, gotchas, code to reuse with licenses, repo layout, the hour-by-hour plan, the eval protocol, the video storyboard, the submission checklist and risks |
| [`reports/Meta AI hackathon winning ideas.md`](reports/Meta%20AI%20hackathon%20winning%20ideas.md) | Round 1: rules, rubric, prizes, Meta model capabilities, past winners, the competitor scan and the original top three ideas |
| `research_notes/Meta hackathon build feasibility/` | Round 2 notes: teardowns of Anthropic, Meta and Google winners; competitors and reusable code; Defect Forge feasibility; DemoScribe and Find-and-Guide feasibility; hardware |
| `research_notes/Meta AI hackathon winning ideas/` | Round 1 notes: event rules and intel, Meta models and API, past Meta winners, winning patterns, opportunity scan |
| [`CLAUDE.md`](CLAUDE.md) | Instructions for coding agents working in this repo |
