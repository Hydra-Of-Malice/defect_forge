# Meta Model API reusable code, competitor collision check, Muse Image/Wonder landscape, and bonus-prize verification (as of Nov 3 2026, ~19:10 UTC)

Method note: GitHub was searched with `gh search repos` (created after Oct 20 2026), `gh search code`, and `gh api` file reads at about 18:45–19:10 UTC on Nov 3. The Official Rules and the Model API Terms were read in the built-in browser, because both pages load by script. No repo was cloned or run. Counts come from repo descriptions and README text, which are self-reported, and from what GitHub search could see. Private repos and entries that do not describe themselves are invisible. "[I]" marks an inference.

## Q1. What is the fastest, most battle-tested code path to call SAM 3.1 (image and video), Muse Image edits, and Spark image/video understanding?

### Takeaway
Copy Meta's own `07_sam/01_api_basics/python/sam_api.py` (MIT) for SAM image and video, and decode with `meta_sam_parser` 0.1.0 or `@meta-sam/parser` 0.1.0 (both under the SAM License). For Muse Image, use the cookbook's Responses-API helper, or Naqsh's raw-JSON `/v1/images/edits` call, and always composite the edit back through a SAM mask. For retry, cost logging and DEMO_MODE, Naqsh (MIT), Walkdown (MIT) and winnow (no license) are the deepest working references. Gotchas repeat across all the repos:
- masks are box-local
- the SAM stream never sends `output_text.done`
- Muse Image has no mask parameter, and its edits shift and drift
- reasoning tokens use up `max_output_tokens`

### Cited Findings

#### Official Meta sample code (github.com/meta-models)
- The meta-models org has five public repos:
  - meta-model-cookbook (MIT, 208★, updated Nov 3)
  - meta-oss-cookbook (Apache-2.0)
  - muse-code-sdk (MIT)
  - meta-sam (SAM License, "NOASSERTION" on GitHub)
  - legal-agent-workshop (no license detected; updated Nov 3)
  
  — [meta-models org](https://github.com/meta-models)
- The dev.meta.ai cookbook index links only these two repos. Its SAM recipes are "SAM API basics", "Video to animated stickers" and "Multi-speaker headlocked captions". Its Muse Image recipes are "Generate, edit, and compose images", "Ground image generation with web search", "Keep an image series consistent" and "Edit image details across turns". Retry is covered by one recipe, "Error handling and retry". The page does not list the workshops. — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)
- **SAM image call (official).** The call is `AsyncOpenAI(base_url="https://api.meta.ai/v1", api_key=MODEL_API_KEY)`, then `responses.create(model="sam-3.1", stream=True, input=[{"type":"message","role":"user","content":[{"type":"input_text","text":<noun phrase>},{"type":"input_image","image_url":<data URL>}]}])`. The result is parsed with `parse_responses_stream(events, image_segmentation_format()).final_result()`.
  - Functions worth copying: `client`, `image_data_url`, `response_input`, `stream_events`, `segment_image`, `validate_result`, `summarize_result` and `write_outputs` (writes SVG masks).
  - The recipe makes one request per noun phrase.
  - In the verified run, `duck` returned 5 masks.
  
  — [sam_api.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/python/sam_api.py); [SAM basics README](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/README.md)
