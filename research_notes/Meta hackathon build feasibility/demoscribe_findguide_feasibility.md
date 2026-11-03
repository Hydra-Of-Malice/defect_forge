# Build feasibility in about 1 day: DemoScribe and Find-and-Guide (Meta Global AI Developer Hackathon)

Research time: about 18:40–19:30 UTC on Nov 3 2026. About 30.5 hours remain before the deadline (Nov 4 2026, 9:00 PM ET, which is 02:00 UTC Nov 5). Facts I measured directly (HF API calls, file probes, label counts) are cited to the exact URL I queried. Anything marked **[inferred]** is my own reasoning or arithmetic, not a sourced fact.

---

## Q0. Go/no-go summary (synthesis of the questions below)

### Takeaway
**DemoScribe: GO.** The data path is effectively solved. The RoboReward test split ships per-episode H.264 MP4s that SAM 3.1 accepts with no transcoding, plus human-verified 1–5 progress labels and a published leaderboard to compare against, all in about 120 MB for the DROID and Bridge subsets. The main risks are a direct competitor (DemoDoctor), SAM's weakness on grippers, and the unknown precision of Spark's timestamps.
**Find-and-Guide: CONDITIONAL, lean NO-GO for a 1-day build.** No published latency exists for the hosted SAM 3.1 API. Strong shipped prior art exists (Lookout Find mode, Seeing AI "Find My Things"). The rules give no clarity on speech output. A real blind or low-vision tester is unlikely to be found within 24 hours. Go only if the first-2-hours test measures a p90 round trip of 1.5 s or less from a phone **and** a blind or low-vision tester commits for tomorrow.

