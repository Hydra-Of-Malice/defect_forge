# Gate test results (Wed Nov 4, 01:20–02:10 IST)

All tests ran live against the Meta Model API on the MVTec AD **hazelnut** category: a 70-file subset fetched from the `foersben/mvtec-ad` Hugging Face mirror into the gitignored `data/` folder. The scripts are in [`spikes/`](../spikes/). The raw outputs (images, JSON, ledger) are in `runs/gate/`, which is **gitignored because the images derive from CC BY-NC-SA data**; re-run the scripts to regenerate them.

**Cost:** 308 API calls (35 Muse Image, 49 SAM 3.1, 224 Muse Spark), about **$1.27** in total.

## Verdict: GREEN for the pipeline, with a NEW headline

Forging, compositing and labeling all work, so build Defect Forge. **But the original headline ("forged examples raise the inspector's recall") is dead on hazelnut**, because Muse Spark is already perfect zero-shot. The new headline comes from T6: **Defect Forge stress-tests an inspector and finds its detection threshold.** It forges a defect, then sweeps its severity deterministically and measures where detection breaks. The ground truth is known by construction, it isn't circular, and it sits inside the "evaluation of your own systems" safe harbor of Model API Terms §10.1(ix).

| Test | Result | Pass? |
|---|---|---|
| T0 key and limits | `/v1/models` lists 9 models. Spark limits: 3,000 RPM and 4M TPM (headers `x-ratelimit-*` appear on chat completions, not on `/models`) | ✅ |
| T1 Muse Image settings | Edit on a 512 px crop: **low strength, tools off = 11.0 s**; low+tools 12.1 s; high 27.0 s; high+tools 17.8 s. All four look equally plausible. Output is always **1600×1600**. ECC shift **≤0.7 px** | ✅ use `low`, tools off for batch |
| T2 forge quality | **31/31 edits succeeded** with no safety refusals (even "crack"). 10–14 s each. Shift 0.1–3.4 px. **Byte-identical outside the mask in 31/31.** Visually: holes and print excellent, cracks plausible (hairline). The text prompt is as good as or better than the red-outline prompt | ✅ ≥2 types |
| T3 SAM 3.1 | **Tight GT-box prompt: median IoU 0.867** (hole 0.87–0.93, print 0.86–0.92, cut 0.85–0.90, crack 0.07–0.64). **Padding the box by 20% hurts** (median 0.477): SAM grabs the whole nut. p50 2.2 s, p90 3.0 s. **Concept prompts fail on these scans**: "hazelnut", "nut", "object" and others return empty; only "shell" sometimes matches. A **single center point prompt** gives the part mask (IoU 0.80–0.87 vs an Otsu mask, about 4 s) | ✅ with changes |
| T4 inspector headroom | 20 test images (10 good, 10 defective), four conditions. **C0 spec-text-only: recall 10/10, specificity 10/10, type 10/10, box hit 10/10.** C1 (+2 good) 9/10 specificity; C2 (+6 forged) 10/10 and 10/10; C3 (+4 real) 10/10 and 10/10. p50 5–6 s. Prompt caching works (cached tokens reported) | ⚠️ **ceiling: no headroom** |
| T5 critic and realism | The Spark critic accepts forgeries (text style): hole 4/5, crack 5/5, print 5/5. On **real** defect crops it accepts only 5/9 and **rejects all 3 real cracks** (wrong "type" vs our hairline description). So the critic is a usable filter, **not a realism judge**. A blind sheet was produced (`runs/gate/t5_blind_sheet.jpg`, key in `t5_blind_key.json`). A non-blind check by the builder spotted all 10 forgeries, because **forgeries are smaller and neater than MVTec's dramatic real defects** (broken-open shells, large prints) | ⚠️ realism OK, distribution mismatch |
| T6 severity ladder (extra) | Each forgery is re-rendered with OpenCV at lower opacity or smaller size and inspected zero-shot. **Recall falls off cleanly** (table below), and type is correct in 77/82 detections | ✅ **new headline** |

T6 detection by severity (5 forgeries per cell, zero-shot Muse Spark):

