# Meta 2026 Developer Models & Tools (Muse Spark, Muse Wonder, Muse Image, SAM 3.1, Meta Model API, Open Weights, Muse Code) — Technical Brief for the Meta Global AI Developer Hackathon

Research date: Nov 3 2026. Main primary sources are the dev.meta.ai docs (fetched live), the Meta and Meta Newsroom blogs, the Hugging Face model card, and the facebookresearch GitHub. Numbers are vendor-reported unless marked otherwise. Anything older than 2026 or unverified is flagged.

**Naming correction to keep in mind:** "Muse Wonder" is not a video, world, or 3D model. It is Meta's frontier text-output agentic LLM, launched Oct 12 2026. Meta's only image generator is **Muse Image**. Meta has no generative video or world model on the API.

---

## 1. Muse Spark series: variants, capabilities, benchmarks, context, speed, killer features

### Takeaway
Muse Spark is Meta Superintelligence Labs' (MSL) natively multimodal reasoning model family. It was released as Muse Spark (Apr 8 2026), 1.1 (Jul 9), 1.2, and 1.3 (Sep 2). Every API version has a 1,048,576-token context and takes text, image, video, audio, and PDF input with text output. Meta markets it for agentic orchestration (subagents), computer use, near-lossless long-context retrieval, and multimodal-to-action workflows, at $1.25/$4.25 per M tokens, or $0.10/$0.20 in "Contributor" mode. `muse-spark-1.3` is the default and recommended API model.

