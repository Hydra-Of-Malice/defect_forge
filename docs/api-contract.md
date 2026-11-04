# Defect Forge HTTP API contract (backend ⇄ frontend)

The backend is FastAPI on `http://localhost:8765`. The frontend dev server (Vite, port 5173) proxies `/api` and `/files` to it. All JSON uses snake_case. All image URLs are relative paths under `/files/...` served by the backend.

## Common types

```ts
type DefectType = string;            // e.g. "hole" | "crack" | "print" | "cut" (comes from the taxonomy)

interface TaxonomyItem {
  defect_type: DefectType;           // short slug
  clause: string;                    // spec clause it came from, e.g. "4.2"
  description: string;               // visual description used to forge it
  severity_note: string;             // what the spec says about size/limits
}
interface Taxonomy {
  part_name: string;                 // "hazelnut"
  part_width_mm: number;             // nominal width, used to convert px -> mm (0 if unknown)
  defects: TaxonomyItem[];
}

interface Part {                     // a photo of a GOOD part
  id: string;
  name: string;
  url: string;                       // /files/parts/<id>.jpg
  mask_url: string | null;           // part mask PNG (white = part)
  width: number; height: number;
  source: "sample" | "upload";
}

interface CallRecord {               // one Meta Model API call (also streamed as SSE "call")
  t: number;                         // unix seconds
  model: string;                     // "muse-image-1.0" | "sam-3.1" | "muse-spark-1.3" | ...
  op: string;                        // "edit" | "segment" | "taxonomy" | "critic" | "inspect" | ...
  ms: number;
  status: number | string;           // 200, 400, "replay", ...
  cost_usd: number;
  run_id: string | null;
  cached_tokens?: number;
}

interface Validator { id: string; name: string; passed: boolean; detail: string }

interface Sample {                   // one forged defect
  id: string;
  run_id: string;
  part_id: string;
  defect_type: DefectType;
  status: "forging" | "accepted" | "rejected" | "failed";
  attempt: number;                   // 1..3 (critic retries)
  prompt: string;
  original_url: string;              // full good image
  crop_original_url: string;         // 512 crop before edit
  crop_raw_url: string | null;       // raw Muse Image output (resized to crop)
  crop_composite_url: string | null; // crop after deterministic composite
  composite_url: string | null;      // full image with the forged defect
  mask_url: string | null;           // full-size defect mask PNG
  overlay_url: string | null;        // full image with mask outline drawn
  bbox: [number, number, number, number] | null;  // x0,y0,x1,y1 px in full image
  area_px: number;
  size_mm: number | null;            // equivalent diameter in mm (if part_width_mm known)
  sam_iou: number | null;            // SAM 3.1 tight-box mask vs diff mask
  critic: { realism: number; matches_type: boolean; artifacts: string; verdict: "accept" | "reject"; revised_prompt: string } | null;
  validators: Validator[];           // 8 deterministic checks
  cost_usd: number;
  ms: number;
}

interface SeverityPoint {            // one severity-ladder variant inspected by the inspector
  sample_id: string;
  defect_type: DefectType;
  kind: "opacity" | "size";
  level: number;                     // opacity 1.0/0.5/0.25/0.12 ; size 0.6/0.35/0.2
  url: string;                       // full image variant
  size_mm: number | null;
  detected: boolean;                 // the inspector's box overlaps the defect
  flagged: boolean;                  // any defect claim, including one in the wrong place
  box_px: [number, number, number, number] | null;
  pred_type: string;
  confidence: number;
}

interface CurveCell { kind: "opacity" | "size"; level: number; n: number; detected: number; flagged: number; rate: number; ci_low: number; ci_high: number; mean_size_mm: number | null }
interface Curve { defect_type: DefectType; cells: CurveCell[]; threshold_note: string }  // e.g. "detection breaks below 0.25 opacity"

interface Run {
  id: string;
  created: number;
  status: "running" | "completed" | "failed";
  spec_text: string;
  taxonomy: Taxonomy;
  part_ids: string[];
  per_type: number;
  samples: Sample[];
  severity: SeverityPoint[];
  curves: Curve[];
  controls: { n: number; flagged: number } | null;   // unedited parts inspected as a false-alarm control
  summary: { accepted: number; rejected: number; failed: number; cost_usd: number; seconds: number; mean_sam_iou: number | null } | null;
  demo: boolean;                     // true if this run is a recorded replay
}
```

## Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET | `/api/health` | | `{ ok: true, demo_mode: boolean, models: string[], spent_usd: number, budget_usd: number }` |
| GET | `/api/ledger?limit=200` | | `{ calls: CallRecord[], spent_usd: number, by_model: Record<string, {calls: number, cost_usd: number}> }` |
| GET | `/api/default-spec` | | `{ spec_text: string }` (sample hazelnut QA spec) |
| POST | `/api/taxonomy` | `{ spec_text: string }` | `Taxonomy` |
| GET | `/api/parts` | | `{ parts: Part[] }` (built-in sample parts + uploads) |
| POST | `/api/parts` | multipart `files` (1..10 images) | `{ parts: Part[] }` (computes part masks) |
| POST | `/api/runs` | `{ spec_text: string, taxonomy: Taxonomy, part_ids: string[], per_type: number, stress: boolean }` | `{ run_id: string }` |
| GET | `/api/runs` | | `{ runs: {id, created, status, per_type, accepted, demo}[] }` |
| GET | `/api/runs/{id}` | | `Run` |
| GET | `/api/runs/{id}/events` | | **SSE** stream (below) |
| POST | `/api/runs/{id}/stress` | `{}` | `{ ok: true }` (runs the severity ladder on accepted samples; streams events; 409 if the run is busy) |
| GET | `/api/runs/{id}/export` | | `application/zip` (COCO JSON + images + masks + provenance) |
| POST | `/api/inspect` | multipart `file` + optional `spec_text`, `use_examples_run_id` | `Inspection` |
| GET | `/api/eval` | | `EvalReport` (precomputed benchmark results, see below) |
| GET | `/files/...` | | static artifacts |

```ts
interface Inspection {
  verdict: "defect" | "good" | "uncertain";   // "uncertain" = model said defect but SAM found no mask in its box
  defect: boolean; type: string; confidence: number; rationale: string;
  box_px: [number, number, number, number] | null;
  image_url: string; overlay_url: string | null; mask_url: string | null;
  ms: number; cost_usd: number;
}

interface EvalReport {
  generated: number;
  real_benchmark: { n_good: number; n_defect: number; recall: number; recall_ci: [number, number]; specificity: number; specificity_ci: [number, number]; type_accuracy: number; box_hit: number; by_type: Record<string, {n: number; detected: number}> } | null;
  in_context: { condition: string; label: string; recall: number; specificity: number; n: number }[];   // C0..C3 supporting table
  faint_lift: { condition: string; label: string; detected: number; n: number }[];                    // zero-shot vs forged examples on hard severity levels
  sam_real: { n: number; median_iou: number; mean_iou: number; by_type: Record<string, number> } | null;
  forge_stats: { attempted: number; accepted: number; acceptance_rate: number; mean_sam_iou: number | null; cost_per_accepted_usd: number; seconds_per_accepted: number; validator_pass_rate: number } | null;
  curves: Curve[];
  notes: string[];
}
```

## SSE events (`/api/runs/{id}/events`)

Each message is `event: <name>` + `data: <json>`. The stream replays all past events for the run first, then live ones, and ends after `run_completed`. After `POST /stress`, it instead streams only that re-run's events and ends after `stress_completed`.

| event | data |
|---|---|
| `run_started` | `{ run_id, total_samples }` |
| `stage` | `{ stage: "taxonomy" \| "locate" \| "forge" \| "composite" \| "label" \| "critic" \| "validate" \| "export" \| "stress", status: "start" \| "done", sample_id?: string, detail?: string }` |
| `call` | `CallRecord` |
| `sample` | `Sample` (sent on every status change; the same `id` updates in place) |
| `severity` | `SeverityPoint` |
| `curves` | `{ curves: Curve[] }` |
| `controls` | `{ n, flagged }` |
| `run_completed` | `{ summary }` |
| `stress_completed` | `{ curves: Curve[] }` |
| `error` | `{ message }` |

## Demo mode

With `DEMO_MODE=1`, the backend makes **no** Meta calls. `/api/runs` POST replays a recorded run from `fixtures/demo_run/` with its original timing (sped up about 4×), `/api/inspect` returns recorded inspections for the built-in sample images, and `/api/health` reports `demo_mode: true`. The UI must show a visible amber "DEMO REPLAY" badge whenever `demo_mode` is true or `run.demo` is true.
