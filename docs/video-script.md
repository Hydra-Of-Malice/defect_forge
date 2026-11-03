# Demo video script (target 2:50, hard cap 3:00)

**Record at 1920×1080** with the browser at 100% zoom and the call-log drawer open where noted. **Show live Meta calls**: the call-log drawer lists every `muse-image-1.0`, `sam-3.1` and `muse-spark-1.3` call with latency and cost. Keep narration calm and concrete. Everything on screen must be built during the event.

The numbers below are filled in from `docs/results/eval.md` (eval of Nov 4).

| Time | On screen | Narration (suggested) | Rubric |
|---|---|---|---|
| 0:00–0:08 | Forge page: the grid of forged hazelnut defects filling in live, each with its orange mask outline | (none; captions only) "Every defect here was forged by Muse Image and labeled to the pixel." | Demo |
| 0:08–0:30 | Stress-test page: the detection-threshold curves | "This inspector looks perfect on obvious defects: 95.5% recall and 100% specificity on the MVTec benchmark. But before your line has produced a single defect, Defect Forge tells you where it breaks: cuts under half a millimetre are mostly missed, cracks fall to 33% at 0.4 mm, and faint holes vanish." **AHA** | Impact |
| 0:30–0:50 | Spec textarea → "Read spec" → taxonomy cards appear | "Start with the QA spec you already have. Muse Spark turns it into a defect taxonomy, with clause numbers and visual descriptions. No real defect images needed." | Tooling |
| 0:50–1:25 | Choose 3 good parts → "Forge defects" → the stage timeline lights up, cards stream in, call-log drawer open | "For each defect, Muse Image edits a crop of a good part. Our deterministic compositor aligns the edit and keeps only the changed pixels; everything else is byte-identical. SAM 3.1 cross-checks the mask, and a Muse Spark critic rejects anything unrealistic and rewrites the prompt." Show one card's before/after slider, raw vs composite, and "validators 8/8" | Demo, Depth |
| 1:25–1:55 | Stress test running: severity strips fill with green ✓ / red ✗, then the curves update | "Then we fade and shrink every forged defect with plain OpenCV. The ground truth is known by construction, so this is a real measurement, not a model grading itself. Muse Spark inspects each variant." | Depth |
| 1:55–2:20 | Inspect page: webcam or phone pointed at a real hazelnut you drilled → DEFECT with SAM overlay; then a good one → GOOD | "And it works on real parts: a nut I drilled at home, caught and masked live." (If filmed, show the drilled-hole size ladder.) | Demo, Impact |
| 2:20–2:40 | Results page: benchmark table, SAM IoU, forge stats ($0.020 and 25 s per sample) and the blind-spot panel, architecture diagram | "Three Meta models in one closed loop: 55 labeled defects at two cents each, SAM masks at 0.84 IoU on real defects, a pre-registered eval, 12 offline tests. And it found a real blind spot: white print read as gloss. Two forged white-print examples fixed it, 17 of 17." | Depth, Tooling |
| 2:40–2:50 | README hero / repo URL | "Defect Forge: know what your inspector will miss before your line makes a single defect." | Impact |

## Shot checklist
- [ ] Clean browser profile, no bookmarks bar, dark OS theme
- [ ] Start backend: `.\scripts\dev.ps1` (live, key in `.env`). Do **not** use DEMO_MODE for the main take
- [ ] Pre-warm: run one small forge first so part masks are cached and the live run starts immediately
- [ ] Take 1: full live run with per-type = 3 on 3 sample parts (about 2–3 min real time; speed up 2–3× in editing, and say so on screen: "sped up ×2")
- [ ] Inspect: prepare 1 drilled hazelnut, 1 ink-marked, 1 good, on black paper under a desk lamp
- [ ] Record narration separately; add captions
- [ ] Export at 1080p, upload as **unlisted** YouTube, paste the link in the submission form
