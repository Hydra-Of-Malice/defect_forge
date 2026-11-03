# Commit to Defect Forge, Then Prove It

Commit to **Defect Forge**, refined into a spec-driven defect test suite, and confirm or kill it with six API tests that finish by **03:00 IST tonight**. Of the three ideas it is the only one that no visible entry is building, that fits a two-person web, labeling and computer-vision team, that needs nothing beyond a phone and a webcam, and that can still produce at least two non-circular numbers if its riskiest claim fails. **DemoScribe is a no-go as the primary.** winnow (263 commits) serves the same robot-learning users with the same SAM-plus-Spark stack, MimicAnno was part of a Gemma 4 Good first-place entry, DemoDoctor and GlassBox overlap further, and the team has no robot-learning background. It survives only as the pivot if the forging test fails, because its data path is the fastest in the notes. **Find-and-Guide is a no-go.** Netra placed third at Gemini 3 with the same hand-guidance loop, four entries in this hackathon chase it, a blindfolded sighted tester is not a valid stand-in for the blind tester you don't have, and Meta offers no text-to-speech while the runtime rule tightened on Nov 1 and 2. Defect Forge's three real risks are known and bounded. Muse Image has no mask parameter and its edits shift 16–40 px, so every edit is registered and composited by deterministic OpenCV code. A published benchmark found that abnormal in-context examples barely move VLM accuracy, so the recall-lift headline has roughly a 35–50% chance; the eval is pre-registered with fallback headlines. Model API Terms §10.1(ix) bars training competing models on outputs, so the forged set is framed as evaluation data and in-context examples, which the Terms explicitly allow. The build is a FastAPI and React app over Muse Image, SAM 3.1 and Muse Spark 1.3, with an eval on the full MVTec hazelnut test split, a live real-hazelnut demo, a call-log trace and a replay mode. Freeze code at 23:30 IST Wed, upload the video by 02:30 IST Thu, and submit by 04:30 IST, three hours before the 07:30 IST deadline. Aim for Best Creative Build as the bonus that matches the core, and treat Most Viral as a one-hour "which crack is real?" post.

## Only Defect Forge clears the collision check and fits this team

