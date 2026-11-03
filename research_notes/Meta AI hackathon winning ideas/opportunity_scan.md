# Opportunity Scan: High-Potential Project Ideas for the Meta Global AI Developer Hackathon (SAM 3.1 + Muse family)

Scope: opportunity side only (real pains, data/tools, demo-ability, crowding, build risk). Event rules, deep model docs and past winners are covered by other researchers. Research date: Nov 3 2026; build window about 1 to 1.5 days.

Legend used in cards: **[F]** = cited fact; **[I]** = my inference or judgment; "(URL not fetched this session)" = pointer from prior knowledge that the report writer should treat as a lead, not a verified fact.

---

## Q0. What are 12 to 20 concrete candidate projects (user and pain, Meta models, data, wow moment, competitors, build risk)?

### Takeaway
The strongest pattern is **"SAM 3.1 for measurement, Muse for meaning"**: SAM 3.1 turns a short noun phrase into per-instance masks with persistent IDs across video frames, and Muse Spark/Wonder (natively video + image + PDF + audio, 1M-token context) turns those pixels into judgments, reports and actions. Muse Image adds a third lever: counterfactual or synthetic imagery (defect injection, instruction cards). Below are 19 cards. My top picks are (1) a Robot Demonstration Data Engine (auto-annotation plus success verification), (2) a phone- or glasses-based QA/field-tech copilot that reads the spec PDF and checks the part or step visually, (3) Find-and-Guide for blind/low-vision users on Meta glasses, and (4) Defect Forge (Muse Image + SAM 3.1 synthetic defect data).