| Defect | Opacity 1.0 | 0.5 | 0.25 | 0.12 | Size 0.6 | 0.35 | 0.2 |
|---|---|---|---|---|---|---|---|
| hole | 5/5 | 5/5 | 3/5 | **0/5** | 5/5 | 5/5 | 3/5 |
| crack | 5/5 | 5/5 | 5/5 | **1/5** | 5/5 | 5/5 | **1/5** |
| print | 5/5 | 5/5 | 4/5 | 3/5 | 4/5 | 5/5 | 3/5 |

## What changes in the build plan

1. **The headline becomes a detection-threshold curve.** "Before your line makes a single defect, Defect Forge tells you the smallest hole, the faintest print and the finest crack your inspector will miss." The eval becomes severity sweeps (size in mm and contrast) per defect type, with Wilson CIs per cell, plus specificity on good parts. The four-condition in-context eval (C0–C3) drops to a single supporting row ("in-context examples don't help when zero-shot is already 100%").
2. **Validate the curve physically.** Drill real hazelnuts with 2–3 bit sizes (e.g. 0.5, 1 and 2 mm) and mark a few with ink at different strengths. Photograph them on the rig and check that the inspector's real detection matches the forged curve. This is the video's strongest "real world" moment and answers "is synthetic severity valid?".
3. **Severity control is deterministic code.** Scale and opacity are applied by OpenCV to the forged delta inside the mask (`spikes/t6_severity.py`). It needs no extra model calls and is exactly reproducible.
4. **Part mask:** use a SAM **point prompt** at the Otsu centroid. Use concept prompts only as an optional extra.
5. **Defect labels:** the diff mask is exact by construction, so use it as the label. Use a SAM box prompt on the **tight** diff box (no padding) only as an independent cross-check (SAM-vs-diff IoU). For cracks, trust the diff mask.
6. **Compositor fix:** keep **all** changed components near the center, not just the largest. Print defects are multi-character and lost characters in 2–3 samples.
7. **Prompts must match the real defect distribution** before the human 2AFC test. Add large variants ("a large piece of shell broken away exposing the kernel", "large white printed characters across the shell"), or compare against **home-made** real defects of matched scale.
8. **Inspector settings that work:** Chat Completions, strict flat schema, `reasoning_effort="low"`, `max_tokens=4000`, `prompt_cache_key`, 768 px JPEG data URLs. p50 is 5–6 s.

## Re-running

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe openai httpx python-dotenv opencv-python-headless numpy pillow scipy meta-sam-parser
# download the hazelnut subset into data/gate/hazelnut (see commands in the handoff), then:
.venv/Scripts/python.exe spikes/t0_key_check.py
.venv/Scripts/python.exe spikes/t3_sam_iou.py
.venv/Scripts/python.exe spikes/t1_t2_forge.py t1
.venv/Scripts/python.exe spikes/t1_t2_forge.py t2
.venv/Scripts/python.exe spikes/t4_t5_spark.py t4
.venv/Scripts/python.exe spikes/t4_t5_spark.py t5
.venv/Scripts/python.exe spikes/t6_severity.py
```

The download command used for the subset (bash), from the repo root:

```bash
D=data/gate/hazelnut; B=https://huggingface.co/datasets/foersben/mvtec-ad/resolve/main/hazelnut
get(){ mkdir -p "$D/$(dirname $1)"; curl -sfL -o "$D/$1" "$B/$1"; }
for i in $(seq 0 9); do get train/good/$(printf %03d $i).png; done
for i in $(seq 0 11); do get test/good/$(printf %03d $i).png; done
for t in crack cut hole print; do for i in 0 1 2 3 4 5; do n=$(printf %03d $i); get test/$t/$n.png; get ground_truth/$t/${n}_mask.png; done; done
```

## Caveats

- The T4 sample is small (20 images). The full 110-image test split may show a few misses, but there is no room for a meaningful in-context lift.
- The T5 human check was done by someone who had seen the forgeries, so it is **not** a blind result. Get 5–10 people who haven't seen them to rate the sheet.
- T6 uses forgeries only. Item 2 above (the drilled-hazelnut ladder) is what makes the curve credible.