The collision check is the freshest evidence here. On Nov 3 at about 19:00 UTC, GitHub showed **625 repos created after Oct 20** that call themselves Meta Global AI Developer Hackathon entries. Of 714 repos in the wider search, **Muse Image appears in 7.4% of descriptions** against 25% for Spark and 19% for SAM 3.x ([GitHub search](https://github.com/search?q=%22meta+global+ai+developer+hackathon%22+created%3A%3E2026-10-20&type=repositories); [Muse Image search](https://github.com/search?q=%22muse+image%22+created%3A%3E2026-10-20&type=repositories)). These counts come from public, self-describing repos only, and most of the roughly 20,000 participants are invisible. Treat them as a signal of crowding, not a census.

| Idea | Verdict | Decisive evidence | What would have changed it |
|---|---|---|---|
| **Defect Forge** | **GO, gated at 03:00 IST** | No visible entry has a "Muse Image forges defects, SAM labels them" core; it plays to the team's CV and labeling skills; total API cost under $30 | No defect type passes the realism test, even after one retry on a second category |
| **DemoScribe** | **NO-GO as primary; pivot only** | winnow, GlassBox, DemoDoctor and MimicAnno already cover the space; no robot-learning insider on the team | A robotics background, or an angle no competitor covers |
| **Find-and-Guide** | **NO-GO** | Netra and shipped products (Lookout, Seeing AI); four in-event rivals; no blind or low-vision tester; no Meta TTS; unmeasured latency | A committed BLV tester plus a measured p90 of 1.5 s or less, and neither can be produced in 30 hours |

**Defect Forge has no direct competitor.** Repo-description searches for "defect muse", "synthetic data muse image", "data augmentation muse" and "defect sam 3.1" all returned zero repos. Code search found 138 files matching `"muse-image-1.0" defect`, and none of the hits reviewed was a synthetic-defect generator ([GitHub repo search](https://github.com/search?q=%22synthetic+defect%22+created%3A%3E2026-10-20&type=repositories)). Several SAM-plus-Spark inspectors exist, such as viaguard, GridSight and sem-triage-agent, but none forges data ([viaguard](https://github.com/Foxcrack/viaguard); [GridSight](https://github.com/Divyanshu-kumar14/GridSight)). The closest prior art is academic. **AnomalyAgent** (Apr 2026) loops an MLLM agent through prompt generation, image generation, quality evaluation and mask generation. It reports 57.0% downstream classification accuracy against **44.7% for Gemini 3.1 Flash Image Preview used as a general editor** ([AnomalyAgent](https://arxiv.org/html/2604.07900v1)). That result validates the loop and sets expectations: general editors produce usable defects that trail specialist methods. No paper uses a Meta model, and none measures in-context gains from synthetic examples for a VLM inspector, so both are novel framings. Muse Image is a credible editor: on Meta-relayed Arena numbers it ranks **#2 in single-image editing (1405, behind GPT Image 2 at 1466)** ([DataCamp](https://www.datacamp.com/blog/meta-muse-image)).

**Walkdown is the overshadow risk, not a collision.** It is MIT-licensed, has 159 commits and a live demo, and is a corrosion-walkdown agent. SAM 3.1 segments rust, Spark grades it, Muse Wonder gives a second opinion, and it adds an on-prem open-weights mode and two Glimmer distillations, with claimed recall of 97.9% in the cloud and 92.4% on-prem. Crucially, it already used Muse Image to make "300 synthetic look-alike images for a false-alarm stress test; never trained on", labelled as evaluation-only under §10.1(ix) ([Walkdown README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)). A judge who has seen Walkdown will see Muse Image used for synthetic inspection data. The answer is to compete on generation, not inspection. Walkdown forges *negatives* inside an inspector, while Defect Forge is the *generator*: spec text in, positive defects with pixel labels out, measured on real defects. The video must open on generation, and the README must cite Walkdown as related work. CounterForge, which uses "controlled image changes, human-verified ground truth and repeated evaluation" to build VLM regression tests for object counting, is adjacent rather than colliding ([CounterForge](https://github.com/ottorafaelcihak/CounterForge)).

**The headline eval number is the weakest link.** The original pitch was "recall X% to Y% with forged examples in context." The best evidence argues for caution. In MMAD (ICLR 2025), the best model reached only **68.63% on anomaly discrimination**, against 95.24% for human experts. Adding an *abnormal* in-context image gave InternVL2-40B **+2.6 points on discrimination and −0.35 on average**, while text domain knowledge raised defect *classification* by 16.7–20.3 points ([MMAD](https://arxiv.org/html/2410.09453v3)). A 2026 thesis harness puts Flash-class models at **~89–91% balanced accuracy zero-shot** on a small DS-MVTec subset. That leaves little headroom, though the source is a single unreviewed repo ([IAD-VLMS](https://github.com/Apcin/IAD-VLMS)). Our estimate is a **35–50% chance** of a clean "≥10-point recall gain with ≤5-point specificity loss, statistically significant." With the fallbacks below, the chance of shipping **at least two defensible numbers is about 85%**. The fix is to pre-register several metrics and decide the headline from data at 17:30 IST, not to drop the idea.

**The Terms create a framing constraint, not a blocker.** Model API Terms §10.1(ix) bars using Outputs "to train, fine-tune, distill, or otherwise improve or create any artificial intelligence or machine learning model or other product or service that competes with Meta's models or services". It also bars systematically collecting Outputs "to build training datasets" for competing models, but states that "using Services or Outputs solely for evaluation, benchmarking, or quality assessment of your own systems does not constitute a prohibited use" ([Model API Terms](https://dev.meta.ai/legal/terms-of-service)). A participant's question to Meta about training on outputs was still unanswered on Oct 29 ([ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)). Framing the forged set as a test suite and as in-context exemplars for a Meta inspector sits inside the explicit safe harbor, and Walkdown's labelling is the precedent.

**Muse Image moves pixels.** The edits endpoint rejects `mask`, `input_fidelity`, `partial_images` and `seed` with a 400. `size` sets only the aspect ratio, returned dimensions "won't match the numbers exactly," and the only preservation promise is that it "changes only what you ask for while keeping the rest intact" ([Image generation docs](https://dev.meta.ai/docs/image-generation.md)). In practice it does not. Naqsh measured an edit that "shifts the page" by about 16 px, later 30–40 px, with clean plate edits in only 4 of 7 runs ([Naqsh submission notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)). Lumen and before-you-post independently composite only inside a mask because "Muse Image also changes pixels it was not asked to" ([Lumen](https://github.com/mikheilkuzmidi/lumen); [before-you-post](https://github.com/WhorideChicken/before-you-post)). Three teams hit the same wall, so registration, colour correction and diff-only compositing are mandatory in our design.

**DemoScribe is crowded at depth, not just at the pitch level.** winnow ("Standard Motion") is an Indie, Push-the-Frontier entry with 263 commits, last pushed Nov 3 17:56 UTC. It tracks "the gripper and objects from a seed box" with SAM 3.1, uses Spark for typed criteria, uses Voice for labelling, and outputs a "filtered dataset in the same (LeRobot) format + a Reason for every rejection" with Clopper-Pearson calibration ([winnow plan](https://github.com/kleongf/winnow/blob/HEAD/docs/plan.md)). GlassBox-SO101 does failure analysis with five Meta models ([glassbox](https://github.com/msheroubi/glassbox)). DemoDoctor does SAM 3.1 plus Spark Open failure investigation ([DemoDoctor](https://github.com/est4ever/DemoDoctor)). **MimicAnno** (Apache-2.0), part of the Gemma 4 Good first-place GEM-4 entry, already does signal-driven subtask boundaries, VLM phase labels with schema validation, SAM 3 tracking and a review UI ([MimicAnno](https://github.com/takaki-maeda-99/MimicAnno)). Winners in this format are domain insiders, and this team has no robot-learning experience. The technical risks also stay high. SAM 3 with a concept prompt scores **10.5 J&F on grippers** against 67.9 for SAM 2.1 with a box ([RobotSeg](https://arxiv.org/html/2511.22950v2)), and frontier VLMs score only 0.69–0.94 MAE on the 1–5 RoboReward scale ([RoboReward paper](https://arxiv.org/html/2601.00675v1)).

**Find-and-Guide fails on three external dependencies that more hours cannot buy.** Prior art includes Netra, third at Gemini 3, whose "Find My..." mode guides the user's hand with audio at a 200 ms tick ([Netra Devpost](https://devpost.com/software/netra-empowering-the-visually-impaired); [Gemini 3 gallery](https://gemini3.devpost.com/project-gallery)). Google Lookout's Find mode "can also tell you the direction and distance to the object" ([Lookout help](https://support.google.com/accessibility/android/answer/9031274)), and Microsoft built Find My Things into Seeing AI ([Microsoft Research](https://www.microsoft.com/en-us/research/story/find-my-things/)). Inside this hackathon, spatial-sense, SightGuide, Gözüm and Halo already chase the concept ([spatial-sense](https://github.com/Kaushal1025/spatial-sense); [SightGuide](https://github.com/fahad3235/sightguide); [Gözüm](https://github.com/gunbaz/gozum)). An empirical study concluded that **blindfolded users should not replace blind users** in evaluations ([drhu.eu](https://www.drhu.eu/2023/07/can-blindfolded-users-replace-blind-ones-in-product-testing-an-empirical-study/)). Meta's API offers no TTS ([Models](https://dev.meta.ai/docs/models)), and after the Nov 1 rule one team rated browser Web Speech "a judge-risky reading of the rule; do not prefer" ([soulbound compliance doc](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)). No first-party SAM latency figure exists ([SAM segmenting](https://dev.meta.ai/docs/sam/segmenting.md)). The strongest counterargument is that Impact carries 30% and accessibility wins often. It still fails here, because its core moment depends on a tester and a latency the team cannot guarantee by 07:30 IST.

## Refine Defect Forge into a spec-driven defect test suite, gated at 03:00 IST

### Five refinements the evidence forces

The idea stays the same: Muse Image forges defects onto photos of a good part, SAM 3.1 labels them to the pixel, and Muse Spark turns the spec into a taxonomy, critiques the forgeries and inspects real parts. Five things change.

First, **reframe the output as a defect test suite**. The pitch becomes: "Before your line has produced a single defect, Defect Forge forges the defects your spec describes, labels them to the pixel, and shows which ones your inspector would miss; the same forgeries, shown in context, teach a Meta inspector." This keeps the work inside the §10.1(ix) evaluation safe harbor, separates it from Walkdown's false-alarm negatives, and keeps the impact story. Synthetic defect data is commercially live: Roboflow and NVIDIA report 0.95 mAP for Corning from **8 real defect images** plus synthetic ones ([Roboflow](https://roboflow.com/blog/synthetic-data-generation-manufacturing-nvidia)), and Overview.ai's Auto Defect Creator needs "a handful of real samples" ([Overview.ai](https://www.overview.ai/blog/top-10-zero-defect-manufacturing-technologies-2026/)). Defect Forge needs **zero real defects**, and that is the wedge.

Second, **use MVTec AD hazelnut for the benchmark and real hazelnuts for the live demo.** Hazelnut defects (crack, cut, hole, print) are local and high-contrast, the photos are top-down on a dark background, and you can damage store-bought hazelnuts one-to-one with the MVTec defect types. The download is 588 MB per category under CC BY-NC-SA 4.0 ([MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad); [MVTec downloads](https://www.mvtec.com/company/research/datasets/mvtec-ad/downloads)). Ship a download script, never the images. Build the video's hero grid and all DEMO_MODE fixtures from **your own hazelnut photos**, so nothing NC-SA ends up in the repo or the public video. VisA cashew, under CC BY 4.0 per Amazon's README, is the license-clean backup, but anomalib lists VisA as NC-SA, so the license question is unresolved ([VisA](https://github.com/amazon-science/spot-diff); [anomalib](https://anomalib.readthedocs.io/en/v1/markdown/guides/reference/data/image/visa.html)).

Third, **put a deterministic core between the models.** Every Muse Image output is resized, registered, colour-matched, diffed and composited back only inside the changed region. Validators that no model can fool then check pixel identity outside the mask, overlap with the part mask, defect size, and SAM-versus-diff agreement. This is the Wrench Board and TARA pattern adapted to images: deterministic code does the verification, and the models do perception and judgment.

Fourth, **pre-register an eval on the full test split with four conditions and fallback headlines** (detailed in the depth section). Use the full split instead of the earlier plan's 40 images, because at n≈70 defectives a recall of 0.7 has a Wilson half-width of about ±10.5 points, against ±19 at n=20 (our arithmetic).

Fifth, **make the work visible and physical.** Run one hero forge through the Responses API so Muse Image's reasoning summary is on screen. Show the critic rejecting a forgery live. Inspect a hazelnut you damaged yourself under the webcam. Keep a call log with model IDs, latency and cost. Two items from the earlier plan are dropped. The Muse Wonder planner goes because Walkdown measured that Wonder's second opinion did not improve accuracy (73.5% agreement before, 72.7% after) ([Walkdown README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)). The Glimmer critic goes because it needs a GPU you do not have.

### Six gate tests decide go, narrow or pivot by 03:00 IST

| # | IST (Wed Nov 4) | Owner | Test | Pass | If it fails |
|---|---|---|---|---|---|
| T0 | 00:45–01:00 | A | Claim the $150 credits, create a key, call `/v1/models`, read the `x-ratelimit-remaining-*` headers. B starts the hazelnut download | Key works on all three models | File at dev.meta.ai/support (a known key-creation bug); use B's key meanwhile ([ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)) |
| T1 | 01:00–01:30 | A | One `/v1/images/edits` call on a 512 px crop of a train/good hazelnut. Grid: `reasoning_strength` low vs high × tools on vs off. Log latency, returned size, and drift (mean absolute difference after resize and alignment) | Low with tools off takes under ~60 s, and the diff isolates a compact region | Slow but working: batch overnight anyway. Errors on "crack": rephrase ("a split", "a small hole"); filtered images are free |
| T2 | 01:30–02:15 | A | 3 defect types (hole, crack, print) × 5 samples × 2 prompt styles: (a) text naming the location at the crop centre; (b) a red outline drawn on the crop with "paint the defect inside the red outline, then remove the outline". Plus one whole-image edit as a control. Composite all of them | Diff-pasted results look plausible to the builder | Move to the outline style or whole-image edits |
| T3 | 01:00–01:30 | B | SAM 3.1 box prompts from ground-truth boxes on 10 real hazelnut test defects; IoU against the GT masks. Concept prompt "hazelnut" for the part mask | Median IoU ≥ 0.5, and a clean part mask | Pad boxes 20–50%, crop and upsample; fall back to diff masks as labels |
| T4 | 01:30–02:15 | B | 20 test images (10 good, 10 defective): zero-shot vs an **oracle** with 4 real held-out defect examples in context. Validate the JSON schema and the 0–1000 box parsing | Zero-shot balanced accuracy between 55% and 90%, and the oracle adds ≥5 points of recall | If even real examples don't help, make label quality and realism the headline now. If zero-shot is ≥90%, headline per-type recall and box hits |
| T5 | 02:15–03:00 | B, then A | B blind-rates 10 forged and 10 real crops in random order; the Spark critic scores the same 10 forgeries | ≥2 defect types with ≥3 of 5 rated realistic; the critic agrees on ≥4 of 5 | See the gate outcomes below |

The thresholds come from the Defect Forge feasibility analysis, so they are judgment calls rather than published benchmarks. Their purpose is to force the decision at hour 2, not hour 20. Post two questions in Discord #questions during T0 and re-ask at office hours (weekdays 10–11 ET, which is 20:30–21:30 IST Wed): can one project win a track prize plus bonuses, and does evaluation-only use of Muse Image outputs satisfy §10.1(ix)?

### Three gate outcomes and the pivot path

| Outcome at 03:00 IST | Condition | Action |
|---|---|---|
| **Green** | ≥2 defect types pass T5, and T3 median IoU ≥ 0.5 | Full Defect Forge as planned |
| **Amber** | Exactly one type passes, or only coarse "print/stain" defects look real | Continue, narrowed to the passing types. Spend at most 1 hour on a second small MVTec category with coarse defects: bottle (148 MB, contamination and broken rim) or metal_nut (157 MB, color and scratch only). Lead the headline with labels and per-type inspection |
| **Red** | No type passes, even with outline prompts, whole-image edits and the second category | Pivot by **04:00 IST** at the latest to the narrow DemoScribe described below |

The pivot is deliberately narrow, because full DemoScribe loses on collision. It becomes **an episode grader benchmarked against a public human-verified leaderboard**. The RoboReward test split's `droid` and `bridge` folders hold 200 H.264 faststart MP4s (about 120 MB, CC-BY-4.0, exactly 20 clips per reward level) that SAM 3.1 accepts without transcoding ([RoboReward](https://huggingface.co/datasets/teetone/RoboReward)). The published MAE rows run from **0.691 for GPT-5 mini to 1.485 for Llama 4 Scout** ([RoboReward paper](https://arxiv.org/html/2601.00675v1)). A Spark-only baseline over all 200 clips can run within an hour of the pivot. It should be positioned against winnow as "a measured grader on a public benchmark," which no visible competitor reports. About 60% of the code carries over: the Meta client layer, the cost ledger, replay, the call-log UI and the eval harness's statistics (our estimate). Expect a lower ceiling than Green Defect Forge. The pivot buys a defensible submission, not a favourite.

## Build a three-model loop around a deterministic OpenCV core

### Architecture

```
 spec.txt / spec.pdf + 5 good-part photos (MVTec train/good, or your own via phone)
        │
 [1] Taxonomy ── muse-spark-1.3 (Responses, effort=medium, strict JSON)
        │          → [{defect_type, clause, size_pct_of_part, zone, description}]
 [2] Locate ──── sam-3.1 concept "hazelnut" → part mask → sample on-part patch centres
 [3] Forge ───── muse-image-1.0 /v1/images/edits, 512 px crop, defect at centre,
        │          reasoning_strength=low, all tools off (batch); Responses + search on (hero shot)
 [4] Composite ─ OpenCV only: resize → ECC align → ring colour-match → LAB diff → Otsu →
        │          largest central component → feathered paste of the diff region only
 [5] Label ───── diff bbox (+20–50% pad) → sam-3.1 box prompt → mask; diff mask if IoU < 0.3
 [6] Critic ──── muse-spark-1.3 (effort=low): realism 1–5, clause match, artifacts,
        │          revised_prompt → re-forge up to 2× (agentic retry)
 [7] Validate ── deterministic V1–V8 (pixel identity outside mask, in-part, size, SAM/diff IoU,
        │          single component, critic ≥4, pHash dedupe, provenance complete) → "8/8"
 [8] Export ──── COCO JSON + RLE masks + provenance JSONL (model, response id, prompt hash, $, ms)
 [9] Inspect ─── muse-spark-1.3: cached prefix [spec + 2 good + 8 forged] + query image
        │          → {defect, type, has_box, x0..y1 (0–1000), confidence} → sam-3.1 box → mask
        │          sanitizer: no "defect" without a SAM mask behind it (else "uncertain")
 [10] Eval ───── C0–C3 on the full MVTec hazelnut test split; Wilson CIs; exact McNemar
 UI: React/Vite ← SSE events {stage_start, call_completed{model, ms, $, cached}, validator, verdict}
 Modes: LIVE (default) | DEMO_MODE=1 (SHA-256 input hash → replay recorded run, amber badge)
```

Stages 4, 7 and 10 make up the core, and none of them calls a model. That is the property the Opus winners shared: "LLM does perception and judgment, deterministic code does computation and verification" ([Anthropic winner teardowns: Wrench Board's simulator](https://github.com/Junkz3/wrench-board); [TARA validator](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py)). OpenCV is explicitly allowed under the runtime rule: "Non-model libraries such as OpenCV are fine" ([soulbound compliance doc](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)). Keep every learned component on Meta's side. That means no LPIPS, CLIP, rembg or MediaPipe anywhere, and no Inception-based IS scores even offline. The community realism metrics need non-Meta networks, which muddies the story.

The backend is Python (FastAPI plus asyncio), because the SAM parser, OpenCV and the statistics all live there. The frontend is React, Vite, TypeScript and Tailwind, because Streamlit is on the kickoff's anti-project list ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)). State lives on disk as JSON, with no database and no auth. Build every capture path behind one "frame source" interface (file upload, phone capture, webcam), so a hardware problem costs a demo moment, not the submission.

### Exact Meta API call patterns

**Client.** The SDKs do not read `MODEL_API_KEY`, so pass it explicitly and pin every model ID. Omitting `model` can silently fall back to 1.1 ([SDKs](https://dev.meta.ai/docs/sdks); [Quickstart](https://dev.meta.ai/docs/quickstart)). Meta's workshop client uses `max_retries=4, timeout=180` ([legal-agent-workshop client.py](https://github.com/meta-models/legal-agent-workshop/blob/HEAD/agent/agent_kit/client.py)).

```python
import os, base64, json, httpx
from openai import OpenAI
BASE, KEY = "https://api.meta.ai/v1", os.environ["MODEL_API_KEY"]
client = OpenAI(base_url=BASE, api_key=KEY, max_retries=4, timeout=180)

def data_url(b: bytes, mime="image/jpeg") -> str:
    return f"data:{mime};base64,{base64.b64encode(b).decode()}"
```

**Spark taxonomy (Responses API, strict schema).** Reasoning tokens share `max_output_tokens`, so set it to at least 4,000. Naqsh saw "398 of 400 output tokens were reasoning" and got an empty `incomplete` answer ([Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md); [Reasoning](https://dev.meta.ai/docs/reasoning)). Strict schemas must be flat objects with every key required and `additionalProperties:false`. `allOf`, `oneOf` and recursion return 400 ([Structured output](https://dev.meta.ai/docs/structured-output)).

```python
r = client.responses.create(
    model="muse-spark-1.3", reasoning={"effort": "medium"}, max_output_tokens=6000,
    text={"format": {"type": "json_schema", "name": "taxonomy", "strict": True, "schema": TAXONOMY_SCHEMA}},
    input=[{"role": "user", "content": [{"type": "input_text", "text": spec_text}]}])
taxonomy = json.loads(r.output_text)
```

**Spark critic and inspector (Chat Completions, strict schema, cached prefix).** Walkdown runs hosted Spark this way, with `json_schema` set to `strict: true`, `reasoning_effort="low"`, `max_tokens=4000` and `prompt_cache_key`, and reports "612 of ~990 input tokens were cached" ([Walkdown DECISIONS.md](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/docs/DECISIONS.md)). Cached input costs $0.15 per million tokens against $1.25 uncached ([Pricing](https://dev.meta.ai/docs/pricing-rate-limits)). Images count only in the `user` role, at most 50 per request and about 1,300–1,500 tokens for a ~1,280 px image. Boxes come back on a 0–1000 grid that can return 1001, so clamp them ([Image understanding](https://dev.meta.ai/docs/image-understanding.md)). To keep the strict schema flat, model the box as four integers plus `has_box` rather than a nullable array. This is our workaround and has not been tested against the API.

```python
INSPECT = {"type": "object", "additionalProperties": False,
  "required": ["defect", "type", "has_box", "x0", "y0", "x1", "y1", "confidence", "rationale"],
  "properties": {"defect": {"type": "boolean"},
    "type": {"type": "string", "enum": ["good", "crack", "cut", "hole", "print"]},
    "has_box": {"type": "boolean"}, "x0": {"type": "integer"}, "y0": {"type": "integer"},
    "x1": {"type": "integer"}, "y1": {"type": "integer"},
    "confidence": {"type": "number"}, "rationale": {"type": "string"}}}

resp = client.chat.completions.create(
    model="muse-spark-1.3", reasoning_effort="low", max_tokens=4000,
    response_format={"type": "json_schema", "json_schema": {"name": "inspection", "schema": INSPECT, "strict": True}},
    extra_body={"prompt_cache_key": f"hazelnut-{condition}-v1"},
    messages=[{"role": "system", "content": SPEC_AND_RULES},          # text only
              {"role": "user", "content": [*exemplar_parts,               # fixed prefix first (cacheable)
                  {"type": "text", "text": "Inspect this part."},
                  {"type": "image_url", "image_url": {"url": query_url}}]}])  # query image last
out = json.loads(resp.choices[0].message.content)
box_px = [min(max(v, 0), 1000) / 1000 * dim for v, dim in zip([out["x0"], out["y0"], out["x1"], out["y1"]], [W, H, W, H])]
```

**Muse Image batch edit (raw JSON, not the SDK).** The OpenAI SDK always sends multipart. The JSON `images` array (1–10 items) needs raw HTTP with `Content-Type: application/json`, or you get a 415. `reasoning_strength` and `tool_enablement` are top-level fields. Any unknown top-level JSON field, including `seed`, returns 400. Safety blocks come back as a free 400 `content_policy_violation`. Per the docs, 503 is retryable and 500 is not ([Image generation docs](https://dev.meta.ai/docs/image-generation.md)). Naqsh posts exactly this body and measured **13.6 s and $0.01 per edit** ([Naqsh meta.py](https://github.com/lleoparden/naqsh/blob/HEAD/backend/app/pipeline/meta.py); [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)). The model is limited to **150 RPM per team**, so put an asyncio semaphore of about 2 calls per second in front of it ([Pricing](https://dev.meta.ai/docs/pricing-rate-limits)).

```python
payload = {"model": "muse-image-1.0", "prompt": prompt, "n": 1,
           "images": [{"image_url": data_url(crop_png, "image/png")}],
           "output_format": "png", "response_format": "b64_json", "reasoning_strength": "low",
           "tool_enablement": {"enable_image_search": False, "enable_web_search": False, "enable_shell": False}}
r = httpx.post(f"{BASE}/images/edits", json=payload, headers={"Authorization": f"Bearer {KEY}"}, timeout=150)
edited_png = base64.b64decode(r.json()["data"][0]["b64_json"])   # size will NOT equal the crop
```

**Muse Image hero shot (Responses, search on, reasoning summary visible).** The cookbook calls `responses.create(model="muse-image-1.0", ...)`. The image comes back as base64 in `result` on the output item whose `type == "image_generation_call"`. A bare list of content parts is rejected with a 400, so wrap the parts in a user message. Meta's robotics demo adds `tools=[{"type":"image_generation","output_format":"png"}]`, `store=False` and the prompt suffix "Preserve identity and framing" ([Muse Image fundamentals](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/05_muse_image/01_image_api_fundamentals/README.md); [muse_image.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/full_demo/muse_image.py)). The Responses API also returns a short reasoning summary item, which is the on-screen proof of Meta's "agentic" image model ([Image generation docs](https://dev.meta.ai/docs/image-generation.md)). Select output items by type, never by position.

```python
r = client.responses.create(model="muse-image-1.0", store=False,
    tools=[{"type": "image_generation", "output_format": "png"}],
    input=[{"role": "user", "content": [
        {"type": "input_text", "text": prompt + " Preserve identity and framing."},
        {"type": "input_image", "image_url": data_url(crop_png, "image/png")}]}])
img_b64 = next(o for o in r.output if o.type == "image_generation_call").result
summary = [o for o in r.output if o.type == "reasoning"]   # show in the trace panel; not guaranteed
```

**SAM 3.1 (non-streaming, Meta's own pattern).** Meta's robotics demo calls `responses.create(model="sam-3.1", input=[...], metadata={"mask_encoding":"one_bit"}, store=False)`. It then feeds `output_text` to `image_segmentation_format().create_parser()`, pastes each mask raster at `record.bounds.left/top` (masks are **box-local**), and resizes with NEAREST when sizes differ ([sam_preview.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/full_demo/sam_preview.py)). Confidence appears only when `include_confidence` is the string `"true"`. Payloads are base85, so use the parser ([meta-sam Python README](https://github.com/meta-models/meta-sam/blob/HEAD/python/README.md)). If you stream instead, copy the cookbook's `stream_events`, because "the API streams `response.content_part.done` but not `response.output_text.done`" ([sam_api.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/python/sam_api.py)). Box prompts need a `<Nf>` frame header, or you get a 400. Build them with the parser's `build_object_prompt`, not by hand ([Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)).

```python
from meta_sam_parser import image_segmentation_format, CompletedOutcome, build_object_prompt  # verify names against sam_preview.py
sam = OpenAI(base_url=BASE, api_key=KEY, timeout=30, max_retries=0)       # our own retry wrapper on top
prompt_text = "hazelnut"                                                 # concept: part mask only
prompt_text = build_object_prompt(...)                                   # defects: box prompt(s), <0f> header, pixel coords
r = sam.responses.create(model="sam-3.1", store=False,
    metadata={"mask_encoding": "one_bit", "include_confidence": "true"},
    input=[{"type": "message", "role": "user", "content": [
        {"type": "input_text", "text": prompt_text},
        {"type": "input_image", "image_url": data_url(img_jpeg)}]}])
p = image_segmentation_format().create_parser(); p.push(r.output_text); p.finish(CompletedOutcome())
# empty result = "not found" (valid, still billed); paste each box-local raster at bounds.left/top
```

**Composite (deterministic; sketch with our helper names).**

```python
def composite(orig, edited):                              # BGR uint8; orig is the 512x512 crop
    ed = cv2.resize(edited, orig.shape[1::-1], interpolation=cv2.INTER_AREA)
    _, warp = cv2.findTransformECC(gray(orig), gray(ed), np.eye(2, 3, dtype=np.float32),
                                   cv2.MOTION_AFFINE, CRITERIA, None, 5)
    ed = cv2.warpAffine(ed, warp, orig.shape[1::-1], flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP)
    ed = match_colour_on_ring(ed, orig)                   # Lumen-style drift removal on an annulus
    diff = cv2.absdiff(to_lab(orig), to_lab(ed)).max(axis=2)
    _, m = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    m = largest_component_near_centre(open_close(m))     # ignore global re-render noise
    a = cv2.GaussianBlur(dilate(m, 3), (0, 0), 2)[..., None] / 255.0
    out = (a * ed + (1 - a) * orig).astype(np.uint8)
    assert (out[a[..., 0] == 0] == orig[a[..., 0] == 0]).all()   # V1: identical outside the mask
    return out, m
```

**Retry.** Retry 429, 5xx, timeouts and connection errors with exponential backoff plus jitter from 0.5 s, honour `Retry-After`, and never retry 400, 401 or 404. The cookbook's own `RETRYABLE` tuple leaves out `APIStatusError` (5xx), so add it. Read `x-ratelimit-remaining-*` through `with_raw_response` ([error handling notebook](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/01_api_fundamentals/09_error_handling.ipynb)). Rate limits apply per team, not per key, so Person A's batch and Person B's eval share one budget ([Pricing](https://dev.meta.ai/docs/pricing-rate-limits)). Spark Standard allows 3,000 RPM. Avoid Contributor mode, which is capped at 150 RPM and may use your content for training.

### Gotchas that have already bitten other teams

| Gotcha | Symptom | Fix | Source |
|---|---|---|---|
| Key not auto-read | 401 | Pass `api_key=` | [SDKs](https://dev.meta.ai/docs/sdks) |
| Reasoning eats the output budget | Empty or `incomplete` answer | `max_tokens`/`max_output_tokens` ≥ 4,000; effort low or minimal | [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md) |
| `reasoning.effort: "none"` | 400 | Use `minimal` or `low` | [Reasoning](https://dev.meta.ai/docs/reasoning) |
| `tool_choice` only "auto" | 400 on "required" | Use strict JSON schemas for deterministic steps | [Tool calling](https://dev.meta.ai/docs/tool-calling) |
| Strict schema limits | 400 on `oneOf`/recursion | Flat object, all keys required, `additionalProperties:false` | [Structured output](https://dev.meta.ai/docs/structured-output) |
| Images outside the user role | Silently ignored | Images only in user turns; ≤50 per call | [Image understanding](https://dev.meta.ai/docs/image-understanding.md) |
| 0–1000 grid returns 1001 | Off-by-one overlays | Clamp to 0–1000 | [Image understanding](https://dev.meta.ai/docs/image-understanding.md) |
| Muse Image `mask`/`seed`/`input_fidelity`/`partial_images` | 400 | Crop, edit, register, composite | [Image generation](https://dev.meta.ai/docs/image-generation.md) |
| JSON edit body with the wrong Content-Type | 415 | `httpx.post(json=...)` | [Image generation](https://dev.meta.ai/docs/image-generation.md) |
| Edit shifts 16–40 px; size differs from request | Misaligned diff | Resize + ECC align before diffing | [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md) |
| Edit changes pixels it was not asked to | Global colour drift | Ring colour-match; paste only the diff component | [Lumen](https://github.com/mikheilkuzmidi/lumen) |
| Responses with a bare content list | 400 | Wrap in `{"role":"user","content":[...]}` | [Muse Image fundamentals](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/05_muse_image/01_image_api_fundamentals/README.md) |
| SAM masks are box-local | Masks in the wrong place | Paste at `bounds.left/top` | [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md) |
| SAM box prompt without `<Nf>` | 400 | `build_object_prompt` | [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md) |
| SAM concept text finds nothing | 200 OK, billed, empty | Concept only for "hazelnut"; boxes for defects | [Naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md) |
| SAM coordinates are post-EXIF | 400 on aspect mismatch | `ImageOps.exif_transpose`, resize ≤1,280 px, send that exact image | [SAM overview](https://dev.meta.ai/docs/sam/overview.md) |
| SAM stream lacks `output_text.done` | Parser never closes | Non-streaming call, or the cookbook's `stream_events` | [sam_api.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/python/sam_api.py) |
| SAM weak on tiny or thin defects | Low IoU | Pad the box, crop and upsample; diff-mask fallback; negative point on clean surface | [SAM 3 remote-sensing eval](https://arxiv.org/pdf/2607.09583) |

### Copy from MIT and Apache repos, re-implement the rest

MIT and Apache-2.0 code can be copied if you keep the license text (and, for Apache, the NOTICE and a note of changes) in `THIRD_PARTY.md`. Code with no license is "all rights reserved", so read it for patterns only. One judgment call: Naqsh, Walkdown and Lumen are competing entries in this hackathon. Their MIT and Apache licenses allow copying, but lifting whole files from a rival may read badly to judges. Take the official Meta cookbook first, copy rival code only in small attributed utilities, and re-implement anything you can rewrite in minutes. This is our inference about optics, not a rule.

| Source | License | Take | Use as |
|---|---|---|---|
| [meta-model-cookbook](https://github.com/meta-models/meta-model-cookbook) `07_sam/.../sam_api.py`, `14_muse_robotics/full_demo/sam_preview.py`, `muse_image.py`, `09_error_handling.ipynb` | MIT | `image_data_url`, `segment_image`, `stream_events`, `validate_result`, full-frame mask paste, Muse Image Responses call, retry table | **Copy** (core of `meta/`) |
| [meta_sam_parser 0.1.0](https://pypi.org/project/meta-sam-parser/) / `@meta-sam/parser` | SAM License | Parser, `build_object_prompt`, `decode_mask_to_rle` | **Dependency** |
| [meta-sam](https://github.com/meta-models/meta-sam) API Playground (`StreamLog.tsx`, `RawOutput.tsx`, `PromptOverlay.tsx`) | SAM License | Call-log and overlay UI ideas | Reference; copy only after reading the SAM License |
| [Naqsh](https://github.com/lleoparden/naqsh) `meta.py`, `segment.py`, `demo.py`, `spend.py` | MIT | `_post` retry with `max(Retry-After, 1.5·(n+1))`, JSON edit body, box-prompt paste fallback, DEMO_MODE hash-and-replay with amber badge, JSONL cost ledger | Small attributed copies, or re-implement |
| [Walkdown](https://github.com/joshuakarthik2005/Walkdown) `perception/sam.py`, DECISIONS.md | MIT | COCO-RLE mask cache keyed by output hash; strict schema + `prompt_cache_key` settings | Pattern / small copy |
| [Lumen](https://github.com/mikheilkuzmidi/lumen) | Apache-2.0 | Ring-based colour-drift removal; upscaling small crops before editing | Copy with NOTICE |
| [CrossBeam](https://github.com/mikeOnBreeze/cc-crossbeam) `app-mode.ts`, tests L0–L4 | MIT | `dev-test`/`judge-demo`/`real` modes, Showcase + Run Live buttons, layered test ladder | Copy and adapt |
| [Elisa](https://github.com/zoidbergclawd/elisa) `MissionControl/` | MIT | `MetricsPanel`, `CommsFeed` React components (cost and tokens per call) | Copy and adapt |
| [TARA](https://github.com/Kye256/tara-transport-assessment) `vision_assess.py`, `test_pipeline.py` | MIT | JSON assessor with retry and deterministic mock; md5 input cache; "12/12" validator printout | Port |
| [Virtual Puppet Theater](https://github.com/rhmoller/virtual-puppet-theater/blob/main/server/asset-generator.ts) | MIT | Description-hash generation cache; `limits.ts` | Copy (Muse Image cache) |
| [Llama CCTV Operator](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_event_detector.py) | Apache-2.0 | Multi-image message builder + `json_schema` | Copy (inspector prompt builder) |
| [MimicAnno](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/vlm_labeler.py) | Apache-2.0 | `parse_and_validate` with a retry instruction per failure type | Copy (critic/inspector validation) |
| [geo-lm](https://github.com/williamjsdavis/geo-lm) | MIT | LLM → constrained JSON → validator → deterministic builder | Pattern (spec → taxonomy) |
| [winnow](https://github.com/kleongf/winnow/blob/HEAD/backend/src/standard_motion/meta/replay.py) | None | Recording/Replay transports for tests and demo | **Pattern only** |
| [legal-agent-workshop](https://github.com/meta-models/legal-agent-workshop/blob/HEAD/README.md) | None | `run_verification(ctx, work) -> {passed, feedback}` run outside the agent's control | **Pattern only** |
| [ARIA](https://github.com/zestones/Aria/blob/main/frontend/src/features/agents/AgentInspector.tsx) | None | Event vocabulary and an inspector drawer | **Pattern only** |
| [Wrench Board](https://github.com/Junkz3/wrench-board/blob/main/benchmark/README.md) | Proprietary | Frozen oracle with a provenance contract; outbound sanitizer | **Pattern only** |
| glassbox, meta-hack, Netra, MedKit | None or not licensed | Provenance tags, `getUserMedia` loop, Zod card contracts | **Pattern only** |

## Develop locally on Windows, tunnel for the phone, deploy only a replay

### Repo layout

Create a **fresh public repo today** (MIT license). Organizers relayed that the repo should be "a standalone extract" with only event work, created Oct 26 or later, with pre-existing material labeled ([ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md); [muse-muse MESSAGING.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/MESSAGING.md)). Commit early and often. CrossBeam won first place with 63 commits ([teardown counts](https://github.com/mikeOnBreeze/cc-crossbeam)), so a dense history covering Nov 4 IST is itself evidence of in-event work.

```
defect-forge/
  README.md  EVAL.md  LICENSE  THIRD_PARTY.md  .env.example  .gitattributes  .gitignore
  docs/        architecture.png  friction-log.md  build-log.md  results/*.json
  backend/app/ main.py (FastAPI, SSE /events)  routes/
    meta/      client.py  spark.py  muse_image.py  sam.py  retry.py  ledger.py  replay.py
    forge/     taxonomy.py  locate.py  crop.py  composite.py  label.py  critic.py  validators.py  batch.py
    inspect/   inspector.py  sanitize.py
    export/    coco.py
  eval/        download_mvtec.py  split.py (frozen IDs + SHA-256)  run_eval.py  metrics.py
               realism_test/ (static 2AFC page)  home_set/ (your photos, owned)
  frontend/    (Vite + React + TS + Tailwind) pages: Forge, Dataset, Eval, LiveInspect
               components: CallLogDrawer, StageTimeline, ForgeGrid, BeforeAfter, MaskOverlay, EvalTable
  fixtures/    demo runs recorded on your own hazelnut photos only (no MVTec images)
  tests/       pytest with a recorded transport (L0–L4 ladder + validators)
  scripts/     setup.ps1  setup.sh  dev.ps1  dev.sh  tunnel.ps1
```

### Windows setup and the HTTPS problem

Put the repo at a path without spaces, such as `D:\dev\defect-forge`, because some tooling breaks on paths like `D:\Meta AI hackathon` (our inference). Use the Python launcher (`py -3.12 -m venv .venv`, then `.venv\Scripts\python -m pip install openai meta-sam-parser fastapi uvicorn httpx opencv-python-headless numpy pillow scipy python-dotenv sse-starlette pytest`) and call `.venv\Scripts\python` directly, which avoids PowerShell activation-policy friction. Use Node 20 with `npm create vite@latest frontend -- --template react-ts`. Proxy `/api` from Vite to `localhost:8000`, so one origin serves both. Defect Forge needs no ffmpeg, which matters because ffmpeg is not installed on this machine (local check during research). Judges will clone on macOS or Linux, so ship `setup.sh` next to `setup.ps1`, add `.gitattributes` with `* text=auto`, and use `pathlib` everywhere. Keep the laptop from sleeping during the overnight batch.

The laptop webcam works without HTTPS, because a page on `localhost` is a secure context. The phone is different. `getUserMedia` "is available only in secure contexts (HTTPS)", and on an insecure origin `navigator.mediaDevices` is `undefined` ([MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)). A phone opening the laptop's LAN IP over HTTP gets no camera. The robust path is a quick tunnel, `cloudflared tunnel --url http://localhost:5173`; `cloudflared` is already on this machine's PATH (local check). Vite's dev server will probably need `server.allowedHosts: ['.trycloudflare.com']` before it serves the tunnel hostname (our inference from recent Vite host checks). For stills, use `<input type="file" accept="image/*" capture="environment">`, which hands off to the phone's native camera with autofocus and macro modes ([MDN capture](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/capture)). Normalize EXIF and resize to 1,280 px or less on the server before calling SAM.

### Deploy decision

Do not deploy a live backend. Organizers said "A public live URL is not required… judging doesn't depend on it", and judges "mainly work from your 3-minute demo video and your public GitHub repo" and "may also try the project themselves, using their own keys" ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10); [muse-muse HANDOFF.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/HANDOFF.md)). A public backend would expose your key and budget for no scoring gain. As a nice-to-have after code freeze, deploy a **static DEMO_MODE frontend** (for example on Vercel) that replays fixtures recorded on your own photos, with the amber replay badge. That gives the X post and Community Vote a clickable link. The Oct 31 answer allows a demo-mode deployment only if "the repo still runs live from its setup instructions and the README explains how to use the demo mode" ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)).

### What the README must say

| Section | Content | Why |
|---|---|---|
| Hero | 15-s GIF of the forge grid filling, the video link, one-line pitch | Winners lead with the artifact ([TARA README](https://github.com/Kye256/tara-transport-assessment)) |
| **Meta models and where they run** | `muse-spark-1.3` (Meta Model API, Meta-hosted): taxonomy, critic, inspector. `muse-image-1.0` (Meta Model API): defect forging. `sam-3.1` (Meta Model API): part masks, defect masks. "No other model runs at runtime; OpenCV, NumPy and SciPy are classical code; no TTS, embeddings or local networks" | Nov 1 rule: "Say in your README which Meta models you use and where they run" ([soulbound](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)) |
| Prior work and third-party code | "Repo created Nov 4 2026; no pre-existing project code." List copied MIT/Apache files in `THIRD_PARTY.md` | Prior-work guidance ([ConformScope](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)) |
| Quickstart (live) | `setup.ps1`/`setup.sh`, `.env.example` with `MODEL_API_KEY=`, `download_mvtec.py`, one command to run | "the repo must run from its setup instructions" ([HANDOFF.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/HANDOFF.md)) |
| Demo mode | `DEMO_MODE=1` replays recorded runs with a visible badge; live is the default | Oct 31 demo-mode answer ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)) |
| Results | EVAL.md link with its pre-registration commit hash; condition table with CIs; SAM IoU; realism; cost and latency per sample; home mini-set counts | The depth bar (next sections) |
| Architecture | Diagram plus a "why each Meta model is needed" table | CrossBeam rewrote its landing page because judges "want to see the architecture" ([progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)) |
| Data and Terms | MVTec CC BY-NC-SA, not redistributed. Forged outputs used for evaluation, benchmarking and in-context inspection by Meta models, consistent with §10.1(ix) | [MVTec](https://www.mvtec.com/company/research/datasets/mvtec-ad); [Terms](https://dev.meta.ai/legal/terms-of-service) |
| Related work | AnomalyAgent, UniDG, DualAnoDiff, MMAD, Walkdown, CounterForge | Pre-empts the "already exists" critique |
| Friction log, tests, license | API quirks found; `pytest` count; MIT | Feeds the "Feedback on Meta products" field |

## Scope for two people and thirty hours

### Must, nice and cut

The must list comes to about 21 working hours per person, which fills the available time after one sleep block and short naps. Nice-to-haves are allowed only when a must item finishes early, in the order listed.

| Priority | Item | Owner | Hours |
|---|---|---|---|
| Must | Gate tests T0–T5 | A + B | 2 + 2 |
| Must | Meta client layer: Image + SAM clients, retry, cost ledger, replay transport | A | 1.5 |
| Must | Spark client + inspector module (shared by the eval and Live Inspect) | B | 1 |
| Must | Forge core: taxonomy, part mask, crop sampler, edit, register/colour-match/diff/composite | A | 3.5 |
| Must | Label (SAM box + diff fallback), critic with `revised_prompt` retry, validators V1–V8, provenance, COCO export | A | 2.5 |
| Must | Batch runner: 150 RPM semaphore, cache, resume | A | 1 |
| Must | Eval harness: split and freeze, EVAL.md pre-registration, C0–C3 × 2 runs, Wilson, McNemar, per-type, box hit | B | 4 |
| Must | SAM IoU against real GT masks; SAM-vs-diff IoU on forgeries | B | 1 |
| Must | Blind 2AFC realism page + 5–10 raters | B | 1.5 |
| Must | UI golden path: spec → taxonomy cards → forge grid → before/after slider with mask → export, plus call-log drawer and stage timeline (SSE) | A | 4 |
| Must | DEMO_MODE replay + Showcase / Run Live buttons | A | 1 |
| Must | Live Inspect page: webcam + phone capture → inspector → SAM overlay → sanitizer | A | 1.5 |
| Must | Hero Muse Image shot via Responses with reasoning summary | A | 0.5 |
| Must | Hazelnut rig; 10 good + 10 self-damaged home mini-set; home forge grid for the video | B | 2 |
| Must | ~60 pytest cases on a recorded transport; validator "N/N" report | B | 1.5 |
| Must | Eval tab UI (results table component) | B | 1 |
| Must | README, model table, EVAL results, friction log, THIRD_PARTY | B | 2.5 |
| Must | Video, X post, form | A + B | 4 + 4 |
| Nice 1 | C2r ablation (critic-rejected forgeries in context) | B | 0.5 |
| Nice 2 | Proxy validity: inspector recall on held-out forgeries vs on real defects, per condition × type | B | 0.75 |
| Nice 3 | Manual-labeling baseline: B times 10 hand-drawn polygon masks | B | 0.3 |
| Nice 4 | Static DEMO_MODE deploy | A | 0.75 |
| Nice 5 | Multi-turn refine ("deeper", "more open") via `previous_response_id` | A | 1 |
| Nice 6 | Steel nut or washer shot for an industrial look | B | 0.25 |
| Nice 7 | Use Muse Code for one subsystem so it can be named in the form | Either | 0.5 |
| Nice 8 | PDF spec upload (Spark reads PDFs natively) | A | 0.5 |
| Cut | Muse Wonder planner; Glimmer or Spark Open (open-weights bonus); training any detector on forgeries; IS/LPIPS metrics; any TTS or voice; Meta glasses, Quest, robot arm, ESP32; auth, database, accounts; a public live backend; all DemoScribe and Find-and-Guide features | — | 0 |

### Hour-by-hour plan in IST

D is 07:30 IST Thu Nov 5 (9:00 PM ET Wed). If you start later than 01:30 IST, shift every row and cut nice-to-haves first. Never cut the freeze, the video block or the submission buffer, since the most common way strong teams lose is overscoping into the video time ([lablab.ai](https://lablab.ai/guide/how-to-win-an-ai-hackathon)).

| IST | Person A (forge + UI) | Person B (eval + data + rig + docs) | Exit check |
|---|---|---|---|
| **Wed 00:45–01:00** | T0: credits, key, `/v1/models`, rate-limit headers; post the two Discord questions | Create the public repo (MIT); start the hazelnut download; commit an EVAL.md stub | Key works |
| 01:00–01:30 | T1 Muse Image smoke grid | T3 SAM box IoU on 10 real defects + part mask | Latency, drift and IoU logged |
| 01:30–02:15 | T2 forge quality: 3 types × 5 × 2 styles + whole-image control, composited | T4 inspector headroom: zero-shot vs oracle on 20 images | Schemas parse |
| 02:15–03:00 | Spark critic on the T2 outputs | T5 blind rating of 10 forged vs 10 real crops | **03:00 gate: Green / Amber / Red** |
| 03:00–04:30 | Forge pipeline v1 as a CLI (stages 1–8) | `split.py` (frozen IDs + hashes, exemplar pool held out), EVAL.md pre-registration committed, `run_eval.py`, `metrics.py` | Pre-registration hash in git |
| 04:30–06:00 | Batch runner; 10 samples end to end; launch the batch (target ~30 accepted per type) | SAM IoU on all real defects; launch C0, C1 and C3 × 2 runs in the background | Both background jobs running |
| 06:00–06:30 | Commit, push, check the jobs | Commit, push, check the jobs | Clean `git status` |
| **06:30–11:30** | Sleep | Sleep | Batch and evals finish unattended |
| 11:30–12:00 | Standup; review rejection rates; **freeze the 8 C2 exemplars** (2 per type, fixed seed) | Order hazelnuts by quick commerce; find a steel nut | Exemplar IDs committed |
| 12:00–13:30 | FastAPI routes, SSE event stream, ledger endpoints | C2 (+ C2r) × 2 runs; SAM-vs-diff IoU on forgeries | C2 results JSON |
| 13:30–15:00 | React golden path + call-log drawer | 2AFC realism page; send to 5–10 raters | Raters invited |
| 15:00–16:30 | DEMO_MODE + Showcase / Run Live; hero shot via Responses | Hazelnut rig; 5 good photos; damage 10 nuts; home mini-set | Home set on disk |
| 16:30–17:30 | Live Inspect page (webcam + phone capture), SAM overlay, sanitizer | Compute all metrics; draft the results table; **apply the headline rule** | **Eval numbers in hand (D−14)** |
| 17:30–19:00 | Tunnel and phone test; error states; COCO export; home forge grid for the video | pytest suite (L0–L4 ladder + validators) | Tests green |
| 19:00–20:30 | Nap | README, model table, architecture diagram, friction log | README draft |
| 20:30–21:30 | Fix bugs from B's test run | Office hours 10–11 ET (stacking, §10.1(ix)) for 10 min, then nap until 22:30 | Answers logged |
| 21:30–22:30 | Run the home mini-set through the UI; record backup takes of the live flow | Nap | Backup footage |
| 22:30–23:30 | **Both:** clean-clone test in a fresh folder using only the README (live and DEMO_MODE); fix | (same) | **CODE FREEZE 23:30 (D−8)** |
| **Thu 23:30–01:00** | Record live takes on three feeds (screen, tripod desk shot, call log) | Write the ≤2:50 script; record narration separately | All raw footage |
| 01:00–02:30 | Re-record weak shots | Edit, add captions, upload as unlisted YouTube | **Video uploaded (D−5)** |
| 02:30–03:30 | 30–45 s X clip and quiz post; optional static deploy | Fill the form fields; check the repo and video logged out | **X post live** |
| 03:30–04:30 | **Both:** final review, submit | (same) | **Submitted (D−3)** |
| 04:30–07:30 | Buffer; no code changes | Buffer | Deadline 07:30 |

## Clear the winners' depth bar with a pre-registered four-condition eval

### What winners actually shipped, and our equivalent

Every placed Opus 4.6 and 4.7 project wrapped a **3–6-stage pipeline around a deterministic core**, gave the model **2+ distinct roles**, showed the agent working live, had a demo mode that could not fail, and offered **one checkable proof** ([Anthropic winner teardowns: Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon); [Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)). Volume varied widely: from 12 commits for Conductr's special prize to 373 for ARIA, which did not place top three. Quality of the proof mattered more than size.

| Depth signal | Winner evidence | Defect Forge implementation |
|---|---|---|
| Ablation against a human truth | MaestrIA rose from **74% to 81%** agreement with a master carpenter on 12 real photos, with the model and prompt unchanged ([CV gallery #194](https://cerebralvalley.ai/e/built-with-4-7-hackathon/hackathon/gallery/194)) | C0 → C1 → C2 → C3 on real MVTec ground truth, plus a blind human realism test |
| Provenance-checked oracle | Wrench Board rejects any scenario without `source_url`, a verbatim quote and an archive, and says "Never refresh just to 'match what the simulator now does'" ([benchmark README](https://github.com/Junkz3/wrench-board/blob/main/benchmark/README.md)) | Eval items are MVTec paths + SHA-256 only; forgeries never enter the test set; EVAL.md committed before any run |
| Deterministic core and validator | TARA's "12/12 validator passing" ([test_pipeline.py](https://github.com/Kye256/tara-transport-assessment/blob/main/video/test_pipeline.py)) | Validators V1–V8 print "8/8" per exported sample |
| Anti-fabrication | Wrench Board's sanitizer flags unverified references ([sanitize.py](https://github.com/Junkz3/wrench-board/blob/main/api/agent/sanitize.py)) | No "defect" claim without a SAM mask ID; otherwise shown amber as "uncertain" |
| Visible agent work | ARIA's Agent Inspector drawer; MedKit's "most valuable shot" of a card rendering live ([AgentInspector.tsx](https://github.com/zestones/Aria/blob/main/frontend/src/features/agents/AgentInspector.tsx)) | Stage timeline, call-log drawer (model, ms, $, cache/live), critic verdict chips, Muse Image reasoning summary |
| Demo mode | CrossBeam added "Showcase + Run Live" 45 minutes before the deadline after realizing "It looks like I faked the output" ([progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md)) | Build both buttons on day one; the LIVE badge is in the video |
| Tests | Winners ranged from 0 (Conductr) through ~40 (MedKit) and 342 (ARIA) to 1,521 (Elisa) ([Elisa](https://github.com/zoidbergclawd/elisa); [ARIA](https://github.com/zestones/Aria)) | ~60 fast tests on a recorded transport, L0 smoke → L4 golden path |
| Cost and latency | CrossBeam published "16 minutes, $8.69"; Naqsh logs ~$0.03 per page ([progress.md](https://github.com/mikeOnBreeze/cc-crossbeam/blob/main/progress.md); [Naqsh](https://github.com/lleoparden/naqsh)) | Cost and p50/p90 latency per accepted sample, from the ledger |

### The eval protocol and the numbers to produce

The protocol follows MMAD's balanced-accuracy convention and its zero-shot, one-shot and in-context ablations ([MMAD](https://arxiv.org/html/2410.09453v3)). It also follows the anomaly-generation field's precedent of holding real anomalies out of the test set ([DualAnoDiff](https://arxiv.org/html/2408.13509v3)).

The data hygiene rules come first. Forge only on **train/good** images. Move 1–2 real defects per type out of the test split into an exemplar pool, drop them from scoring, and use them only for C3. Freeze the exemplar draw with a fixed seed and log the IDs. Count the hazelnut test split after download. The notes estimate roughly 40 good and 70 defective images but have not verified it. Use the same prompt, schema, effort level (`low`) and one query image per call in every condition, and run each condition twice, because the API is not deterministic. The conditions are C0 (spec and taxonomy text only), C1 (C0 plus 2 good references, which controls for "more images"), C2 (C1 plus 8 forgeries, 2 per type: the treatment), C3 (C1 plus 8 real held-out defects: the upper bound) and an optional C2r (C1 plus 8 critic-rejected forgeries, which shows the critic does work).

| Number | Data and n | Computation | Expected (our estimate) | Claim it supports |
|---|---|---|---|---|
| Recall, specificity, balanced accuracy, F1 per condition | Full hazelnut test split minus exemplars; ~880–1,100 Spark calls in total | 95% Wilson CIs; **exact McNemar C2 vs C1** on paired predictions | Zero-shot balanced accuracy 70–90%; C2 − C1 recall −3 to +10 pts | "Forged defects teach the inspector" (if significant) |
| Per-type recall and box hit rate | Same | Box centre inside the GT mask, or IoU ≥ 0.1 with the GT box | Largest gains, if any, in type naming and localization (MMAD's +17–20 on classification) | "Names and finds the defect" |
| SAM 3.1 box-prompt IoU vs real GT masks | All real defects (~70) | Median and IQR, binned by defect area | 0.5–0.8 median for holes and cracks; below 0.4 for thin defects | "Labels to the pixel" (non-circular) |
| SAM vs diff mask IoU | All accepted forgeries | Median | — | Label consistency |
| Blind 2AFC realism | 20 real + 20 forged crops; 5–10 raters → 100–200 judgments | Accuracy vs 50% chance with a Wilson CI (about ±7 pts at n=200; raters are clustered, so say so) | — | "People can't tell" if the CI reaches ~50–60% |
| Critic value | C2r vs C2; human ratings of accepted vs rejected | Paired difference | — | "The critic matters" |
| Cost and latency per accepted sample | Ledger | Mean $; p50 and p90 per model | ~$0.01–0.03 per sample; Naqsh measured 13.6 s per edit and 3.4 s per SAM call | "Seconds and cents vs minutes of polygons" (time B's 10 manual masks) |
| Home mini-set | 10 good + 10 self-damaged own hazelnuts, same rig | Counts only ("8 of 10 flagged, 1 of 10 false alarm") | — | Real-world transfer |
| Validators | Every exported sample | N/N pass | 100% of exported samples | Deterministic integrity |
| Proxy validity (nice) | Held-out forgeries vs real defects | Per (condition × type) cell: forged recall vs real recall, MAE | Unknown, and untested anywhere | "Your forged suite predicts real-world misses" |

Sample size decides credibility. At n≈70 defectives, a recall of 0.7 has a 95% Wilson half-width of about ±10.5 points, and a McNemar split of 13 versus 2 discordant pairs gives a two-sided p≈0.007. A 15-point gain is therefore detectable on one category. API cost for the whole eval is about **$18 uncached**, or a few dollars with the cached prefix (our arithmetic from the [Pricing](https://dev.meta.ai/docs/pricing-rate-limits) page). Total project spend stays under about $30 of each participant's $150 credit.

Apply the **headline decision rule at 17:30 IST** and write it into EVAL.md before any run. If C2 beats C1 by ≥10 recall points with ≤5 points of specificity loss and McNemar p < 0.05, the headline is "recall X% → Y% on real defects it never saw." Otherwise, if the 2AFC CI reaches chance, the headline is "people can't tell our forgeries from real defects," paired with SAM IoU. Otherwise the headline is "labels to the pixel": median SAM IoU on real masks, cost per labeled sample against B's timed manual masks, and the per-type miss map. In every case, report all conditions, including a null or negative C2 next to the C3 upper bound. Honest nulls with an upper bound read as rigor. A Spark-judged realism score on its own reads as circular.

## Use the phone and webcam as a desk rig; skip all other hardware

The physical moment does more for the 25% Demo score than for Tooling, because "phone and webcam add no Tooling points by themselves" (hardware analysis, our inference). Use three capture paths, all behind one frame-source interface. The **phone's native camera** goes through the `capture="environment"` input, which takes about 15–30 minutes to build and gives the best stills ([MDN capture](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/capture)). The **USB webcam** on `localhost` provides the live inspection view; it needs no network hop and takes 15–30 minutes. A **cloudflared tunnel** carries phone `getUserMedia` only if you want a live phone preview.

The rig takes 15–30 minutes. Stand the phone on a stack of books above matte black paper, which mimics MVTec's dark background. Light the part diffusely, with a window or a lamp bounced off white or tracing paper. Tap and hold to lock focus and exposure, and keep the hazelnut centred at about 60% of the frame. Shoot the home mini-set with the same rig and distance as the live demo, so live and eval conditions match. Damage the hazelnuts to match the MVTec types: crack with pliers, hole with a nail, cut with a knife, "print" with a marker. Add one steel nut or washer shot for an industrial look. A clip-on macro lens adds no code but brings shallow depth of field and glare risks, so it stays optional; its price in India was not verified.

Skip phone-as-webcam (Windows "connected camera" or DroidCam) unless the webcam cannot focus at 20–30 cm. It adds pairing and Wi-Fi dependence, and free DroidCam is limited to standard definition ([Microsoft Support](https://support.microsoft.com/da-DK/Windows/apps/phonelink/use-your-mobile-device-s-camera); [DroidCam](https://www.dev47apps.com/)). Skip Meta glasses: the Device Access Toolkit is native-only (Kotlin or Swift) and needs firmware and app versions plus an app ID ([DAT docs](https://wearables.developer.meta.com/docs/develop/)), which means 6–10 hours for a web team. Skip Quest, SO-101 arms and ESP32 cameras entirely. For filming, run three feeds: a phone screen recording, a tripod third-person shot of the desk, and a laptop capture of the call log, edited picture-in-picture with a visible clock so the viewer reads it as live.

## Aim bonuses at Creative Build; treat Most Viral as a quiz

The only verified official text says organizers "may award additional prizes of up to $50,000 in the aggregate". Categories "may include… a community vote award, most viral project award, or other unique or notable project categories". Bonus prizes will be "announced on or about November 10, 2026," and "Additional prizes do not reduce the track prizes above" ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). No one-prize limit appears in the rules, so stacking a track place with a bonus is likely but unconfirmed. Ask at office hours. The amounts come from at least five participant copies of the Participant Guide, not public pages ([Trackdub criteria](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md); [sayso rules](https://github.com/code-sakib/sayso/blob/HEAD/docs/hackathon-rules.md)).

| Bonus (participant-guide amount) | Criteria as relayed | Our play | Effort |
|---|---|---|---|
| **Best Creative Build ($5K)** | "most original creative project using Muse Image or Muse Wonder… originality, execution, and how effectively the model is used"; "flagged during round one" ([Trackdub](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md)) | **Primary.** The winning pattern among contenders (Elsewhen, Ayna, Lumen, Naqsh) is Muse Image output **verified by SAM and code**, which is exactly our loop ([Elsewhen](https://github.com/StanislavSava/elsewhen); [Ayna](https://github.com/sabr2007/meta-global-hackathon)). Name Muse Image as load-bearing in "Use of Meta products"; show the search-grounded hero shot | 0 extra |
| **Most Viral ($20K)** | Highest likes + reposts + comments on the X post linked in the submission, through Nov 8 EOD; a shorter clip than the demo is allowed; no hashtag ([ConformScope](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md); [event notes](https://github.com/lleoparden/naqsh/issues/10)) | **Cheap lottery ticket.** Post a native 30–45 s clip as a quiz, "One of these four cracks is real. Reply with your guess", since comments count; reveal the answer Nov 6. Post by ~03:30 IST (5 PM ET); rally your network; reshare in US hours on Nov 5–8 | ≤1 h |
| Community Vote ($10K) | Public gallery, one vote per verified account; winner reportedly Nov 16 | Share the gallery link with the static demo once the gallery opens | 15 min |
| Best Agentic Use-Case ($5K) | "autonomy, effectiveness, and practical usefulness" | Tick it if the form allows. The critic writes the `revised_prompt` and the loop re-forges, but Walkdown, Ayna and DemoBot are strong agentic contenders with deeper loops | 0 |
| Open Weights ($10K) | Glimmer or Spark Open, self-hosted or partner inference, verified by the partner; eligibility details conflict across copies | **Skip**: no GPU, and the partner-verification route is unclear | — |

Most Viral rewards whoever already has an audience, so cap it at an hour. The quiz format is the one lever under your control, because it is on-brand and invites comments.

## A 2:50 video that shows live calls, then a twelve-item submission check

The binding clarifications are these. On Oct 31, organizers said the video must show "the working product with the live Meta model calls visible," with recorded runs "only a fallback" ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)). On Nov 1 they ruled that "Every model your project calls at runtime must be a Meta model… This replaces earlier guidance," and that the README must say which Meta models run where ([soulbound](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)). On Nov 2 they added "no non-Meta helper either," said Llama does not count, and said an optional API mode is fine "if Meta models do real work in it, and the demo must show that path working" ([muse-muse MESSAGING.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/MESSAGING.md)). Judges "mainly work from your 3-minute demo video and your public GitHub repo" ([HANDOFF.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/HANDOFF.md)). The video should open by stating what existed before and what was built ([ConformScope](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)). Every Opus 4.6 and 4.7 winner video ran **160–182 s**, and builders called the video "the single biggest time sink" ([PostVisit BUILD-LOG](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/BUILD-LOG.md)). Lock the UI before shooting, and record narration separately so it can be re-recorded without re-rendering.

### Storyboard

| Time | On screen | Voiceover or caption | Rubric | Rule satisfied |
|---|---|---|---|---|
| 0:00–0:08 | Grid of 24 forged defects on **your own** hazelnuts fills in, each outlined by a SAM mask. Caption: "Built Nov 4–5 for the Meta hackathon. No prior code." | "Every crack here is fake. Every label is pixel-exact." | Impact | Prior-work statement up front |
| 0:08–0:25 | A QA engineer's problem card: new line, zero defects to test an inspector on | "You can't test an inspector on defects you've never seen. Defect Forge forges them from your spec." (the aha by 0:25) | Impact | — |
| 0:25–1:15 | **LIVE badge.** Spec typed → Spark taxonomy cards → hero Muse Image edit with its reasoning summary → ECC alignment overlay ("drift 23 px corrected") → SAM mask snaps on → critic rejects one forgery and re-forges it. Call-log drawer shows `muse-image-1.0`, `sam-3.1`, `muse-spark-1.3`, ms and $ | "Three Meta models, one loop; deterministic code checks every pixel." | Demo, Tooling, Depth | Live Meta calls visible |
| 1:15–1:45 | Tripod shot: a real hazelnut photographed by phone, forged on screen; then a nut you cracked yourself under the webcam, flagged with a box and mask; a good nut passes | "Real parts on a real desk." | Demo | Physical-world proof |
| 1:45–2:15 | Eval table: C0/C1/C2/C3 with CIs on real MVTec defects it never saw; SAM IoU; 2AFC result; cost per labeled sample | The pre-registered headline, stated honestly | Depth, Impact | — |
| 2:15–2:35 | Architecture: each Meta model, its job, "runs on the Meta Model API"; OpenCV core; "no non-Meta model at runtime" | The unexpected capability: an image model as a labeled-data factory, checked by a segmenter | Tooling | README model table mirrored |
| 2:35–2:50 | COCO export opens; who uses it (QA engineers, inspection integrators); repo URL | Call to action | Impact | — |

### Submission checklist

| # | Item | Why | Owner | By (IST) |
|---|---|---|---|---|
| 1 | Claim $150 credits; key works | Credits need claiming ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)) | A | Wed 01:00 |
| 2 | Fresh public repo created Nov 4, MIT, opens in a logged-out browser | Kickoff: "Check that it opens in a logged-out browser" ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)) | B | Thu 03:30 |
| 3 | README model table with where each model runs, and a "no non-Meta model at runtime" statement | Nov 1 rule | B | Wed 23:30 |
| 4 | Prior-work statement + THIRD_PARTY.md | Prior-work guidance | B | Wed 23:30 |
| 5 | Clean-clone run from the README only, live and DEMO_MODE; macOS/Linux script present | Nov 2 judging guidance | Both | Wed 23:30 |
| 6 | No secrets, no MVTec images, no `.env` in git | Key safety; NC-SA license | B | Wed 23:30 |
| 7 | EVAL.md pre-registration commit precedes the results commits | Provenance defense | B | Wed 04:30 |
| 8 | Video ≤3:00 (target 2:50), LIVE calls visible, prior-work caption, unlisted YouTube that plays logged out | Oct 31 and kickoff rules | Both | Thu 02:30 |
| 9 | X post live with the shorter clip; its link in the form | Most Viral counts only that post ([ConformScope](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)) | A | Thu 03:30 |
| 10 | Form: Indie track; Push the Frontier; all teammates; description; repo; video; "Use of Meta products" (per-model role + numbers); "Why Meta's models matter"; "Feedback on Meta products" (friction log); bonus ticks if offered | Form fields as recorded ([naqsh notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)) | B | Thu 04:00 |
| 11 | Submit; screenshot the confirmation | No edits after the deadline ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)) | Both | **Thu 04:30** |
| 12 | Nov 5–8: reshare the X post; share the gallery link | Engagement counts through Nov 8 | Both | Nov 8 |

## Risks ranked by what can still sink the entry

| Risk | Early signal | Mitigation |
|---|---|---|
| Forgeries look fake (est. 25–35% chance) | T2/T5 at 03:00 | Outline-marker and whole-image prompts; crop at the defect centre; favor coarse types; Amber/Red gate with the 04:00 pivot |
| No in-context recall gain (est. 50–65%) | T4 oracle shows no lift at 02:15 | Pre-registered fallbacks (SAM IoU on real masks, 2AFC, per-type and box hits); report the null beside C3 |
| Muse Image drift and out-of-region changes | T1 drift metric | ECC alignment, ring colour-match, diff-only paste, V1 pixel-identity assertion |
| "You graded your own synthetic data" | Judge reaction | Test set is real MVTec images only, with hashes; human 2AFC; C2r; Spark never judges its own eval |
| Walkdown overshadows "Meta inspection" | Judges compare | Open on generation; cite Walkdown; claim zero-real-defect, spec-driven, pixel-labeled data, not inspection depth |
| §10.1(ix) Terms | Office-hours answer | Evaluation and in-context framing; no detector training; README note |
| MVTec NC-SA license | — | Download script only; video and fixtures use your own photos; VisA cashew as the license-clean swap |
| Unknown latency, 150 RPM, safety filter on "crack" | T1 | Semaphore, cache, resume; rephrase prompts; filtered images are free |
| SAM weak on thin defects | T3 IoU below 0.5 | Pad and upsample; diff-mask fallback; report IoU binned by area |
| Hidden non-Meta model sneaks in (a dependency) | `pip freeze` review | No LPIPS, CLIP, rembg or MediaPipe; README purity statement |
| Live demo fails on camera | Rehearsal | DEMO_MODE + Showcase / Run Live; backup takes recorded at 21:30; phone hotspot |
| Judge's clean clone fails on macOS/Linux | Clean-clone test | `setup.sh`, pinned versions, `pathlib`, `.gitattributes` |
| Spark nondeterminism | Run-to-run disagreement | Two runs per condition; report stability |
| Overscoping eats the video | Missed 17:30 or 23:30 checkpoints | Must-list only; hard freeze at 23:30 |
| Portal congestion at the deadline | — | Submit at 04:30 IST, three hours early ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)) |
| Fatigue errors | — | 5-hour sleep block while jobs run; staggered 90-minute naps |

The probability estimates in this table are ours, derived from the feasibility analysis's 65–75% chance of a convincing forged grid and 35–50% chance of a clean recall headline. They are not measured.

## Conclusion

The collision check changed the decision more than any technical finding. In a field of roughly 20,000 builders, DemoScribe and Find-and-Guide turned out to be ideas other teams were already executing deeply, or had already won with elsewhere. Defect Forge remains open because it uses Meta's least-used model for something other than pictures. The sharper insight is that Defect Forge's weakest claim, that forgeries teach an inspector, is not the one it needs in order to win. A generator whose labels are checked to the pixel against real ground truth, whose realism is tested blind on humans, and whose every step is replayable already clears the bar the Opus winners set. A recall lift would be a bonus headline, not the foundation.

The second implication is procedural. The plan front-loads all irreversible uncertainty into two hours of API calls tonight and pre-registers the eval before any result exists. That converts a 30-hour gamble into a 2-hour test followed by 28 hours of execution. If the 03:00 gate comes back red, the pivot is already specified. If it comes back green, the rest of the plan is engineering and discipline: freeze at 23:30, film on your own hazelnuts, and submit at 04:30.
