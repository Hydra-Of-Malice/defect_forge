# Defect Forge: build feasibility (Muse Image forges defects, SAM 3.1 labels them, Muse Spark critiques and inspects)

Research date: Nov 3–4 2026 (about 31 h before the 02:00 UTC Nov 5 deadline). Plan source: `D:\Meta AI hackathon\reports\Meta AI hackathon winning ideas.md`, section "#1 Defect Forge". Platform facts come from `research_notes\Meta AI hackathon winning ideas\meta_models_and_api.md` and from the dev.meta.ai image-generation page, re-fetched today. Team profile (from the coordinator): Indie track, 2 people, web/full-stack plus labeling/CV background, phone + laptop + webcam only.

---

## Overall go/no-go, expected numbers, biggest risks, and first-2-hour de-risking tests

### Takeaway
**Conditional GO.** Every component exists on the API and the cost is trivial (well under $30 of the $150 credit). Close prior art (AnomalyAgent, Apr 2026) already shows that an MLLM agent looping a general-purpose image generator with a quality critic yields usable zero-shot defect data. The two real unknowns are whether Muse Image's local edits look real on a 512 px crop, and whether forged in-context examples raise a VLM inspector's recall. The literature suggests the second is a coin flip at best: MMAD found that adding an abnormal in-context image barely moved accuracy. So pick a category with visible, forgeable defects (MVTec **hazelnut** is the best fit), gate the project at hour 2 on forge realism, and plan the headline so it survives a null recall result.

