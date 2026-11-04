# Evaluation protocol (pre-registered)

This protocol was committed **before** the evaluation below was run. Results go to `docs/results/eval.json` and `docs/results/eval.md`, produced by `python eval/run_eval.py`. Any deviation is listed under "Deviations" at the end of `docs/results/eval.md`.

## Question

Can Defect Forge, given only a text QA spec and photos of **good** parts, produce pixel-labeled defects realistic enough to **measure an inspector's detection threshold**? And where does that threshold lie for a Muse Spark inspector on hazelnuts?

## Data

- **Benchmark:** MVTec AD `hazelnut` (CC BY-NC-SA 4.0, used for evaluation only, never committed). Test split: 40 good, 70 defective (crack 18, cut 17, hole 18, print 17), each with a ground-truth mask.
- **Forging sources:** MVTec `train/good` images only, so no test image is ever edited.
- **Oracle exemplars (C3):** the last test image of each defect type (crack 017, cut 016, hole 017, print 016). These 4 images are excluded from scoring in **all** conditions, giving 66 defective images per condition.

## Systems

- **Inspector:** `muse-spark-1.3`, Chat Completions, strict JSON (defect, type, 0–1000 box, confidence), `reasoning_effort=low`. The system prompt is the spec text (`backend/app/forge/spec.py: DEFAULT_SPEC`).
- **Forge:** spec → taxonomy (Muse Spark) → 512 px crop edit (Muse Image, `reasoning_strength=low`, tools off) → deterministic composite → SAM 3.1 tight-box mask → Muse Spark critic (up to 3 attempts) → 8 validators. Only accepted samples are used.
- **Severity ladder:** deterministic OpenCV transforms of each accepted forgery: opacity 1.0 / 0.5 / 0.25 / 0.12 and size 0.6 / 0.35 / 0.2.

## Measurements

1. **Real benchmark (C0):** recall, specificity, type accuracy and box hit (box overlaps the GT mask) on the 106 scored test images, with Wilson 95% CIs.
2. **In-context conditions:**

   | Condition | Inspector input |
   |---|---|
   | C0 | Spec only |
   | C1 | + 2 good train images |
   | C2 | + 8 forged defects (2 per type) |
   | C3 | + 4 real defects (oracle) |

   Compare C2 vs C1 with an exact McNemar test on paired outcomes over all 106 images.
3. **SAM 3.1 on real defects:** IoU of tight-GT-box prompts against GT masks on all 70 real defects, by type.
4. **Forge statistics:** attempts, acceptance rate, critic retries, mean SAM-vs-diff IoU, cost and seconds per accepted sample.
5. **Detection-threshold curves (headline):** detection rate per defect type × severity level over all accepted forgeries (target 15 per type), with Wilson CIs. Equivalent defect diameter in mm assumes the spec's 20 mm nominal width.
6. **Faint-defect lift:** on the three hardest levels (opacity 0.25, opacity 0.12, size 0.2), detection with spec only vs with 8 forged exemplars from *other* samples.

## Headline rule

1. Measurement 5 is the headline, stated as the smallest or faintest level per type still caught at ≥80%, and the first level caught below 50%.
2. Measurement 6 is reported as an in-context result **only if** the exact McNemar p < 0.05. Otherwise it is reported as "no significant lift".
3. A null result in measurement 2 is reported as-is.

## Known limitations (stated in advance)

- Forged severity is synthetic. Physical validation with drilled and marked real hazelnuts is a separate, smaller check (`eval/home_set/`).
- The inspector and the critic are both Muse Spark. The headline (5) does **not** depend on the critic's judgment, because ground truth comes from construction.

## Addendum: revalidation (committed before these runs, Nov 4)

An audit of the first results found four problems. This addendum was written before any of the runs below, and `eval/revalidate.py` implements it.

1. A "caught" defect only meant the inspector claimed a defect somewhere in the image.
2. Every number came from a single pass, yet two spec-only passes missed 3 and then 5 real print images.
3. The conclusion that forged white-print examples fixed the blind spot was confounded: the run also contained 2 good photos, and 2 good photos alone (C1) already scored 16/16.
4. Forged and real results disagree by defect type, and forged defects are much smaller than MVTec's.

### R1. Located detection, repeated, with controls

- Same accepted forgeries and the same 7 severity levels, inspected in **3 independent passes**.
- A variant counts as **caught** only if the inspector's box overlaps the defect mask in at least 2 of the 3 passes. Any defect claim is reported separately as **flagged**.
- **Controls:** the unedited source part of every forgery, inspected in each pass, gives the false-alarm rate.
- Report per cell: caught, flagged, Wilson 95% CI, and the count from each pass. Also report the share of variants on which all 3 passes agree.
- These curves replace the single-pass curves as the headline.

### R2. White-print attribution

| Condition | Inspector input |
|---|---|
| W0 | Spec only |
| W1 | + 2 good photos |
| W2 | + 2 forged white prints |
| W3 | + 2 good photos + 2 forged white prints |

- Images: all 17 real print defects and all 40 real good parts, 3 passes per condition. Each image's outcome is its majority over the passes.
- **Credit rule, fixed in advance:** forged white-print examples get credit only if W2 beats W0 on print (exact McNemar p < 0.05 on majority outcomes) **and** W3 has at least W1's print recall with no more false alarms. Otherwise we report that the forged examples showed no proven benefit.

### R3. Real-benchmark stability

Two more full passes of C0 over the 106 scored images. Report the range of recall and specificity next to the original figures.

### R4. Real and forged at matched size

No API cost. For each defect type, compare real and forged detection inside the size band where both exist, using equivalent diameter at the spec's 20 mm width. If the band is empty or tiny, say so.

### Limits that stay

None of this replaces the physical check on real damaged parts (`eval/home_check.py`). Below the smallest real defect in MVTec, the curves have no real-world validation until that check is done.