### Cited Findings (platform facts that constrain every idea)
- Meta Model API lists `sam-3.1`: input is a text prompt, image or video; output is boxes and masks. It "segments all matches to a short noun phrase, or only objects marked with boxes and points. In video, it follows each object across frames." — [Meta Model API models page](https://dev.meta.ai/docs/models.md)
- `muse-spark-1.3` ("recommended for new work") and `muse-wonder-1.0` (preview) both take text, image, video, audio and PDF and return text, with a 1,048,576-token context. Both support tool calling, structured output and search grounding, and Wonder adds computer use. Muse Wonder is not available in South Korea, and Muse Wonder Full is only in Muse Code with a subscription. — [Meta Model API models page](https://dev.meta.ai/docs/models.md)
- `muse-image-1.0`: text + image → image, for generation and editing. It "can search the web and run code to build layouts before rendering." It is served via the Responses API, `/v1/images/generations` and `/v1/images/edits`. — [Meta Model API models page](https://dev.meta.ai/docs/models.md)
- `muse-voice-transcribe-1.0`: streaming speaker diarization, 25 evaluated languages with code-switching, and turn-level timestamps, but no word-level timestamps. — [Meta Model API models page](https://dev.meta.ai/docs/models.md)
- Third parties report Muse Image pricing of about $0.01 to $0.011 per image. Meta describes it as supporting precise edits, iterative refinement and composition from multiple references. Internal tests reportedly put it behind GPT Image 2 on complex edits but ahead of Nano Banana 2. — [WaveSpeedAI](https://wavespeed.ai/blog/ai-models/meta-muse-image-api/); [Flowith](https://flowith.io/ai-models/meta-muse-image/); [fal/ATDB](https://www.theatdb.com/news/muse-image-the-agentic-image-model-from-meta-is-now-available-on-fal)
- SAM 3.1 (Mar 27 2026) adds "Object Multiplex," shared-memory multi-object tracking. Meta reports roughly a 7x speedup at 128 objects on one H100, with mixed accuracy changes across benchmarks (secondary coverage). — [all-ai.de](https://www.all-ai.de/news/beitrage2026/meta-sam-3-1-smart.md); [ComfyUI wiki](https://comfyui-wiki.com/ru/models/sam/sam3.1)
- The SAM 3.1 API streams results per video frame with a completion event. Prompts are concepts ("yellow school bus"), not instructions. The article gives no pricing or latency figures. — [Mind-Verse](https://www.mind-verse.de/news/meta-sam-3-1-bild-video-analyse-api)
- Muse Spark uses visual chain-of-thought. Meta itself acknowledges gaps in long-horizon agentic and coding workflows. — [Neowin](https://www.neowin.net/news/meta-launches-muse-spark-ai-with-reasoning-and-native-multimodal-capabilities/); [Interesting Engineering](https://interestingengineering.com/ai-robotics/meta-muse-spark-ai-launch)
- The Meta Connect 2026 developer recap lists: Muse Code (multi-agent terminal coding agent, now on Windows); Muse Glimmer (30B open weights, single GPU or Mac Mini); the Wearables Device Access Toolkit 1.0 ("camera capture, voice streaming, and motion tracking" on AI glasses); web apps for Meta Ray-Ban Display; and Meta XR Operator ("lets an agent interact with a running app in the simulator and verify results with screenshots"). — [Meta Connect 2026 recap](https://developers.meta.com/blog/meta-connect-recap/)
- Muse Wonder API pricing is reportedly $4 per M input tokens and $20 per M output tokens (secondary). — [BetaNews](https://betanews.com/article/muse-wonder-frontier-model-developers/)
- Roboflow's own docs say SAM 3-powered Auto Label suits generic objects but "cannot distinguish different kinds of cracks or identify defects specific to electronics." That is exactly the gap a Muse reasoning layer fills. — [Roboflow Auto Label docs](https://docs.roboflow.com/datasets/ko/annotate/annotate/ai-labeling/auto-label.md)

### Inferences: the 19 candidate project cards

---

#### PUSH THE FRONTIER: Robotics and embodied AI

**1. Robot Demonstration Data Engine ("DemoScribe"): auto-annotate teleop and robot episodes**
- **User and pain:** Robot-learning teams and data vendors collecting demonstrations. [F] A single teleop setup can cost $40,000+ in hardware, and each operator runs one robot at a time — [AXIS Robotics (vendor)](https://axisrobotics.ai/resources/blog/best-robot-training-data-companies). [F] Voxel51's 2026 Physical AI report (as cited) found that 59% of teams struggle with poor labels and 47% cannot identify data that hurts model performance — [Pebblous](https://blog.pebblous.ai/blog/agibot-world-failure-annotation/en/). [F] The ICCV 2025 RoboAnnotatorX paper calls manual annotation "expensive and poorly scalable" — [RoboAnnotatorX](https://openaccess.thecvf.com/content/ICCV2025/html/Kou_RoboAnnotatorX_A_Comprehensive_and_Universal_Annotation_Framework_for_Accurate_Understanding_ICCV_2025_paper.html). [F] A May 2026 preprint (DeMiAn) shows that dense VLM re-annotation of existing demos matched a no-annotation baseline with ~62% less compute at 1M-clip scale — [arXiv 2605.17077](https://arxiv.org/pdf/2605.17077). [F] AgiBot World 2026 keeps failed demos, and Pebblous argues failure annotation is becoming a prerequisite — [Pebblous](https://blog.pebblous.ai/blog/agibot-world-failure-annotation/en/).
- **Meta models and why essential:** SAM 3.1 tracks every manipulated object (and the gripper, via box prompt) across the episode with stable IDs, which yields object-centric trajectories, contact and grasp moments, and masks for training. Muse Spark (video input, 1M context) segments the episode into subtasks, writes dense language instructions, and labels failures with reasons as structured JSON. [I] A generic VLM can caption, but it cannot produce pixel-accurate, ID-stable object tracks. SAM 3.1's open-vocabulary video tracking is the hero.
- **Data and sims:** [F] Open X-Embodiment: 1M+ trajectories from 22 embodiments — [OXE paper](https://arxiv.org/pdf/2310.08864). A later report says 20 embodiments — [RLDX-1 tech report](https://arxiv.org/pdf/2605.03269). [F] DROID: widely cited at ~76K trajectories, ~350 h, 86 tasks, 564 scenes, though a 2026 report cites 92K, so the count is unsettled — [RLDX-1 tech report](https://arxiv.org/pdf/2605.03269). Leads (URLs not fetched this session): DROID site droid-dataset.github.io, LeRobot datasets on Hugging Face, AgiBot World.
- **Wow moment (2 min):** Drop a raw DROID episode in. Within seconds you see colored masks tracking the mug, drawer and gripper; a timeline auto-split into "reach / grasp / lift / place"; a red flag at 0:14 ("grasp slipped, mug re-grasped"); and a one-click export to LeRobot/RLDS format with language annotations. End with a dashboard: "1,000 episodes annotated for $X in Y minutes vs Z human-hours."
- **Competitors and crowding:** [F] Roboflow integrated SAM 3 auto-labeling in November 2025, but for generic image labeling — [Roboflow SAM 3 launch](https://blog.roboflow.com/sam3/). Academic tools include RoboAnnotatorX and DeMiAn. [I] Scale AI, Encord and Labelbox likely serve robotics data too (not verified this session). The specific episode → subtask + failure + object-track pipeline looks moderately crowded academically but thin as a dev tool.
- **Build risk (1–1.5 days): LOW-MEDIUM.** [F] The RobotSeg paper found SAM 3 is not tailored to articulated robot geometry, fine-grained arm-gripper separation, or temporally consistent segmentation — [RobotSeg arXiv 2511.22950](https://arxiv.org/pdf/2511.22950). [I] Mitigation: prompt manipulated objects by noun, box-prompt the gripper on frame 0, and pre-cache the demo episodes. Unknown SAM 3.1 video latency and rate limits mean you should process 5 to 20 short clips offline.
- **Track fit:** Startup (clear B2B buyer). It also aligns with the YC Fall 2026 RFS "Data for the Real World" — [explainx summary](https://explainx.ai/blog/yc-requests-for-startups-fall-2026).

**2. Zero-shot Robot Referee: object-centric reward and success verification from video**
- **User and pain:** Policy-learning teams that need cheap, reliable evals and rewards. [F] The 2023 DeepMind-era work found zero- and few-shot VLM success detection unreliable without in-domain finetuning — [arXiv 2303.07280](https://arxiv.org/pdf/2303.07280). 2026 work keeps attacking this: TOPReward (token-probability progress, ManiRewardBench with 130+ real tasks) — [arXiv 2602.19313](https://arxiv.org/html/2602.19313); RoboReward (2,800 real episodes with human-verified progress scores, plus counterfactual negatives) — [arXiv 2601.00675](https://arxiv.org/pdf/2601.00675v1); Demo2Reward (test-time prompt optimization for VLM rewards) — [arXiv 2606.00083](https://arxiv.org/pdf/2606.00083).
- **Meta models and why essential:** SAM 3.1 supplies geometry (mask centroids, overlap, containment such as "is the mug mask inside the shelf mask"), which gives a dense, interpretable progress signal. Muse Spark reasons over video plus these mask-derived features, adjudicates success, and explains "fake successes" (for example, a gripper hovering). [I] Combining hard geometry with reasoning is the novel angle versus pure-VLM rewards.
- **Data and sims:** [F] The RoboReward and ManiRewardBench datasets give a ground-truth scoreboard (papers above). Leads (URLs not fetched): LIBERO, ManiSkill, MuJoCo Menagerie, and Genesis rollouts rendered to video.
- **Wow moment:** Two rollouts of the same task play side by side. Live progress curves rise and fall, one is caught "succeeding" without actually placing the object, and you show agreement with human labels on RoboReward ("X% agreement, zero training").
- **Competitors:** Mostly academic (above). [I] Commercial robot-eval startups likely exist, but I found none in this session.
- **Build risk: MEDIUM.** Quantifying accuracy needs a labeled subset, which RoboReward provides. Keep to 2 or 3 task families.
- **Track fit:** Indie (technical ambition) or Startup as an eval API. It merges naturally with card 1 into one "Robot Data Engine."

**3. Watch-and-Do: one human video becomes a simulated robot program**
- **User and pain:** Small manufacturers and integrators who cannot afford robot programming. [F] Small manufacturers lag in AI adoption (larger firms 2.3x more likely to adopt AI; 87% of manufacturers have not adopted it into workflows, per a secondary source) — [Digit Software](https://www.digit-software.com/blog/study-ai-adoption-in-us-manufacturing).
- **Meta models:** SAM 3.1 tracks hands and objects in a top-down tabletop video, which gives 2D waypoints and pick/place events. Muse Spark builds a step graph ("pick red block → place in bin B") as structured output. Muse Code or Muse Wonder generates MuJoCo/Genesis scripted-policy code and iterates until the simulated rollout matches. Card 2's referee verifies the result.
- **Data and sims:** Leads (URLs not fetched): MuJoCo Menagerie Franka/UR5 models, Genesis, PyBullet; Ego4D/Ego-Exo4D (Meta's own) for human procedure video.
- **Wow moment:** Film yourself sorting three objects on a desk. Ninety seconds later a simulated Franka does the same sort, with the SAM masks overlaid on both videos.
- **Competitors:** [I] Academic video-to-robot imitation work and industrial programming-by-demonstration vendors (not verified this session).
- **Build risk: HIGH.** Lifting 2D to 3D is the crux. Constrain it to a calibrated top-down camera and a planar table, and use scripted IK in sim, not learned policies. Huge wow if it lands; prepare a fallback recorded run.
- **Track fit:** Indie (creativity plus ambition), Push the Frontier.

---

#### PUSH THE FRONTIER: Manufacturing, energy, materials, software

**4. Defect Forge: synthetic, auto-labeled defect data with Muse Image + SAM 3.1**
- **User and pain:** QA and ML teams with too few defect examples. [F] Cost of poor quality is commonly cited at 15 to 20% of revenue (vendor blogs attributing it to ASQ), with wider ranges of 5 to 35% — e.g., [Oxmaint](https://oxmaint.com/industries/manufacturing-plant/manual-vs-automated-quality-inspection-manufacturing), [Ombrulla](https://ombrulla.com/blog/ai-visual-inspection-roi-2026-investment-case). Treat these as vendor benchmarks. [F] Generic SAM 3 auto-labeling cannot distinguish crack types or electronics-specific defects — [Roboflow docs](https://docs.roboflow.com/datasets/ko/annotate/annotate/ai-labeling/auto-label.md).
- **Meta models and why essential:** Muse Image `/v1/images/edits` injects a realistic scratch, dent or contamination onto a good-part image, guided by reference defect images (it supports multi-reference composition — [Flowith](https://flowith.io/ai-models/meta-muse-image/)). SAM 3.1 then segments the injected defect, so the label comes free. Muse Spark acts as realism critic and taxonomy assigner and rejects implausible samples. [I] All three Meta models are load-bearing, which makes this a "full Meta stack" story judges will like.
- **Data:** Leads (URLs not fetched): MVTec AD (mvtec.com, about 5.3K images across 15 categories, per my prior knowledge), VisA (amazon-science/spot-diff), Kolektor SDD, NEU surface defects.
- **Wow moment:** Select "metal nut, scratch, 200 samples." A grid fills with photoreal defects, each with a mask. Then hold up real MVTec scratches and show the SAM 3.1 + Muse pipeline, prompted with a few synthetic exemplars, flagging them.
- **Competitors:** [I] Synthetic-data vendors (e.g., Synthesis AI, Datagen, NVIDIA Omniverse Replicator) and anomaly-detection vendors. Generative defect injection via an edit API is less crowded (not verified).
- **Build risk: MEDIUM.** The rules say no custom training, so prove value via labeled-dataset generation plus a retrieval or few-shot check instead of training a detector. Edit fidelity on tiny defects is uncertain.
- **Track fit:** Both. Strong startup path (synthetic data for QA).

**5. Inspector-in-a-Phone: spec-aware visual QA copilot for small manufacturers**
- **User and pain:** Quality techs at job shops and SMB manufacturers with no ML team. [F] Manual inspection catches roughly 60 to 80% (up to 85 to 90%) of defects by vendor estimates — [Oxmaint](https://oxmaint.com/industries/manufacturing-plant/manual-vs-automated-quality-inspection-manufacturing). [F] An MEP-linked national assessment found the biggest barriers are organizational, not technological, and nearly 7 in 10 manufacturers would consider a structured AI pilot within six months — [FME assessment press release](https://norfolkdailynews.com/online_features/press_releases/national-assessment-identifies-a-practical-path-for-ai-adoption-in-manufacturing/article_14856071-4f70-58b8-bca9-af4917332a5a.html). [F] Only 8.2% of manufacturers are actively scaling AI (Amper survey) — [Amper](https://www.amper.xyz/post/manufacturing-in-the-age-of-ai-part-4).
- **Meta models and why essential:** Muse Spark ingests the customer drawing or spec PDF plus a golden-sample photo plus the new part's video in one 1M-token call (it accepts PDF, image and video — [models page](https://dev.meta.ai/docs/models.md)). SAM 3.1 isolates the part and features ("hole," "weld bead," "label") and measures them in pixels, scaled by a reference object. Muse Spark returns pass/fail per spec clause and drafts a nonconformance report (NCR) or 8D. [I] Zero training, configured by a PDF, is the SMB unlock.
- **Data:** MVTec AD and VisA (as above); any public engineering drawing PDFs; a phone video of a real part.
- **Wow moment:** Upload a drawing PDF and wave a phone over a bracket. The screen highlights "hole 3 missing, violates note 4 on sheet 2" with the mask overlaid, and an auto-filled NCR appears.
- **Competitors:** [I] Landing AI (LandingLens), Instrumental, Elementary, Cognex/Keyence smart cameras, Roboflow (not verified this session). Crowded for trained-model inspection; less crowded for spec-PDF-driven, zero-shot checks.
- **Build risk: LOW-MEDIUM.** Pixel-to-mm accuracy is shaky, so demo presence/absence and gross geometry rather than tolerances.
- **Track fit:** Startup (clear wedge). Also Build for Your World if a team member has shop-floor experience.

**6. LineSight: natural-language triage of power-line drone imagery**
- **User and pain:** Utility inspection and vegetation-management teams. [F] One vendor says vegetation management costs US utilities about $8B a year, and relays an EPRI estimate that outages and disturbances cost the US economy nearly $120B a year (vendor relay, not primary) — [Border States blog](https://solutions.borderstates.com/blog/drone-vegetation-management-for-utilities/). [F] In Georgia Power's drone pilot, drones found 1,757 line issues that ground crews missed, with about 100,000 images collected per year — [T&D World](https://www.tdworld.com/overhead-transmission/article/55131627/how-drones-are-revolutionizing-power-line-inspections-georgia-powers-success-story). [F] Helicopter inspection runs about $4K per day — [INL GridTechPedia](https://gridtechpedia.inl.gov/?p=27240).
- **Meta models and why essential:** SAM 3.1 handles open-vocabulary prompts like "insulator," "bird nest," "broken strand," "tree," "conductor" with no per-utility training. Muse Spark reasons about relationships (vegetation encroaching on conductor, cracked insulator) and severity, writes the work order, and answers analyst questions ("show every tower with a nest near energized parts"). [I] The noun-phrase retargeting is what replaces months of model training per asset class.
- **Data:** Leads (URLs not fetched): TTPLA (transmission towers and power lines), InsPLAD (insulator defects), CPLID; public utility drone videos.
- **Wow moment:** A chat box over 500 drone images. Type "nests on crossarms" and get instant masked hits, a severity-ranked map, and a generated work-order PDF.
- **Competitors and crowding:** [F] Buzz Solutions raised a $20M Series A (Aug 2026) for grid visual AI — [Axios](https://www.axios.com/pro/climate-deals/2026/08/04/buzz-solutions-20m-grid-ai). It claims Dominion processed 74,000 images of about 47,000 towers in 3.5 hours, and AEP Texas cut manual analysis time by 70% — [Unite.ai](https://www.unite.ai/?p=448568). [I] Others include Sharper Shape, AiDash, Skydio and Percepto (not verified). Crowded with funded incumbents, so differentiate on zero-training open vocabulary plus chat.
- **Build risk: LOW.** Images only, no video required.
- **Track fit:** Startup (but incumbents exist) or Push the Frontier (energy).

**7. Solar Fault Hunter: IR + RGB module-level fault classification with kWh-loss estimates**
- **User and pain:** Solar O&M operators and asset owners. [F] Controlled IEA-PVPS/DTU tests found losses by defect type: cell cracks about 4 to 5%, broken interconnections 3 to 14%, PID about 5%, shorted bypass diode 33 to 66%, heavy soiling about 66% — [IEA PVPS slides](https://iea-pvps.org/wp-content/uploads/2025/08/07_S.-Spataru_Framing-Drone-IRT-Conditions.pdf); [EPJ PV 2025](https://www.epj-pv.org/articles/epjpv/pdf/2025/01/pv20250040.pdf). [F] Raptor Maps (vendor, as cited) reports a 5.08% average power loss from undetected faults — [SKYMODEL](https://skymodel.de/en/pv-thermografie/). [F] A peer-reviewed rooftop study found a higher share of defective modules meant lower generation — [Energies 2023](https://doaj.org/article/9066729eb4054182bc96c89fb37d8fc9).
- **Meta models:** SAM 3.1 segments each module and hotspot ("solar panel," "hot spot") in drone video and tracks modules across frames to avoid double counting. Muse Spark classifies the fault pattern (diode string vs cell vs soiling), applies the loss table above, and ranks repairs by $/kWh recovered.
- **Data:** Leads (URLs not fetched): Raptor Maps InfraredSolarModules (GitHub), ELPV electroluminescence dataset, PVEL-AD.
- **Wow moment:** A drone flyover. Modules light up by fault class, and a running "$ lost per year" counter ticks up, followed by a prioritized repair list.
- **Competitors:** [I] Raptor Maps, Zeitview, Heliolytics (not verified). Crowded commercially.
- **Build risk: LOW-MEDIUM.** SAM on thermal imagery is a domain-shift risk, so test early and fall back to box prompts.
- **Track fit:** Push the Frontier (energy). It could be a module inside card 6 as an "energy infrastructure inspector."

**8. GrainCounter: microscopy quantification linked to materials databases**
- **User and pain:** Materials-science grad students and lab engineers who hand-measure grains, particles, pores and cracks in SEM/optical micrographs. [I] Intense manual pain in academia, but I found no cost statistic this session (see Gaps).
- **Meta models:** SAM 3.1 handles "grain," "particle," "pore," "crack" with point prompts as a fallback, producing size and shape distributions. Muse Spark reads the paper or processing-log PDF, interprets the distributions against expectations, queries the Materials Project API via tool calling for phase data, and suggests the next experiment.
- **Data:** Leads (URLs not fetched): Materials Project API (next-gen.materialsproject.org/api), the NFFA-EUROPE SEM image set, the UHCS steel micrograph dataset, and open battery-electrode CT data.
- **Wow moment:** Drop in 20 micrographs and get a histogram, an ASTM-style grain-size number, and "your grain size suggests the anneal was too short; Materials Project shows phase X is stable at..."
- **Competitors:** [I] MIPAR, ImageJ/Fiji plugins, Dragonfly, Thermo Fisher Avizo (not verified). Fragmented, with SAM-based academic tools emerging.
- **Build risk: MEDIUM.** SAM performance on dense micrographs is unverified, so check on day 0.
- **Track fit:** Indie / Push the Frontier (materials). It ties into "self-driving labs" narratives.

**9. Visual QA Agent for web and XR apps: component-level visual regression plus repro**
- **User and pain:** Frontend, mobile and XR developers drowning in flaky UI tests. [F] Meta's own end-to-end tests reportedly run at about 10% flakiness versus under 1% for unit tests, and Atlassian reportedly loses 150,000 developer hours a year (secondary blog) — [Panto](https://www.getpanto.ai/blog/flaky-test-statistics). [F] The ICST 2022 survey found that lost trust and wasted developer time are the most severe perceived impacts of flakiness — [Eck et al., arXiv 2203.00483](https://arxiv.org/abs/2203.00483v4). [F] One vendor relays a claim that 72% of test failures are false positives (unverified) — [Bug0](https://bug0.com/blog/true-cost-of-flaky-tests-2026).
- **Meta models and why essential:** Muse Wonder (computer use) drives the app. SAM 3.1 segments UI components ("button," "modal," "avatar," "text field") in before/after screenshots, so diffs are per component rather than per pixel, which cuts false positives from anti-aliasing or shifts. Muse Spark explains which regressions are real. Muse Code opens the fix PR. [F] Meta just launched XR Operator for agents that verify VR apps with screenshots — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/). [I] An XR-app QA variant aligns tightly with Meta's own ecosystem.
- **Data and tools:** Any open-source web app (e.g., a TodoMVC clone) seeded with regressions; Meta XR Simulator / Immersive Web Emulator for the XR variant — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/).
- **Wow moment:** Push a CSS change. The agent runs the flow, shows "1 real regression (checkout button hidden behind modal), 14 pixel diffs ignored," then opens a PR with the fix and before/after masks.
- **Competitors and crowding:** [I] Applitools, Percy, Chromatic, Meticulous, QA Wolf, Momentic (not verified). Very crowded on the web, much less so for XR.
- **Build risk: MEDIUM.** SAM on synthetic UI imagery is a domain-shift risk, and the computer-use loop is brittle. Keep the flow scripted.
- **Track fit:** Startup (dev tools have clear buyers). Pick the XR angle to stand out.

---

#### BUILD FOR YOUR WORLD and physical industries

**10. Site Replay: OSHA "Focus Four" hazard detection from site video**
- **User and pain:** Superintendents and safety managers at small and mid GCs. [F] BLS counted 1,034 private construction deaths in 2024. Falls, slips and trips caused 389 (over one-third), about 96% of them falls to a lower level — [BLS TED 2026](https://www.bls.gov/opub/ted/2026/national-safety-stand-down-highlights-fall-hazards-in-construction.htm). [F] Transportation incidents were second at 244 and contact incidents 161 — [Construction Dive](https://www.constructiondive.com/news/constructions-deaths-fatality-rate-2024-hazards/812666/).
- **Meta models and why essential:** SAM 3.1 tracks every worker, excavator, ladder, guardrail and floor opening with persistent IDs (Object Multiplex suits busy scenes). Muse Spark reasons about relations over time ("worker 7 inside the excavator swing radius for 12 s," "worker at slab edge, no guardrail mask present") and writes a toolbox talk in the crew's language.
- **Data:** Leads (URLs not fetched): SODA and MOCS construction datasets, hard-hat datasets, public site timelapse and YouTube footage.
- **Wow moment:** A site clip replays with tracked IDs. A red event card pops ("struck-by risk, 0:42"), and a 30-second Spanish/English toolbox talk with stills is auto-generated.
- **Competitors and crowding:** [F] Voxel raised a $44M Series B in 2025 — [Shopifreaks](https://www.shopifreaks.com/voxel-raises-44m-series-b-to-expand-ai-powered-workplace-safety-tech/). Intenseye raised a $64M Series B in 2024 — [Pulse 2.0](https://pulse2.com/intenseye-64-million-funding/amp/). Crowded for warehouses and factories. [I] Open-vocabulary rules authored in plain language ("flag anyone under a suspended load") are the differentiator.
- **Build risk: MEDIUM.** Monocular distance reasoning is noisy, so use curated clips and relative proximity, not meters.
- **Track fit:** Startup or Build for Your World (anyone from construction).

**11. TrapTales: camera-trap video to ecology dataset (species, counts, behavior)**
- **User and pain:** Field ecologists and conservation NGOs. [F] Every camera-trap image must be classified, "requiring significant labor, and potentially creating an information bottleneck." MegaDetector reached 99% precision and 95% recall on humans, and 82% precision and 92% recall on animals, in one test — [Fennell et al. 2022](https://doaj.org/article/0ace75670ca4470c9a9be18572c2b496). [F] MegaDetector only detects animals, people and vehicles. Its docs note that researchers could keep pace if they could just clear the backlog — [MegaDetector docs](https://megadetector.readthedocs.io/en/latest/getting-started.html).
- **Meta models and why essential:** SAM 3.1 prompts per species ("zebra," "lion cub") and tracks individuals through a clip, which gives counts without double counting plus movement paths. Muse Spark identifies species and behavior (vigilance, feeding, nursing), reasons about uncertain IDs, and outputs occupancy-model-ready CSV. [I] MegaDetector does detection only. Tracking plus behavior plus species is the step change.
- **Data:** Leads (URLs not fetched): LILA BC (lila.science: Snapshot Serengeti, Caltech Camera Traps), DrivenData Zamba video datasets, Wildlife Insights.
- **Wow moment:** Fifty night-vision clips go in. Out comes a map of species, a counted herd with tracked IDs, and a ranger-ready summary ("a female leopard with 2 cubs visited station 4 three times this week").
- **Competitors:** MegaDetector / EcoAssist / Timelapse — [WildLabs](https://wildlabs.net/node/5725). [I] Zamba, Wildlife Insights, Conservation AI (not verified). Moderately crowded on images, less on video behavior.
- **Build risk: LOW.** Public data, forgiving users.
- **Track fit:** Indie (impact plus wow). The startup path is weak (grant-funded buyers).

**12. OR Rewind: surgical video review and operative-note copilot**
- **User and pain:** Surgeons, residents and quality teams. [F] Theator raised $15.5M (2021) plus a $24M extension (2022), led by Insight Partners with Mayo Clinic participating, to flag key moments in surgical video. It reports 30,000+ hours of video analyzed — [Insight Partners](https://www.insightpartners.com/ideas/theator-raises-15-5m-series-a-round-to-scale-its-surgical-intelligence-platform/); [HIT Consultant](https://hitconsultant.net/2022/07/25/theator-surgical-intelligence-funding/).
- **Meta models and why essential:** [F] SAM 3 shows clear improvements over SAM and SAM 2 under spatial prompts on EndoVis surgical benchmarks — [arXiv 2512.07596](https://arxiv.org/abs/2512.07596v1). SAM 3.1 tracks instruments ("grasper," "clip applier," "hook"). Muse Spark labels phases, checks Critical View of Safety, and drafts the operative note and coaching feedback.
- **Data:** Leads (URLs not fetched): Cholec80 / CholecT50 / CholecSeg8k (CAMMA; access requires a request form, which is a timing risk), EndoVis challenges.
- **Wow moment:** A 30-minute cholecystectomy collapses into a 60-second highlight reel with tracked instruments, a phase timeline, and "CVS achieved at 18:42," plus an auto-drafted op note.
- **Competitors:** Theator (above). [I] Caresyntax, Medtronic Touch Surgery, Activ Surgical (not verified). Crowded and regulated.
- **Build risk: MEDIUM-HIGH.** Dataset access lead time, and clinical claims need careful framing.
- **Track fit:** Indie (wow). The startup path is long because of regulation.

**13. Sideline: a pro-grade tactical analyst for amateur teams from a phone video**
- **User and pain:** Grassroots and youth coaches. [F] Hudl, Veo, Pixellot (Vidswap) and PlaySight sell automated cameras and analysis — [Hudl Focus](https://www.hudl.com/products/focus/indoor); [CB Insights](https://www.cbinsights.com/company/hudl/alternatives-competitors). A German review calls Veo or Kinovea the cheaper options for amateur clubs on very limited budgets — [KI-Syndikat](https://www.ki-syndikat.de/tools/hudl/). [F] Leagues are adopting AI cameras for youth sports — [KTLA](https://ktla.com/news/local-news/ai-cameras-give-youth-sports-a-pro-upgrade/amp/).
- **Meta models and why essential:** SAM 3.1 Object Multiplex tracks all 22 players plus the ball with IDs (multi-object tracking is its headline upgrade). Muse Spark answers "why did we concede at 34:10?" with tactical reasoning. Muse Image renders a tactics-board diagram of the moment.
- **Data:** Leads (URLs not fetched): SoccerNet (tracking, game-state), SportsMOT; any phone-filmed match.
- **Wow moment:** Ask "show every time our left back was caught upfield." Clips appear with the player's mask highlighted, plus a Muse Image tactics card per clip.
- **Competitors:** Hudl, Veo, Pixellot, PlaySight (above). Crowded, but phone-only, zero-hardware, conversational analysis is the gap.
- **Build risk: MEDIUM.** Small, fast ball; panning camera. Demo on a fixed wide-angle clip.
- **Track fit:** Indie (high wow), Build for Your World (players and coaches).

**14. Find-and-Guide: glasses-native object finding and guidance for blind/low-vision users**
- **User and pain:** [F] At least 2.2 billion people have near or distance vision impairment, at least 1 billion of it preventable or unaddressed, with about US$411B a year in productivity loss (WHO, Feb 2026) — [WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment). [F] In an AFB survey, 98.7% of Be My Eyes users who gave an opinion were positive about Be My AI — [AFB](https://afb.org/aw/fall2024/ai-usage-research). Be My Eyes reports 1M+ blind/low-vision users (opinion page relaying an official milestone) — [sheets.works](https://sheets.works/data-viz/be-my-eyes).
- **Meta models and why essential:** The Wearables Device Access Toolkit gives camera capture and voice streaming from Meta glasses — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/). The user says "find my keys," "the empty seat," or "the door handle." SAM 3.1 finds and tracks that object across frames (persistent tracking is what enables continuous left/right/closer cues, which one-shot scene description can't do). Muse Spark gives conversational spatial guidance and safety caveats. Muse Voice Transcribe handles noisy multilingual speech.
- **Data:** Leads (URLs not fetched): the VizWiz dataset (photos and questions from blind users); self-recorded glasses video.
- **Wow moment:** First-person glasses video. "Find my white mug." The mask locks on, audio says "slightly right, arm's length," and the cue updates as the head turns, until the hand closes on the mug.
- **Competitors:** Be My Eyes / Be My AI (above). [I] Seeing AI, Envision glasses, Aira (not verified). Crowded for describing scenes, less served for continuous tracking-based guidance.
- **Build risk: MEDIUM.** Real-time latency over the API is unknown, so demo at 1 to 2 fps on recorded or near-live video. Toolkit setup time is a risk, so a phone camera is the fallback.
- **Track fit:** Indie (emotional wow) or Build for Your World. Strong Meta-hardware alignment.

**15. Second Pair of Hands: a field-technician copilot on Meta glasses that checks each step visually**
- **User and pain:** HVAC, electrical, appliance and telecom field techs. [F] The YC Fall 2026 RFS "New Operating Systems for the Physical World" (Charlie Warren) asks for software coordinating AI agents, field robots and wearable-equipped workers in construction, maintenance and fleet ops — [explainx summary of YC RFS](https://explainx.ai/blog/yc-requests-for-startups-fall-2026).
- **Meta models and why essential:** Muse Spark loads the equipment manual PDF (1M context) and plans steps. SAM 3.1 segments the referenced components ("run capacitor," "contactor," "breaker 14") in the tech's camera view and highlights them. After each step, Muse Spark verifies with a frame ("wire moved to terminal C? yes"). Muse Voice Transcribe enables hands-free, code-switched speech in 25 languages — [models page](https://dev.meta.ai/docs/models.md).
- **Data:** Public HVAC/appliance manuals (PDF); Ego-Exo4D skilled-activity video (bike repair etc., URL not fetched); self-filmed repair.
- **Wow moment:** First-person furnace repair. The glasses highlight the exact part, the tech says "done," and the system catches a mistake: "that's the C terminal, not HERM — stop."
- **Competitors:** [I] TeamViewer Frontline, Augmentir, Taqtile, Microsoft Dynamics 365 Guides, Scope AR (not verified). These are mostly authored AR instructions, so zero-authoring from the PDF is the gap.
- **Build risk: MEDIUM.** Same glasses-toolkit risk as card 14, so a phone fallback is fine.
- **Track fit:** Startup (B2B field service) and Build for Your World (anyone from the trades).

**16. Leaf-Level Scout: multilingual crop scouting with counts and severity from phone video**
- **User and pain:** Smallholders and agronomy extension workers. [F] FAO estimates up to 40% of global crop production is lost to pests and diseases; plant diseases cost more than $220B a year and invasive insects at least $70B — [WEF/FAO](https://www.weforum.org/stories/2021/06/climate-change-insects-pests-crops-agriculture/); [Down to Earth](https://www.downtoearth.org.in/news/agriculture/at-least-40-global-crops-lost-to-pests-every-year-fao-77252). [F] An IITA official puts Sub-Saharan Africa losses above $200B a year — [Guardian NG](https://guardian.ng/?p=1080100).
- **Meta models and why essential:** SAM 3.1 segments and counts leaves, lesions, pests ("fall armyworm") and weeds across a row walk, and tracks them across frames to count once. That gives a quantitative severity score, versus a single-leaf classifier. Muse Spark diagnoses and gives IPM advice grounded by search. Muse Voice Transcribe takes code-switched speech (e.g., Hindi-English). Muse Image produces a "what to look for" picture card for low-literacy users.
- **Data:** Leads (URLs not fetched): PlantVillage, PlantDoc, DeepWeeds, CropAndWeed, IP102 pests.
- **Wow moment:** A farmer speaks Hinglish and films 10 seconds of a maize row. Back comes "23% of leaves show fall armyworm damage, above action threshold," spoken back in Hindi with a generated picture card.
- **Competitors:** [I] Plantix, Kissan AI, Taranis, xarvio (not verified). Crowded for single-leaf disease ID, less so for video-based severity quantification.
- **Build risk: MEDIUM.** Diagnosis accuracy, so frame it as triage and refer to an agronomist.
- **Track fit:** Build for Your World (strong if a team member farms or comes from an agricultural region). Indie.

**17. Aisle Walk: planogram and out-of-stock audit from a phone walk-through video**
- **User and pain:** Independent grocers and CPG field reps. [F] IHL estimates global inventory distortion at about $1.73T, with about $1.157T lost to out-of-stocks — [Chain Store Age](https://chainstoreage.com/ihl-group-inventory-issues-cause-17t-annual-losses); [Board](https://www.board.com/resources/the-1-73-trillion-wake-up-call). IHL projects about $1.7T in 2026, equal to 6.2% of global retail sales (modeled estimate).
- **Meta models and why essential:** SAM 3.1 segments every facing and gap ("empty shelf space," "price tag") and tracks across the walk to avoid double counting. Muse Spark reads the planogram PDF and product labels and lists the misplaced items, out-of-stocks and price-tag mismatches as a task list.
- **Data:** Leads (URLs not fetched): SKU-110K (dense shelf images), the RPC retail checkout dataset; a self-filmed store aisle.
- **Wow moment:** A 20-second aisle walk produces a heat-mapped shelf, "7 OOS, 3 misplaced, 2 wrong prices," and a restock list sorted by lost revenue.
- **Competitors:** [I] Trax, Simbe (Tally), Focal Systems, Pensa (not verified). Crowded at the enterprise level, which makes SMB with a phone and no hardware the wedge.
- **Build risk: MEDIUM.** Fine-grained SKU identity, so lean on Muse reading the label text.
- **Track fit:** Startup.

**18. Damage Ledger: per-building disaster damage assessment from satellite and drone**
- **User and pain:** Emergency managers and insurers after hurricanes, floods and wildfires. [I] High pain and time-critical, but I did not collect cost statistics this session (see Gaps).
- **Meta models:** SAM 3.1 segments buildings in pre/post imagery, or tracks them in drone video. Muse Spark grades damage per building (none/minor/major/destroyed) with reasoning and writes a preliminary damage assessment summary. Muse Image is not needed.
- **Data:** Leads (URLs not fetched): xView2/xBD (pre/post building damage across many disasters), Maxar Open Data, SpaceNet.
- **Wow moment:** A post-hurricane tile in which every roof is colored by damage class, with a generated "312 homes destroyed in ZIP X" briefing.
- **Competitors:** [I] Google's SKAI, Microsoft AI for Good, Planet (not verified). Crowded among research and NGO players.
- **Build risk: LOW.** Images only.
- **Track fit:** Indie or Push the Frontier.

**19. Dock Witness: logistics chain-of-custody and damage-claim builder**
- **User and pain:** Warehouse and 3PL claims teams. [I] Plausible pain (damage disputes), but I found no cited cost statistic this session (see Gaps).
- **Meta models:** SAM 3.1 tracks each pallet and parcel ID across dock-camera video (identity stability is a use case the SAM 3.1 API coverage names explicitly for logistics — [Mind-Verse](https://www.mind-verse.de/news/meta-sam-3-1-bild-video-analyse-api)). Muse Spark detects drop, crush and forklift-pierce events and writes a timestamped claim packet with stills.
- **Data:** Public warehouse or forklift footage (YouTube); [I] there are few labeled public datasets, which is a risk.
- **Wow moment:** "Show me everything that happened to pallet 14" returns a 15-second chain-of-custody reel and a claim PDF.
- **Competitors:** [I] Warehouse vision vendors (e.g., Voxel also does warehouses — [Shopifreaks](https://www.shopifreaks.com/voxel-raises-44m-series-b-to-expand-ai-powered-workplace-safety-tech/)).
- **Build risk: MEDIUM** (data).
- **Track fit:** Startup.

### Gaps
- No pricing, rate limits or latency for `sam-3.1` video calls appear on the models page or in coverage — [Mind-Verse](https://www.mind-verse.de/news/meta-sam-3-1-bild-video-analyse-api); [models page](https://dev.meta.ai/docs/models.md). This is the single biggest feasibility unknown for every video idea, so test throughput in the first hour.
- I did not verify whether `sam-3.1` accepts exemplar-image prompts via the API. The docs mention noun phrases, boxes and points only.
- Dataset specifics (MVTec AD counts, Cholec80 access terms, TTPLA, LILA, SoccerNet, VizWiz, SKU-110K, xBD, PlantDoc, Materials Project API) come from prior knowledge, not pages fetched in this session. Verify licenses (several are non-commercial) before relying on them.
- No cost statistics were collected for microscopy labor (card 8), disaster assessment (card 18) or logistics damage claims (card 19).
- I found no Devpost or prior-hackathon winners built on SAM 2/SAM 3 in search ([search returned only repos and docs](https://github.com/facebookresearch/sam2)), so prior-hackathon crowding is unverified. The past-winners researcher should cross-check.
- Competitor names marked "(not verified)" are from prior knowledge.

---

## Q1. Where do segmentation + tracking + multimodal reasoning create step-change value in physical industries?

### Takeaway
Step-change value appears where today's workflow is "humans scroll through thousands of images or hours of video to find, count and judge a few things." SAM 3.1 removes per-domain model training (noun-phrase retargeting) and adds identity-stable counting and tracking. Muse adds the judgment and paperwork layer (severity, spec compliance, reports), which generic auto-labelers explicitly cannot do. The highest-evidence domains are energy inspection, manufacturing QA, construction safety, conservation and retail.

### Cited Findings
- Image-review volume is the bottleneck in utility inspection: Georgia Power collects about 100,000 images a year, and drones found 1,757 issues ground crews missed — [T&D World](https://www.tdworld.com/overhead-transmission/article/55131627/how-drones-are-revolutionizing-power-line-inspections-georgia-powers-success-story). Buzz Solutions claims 74,000 images processed in 3.5 hours for Dominion and a 70% cut in manual analysis time at AEP Texas — [Unite.ai](https://www.unite.ai/?p=448568).
- Investors are funding this space: Buzz Solutions raised a $20M Series A in Aug 2026 — [Axios](https://www.axios.com/pro/climate-deals/2026/08/04/buzz-solutions-20m-grid-ai); Voxel a $44M Series B in 2025 — [Shopifreaks](https://www.shopifreaks.com/voxel-raises-44m-series-b-to-expand-ai-powered-workplace-safety-tech/); Intenseye a $64M Series B in 2024 — [Pulse 2.0](https://pulse2.com/intenseye-64-million-funding/amp/); Theator about $39.5M+ for surgical video — [HIT Consultant](https://hitconsultant.net/2022/07/25/theator-surgical-intelligence-funding/).
- Manufacturing: COPQ is commonly cited at 15 to 20% of revenue (vendor-relayed ASQ figure), and manual inspection catches about 60 to 90% of defects (vendor estimates) — [Oxmaint](https://oxmaint.com/industries/manufacturing-plant/manual-vs-automated-quality-inspection-manufacturing).
- Generic SAM 3 auto-labeling is not enough for fine-grained industrial classes such as crack types or electronics defects — [Roboflow docs](https://docs.roboflow.com/datasets/ko/annotate/annotate/ai-labeling/auto-label.md). Roboflow already chains SAM 3 with VLMs in consensus workflows (July 2026 blog) — [Roboflow blog](https://blog.roboflow.com/multi-model-auto-labeling-for-segmentation/).
- Solar: per-defect losses range from about 4 to 5% (cell cracks) to 33 to 66% (shorted bypass diode) — [IEA PVPS](https://iea-pvps.org/wp-content/uploads/2025/08/07_S.-Spataru_Framing-Drone-IRT-Conditions.pdf).
- Construction: 1,034 deaths in 2024, falls 389 — [BLS](https://www.bls.gov/opub/ted/2026/national-safety-stand-down-highlights-fall-hazards-in-construction.htm).
- Conservation: classification labor is an "information bottleneck" — [Fennell et al.](https://doaj.org/article/0ace75670ca4470c9a9be18572c2b496).
- Retail: about $1.157T is lost to out-of-stocks (IHL) — [Chain Store Age](https://chainstoreage.com/ihl-group-inventory-issues-cause-17t-annual-losses).
- Agriculture: up to 40% of crop production is lost to pests and diseases (FAO) — [WEF](https://www.weforum.org/stories/2021/06/climate-change-insects-pests-crops-agriculture/).
- SAM 3.1 coverage itself lists quality control (surface-area and defect analysis), logistics (tracking containers and pallets) and sports tracking as target uses, with a caution to validate before safety-critical decisions — [Mind-Verse](https://www.mind-verse.de/news/meta-sam-3-1-bild-video-analyse-api).

### Inferences
- The "differentiated wedge" in crowded domains (grid, safety, retail) is **zero-training, natural-language configurability**: "flag anyone under a suspended load" or "nests near energized parts." Incumbents train a model per class. SAM 3.1 + Muse lets the customer author new checks in English, which is a good live-demo moment (type a new rule, watch it apply).
- **Counting with identity** (tracking so each object counts once) is an underrated SAM 3.1 superpower for agriculture, retail, wildlife and solar. Image-only VLM pipelines double-count across frames.
- **Spec-PDF + video in one context window** (Muse Spark) is a strong differentiator for manufacturing and field service. The compliance logic comes from the customer's own documents, with no training.
- Least crowded with strong pain: video behavior analytics in conservation, spec-driven SMB QA, and XR app QA. Most crowded: workplace safety, grid inspection, retail shelf audit, sports cameras.

### Gaps
- No independent audits of incumbents' claimed savings. Most cost figures are vendor-sourced (flagged above).
- No struck-by fatality figure for 2024 was verified ([Construction Dive](https://www.constructiondive.com/news/constructions-deaths-fatality-rate-2024-hazards/812666/) lists only broader "contact incidents": 161).
- Primary ASQ COPQ source not located.

---

## Q2. What are the bottlenecks in robotics and embodied AI where SAM 3.1 + Muse could help?

### Takeaway
The live bottlenecks are (a) turning raw demonstrations into rich, trustworthy labels (subtasks, language, failures, object tracks), (b) cheap and reliable rewards and success detection for evaluation and RL, and (c) curating which data helps or hurts. SAM 3.1 provides object-centric geometry over time, and Muse provides semantic segmentation of the task and adjudication. Together they make a credible "robot data engine," which matches YC's 2026 "Data for the Real World" RFS. Known weakness: SAM 3 struggles with articulated robot parts, so track objects, not arms.

### Cited Findings
- The main constraint is the cost of collecting demonstrations, while language re-annotation of existing demos is comparatively cheap and boosts efficiency (DeMiAn preprint, ~62% less compute at 1M-clip scale to match a no-annotation baseline) — [arXiv 2605.17077](https://arxiv.org/pdf/2605.17077).
- A single teleop rig costs $40K+ in hardware, with one operator per robot (vendor) — [AXIS Robotics](https://axisrobotics.ai/resources/blog/best-robot-training-data-companies).
- 59% of physical-AI teams struggle with poor labels and 47% cannot identify harmful data (Voxel51 report via Pebblous) — [Pebblous](https://blog.pebblous.ai/blog/agibot-world-failure-annotation/en/).
- Sparse annotation adds about 15% to total data-collection time (older JUICER paper) — [arXiv 2404.03729](https://arxiv.org/pdf/2404.03729).
- The MLLM-based annotation framework RoboAnnotatorX (ICCV 2025) exists because manual annotation is expensive and doesn't scale — [CVF](https://openaccess.thecvf.com/content/ICCV2025/html/Kou_RoboAnnotatorX_A_Comprehensive_and_Universal_Annotation_Framework_for_Accurate_Understanding_ICCV_2025_paper.html).
- SAM 3 is weak on articulated robot geometry, arm-gripper separation and temporal consistency for robots (RobotSeg) — [arXiv 2511.22950](https://arxiv.org/pdf/2511.22950).
- SAM 3 is used as the text-guided perception server in the CaP-X embodied framework (forum post, unverified) — [HF discussion](https://huggingface.co/facebook/sam3/discussions/391). A 2026 shared-autonomy paper pairs SAM 2 tracking with a VLM for grounding — [arXiv 2607.17323](https://arxiv.org/pdf/2607.17323).
- Reward and success detection is an active 2026 research front: TOPReward (zero-shot progress and success; ManiRewardBench with 130+ tasks) — [arXiv 2602.19313](https://arxiv.org/html/2602.19313); RoboReward (2,800 real episodes with progress labels) — [arXiv 2601.00675](https://arxiv.org/pdf/2601.00675v1); Demo2Reward — [arXiv 2606.00083](https://arxiv.org/pdf/2606.00083). Earlier evidence showed zero-shot VLM success detection unreliable — [arXiv 2303.07280](https://arxiv.org/pdf/2303.07280).
- Open data at scale: OXE has 1M+ trajectories over 22 embodiments — [arXiv 2310.08864](https://arxiv.org/pdf/2310.08864); DROID is about 76K to 92K trajectories, with sources disagreeing — [RLDX-1](https://arxiv.org/pdf/2605.03269).
- YC Fall 2026 RFS "Data for the Real World" (Austin Tindle & Diana Hu) asks for dense data from sensors, robotics and autonomous systems — [explainx](https://explainx.ai/blog/yc-requests-for-startups-fall-2026). Third-party tallies put robotics/physical AI at about 32 of 208 recent YC companies — [Pinggy](https://pinggy.io/blog/what_yc_is_funding_in_2026/).

### Inferences
- Best robotics demo for a 1-day build: **cards 1 + 2 merged.** Annotate DROID/OXE episodes (subtasks, language, failures, object tracks), then score them with a SAM-geometry + Muse referee, validated against RoboReward labels. It is high on "technical ambition" (Indie) and has a clear buyer (Startup).
- **Object-centric progress** (distance and containment between tracked object masks) is a cheap, interpretable complement to token-probability rewards like TOPReward. It is a defensible "novel twist" to pitch.
- **Data curation** ("find the 5% of episodes where the grasp slipped") is a natural extension that answers the 47% "can't identify harmful data" pain.
- Sim-to-real, as video → sim scene → program (card 3), is the highest wow but the highest risk. Recommend it only if the team has MuJoCo/Genesis experience.
- Avoid prompting SAM 3.1 for robot links and joints (per RobotSeg). Use box prompts for the gripper or rely on robot proprioception from the dataset.

### Gaps
- No independent dollar figure for robot-data labeling cost (the search summary explicitly found none).
- Whether SAM 3.1's Object Multiplex fixes the temporal-consistency issues RobotSeg found in SAM 3 is untested.
- No commercial robot-eval or reward-model startups were identified in this session.

---

## Q3. Which "Build for Your World" niches are underserved by AI but have intense pain?

### Takeaway
The best niches combine intense, documented pain, users far from ML teams, and a Meta-specific modality advantage (glasses, multilingual voice, PDF + video context): blind/low-vision navigation and object finding, field technicians and tradespeople, small manufacturers, smallholder farmers speaking non-English or code-switched languages, and conservation field teams. Judges will reward a team member's firsthand story, so pick the niche your team actually lives in.

### Cited Findings
- Vision impairment affects at least 2.2B people, 1B of it preventable or unaddressed, with about $411B a year in productivity loss (WHO, Feb 10 2026) — [WHO](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment).
- 98.7% of Be My Eyes users who gave an opinion were positive about Be My AI (AFB survey, before the GPT-4o upgrade) — [AFB](https://afb.org/aw/fall2024/ai-usage-research). Be My Eyes reported 900K+ blind/low-vision users (2025 listing), and 1M+ is claimed for 2026 — [civictech.guide](https://directory.civictech.guide/listing/be-my-ai); [sheets.works](https://sheets.works/data-viz/be-my-eyes).
- Meta's Wearables Device Access Toolkit 1.0 provides camera capture, voice streaming and motion tracking on AI glasses, and Ray-Ban Display web apps can use device position, location and wrist motion — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/).
- Muse Voice Transcribe covers 25 evaluated languages with code-switching and streaming diarization — [models page](https://dev.meta.ai/docs/models.md).
- Small manufacturers: larger firms are 2.3x more likely to adopt AI (secondary) — [Digit Software](https://www.digit-software.com/blog/study-ai-adoption-in-us-manufacturing); the barriers are mainly organizational, and about 70% would consider a pilot — [FME assessment](https://norfolkdailynews.com/online_features/press_releases/national-assessment-identifies-a-practical-path-for-ai-adoption-in-manufacturing/article_14856071-4f70-58b8-bca9-af4917332a5a.html).
- Farmers: up to 40% of crops are lost to pests and diseases (FAO); Sub-Saharan Africa losses exceed $200B a year (IITA) — [Down to Earth](https://www.downtoearth.org.in/news/agriculture/at-least-40-global-crops-lost-to-pests-every-year-fao-77252); [Guardian NG](https://guardian.ng/?p=1080100).
- Field and wearable workers: the YC RFS "New Operating Systems for the Physical World" and "AI for the Aging Population" (assistive robotics, independence monitoring) — [explainx](https://explainx.ai/blog/yc-requests-for-startups-fall-2026).
- Amateur sports: budget-limited clubs fall back on cheaper tools (Veo, Kinovea) — [KI-Syndikat](https://www.ki-syndikat.de/tools/hudl/).

### Inferences
- **Glasses-native builds** (cards 14 and 15) are the most "Meta-aligned" Build-for-Your-World entries: they use Meta hardware SDKs plus SAM 3.1 plus Muse, which competitors' stacks cannot replicate end to end. Mitigate SDK setup risk with a phone-camera fallback.
- **Continuous tracking guidance** for BLV users (keep a lock on the target and update directional cues) is underserved compared with "describe this scene." That is where SAM 3.1 tracking is not swappable.
- **Multilingual, low-literacy farmer UX** (code-switched voice in; Muse Image picture card out) is a strong story for non-English-speaking teams.
- **Aging-in-place** (from the YC RFS) could adapt card 14 or 15 ("did grandma take her pills? where did she leave her glasses?"). It isn't carded separately, but it is a viable variant.

### Gaps
- No verified statistic on the skilled-trades labor shortage or field-service first-time-fix rates (would strengthen card 15).
- Be My Eyes 2026 user counts come from an opinion page; there is no official press release in the results.
- The Wearables Device Access Toolkit's real-world frame rate and latency to cloud APIs are unknown.

---

## Q4. What developer-tool or software opportunities exist?

### Takeaway
The clearest software opportunity is **visual QA**: Muse Wonder's computer use drives an app, SAM 3.1 diffs UI at the component level, Muse Spark triages, and Muse Code fixes. The web version is crowded. The **XR/VR app QA** variant is fresh and aligned with Meta's newly launched XR Operator and simulators. A second opportunity is a **"vision pipeline compiler"**: a Muse Code agent that turns a plain-English inspection spec into a deployed SAM 3.1 + Muse pipeline with an eval harness.

### Cited Findings
- Flakiness pain: Meta's E2E tests reportedly run at about 10% flakiness versus under 1% for unit tests, and Atlassian reportedly loses 150K developer hours a year (secondary) — [Panto](https://www.getpanto.ai/blog/flaky-test-statistics). Developers rank lost trust and wasted time as the worst impacts — [Eck et al.](https://arxiv.org/abs/2203.00483v4). A vendor relays a claim that 72% of failures are false positives (unverified) — [Bug0](https://bug0.com/blog/true-cost-of-flaky-tests-2026).
- Muse Wonder supports computer use, tool calling, structured output and search grounding — [models page](https://dev.meta.ai/docs/models.md).
- Muse Code is multi-agent by default, with parallel workers that write and test code in isolated workspaces. Meta XR Operator lets an agent interact with a running app in the simulator and verify results with screenshots. The Meta VR CLI gives agents platform docs, device debugging and profiling — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/).
- Meta acknowledges Muse Spark's gaps in long-horizon agentic and coding workflows — [Interesting Engineering](https://interestingengineering.com/ai-robotics/meta-muse-spark-ai-launch). Muse Wonder is the frontier option, scoring 52 on the Artificial Analysis index (Wonder Full 56) per secondary coverage — [BetaNews](https://betanews.com/article/muse-wonder-frontier-model-developers/).
- YC Fall 2026 RFS developer-tool asks include "Self-Maintaining APIs," "A Cloud for Small Software" and "Multiplayer AI" — [explainx](https://explainx.ai/blog/yc-requests-for-startups-fall-2026).

### Inferences
- Use **Muse Wonder or Muse Code** for agentic and coding loops, and **Muse Spark** for per-frame visual judgment (cheaper, and Meta itself flags Spark's agentic weakness).
- **XR QA agent** (card 9, XR variant): "the agent plays your Quest app in XR Simulator, SAM 3.1 segments the hands, controllers and UI panels, and Muse flags 'menu clips through wall' or 'grab target unreachable.'" This is likely uncrowded and judge-friendly for a Meta event.
- **Vision Pipeline Compiler**: the user writes "count cracked eggs per tray and alert above 2%," and Muse Code scaffolds a SAM 3.1 prompt set, Muse Spark rubric, eval on a sample set and a dashboard. It turns every card in Q0 into a reusable product and is a strong Startup-track platform play, but its demo is less visceral.
- Screen-recording bug report → reproducible test (SAM 3.1 tracks the cursor and UI elements; Muse writes a Playwright script) is another variant. [I] It is likely crowded (not verified).

### Gaps
- No data specific to visual-regression false positives (search found only general flakiness data).
- Whether SAM 3.1 segments synthetic UI imagery well is unverified. Test before committing.
- The Meta XR Operator API surface and availability to hackathon participants were not checked.

---

## Q5. Which ideas have a credible startup path (Startup track) vs pure creativity and wow (Indie track)?

### Takeaway
Startup track: ideas with a budget-holding buyer, recurring volume and a production story (QA copilot, robot data engine, grid/solar inspection, field-service copilot, shelf audit, visual QA). Indie track: ideas whose two-minute video produces an emotional or "how is that possible" reaction (glasses guidance for BLV users, Watch-and-Do, TrapTales, Sideline, Defect Forge, OR Rewind). Two ideas straddle both convincingly: the Robot Data Engine (cards 1+2) and Defect Forge (card 4).

### Cited Findings
- Startup-track judging is on technical execution and production robustness, and Indie on creativity, technical ambition and whether it works (from the assignment brief; event rules are covered elsewhere). Meta's recap confirms indie and startup tracks with a $1M cash pool and free Model API credits — [Connect recap](https://developers.meta.com/blog/meta-connect-recap/). An aggregator lists the event as 10 days, Oct 26 to Nov 4 2026 — [Internshala](https://internshala.com/competitions/?p=12509).
- Market validation for the startup-track domains: Buzz Solutions $20M (grid) — [Axios](https://www.axios.com/pro/climate-deals/2026/08/04/buzz-solutions-20m-grid-ai); Voxel $44M (safety) — [Shopifreaks](https://www.shopifreaks.com/voxel-raises-44m-series-b-to-expand-ai-powered-workplace-safety-tech/); Theator about $39.5M (surgical) — [HIT Consultant](https://hitconsultant.net/2022/07/25/theator-surgical-intelligence-funding/); retail out-of-stocks at about $1.157T — [Chain Store Age](https://chainstoreage.com/ihl-group-inventory-issues-cause-17t-annual-losses).
- YC 2026 RFS themes that map to these ideas: "Data for the Real World" (card 1/2), "New Operating Systems for the Physical World" (cards 10 and 15), "AI for the Aging Population" (card 14 variant) — [explainx](https://explainx.ai/blog/yc-requests-for-startups-fall-2026); the Summer 2026 RFS includes "Physical AI" — [RoundFunded](https://www.roundfunded.com/blogs/yc-summer-2026-request-for-startups-15-categories).

### Inferences

**Ranking matrix (my judgment; 5 = best)**

| # | Idea | Meta-model hero (SAM 3.1 / Muse essential) | 2-min wow | 1–1.5 day feasibility | Crowding (5 = open) | Best track |
|---|---|---|---|---|---|---|
| 1+2 | Robot Data Engine (annotate + referee) | 5 | 4 | 4 | 4 | Startup / Indie (Frontier) |
| 4 | Defect Forge (Muse Image + SAM labels) | 5 (all 3 models) | 4 | 3 | 4 | Both (Frontier) |
| 5 | Inspector-in-a-Phone (spec PDF QA) | 5 | 4 | 4 | 3 | Startup (Frontier / Your World) |
| 14 | Find-and-Guide on Meta glasses (BLV) | 5 (+ glasses SDK) | 5 | 3 | 3 | Indie (Your World) |
| 15 | Field-tech glasses copilot | 5 (+ glasses SDK) | 4 | 3 | 3 | Startup (Your World) |
| 3 | Watch-and-Do (video → sim robot) | 4 | 5 | 2 | 4 | Indie (Frontier) |
| 11 | TrapTales (wildlife video) | 4 | 4 | 5 | 3 | Indie (Your World) |
| 6 | LineSight (grid) | 4 | 3 | 5 | 2 | Startup (Frontier) |
| 7 | Solar Fault Hunter | 4 | 3 | 4 | 2 | Startup (Frontier) |
| 9 | Visual QA agent (XR variant) | 4 | 3 | 3 | 2 web / 4 XR | Startup (software) |
| 10 | Site Replay (construction) | 4 | 4 | 3 | 2 | Startup |
| 13 | Sideline (amateur sports) | 5 (multi-object tracking) | 5 | 3 | 2 | Indie |
| 16 | Leaf-Level Scout (agri, multilingual) | 4 | 4 | 4 | 3 | Indie / Your World |
| 17 | Aisle Walk (retail) | 4 | 3 | 3 | 2 | Startup |
| 12 | OR Rewind (surgical) | 4 | 4 | 2 | 2 | Indie |
| 8 | GrainCounter (materials) | 3 | 3 | 3 | 4 | Indie (Frontier) |
| 18 | Damage Ledger (disaster) | 3 | 3 | 5 | 2 | Indie |
| 19 | Dock Witness (logistics) | 4 | 3 | 3 | 3 | Startup |

- **Recommended shortlist for a 1 to 1.5 day build:**
  1. **Robot Data Engine** (Startup or Indie, Push the Frontier): public data, offline-cacheable, quantifiable result (agreement with RoboReward labels), YC-RFS aligned, and SAM 3.1 tracking is the hero.
  2. **Inspector-in-a-Phone / Defect Forge combo** (Startup, Frontier): "configure inspection with your drawing PDF, bootstrap defects with Muse Image." Uses all three flagship Meta models.
  3. **Find-and-Guide on Meta glasses** (Indie, Your World): the most emotional demo, Meta-hardware-native, with continuous tracking that cannot be swapped out.
  4. **TrapTales** (Indie safety pick): lowest risk, strong visuals, clear step beyond MegaDetector.
- **Demo-craft tips:** [I] Pre-compute SAM 3.1 video results for the hero clip (latency and limits unknown); show a live "type a new noun phrase → instant re-segmentation" moment to prove zero-training; always show the structured output (JSON, report, PDF) to signal production-readiness for Startup judges; show one before/after metric (minutes saved, agreement percent, defects caught).
- **"Not swappable" framing for judges:** [I] (a) SAM 3.1 is the API-served model on this platform that returns per-instance masks with persistent IDs from a noun phrase in video ([models page](https://dev.meta.ai/docs/models.md)), and the counting, tracking and geometry steps depend on that; (b) Muse Spark/Wonder take video, PDF, image and audio in one 1M-token context, so spec + footage + manual are reasoned over jointly; (c) Muse Image's multi-reference edits create the counterfactual data; (d) the Meta glasses toolkit supplies first-person capture.

### Gaps
- Exact judging weights and any requirement that projects use specific Meta models were not verified here (covered by the rules researcher).
- Muse Image's edit fidelity for tiny industrial defects is unverified (the competitive edit benchmark is from Meta-internal tests relayed by third parties — [Flowith](https://flowith.io/ai-models/meta-muse-image/)).
- Whether the hackathon's free Model API credits cover high-volume SAM 3.1 video processing is unknown.
