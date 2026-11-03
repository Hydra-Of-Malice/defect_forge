# Handoff: Defect Forge

**Status (Wed Nov 4, IST):** the product is **built, tested and evaluated**. Everything that can be done in code is in this repo. The remaining items are human-only (video, real-part photos, X post, form, making the repo public). They're listed below in order.

**Deadline: Thu Nov 5, 07:30 IST** (Wed Nov 4, 9:00 PM ET). Target submit time is 04:30 IST, which leaves a 3-hour buffer.

## What exists

| Piece | Where | State |
|---|---|---|
| Backend (FastAPI): Meta client, forge pipeline, 8 validators, critic retries, severity ladder, curves, inspector, COCO export, SSE, cost ledger, budget guard, demo replay | `backend/app/` | ✅ live-tested |
| Frontend (React): Forge, Stress test, Inspect, Results, call-log drawer, demo badge | `frontend/` (built into `frontend/dist`, served by the backend at :8765) | ✅ live-tested in a browser |
| Evaluation (pre-registered in `EVAL.md`) | `eval/run_eval.py` → `docs/results/eval.md` and `eval.json` | ✅ run |
| Blind-spot experiment (white print) | `eval/blind_spot.py` → `docs/results/blind_spot.json` | ✅ run |
| Physical check on real damaged parts | `eval/home_check.py` + `eval/home_set/` | ⏳ needs your photos |
| Offline tests (fake Meta transport) | `tests/` (`python -m pytest -q tests`) | ✅ 12 passing |
| Demo replay fixture (Muse-Image-generated parts, no MVTec) | `fixtures/demo_run/`, `fixtures/demo_inspect/` | ✅ |
| Docs | `README.md`, `EVAL.md`, `THIRD_PARTY.md`, `docs/friction-log.md`, `docs/api-contract.md`, `docs/video-script.md`, `docs/submission.md`, `docs/gate-results.md` | ✅ |

## Run it

```powershell
.\scripts\setup.ps1          # once: venv, deps, frontend build, .env
.\scripts\dev.ps1            # http://localhost:8765  (live if MODEL_API_KEY is set in .env)
```

On macOS or Linux, use `./scripts/setup.sh` and `./scripts/dev.sh`.

- **Demo mode:** set `DEMO_MODE=1` in `.env`, or leave the key empty.
- **Phone camera:** run `.\scripts\tunnel.ps1` and open the https URL on the phone.
- **Spend:** a live forge of 4 types × 1 sample plus the stress test costs about $0.21. 4 types × 3 costs about $0.57. The ledger is `var/ledger.jsonl`, and the call-log drawer shows the running total.

## Human-only tasks, in order

1. **Accept the GitHub invite** (Pallav, `PDGamerSG`) and confirm Pallav is listed as a teammate on the Cerebral Valley submission.
2. **Real-part check (about 45 min):**
   - Buy hazelnuts and damage them: drill 0.5, 1 and 2 mm holes (or use a heated needle); make one faint and one strong ink mark, including **white** ink (white print is the real blind spot); crack one with pliers; keep some good.
   - Shoot top-down on matte black paper under a desk lamp, one folder per condition in `eval/home_set/` (see `eval/home_check.py`).
   - Run `python eval/home_check.py`, and add its table to `docs/results/eval.md` and the video.
3. **Record the video** following `docs/video-script.md`: ≤ 2:50, live run, call-log drawer visible, the aha by 0:30. Upload it as unlisted YouTube.
4. **X post:** post the "which crack is real?" quiz with a 30–45 s clip, using the text in `docs/submission.md`. Put the post link in the form *before* submitting.
5. **Make the repo public** (Settings → General → Change visibility). Before that, decide whether `reports/` and `research_notes/` stay, since they contain competitor analysis, and choose a license (MIT is suggested).
6. **Fill in the form** from `docs/submission.md` (numbers are in `docs/results/eval.md`). Check that the repo, video and post all open in a logged-out browser. Submit by 04:30 IST.
7. **After the event:** rotate the Meta API key, since it was pasted in chat.

## Rules this build already satisfies

- **Every runtime model is Meta's:** `muse-spark-1.3`, `muse-image-1.0`, `sam-3.1`. OpenCV, NumPy and Pillow are classical code. There's no TTS and no other model. The README states which models run where.
- **No MVTec images are committed** (CC BY-NC-SA). `data/` and `var/` are gitignored. The demo uses Muse-Image-generated parts.
- **Model API Terms §10.1(ix):** forged images are used for evaluation, benchmarking and in-context inspection only, and the export is labeled as an evaluation suite.
- **Demo mode** is opt-in. The live path is the default, and the README explains both.

## If something breaks

- **Port 8000** is taken by another app on the original dev machine, which is why everything uses **8765**. Override the frontend's target with `VITE_API_TARGET`.
- **The Model API intermittently returns 404 "model not found"** for valid models. The client retries it (`backend/app/meta/client.py`).
- **Budget guard:** the backend refuses new calls once `var/ledger.jsonl` passes `BUDGET_USD` (default 100).

## History

- Round-1 research: `reports/Meta AI hackathon winning ideas.md`.
- The build plan: `reports/Meta hackathon build feasibility.md`.
- Gate tests that changed the headline from "teach the inspector" to "measure its detection threshold": `docs/gate-results.md`.
