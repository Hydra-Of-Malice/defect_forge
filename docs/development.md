# Development notes

This repo is **Defect Forge**, an Indie-track entry in the Meta Global AI Developer Hackathon. The deadline is Thu Nov 5 2026, 07:30 IST (02:00 UTC). The product is built. Read [`HANDOFF.md`](HANDOFF.md) for its status and the remaining human tasks, and [`README.md`](README.md) for the architecture.

## Commands

- Setup: `.\scripts\setup.ps1` (Windows) or `./scripts/setup.sh`.
- Run: `.\scripts\dev.ps1` serves the API and built UI on **http://localhost:8765**. **Port 8000 is taken on the dev machine; never use it.**
- Tests: `.venv\Scripts\python -m pytest -q tests`. They run offline on a fake Meta transport and must stay green.
- Frontend: `cd frontend; npm run build` (needs zero TS errors). Mock UI: `$env:VITE_MOCK='1'; npm run dev`.
- Eval: `python eval/run_eval.py` is resumable and cached in `docs/results/raw/`; re-running it costs $0 unless you delete raw files.
- Live checks: `python scripts/system_check.py` exercises every live path with PASS/FAIL (about $0.30); `python scripts/smoke_run.py --per-type 1` is a quick forge (about $0.20). Every call lands in `var/ledger.jsonl`; `BUDGET_USD` is a hard stop.
- The HTTP contract between backend and frontend is `docs/api-contract.md`. Keep both sides in sync.

## Hard rules

- **Only Meta models at runtime:** `muse-spark-1.3`, `muse-image-1.0` and `sam-3.1` through the Meta Model API. Never add a call to, or a dependency on, any other learned model: OpenAI, Gemini, Llama, Whisper, any TTS, embeddings, CLIP, LPIPS, rembg, MediaPipe, YOLO or torchvision models. OpenCV, NumPy, SciPy and Pillow are fine.
- **Never train a model on Muse Image outputs.** Forged images are evaluation data and in-context examples only (Model API Terms §10.1(ix)).
- **Never commit `.env`, API keys, or MVTec AD images** (CC BY-NC-SA). Fixtures come only from the team's own photos or Muse Image generations (`fixtures/parts/`). `scripts/record_demo.py` refuses runs that use non-fixture parts.
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
  - Edits move and recolour pixels they weren't asked to (other teams saw 16–40 px shifts on whole pages; we measured at most 3.4 px on 512 px crops), so always resize → ECC-align → colour-match → diff → composite only the changed region.
  - Limited to 150 requests per minute per team; use a semaphore.
- **SAM 3.1:**
  - Call it non-streaming via `responses.create(model="sam-3.1", ...)` and decode with the `meta-sam-parser` package.
  - Masks are box-local, so paste each one at `bounds.left/top`.
  - Box prompts need a `<Nf>` frame header; build them with the parser's `build_object_prompt`.
  - Run `ImageOps.exif_transpose` and resize to 1280 px or less before calling it.
  - An empty result is valid and still billed.
- **Measured in the gate tests (`docs/gate-results.md`):**
  - Muse Image edits at `reasoning_strength="low"` with tools off take about 11 s, always return 1600×1600, and shift at most 3.4 px after ECC alignment.
  - SAM concept prompts ("hazelnut", "nut") come back **empty** on MVTec scans. Part masks come from a **Muse Spark box into SAM 3.1** (`forge/locate.py`), with a point prompt at the Otsu centroid and then Otsu as fallbacks. Thresholding alone fails on paper and grid mats.
  - SAM box prompts must be **tight**: padding by 20% drops the median IoU from 0.87 to 0.48.
  - Spark inspector calls take 5–6 s (p50), and `prompt_cache_key` caching works.
  - Working reference code is in `spikes/metaapi.py` and `spikes/forge_lib.py`.
- **Retries:** retry 429, 5xx, timeouts and connection errors with exponential backoff plus jitter, and honour `Retry-After`. Never retry 400 or 401. The Model API intermittently answers 404 "model not found" for valid models, so `meta/client.py` retries 404 too (3 attempts).
- **Logging:** log every call (model, latency, cost, cached flag) to a JSONL ledger; the UI's call-log drawer reads it.

## Working conventions

- Commit small and often, with clear messages; the commit history is evidence of in-event work.
- Judges clone on macOS and Linux, so use `pathlib`, ship both `setup.ps1` and `setup.sh`, and keep line endings normalized (`.gitattributes`).
- Prefer copying from the official Meta cookbook (MIT). Record any copied MIT/Apache code in `THIRD_PARTY.md` with its license. Code from repos with no license is a pattern to re-implement, never something to copy.
- A stress variant counts as **caught** only if the inspector's box overlaps the defect; any other defect claim is `flagged`. Report repeated passes, because the inspector varies between runs.
- Deterministic code verifies and models perceive and judge. Validators (pixel identity outside the mask, inside the part, size, SAM-vs-diff IoU, provenance complete) must not call a model.