### Cited Findings
- Muse Image `/v1/images/edits` takes 1–10 input images, but it has **no mask, no `input_fidelity`, and no seed** (all return 400). `size` only sets the aspect ratio, and returned dimensions "won't match the numbers exactly." The only preservation claim is that the model "changes only what you ask for while keeping the rest intact." No latency figure is published. — [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
- Pricing is $0.01 per image, and failed or filtered images are free. Muse Image is limited to 150 RPM, Spark Standard to 3,000 RPM, and SAM 3.1 to 3,000 RPM at $2.50 per 1,000 images. — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits) (via local brief)
- On Meta-relayed Arena numbers, Muse Image ranks #2 in single-image editing (1405 vs GPT Image 2 at 1466; Nano Banana 2 at 1387). — [DataCamp](https://www.datacamp.com/blog/meta-muse-image)
- In MMAD (ICLR 2025), the best model, GPT-4o, reaches only **68.63%** on anomaly discrimination (the mean of normal and abnormal accuracy). Adding an abnormal image in context gave InternVL2-40B **+2.6 pts** on anomaly discrimination (63.84→66.47) and **−0.35 pts** on average. — [MMAD](https://arxiv.org/html/2410.09453v3)
- AnomalyAgent (Apr 2026) is an MLLM agent with five tools (prompt generation, image generation, quality evaluation, knowledge retrieval, mask generation) that loops until quality passes. It reports MVTec IS 2.10 / IC-L 0.33 and 57.0% downstream classification accuracy, against 52.6% for the best zero-shot baseline and **44.7% for Gemini 3.1 Flash Image Preview used as a general editor**. — [AnomalyAgent](https://arxiv.org/html/2604.07900v1)

### Inferences
**Expected numbers. All are inferred estimates, to be confirmed by the hour-2 tests.**

| Quantity | Expected | Basis |
|---|---|---|
| Muse Image edit latency | 10–60 s per edit at `reasoning_strength=low` with tools off; longer at high with search on | No published figure; "high" does multiple passes and tools add lookups (docs) |
| Critic acceptance of forged samples | 30–70% for holes, cracks, stains and print; under 30% for hairline scratches and geometric "bent" defects | "Uncanny" and "fake texture" reports; GPT-4o-class editors drift outside the edit region |
| Total API spend | ~$5 to forge (~360 Image calls with retries), ~$2 for the critic, ~$10–20 for the eval | Pricing above; ~1,300–1,500 tokens per ~1280 px image |
| SAM 3.1 box-prompt IoU on real defects | 0.5–0.8 median for holes and cracks; under 0.4 for thin scratches | SAM Era and the SAM 3 small-object findings (see the SAM section) |
| Spark 1.3 zero-shot balanced accuracy, one MVTec category | 70–90% | GPT-4o 68.6 (MMAD, 2024); Gemini 3.x Flash ~89–91 on DS-MVTec (2026 thesis repo) |
| Change from 8 forged in-context examples | −3 to +10 pts balanced accuracy; recall +0 to +15 pts, often with lower specificity | MMAD in-context ablation; no published study of in-context gains from synthetic examples |
| P(clean "recall X→Y" headline: ≥10-pt recall gain, ≤5-pt specificity loss, significant) | ~35–50% | Above |
| P(convincing forged grid for ≥1 defect type) | ~65–75% | Arena #2 on editing, offset by uncanny-valley reports |
| P(submission with ≥2 defensible numbers, using the fallbacks below) | ~85% | Fallbacks rely only on SAM and human judges |

**Biggest technical risks, in order:**
1. **Forge realism and drift.** The model may re-render the whole crop (color or texture shift), add an "AI-looking" defect, or ignore the requested scale. Without a mask the only levers are the crop and the prompt. Mitigations: crop tightly, align (phase correlation or ECC), color-match, threshold the diff, keep the largest connected component, feather-paste **only the diff region**, and disable search and shell for batch runs.
2. **Inspector shows no gain, or loses specificity.** The MMAD in-context result is ~0. Strong current VLMs may also sit near the ceiling (~90% balanced accuracy), which leaves no headroom.
3. **Circular evaluation.** Spark is both critic and inspector, and SAM masks are scored against diff masks from the same pipeline. Judges with ML backgrounds will spot this, so use human blind tests and real ground-truth masks.
4. **SAM on tiny defects.** Box prompts help, but thin scratches are weak.
5. **Unknown Muse Image latency, the 150 RPM limit, and possible safety-filter false positives on words like "crack" or "damage".** All are manageable with a batch queue and a cache.
6. **MVTec's non-commercial license.** Fine for hackathon evaluation if you don't redistribute the images (inferred; not legal advice). VisA is CC BY 4.0, which is cleaner.

**First 2 hours (two people in parallel), with pass/kill criteria:**

| Time | Person A (forge) | Person B (labels and eval) |
|---|---|---|
| 0:00–0:30 | **T1 API smoke test.** Download MVTec hazelnut (588 MB). Make one `/v1/images/edits` call on a 512 px crop of a *train/good* image. Grid: `reasoning_strength` low vs high, tools on vs off. Log latency, returned size and drift outside the target area (mean absolute difference after resize and alignment). **Pass:** latency under ~60 s at low, and the diff isolates a compact region. | **T3 SAM test.** Box-prompt SAM 3.1 with GT bounding boxes on 10 real hazelnut test defects, and measure IoU against the GT masks. Run the concept prompt "hazelnut" for the part mask. **Pass:** median IoU ≥ 0.5 and the part mask is clean. |
| 0:30–1:15 | **T2 forge-quality test.** 3 types (hole, crack, print/stain) × 5 samples × 2 prompt styles: (a) plain text with the location described; (b) a red-outline visual marker on the crop plus "paint the defect inside the red outline and remove the outline". Also try one whole-image edit as a control. Feather-paste the results. | **T4 inspector headroom test.** 20 test images (10 good, 10 defective): zero-shot vs **oracle** (4 *real* defect examples in context, held out from the test set). Validate the JSON schema and box parsing on the 0–1000 grid. |
| 1:15–2:00 | Run a blind check: mix 10 forged crops with 10 real defect crops, and B rates them without knowing which is which. **Pass:** ≥2 defect types with ≥3 of 5 rated realistic, and the Spark critic agrees (≥4 of 5). | **Pass:** zero-shot balanced accuracy between 55% and 90%, and the oracle shows ≥ +5 pts recall. **If even real examples don't help**, switch the headline to label quality plus the realism test now, not at hour 20. |
| 2:00 | **Kill or pivot gate.** If no defect type passes T2 even with whole-image edits, drop Defect Forge as the hero and fall back to idea #2 (DemoScribe). | Also take 5 phone photos of store-bought hazelnuts and a steel nut on black paper, and run one forge on them (T5). |

### Gaps
- No published Muse Image latency, max input size or output resolution. These can only be measured (T1).
- No published evaluation of Muse Spark on MVTec AD, VisA or MMAD.
- No public evidence of Muse Image fidelity on small industrial edits such as scratches, rust or dents.

---

## Muse Image edits: what the docs say, and public evidence on small localized edits

### Takeaway
The edits endpoint is a single-shot, prompt-only editor. It accepts up to 10 reference images, has no mask, no seed and no fidelity control, sets only the aspect ratio of the output, and makes a single vendor claim that it keeps the rest of the image intact. Public evidence on fidelity is thin: Meta's own figures (Arena #2 in editing; self-refinement raises the editing win rate from ~44% to ~56%), plus a few reviews that flag "uncanny" or fake-looking textures. Nobody has published Muse Image results on scratches, rust or dents, so the crop-and-paste-back design is necessary, not optional.

### Cited Findings
**Endpoint and parameters** — all from [dev.meta.ai Image generation](https://dev.meta.ai/docs/image-generation.md)
- `POST /v1/images/edits` is single-shot with no conversation state. The OpenAI SDK sends multipart with `image` (one file or a list, or `image[N]`). Raw HTTP can send JSON with an `images` array of 1–10 items, each being exactly one of `image_url` (public URL or base64 data URL) or `file_id`. The SDK can't send the JSON form, so use `requests` or curl for it.
- `model` and `prompt` are required (an over-long prompt returns 400). Other parameters:
  - `n`: 1–10.
  - `size`: `"WxH"`, which sets aspect ratio only, up to 16:1.
  - `response_format`: `b64_json` or `url`.
  - `output_format`: `webp` (default), `png` or `jpeg`.
  - `user`: optional.
- `reasoning_strength` is a **top-level** field. `"high"` (the default) refines over several passes; `"low"` returns after one pass. No other values are defined.
- **`tool_enablement`** is an object with `enable_image_search`, `enable_web_search` and `enable_shell`, all on by default. The SDK passes it via `extra_body`. Disabling tools "can speed up prompts that don't need real-world references."
- `stream: true` returns one `image_edit.completed` event with `b64_json`. Intermediate lookups are never returned.
- **Multi-image references:** inputs "can be fused into one scene," and the example places a subject from one image into another image's setting. The multipart input count is not stated; the JSON array allows 1–10.
- **Preservation:** the only statement is that the model "changes only what you ask for while keeping the rest intact." No fidelity or identity guarantee is given.
- **Sizes:** input size and resolution limits are not stated. Output resolution is not fixed, and returned dimensions "won't match the numbers exactly."
- **Rejected fields:**
  - `mask`, `input_fidelity` and `partial_images` return 400 `unsupported_parameter`.
  - `seed` and any other unknown top-level JSON field return 400.
  - `moderation` returns 400 on `muse-image-1.0`.
  - Other unrecognized multipart fields are silently ignored.
- **Errors:**
  - 400 `content_policy_violation` for safety blocks.
  - 503 is retryable ("retry with backoff").
  - 500 is not retryable.
  - 415 for a JSON body with the wrong Content-Type.
- **Response fields:** `background` is always `opaque`, and `usage` tokens are informational only, since billing is per image.
- **Latency:** no numbers. The docs say only that `low` and disabling tools are faster.

**Meta's claims**
- "Muse Image edits images with precision, changing exactly what the user asks for." Self-refinement can apply "a local edit to the current image draft when a small detail is off" or regenerate the whole image. This self-refinement behavior "emerged during RL training." The model holds No. 2 on Arena for text-to-image, single-image editing and multi-image editing (Elo values appear only in charts dated July 5 2026). — [Meta AI blog](https://ai.meta.com/blog/introducing-muse-image-muse-video-msl/)
- Meta's self-refinement ablation raised single-image edit win rates from 43.7% to 56.3%, and multi-image from 43.4% to 56.6% (Meta numbers). — [eesel review](https://www.eesel.ai/blog/meta-muse-image-review)

**Independent and third-party evidence**
- Arena scores relayed from Meta's internal comparisons:

  | Model | Text-to-image | Single-image edit | Multi-image edit |
  |---|---|---|---|
  | GPT Image 2 | 1385 | 1466 | 1454 |
  | Muse Image | 1280 | 1405 | 1399 |
  | Nano Banana 2 | 1270 | 1387 | 1376 |

  — [DataCamp](https://www.datacamp.com/blog/meta-muse-image)
- In a hands-on kitchen test, the edit "is consistent with the original," but the added croissants looked "decidedly fake," with the wrong size and texture. The reviewer adds that the model "does not yet reliably track a full 'scene state' across many sequential edits," and reports latency spikes at peak load. — [DataCamp](https://www.datacamp.com/blog/meta-muse-image)
- HN tester minimaxir said outputs "more often evoke uncanny valley" and rated the model "a step below" Nano Banana and ChatGPT Images. — [eesel review](https://www.eesel.ai/blog/meta-muse-image-review)
- In the consumer app, users can circle or annotate a region to target an edit. That is a visual-prompt mechanism, and it is not documented for the API. — [eesel review](https://www.eesel.ai/blog/meta-muse-image-review)
- One review is titled "Social-Ready, Not Studio-Ready." — [omidsaffari](https://omidsaffari.com/blog/meta-muse-image-review)
- Analogous evidence: GPT-4o "may fail to retain image details outside the intended edit region" in some cases. — [Empirical study of GPT-4o image generation](https://arxiv.org/html/2504.05979v2)

### Inferences
- Treat each edit as a re-render of the crop. Resize the output back to the crop size, align it, color-match it, compute the diff, and paste back only the changed component. Then the rest of the photo is pixel-identical by construction, whatever the model did.
- Region control has to come from the crop (put the defect location at the crop center and say so in the prompt), or from a visual marker drawn on the input, as the consumer app's circle-to-edit suggests. A second reference image showing a target region is also worth one test. All three are untested on the API, so T2 must test them.
- Because the label comes from the diff, the label stays correct even if the model paints the defect slightly off-target. The risks are realism and scale, not label correctness.
- For the batch, set tools off and `reasoning_strength=low` for speed. For the single live hero shot, use `/v1/responses` with search on so the reasoning summary is visible (the plan's idea).

### Gaps
- No measured latency, max input resolution, or output pixel size.
- No public examples of Muse Image adding scratches, rust, dents or other industrial defects. No X or Reddit posts on this were found.
- No independent (non-Meta) editing benchmark with numbers.

---

## Prior art in synthetic defect and anomaly generation, including general-purpose editors

### Takeaway
There are two lines of prior work. Crude self-supervised synthesis (CutPaste, DRAEM, NSA, RealNet) trains dedicated detectors and doesn't need realism. Few-shot diffusion generators (AnomalyDiffusion, DualAnoDiff, AnoGen, DefectFill) need roughly 1/3 of the real defects (about 8 images per category) and train a LoRA per defect type. **Defect Forge is zero-real-defect**, which puts it in the newer zero-shot line (training-free diffusion, AnomalyAgent, UniDG). General-purpose editors (Gemini 3.x Image, Nano Banana Pro) have now been benchmarked as baselines. They work but trail specialist methods (AnomalyAgent: 44.7% vs 57.0% downstream accuracy), especially on rare defects. No paper uses a Meta model, and none measures *VLM in-context* gains from synthetic examples. Both points are novel framing for the pitch.

### Cited Findings
- **DualAnoDiff (CVPR 2025) vs AnomalyDiffusion and others, MVTec AD averages.**

  Generation quality:

  | Method | IS | IC-LPIPS |
  |---|---|---|
  | Crop-Paste | 1.51 | 0.14 |
  | DFMGAN | 1.72 | 0.20 |
  | AnomalyDiffusion | 1.80 | 0.32 |
  | DualAnoDiff | 1.93 | 0.38 |

  Downstream localization (AUC-P / AP-P / F1-P / AP-I):

  | Method | AUC-P | AP-P | F1-P | AP-I |
  |---|---|---|---|---|
  | DRAEM | 92.2 | 54.1 | 53.1 | 97.0 |
  | DFMGAN | 90.0 | 62.7 | 62.1 | 94.8 |
  | AnomalyDiffusion | 99.1 | 81.4 | 76.3 | 99.7 |
  | DualAnoDiff | 99.1 | 84.5 | 78.8 | 98.9 |

  Anomaly-type classification accuracy: Crop-Paste 40.55, DFMGAN 49.61, AnomalyDiffusion 66.09, DualAnoDiff 79.67. **Protocol:** 1/3 of the real anomalies are used for training, on average 8 images per category, with one LoRA per anomaly type trained for 5,000 epochs. — [DualAnoDiff](https://arxiv.org/html/2408.13509v3)
- **UniDG (Apr 2026)** is a universal defect-generation foundation model trained on a 300K-sample dataset.
  - In its single-class downstream table, AnomalyDiffusion reaches 97.9 AUROC-I and 98.9 AP-I, InsertAnything (a general insertion model fine-tuned on their data) 95.3 / 95.5, and UniDG-RFT 98.4 / 99.0. AnyDoor collapses to 80.3 AUROC-I and 18.1 AP-P.
  - Its MLLM-judged quality scores (Gemini-3 Pro and GPT-5.1 as judges) range from 3.55 to 4.24 out of 5.
  - It says "even the most advanced Gemini-3-Pro-Image remains limited performance in rare defects," and shows UniDG with "stronger fidelity and reference adherence than nano-banana-pro on rare defect cases." That comparison is qualitative only.
  — [UniDG](https://arxiv.org/html/2604.08915v1)
- **AnomalyAgent (Apr 2026)** is the closest prior art to Defect Forge. It is an MLLM agent (Qwen3-VL-4B-Thinking) whose tools are prompt generation, image generation, quality evaluation, knowledge retrieval and mask generation. It trains with SFT and then GRPO, using an LLM-as-judge realism reward. On MVTec AD it reports IS 2.10 / IC-L 0.33, 57.0% ResNet34 classification accuracy (vs 52.6% for AnoHybrid and **44.7% for Gemini 3.1 Flash Image Preview**), and 99.3% / 74.2% image / pixel AP. The fetch summary also notes that the agent "uses commercial Gemini models for PG, QE, and IG," so its reproducibility depends on those APIs. — [AnomalyAgent](https://arxiv.org/html/2604.07900v1)
- Other training-free and zero-shot generators:
  - TF-IDG (ICCV 2025) does one-shot, training-free defect generation, with texture preservation from defect-free images. — [TF-IDG](https://openaccess.thecvf.com/content/ICCV2025/papers/Xu_Training-Free_Industrial_Defect_Generation_with_Diffusion_Models_ICCV_2025_paper.pdf)
  - AAG needs no anomaly samples and no defect types (Stable Diffusion). — [AAG](https://arxiv.org/pdf/2508.11550)
  - CORE (Oct 2026) optimizes anomaly-synthesis prompts with an LMM, training-free. — [CORE](https://www.alphaxiv.org/abs/2610.19610)
- One-to-More (Mar 2026) uses nano-banana only to generate masks for real-world scenes, not to synthesize defects. — [One-to-More](https://arxiv.org/pdf/2603.18093)
- A segmentation-driven editing method for bolt-defect augmentation exists, combining segmentation with editing for detection. Only its title and abstract were seen. — [arXiv 2508.10509](https://arxiv.org/pdf/2508.10509)
- On detectability, most AI-image detectors exceed 95% accuracy on whole GPT-4o-generated images. — [GPT-ImgEval](https://arxiv.org/abs/2504.02782)

### Inferences
- The defensible positioning is "zero real defects, spec-driven, fully Meta-native, labels free," not "better than DualAnoDiff." Specialist few-shot methods see real defects, and Defect Forge does not.
- AnomalyAgent validates both the agent-plus-critic loop and the use of a general editor. It is also the paper a knowledgeable judge might cite, so name it in the README as related work. The difference to stress: AnomalyAgent trains an RL policy, while Defect Forge needs no training and adds SAM labeling and an inspector eval.
- Expect general-editor forges to be **plausible but less faithful on rare or fine defects**, so favor coarse, visible defect types (holes, cracks, stains, print).
- IS and IC-LPIPS, the community metrics, need Inception and AlexNet networks. Using them offline for analysis probably doesn't break the runtime rule, but it muddies the "Meta-only" story (inferred). Prefer human and Spark-judged realism.

### Gaps
- CutPaste, NSA and RealNet headline numbers were not re-fetched this session. From memory, unverified: CutPaste ~96 image AUROC, DRAEM ~98.0 image AUROC / 68.4 pixel AP as a detector, NSA ~97 image AUROC, RealNet ~99.6 image AUROC. These detector-training methods don't address realism.
- The DefectFill and AnoGen papers were not retrieved (one guessed arXiv ID was wrong). No numbers for them.
- AnomalyAgent's full baseline table (e.g., GPT-4o image baselines and VisA numbers) was only partly read. The 44.7% Gemini figure comes from the fetch summary.
- No study found uses GPT-image, Gemini or FLUX Kontext edits to train a defect detector, beyond the baseline rows above.

---

## VLM-as-inspector baselines, and whether in-context defect examples raise recall

### Takeaway
Frontier VLMs reached ~68% anomaly-discrimination accuracy on MMAD in 2024 (GPT-4o, Gemini 1.5 Pro), well below expert humans (95%). 2026 Flash-class models reach ~89–91% balanced accuracy zero-shot on a small DS-MVTec subset. The key predictor for the headline is MMAD's ablation: a template *normal* image helps a few strong models by +3–5 pts, while adding an *abnormal* in-context example gave +2.6 pts on discrimination but −0.35 on average. Text domain knowledge (RAG) helped defect *classification* by +17–20 pts but discrimination by only −1.6 to +5.6. **Expect a small recall gain at best.** Design the eval so the forged examples' contribution shows up in defect-type naming and localization as well as recall.

### Cited Findings
- **MMAD (ICLR 2025):** 39,672 questions over 8,366 images from 38 classes.

  Anomaly discrimination (AD) and average (1-shot with a template):

  | Model | AD | Avg |
  |---|---|---|
  | GPT-4o | 68.63 | 74.92 |
  | Gemini-1.5-pro | 68.63 | 73.09 |
  | InternVL2-76B | 68.25 | 70.75 |
  | GPT-4o-mini | 64.33 | 66.29 |
  | Claude-3.5-sonnet | 60.14 | 68.36 |
  | Gemini-1.5-flash | 58.58 | 68.90 |
  | AnomalyGPT | 65.57 | 36.52 |
  | Human expert | 95.24 | 86.65 |
  | Human ordinary | 86.90 | 78.69 |

  — [MMAD](https://arxiv.org/html/2410.09453v3)
- **MMAD, 0-shot vs 1-shot+ (most similar normal image as a template), AD:**
  - Gemini-1.5-flash: 58.43→62.22 (+3.79)
  - InternVL2-76B: 64.30→69.23 (+4.93)
  - LLaVA-NeXT-34B: 60.25→56.80 (−3.45)

  "Most models fail to use template information." — [MMAD](https://arxiv.org/html/2410.09453v3)
- **MMAD, InternVL2-40B:**

  | Setting | AD | Avg |
  |---|---|---|
  | 1-shot | 63.84 | 69.67 |
  | 1-shot+ | 67.81 | 71.66 |
  | 2-shot | 63.75 | 69.66 |
  | In-context with an abnormal image added | 66.47 | 69.32 |

  On InternVL2-76B, gains from more normal images are small up to ~4 shots, and some subtasks decline beyond 8, which the authors attribute to information overload. — [MMAD](https://arxiv.org/html/2410.09453v3)
- **MMAD RAG (text descriptions of normal parts and anomaly types):** average +5.4 to +6.8 pts; defect classification +16.7 to +20.3; anomaly discrimination −1.6 to +5.6. — [MMAD](https://arxiv.org/html/2410.09453v3)
- **MMAD case studies:** minor defects on complex objects are often missed, and every model scores higher on object questions than on defect questions. — [MMAD](https://arxiv.org/html/2410.09453v3)
- **2026 zero-shot balanced accuracy on DS-MVTec / VisA** (same harness; 90 DS-MVTec and 47 VisA images per the search summary):

  | Model | DS-MVTec | VisA |
  |---|---|---|
  | Gemini 3.6 Flash (low thinking) | 90.60 | 82.01 |
  | Gemini 3.5 Flash | 89.28 | 76.44 |
  | Gemini 3.8 Flash | 89.52 | 79.66 |
  | Gemini 2.5 Flash | 81.52 | 75.18 |
  | GPT-5-mini (low) | 77.10 | 68.23 |
  | Qwen3-VL-8B base | 78.68 | 64.45 |

  This is a single thesis repo, not peer reviewed. The README reports full set sizes of n=1670 and n=2141, which conflicts with the 90/47 subset. It has no few-shot results. — [IAD-VLMS repo](https://github.com/Apcin/IAD-VLMS)
- IndusAgent reports zero-shot **anomaly recall** for GPT-4.1 of 81.9 on MVTec and 69.1 on VisA. This comes from a search snippet and was not verified. — [IndusAgent](https://arxiv.org/pdf/2605.20682)
- Fine-tuned in-context systems exist, such as AnomalyGPT (1/2/4/8-shot with a normal-feature memory) and IADGPT (in-context learning). — [AnomalyGPT](https://ojs.aaai.org/index.php/AAAI/article/download/27963/27945); [IADGPT](https://arxiv.org/pdf/2508.10681)
- Muse Spark 1.3 accepts up to 50 images per request, at ~1,300–1,500 tokens for a ~1280 px image, and grounds boxes on a 0–1000 grid (clamp it, since 1001 can occur). — [dev.meta.ai Image understanding](https://dev.meta.ai/docs/image-understanding.md) (via local brief)

### Inferences
- MMAD's tests used single examples on 2024 models. A 2026 frontier model given 8 labeled forged examples **plus a text taxonomy** might gain more, but no published evidence supports a large recall jump. Plan for +0 to +10 pts.
- In-context defect examples tend to make a model more willing to call "defect," which raises recall and lowers specificity. Always report both, plus balanced accuracy.
- Choose a category where zero-shot is neither at the ceiling (≥90%) nor at the floor. Hazelnut holes and prints may be too easy; cracks and cuts are subtler. Running T4 on 20 images in hour 1 decides this.
- Forged examples are most likely to help with **defect-type naming and box localization** (the RAG finding: classification +17–20 pts). Measure per-type recall and the box hit rate, not only defect yes/no.
- Include a "+2 good references only" control so any gain can be credited to forged *defects*, not just to having more images in the prompt.

### Gaps
- No results for Muse Spark (any version) on MMAD, MVTec AD or VisA.
- No paper measures in-context gains from *synthetic* defect examples for a VLM inspector. This is genuinely untested, and novel if it works.

---

## Datasets: licenses, sizes, fastest subsets, and the best forgeable category

### Takeaway
**MVTec AD** is CC BY-NC-SA 4.0 (non-commercial), 4.9 GB in total, and downloadable per category (hazelnut 588 MB, metal_nut 157 MB, screw 186 MB, capsule 385 MB, bottle 148 MB, pill 262 MB). **VisA** is CC BY 4.0, a single ~1.8 GB archive with 100 anomalous images per category. MVTec AD 2 (~30 GB) and Real-IAD (~151K images, non-commercial) are too heavy for one day. **Recommended primary category: MVTec AD hazelnut.** Its defects (crack, cut, hole, print) are visible, local and forgeable; the images are top-down on a plain dark background; and you can buy hazelnuts and damage them at home. **License-clean alternative: VisA cashew or capsules.**

### Cited Findings
- MVTec AD: "released under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License … it is not allowed to use the dataset for commercial purposes." Contact MVTec if unsure. It has over 5,000 high-resolution images in 15 categories. — [MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad)
- MVTec AD size: ~4.9 GB in total. Per category: metal_nut 157 MB, screw 186 MB, hazelnut 588 MB, capsule 385 MB, bottle 148 MB, pill 262 MB, tile 335 MB, cable 481 MB. — [MVTec AD downloads](https://www.mvtec.com/company/research/datasets/mvtec-ad/downloads)
- VisA: "The data is released under the CC BY 4.0 license." It has 10,821 images (9,621 normal, 1,200 anomalous) in 12 categories with 100 anomalous each (PCB1–4, capsules, candles, macaroni1/2, cashew, chewing gum, fryum, pipe fryum). Single tarball: `VisA_20220922.tar` on S3. — [amazon-science/spot-diff](https://github.com/amazon-science/spot-diff). Conflict: anomalib's docs list VisA as CC BY-NC-SA 4.0. — [anomalib VisA](https://anomalib.readthedocs.io/en/v1/markdown/guides/reference/data/image/visa.html)
- VisA archive size: 1.78 GB, from a mirror listing. — [hyper.ai](https://hyper.ai/en/datasets/31525)
- MVTec AD 2 is about 30.4 GB, from a search summary of the MVTec download page. — [MVTec AD 2 downloads](https://www.mvtec.com/company/research/datasets/mvtec-ad-2/downloads)
- Real-IAD has ~150K images (151,050) in 30 categories, multi-view. A Hugging Face repackaging card gives the upstream license as CC BY-NC-SA 4.0. — [Real-IAD paper](https://arxiv.org/pdf/2403.12580); [HF card](https://huggingface.co/datasets/AI4Manufacturing/192-single) (it is unclear whether this card covers all of Real-IAD)

### Inferences
- **Public-repo use (inferred, not legal advice):**
  - A hackathon evaluation reads as research or non-commercial use. Ship a download script, not the MVTec images, and cite the paper.
  - Showing a few MVTec images in the video with attribution is ordinary academic practice, but NC-SA is ambiguous for a prize competition.
  - VisA's CC BY 4.0 (per Amazon's own README) allows redistribution with attribution.
- **Category fit for forging:**

  | Category | Fit | Why |
  |---|---|---|
  | **MVTec hazelnut** | Best | Holes, cracks, cuts and "print" are all local, high-contrast edits; single object on a dark background. |
  | MVTec bottle | Good | Contamination and broken rim from a top view; smallest download (148 MB). |
  | MVTec metal_nut | Partial | "Color" and "scratch" are forgeable. "Flip" is a global pose change and "bent" is a geometric change, neither of which a local paste can fake. Restrict the eval to color and scratch if you use it. |
  | MVTec screw | Weak | Thread and neck defects are tiny on a small object; hard both to forge and to inspect. |
  | VisA cashew, capsules | Good | License-clean. Capsules and macaroni have multiple instances per image, which complicates boxes. |
  | VisA PCB1–4 | Weak | Fine detail, and hard to forge believably. |

- Test-split sizes, from memory of the MVTec AD paper (unverified, so check after download): hazelnut test is about 40 good + 70 defective (crack ~18, cut ~17, hole ~18, print ~17), with ~391 good training images. Metal_nut is about 22 good + 93 defective, with ~220 good training images.

### Gaps
- The full MVTec Terms & Conditions page on redistribution was not read.
- Real-IAD and MVTec AD 2 licenses were not confirmed from primary pages.
- The VisA license conflict (Amazon README vs anomalib) is unresolved. Amazon's own README is the stronger source.

---

## SAM 3 / SAM 3.1 on industrial defects

### Takeaway
No published benchmark tests SAM 3 or SAM 3.1 *box prompts* on small industrial defects. Earlier SAM versions did reasonably on small and slender defects only with manual prompt selection, and they are generally poor zero-shot in the defect domain. SAM 3 is weak on tiny objects in text mode, and visual prompts help. **Use box prompts only (never a concept prompt like "scratch"), treat the diff mask as the primary forged label, and let SAM refine it.** Measure SAM against real MVTec ground-truth masks to get a non-circular number.

### Cited Findings
- SAM Era (2024, original SAM): it handles small and slender defects reasonably zero-shot only "under the selection strategy with manual intervention." It otherwise lacks zero-shot generalization to defects and is not the best performer in that framework. — [SAM Era](https://www.sciencedirect.com/org/science/article/pii/S1546221824003394)
- DefectSAM: SAM's performance in industrial defect detection "is relatively poor," which motivates few-shot fine-tuning. — [DefectSAM](https://www.researchgate.net/publication/389619228_DefectSAM_Prototype_Prompt_Guided_SAM_for_Few-Shot_Defect_Segmentation)
- SAM 3 on remote sensing (2026): small vehicles reach only 6.76 mAP zero-shot in text mode, attributed to resolution and feature-space limits. Adding visual prompts improves results. — [SAM 3 remote-sensing evaluation](https://arxiv.org/pdf/2607.09583)
- SAM 3 reports 48.8 zero-shot mask AP on LVIS (general concepts, not defects). — [SAM 3 paper](https://arxiv.org/html/2511.16719v1) (via search summary)
- Roboflow presents SAM 3 (text, point, box and mask prompts) as promising for defect detection but gives no industrial numbers. Its docs note that generic SAM auto-labeling "cannot distinguish different kinds of cracks." — [Roboflow blog](https://roboflow.com/blog/defect-detection-algorithms-for-manufacturing); [Roboflow docs via plan](https://docs.roboflow.com/datasets/ko/annotate/annotate/ai-labeling/auto-label.md)
- Hosted SAM 3.1:
  - Box and point prompts, up to 16 objects.
  - Coordinates in media pixels after EXIF rotation (a mismatched aspect ratio returns 400).
  - `mask_encoding` is lossless or one_bit, and `include_confidence` is available.
  - Zero matches return empty output, and results "can vary slightly run to run."
  - Price: $2.50 per 1,000 images.

  — [dev.meta.ai SAM overview](https://dev.meta.ai/docs/sam/overview.md) (via local brief)

### Inferences
- For forged samples, the diff mask *is* the ground truth. SAM 3.1 adds value by snapping to defect boundaries when the diff is noisy (paste seams, color drift), and as the step that labels *real* photos from Spark's boxes in the live demo.
- For tiny defects, pad the box by 20–50%, crop and upsample before prompting SAM, and fall back to the diff mask when SAM's IoU against it is below ~0.3. This is untested and should be checked in T3.
- On metal parts, SAM may segment the whole specular facet instead of the scratch. Use a negative point on the clean surface.

### Gaps
- No quantitative SAM 3 or 3.1 results on MVTec AD, VisA or steel-defect sets were found. T3 produces the first number.

---

## Strong fallback headline metrics if in-context recall doesn't improve

### Takeaway
Three numbers are cheap, non-circular and judge-legible:
1. **SAM 3.1 box-prompt mask IoU against real MVTec ground-truth masks.**
2. **A blind human realism test** (fool rate, or two-alternative forced-choice accuracy against 50% chance).
3. **Cost and time per labeled sample against manual masking.**

A fourth, **inspector localization and type accuracy**, may improve even when yes/no recall doesn't.

### Cited Findings
- MMAD shows that adding knowledge mostly lifts *classification* (+17–20 pts) rather than *discrimination* — [MMAD](https://arxiv.org/html/2410.09453v3)
- Published anomaly-generation papers score realism with IS / IC-LPIPS and MLLM judges (UniDG used Gemini-3 Pro and GPT-5.1 for 1–5 ratings) — [UniDG](https://arxiv.org/html/2604.08915v1); [DualAnoDiff](https://arxiv.org/html/2408.13509v3)
- Roboflow's Corning case reports 0.95 mAP from **8 real defect images** plus Cosmos synthetic images, and claims to beat real-only. This is useful framing for "few real defects are the bottleneck" — [Roboflow + NVIDIA](https://roboflow.com/blog/synthetic-data-generation-manufacturing-nvidia)
- Pricing: Muse Image $0.01 per image; SAM $0.0025 per image — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits)

### Inferences
- **Fallback headline options, in order of preference:**
  1. **"Labels to the pixel."** Median SAM 3.1 IoU on N real defects, prompted with ground-truth boxes, plus IoU between SAM masks and diff masks on forged samples. Each forged sample costs about $0.01–0.03 all-in and takes seconds to label, against minutes of manual polygon work.
  2. **"Humans can't tell."** Blind test with 5–10 friends: 20 real versus 20 forged defect crops, shown at random. A fool rate near 50% means the forges are indistinguishable from real defects. Run it with a one-page web form you build yourself, so no non-Meta model is involved.
  3. **"Names and finds the defect."** Defect-type accuracy, and box hit rate (the box center falls inside the ground-truth mask), compared across zero-shot and forged in-context prompting.
  4. **"Critic matters."** Ablation of inspector or human realism scores on critic-accepted versus critic-rejected forges. This adds technical depth.
- Don't headline Spark-as-critic realism scores alone. The same model family judging its own pipeline will look circular.

### Gaps
- I found no sourced figure for manual pixel-mask labeling time per defect. If you quote one, time a teammate labeling 10 masks during the hackathon.

---

## Commercial and hackathon competition (pitch evidence)

### Takeaway
Synthetic defect data is commercially live, which is good pitch evidence. **Roboflow + NVIDIA** (Cosmos and Isaac Sim, June 2026) and **Overview.ai's "Auto Defect Creator"** both need a handful of real defect samples, product geometry, or both. Defect Forge's differentiators are: zero real defects (spec text plus good photos), a fully Meta loop, pixel labels for free, and a VLM inspector that needs no training. I found no public sign of a similar hackathon entry. The earlier scan found ~9 manufacturing entries, none of which generate defect data.

### Cited Findings
- Roboflow (blog May 31 / press release June 1 2026) uses the NVIDIA Defect Image Generation skill, the Cosmos world foundation model and Isaac Sim. It generates "photorealistic, physics-consistent defect images" from product geometry plus a small set of real references. Corning reached 0.95 mAP, with "perfect recall on the hardest defect class," from 8 real defect images plus synthetic images. No baseline numbers are given — [Roboflow](https://roboflow.com/blog/synthetic-data-generation-manufacturing-nvidia)
- Overview.ai describes an Auto Defect Creator that synthesizes photorealistic defect images "from a handful of real samples" — [Overview.ai](https://www.overview.ai/blog/top-10-zero-defect-manufacturing-technologies-2026/)
- Academic competition: AnomalyAgent, UniDG and CORE (see prior art) all target zero-shot or few-shot synthesis — [AnomalyAgent](https://arxiv.org/html/2604.07900v1); [UniDG](https://arxiv.org/html/2604.08915v1)
- Hackathon: "Manufacturing and materials have about nine visible entries, and none appears to generate defect data. Muse Image appears in five descriptions in total" — [local plan](D:\Meta AI hackathon\reports\Meta AI hackathon winning ideas.md). A web search for Devpost or Meta hackathon projects combining Muse Image with defects returned nothing relevant.

### Inferences
- Pitch line: incumbents need either a CAD model or real defects, whereas Defect Forge works from the spec sheet on day one of the line. Positioned that way, it complements Roboflow/NVIDIA rather than duplicating them. The claim is inferred from the two vendor descriptions.
- The "Best Creative Build" bonus ("most original use of Muse Image") fits well, given only ~5 entries mention Muse Image.

### Gaps
- No funding data was found for a 2026 synthetic-defect startup.
- Other likely players (Landing AI, SKY ENGINE AI, Cognex, Instrumental) were not checked this session.
- The hackathon gallery was not enumerated directly.

---

## Live "inspect a real part with a phone or webcam" path, home-photographable parts, and category matching

### Takeaway
Yes, the team can do this with only a phone and laptop. Shoot 5 good photos of a household part on black paper, forge 8 defects on those photos (about 1–3 min with concurrency), then hold up a good part or a **part you damaged yourself** in front of the webcam. Spark returns defect, type and a 0–1000 box, and SAM 3.1 draws the mask. The desk part **doesn't technically need to match** the benchmark category, because the VLM inspector is untrained and each part gets its own forged examples. Matching makes the story stronger, though, so **hazelnuts at home ↔ MVTec hazelnut** is the natural pair. For an "industrial" look, add a steel hex nut or washer, or household screws.

### Cited Findings
- Spark accepts up to 50 images per request, grounds boxes on a 0–1000 grid (clamp values, since 1001 occurs), and ignores images outside the `user` role — [dev.meta.ai Image understanding](https://dev.meta.ai/docs/image-understanding.md) (via local brief)
- SAM 3.1 box coordinates are in media pixels after EXIF rotation, and a mismatched aspect ratio returns 400. This matters for phone photos — [dev.meta.ai SAM overview](https://dev.meta.ai/docs/sam/overview.md) (via local brief)
- Cached input costs $0.15 per M tokens against $1.25 uncached on Spark, so a fixed prefix of examples is cheap to reuse — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits) (via local brief)
- MVTec hazelnut defect types are crack, cut, hole and print. The MVTec categories also include screw, metal_nut, pill and capsule. VisA includes cashew, capsules, candles, macaroni, chewing gum and PCBs — [MVTec AD](https://www.mvtec.com/company/research/datasets/mvtec-ad); [VisA](https://github.com/amazon-science/spot-diff)

### Inferences
**Capture path (all inferred, standard web practice):**
- **Laptop webcam:** use `getUserMedia`, which works on `http://localhost`.
- **Phone:** `getUserMedia` needs HTTPS. Use a Cloudflare or ngrok tunnel, or deploy. The simplest robust option is `<input type="file" accept="image/*" capture="environment">`, which opens the phone camera with no streaming code.
- **Before sending to SAM:** normalize EXIF orientation and resize to ≤1280 px on the long side.
- **Rig:** a fixed phone on a stack of books, matte black paper (to mimic MVTec hazelnut, screw and metal_nut), and diffuse light (a window or a lamp bounced off white paper). Tap-and-hold to lock focus and exposure. Keep the part centered and filling about 60% of the frame.

**Live flow:**
1. Capture 5 good photos.
2. Spark turns the spec text into a taxonomy.
3. Forge 8 examples on those photos in the background.
4. Live frame → Spark inspector, with a cached prefix of the spec, 2 good and 8 forged images.
5. Spark returns JSON with a box; SAM 3.1 box prompt gives the mask; overlay both.

Latency should be a few seconds per inspection at `reasoning.effort=low`. That is unmeasured, and the call costs about 1.5–2¢ uncached or about 0.5¢ with caching.

**Everyday parts, and the real defects you can make at home** (for honest live tests and a tiny real-world test set):

| Household part | Matching category | Home-made real defects |
|---|---|---|
| **Hazelnuts in shell** (grocery store) | MVTec hazelnut | Crack with pliers, poke or drill a hole with a nail, cut with a knife, write on it with a marker ("print"). One-to-one with the MVTec defect types. |
| **Wood or machine screws** | MVTec screw | Scratch the head with sandpaper or a file, crush the thread with pliers. |
| Steel hex nuts or washers (hardware store, IKEA kit spares) | MVTec metal_nut only loosely (MVTec's nut is a specific stamped shape) | Scratch, paint dot or marker "color" stain, file a notch. Rust overnight with salt water and vinegar. |
| Vitamin capsules or pills | MVTec capsule and pill, VisA capsules | Squeeze, scratch with a pin, marker contamination. |
| Cashews, macaroni, chewing gum, candles | VisA (CC BY 4.0) | Break, burn spot, scratch, embedded crumb. |
| Glass bottle rim, top view | MVTec bottle | Marker contamination. Avoid breaking glass. |
| Plastic: LEGO bricks, bottle caps | None (no matching public category) | Scratch, chip with a knife, marker stain. Fine for a demo-only part. |
| Old PCB (router, Arduino) | VisA PCB1–4, loosely | Solder blob, missing component, marker. Hard to forge. |

- **Recommendation:** MVTec hazelnut for the benchmark plus hazelnuts at home for the hero live demo, so the same defect taxonomy covers both. Add one steel nut or washer shot so the video looks industrial. If license cleanliness matters more than visual fit, use VisA cashew with cashews at home.
- A home mini-set of 10 good parts and 10 self-damaged parts under the same rig gives a small *real-world* transfer check that nobody else will have. Report it as counts (e.g., "8 of 10 damaged nuts flagged, 1 of 10 good falsely flagged"), not as a headline percentage.

### Gaps
- Live Spark latency with ~11 images in context is unmeasured.
- Whether Muse Image's safety filter tolerates "crack," "burn" or "rust" prompts is unknown, so test it in T2.

---

## A convincing eval protocol for a 2-person team in about 1 day

### Takeaway
Pre-register a small but paired protocol:
- **One category's full test split** (about 110 images for hazelnut), not 40 images.
- **Four conditions:** zero-shot, plus good references, plus forged defects, plus *real* defects as an upper bound.
- **Metrics:** recall, specificity and balanced accuracy with Wilson CIs, a McNemar test on the paired predictions, per-type recall and box hit rate.
- **Two cheap non-circular side metrics:** SAM IoU on real ground truth, and a human blind realism test.

It costs about $10–20 and takes about 3 h of harness work plus under 1 h of runtime, given Spark's 3,000 RPM.

### Cited Findings
- MMAD reports discrimination as the mean of normal and abnormal accuracy (balanced accuracy). Its 0-shot / 1-shot+ / in-context ablations are the template for these conditions — [MMAD](https://arxiv.org/html/2410.09453v3)
- The 2026 thesis harness scores balanced accuracy strictly, counting unparsed answers as wrong, and runs the same prompt across models — [IAD-VLMS](https://github.com/Apcin/IAD-VLMS)
- DualAnoDiff and AnomalyDiffusion split real anomalies into 1/3 for training and 2/3 for testing. That is the field's precedent for holding out the real defects used as "oracle" examples — [DualAnoDiff](https://arxiv.org/html/2408.13509v3)
- Spark Standard allows 3,000 RPM and Muse Image 150 RPM — [dev.meta.ai Pricing](https://dev.meta.ai/docs/pricing-rate-limits) (via local brief)

### Inferences
**Protocol (inferred design):**
1. **Data hygiene.**
   - Forge only on **train/good** images. Never use a test image as a forge base or an in-context example.
   - For the "real defects" oracle, move 1–2 real defects per type out of the test set and into a separate exemplar pool, and drop them from scoring.
   - Fix the in-context examples once, using a fixed random draw, and log their IDs.
2. **Conditions,** with the same prompt and schema `{defect: bool, type: enum, box_0_1000: [x0,y0,x1,y1] | null, confidence}`, the same `reasoning.effort`, and one query image per call:
   - **C0:** spec and taxonomy text only (zero-shot).
   - **C1:** C0 plus 2 good references. This controls for "more images."
   - **C2:** C1 plus 8 forged defects (2 per type). This is the treatment.
   - **C3:** C1 plus 8 real defects. This is the upper bound, showing how close forged gets to real.
   - *Optional C2r:* C1 plus 8 critic-*rejected* forges. This shows the critic is doing work.
3. **Metrics.**
   - Recall (TPR), specificity (TNR), balanced accuracy and F1.
   - Per-defect-type recall.
   - Box hit rate: the box center is inside the ground-truth mask, or IoU ≥ 0.1 with the ground-truth box.
   - 95% Wilson intervals.
   - **Exact McNemar test C2 vs C1** on paired predictions.
   - Run each condition twice to report stability, since the API isn't deterministic.
4. **Sample size** (arithmetic, inferred).
   - With n≈70 defectives, a recall of 0.7 has a 95% Wilson half-width of about ±10.5 pts. With the plan's 20 defectives it is about ±19 pts, too wide to support a claim.
   - A McNemar split of 13 vs 2 discordant pairs gives a two-sided p≈0.007, so a gain of ~15 pts is detectable on one category.
5. **Cost and time** (inferred).
   - About 110 images × 4 conditions × 2 runs ≈ 880 Spark calls.
   - At ~11 images × ~1.4k tokens ≈ 16k input tokens per call, that is about $18 uncached, or a few dollars with the cached example prefix.
   - The harness takes Person B about 2–3 h. Runtime is under 1 h.
6. **Side metrics.**
   - SAM 3.1 IoU against ground-truth masks on all ~70 real defects (with ground-truth boxes as prompts), binned by defect area.
   - IoU between SAM masks and diff masks on forged samples.
   - Human blind test: 20 real vs 20 forged crops, 5–10 raters, reporting the fool rate.
   - Cost and latency per accepted sample, taken from the provenance log.
   - The home mini-set of 10 good and 10 self-damaged parts, reported as counts.
7. **Pre-register.** Commit `EVAL.md`, which fixes the category, conditions, prompt hash and metrics, *before* running the eval. Report a null or negative C2 result honestly, alongside the C3 upper bound. Judges reward this.
8. **Division of labor:**
   - Person A: forge pipeline, critic and the UI golden path.
   - Person B (CV and labeling background): eval harness, SAM IoU, the blind-test page, home photos and the README tables.

### Gaps
- There is no external precedent for the C2 condition (synthetic in-context examples for a VLM), so its effect size can't be predicted from the literature.
- The exact MVTec hazelnut split counts should be confirmed after download.
