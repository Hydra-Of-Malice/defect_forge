# Submission form drafts (Cerebral Valley portal)

Numbers are from `docs/results/eval.md`. Track: **Indie**. Theme: **Push the Frontier**.

## Project name
Defect Forge

## Problem statement (one or two lines)
A new production line has no defects to learn from, so nobody knows what its visual inspector will miss until bad parts ship. Defect Forge forges realistic, pixel-labeled defects from your QA spec and photos of good parts, then measures the smallest and faintest defect your inspector still catches.

## Description (100–200 words)
Defect Forge turns a QA spec and a few photos of **good** parts into a stress test for visual inspection.

Muse Spark reads the spec into a defect taxonomy and finds the part, and SAM 3.1 masks it. Muse Image paints each defect onto a crop, and our deterministic compositor keeps only the changed pixels. SAM 3.1 cross-checks the mask, a Muse Spark critic rejects weak forgeries and rewrites the prompt, and eight deterministic validators gate every sample.

OpenCV then fades and shrinks every forgery on a severity ladder, and Muse Spark inspects each variant over three passes. Ground truth is known by construction, so this is a measurement, not a model grading itself. Defect Forge plots detection-threshold curves: on forged hazelnut defects, cuts are 73% caught at full size and 0% at about 0.5 mm, while sub-millimetre holes are noticed but not pinpointed.

On the real MVTec hazelnut benchmark, the spec-only inspector scores 94–97% recall with no false alarms across three passes. Its weak spot is white print read as gloss.

Each labeled defect costs $0.02. The evaluation was pre-registered, and we publish our null results and a claim we withdrew.

## Hosted demo link
https://defect-forge-kappa.vercel.app (a replay of a recorded live run; live mode runs locally from the repo)

## Use of Meta products
- **muse-image-1.0** (`/v1/images/edits`): forges each defect on a 512 px crop. It also generated the license-clean sample good parts and the demo fixtures (`/v1/images/generations`).
- **sam-3.1**:
  - part masks from Muse Spark's box (concept prompts came back empty on studio scans, and thresholding fails on paper or grid mats)
  - tight box prompts to cross-check every forged mask (mean IoU 0.82 vs the diff mask; median 0.84 vs ground truth on real defects)
  - masks behind every live inspection claim (a claimed defect with no SAM mask is reported as "uncertain")
- **muse-spark-1.3**:
  - spec → taxonomy (strict JSON with arrays)
  - finding the part in any photo, ignoring the paper or desk under it
  - realism critic with revised prompts (agentic retry)
  - the inspector under test (strict JSON with 0–1000 boxes, prompt caching)

Every runtime model is a Meta model. OpenCV and NumPy only do alignment, compositing, severity transforms and validation.

## Why Meta's models matter
The loop only works because the three models do different jobs no single model covers:
- **Muse Image:** an editor that preserves the photo closely enough to composite.
- **SAM 3.1:** a promptable segmenter that labels any defect from a box, with no training.
- **Muse Spark:** a reasoner that reads a spec, judges realism and inspects parts with structured output.

Each one is replaceable on paper, but together they turn *a text spec* into *a measured inspection threshold* in minutes, for about $0.02 per labeled defect, with zero real defect images.

## Feedback on Meta products
Paste `docs/friction-log.md`, rows 1–6, 8 and 12–13.

## X post (Most Viral bonus): post natively with the 30–45 s clip
> Which crack is real? 🔍 One of these hazelnut defects is real (a nut we drilled ourselves); the rest were forged by @AIatMeta's Muse Image and labeled to the pixel by SAM 3.1. Then we used them to measure where an AI inspector stops seeing defects. Built for the #MetaAIHackathon. Guess in the replies 👇 [video] [repo link]

Reply later with the answer and the detection-threshold curve image. Use only your own photos and Defect Forge outputs in the post, never MVTec images (CC BY-NC-SA).
