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
