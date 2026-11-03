# Instructions for coding agents

This repo is **Defect Forge**, an Indie-track entry in the Meta Global AI Developer Hackathon. The deadline is Thu Nov 5 2026, 07:30 IST (02:00 UTC). Read [`HANDOFF.md`](HANDOFF.md) first for the plan, rules and current status. The build plan, exact API call patterns and gotchas are in [`reports/Meta hackathon build feasibility.md`](reports/Meta%20hackathon%20build%20feasibility.md).

## Hard rules

- **Only Meta models at runtime:** `muse-spark-1.3`, `muse-image-1.0` and `sam-3.1` through the Meta Model API. Never add a call to, or a dependency on, any other learned model: OpenAI, Anthropic, Gemini, Llama, Whisper, any TTS, embeddings, CLIP, LPIPS, rembg, MediaPipe, YOLO or torchvision models. OpenCV, NumPy, SciPy and Pillow are fine.
- **Never train a model on Muse Image outputs.** Forged images are evaluation data and in-context examples only (Model API Terms §10.1(ix)).
- **Never commit `.env`, API keys, or MVTec AD images** (CC BY-NC-SA). Fixtures come from the team's own photos only.
- **No Streamlit.** The frontend is Vite + React + TypeScript + Tailwind; the backend is FastAPI + asyncio. State lives on disk as JSON: no database, no auth.
- **The live path is the default.** `DEMO_MODE=1` replays recorded runs with a visible badge.

## Meta Model API essentials

- Base URL `https://api.meta.ai/v1`. Use the `openai` Python SDK with `base_url` and `api_key=os.environ["MODEL_API_KEY"]` passed explicitly, because the SDK does not read that variable. Pin every model ID.
- **Spark:**
  - Strict `json_schema` output must be a flat object with every key required and `additionalProperties: false`.
  - Reasoning tokens count against `max_output_tokens` / `max_tokens`, so set at least 4000 and use effort `low` or `minimal` (`none` returns 400).
  - `tool_choice` only accepts `"auto"`.
  - Images go in user turns only, at most 50 per call. Boxes come back on a 0–1000 grid; clamp them.
- **Muse Image edits:**
  - Send a raw JSON POST to `/v1/images/edits` with `httpx` (`images: [{image_url: data_url}]`, `response_format: "b64_json"`). The SDK sends multipart and gets a 415.
  - `mask`, `seed`, `input_fidelity` and `partial_images` return 400.
  - Edits shift the image 16–40 px and change pixels they weren't asked to, so always resize → ECC-align → colour-match → diff → composite only the changed region.
  - Limited to 150 requests per minute per team; use a semaphore.
- **SAM 3.1:**
  - Call it non-streaming via `responses.create(model="sam-3.1", ...)` and decode with the `meta-sam-parser` package.
  - Masks are box-local, so paste each one at `bounds.left/top`.
  - Box prompts need a `<Nf>` frame header; build them with the parser's `build_object_prompt`.
  - Run `ImageOps.exif_transpose` and resize to 1280 px or less before calling it.
  - An empty result is valid and still billed.
- **Retries:** retry 429, 5xx, timeouts and connection errors with exponential backoff plus jitter, and honour `Retry-After`. Never retry 400, 401 or 404.
- **Logging:** log every call (model, latency, cost, cached flag) to a JSONL ledger; the UI's call-log drawer reads it.

## Working conventions

- Commit small and often, with clear messages; the commit history is evidence of in-event work.
- Judges clone on macOS and Linux, so use `pathlib`, ship both `setup.ps1` and `setup.sh`, and keep line endings normalized (`.gitattributes`).
- Prefer copying from the official Meta cookbook (MIT). Record any copied MIT/Apache code in `THIRD_PARTY.md` with its license. Code from repos with no license is a pattern to re-implement, never something to copy.
- Deterministic code verifies and models perceive and judge. Validators (pixel identity outside the mask, inside the part, size, SAM-vs-diff IoU, provenance complete) must not call a model.
