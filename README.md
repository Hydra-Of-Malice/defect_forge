# Defect Forge (working title)

Defect Forge is an entry in the **Meta Global AI Developer Hackathon** (Indie track, theme: Push the Frontier).

> Before your line has produced a single defect, Defect Forge forges the defects your spec describes, labels them to the pixel, and shows which ones your inspector would miss.

**Status:** the plan is finalized and the build hasn't started. **New contributors start with [`HANDOFF.md`](HANDOFF.md).**

## Planned Meta models and where they run

| Model | Runs on | Job |
|---|---|---|
| `muse-spark-1.3` | Meta Model API (Meta-hosted) | Reads the spec into a defect taxonomy, critiques each forgery's realism, inspects real parts |
| `muse-image-1.0` | Meta Model API (Meta-hosted) | Forges defects onto photos of good parts |
| `sam-3.1` | Meta Model API (Meta-hosted) | Part masks and pixel-accurate defect masks |

No other model runs at runtime. OpenCV, NumPy and SciPy handle alignment, compositing and validation as classical code.

## What's in this repo now

- [`HANDOFF.md`](HANDOFF.md): the decided plan, rules, gate tests, schedule and open questions
- [`CLAUDE.md`](CLAUDE.md): instructions for AI coding agents
- [`reports/`](reports/): the two research reports (rules and ideas; feasibility and build plan)
- [`research_notes/`](research_notes/): the underlying sourced research notes
- `.env.example`: copy it to `.env` and add your `MODEL_API_KEY`

This README will be replaced by the final project README before submission. The feasibility report's section "What the README must say" lists what that README needs.