- **Gotcha (in Meta's own code comment):** "The API streams `response.content_part.done` but not `response.output_text.done`, which the parser uses to close a lane, so synthesize it from the content part." The helper `stream_events` does this. Also, the event generator must be closed before the response, using `aclosing(...)`. — [sam_api.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/python/sam_api.py)
- **SAM video call (official).**
  1. Upload with `files.create(file=..., purpose="user_data")` and check that the ID starts with `file-`.
  2. Call `responses.create(model="sam-3.1", stream=True, input=[... {"type":"input_video","file_id": id}])` and parse with `video_segmentation_format()`.
  3. Parser snapshots are cumulative. Call `final_result()` inside `async with parsed`.
  4. Pass `--file-id` to reuse an upload.
  
  In the verified run, "ping pong ball" returned "one stable object across all 134 video frames". — [SAM basics README](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/README.md); [sam_api.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/07_sam/01_api_basics/python/sam_api.py)
- **Non-streaming SAM pattern (official robotics demo).**
  - The client is `OpenAI(..., timeout=5, max_retries=0)`.
  - The call is `responses.create(model="sam-3.1", input=[...], metadata={"mask_encoding":"one_bit"}, store=False)`, followed by `parser = image_segmentation_format().create_parser(); parser.push(output_text); parser.finish(CompletedOutcome())`.
  - Each mask raster is pasted at `record.bounds.left/top`, and resized to the box with NEAREST if the sizes differ.
  - SAM is kept "outside the control loop"; errors and timeouts "fail open".
  
  — [sam_preview.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/full_demo/sam_preview.py); [Muse robotics README](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/README.md)
- **Parser facts.**
  - Wire grammar: `<Nf>id<|box;x1..;y1..;x2..;y2..;w=;h=[;c=]|><|mask;...data=<H>,<W>,<enc>payload|>`.
  - Payloads are base85, not base64 ("a base64 regex will not match it").
  - Confidence appears only when the request metadata has `include_confidence` set to the string `"true"`.
  - `decode_mask_to_raster`, `decode_mask_to_rle` (COCO RLE) and `decode_mask_to_svg_path` are provided. `build_object_prompt` builds box and point prompts with caller-chosen IDs.
  - An empty lane is a valid completed response with no records.
  
  — [meta-sam Python README](https://github.com/meta-models/meta-sam/blob/HEAD/python/README.md)
- Package versions: PyPI `meta-sam-parser` 0.1.0 under the SAM License. On npm: `@meta-sam/parser` 0.1.0, `@meta-sam/graphics` 0.1.13, `@meta-sam/video` 0.1.5 and `@meta-sam/react` 0.1.14. — [PyPI](https://pypi.org/project/meta-sam-parser/); [npm @meta-sam/parser](https://www.npmjs.com/package/@meta-sam/parser)
- meta-sam ships a React/Vite **API Playground** (`typescript/examples/api-playground`). Its components include `StreamLog.tsx`, `RawOutput.tsx`, `Inspector.tsx`, `ObjectPromptPanel.tsx` and `PromptOverlay.tsx`, which makes it a ready-made call-log and overlay UI for SAM. It also has 42 parser and 22 object-prompt conformance cases. — [meta-sam repo](https://github.com/meta-models/meta-sam); [meta-sam README](https://github.com/meta-models/meta-sam/blob/HEAD/README.md)
- **Muse Image (official) uses the Responses API**:
  - Call `client.responses.create(model="muse-image-1.0", input=...)`. The image comes back as base64 in `result` on the output item whose `type == "image_generation_call"`.
  - Later turns pass `previous_response_id` and only the change.
  - Reference images are `input_image` parts inside a `{"role":"user","content":[...]}` message. "A bare list of content parts is rejected with an HTTP 400."
  - With `store=False`, replay the prior `image_generation_call` item as input.
  - Example usage: 9,996 input tokens (7,936 of them cached) and 908 output tokens.
  
  — [Muse Image fundamentals](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/05_muse_image/01_image_api_fundamentals/README.md)
- The robotics demo's Muse Image restyle adds `tools=[{"type":"image_generation","output_format":"png"}]`, `store=False`, and the prompt suffix "Preserve identity and framing." — [muse_image.py](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/full_demo/muse_image.py)
- **Error handling (official).**
  - Retry 429, 5xx, timeouts and connection errors with exponential backoff plus jitter (base 0.5 s), with a cap. Never retry 400, 401 or 404.
  - `stop`, `n > 1`, `logit_bias` and `verbosity` return 400.
  - Read `x-ratelimit-remaining-*` through `with_raw_response`.
  - Branch on `type` and `status_code`, not `code`.
  
  [I] The recipe's `RETRYABLE` tuple leaves out `APIStatusError` (5xx), even though its own table says 5xx should be retried. Add it. — [09_error_handling.ipynb](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/01_api_fundamentals/09_error_handling.ipynb)
- Meta's robotics recipe says: "Muse Voice is speech-to-text; spoken replies require a separately licensed TTS engine." Its optional STT fallback is FasterWhisper, which is non-Meta and would be disallowed at runtime under the hackathon rule. — [Muse robotics README](https://github.com/meta-models/meta-model-cookbook/blob/HEAD/03_use_cases/14_muse_robotics/README.md)

#### Official workshop repos
- **Agents 101** (Oct 27, Suraj Subramanian) and **Agents 102 "Best Practices for Verifiable Agents"** (Oct 28, Yash Khare). Participant notes give the recordings as vimeo.com/1239550947 (101) and vimeo.com/1239918451 (102). They map the repo to `meta-models/legal-agent-workshop`. — [ConformScope Discord notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md); schedule in [meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md)
- **legal-agent-workshop**:
  - Session 1 builds the agent loop "in plain OpenAI Python SDK code" on a kit with one file per tool and Files API document reading. Session 2, "Make it trustworthy", adds a verification layer "which the kit runs outside the agent's control".
  - The Agent Console UI runs with `python3 ui/ui.py` at 127.0.0.1:8765.
  - Each check is one file with `run_verification(ctx, work) -> {"passed", "feedback"}`, called by tools at fixed points.
  - Refusals are capped at 3, then escalate to a person, then wait for attorney sign-off. Feedback must not leak the ground truth.
  
  — [README](https://github.com/meta-models/legal-agent-workshop/blob/HEAD/README.md); [VERIFICATION.md](https://github.com/meta-models/legal-agent-workshop/blob/HEAD/agent/VERIFICATION.md)
- The workshop client (`agent/agent_kit/client.py`) is `OpenAI(api_key=MODEL_API_KEY, base_url=MODEL_API_BASE_URL or "https://api.meta.ai/v1", max_retries=4, timeout=180)`. Its docstring says "The SDK retries rate limits (429) and overloads (503) on its own, waiting as long as the API asks." The repo has no LICENSE file; GitHub's license API returns 404. — [client.py](https://github.com/meta-models/legal-agent-workshop/blob/HEAD/agent/agent_kit/client.py)
- **Fireworks "Specialized intelligence" workshop** (Oct 30, Sinan Ozdemir). Its full title is "Building Specialized Intelligence on Fireworks: From Inference to Training with Muse Open Models". — [ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)
  - The likely repo is `fw-ai/forge-workshops` (updated Nov 3). Its workshops train Kimi K3 (research-agent-rl), Qwen 3.8 (decision-router) and GLM 5.3 Flash (skill-to-weights). The only Meta content is `workshop_skill_to_weights_glimmer.ipynb`.
  - Gotcha: "Glimmer is on serverless training but not serverless inference" on Fireworks.
  
  — [forge-workshops README](https://github.com/fw-ai/forge-workshops/blob/HEAD/README.md); [skill-to-weights README](https://github.com/fw-ai/forge-workshops/blob/HEAD/skill-to-weights/README.md)

#### Strongest participant repos (code worth copying)
- **Naqsh** ([lleoparden/naqsh](https://github.com/lleoparden/naqsh)): MIT, 273 commits, pushed Nov 3. It chains Spark, SAM 3.1 box prompts and Muse Image.
  - `backend/app/pipeline/meta.py`:
    - `_post` retries 429/500/502/503/504 with `max(Retry-After, 1.5*(attempt+1))`, using connect/read timeouts of 10 s and up to 150 s.
    - `_post_stream` parses SSE by hand.
    - `sam_segment` sends `metadata={"mask_encoding":"one_bit","include_confidence":"true"}`.
    - `image_edit` posts JSON to `/images/edits` with `{"model","prompt","images":[{"image_url":<data URL>}],"n":1,"output_format":"png","response_format":"b64_json"}` and reads `data[0].b64_json`.
    - Price constants are in the file.
  - `segment.py` builds `"<0f>" + "1<|box;...|>,2<|box;...|>"` and pastes box-local masks, falling back to the box when SAM returns nothing.
  - `demo.py` implements `DEMO_MODE=1`: it SHA-256-hashes the upload and replays a byte-identical fixture with its original receipts and stage timings, under an amber "Demo mode: replaying recorded run" badge.
  - `spend.py` writes a JSONL cost ledger. `throttle.py` allows one in-flight call per region and 6 per minute per job.
  
  — [meta.py](https://github.com/lleoparden/naqsh/blob/HEAD/backend/app/pipeline/meta.py); [segment.py](https://github.com/lleoparden/naqsh/blob/HEAD/backend/app/pipeline/segment.py); [submission-notes.md](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)
- **Naqsh API friction log** (verbatim facts from the builder):
  - A multipart `mask` on Muse Image "returns `400 unsupported_parameter`; edits are instruction-only".
  - The SAM mask raster "is the size of the object's box, not the page". A hand-built decoder fails.
  - "398 of 400 output tokens were reasoning", which produced an empty `incomplete` answer. The fix is `reasoning.effort: minimal` plus a realistic budget.
  - The SAM concept `text` "finds nothing… 200 OK… still billed".
  - A box prompt without a frame header returns "400 … geometric prompts go after a <Nf> frame header".
  - A Muse Image edit "shifts the page" by about 16 px, later 30–40 px, so per-run registration is needed.
  - Plate edits were clean in 4 of 7 runs.
  
  — [submission-notes.md](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)
- **Naqsh measured latency and cost:**

  | Call | Latency | Cost |
  | --- | --- | --- |
  | Spark vision read | 6.8 s | $0.00606 |
  | SAM, 2 masks | 3.4 s | $0.0025 |
  | Muse Image generate | 12.2 s | $0.01 |
  | Muse Image edit | 13.6 s | $0.01 |

  A 1024×1536 generate request returned a 1280×1920 image. — [submission-notes.md](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)
- **Walkdown** ([joshuakarthik2005/Walkdown](https://github.com/joshuakarthik2005/Walkdown)): MIT, 159 commits. A corrosion-walkdown agent with a live demo.
  - `backend/perception/sam.py`, `segment_video`: re-encodes the clip to `sample_fps=2.0` before upload "so only the sampled frames are billed". It bills `max(frames, 50)` at $0.20 per 1,000 frames, uploads with `with_retries`, and reads `output_text`.
  - It caches decoded masks on disk as COCO RLE, keyed by a hash of the output text.
  - Its own warning: on a synthetic clip, a video request "is accepted, billed and completes but returns no detections".
  - DECISIONS.md: hosted Spark runs through Chat Completions with `response_format` json_schema `strict: true`, `reasoning_effort="low"`, `max_tokens=4000` and `prompt_cache_key`, and "612 of ~990 input tokens were cached". On Baseten, Muse Spark Open has no structured outputs.
  - Public demo mode uses cached sample results, upload limits and a "$5 daily budget". The UI shows "every model turn and tool call… live… with timing and cost".
  
  — [sam.py](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/backend/perception/sam.py); [DECISIONS.md](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/docs/DECISIONS.md); [README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)
- **winnow / "Standard Motion"** ([kleongf/winnow](https://github.com/kleongf/winnow)): no license, 263 commits.
  - `meta/openai_transport.py`:
    - Uses `AsyncOpenAI(..., max_retries=0)`; retries are handled by its own client.
    - SAM uses `responses.stream(...).get_final_response()` because "SAM answers long tracks as a stream".
    - Meta-only fields go through `extra_body`.
    - Errors are classified as transient (429/5xx) or "file gone" (400/404 mentioning file).
    - `responses.input_tokens.count` is used for budgeting.
  - `meta/limits.py` caps in-flight and per-minute calls: Spark Contributor 150/min, Standard 3,000/min, SAM 8 in flight, Voice 16,000 per hour.
  - `meta/replay.py` provides Recording and Replay transports for CI and demo use.
  
  — [openai_transport.py](https://github.com/kleongf/winnow/blob/HEAD/backend/src/standard_motion/meta/openai_transport.py); [limits.py](https://github.com/kleongf/winnow/blob/HEAD/backend/src/standard_motion/meta/limits.py); [replay.py](https://github.com/kleongf/winnow/blob/HEAD/backend/src/standard_motion/meta/replay.py)
- winnow's plan notes three gotchas:
  - SAM text prompts "fail on the gripper and small objects at 320×180", so it tracks from a seed box.
  - "The API has no hosted code execution."
  - Voice has "no word-level timestamps".
  
  — [winnow docs/plan.md](https://github.com/kleongf/winnow/blob/HEAD/docs/plan.md)
- **Muse Image compositing lessons** from other repos:
  - Lumen (Apache-2.0, 183 commits): "Muse Image takes no mask, so the prompt names the thing and where it is in the crop". Small crops are upscaled first. The patch is composited through the SAM mask, "with the generator's colour drift measured on a ring around the region and taken out". — [mikheilkuzmidi/lumen](https://github.com/mikheilkuzmidi/lumen)
  - before-you-post: the result is "composited back only inside the mask, because Muse Image also changes pixels it was not asked to". — [WhorideChicken/before-you-post](https://github.com/WhorideChicken/before-you-post)
- **meta-hack** ([meta-ai-hackathon/meta-hack](https://github.com/meta-ai-hackathon/meta-hack)): no license, 128/128 validation assertions, Next.js. It is not reusable for vision, because it is a benefits-form voice app. Its spoken replies use **ElevenLabs** (`eleven_multilingual_v2`), which replaced Gemini `gemini-3.8-flash-tts`, with browser `speechSynthesis` as the fallback. It transcribes with `muse-voice-transcribe-1.0`. — [meta-hack README](https://github.com/meta-ai-hackathon/meta-hack/blob/main/README.md); [TTS fixtures README](https://github.com/meta-ai-hackathon/meta-hack/blob/main/specs/fixtures/tts/README.md)

### Inferences
- [I] **Fastest path for any of our three ideas, in Python:**
  1. The client: `openai` with `base_url="https://api.meta.ai/v1"` and the key passed explicitly.
  2. SAM: Meta's `stream_events`, `segment_image` and `segment_video`, plus `validate_result` and `summarize_result`, used as-is.
  3. A full-frame paste helper modelled on `sam_preview._parse_hosted_mask`.
  4. Muse Image: Naqsh's `image_edit` JSON body, or the cookbook's Responses helper when multi-turn refinement is needed.
  5. Retry: the legal-workshop client settings (`max_retries=4`, `timeout=180`), plus Naqsh's `_post` or the cookbook's jitter wrapper.
  6. DEMO_MODE: Naqsh's hash-and-replay with a visible badge.
  7. Cost: Naqsh's JSONL ledger with Walkdown's frame-billing formula.
  
  This is about 300 lines of mostly copyable code. Licenses: MIT for the cookbook, Naqsh and Walkdown; the SAM License for the parser.
- [I] Avoid copying code verbatim from winnow, meta-hack, glassbox or legal-agent-workshop, because none has a license file. Re-implement their patterns instead.
- [I] For Defect Forge, plan on registration plus mask compositing plus colour-drift correction for every Muse Image edit. Three independent repos hit the same shift, drift and out-of-mask change problems.
- [I] For DemoScribe, resample to 1–2 fps before SAM video upload to control cost. Seed-box prompts beat text prompts on small or robot-gripper objects. Also re-verify video output on real footage, because Walkdown saw empty results on synthetic clips.

### Gaps
- No standalone Agents 101 or Agents 102 repo was found. The mapping to legal-agent-workshop rests on one participant's notes. The Vimeo recordings were not watched.
- The Fireworks workshop repo is inferred to be fw-ai/forge-workshops. No Meta page links them.
- No working repo was inspected for **Spark video understanding** (`input_video` with `muse-spark-1.3`). Code search shows 198 files with both strings, but none was read. The earlier notes in meta_models_and_api.md (Video understanding docs) remain the source: MP4 only, sent as an `input_video` URL or data URL, or as a file_id.
- The legal-agent-workshop `ui/` folder appears in its README but not in the file tree that was retrieved. Its existence was not verified.

## Q2. Who else is building something like Defect Forge, DemoScribe or Find-and-Guide (collision check, Nov 3)?

### Takeaway
- **DemoScribe has a direct, deep competitor**: winnow ("Standard Motion", 263 commits) curates robot demonstrations with SAM 3.1 tracking, Spark rubrics and Voice labelling, and exports to LeRobot.
- **Find-and-Guide has 3–4 direct but shallow competitors**: spatial-sense, SightGuide, Gözüm and Halo. All are early or mock-mode, and none tracks objects across frames.
- **Defect Forge has no visible competitor** whose core is "Muse Image forges defects → SAM labels". Several SAM+Spark defect inspectors exist, and Walkdown already uses Muse Image for synthetic look-alike negatives inside a very deep inspection entry.

### Cited Findings

#### Defect Forge (synthetic defects with Muse Image, SAM labels, Spark inspects)
- **Walkdown**: MIT, 159 commits, live demo.
  - SAM 3.1 segments "rust", Spark verifies and grades it (severity 1–5), and Muse Wonder gives a second opinion.
  - Muse Image made "300 synthetic look-alike images for a false-alarm stress test; never trained on", labelled "Meta Model API terms (evaluation only, §10.1(ix))". FLUX.1-schnell on Modal made synthetic images "for training only".
  - It has an on-prem open-weights mode (SAM 3.1 weights plus Muse Spark Open on Baseten) and two Muse Glimmer distillations (QLoRA on Modal, LoRA on Fireworks).
  - Benchmarks: 97.9% recall in Cloud mode and 92.4% on-prem.
  
  — [Walkdown README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)
- **CounterForge**: MIT, 17 commits. A "visual-model reliability laboratory" that uses "controlled image changes, human-verified ground truth and repeated evaluation" to turn VLM failures into regression tests, "starting with single-image object counting". — [ottorafaelcihak/CounterForge](https://github.com/ottorafaelcihak/CounterForge)
- **Evidomo**: Apache-2.0, 182 commits. Real-estate listing packs. It "plants known problems into synthetic inputs" as an eval, and uses Muse Image for staging. It is not a physical-defect tool. — [EtkinD/evidomo](https://github.com/EtkinD/evidomo)
- **SAM+Spark defect or inspection entries without Muse Image forging:**
  - [Foxcrack/viaguard](https://github.com/Foxcrack/viaguard): roads and construction sites, 13★, the most-starred in this cluster
  - [Divyanshu-kumar14/GridSight](https://github.com/Divyanshu-kumar14/GridSight): substation footage to "Evidence-Linked Defect Reports"
  - [dptel22/sem-triage-agent](https://github.com/dptel22/sem-triage-agent): SEM wafer defects on the Carinthia-S benchmark, using sam-3.1 plus muse-spark and Spark Open
  - [thtcsec/securecoating-meta-2026](https://github.com/thtcsec/securecoating-meta-2026): battery-electrode coating, built on a disclosed pre-existing YOLO stack, 1 commit
  - [shahzaibswe/infrascan-3d](https://github.com/shahzaibswe/infrascan-3d)
  - [monigarr/asset-intelligence](https://github.com/monigarr/asset-intelligence)
  - [TriadStudios/owl](https://github.com/TriadStudios/owl): network rack
- Entries that use Muse Image to "reconstruct" or correct, not to forge training data:
  - [abdo0620/InfraSight](https://github.com/abdo0620/InfraSight): "segment, diagnose, and visually reconstruct broken infrastructure"
  - [irrepressible007/kinesight](https://github.com/irrepressible007/kinesight): assembly-line SOP compliance with "Muse Image corrective" output, 1 commit
- Dozens of non-Meta MVTec AD and NEU-DET defect repos were created after Oct 20, from courses and class projects. Examples: [GiannisPap24/factoryvision-ai](https://github.com/GiannisPap24/factoryvision-ai) and [AndyYeom/Visual_Defect_Detection](https://github.com/AndyYeom/Visual_Defect_Detection). Also [WENDGOUNDI/gemini-sam-industrial-defect-inspection](https://github.com/WENDGOUNDI/gemini-sam-industrial-defect-inspection), which uses Gemini and is not eligible.
- Search coverage: repo-description searches for "defect muse", "synthetic data muse image", "data augmentation muse" and "defect sam 3.1" returned **0** repos. Code search returned 138 files matching `"muse-image-1.0" defect` and 11 matching `"muse-image-1.0" augmentation`. In the hits that were reviewed, none was a synthetic-defect generator. — GitHub search, Nov 3 2026 ([repo search](https://github.com/search?q=%22synthetic+defect%22+created%3A%3E2026-10-20&type=repositories))
- **Terms constraint:** Model API Terms §10.1(ix) bars using "the Outputs of the Services, to train, fine-tune, distill, or otherwise improve or create any artificial intelligence or machine learning model or other product or service that competes with Meta's models or services, or systematically collect Outputs or other data to build training datasets for use in developing competing models or services, without Meta's prior written authorization". It also says "using Services or Outputs solely for evaluation, benchmarking, or quality assessment of your own systems does not constitute a prohibited use". — [Meta Model API Terms of Service](https://dev.meta.ai/legal/terms-of-service)

#### DemoScribe (robot video becomes labeled training data)
- **winnow / "Standard Motion"**: Indie track, Push the Frontier, 263 commits, pushed Nov 3 17:56 UTC.
  - Pitch: "Describe what a good robot demonstration looks like. Standard Motion watches every one and keeps only those."
  - SAM 3.1 "Tracks the gripper and objects from a seed box" as the "measurement backbone". Spark composes typed Criteria and judges "only what geometry can't". Muse Voice Transcribe supports push-to-talk labelling.
  - It outputs a "filtered dataset in the same (LeRobot) format + a Reason for every rejection", with risk-coverage and Clopper-Pearson calibration.
  - The builder is motivated by a robotics club's ping-pong policy.
  
  — [winnow docs/plan.md](https://github.com/kleongf/winnow/blob/HEAD/docs/plan.md)
- **GlassBox-SO101**: 1 commit (pushed in one go on Nov 3), no license. "Explainable failure analysis and one-click recovery for a LeRobot SO-101 arm". It uses SAM 3.1 (scene by concept), Spark (diagnosis), Muse Wonder (joint-space bypass plans), Muse Image ("Counterfactual 'what the policy should have seen' rendering") and Voice. "Every Meta call has a local fallback", and each result is tagged `meta-api`, `cache` or `local-fallback`. — [msheroubi/glassbox](https://github.com/msheroubi/glassbox)
- **auto-robo-pipeline**: 142 commits, 10★. "Autonomous robot episode curation and labeling" with LeRobot export and Label Studio review on DROID. It uses **local Qwen**, so it is a functional competitor but not a valid Meta-hackathon entry, and it may not be an entry at all [I]. — [dyl-joseph/auto-robo-pipeline](https://github.com/dyl-joseph/auto-robo-pipeline)
- **Video to robot program (adjacent, "Watch-and-Do")**:
  - [S-Raha23/Demobot](https://github.com/S-Raha23/Demobot): MIT, 35 commits, live Modal "judge mode", "5/5 real phone clips and 10/10 synthetic clips learned end to end; 202 backend + 19 frontend tests green"
  - [nikocallas/show-and-tell-robotics](https://github.com/nikocallas/show-and-tell-robotics): Muse Wonder + SAM 3.1 + MuJoCo, created Nov 3
  - [salch-cred/showonce](https://github.com/salch-cred/showonce)
  - [nickthelegend/mimic-meta](https://github.com/nickthelegend/mimic-meta)
  - [SungHyunC/video2urdf](https://github.com/SungHyunC/video2urdf): articulated object to URDF, with open weights
  - [Athmeeya2006/Physicslens](https://github.com/Athmeeya2006/Physicslens): 237 commits, video to verified physics model
- Non-Meta robot-data tools created after Oct 20:
  - [avidesai/episode-triage](https://github.com/avidesai/episode-triage): "Run on 1,427 LeRobot community arms"
  - [jlindahl11/robot-data-qa](https://github.com/jlindahl11/robot-data-qa)
  - [codeofwhite/robot-data-generation](https://github.com/codeofwhite/robot-data-generation)
  - [josefchen/robojev](https://github.com/josefchen/robojev): a dataset grader and video overlay

#### Find-and-Guide (SAM-tracked audio cues guide a blind user)
- **Spatial Sense**: 14 commits, pushed Nov 3. A web app built with SAM 3.1 and Muse Spark.
  - About every 2 s it speaks "what known object is nearest, roughly how many steps away it is, which way to turn". It also answers voice queries such as "where is the frying pan".
  - Status, in its own words: mock mode is working, while live SAM and Spark latency and cost are "not verified" and real phones are "not yet tested".
  - Its listed limits include "Tracking objects between frames, depth sensing, or floor and drop-off detection".
  
  — [Kaushal1025/spatial-sense](https://github.com/Kaushal1025/spatial-sense)
- **SightGuide**: MIT, 15 commits, last pushed Oct 29. Muse Spark plus SAM 3.1, sampled every 1.5 s, with a local tracker that assigns track IDs, "Server-side and client-side fallback TTS engines", spatial audio and 5 pre-calibrated demo scenarios. It warns of 1–3 s latency. — [fahad3235/sightguide](https://github.com/fahad3235/sightguide)
- **Gözüm**: MIT, 1 commit on Oct 28. A "Turkish-language find-and-guide agent for blind and low-vision people". Spark plans `locate`, `read_text`, `ask_user` and `whats_ahead`. SAM is "planned". It uses Muse Voice Transcribe, and Turkish speech synthesis is its output. — [gunbaz/gozum](https://github.com/gunbaz/gozum)
- **Halo**: MIT, 1 commit on Nov 2. It makes one object findable for a child with cerebral visual impairment using Spark, SAM 3.1 and Muse Image. It adapts photos and does not guide in real time. — [AsafMeizner/halo-cvi](https://github.com/AsafMeizner/halo-cvi)
- Adjacent accessibility entries:
  - [nathanlegit/NameIt](https://github.com/nathanlegit/NameIt): audio descriptions for "this" in how-to videos, using Voice + SAM 3.1 + Spark. Its description voice is ElevenLabs, a non-Meta runtime model.
  - [alekslime/Resona](https://github.com/alekslime/Resona): a voice and haptic picture tutor for blind students, 276 commits, with "stereo-panning" sound cues.

### Inferences
- [I] **DemoScribe is the most collided idea.** winnow targets the same user (robot-learning teams), the same models (SAM seed-box tracking plus Spark plus Voice) and the same output (LeRobot plus reasons). It has a 34 KB plan and 263 commits. DemoScribe would need a clearly different angle, such as dense subtask and language annotation rather than keep/reject curation, plus a head-to-head metric.
- [I] **Find-and-Guide is crowded at the pitch level but open at the depth level.** No competitor shows SAM 3.1 video tracking feeding continuous spatialized audio, verified on a real phone. Gözüm's name and framing are nearly identical ("find-and-guide agent"), so differentiate on SAM tracking plus measured guidance accuracy.
- [I] **Defect Forge is the least collided.** The risks are Walkdown overshadowing it in "inspection with Meta models", and the §10.1(ix) terms question. Training a customer's narrow defect detector arguably does not "compete with Meta's models", but that is a judgment call. Framing the forged set as an **evaluation and stress-test set**, as Walkdown does, sits inside the explicit safe harbour.

### Gaps
- GitHub sees only public repos that describe themselves. With about 20,000 accepted participants and about 625 repos self-labelled "Meta Global AI Developer Hackathon", most entries are not visible. The CV gallery and Discord were not checked.
- Whether CounterForge uses Muse Image for its "controlled mutations" was not confirmed. Only a code-search hit in its PRD was seen.

## Q3. Is the Muse Image / Muse Wonder gap still open, how are they used, and who are the strongest Creative Build and Agentic contenders?

### Takeaway
The gap has narrowed but is still open. About 7% of visible hackathon repos name Muse Image in their description and about 6% name Muse Wonder, against about 19% for SAM 3.x and about 25% for Spark. Most Muse Image uses are peripheral: product photos, illustrations, mascots. A handful use it centrally and originally (Elsewhen, Lumen, Naqsh, Ayna, before-you-post, GlassBox's counterfactuals). A Creative Build entry stands out when Muse Image output is **verified by SAM and code**, not just displayed.

### Cited Findings
- On Nov 3, GitHub reported **625** repos created after Oct 20 matching "meta global ai developer hackathon". — [GitHub search](https://github.com/search?q=%22meta+global+ai+developer+hackathon%22+created%3A%3E2026-10-20&type=repositories)
- The union of that set with the "muse image", "muse wonder" and "muse hackathon" searches is 714 unique repos. Their descriptions mention:

  | Model | Repos | Share |
  | --- | --- | --- |
  | Muse Image | 53 | 7.4% |
  | Muse Wonder | 45 | 6.3% |
  | SAM 3.x | 135 | 19% |
  | Spark | 182 | 25% |
  | Voice Transcribe | 30 | 4% |
  | Glimmer, Spark Open or "open weight" | 28 | 4% |

  These are description-only counts, so they undercount. — GitHub search API, run Nov 3 ~19:00 UTC ([muse image search](https://github.com/search?q=%22muse+image%22+created%3A%3E2026-10-20&type=repositories))
- Code-search totals across all of GitHub: `"muse-spark-1.3"` 85,632 files, `"muse-wonder-1.0"` 11,920, `"muse-image-1.0"` 10,144, `"sam-3.1"` 5,688. These totals include model catalogs and third-party tools, so they are noisy. — [GitHub code search](https://github.com/search?q=%22muse-image-1.0%22&type=code)
- **Central or original Muse Image uses (Creative Build contenders):**
  - **Elsewhen**: 34 commits, no license. "Point your phone at any place and scrub from a million years ago to a million years ahead". Muse Image "Repaints the photo for every era", and each era is painted with its already-painted neighbour as a second image for continuity. SAM masks drive a per-pixel shader blend. — [StanislavSava/elsewhen](https://github.com/StanislavSava/elsewhen)
  - **Ayna** (sabr2007): MIT, 152 commits. Muse Image "Develops 3 versions of the after photo in parallel by editing the real hero photo". SAM 3.1 conservation checks reject versions where objects vanished or changed size. The after masks become centimetre goals for robots in a MuJoCo twin, alongside SAM 3D Objects. — [sabr2007/meta-global-hackathon](https://github.com/sabr2007/meta-global-hackathon)
  - **Lumen**: 183 commits. Sentence-driven photo editing: Spark plans, SAM finds regions, Muse Image redraws, and each step is an undoable layer with drift correction. — [mikheilkuzmidi/lumen](https://github.com/mikheilkuzmidi/lumen)
  - **Naqsh**: 273 commits. Arabic comic and menu localisation with a clean-plate Muse Image edit composited through SAM masks. Evals: recall 1.00 on 8 fixtures, and the self-check caught 11/12 injected faults. — [naqsh submission-notes](https://github.com/lleoparden/naqsh/blob/HEAD/docs/submission-notes.md)
  - **before-you-post**: 42 commits. A privacy red-team that attacks a photo, removes clues with SAM masks plus Muse Image, then attacks again. Muse Image also generated "LeakBench". — [WhorideChicken/before-you-post](https://github.com/WhorideChicken/before-you-post)
  - **GlassBox**: Muse Image counterfactual "what the policy should have seen". — [msheroubi/glassbox](https://github.com/msheroubi/glassbox)
  - Others:
    - [FX-DOVE/reelforge](https://github.com/FX-DOVE/reelforge): an AI movie studio on Wonder, Spark and Image, 87 commits, with a continuity pass that redoes drifted frames
    - [Shamanthnp1/sketch-world](https://github.com/Shamanthnp1/sketch-world): drawing to a walkable 3D pop-up world, 108 commits
    - [falcon123212/matterlift](https://github.com/falcon123212/matterlift): photo to PBR material, 70 commits
    - [ong6/lives-in-motion](https://github.com/ong6/lives-in-motion): illustrated books
    - [NamiduHarshana/minutecanvas](https://github.com/NamiduHarshana/minutecanvas): a live meeting graphic recorder
    - [MuraliKrishnaGR/retrodict](https://github.com/MuraliKrishnaGR/retrodict)
    - [mizzleinetimi/paneller-open](https://github.com/mizzleinetimi/paneller-open)
    - [TusharTechs/rangrez](https://github.com/TusharTechs/rangrez): a dye lab using SAM, Wonder, Glimmer, Spark, Image and Voice
- **Peripheral Muse Image uses (the majority):** product and studio photos for sellers ([listsnap](https://github.com/bhoot-biswas/listsnap), [hubog-shoot](https://github.com/limeric29/hubog-shoot), [camtoshop](https://github.com/cabetan/camtoshop), [snapshop](https://github.com/Sachiya2000/snapshop)), try-on ([tryit-meta](https://github.com/hhlorsdemir/tryit-meta), [rewear-studio](https://github.com/gn00295120/rewear-studio)), receipts and illustrations ([agentpay](https://github.com/deaabie/agentpay)) and mascots.
- **Muse Wonder uses** are mostly as a verifier, second opinion or patch writer:
  - [igoreduardoai/repropatch](https://github.com/igoreduardoai/repropatch), [imthi16/proofmerge](https://github.com/imthi16/proofmerge), [momoikura/The-Polisher](https://github.com/momoikura/The-Polisher), [Juanpighelfi/cadverify-ai](https://github.com/Juanpighelfi/cadverify-ai)
  - A robot-program writer: [nikocallas/show-and-tell-robotics](https://github.com/nikocallas/show-and-tell-robotics)
  - A survey-program writer: [edycutjong/draftmark](https://github.com/edycutjong/draftmark), 112 commits, "Read a ship's draft from a short video… Muse Wonder 1.0 writes the survey program, which must pass the booklet self-test"
  - A rule-to-code writer: [takingbreath/whenever](https://github.com/takingbreath/whenever)
  - Walkdown measured that Wonder's second opinion "does not make grades more accurate" (73.5% agreement before, 72.7% after) and used it to surface disagreements. — [Walkdown README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)
- **Creative Build criteria** (participant copy of the Participant Guide): "most original creative project using Muse Image or Muse Wonder, judged on originality, execution, and how effectively the model is used in the final experience". It is "flagged during round one". — [Trackdub-Director criteria.md](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md)
- **Best Agentic Use-Case criteria** (same source): "strongest use of agents to complete tasks, make decisions, or coordinate multi-step workflows; judged on autonomy, effectiveness, and practical usefulness". — [Trackdub-Director criteria.md](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md)
- **Strong agentic contenders seen:**
  - Walkdown: a Spark tool-calling agent with a live trace and replanning, plus open-weights mode and evals. — [README](https://github.com/joshuakarthik2005/Walkdown/blob/HEAD/README.md)
  - Ayna: perceive, edit, verify, then robots, with a receipt. — [sabr2007/meta-global-hackathon](https://github.com/sabr2007/meta-global-hackathon)
  - DemoBot: watch a video, write a robot program, test it, attack it, fix it. — [S-Raha23/Demobot](https://github.com/S-Raha23/Demobot)
  - winnow. — [kleongf/winnow](https://github.com/kleongf/winnow/blob/HEAD/docs/plan.md)
  - ClosedLoop: falsify, repair, certify, 99 commits. — [Saqlain-mushtaq-alamin/closedloop](https://github.com/Saqlain-mushtaq-alamin/closedloop)
  - Muse Muse: sentence to tested app, with Glimmer tuning. — [Offline-Base/muse-muse](https://github.com/Offline-Base/muse-muse)

### Inferences
- [I] The strongest Creative Build contenders are **Elsewhen** (original concept plus multi-image era chaining), **Ayna** (Muse Image output becomes a physical goal, checked by SAM) and **Lumen, Naqsh and before-you-post** (Muse Image held to SAM masks with measured quality). The common pattern is Muse Image **plus a SAM/code verifier**. A "generate a picture" use will not stand out.
- [I] Defect Forge fits the winning Creative pattern if it shows that Muse Image is used in an unexpected way (counterfactual defect forging) and that the result is verified:
  - SAM recovers the forged region (IoU against the edit-difference mask).
  - Spark rejects implausible forgeries.
  - A held-out real-defect check shows the forged set catches what a baseline misses.
  
  Using reference defect images (multi-reference composition) and search-grounded edits would surface Muse Image's "agentic" capabilities, which the rubric's "unexpected capabilities" clause rewards.
- [I] The Wonder gap is more open for **Creative** use than for verification. Almost no visible entry uses Wonder creatively (reelforge's director role is one).

### Gaps
- Description counts cannot tell central use from peripheral use across all 714 repos. Only about 40 were classified by hand.
- None of the contenders' demo videos or live sites were watched.

## Q4. Bonus prizes (categories, amounts, eligibility, stacking) and new organizer clarifications (runtime rule, demo mode, TTS, open weights, submission)

### Takeaway
- **Official text** confirms only "up to $50,000 in the aggregate". It names a community vote award and a most-viral award, says the awards will be "announced on or about November 10, 2026", and says "Additional prizes do not reduce the track prizes."
- **Five categories and amounts** ($20K / $10K / $10K / $5K / $5K) are consistent across at least five participant copies of the Participant Guide, but are not in the public rules.
- **Stacking**: no rule forbids one project from winning a track prize and a bonus prize. It is also not confirmed.
- **Runtime rule** was tightened on Nov 1–2: no non-Meta model at all, including helpers, and Llama does not count.
- **TTS**: no explicit organizer ruling on browser or OS text-to-speech was found. A Meta open-source TTS model (MMS) is the safe route.

### Cited Findings
- **Official Rules (browser-read on Nov 3)**: "Bonus Prizes. The Organizers may award additional prizes of up to $50,000 in the aggregate for bonus awards recognizing standout projects or community achievements. Those categories may include, without limitation, a community vote award, most viral project award, or other unique or notable project categories designated by the Organizers. The number, categories, allocation, and value of individual bonus prizes may be determined by the Organizers before or during the judging process. Any additional prize, including a public-vote prize, will be announced on or about November 10, 2026. Additional prizes do not reduce the track prizes above." No sentence limiting a project to one prize was found. Searches for "only one", "one prize", "multiple" and "more than one" found nothing relevant. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- The Official Rules' Event Overview says: "Participants build with Meta AI products, including Muse Spark, Glimmer, SAM 3, and any other Meta AI products identified on the Event page." The judging criteria start with "Impact (30%)". — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- The CV event page and the dev.meta.ai event page list **no bonus categories**. The dev.meta.ai page says "Every project enters one track" and "Dates may be subject to change… Any change will be posted on this page". — [CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon); [dev.meta.ai event page](https://dev.meta.ai/events/global-hackathon)
- **Participant Guide copies** (consistent across sources):
  - Most Viral Project: **$20,000**
  - Best Build on Meta Open Weight Models: **$10,000**, "best project on Muse Glimmer or Muse Spark Open, self-hosted or partner inference; flagged in round one, verified by the infrastructure partner"
  - Community Vote: **$10,000**
  - Best Agentic Use-Case: **$5,000**
  - Best Creative Build: **$5,000**
  
  — [Trackdub-Director criteria.md](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md) ("Pulled from the full Participant Guide text… Oct 26"); same amounts in [meta-hack grading criteria](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/grading%20criteria.md), [asiifdev rules notes](https://github.com/asiifdev/business-ai-operation/blob/HEAD/docs/01-aturan-hackathon.md) and [kasafi-agent brief](https://github.com/bawanallahbilyaminu/kasafi-agent/blob/HEAD/docs/hackathon-brief.md); categories with $5K agentic and creative in [sayso hackathon-rules](https://github.com/code-sakib/sayso/blob/HEAD/docs/hackathon-rules.md)
- **Open-weights eligibility conflicts across participant copies:**
  - One says it requires Glimmer or Spark Open "di hardware sendiri" (on your own hardware) and does not qualify automatically through the Model API. — [asiifdev](https://github.com/asiifdev/business-ai-operation/blob/HEAD/docs/01-aturan-hackathon.md)
  - Others say "self-hosted or partner inference", with "Muse Spark Open served via a partner (Baseten/Fireworks). The partner verifies this." — [Trackdub](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md); [kasafi-agent](https://github.com/bawanallahbilyaminu/kasafi-agent/blob/HEAD/docs/hackathon-brief.md)
- **How bonuses are entered:** one participant writes "Bonus prizes ($50K total). Tick them in the submission form". Another says categories are "flagged in round one". — [sayso](https://github.com/code-sakib/sayso/blob/HEAD/docs/hackathon-rules.md); [Trackdub](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md)
- **Stacking is unresolved among participants.** One strategy doc says to ask "organizers whether one entry can receive multiple bonus prizes and whether separate nominations are required", and that "award-stacking rules must be verified". — [SMAJ award strategy](https://github.com/SMAJORG/smaj-verified-delegation/blob/HEAD/SMAJ_AI_Hackathon_Award_Strategy_2026.md)
- **Rubric weighting conflict:** one participant's copy of the guide says Stage Two's "four criteria, equally weighted". The Official Rules give 30/25/25/20. Finals are on Nov 9 at 12 PM ET, and judging runs Nov 5–8. — [Trackdub criteria.md](https://github.com/MesilimLLC/Trackdub-Director/blob/HEAD/docs/criteria.md); contradicted by the [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- **Most Viral:** "CV confirmed the X post can be a *shorter* clip than the 3-minute demo. Only engagement on that single post counts, until Nov 8 EOD." — [ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)
- **Runtime rule, Nov 1** (organizer text relayed by a participant): "Every model your project calls at runtime must be a Meta model. Meta models being a core part of the project doesn't allow other models to run alongside them. This replaces earlier guidance that non-Meta models could run alongside Meta's. Non-model libraries such as OpenCV are fine within their terms, and open-source Meta models such as SAM count however you run them. Say in your README which Meta models you use and where they run." — [ToXMon/soulbound compliance doc](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)
- **Runtime rule, Nov 2, 3:57 PM** (Discord, relayed):
  - "Llama is not part of this hackathon and does not count as a Meta model, however it is run."
  - Open Meta models count, naming "Muse Glimmer, Muse Spark Open, SAM, V-JEPA 2".
  - "no non-Meta helper either (their example was an embedding model, even beside a Meta chat model)".
  - "An optional Muse Spark API mode is fine if Meta models do real work in it, and the demo must show that path working."
  - Quantized Glimmer builds still count.
  
  — [Offline-Base/muse-muse MESSAGING.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/MESSAGING.md)
- **Nov 2 judging guidance** (relayed): "Judges mainly work from your 3-minute demo video and your public GitHub repo… Judges may also try the project themselves, using their own keys if needed, so the repo must run from its setup instructions. A hosted demo is optional." — [muse-muse HANDOFF.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/HANDOFF.md)
- **Demo mode** (Oct 31 organizer answer, unchanged since): the video must show "live Meta model calls visible". If a public deployment runs in demo mode, "make sure the repo still runs live… and the README explains how to use the demo mode". The naqsh issue's last comment is Oct 31, with no newer answers. — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- **Prior work** (CV #faqs, relayed): the repo must be "a standalone extract" with only event work, and the video should open by stating what existed before and what was built. Another participant relays that the organizers ask for "a fresh public repo created Oct 26 or later, with pre-existing material labeled". — [ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md); [muse-muse MESSAGING.md](https://github.com/Offline-Base/muse-muse/blob/HEAD/docs/MESSAGING.md)
- **TTS evidence (no definitive ruling found):**
  - One README, last committed Oct 29 (before the Nov 1 tightening), says: "Voice in/out: browser Web Speech API — organizer-confirmed allowed; it is not a model call." It gives no quote or date. — [consumer-voice README](https://github.com/salahnbilii-arch/consumer-voice/blob/HEAD/README.md)
  - Another spec says browser `speechSynthesis` read-back is something "the rules allow", with no source. — [rackwatch DESIGN.md](https://github.com/Acidni-LLC/rackwatch/blob/HEAD/DESIGN.md)
  - After the Nov 1 rule, one team rated browser Web Speech "No model call by the project, but weak voice and a judge-risky reading of the rule; do not prefer". It recommended "self-hosted Meta MMS (facebook/mms-tts-eng). Open-source Meta model, so it counts however run", noting "MMS is CC-BY-NC 4.0". It also noted "No Meta TTS is offered" on the Model API. — [soulbound compliance doc](https://github.com/ToXMon/soulbound/blob/HEAD/docs/029-meta-model-compliance.md)
  - Other entries ship local Meta MMS voice: [Velu2k03/reel-director](https://github.com/Velu2k03/reel-director) ("local MMS voice") and [nickthelegend/yadori](https://github.com/nickthelegend/yadori/blob/HEAD/AUDIT.md) ("MMS-TTS synthesis").
- **Terms for training on outputs:** the §10.1(ix) text above is verified on the live Terms page. A participant reported asking Meta in #office-hours whether training Glimmer on Spark API outputs is allowed, with "No answer yet (2026-10-29)". — [Model API Terms](https://dev.meta.ai/legal/terms-of-service); [ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)
- **Other operational notes:**
  - An API key creation bug ("Failed to create API key", then logged out) should be filed at dev.meta.ai/support.
  - #office-hours with Meta staff runs on weekdays at 10–11 ET.
  - The kickoff recording is at vimeo.com/1238909940/6d91bab1b2.
  
  — [ConformScope notes](https://github.com/Azizomezine/ConformScope/blob/HEAD/docs/hackathon-notes.md)

### Inferences
- [I] **Stacking:** the rules call bonuses "additional prizes" that "do not reduce the track prizes". They impose a one-track limit but no one-prize limit, so a track finalist can most likely also win a bonus. Treat this as likely, not confirmed. If it matters, ask in #office-hours before 9 PM ET Nov 4.
- [I] **Creative Build entry:** it appears to need nothing beyond central Muse Image or Wonder use, flagged in the form or in round one. Write the "Use of Meta products" field to name Muse Image as load-bearing. Make sure the README model table says where each Meta model runs, as the Nov 1 rule text requires.
- [I] **Find-and-Guide speech options, best first:**
  1. Non-speech spatial earcons through WebAudio. These involve no model, so there is zero rule risk.
  2. Meta MMS-TTS run locally. It is a Meta open model, but its CC-BY-NC licence is fine for a non-commercial entry, and latency is unmeasured.
  3. Browser `speechSynthesis`. This is probably fine as "not a model call", but it is unconfirmed after Nov 1, and one team calls it judge-risky.
  
  Avoid ElevenLabs or any cloud TTS: meta-hack and NameIt use it, which is now a clear violation risk.
- [I] **Defect Forge or any Glimmer fine-tune:** training on Muse Image or Spark outputs runs into §10.1(ix) only if the trained model "competes with Meta's models or services". "Evaluation, benchmarking, or quality assessment of your own systems" is explicitly allowed. Pitching forged defects as a stress-test or eval set is the conservative framing.

### Gaps
- The bonus amounts and the five category names appear only in participant copies of the gated Participant Guide and kickoff slides. They were not found on any public organizer page.
- No organizer statement explicitly addresses winning a track prize and a bonus prize, winning multiple bonuses, or browser or OS TTS. Discord is gated and was not accessed.
- The CV public gallery, needed for the Community Vote, was not re-checked on Nov 3.
- The submission form fields could not be read, because the form requires sign-in.