### Cited Findings
- RoboReward's test split has 2,831 labeled rows with columns `file_name, task, reward, gpt5_mini_check`, and its clips are H.264 (`avc1`) with the `moov` atom at byte 36, which means faststart — [teetone/RoboReward test/metadata.jsonl](https://huggingface.co/datasets/teetone/RoboReward/resolve/main/test/metadata.jsonl) (downloaded and probed by me)
- SAM 3.1 video accepts MP4 or MOV with H.264, H.265 or MPEG-4, but not VP9 or WebM, and recommends `+faststart` — [dev.meta.ai SAM overview, via project notes](https://dev.meta.ai/docs/sam/overview.md)
- DemoDoctor, a hackathon entry created Nov 1 2026, does "Evidence-grounded robot failure investigation powered by Meta SAM 3.1 and Muse Spark Open" — [est4ever/DemoDoctor](https://github.com/est4ever/DemoDoctor)
- The Meta SAM docs give no latency figures and say nothing about live camera use — [dev.meta.ai Segmenting](https://dev.meta.ai/docs/sam/segmenting.md)
- Google Lookout's Find mode (beta since May 2024) "can also tell you the direction and distance to the object" — [Google Lookout help](https://support.google.com/accessibility/android/answer/9031274); [Google GAAD 2024 blog](https://blog.google/company-news/outreach-and-initiatives/accessibility/ai-accessibility-update-gaad-2024/)

### Inferences
- [inferred] DemoScribe's demo can be cached end to end. Its risk is analytical (accuracy numbers), not live latency, which fits the organizer's rule that the video show live Meta calls, with recorded runs only as a fallback.
- [inferred] Find-and-Guide's hero moment depends on an unmeasured network loop and on a tester. Both are external dependencies that can't be fixed by working harder in 30 hours.

### Gaps
- Neither idea has had a live API call made against it yet. All latency and cost figures below are estimates until the first-2-hours tests run.

---

## Q1 (DemoScribe). What is the fastest data path? Which LeRobot, DROID, Bridge and AgiBot sets ship quick-to-download MP4 episodes, and what are their sizes and licenses?

### Takeaway
The fastest path is **RoboReward's `test/droid` and `test/bridge` folders**: 200 per-episode H.264 MP4s, about 120 MB, CC-BY-4.0, already faststart, with labels. All LeRobot v3 datasets checked (droid_100, so100/so101, aloha, libero, droid_1.0.1) use **AV1** video, which SAM 3.1 does not accept, and v3 packs many episodes into one large MP4. Using them means installing ffmpeg with an AV1 decoder and cutting episodes out by timestamp. **ffmpeg and ffprobe are not installed on this machine.**

### Cited Findings
**RoboReward test split (best fit)**
- 2,831 rows in total. Reward counts are 1: 689, 2: 641, 3: 556, 4: 418, 5: 527. The `droid` and `bridge` folders each hold 100 rows, exactly 20 per reward level. `robo_arena` holds 1,000 rows (266/263/174/141/156), but only **158 unique episode IDs**, because file names carry view suffixes such as `_B_left`, `_C_wrist`, `_D_right`, `_E_left`. — [metadata.jsonl](https://huggingface.co/datasets/teetone/RoboReward/resolve/main/test/metadata.jsonl) (my count)
- Sizes: `test/droid` is 100 files, 59.8 MB; `test/bridge` is 100 files, 60.7 MB; `test/robo_arena` is 1,000 files, 666.8 MB. Each clip is about 0.4–1.1 MB. The full dataset is about 27.0 GB, license CC-BY-4.0, not gated. — [HF API tree](https://huggingface.co/api/datasets/teetone/RoboReward/tree/main/test); [dataset card](https://huggingface.co/datasets/teetone/RoboReward)
- The probed DROID and Bridge clips are `avc1` (H.264) with `moov` before `mdat`, i.e. faststart — [droid clip](https://huggingface.co/datasets/teetone/RoboReward/resolve/main/test/droid/droid_originalsplit_train_index_11250.mp4); [bridge clip](https://huggingface.co/datasets/teetone/RoboReward/resolve/main/test/bridge/bridge_originalsplit_test_index_1152.mp4) (byte probe)

**LeRobot v3 sets (all AV1, multi-episode files)**

| Dataset | Episodes / frames / fps | Cameras | Codec | Repo storage | License |
|---|---|---|---|---|---|
| [lerobot/droid_100](https://huggingface.co/datasets/lerobot/droid_100) | 100 / 32,212 / 15 (≈21 s per episode) | 3 at 180×320 | AV1; file-000 for one camera is 174.9 MB, moov not at the front | 931.8 MB | MIT |
| [lerobot/svla_so101_pickplace](https://huggingface.co/datasets/lerobot/svla_so101_pickplace) | 50 / 11,939 / 30 (≈8 s) | 2 at 480×640 | AV1; file-000 for one camera is 40.1 MB | 258.7 MB | Apache-2.0 |
| [lerobot/svla_so100_pickplace](https://huggingface.co/datasets/lerobot/svla_so100_pickplace) | 50 / 19,631 / 30 (≈13 s) | top + wrist at 480×640 | AV1 | 941.4 MB | Apache-2.0 |
| [lerobot/aloha_static_cups_open](https://huggingface.co/datasets/lerobot/aloha_static_cups_open) | 50 / 20,000 / 50 (8 s) | 4 at 480×640 | AV1; file-000 for one camera is 143.7 MB, moov not at the front | 1,975 MB | MIT |
| [lerobot/libero](https://huggingface.co/datasets/lerobot/libero) | 1,693 / 273,465 / 10 (≈16 s) | 2 at 256×256 | AV1 | 1,936 MB | Apache-2.0 |
| [lerobot/droid_1.0.1](https://huggingface.co/datasets/lerobot/droid_1.0.1) | 95,658 / 27.6M / 15 | 3 | AV1 | **824.9 GB** | Apache-2.0 |

  Sources: each dataset's `meta/info.json` and the HF API (`usedStorage`, `cardData.license`), queried by me; codec and faststart from byte probes of `videos/.../file-000.mp4`.
- `lerobot/droid_1.0.1` has per-frame **`is_episode_successful`**, `language_instruction`, `_2` and `_3`, `task_category`, `building` and `collector_id` features. It is the only LeRobot set checked that carries success and failure labels. — [droid_1.0.1 info.json](https://huggingface.co/datasets/lerobot/droid_1.0.1/resolve/main/meta/info.json)
- `lerobot/droid_100` has only `next.reward` and `next.done`, with no success flag or language columns beyond `task_index` — [droid_100 info.json](https://huggingface.co/datasets/lerobot/droid_100/resolve/main/meta/info.json)
- Bridge in LeRobot format, [IPEC-COMMUNITY/bridge_orig_lerobot](https://huggingface.co/datasets/IPEC-COMMUNITY/bridge_orig_lerobot), is LeRobot **v2.0** with **per-episode** MP4 files: 53,192 episodes, 1.89M frames, 5 fps, 256×256, AV1, 21.4 GB, Apache-2.0. — [dataset card](https://huggingface.co/datasets/IPEC-COMMUNITY/bridge_orig_lerobot)
- `lerobot/bridge_orig_lerobot` and `lerobot/so100_pickplace` do not exist under those names (the API returns an error) — HF API (queried by me)

**AgiBot World 2026 (failure- and subtask-annotated)**
- License CC BY-NC-SA 4.0. Total storage is about 17.9 TB. LeRobot v2.1. There is a **~7 GB sample** at `task3777/380098_380609.tar.gz`. — [agibot-world/AgiBotWorld2026](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026)
- `meta/info.json` adds annotation layers. "Task Frame" segments carry a subtask instruction plus `[start, end)` frame indices. There are 2D bounding boxes and key frames of type `Error Frame`, `Success Frame` and `Intervention Frame`, plus a `success_frame_index` field. — [AgiBotWorld2026 README](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026)

### Inferences
- [inferred] **The fastest command is**: `hf download teetone/RoboReward --repo-type dataset --include "test/metadata.jsonl" "test/droid/*" "test/bridge/*"`. That is about 120 MB, likely a few minutes on a normal connection. Add `test/robo_arena/*` (667 MB) for organic (non-synthetic) failures.
- [inferred] **Cost per episode.** A DROID episode is about 322 frames at 15 fps, so one SAM noun-phrase request costs about $0.064. Three object phrases plus one gripper box request come to about $0.26 per episode, or about $0.13 if downsampled to 7.5 fps. 100 episodes cost about $13–26 in SAM, against $150 in credits. Bridge episodes (≈36 frames at 5 fps) fall under the **50-frame minimum** per request, so each request bills as 50 frames ($0.01).
- [inferred] If LeRobot SO-101 or ALOHA footage is wanted for visual variety, install ffmpeg (for example `winget install Gyan.FFmpeg`; full builds include an AV1 decoder, but verify with `ffmpeg -decoders | findstr av1`). Then cut each episode by the `from_timestamp`/`to_timestamp` columns in `meta/episodes/*.parquet` and re-encode with `-c:v libx264 -movflags +faststart`. Budget 30–60 minutes for this.
- [inferred] DROID 1.0.1's success flag is attractive, but each video file is ~500 MB per camera and holds many episodes. Not worth it for a 1-day build when RoboReward already includes DROID clips with labels.
- [inferred] AgiBot's 7 GB sample is the only located source of **human subtask boundaries and error frames**. Its NC-SA license is fine for an Indie demo but a problem for a Startup data product.

### Gaps
- Frame counts and fps of the RoboReward clips were not measured (no ffprobe on the machine). Clip sizes suggest a few hundred frames.
- I did not verify that AV1 decoding works in a given local ffmpeg build, or that PyAV wheels include dav1d.
- The fraction of failure episodes in DROID 1.0.1 was not computed.

---

## Q2 (DemoScribe). Is there an existing human-labeled subset to evaluate against (success/failure or subtasks)?

### Takeaway
**Yes, for success: RoboRewardBench.** It is CC-BY-4.0, has an end-state 1–5 rubric and a public leaderboard, and its card says the test split is human-verified. **For subtask boundaries there is no quick human ground truth in DROID or Bridge.** Options are the AgiBot 2026 sample (human Task Frame segments), SPARC DROID annotations (provenance unclear), or hand-labeling 10–20 episodes. ECoT Bridge features are machine-generated, so they make a silver baseline, not ground truth.

### Cited Findings
- RoboReward pairs "a task instruction with a real-robot rollout video and a discrete end-of-episode progress reward score in {1,…,5}". "The **test split is fully human-verified** and released as **RoboRewardBench**." Negatives for OXE come from **counterfactual relabeling** (a swapped instruction) and **temporal clipping**. RoboArena supplies organic successes and failures. — [RoboReward card](https://huggingface.co/datasets/teetone/RoboReward)
- The paper's rubric: 1 is no success, 2 minimal progress, 3 partial completion, 4 near completion (misses one minor requirement), 5 perfect completion. The paper refers to 2,831 test episodes, and says human annotators checked each test example and discarded failing ones — [arXiv 2601.00675 (HTML)](https://arxiv.org/html/2601.00675v1). **Conflict:** the HF test `metadata.jsonl` still has 2,831 rows, so either nothing was discarded or the HF split is the pre-filter set. Treat the labels as mostly, not certainly, verified.
- DROID 1.0.1 includes per-frame `is_episode_successful` and three language instructions per episode — [droid_1.0.1 info.json](https://huggingface.co/datasets/lerobot/droid_1.0.1/resolve/main/meta/info.json)
- SPARC DROID annotations: 128,136 "interaction subtask" rows across two external views, covering about 98.7–99.3% of 53,282 source episodes. Masks, coordinates and frame indices sit in HDF5 sidecars, and DROID media is not included. The card states no license. Storage is 7.8 GB. — [irl-kit/sparc-droid-annotations](https://huggingface.co/datasets/irl-kit/sparc-droid-annotations)
- ECoT's Bridge features ([Embodied-CoT/embodied_features_bridge](https://huggingface.co/datasets/Embodied-CoT/embodied_features_bridge), MIT, 1.4 GB) come from a scripted pipeline. `full_reasonings.py` calls `gemini-1.5-flash`, `gripper_positions.py` uses OWL-ViT plus `facebook/sam-vit-base`, and `generate_bboxes.py` uses a zero-shot detector — [MichalZawalski/embodied-CoT scripts](https://github.com/MichalZawalski/embodied-CoT/tree/main/scripts/generate_embodied_data)
- AgiBot World 2026 Task Frame entries give subtask `[start, end)` frame ranges plus `Error Frame` and `Success Frame` key frames — [AgiBotWorld2026 README](https://huggingface.co/datasets/agibot-world/AgiBotWorld2026)
- A community SO-101 evaluation in the RoboJev repo has "200 manually labelled clips: 135 have a clear binary outcome … 65 are ambiguous" — [josefchen/robojev](https://github.com/josefchen/robojev)

### Inferences
- [inferred] **Eval design that fits in hours.** (a) Success: run DemoScribe's verdict on the 200 DROID and Bridge clips plus about 50 RoboArena episodes. Report 1–5 MAE, which compares directly to the RoboRewardBench table in Q4, and binary accuracy (5 vs ≤2, with 3–4 excluded or reported separately). (b) Subtasks: hand-label boundaries on 15–20 clips while the batch runs, and report median boundary error in seconds.
- [inferred] RoboReward's DROID and Bridge negatives are partly synthetic (swapped instruction or truncated clip). A "fake success" demo, where the gripper hovers without placing, should draw its examples from RoboArena's organic rows.
- [inferred] LIBERO demos are teleoperated successes, so they contain no failure labels to evaluate against.

### Gaps
- I did not determine whether SPARC's subtask annotations are human or model-generated, or what their license is.
- I did not check how RoboArena's per-view rows map to policies and episodes (letters B–F could be policy IDs).

---

## Q3 (DemoScribe). Prior art and reusable code: which repos give code to adapt, and under what licenses?

### Takeaway
Reuse **LeRobot (Apache-2.0)** for format and export, the **ECoT annotation scripts (MIT)** as the pattern for prompting the gripper once, naming objects and labeling primitives, **meta-sam parsers (SAM License)** for SAM output, and possibly **DemoDoctor (Apache-2.0)** or **RoboJev (Apache-2.0)** for their viewer and frame-extraction ideas. Note that code written before the event is not scored. Grounded-SAM-2 (Apache-2.0) is the canonical "detect then track" robot pipeline, but it is superseded here by SAM 3.1's native concept tracking.

### Cited Findings
- [huggingface/lerobot](https://github.com/huggingface/lerobot): Apache-2.0, ~28.7k stars, pushed Nov 3 2026 — GitHub API
- [MichalZawalski/embodied-CoT](https://github.com/MichalZawalski/embodied-CoT): MIT, 420 stars. `scripts/generate_embodied_data/` has `bounding_boxes/generate_bboxes.py`, `gripper_positions.py` (OWL-ViT box, then SAM mask for the gripper), `primitive_movements.py` (move primitives from proprioception) and `full_reasonings.py` (Gemini 1.5 Flash writes plan, subtask and reasoning) — GitHub API tree and file headers
- [IDEA-Research/Grounded-SAM-2](https://github.com/IDEA-Research/Grounded-SAM-2): Apache-2.0, ~3.8k stars — "Ground and Track Anything in Videos with Grounding DINO, Florence-2 and SAM 2" — GitHub API
- [meta-models/meta-sam](https://github.com/meta-models/meta-sam): "Client libraries for SAM 3.1 streaming segmentation … parser, graphics, video, and React for TypeScript; parser for Python". The LICENSE file is the "SAM License, Last Updated: November 19, 2025". It ships conformance cases, including `compact-api-video-frame-order.json` — GitHub API
- [facebookresearch/sam3](https://github.com/facebookresearch/sam3): ~12.2k stars; GitHub reports the license as NOASSERTION (custom) — GitHub API
- [meta-models/meta-model-cookbook](https://github.com/meta-models/meta-model-cookbook): MIT, with use cases including `10_perception_grounding` and `03_visionclaw` — GitHub API tree
- [est4ever/DemoDoctor](https://github.com/est4ever/DemoDoctor): Apache-2.0, React + FastAPI, SAM 3.1 plus Muse Spark Open via Fireworks. Its claims: "Six bundled replays", "One completed unfamiliar-video run" on a private DROID recording, multi-camera "mock-tested", and "**no validated generalized failure-detection accuracy**" — README
- [josefchen/robojev](https://github.com/josefchen/robojev) (Apache-2.0, created Oct 24 2026): a 27B success-probability model with a "Python client, dataset grader, video overlay, and LeRobot plugin". It "parse[s] ten frames/episode via HTTP byte ranges" and supports LeRobot v3 metadata — README
- [LongXinKou/RoboannotatorX](https://github.com/LongXinKou/RoboannotatorX) (ICCV 2025): no license file, 6 stars — GitHub search; [clvrai/sprint](https://github.com/clvrai/sprint) (SPRINT language relabeling): no license file — GitHub API

### Inferences
- [inferred] Under the runtime rule, ECoT's Gemini, OWL-ViT and SAM-vit calls must all be replaced by Spark 1.3 and SAM 3.1. What carries over is the *structure*: gripper positions to motion primitives to an LLM plan, and the JSON feature schema, which suits an export format.
- [inferred] Without a license file, RoboAnnotatorX and SPRINT code is "all rights reserved". Cite them as prior art and don't copy their code.
- [inferred] The RoboJev byte-range frame-sampling idea (keyframes for the referee without decoding whole files) is worth copying in concept for the LeRobot ingest path.

### Gaps
- I did not search for Gemini Robotics-ER labeling code, AutoRT or DeMiAn code; time-boxed, and none is needed for the build.
- I did not read the cookbook `03_visionclaw` or `10_perception_grounding` recipes in detail.

---

## Q4 (DemoScribe). Known failure modes: is SAM weak on articulated arms or occlusion, how good are VLMs at success detection on robot video, and what eval numbers should we expect?

### Takeaway
**SAM is weak on robots, especially on grippers with concept prompts** (SAM 3 gripper J&F of 10.5). Box prompts are much better (SAM 2.1 gripper box J&F of 67.9). So: never concept-prompt "gripper", box-prompt it once, and track objects by noun phrase. **VLM success grading is mediocre on the 1–5 scale** (frontier MAE 0.69–0.94; Llama 4 Scout 1.49). Binary success on narrow, single-lab data can reach 92–93% balanced accuracy. Realistic DemoScribe targets are a 1–5 MAE of about 0.8–1.0 and binary accuracy of about 80–90% [inferred].

### Cited Findings
- RobotSeg (arXiv 2511.22950) on the VRS video benchmark, J&F:
  - **SAM 2.1 (original)**: arm 28.9 with 1 click, 57.1 with 3 clicks, 50.2 with a box, 61.8 with OI; gripper 47.7, 65.8, **67.9 with a box**, 69.1.
  - **SAM 3 with concept prompts**: arm 45.0, **gripper 10.5**, whole robot 34.7.
  - RobotSeg: about 75–77 on all settings.
  - Stated failure modes: SAM "lacks mechanisms for modeling articulated robot structures, often resulting in incomplete or structurally broken masks". With one click it "confuses the black robot gripper with the similarly colored background". Finetuned SAM 2.1 drops to 38.7 on the MobileALOHA arm, showing embodiment dependence.
  - The paper does not specifically discuss occlusion.
  - — [RobotSeg HTML v2](https://arxiv.org/html/2511.22950v2)
- RoboRewardBench MAE on the 1–5 end-state scale (lower is better):

  | Model | MAE |
  |---|---|
  | RoboReward 8B | 0.665 |
  | GPT-5 mini | 0.691 |
  | GPT-5 | 0.811 |
  | RoboReward 4B | 0.845 |
  | Gemini 3 Pro (Preview) | 0.851 |
  | Qwen3-VL 8B | 0.892 |
  | Gemini 2.5 Pro | 0.902 |
  | Gemini Robotics-ER 1.5 | 0.906 |
  | Gemini 2.5 Flash | 0.943 |
  | **Llama 4 Scout** | **1.485** |

  The abstract adds that "no model excels across tasks". No binary accuracy is reported, and frame count and fps given to models are not specified. — [arXiv 2601.00675 HTML](https://arxiv.org/html/2601.00675v1); [abstract](https://arxiv.org/abs/2601.00675)
- AHA (ICLR 2025): AHA-13B scores 0.702 binary success vs **0.611 for GPT-4o in-context learning** on the AHA test set — [AHA paper](https://arxiv.org/pdf/2410.00371) (figures via a secondary summary; unverified against the table)
- RoboFAC-7B reportedly beats GPT-4o by 34.1% on its failure-VQA benchmark (a relative figure) — [arXiv 2505.12224](https://arxiv.org/pdf/2505.12224v1)
- RoboJev README: on 268 held-out SO-101 runs, frontier models (GPT-6 Astra, GPT-6.1 Sol, Claude Opus 5.5, Claude Sonnet 5.5) got **91.9–93.3% balanced accuracy** from 4 frames, and RoboJev-27B got 95.2%. Final-frame-only input drops to an AUROC of 0.776 on unseen labs. — [josefchen/robojev](https://github.com/josefchen/robojev) (self-reported, not peer-reviewed)
- SuccessVQA (arXiv 2303.07280) frames success detection as VQA with a Flamingo model trained on human reward annotations. It reports that success detection on unseen real videos is harder, and its abstract gives no figures — [arXiv 2303.07280](https://arxiv.org/abs/2303.07280)
- The Meta docs say Spark "reads a video's embedded audio too", but also that "**Audio understanding in Muse Spark 1.3 is currently not fully supported**". They do not state frame sampling, tokens per second or timestamp output — [dev.meta.ai Video understanding](https://dev.meta.ai/docs/video-understanding.md)

### Inferences
- [inferred] **Expected numbers to put in the README.** These are estimates, not measurements.
  - Spark 1.3 alone is likely to land somewhere around 0.8–1.0 MAE on the 200 DROID and Bridge RoboReward clips. Spark is a newer frontier-class model than Llama 4 Scout, but its robot-reward ability is unpublished.
  - The geometry-plus-referee pass should be presented as **reducing false successes**. Report precision on label 5 and the confusion between labels 4 and 5, not just MAE.
  - Binary success (5 vs 1–2) is likely to reach about 80–90%.
  - Even beating GPT-5 mini (0.691) on the same clips would be a headline result. Matching Gemini Robotics-ER 1.5 (0.906) is a credible "zero training" story.
- [inferred] For the gripper, put one box prompt on frame 0 (or the first frame where it's visible) and propagate in both directions. Report gripper-track dropout as a QC flag. Use the wrist camera only for "contact" cues, not for tracking.
- [inferred] The Spark audio caveat is harmless here: robot episodes are usually silent, and RoboReward clips may have no audio track at all.

### Gaps
- No published Muse Spark (any version) result on any robot-reward or success benchmark was found.
- No published accuracy for Spark video timestamps was found. Snap subtask boundaries to geometry events.
- SAM 3.1 (as opposed to SAM 3 or SAM 2.1) has not been benchmarked on robot arms or grippers.

---

## Q5 (DemoScribe). How crowded is robotics in this hackathon?

### Takeaway
It is crowded in "Push the Frontier" robotics (about 14 visible entries in earlier notes), and **one entry directly overlaps: DemoDoctor**. DemoDoctor is single-episode forensic investigation with deliberate abstention and no accuracy claim. DemoScribe's moat would be **batch labeling, export as training data, and a number measured against a public human-verified benchmark**.

### Cited Findings
- Earlier scan: about 14 visible robotics or Push the Frontier repos, including athlete2humanoid, video2urdf and muse-qc-cell — [project notes, event_rules_and_intel.md](https://github.com/PandaGrdn/athlete2humanoid)
- DemoDoctor (created Nov 1 2026, Apache-2.0) does robot-demo failure investigation with SAM 3.1 masks, "deterministic checks", and cited Muse Spark Open explanations. Outcomes such as EP010 stay "Uncertain". It states "no validated generalized failure-detection accuracy" — [est4ever/DemoDoctor](https://github.com/est4ever/DemoDoctor)
- Other recent robotics-annotation repos turned up by GitHub search: [sabdulmajid/batch-inference-robotics](https://github.com/sabdulmajid/batch-inference-robotics) (created Oct 31 2026; "Recorded rollouts → reviewed labels → offline RL", no Meta model mentioned in its README), [rajan12thakur/aura-robotics-data-platform](https://github.com/rajan12thakur/aura-robotics-data-platform) (created Oct 26 2026; a Django and React annotation workspace, no Meta model found), and [josefchen/robojev](https://github.com/josefchen/robojev) (created Oct 24 2026; a non-Meta success model with a LeRobot plugin) — GitHub search

### Inferences
- [inferred] Position DemoScribe as "DemoDoctor answers *what went wrong in this episode*; DemoScribe labels *1,000 episodes* and proves its accuracy on RoboRewardBench." Show the RoboRewardBench MAE next to the published leaderboard rows. No visible competitor does that.
- [inferred] Robotics judges will ask for a number, so the benchmark comparison is the most important deliverable after the export.

### Gaps
- GitHub search matches repo descriptions only, and private repos that go public at submission are invisible. The true count could be higher.

---

## Q6 (Find-and-Guide). Prior art on audio and haptic guidance for reaching objects: what worked, and what are typical times-to-target?

### Takeaway
The category is **shipped and familiar**. Google Lookout's Find mode gives direction and distance. Microsoft's Find My Things in Seeing AI offers teachable personal-object finding with audio, haptic and visual cues. The 2025 Gemma 3n winner used a chest-mounted phone with a blind family member co-designing. Published reach timings: **about 4.2 s from cue to grasp** when the target location is known and a human operator guides, **about 20 s** to locate an object with a head camera, and **about 40 s** of search with sonified glasses, at roughly 82–86% success. One study found speech guidance beat pure sonification by about 35–40%.

### Cited Findings
- **Google Lookout Find mode** (beta, May 2024): users pick one of seven categories (doors, bathrooms, cups, vehicles, seating and tables, and others). It "can also tell you the direction and distance to the object", and users "hold your device, move it slowly" — [Lookout help](https://support.google.com/accessibility/android/answer/9031274); [Google blog, GAAD 2024](https://blog.google/company-news/outreach-and-initiatives/accessibility/ai-accessibility-update-gaad-2024/)
- **Microsoft Find My Things** (ASSETS '23, CHI '24): users record four short videos to teach a personal item, and the app then guides them "with auditory, haptic, and visual cues". It was integrated into Seeing AI in 2024 and co-designed with 8 blind or low-vision young people aged 14–25 — [Microsoft Research story](https://www.microsoft.com/en-us/research/story/find-my-things/); [ASSETS 2023 paper](https://www.microsoft.com/en-us/research/uploads/prod/2023/08/FindMyThings-ASSETS-2023.pdf)
- **Gemma Vision** (1st place, Gemma 3n Impact Challenge): visuals come from "a phone camera strapped to the user's chest". It is triggered by an 8BitDo Micro controller or voice. The developer's blind brother "played a vital role". The 2nd-place entry (Vite Vere) read instructions aloud with the device's TTS — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/)
- **Acoustic touch glasses** (PLoS ONE 2023):
  - 14 participants: 7 blind or low-vision (BLV), 7 blindfolded sighted.
  - Search time was about 40 s (BLV 38.25 ± 5.31 s).
  - Seated pick-up success with the device was 81.66% for BLV and 73.01% for sighted participants, vs 90.71% and 93.78% with a verbal "clock face" baseline. Overall success was 85.53%. The standing task took 1.67 reach attempts.
  - Cue design: repetition rate increases toward the center of view (20 ms per layer, ~100 ms at the edge).
  - — [PLoS ONE 10.1371/journal.pone.0290431](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0290431)
- **Vibrotactile vs auditory grasp guidance** (Scientific Reports 2025):
  - 41 blind or partially sighted participants.
  - Cue-to-grasp time was **4,198 ± 1,691 ms with audio** vs 4,784 ± 2,255 ms with tactile cues. Corner targets took ~1.4 s longer than edge targets.
  - Localization accuracy was 90.6%.
  - An experimenter guided each trial manually from a helmet-camera feed, so no automatic tracking or latency was involved.
  - — [PMC12586706](https://pmc.ncbi.nlm.nih.gov/articles/PMC12586706/)
- With a head-mounted camera and bone-conduction audio or vibration, "subjects were able to locate the correct object within 20 seconds" on average — [IEEE 8512918](https://ieeexplore.ieee.org/document/8512918) (via search snippet)
- In Fiannaca et al.'s Google Glass doorway study (8 blind participants), speech led to faster discovery (39.9%) and guidance (34.5%) than sonification — secondary summary in [arXiv 1506.07272](https://arxiv.org/pdf/1506.07272)
- A Grenoble group proposes Fitts' law as the standard metric for non-visual target reaching, since raw time depends on target size and distance — [HAL hal-04492351](https://hal.univ-grenoble-alpes.fr/hal-04492351)

### Inferences
- [inferred] A realistic eval target is a median time-to-touch under 20 s on a cluttered table, with ≥80% correct-object success, compared against a describe-only baseline. Report it in Fitts'-law terms (an index of difficulty from distance and object size) to look rigorous.
- [inferred] Differentiation from Lookout and Seeing AI has to be **open vocabulary with attributes** ("the chipped mug, not the white one"), done by Spark plus SAM with no teaching step, and **hand-to-object** guidance rather than phone pointing. Both claims must show on screen.
- [inferred] Speech beat sonification in one study, so a speech-free design is a real usability cost, not only a rules workaround. Short `aria-live` phrases spoken by the user's screen reader partly recover it.

### Gaps
- VizLens, Envision, Aira, OrCam and Be My Eyes "find" flows were not researched in depth. No times-to-target were found for them.
- The claim that Netra placed 3rd at the Gemini 3 hackathon could not be verified: Devpost's updates page returned 403, and search found only a Devfolio "NetraSathi" project with no placement.

---

## Q7 (Find-and-Guide). Is there evidence for SAM 3.1 API latency, and is a 1–2 Hz loop from a phone browser plausible?

### Takeaway
**No first-party latency figures exist.** The "≈0.4 s/frame (Reka)" citation could not be re-verified: the page now redirects to tryinfer.com and lists only "$0.01 per image" for SAM 3. A 1 Hz loop is plausible but unproven; 2 Hz is doubtful [inferred]. Note too that one image request per frame has **no tracking memory**: the "lock" is re-detection each frame, not SAM video tracking.

### Cited Findings
- The Meta docs say "Each frame arrives as its own `response.output_text.delta`" for video, "Streaming is not required", and an image returns on a single line. They give no latency, max-resolution or real-time guidance — [dev.meta.ai Segmenting](https://dev.meta.ai/docs/sam/segmenting.md)
- The Reka URL redirects to [tryinfer.com/models/sam-3-1](https://tryinfer.com/models/sam-3-1). That page shows no latency or fps, and prices SAM 3 image-to-bbox at "$0.01 per image"
- Secondary blogs claim per-frame latency fell "from 200ms to under 100ms" with Object Multiplex. These are self-hosted GPU figures, not the hosted API — [blockchain.news](https://blockchain.news/ainews/meta-releases-sam-3-1-with-object-multiplexing-latest-analysis-on-3x-10x-video-segmentation-efficiency-gains); [vucense](https://vucense.com/ai-intelligence/open-source-ai/meta-sam-3-1-release-video-segmentation-local-ai/)
- Project notes:
  - SAM 3.1 images cost $2.50 per 1,000 and the rate limit is 3,000 RPM.
  - Box and point coordinates are in post-EXIF-rotation pixels, and a mismatched aspect ratio returns 400.
  - Spark has a reported OpenRouter P50 of about 1.83 s latency (unverified).
  - — [dev.meta.ai pricing](https://dev.meta.ai/docs/pricing-rate-limits); [aireiter review](https://aireiter.com/blog/muse-spark-1-3-api-pricing-review)

### Inferences
- [inferred] **Latency budget for one guidance tick**:
  - Encode a 640 px JPEG (~40–80 KB) on the phone: 10–30 ms.
  - Upload over Wi-Fi or LTE: 30–150 ms.
  - Backend-to-API round trip plus SAM inference on one image: unknown, guessed at 300–900 ms.
  - Return plus Web Audio update: under 50 ms.
  - Total p50 is roughly 0.5–1.2 s. That gives 1 Hz with one request in flight, or about 2 Hz if 2–3 requests are pipelined, since the rate limit allows it.
  - Cost at 2 Hz is about $0.30 per minute.
- [inferred] Use Spark grounding **only for the first lock**. At about 1.8 s p50 it is too slow for the loop. Seed SAM with a box prompt from the previous bbox (expanded by 20–30%) and associate across frames by IoU on the client. That gives "lock persistence" without video mode.
- [inferred] Chrome on Android `MediaRecorder` produces WebM (VP8/VP9), which SAM rejects. That is why the plan's JPEG-per-frame path is right. Short H.264 MP4 chunks would need server-side transcoding and add seconds.
- [inferred] Guiding the *hand* (rather than the camera) needs the hand's position too: either a second parallel SAM request for "hand", which doubles cost, or a chest-mount geometry assumption (the frame center is in front of the hand).

### Gaps
- No measured hosted SAM 3.1 image latency exists anywhere I could find. This is test #1.

---

## Q8 (Find-and-Guide). Is there reusable code for phone camera → WebSocket, Web Audio cues and accessible screen-reader UIs?

### Takeaway
All the pieces are standard browser APIs, and permissively licensed helpers exist: FastAPI (MIT) WebSockets, aiortc (BSD-3) if WebRTC is wanted, Tone.js (MIT) for sound, and MDN-documented `StereoPannerNode`, `aria-live` and `DeviceOrientationEvent`. No single open repo was found that already combines camera, segmentation and sonified guidance. **iOS gotchas:** HTTPS is required, orientation needs a permission tap, and iOS VoiceOver double-announces when `role="alert"` and `aria-live` are combined.

### Cited Findings
- `StereoPannerNode` pans "left or right" using "a low-cost equal-power panning algorithm". `pan` ranges from −1 to 1, and it has been Baseline-widely-available since April 2021 — [MDN StereoPannerNode](https://developer.mozilla.org/en-US/docs/Web/API/StereoPannerNode)
- `aria-live="polite"`: "The screen reader will speak changes whenever the user is idle". `assertive` is for critical updates and "will interrupt" the current announcement. "Establish the live region before updating its content." `role="alert"` combined with `aria-live` "causes double speaking in VoiceOver on iOS". Behavior "can vary across browser and assistive technology combinations" — [MDN ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions)
- `DeviceOrientationEvent.requestPermission()` "requires transient activation", meaning a button click, and is "available only in secure contexts (HTTPS)" — [MDN requestPermission](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/requestPermission_static)
- [aiortc/aiortc](https://github.com/aiortc/aiortc): BSD-3-Clause, ~5.1k stars, with `webcam` and `server` examples. [Tonejs/Tone.js](https://github.com/Tonejs/Tone.js): MIT, ~14.9k stars. [fastapi/fastapi](https://github.com/fastapi/fastapi): MIT — GitHub API
- `@meta-sam/parser` exposes `parseImageStream` and `decodeMaskToRaster` (a 0/1 Uint8Array of W×H) for browser-side mask decoding — [dev.meta.ai SDKs](https://dev.meta.ai/docs/sdks); license per [meta-models/meta-sam](https://github.com/meta-models/meta-sam) is the SAM License
- GitHub searches for a combined "sonification blind", "object finder blind" or "getUserMedia websocket" repo returned no results with these query forms — GitHub search (gh CLI)

### Inferences
- [inferred] Minimal stack (a few hours):
  - `getUserMedia({video:{facingMode:'environment', width:640}})`, then a canvas, then `toBlob('image/jpeg', 0.7)` sent over a WebSocket to FastAPI, which calls the SAM API, computes the centroid and area, and returns `{dx, dy, prox, locked}`.
  - The client maps `dx` to `StereoPannerNode.pan`, `dy` to oscillator pitch, and `prox` to click interval, with `navigator.vibrate` as a fallback. iOS Safari doesn't support vibrate.
  - A `role="status"` region receives short text such as "left", "up", "got it".
- [inferred] Drawing canvas frames avoids the EXIF-rotation and aspect mismatch that produce SAM 400s, because canvas output carries no EXIF orientation.
- [inferred] The phone needs HTTPS for the camera and orientation: use a cloudflared tunnel or a Vercel or Fly deployment. `cloudflared` is already on this machine's PATH.
- [inferred] Unlock the `AudioContext` on the same start-button tap that requests orientation permission, since iOS requires a user gesture for audio.

### Gaps
- I did not verify `navigator.vibrate` support on iOS Safari against a source; it is widely reported as unsupported.
- I did not find a published, accessible reference UI for camera guidance apps.

---

## Q9 (Find-and-Guide). Under the runtime rule, are browser speech synthesis or screen-reader output safe? Did organizers clarify?

### Takeaway
The organizer rule is "Every model your project calls at runtime must be a Meta model." **No clarification about TTS, `speechSynthesis` or screen readers was found** in participant repos or issues. Screen-reader output via `aria-live` is the safest option: the user's own assistive technology speaks, and the project calls no model. **Avoid `speechSynthesis`**: some voices are remote services, which could count as a non-Meta model call.

### Cited Findings
- Organizer answer on Discord, Oct 31, recorded verbatim by a participant: "Every model your project calls at runtime must be a Meta model, and this won't affect your eligibility as long as that holds." — [lleoparden/naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- `SpeechSynthesisVoice.localService` returns false when a voice comes from a **remote** synthesizer service, and "Remote voices might have extra latency, bandwidth or cost" — [MDN localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService)
- GitHub issue search for "text-to-speech" or "speechSynthesis" since Oct 18 found no hackathon-related organizer clarification. The only hit was an unrelated repo's "Integrate text-to-speech" issue — [ChrislSparks/GHOST_AI #24](https://github.com/ChrislSparks/GHOST_AI/issues/24)
- Earlier notes flag a visible entry (meta-hack) that uses ElevenLabs for spoken replies, which appears to break the rule — [project notes, event_rules_and_intel.md](https://github.com/meta-ai-hackathon/meta-hack)

### Inferences
- [inferred] Rank by risk:
  1. Earcons and Web Audio tones: no model, safe.
  2. `aria-live` text read by the user's screen reader (VoiceOver or TalkBack): the project doesn't call it, so it is very likely safe.
  3. `speechSynthesis` restricted to `localService === true` voices: an on-device OS engine, gray zone.
  4. `speechSynthesis` with remote voices such as Chrome's "Google …" voices: risky.
- [inferred] If speech is used at all, filter to `localService` voices and say so in the README. Better still, post the question in Discord #questions during the first hour and quote the answer in the README.

### Gaps
- Discord #questions and #announcements need a login and were not read. A clarification may exist there.

---

## Q10 (Find-and-Guide). What are the safety and ethics expectations, and how do we find a real blind or low-vision tester quickly?

### Takeaway
Recruiting blind or low-vision participants is usually the bottleneck. Proven channels are the local National Federation of the Blind (NFB) chapter president or listserv, blindness service organizations and snowball referrals, but responses are slow, so a 24-hour turnaround is optimistic. **Blindfolded sighted testers are not a valid substitute** in evaluation and must be labeled as such. Scope the app to finding objects indoors, make no navigation or obstacle claims, record only with consent, and pay testers.

### Cited Findings
- Recruitment channels used by blind and visually impaired (BVI) study teams:
  - contacting World Services for the Blind
  - contacting the president of the local NFB chapter
  - posting a flyer to the NFB listserv
  - snowball sampling
  - — [UWM BVI study guidelines](https://sites.uwm.edu/guidelines/?p=1120)
- An NN/g write-up of a mobile accessibility study: outreach responses were slow, and a paid recruiting partner helped. Recruiting is often the bottleneck — [NN/g mobile accessibility research](https://www.nngroup.com/articles/mobile-accessibility-research/)
- An empirical study concluded that blind users should not be replaced by blindfolded users in product evaluations where communication quality is measured — [drhu.eu](https://www.drhu.eu/2023/07/can-blindfolded-users-replace-blind-ones-in-product-testing-an-empirical-study/)
- The 2025 Gemma 3n winner had a blind family member shaping its features — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/)
- Lookout's own guidance asks users to move slowly while the app identifies objects in real time — [Lookout help](https://support.google.com/accessibility/android/answer/9031274)

### Inferences
- [inferred] The fastest realistic channels within 24 hours:
  1. Anyone in the team's personal network.
  2. A campus disability services office or accessibility lab.
  3. The local NFB or American Council of the Blind (ACB) chapter (US), a Lighthouse for the Blind affiliate, or national blindness associations elsewhere.
  4. Online communities such as AppleVis forums or r/Blind, with a clear paid offer (for example $50 for a 30-minute remote session) and a consent form.
  - Paid accessibility-testing panels may exist, but I did not verify any provider.
- [inferred] Safety copy for the README and video:
  - "Not a mobility aid; do not use for navigation, traffic, stairs, medication, or hot or sharp objects."
  - A latency and confidence indicator.
  - A "lost lock" earcon, so silence never means "safe".
- [inferred] Ethics checklist: written or recorded consent before filming, the option to blur faces and homes, credit the tester by name only if they agree, and present the footage without "inspiration" framing.

### Gaps
- I verified no paid tester service (for example Fable or AccessWorks): search returned nothing about them.
- I found no hackathon-specific safety guidance for assistive-tech entries in the rules notes.

---

## Q11. Key risks and the first-2-hours de-risking tests for each idea

### Takeaway
Each idea has one test that decides go or no-go within 2 hours. For DemoScribe: one SAM video call and one Spark video call on a RoboReward DROID clip, returning parsable masks and JSON, with per-clip cost and time under about $0.30 and 2 minutes. For Find-and-Guide: phone-to-backend-to-SAM image round trips with a p90 of 1.5 s or less over 50 frames.

### Cited Findings
- SAM 3.1 video limits: 15,000 frames, 16 objects, a 50-frame minimum, one noun phrase per concept request, and `propagation_direction` set to both, forward or backward. Frame order is not guaranteed for box and point prompts, so key results by frame marker — [dev.meta.ai SAM overview, via project notes](https://dev.meta.ai/docs/sam/overview.md)
- Spark is a reasoning model whose reasoning "shares the output budget". Set `max_output_tokens` to at least 4000 and use `stream: true` or lower effort to avoid idle timeouts — [dev.meta.ai Video understanding](https://dev.meta.ai/docs/video-understanding.md)
- `POST /v1/responses/input_tokens` counts tokens before a call — [project notes, meta_models_and_api.md](https://dev.meta.ai/docs)
- ffmpeg and ffprobe are not on this machine's PATH — local `which` check

### Inferences
**DemoScribe, first 2 hours [inferred]**
1. (10 min) `hf download teetone/RoboReward --repo-type dataset --include "test/metadata.jsonl" "test/droid/*" "test/bridge/*"`. Pick 5 clips: two with label 5, one with label 3 and two with label 1.
2. (20 min) Upload one DROID clip with `POST /v1/files`, then make a SAM 3.1 video request with concept "mug" (or the clip's object) and `mask_encoding: "one_bit"`. Parse with `meta_sam_parser`. **Exit:** masks on at least 80% of frames where the object is visible. Record wall time and frames billed.
3. (20 min) Make a second SAM request with a **box prompt on the gripper** in the first frame. **Exit:** the gripper track survives at least 70% of frames (eyeballed). If it doesn't, drop the gripper and use "object lifted or moved" geometry only.
4. (20 min) Spark 1.3 video call (effort low, then medium) with a JSON schema `{objects[], subtasks[{t0,t1,label}], reward_1to5, success, failure_reason}`. Count tokens with `/v1/responses/input_tokens` first. **Exit:** valid JSON, and p50 latency under 60 s.
5. (30 min) Run Spark alone over all 200 DROID and Bridge clips in the background. This gives a **baseline MAE within the hour** to compare against RoboRewardBench (Spark alone vs the published 0.69–1.49 range).
6. (20 min) Check the overlap: read DemoDoctor's `docs/submission/RESULTS.md` and fix positioning ("batch + export + benchmarked").
   - Optional: install ffmpeg only if SO-101 or ALOHA footage is wanted; RoboReward needs none.
- Key risks [inferred]:
  - Spark-alone MAE might already be "good enough", making the geometry layer look decorative. Mitigation: report false-success precision and the 4-vs-5 confusion, where geometry helps.
  - SAM may miss small objects at 180×320 (DROID) or 256×256 (Bridge) resolution.
  - The synthetic negatives in RoboReward's OXE subsets: counterfactual relabels have the *same video* as successes, so only the instruction changes. The pipeline must condition on the task text.
  - DemoDoctor overlap.

**Find-and-Guide, first 2 hours [inferred]**
1. (30 min) A FastAPI WebSocket endpoint plus an HTTPS tunnel (cloudflared) plus a phone page that sends 640 px canvas JPEGs at 2 fps. The backend calls SAM 3.1 image with the concept "mug" and logs t_send, t_api_start, t_first_byte and t_done. **Exit:** p50 and p90 over 50 frames on cellular and on Wi-Fi. Go if p90 is 1.5 s or less; otherwise switch to recorded-clip mode.
2. (15 min) The same loop with a **box prompt** (previous bbox) instead of a concept prompt. Compare latency and lock stability.
3. (15 min) Time Spark 1.3 grounding (effort low) on one frame for "my blue bottle, not the glass one". **Exit:** under 3 s, and the box overlaps the target.
4. (15 min) Web Audio pan, pitch and click prototype driven by a fake `dx/dy`. Test with VoiceOver or TalkBack on and an `aria-live` region updating at 1 Hz, to check that the speech doesn't drown out the earcons.
5. (15 min) Post the TTS and screen-reader question in Discord #questions. Send tester outreach (personal network, campus disability office, local NFB chapter).
6. (30 min) Hold a go/no-go meeting with measured numbers.
- Key risks [inferred]:
  - Latency over 1.5 s turns the live demo into a recorded one, which the organizers consider a fallback.
  - Strong prior art (Lookout Find, Seeing AI Find My Things) could invite "already exists".
  - Without a BLV tester, the Impact story weakens. A blindfolded stand-in must be labeled as such.
  - Per-image requests lose SAM's video memory, so a "lock" across clutter may flicker.
  - iOS permission and HTTPS friction.

### Gaps
- All thresholds above are judgment calls, not sourced benchmarks.
