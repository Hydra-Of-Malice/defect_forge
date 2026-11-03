# Submission form drafts (Cerebral Valley portal)

Fill **{braces}** from `docs/results/eval.md`. Track: **Indie**. Theme: **Push the Frontier**.

## Project name
Defect Forge

## Problem statement (one or two lines)
A new production line has no defects to learn from, so nobody knows what its visual inspector will miss until bad parts ship. Defect Forge forges realistic, pixel-labeled defects from your QA spec and photos of good parts, then measures the smallest and faintest defect your inspector still catches.

## Description (100–200 words)
Defect Forge turns a QA spec plus a handful of photos of **good** parts into a stress-test suite for visual inspection.

1. **Muse Spark** reads the spec into a defect taxonomy.
2. **SAM 3.1** finds the part.
3. **Muse Image** paints each defect onto a crop.
4. Our deterministic compositor aligns the edit and keeps only the changed pixels (byte-identical elsewhere).
5. SAM 3.1 cross-checks the mask, and a **Muse Spark critic** rejects unrealistic forgeries and rewrites the prompt.
6. Eight deterministic validators gate every sample.

Then comes the part no inspector vendor shows you: OpenCV fades and shrinks every forged defect on a severity ladder, Muse Spark inspects every variant, and Defect Forge plots **detection-threshold curves**, e.g. "holes caught down to {hole mm} mm, missed below". Ground truth is known by construction, so this is a measurement, not a model grading itself.

- **Benchmark:** on MVTec AD hazelnut, the spec-only inspector scores {recall} recall / {specificity} specificity, yet the curves expose its blind spots.
- **Cost:** {accepted} labeled defects at ${cost} each.
- **Rigour:** a pre-registered eval, {n} offline tests, and a COCO export.

## Use of Meta products
- **muse-image-1.0** (`/v1/images/edits`): forges each defect on a 512 px crop. It also generated the license-clean sample good parts and the demo fixtures (`/v1/images/generations`).
- **sam-3.1**:
  - point prompts for part masks (concept prompts came back empty on studio scans, so we switched)
  - tight box prompts to cross-check every forged mask (mean IoU {forge iou} vs the diff mask)
  - masks behind every live inspection claim (a claimed defect with no SAM mask is reported as "uncertain")
- **muse-spark-1.3**:
  - spec → taxonomy (strict JSON with arrays)
  - realism critic with revised prompts (agentic retry)
  - the inspector under test (strict JSON with 0–1000 boxes, prompt caching)

Every runtime model is a Meta model. OpenCV and NumPy only do alignment, compositing, severity transforms and validation.

## Why Meta's models matter
The loop only works because the three models do different jobs no single model covers:
- **Muse Image:** an editor that preserves the photo closely enough to composite.
- **SAM 3.1:** a promptable segmenter that labels any defect from a box, with no training.
- **Muse Spark:** a reasoner that reads a spec, judges realism and inspects parts with structured output.

Each one is replaceable on paper, but together they turn *a text spec* into *a measured inspection threshold* in minutes, for about ${cost} per labeled defect, with zero real defect images.

## Feedback on Meta products
Paste `docs/friction-log.md`, rows 1–6 and 8.

## X post (Most Viral bonus): post natively with the 30–45 s clip
> Which crack is real? 🔍 One of these hazelnut defects is from a real factory dataset; the rest were forged by @AIatMeta's Muse Image and labeled to the pixel by SAM 3.1. Then we used them to find exactly where an AI inspector goes blind. Built for the #MetaAIHackathon. Guess in the replies 👇 [video] [repo link]

Reply later with the answer and the detection-threshold curve image.