### Cited Findings
**Lineage and dates**
- The original Muse Spark launched Apr 8 2026 as MSL's first model, powering the Meta AI app and meta.ai, with planned rollout to WhatsApp, IG, FB, Messenger, and AI glasses — [TechCrunch](https://techcrunch.com/2026/04/08/meta-debuts-the-muse-spark-model-in-a-ground-up-overhaul-of-its-ai/)
- The April Muse Spark had Instant and Thinking modes, parallel subagents (one example ran three subagents to plan a trip), camera-based perception (e.g. ranking snacks by protein), health answers developed with physicians, and "visual coding" of websites, dashboards, and mini-games. Meta called it "small and fast by design." API access at launch was private preview only — [Meta Newsroom, Apr 2026](https://about.fb.com/news/2026/04/introducing-muse-spark-meta-superintelligence-labs/)
- Muse Spark 1.1 (Jul 9 2026) launched with the Meta Model API public preview and Muse Image. Meta calls it "a multimodal reasoning model built for agentic tasks" with a 1M-token context that it actively manages: it remembers earlier actions, retrieves from much earlier work, and compacts history — [Meta AI blog](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- Muse Spark 1.3 (Sep 2 2026) is focused on agentic and coding work. Meta's internal comparison says it uses ~20% fewer tool calls and ~25% fewer tokens than 1.2. It asks clarifying questions, confirms before consequential actions, adapts how often it sends updates, is "trained to report hitting hurdles rather than fabricating outcomes," and was trained across many harnesses — [Meta research blog](https://research.meta.ai/blog/introducing-muse-spark-1-3)
- Meta's roadmap lists "bigger models and a Muse Spark open-weights release." Muse Spark Open later shipped Oct 15 (see §6) — [Meta research blog](https://research.meta.ai/blog/introducing-muse-spark-1-3)

**API variants (exact model IDs)** — [dev.meta.ai Models](https://dev.meta.ai/docs/models)
- `muse-spark-1.3`: text, image, video, audio, PDF → text. 1,048,576 context. All reasoning levels including `max`. Works on Responses, Chat Completions, and Messages. "Recommended for new work" and the default in most examples. Caveat: "Audio understanding in Muse Spark 1.3 is not fully supported."
- `muse-spark-1.3-contributor`: same model, no `max` effort, lower price. Your content may be used to train Meta models.
- `muse-spark-1.2` and `muse-spark-1.2-contributor`: previous version. The docs **recommend 1.2 for audio input**.
- `muse-spark-1.1`: original API version, Standard mode only, not in Muse Code.
- Conflict: Artificial Analysis marks Muse Spark 1.3 as "deprecated," with Muse Wonder as its successor — [Artificial Analysis](https://artificialanalysis.ai/models/muse-spark-1-3/providers). Meta's docs still call 1.3 "recommended for new work" — [dev.meta.ai Models](https://dev.meta.ai/docs/models)
- Promptfoo says `muse-spark-1.1` is used when the model is omitted. The Meta quickstart uses `muse-spark-1.3` everywhere. **Always pass `model` explicitly** — [promptfoo](https://www.promptfoo.dev/docs/providers/meta/); [dev.meta.ai Quickstart](https://dev.meta.ai/docs/quickstart)

**Capabilities Meta emphasizes (1.1 launch)** — [Meta AI blog](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- Generalizes zero-shot to new native tools, MCP servers, and custom skills. It is trained to orchestrate multi-agent systems to cut end-to-end latency, acting as a main agent that plans and delegates to parallel subagents, or as a subagent that knows when to escalate.
- Computer use: multi-app workflows where information changes mid-task. It chooses between writing scripts, clicking directly, or batching actions per step. The demo organizes a dinner party and adjusts the order when new context arrives.
- Multimodal: visual-to-code, detailed image and video captioning, multimodal agentic workflows. **Demo: building a Facebook Marketplace listing from a smartphone video** — it extracts photos, reasons about the product, and operates a browser.
- Coding: large codebases, migrations, planning mode, goal conditioning, subagent delegation, context compaction.
- Partner quotes: Replit praised the 1M context, multimodality, "built-in search with citations, structured output, parallel tool calling," and the OpenAI-compatible interface. Cline, Box, and OpenClaw also gave quotes.

**Benchmarks (Meta-reported, 1.3 max vs GPT-5.6 Sol max vs Opus 5 max)** — [DataCamp summary of Meta's scorecard](https://www.datacamp.com/blog/muse-spark-1-3)
- DeepSWE v1.1: 75.4 / 73.0 / 74.0. SWEAtlas CodeBase QnA: 59.4 / 53.5 / 52.7. Terminal-Bench 2.1: 88.8 / 88.8 / 86.7.
- **Long context: MRCR 256K–512K = 98.5 (GPT-5.6 Sol 91.5). MRCR 512K–1M = 98.1 (GPT-5.6 Sol 73.8).** This is the clearest differentiator.
- OSWorld 2.0: 66.9 / 62.7 / 68.3. GDPVal-AA v2: 1754 / 1710 / 1824. JobBench: 64.9 / 45.4 / 65.7. DeepSearchQA: 89.4 / 93.0 / 90.4. Agentic IF: 57.8 / 60.5 / 59.1. AutomationBench: 49.4 / 46.7 / 50.3.
- Artificial Analysis (via DataCamp): 1.3 at xhigh scores Intelligence Index 61, 182 tok/s, $0.55 per task. Max scored 62 in limited preview — [DataCamp](https://www.datacamp.com/blog/muse-spark-1-3)
- DataCamp lists these weaknesses: no exposed reasoning traces, max mode held back pending safety testing, higher abstention (lower AA-Omniscience accuracy but fewer hallucinations), and narrowly trailing Opus 5 on most agent benchmarks — [DataCamp](https://www.datacamp.com/blog/muse-spark-1-3)

**Speed and latency (independent)**
- Muse Spark 1.3 (Max) on Meta's API: ~190 output tok/s, **time to first answer token 48.5 s**, median first chunk 42 s, 54.9 s end-to-end for 500 tokens. **Max effort is too slow for interactive UX** — [Artificial Analysis](https://artificialanalysis.ai/models/muse-spark-1-3/providers)
- A third-party review cites OpenRouter P50 figures of ~62 tok/s and ~1.83 s latency. The variant and effort level are unclear, and it is unverified — [aireiter review](https://aireiter.com/blog/muse-spark-1-3-api-pricing-review)

**Pricing and limits** — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- Standard (1.1, 1.2, 1.3): $1.25 input / $0.15 cached / $4.25 output per M tokens. 3,000 RPM and 4M TPM per team.
- Contributor (1.2 and 1.3): $0.10 / $0.002 / $0.20 per M. **Only 150 RPM**, 3M TPM.
- There is no long-context premium. Web search grounding costs $2.50 per 1k queries.

### Inferences
- **Most demo-able unique strengths:** (a) near-lossless retrieval over a 1M-token context at low price, so whole codebases, long videos, or document dumps fit in one call; (b) native video+audio understanding in one model, including the soundtrack; (c) built-in subagent orchestration and computer use; (d) built-in search grounding with citations.
- For a live demo, use `reasoning.effort` of `low`, `medium`, or `high` on 1.3. Avoid `max` and `xhigh` in interactive paths because they cost 40+ s to the first token. Use 1.2 when audio quality matters.
- Contributor mode is ~12x cheaper and makes the $150 credit go far. The 150 RPM cap and training-data consent make it unsuitable for any "privacy/production-ready" pitch in the Startup track.

### Gaps
- No primary-source numeric benchmarks for 1.1 or 1.2. The 1.3 numbers come from DataCamp's transcription of Meta's scorecard image.
- No published max-output-token limit per model.
- No official TTFT or throughput figures at low and medium effort.
- No exact release date found for 1.2.

---

## 2. Muse Wonder: what it is, inputs and outputs, latency

### Takeaway
Muse Wonder (`muse-wonder-1.0`, Oct 12 2026) is Meta's first frontier-class model. It is a text-output agentic LLM with the same input modalities and 1M context as Spark, priced at $4/$20 per M tokens. **It is not a video, world, or 3D generator.** Muse Wonder Full, the larger model behind the headline benchmarks, is available only in Muse Code subscriptions, not via the API.

### Cited Findings
- `muse-wonder-1.0`: text, image, video, audio, PDF → text. 1,048,576 context. Reasoning `minimal`→`max`. Tool calling, structured output, and search grounding. Works on Responses, Chat Completions, and Messages. "Preview." Standard mode only, no Contributor mode. Not available in South Korea — [dev.meta.ai Models](https://dev.meta.ai/docs/models)
- Muse Wonder Full is Muse Code only, on the Power and Maximum plans. Setting `"max"` effort on `muse-wonder-1.0` does **not** select Wonder Full — [dev.meta.ai Models](https://dev.meta.ai/docs/models); [dev.meta.ai Reasoning](https://dev.meta.ai/docs/reasoning)
- Meta positions it for "personal and professional agentic work": insurance claims, lease comprehension, personal finance, law, finance, health, and building apps and games. The headline features are **Active Memory** (carries information across conversations) and **Active Focus** (persists on hard goals, recovers from errors, checks in before important actions) — [Meta Newsroom, Oct 2026](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)
- Pricing is $4 input / $0.20 cached / $20 output per M tokens. Rate limits are 3,000 RPM and 4M TPM — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- Benchmarks, Meta's table (Wonder Full / Wonder / GPT-6 Astra / Opus 5.5):
  - Harvey LAB-AA legal: 13.1 / 10.0 / 8.6 / 4.2
  - AutomationBench-AA: 45.4 / 39.1 / 41.6 / 41.2
  - JobBench: 75.3 / 70.5 / 66.1 / 75.4
  - DeepSWE 1.1: 79.0 / 78.8 / 74.1 / 74.2
  - SWE-Marathon: 57.5 / 53.1 / 42.5 / 46.3
  - Terminal-Bench 4.0-AA: 57.1 / 52.0 / 59.1 / 59.6
  - HealthBench Pro: 62.3 / 60.5 / 65.3 / 65.6
  - Source: [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api)
- Artificial Analysis Intelligence Index: Opus 5.5 58, Wonder Full 56, Sonnet 5.5 56, GPT-6 Astra 53, Gemini 4 Argon 53, Fable 5.1 53, **Muse Wonder (API) 52**. Estimated cost per AA task: Wonder $4.52, Opus 5.5 $5.98, GPT-6 Astra $3.26 — [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api)
- Zero Data Retention mode does not support server-side conversation state, background requests, file uploads, or built-in web search — [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api)
- The Meta computer-use guide and agent-framework guides use `muse-wonder-1.0` as the recommended model — [dev.meta.ai Computer use](https://dev.meta.ai/docs/computer-use.md); [dev.meta.ai Models](https://dev.meta.ai/docs/models)
- On HN, a top comment noted the marketing-page benchmarks are for **Wonder Full**, not the API model. There was "benchmaxxing" debate, and one test found Wonder Full worse than Opus 5.5 at image→HTML (some blamed the Muse Code harness) — [HN thread](https://news.ycombinator.com/item?id=50059115); [eesel summary](https://www.eesel.ai/blog/meta-muse-wonder-review)

### Inferences
- Use Wonder for the hardest agent step in a pipeline, such as the planner, computer-use driver, or legal/financial reasoning. Use Spark 1.3 for high-volume steps. Wonder output is ~4.7x the price of Spark 1.3, so the $150 credit runs out faster.
- Wonder's clearest lead is on legal (Harvey LAB) and long-horizon SWE (SWE-Marathon). A "Build for Your World" legal, insurance, or lease agent is aligned with Meta's own marketing.

### Gaps
- No published latency or throughput for `muse-wonder-1.0`.
- No max-output-token figure.
- The research blog (research.meta.ai/blog/muse-wonder) was not fetched.

---

## 3. Muse Image: generation and editing

### Takeaway
`muse-image-1.0` (launched Jul 2026) does text→image, instruction editing, multi-turn refinement, multi-image composition, and reference-guided series consistency. Its standout feature is that it is **agentic**: before rendering, it automatically runs image search, web search, and a shell (for computed charts and infographics). It costs a flat $0.01 per image.

### Cited Findings
- Endpoints — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
  - `/v1/responses` with an `image_generation` tool, for multi-turn work.
  - `/v1/images/generations`, for single-shot text→image.
  - `/v1/images/edits`, for single-shot edits and compositions (multipart via the OpenAI SDK, or a JSON `images` array over raw HTTP).
- Parameters on the images endpoints: `n` 1–10; `size` "WxH" (**sets aspect ratio only**, max 16:1); `response_format` `b64_json` (default) or `url`; `output_format` `webp` (default), `png`, or `jpeg` — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
- Agentic grounding — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
  - The flags `enable_image_search`, `enable_web_search`, and `enable_shell` all default to true. In the OpenAI SDK, pass them through `extra_body` on the images endpoints.
  - `reasoning_strength` is `"high"` (default, multiple refinement passes) or `"low"` (single pass, faster).
  - The Responses API returns a short `reasoning` summary item.
- Multi-turn editing: pass `previous_response_id` and the new instruction (e.g. a snowy fox, then "now make it night, with the aurora overhead"). The output contains `image_generation_call` items with base64 in `result`. Select items by `type`, not by position — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
- Streaming emits only the final `image_generation.completed` event. There are **no partial images** — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
- Gotchas — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
  - Passing `web_search` as a tool returns 400 because search is built in.
  - Unknown top-level fields such as `seed` return 400.
  - `mask`, `input_fidelity`, `partial_images`, and `moderation` are rejected, so there is **no mask-based inpainting**.
  - The OpenAI SDK always sends multipart for edits.
- Pricing is $0.01 per generated image. Price does not depend on reasoning strength or tool use, and failed or safety-filtered images are not billed. Rate limit is **150 RPM** — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- Cookbooks — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)
  - "Generate, edit, and compose images"
  - "Ground image generation with web search" (current products, places, styles)
  - "Keep an image series consistent" (characters, style, settings)
  - "Edit image details across turns"
- Meta's 1.1 blog cites arena leaderboards for image generation and editing, but no numbers appear in the text — [Meta AI blog](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)

### Inferences
- The unique angle versus other image models is search- and code-grounded rendering: accurate current products and places, and data-correct charts and infographics. At 1¢ per image it is cheap enough to generate many variants in a demo.
- Do not plan features around mask inpainting or seeds. Precise local edits must be described in language, or combined with SAM 3.1 masks on the client side (for example, composite the edited image back through the SAM mask).

### Gaps
- No latency figures.
- No max resolution stated.
- No text-rendering benchmark.
- No public arena numbers in text form.

---

## 4. SAM 3.1: what's new, prompting, video, 3D, real-time, access

### Takeaway
SAM 3.1 (Mar 27 2026) is a drop-in upgrade of SAM 3 (Nov 2025). It adds **Object Multiplex**, joint multi-object tracking that is ~7x faster at 128 objects on one H100. It is available **both** as gated open weights (`facebook/sam3.1`) and as a hosted API model `sam-3.1` on the Meta Model API. The API takes a text concept prompt or box/point prompts on images or videos up to ~10 minutes and streams boxes and masks per frame. SAM 3D (Nov 2025) is separate, open-weights only, and not on the API.

### Cited Findings
**What's new (open-source release notes)** — [facebookresearch/sam3 RELEASE_SAM3p1.md](https://raw.githubusercontent.com/facebookresearch/sam3/main/RELEASE_SAM3p1.md)
- Object Multiplex is a shared-memory method that groups objects into fixed-capacity buckets processed jointly. SAM 3 processed each object independently, so cost scaled linearly with object count.
- ~7x speedup at 128 objects on a single H100 versus the Nov 2025 SAM 3 release. Other improvements: less CPU-GPU sync, better `torch.compile` fusion, batched post-processing and vision encoder.
- Accuracy is mixed:
  - Video PCS: YT-Temporal-1B cgF1 50.8→52.9; LVVIS mAP 36.3→34.3; BURST 44.5→43.3; OVIS 60.5→61.5.
  - VOS improved on 6 of 7 benchmarks (MOSEv2 J&F 60.3→62.3).
- A secondary source reports throughput for medium object counts doubling from ~16 to ~32 fps on one H100 — [awesomeagents.ai](https://awesomeagents.ai/news/meta-sam-3-1-object-multiplex/) (secondary)
- SAM 3 (Nov 2025, **older**) introduced open-vocabulary "concept" segmentation: exhaustively segment all instances of a short noun phrase in images and video — [Hugging Face facebook/sam3.1](https://huggingface.co/facebook/sam3.1); [Ultralytics](https://docs.ultralytics.com/models/sam-3)
- SAM 3D (Nov 2025, **older**) includes SAM 3D Objects (object and scene reconstruction) and SAM 3D Body (human pose and shape) — [Meta SAM 3 blog](https://ai.meta.com/blog/segment-anything-model-3/); [Roboflow](https://playground.roboflow.com/models/compare/sam-3-vs-sam-3d-objects)
- Weights on HF `facebook/sam3.1` are gated (contact-info agreement). The repo has checkpoints only, with **no HF Transformers integration**. Ultralytics uses `sam3.1_multiplex.pt` — [HF](https://huggingface.co/facebook/sam3.1); [Ultralytics](https://docs.ultralytics.com/models/sam-3)

**Hosted API (`sam-3.1`)** — [dev.meta.ai SAM overview](https://dev.meta.ai/docs/sam/overview.md); [Segmenting](https://dev.meta.ai/docs/sam/segmenting.md)
- Called through `POST /v1/responses` with the same key. Use `input_text` (concept) plus `input_image` or `input_video` (URL, data URL, or `file_id`).
- **Concept prompt:** one short noun phrase per request (e.g. "yellow school bus"). Commands, questions, lists, negation, OR, and spatial phrasing are unreliable. To segment several concepts, send several requests.
- **Box and point prompts:** `<|box;...|>` and positive/negative `<|point;...|>` per object id, **up to 16 objects**. Coordinates are in media pixels after EXIF rotation, and a mismatched aspect ratio returns 400.
- Video
  - MP4 or MOV with H.264, H.265, or MPEG-4. **No VP9 or WebM.**
  - **Up to 15,000 frames (~10 min).** Tracks up to 16 objects per frame. Prompts can be placed on any frame with `<Nf>` markers.
  - `metadata.propagation_direction` is `both` (default), `forward`, or `backward`.
  - Upload clips with `POST /v1/files` (`purpose: user_data`). Export with `-movflags +faststart` to avoid a remux.
- Output
  - Streams in `output_text` as a special-token grammar: one line per image or frame, with a frame marker `<0f>`, an object ordinal, a box in source pixels, and a mask.
  - `mask_encoding` is `"lossless"` (default) or `"one_bit"` (several times smaller). Set `include_confidence: "true"` (a string) for 0–1 scores.
  - Zero matches return an empty `output_text`, not an error.
  - Frame order is not guaranteed for box and point prompts, so key results by frame marker. Results can vary slightly run to run.
- Parsers: `@meta-sam/parser` (npm) and `meta_sam_parser` (pip). The npm package exposes `parseImageStream`, `recordsOfKind`, and `decodeMaskToRaster` (returns a 0/1 Uint8Array of length W*H). Optional graphics, video, and React packages render overlays and segmented video — [dev.meta.ai SDKs](https://dev.meta.ai/docs/sdks); [SAM overview](https://dev.meta.ai/docs/sam/overview.md)
- Pricing is **$2.50 per 1,000 images; $0.20 per 1,000 video frames**, with a 50-frame minimum per video request. Rate limit is 3,000 RPM — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- SAM cookbooks — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)
  - "SAM API basics"
  - "Video to animated stickers": track a pet, remove the background, export transparent stickers.
  - "Multi-speaker headlocked captions": match diarized voices to tracked people, add speech bubbles, download the captioned video. Combines SAM with Voice Transcribe.
- A third-party host lists SAM 3.1 at ~0.4 s per frame — [Reka infer listing](https://infer.reka.ai/models/sam-3-1) (third party, unverified)

### Inferences
- The hosted API removes all GPU setup. Ten minutes of 30 fps video (18k frames) exceeds the 15k cap, so downsample to ~24 fps or less, or trim. 15k frames costs about $3.
- The killer combinations are Muse Spark for reasoning and naming concepts, SAM 3.1 for pixel-exact tracking, and Muse Image for regeneration. Spark's own grounding (0–1000 boxes and points, see §5) gives coarse location; SAM gives exact masks.
- For robotics or physical-world "Push the Frontier" work: run open-weights SAM 3.1 locally for real-time multi-object tracking and keep the API for batch work. The API is streaming and request-based, not built for live low-latency camera feeds.

### Gaps
- No official API latency, fps, or max resolution.
- SAM 3D is not on the Model API (only `sam-3.1` is listed); verify license and weights separately.
- The SAM 3.1 open-weights license was not stated in the release notes.

---

## 5. Meta Model API: endpoints, compatibility, SDKs, auth, features, limits, credits

### Takeaway
The Meta Model API (api.meta.ai, docs at dev.meta.ai/docs) has been GA since Connect 2026. Base URL `https://api.meta.ai/v1`, bearer auth with `MODEL_API_KEY`. It is **drop-in compatible with the OpenAI SDK (Responses and Chat Completions) and the Anthropic SDK (Messages)**. It supports streaming, function calling (parallel by default), schema-constrained JSON, vision, video, audio, PDF, a Files API, built-in web search grounding, tool search, a `computer` tool, background responses, and prompt caching. The biggest gotchas are `tool_choice` accepting only "auto", reasoning tokens consuming the output budget, and passing keys explicitly. Hackathon participants get $150 in Model API credits.

### Cited Findings
**Base, auth, endpoints** — [dev.meta.ai API reference](https://dev.meta.ai/docs/api-reference)
- Base URL `https://api.meta.ai/v1`. Header `Authorization: Bearer $MODEL_API_KEY`. Keys are created in the Model API dashboard under API keys → Create API key — [Quickstart](https://dev.meta.ai/docs/quickstart)
- `POST /v1/responses` is "server-managed, agentic generation with reasoning replay" and is OpenAI-compatible. It also supports retrieve, delete, cancel, and `POST /v1/responses/input_tokens` (count tokens).
- `POST /v1/chat/completions` is OpenAI-compatible. `POST /v1/messages` is Anthropic-compatible (plus count-tokens).
- `/v1/files` (upload, list, retrieve, content, delete), `/v1/models`, and `GET /v1/status` (unauthenticated).
- Images: `/v1/images/generations` and `/v1/images/edits`. Voice: `POST /v1/asr/transcribe` and `wss://api.meta.ai/v1/asr/realtime` — [Models](https://dev.meta.ai/docs/models)
- Errors use the OpenAI envelope `{error:{message,type,param,code}}`.
- The legacy Llama API (api.llama.com) was **retired Jul 6 2026** — [promptfoo](https://www.promptfoo.dev/docs/providers/meta/)

**SDKs and compatibility** — [dev.meta.ai SDKs](https://dev.meta.ai/docs/sdks); [Quickstart](https://dev.meta.ai/docs/quickstart)
- Meta has no proprietary SDK; you use `pip install openai` (Py 3.9+) or `npm install openai` (Node 18+). "Full support for Responses and Chat Completions, including streaming, tool calling, structured output, vision, video and audio, and file uploads."
- Anthropic SDK: base URL `https://api.meta.ai` (**no /v1**). Pass the key as `auth_token`. The first content block is `redacted_thinking`, so filter for `text` blocks. Claude Code and other Anthropic-format harnesses can point at this endpoint.
- LiteLLM: `model="openai/muse-spark-1.3"`. LangChain, LlamaIndex, and the Vercel AI SDK work through a custom OpenAI base URL.
- Gotcha: the SDKs do not read `MODEL_API_KEY` automatically. Pass `api_key=` or set `OPENAI_API_KEY`.
- Third-party gateways also list Meta models: OpenRouter, Vercel AI Gateway (`meta/muse-spark-open`), and Mastra and promptfoo providers — [Vercel AI Gateway](https://vercel.com/ai-gateway/models/muse-spark-open); [mastra](https://mastra.ai/models/providers/meta.md)

**Quickstart pattern (adapted from official docs)** — [Quickstart](https://dev.meta.ai/docs/quickstart)
```python
from openai import OpenAI; import os
client = OpenAI(base_url="https://api.meta.ai/v1", api_key=os.environ["MODEL_API_KEY"])
r = client.responses.create(model="muse-spark-1.3", input="...", reasoning={"effort": "low"})
print(r.output_text)
```
TypeScript is identical: `new OpenAI({ baseURL: 'https://api.meta.ai/v1', apiKey })`. Install Muse Code with `curl -fsSL https://dev.meta.ai/install.sh | sh` (macOS/Linux) or `irm https://dev.meta.ai/install.ps1 | iex` (Windows).

**Tool and function calling** — [dev.meta.ai Tool calling](https://dev.meta.ai/docs/tool-calling)
- Responses tools are flat `{type:"function", name, description, parameters}`. The output contains `function_call` items, and you return a `function_call_output` with `call_id` plus `previous_response_id`, so history is not rebuilt.
- Chat Completions uses the nested `function` format with `tool_calls` and `tool` messages.
- `parallel_tool_calls` defaults to true.
- **`tool_choice` only supports "auto". `none`, `required`, and named tools return HTTP 400**, so you cannot force a tool call and your code must handle plain-text replies.
- Built-in tools are `web_search` (search grounding) and `tool_search`. Use `defer_loading: true` for large tool sets. `max_tool_calls` caps built-in calls only.
- `strict` defaults to false. Responses-only `custom` (freeform-text) tools exist.
- Names must match `^[a-zA-Z0-9_.-]+$` with at most one dot. `call_id` is 1–64 characters. Legacy `functions` and `function_call` are deprecated.
- Streaming: on Responses, use `response.function_call_arguments.delta`/`.done`. On Chat, accumulate `tool_calls` deltas by index.

**Structured output** — [dev.meta.ai Structured output](https://dev.meta.ai/docs/structured-output)
- Chat Completions uses `response_format: {type:"json_schema", json_schema:{name, schema, strict}}`. Responses uses `text.format`. Each parameter only works on its own endpoint.
- Decoding is constrained (output is guaranteed to conform). `strict:true` adds server-side schema validation: object root, no allOf/oneOf, `additionalProperties:false`, all keys required.
- Limits: nesting depth 10, 5,000 properties, 1,000 enum values. **Recursive schemas return 400.**
- Pydantic works through `client.beta.chat.completions.parse()`.

**Reasoning** — [dev.meta.ai Reasoning](https://dev.meta.ai/docs/reasoning)
- Chat uses `reasoning_effort`; Responses uses `reasoning.effort`. Levels: `minimal|low|medium|high|xhigh|max`. **`none` returns 400.** `max` works only on wonder-1.0 and spark-1.3 (not contributor).
- Reasoning tokens count toward `max_output_tokens` and are billed as output. **Set output limits generously** (the video docs say ≥4000) or visible output may be truncated or empty.
- Raw reasoning is never returned. Optional summaries are available on Responses (`reasoning.summary: auto|concise|detailed`, not guaranteed). Stateless replay uses `include:["reasoning.encrypted_content"]`. Chat Completions does not carry reasoning across turns.
- `logprobs` returns 400.

**Multimodal input**
- Images: up to 50 per request, 50 MB inline or 1 GiB via the Files API. JPEG, PNG, GIF, WebP, ICO. A ~1280px image costs ~1,300–1,500 tokens. Images are ignored outside the `user` role — [Image understanding](https://dev.meta.ai/docs/image-understanding.md)
- **Grounding:** the model outputs points, boxes, and counts on a normalized 0–1000 grid. Combine with structured output, and clamp values (1001 can occur). Dividing by 10 gives CSS percentages for HTML overlays — [Image understanding](https://dev.meta.ai/docs/image-understanding.md)
- Video: **MP4 only**. Send as an `input_video` URL or data URL, an `input_file` file_id, or a Chat `video_url` part. Embedded audio is understood, so one call returns both a visual description and a transcript — [Video understanding](https://dev.meta.ai/docs/video-understanding.md)
- Audio: MP3 or WAV through `input_audio` or a file_id. Use `muse-spark-1.2` for audio. For long audio, stream and lower effort to avoid idle-timeout disconnects — [Video understanding](https://dev.meta.ai/docs/video-understanding.md)
- PDF: text from the first 100 pages and images from the first 50, which count toward the 50-image cap — [File handling](https://dev.meta.ai/docs/file-handling.md)
- Files: 1 GiB per upload, 100 GiB team storage. **Files do not expire by default**; set `expires_after` (1 h–30 d). Purposes are `user_data` and `batch` — [File handling](https://dev.meta.ai/docs/file-handling.md)

**Computer use** — [dev.meta.ai Computer use](https://dev.meta.ai/docs/computer-use.md)
- Responses-only `{"type":"computer"}` tool. Actions: click, double_click, drag, keypress, move, scroll, type, screenshot, wait. Coordinates are pixels in your last screenshot (≤25 MiB PNG or JPEG data URL).
- **Meta hosts no VM**; you drive Playwright, Puppeteer, or pyautogui yourself. `pending_safety_checks` must be echoed in `acknowledged_safety_checks`.
- Stateless replay holds up to 29 call/output pairs. `truncation:"auto"` (trims old screenshots) only works where enabled for your account, otherwise 400.
- The recommended model is `muse-wonder-1.0`; `muse-spark-1.3` is cheaper on long runs.

**Other platform features**
- Voice: `muse-voice-transcribe-1.0`, $0.18 per audio hour, 25 languages, realtime WebSocket with speaker-attributed turns. No TTS, word timestamps, or emotion detection — [Models](https://dev.meta.ai/docs/models); [Pricing](https://dev.meta.ai/docs/pricing-rate-limits); [Cookbook](https://dev.meta.ai/docs/cookbook.md)
- Background responses: limited to 600 new submissions per minute per team — [Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- Prompt caching: a cookbook recipe exists, and cached input costs $0.15 on Spark versus $1.25 uncached — [Cookbook](https://dev.meta.ai/docs/cookbook.md)

**Rate limits** — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)
- Limits are per **team, not per key**, and per model:
  - Spark Standard and Wonder: 3,000 RPM and 4M TPM.
  - Contributor: 150 RPM and 3M TPM.
  - `muse-image-1.0`: 150 RPM.
  - `sam-3.1`: 3,000 RPM.
  - Voice: 256 concurrent streams and 16k streams per hour.
- Headers: `x-ratelimit-{limit,remaining}-{tokens,requests}`. On 429, use exponential backoff with jitter starting at ~500 ms and honor `Retry-After`.

**Hackathon credits and judging (practical)**
- Meta posted: "Each selected participant gets $150 in Meta Model API credits" — [Meta for Developers on X](https://x.com/MetaforDevs/status/2110045152601633114)
- Partner credits conflict:
  - The brief says Baseten, Modal, and Fireworks offer $100 each.
  - A secondary search summary said Baseten and Modal offer $100 and **Fireworks $25**, with no primary source — [resourify / aggregator results](https://resourify.com/resources/meta-api)
  - The official hackathon page does not list partner credit amounts — [dev.meta.ai hackathon page](https://dev.meta.ai/events/global-hackathon)
- Official track criteria: Indie is judged on "creativity, technical ambition, and whether the project works." Startup is judged on "technical execution and whether it holds up in production." Allowed: Muse Spark series, Muse Image, and SAM 3.1 via the Model API, plus open-weights models and Muse Code — [dev.meta.ai hackathon page](https://dev.meta.ai/events/global-hackathon)
- Secondary report of final judging weights: **Impact 30%, Use of Meta AI Tooling 25%, Demo 25%, Technical Depth & Execution 20%**. Judging Nov 4–8, finals Nov 9. Prize split: Indie 1st $150k; Startup 1st $250k — [AImagazine](https://aimagazine.blog/meta-opens-its-1m-global-ai-developer-hackathon-20000-seats-150-api-credits-each-and-applications-close-october-25/) (secondary; the official rules were not fetched)
- The official page also lists Muse Wonder, Muse Glimmer, Muse Voice Transcribe, and Meta AI Connectors, but does not say they are part of the hackathon. AImagazine says Muse Wonder is listed on the hackathon page — [dev.meta.ai hackathon page](https://dev.meta.ai/events/global-hackathon); [AImagazine](https://aimagazine.blog/meta-opens-its-1m-global-ai-developer-hackathon-20000-seats-150-api-credits-each-and-applications-close-october-25/)

### Inferences
- **Fastest path:** use the OpenAI SDK with the Responses API, `muse-spark-1.3`, `reasoning.effort: "low"` or `"medium"`, `stream: true`, and `text.format` JSON schema. This should take minutes to wire up.
- If "Use of Meta AI Tooling" really carries 25%, a project that chains **several** Meta surfaces (Spark/Wonder + SAM 3.1 + Muse Image + Voice + Muse Code for the build) should score better than a single-model wrapper.
- Budget: $150 buys ~120M Spark Standard input tokens, ~15k Muse Image generations, ~750k SAM video frames, or ~7.5M Wonder output tokens. Credits are not the bottleneck for a demo; RPM on Image (150) and Contributor (150) might be under load.
- Because `tool_choice` can't be forced, use structured output (`text.format`) for deterministic extraction steps instead of "required" tool calls.

### Gaps
- Official Rules and the submission requirements (video length, repo) were not fetched.
- Partner credit amounts are not confirmed from a primary source.
- No documented free tier beyond the credits.
- No documented max output tokens.
- Whether hackathon credits apply to Contributor mode, Image, and SAM is unconfirmed.

---

## 6. Meta open-weights models (late 2026) and serving via Baseten, Modal, Fireworks

### Takeaway
The current Meta open-weights lineup is **Muse Spark Open** (816B MoE, 42B active, 1M context, text+image+video+audio in, released Oct 15 2026, Muse Model License) and **Muse Glimmer** (30B dense, text+image in, 128K context, Apache 2.0, released Aug 10 2026), plus SAM 3.1 and SAM 3D weights. Llama 4 (Apr 2025) is now legacy. Spark Open is served per-token by Baseten, Fireworks, Modal, Together, Groq, and others at ~$1.25/$4.25 per M. Self-hosting needs ≥700 GB of GPU memory, which is not realistic in a 1-day hackathon.

### Cited Findings
**Muse Spark Open** — [HF model card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B); [VentureBeat](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops)
- HF ID `meta-models/Muse-Spark-Open-816B-A42B`, released Oct 15 2026. Gated: the form asks for legal name, DOB, and organization, and cannot be edited after submission.
- Architecture: 816B total and 42B active, 256 experts with top-8 routing. A 1.8B Perception Encoder handles images, video, and audio input. Text output only. 1M context.
- Reasoning effort: `low|medium|high|xhigh`. **The default is xhigh**, and other values return an error. Recommended sampling: temperature 1.0, top_p 1.0.
- Memory: NVFP4 needs ≥700 GB VRAM; BF16 needs 2 TB. Meta's demo ran on two M5 Ultra Mac Studios with MLX.
- Serving: SGLang (recommended), vLLM, TensorRT-LLM, Transformers, llama.cpp, Unsloth GGUF. Both vLLM and SGLang expose an OpenAI `/v1/chat/completions` endpoint.
- Video gotcha: very short or ~100px clips can return "can't view." Use ≥448px on the short side.
- Benchmarks (Meta, xhigh):
  - AA Intelligence Index 39 (GLM 5.3 45, Kimi K3 44, Qwen3.8 40)
  - MCP-Atlas 89.2; JobBench 61.8; OSWorld Verified 80.4; Toolathlon 72.8
  - GPQA Diamond 89.0; Terminal-Bench 2.1 76.4; DeepSWE 1.1 60
  - VideoMMEv2 61.5; IntPhys2 68.3; SimpleVQA 73.6
  - Several Chinese open models score higher on the AA index.
- License (Muse Model License): commercial use is OK, but you must show **"Built with Muse Spark Open"** attribution. Model-as-a-service providers over $20M revenue need a separate agreement, and derivatives include distillations.
- Meta's launch post lists hosted API providers Baseten, Fireworks AI, Groq, Modal, Nebius, OpenRouter, and Together AI. Weights are on SageMaker, Vertex Model Garden, HF, and Microsoft Foundry — [AI at Meta on X](https://x.com/AIatMeta/status/2110779758334386491)
- Groq requires org approval and caps context at 131K. Fireworks offers 1,048,576 context. Together charges $1.25 / $0.15 cached / $4.25 — [VentureBeat](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops)
- Wikipedia's Muse Spark article gives a July 2026 release date, which contradicts the April launch — [Wikipedia MSL](https://en.wikipedia.org/wiki/Meta_Superintelligence_Labs)

**Provider specifics**
- **Fireworks:** serverless ID `accounts/fireworks/models/muse-spark-open`, base `https://api.fireworks.ai/inference/v1`, env var `FIREWORKS_API_KEY`, $1.25/$4.25. Do not use the bare `muse-spark-open` slug. Fireworks also lists Muse Glimmer 30B — [LLMReference](https://www.llmreference.com/provider/fireworks-ai/muse-spark-open) (third party); [Fireworks model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b)
- **Baseten:** Model APIs (per-token) list Muse Spark Open at $1.25 / $0.15 cached / $4.25, added in Oct 2026. An aggregator gives the ID as `baseten/meta-models/muse-spark-open` (verify in the Baseten dashboard) — [UsagePricing](https://www.usagepricing.com/blueprint/activity/baseten-2026-10-23-beam-muse-spark-open); [Maxim](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/baseten/model/muse-spark-open)
- **Modal:** Meta names Modal as an API platform for Spark Open, but no Modal-specific Muse recipe was found. Modal's generic vLLM guide (Qwen3-8B on an H100) is a template. Spark Open would need a multi-GPU node (e.g. 4x GB200/GB300 per NVIDIA Dynamo, or ≥700 GB NVFP4). **Modal is realistic for Muse Glimmer (30B) or SAM 3.1 weights**, not for self-hosting Spark Open — [Modal vLLM guide](https://modal.com/blog/how-to-deploy-vllm); [NVIDIA Dynamo recipe](https://docs.nvidia.com/dynamo/dev/recipes/Muse-Spark-Open.md); [SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/Meta/MuseSparkOpen.md)

**Muse Glimmer**
- 30B dense decoder with a vision encoder, distilled from Muse Spark. Text+image in, text out. 128K default context. Apache 2.0. Self-host only; it is not returned by `/v1/models` — [dev.meta.ai Muse Glimmer](https://dev.meta.ai/docs/muse-glimmer/); [Models](https://dev.meta.ai/docs/models)
- Runtimes: vLLM, SGLang, llama.cpp, Ollama. Partners include LM Studio, Unsloth, Fireworks, Together, and OpenRouter. Runs on a single GPU or Mac Mini. Weights are ~60 GB in BF16 and ~18 GB at 4-bit — [Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/); [AA article](https://artificialanalysis.ai/articles/muse-glimmer)
- Together prices it at $0.35/$1.50 per M — [VentureBeat](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops)
- Its AA Intelligence Index score conflicts between sources. The AA article says 35, 21 above Llama 4 Maverick's 14 — [AA article](https://artificialanalysis.ai/articles/muse-glimmer). The AA tweet at the Spark Open launch says Glimmer (high) scores 17, 22 below Spark Open — [Artificial Analysis on X](https://x.com/ArtificialAnlys/status/2110893784422908225). The index version likely changed.
- The Register called it underwhelming: "doesn't exactly move the needle much" — [The Register](https://www.theregister.com/a/5285666)
- Cookbook: **"Local agent that asks first"** runs Glimmer locally and sends text to Muse Spark only after user approval, a hybrid local/cloud privacy pattern — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)

**Llama (legacy)**
- Glimmer is described as Meta's first open-weight model since Llama 4 — [mer.vin](https://mer.vin/linkedin/muse-glimmer-30b-is-metas-first-open-weight-model-since-llama-4-linkedin/). The hackathon page still links github.com/meta-llama/llama — [hackathon page](https://dev.meta.ai/events/global-hackathon). **Llama 4 Scout and Maverick (Apr 2025) are older facts** and no Llama 4.x successor was found.

### Inferences
- For a 1-day build, call Spark Open through a provider (Fireworks, Baseten, or Together) using the OpenAI SDK with a changed base_url and model ID. It is the same price as hosted Spark 1.3 and burns partner credits, not Meta credits.
- The open-weights story that fits a hackathon demo is **Glimmer on-device/local** (privacy, offline, robotics or edge), escalating to Spark or Wonder in the cloud, as in Meta's own cookbook. Glimmer on Modal (one H100 or A100-80GB) or locally via Ollama or llama.cpp is feasible in hours.
- Fine-tuning Spark Open (TorchTitan SFT/RL cookbooks) is not feasible in 1–1.5 days.

### Gaps
- No official Baseten or Modal docs pages for Muse models were retrieved.
- Glimmer's HF repo ID and tool-call format are unconfirmed (one aggregator cites `meta-models/Muse-Glimmer-30B`).
- No official Glimmer benchmarks.
- Partner throughput and latency for Spark Open are unknown.

---

## 7. Muse Code: what it is and how to access it

### Takeaway
Muse Code is Meta's terminal and CI coding agent (comparable to Claude Code or Codex CLI). It is GA on macOS, Linux, and Windows, multi-agent by default (parallel workers in isolated git worktrees), has headless `muse exec`, a TypeScript SDK, and skills, hooks, MCP, and subagents. You can bill it with a Model API key (pay-as-you-go, so it should draw on hackathon credits) or a subscription. Wonder Full is only available in Muse Code Power and Maximum plans.

### Cited Findings
- Install: `curl -fsSL https://dev.meta.ai/install.sh | sh` (macOS/Linux) or `irm https://dev.meta.ai/install.ps1 | iex` (Windows). Check with `muse --version`, then run `muse` in the project. It asks you to trust the workspace (loads skills, rules, hooks) and sign in. The docs state the default model is `muse-spark-1.2` — [dev.meta.ai Muse Code](https://dev.meta.ai/docs/muse-code.md)
- Auth: browser sign-in or an API key. Use `/login` interactively and `META_API_KEY` for CI and non-interactive runs (note this differs from the API's `MODEL_API_KEY`) — [dev.meta.ai Muse Code](https://dev.meta.ai/docs/muse-code.md)
- Modes: interactive TUI with slash commands and approvals; headless `muse exec "<prompt>"`; `muse serve` (versioned session protocol); `muse schema`. TS SDK: `npm install @muse-code/sdk`, docs at meta-models.github.io/muse-code-sdk — [dev.meta.ai Muse Code](https://dev.meta.ai/docs/muse-code.md)
- Features: workflows (parallel and staged multi-agent work, not on every build), session messaging between live sessions (not on Windows), rewind/branching, an OS sandbox with approval modes and staged shell review. On Windows, agent commands run in PowerShell, the sandbox may prompt UAC once, and voice input is unavailable — [dev.meta.ai Muse Code](https://dev.meta.ai/docs/muse-code.md)
- Connect 2026: "Out of beta and available on Windows. Multi-agent by default, with parallel workers that write and test code in isolated workspaces" — [Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)
- Bundled skills: `/plan`, `/grilling`, `/grill-with-docs`, `/taste`. Cookbooks cover subagent fanout (one git worktree each), goal tracking with acceptance criteria, loop and cron scheduling, side chats, staged approvals, immutable guardrails, deterministic replay in CI, and session audit and resume — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)
- Plans: Everyday (10–50 prompts per 5 h), High (5x), Power (20x, adds Wonder Full), Maximum (80x). Prices are not on the page. Third parties report Power at $50/mo and Maximum at $200/mo. **Contributor mode defaults ON for subscriptions** (content may train Meta models); toggle it with `/settings` or `--contributor-mode off`. Pay-as-you-go bills per token through a Model API key — [dev.meta.ai Subscriptions](https://dev.meta.ai/docs/muse-code/subscriptions.md); [VentureBeat](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api)
- The Muse Code API key that onboarding creates is covered by the subscription and is for Muse Code only. Any other keys bill pay-as-you-go — [dev.meta.ai Subscriptions](https://dev.meta.ai/docs/muse-code/subscriptions.md)
- Third-party review (older 1.2 version): "fast beta terminal agent." One test failed to complete a provider integration — [joaoqueiros review](https://www.ai.joaoqueiros.com/blog/muse-code-spark-1-2-pricing-contributor-data-reliability-review)

### Inferences
- Using Muse Code to build the project, and showing it in the demo or README, likely counts toward "Use of Meta AI Tooling." It also enables an "agent that ships agents" narrative.
- Muse Code's headless `muse exec` and TS SDK can be embedded **inside** a product (e.g. a GitHub bot or an auto-fixer), which is the pattern in Meta's "GitHub agent" cookbook.

### Gaps
- No primary-source subscription prices.
- Whether hackathon credits cover Muse Code pay-as-you-go is unconfirmed, though it should, since it is Model API billing.
- Default model may now be 1.3 or Wonder; the docs say 1.2.

---

## 8. Official cookbooks, sample apps, demos, and showcase use cases

### Takeaway
The dev.meta.ai cookbook and github.com/meta-models show the use cases Meta wants highlighted. These include perception-to-action, smart glasses, computer use, SAM video effects, voice-controlled agents, multi-agent Kanban orchestration, grounded image series, and local-first Glimmer agents. Launch demos include a Facebook Marketplace listing from phone video, dinner-party computer use, a holiday campaign across Google Docs and a terminal, an X-wing CFD simulation report, and a bass edit and mix report.

### Cited Findings
- Cookbook recipes (all at dev.meta.ai/docs/cookbook/...) — [dev.meta.ai Cookbook](https://dev.meta.ai/docs/cookbook.md)
  - **Perception:** chart analysis; error screenshot→fix; "Perception grounding" (pin interactive markers to object pixel locations in a generated HTML overlay).
  - **Wearables:** "Smart glasses with OpenClaw" (look through Ray-Ban Meta glasses, ask aloud, hear the answer).
  - **Coding agents:** browser-verified web design; iterative and one-shot 3D browser game dev; GitHub Actions agent (triage, PR review, bug-fix PRs); generating slides; sandboxed execution.
  - **Agent patterns:** basic loop, interleaved reasoning and tool use, multi-turn context management, "Alert fatigue copilot" (grounded patterns in noisy alerts with strict JSON), "Multi-agent orchestration" (specialist agents on a shared Kanban board).
  - **Computer use:** Linux desktop and macOS native recipes.
  - **Muse Image:** compose and edit, web-search-grounded images, consistent series, multi-turn detail edits.
  - **Voice:** realtime STT with speakers; "Control Apple Chess with voice" (spoken moves → validated computer-use actions, dry-run mode, fail-closed input).
  - **SAM:** API basics; pet video→animated sticker pack; multi-speaker headlocked speech-bubble captions.
  - **Open weights:** Spark Open on 2–4 Mac Studios; TorchTitan RL (GRPO/DAPO) and SFT; Glimmer local agent that asks before calling Spark.
- Launch demos:
  - Muse Spark 1.1: Marketplace listing from smartphone video; dinner-party computer use; OpenCode debugging; DeepSWE self-evaluation — [Meta AI blog](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
  - Muse Spark 1.3: holiday campaign across Google Docs and a terminal; X-wing CFD flow-simulation report; bass edit and mix report; Parks & Rec presentation — [Meta research blog](https://research.meta.ai/blog/introducing-muse-spark-1-3)
- Adjacent Connect 2026 platforms: Wearables Device Access Toolkit 1.0 (camera capture, voice streaming, motion tracking on AI glasses); web apps for Meta Ray-Ban Display; WebMCP (dev preview); Meta AI Connectors (dev preview, API or MCP server); Muse Connector Platform. Code resources are at github.com/meta-models — [Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)
- Muse Spark 1.3 is on Oracle Cloud AI Platform and in private preview on Google Cloud — [Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)

### Inferences
- The recurring themes are **perception → structured understanding → action in the real world or real apps**, plus agents that confirm before consequential actions. A project that sees (video or glasses), segments (SAM), reasons over long context (Spark/Wonder), acts (computer use or tools), and asks before irreversible steps matches Meta's narrative closely.
- Combining Muse Spark with SAM 3.1 video and Voice Transcribe is already validated by Meta's own "headlocked captions" recipe, so it is a low-risk technical base to extend in a new direction.

### Gaps
- The contents of the github.com/meta-models repos (e.g. full sample apps) were not enumerated.
- The glasses DAT kit's hackathon eligibility is unclear.

---

## 9. Developer sentiment: strengths, weaknesses, reliability (HN, Reddit, X)

### Takeaway
Sentiment is cautiously positive on price-performance, long context, and the open-weights return, and skeptical about benchmark framing (Wonder Full vs Wonder), reasoning latency at high effort, data use in Contributor mode, privacy, and regional availability. Direct Reddit and HN threads were thinly indexed, so most of this evidence is secondhand.

### Cited Findings
- HN, Muse Wonder launch thread: the headline benchmarks are for Wonder Full (subscription-only), there was debate over "benchmaxxing," and Wonder Full underperformed Opus 5.5 on an image→HTML test (some blamed the Muse Code harness). One user said "two somewhat small prompts" on Wonder Max-contributor used 4% of a weekly quota. Plans were North America-only at launch — [HN](https://news.ycombinator.com/item?id=50059115); [eesel summary](https://www.eesel.ai/blog/meta-muse-wonder-review)
- HN privacy concern: Meta's internal ~3% violation rate for mishandling personal information was called "unacceptably high" — [HN comment](https://news.ycombinator.com/item?id=50059638) (via search summary)
- Nathan Lambert on Spark Open: "I waited so long for US open weight models to be relevant again" — [VentureBeat](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops)
- Latency: TTFAT of ~48 s at max effort — [Artificial Analysis](https://artificialanalysis.ai/models/muse-spark-1-3/providers). A review of 1.2 found max effort "often is not worth it for interactive coding" — [aireiter 1.2 review](https://aireiter.com/blog/muse-spark-1-2)
- Reviews say Spark is "not ready to be the only production model for latency-sensitive, audio-heavy, privacy-sensitive, or redundancy-critical systems" — [layer3labs review](https://www.layer3labs.io/guides/muse-spark-1-3-review) / [aireiter](https://aireiter.com/blog/muse-spark-1-3-api-pricing-review) (secondary; the exact attribution between the two came via a search summary)
- DataCamp: reasoning traces are not exposed, which makes debugging harder. Some Reddit users reported meta.ai serving 1.1 in the EU — [DataCamp](https://www.datacamp.com/blog/muse-spark-1-3)
- The Register on Glimmer: "doesn't exactly move the needle much" — [The Register](https://www.theregister.com/a/5285666)
- Muse Code: "cheap coding agent has a data price" (Contributor default). It is a fast beta agent with an occasional failed integration — [joaoqueiros review](https://www.ai.joaoqueiros.com/blog/muse-code-spark-1-2-pricing-contributor-data-reliability-review)
- An unverified report from Tech Insider headlines a "Meta Muse backdoor" that stayed unpatched for 24 hours — [tech-insider](https://tech-insider.org/meta-muse-backdoor-unpatched-24-hours-2026/) (low-quality source, unverified)

### Inferences
- In a live demo, keep effort low or medium, stream everything, and use background or async jobs for heavy steps so the UI never sits idle for 40+ s.
- For Startup-track "production-readiness," show retry and backoff on 429/503, a model fallback (Spark → Spark Open on Fireworks or Baseten, which is the same model family, or Glimmer locally), Standard mode rather than Contributor for user data, file expiry (`expires_after`), and human-confirmation gates. All of these address the documented skepticism.

### Gaps
- No direct r/LocalLLaMA thread content was retrievable.
- X sentiment was not sampled beyond official accounts and a few named voices.
- There are no independent uptime or SLA statistics for api.meta.ai.
