# Close the Loop to Win Meta's Hackathon

To win, build a closed loop in which **three or more Meta models each do real work**: SAM 3.1 sees and measures, Muse Spark (or Muse Wonder) reasons over long multimodal context, and Muse Image or a tool generates or acts. Aim it at an uncrowded physical-world domain, back it with **one measured number**, and sell it with a video under three minutes whose "aha" arrives by 0:30. Our first-ranked build is **Defect Forge**. Muse Image paints realistic defects onto photos of a good part, SAM 3.1 labels each one to the pixel, and Muse Spark reads the customer's spec, rejects unrealistic samples, and then uses the forged examples to inspect real parts, with recall measured on a public defect set. It ranks first for three reasons: it gives a central role to Meta's least-used model (only 5 of 305 visible entries mention Muse Image), every step can be cached, and it sits in a thin category (about 9 manufacturing entries). **DemoScribe** ranks second: it automatically annotates and referees robot demonstration videos, and it has the deepest technical story but faces stiffer robotics competition. **Find-and-Guide** ranks third: SAM-tracked audio cues steer a blind user's hand to a named object. It has the highest emotional and viral ceiling, but also the most live-latency risk and the most exposure to the runtime-model rule. Judging is a pass/fail check, then 0–10 scoring on **Impact 30%, Use of Meta AI Tooling 25%, Demo 25%, Technical Depth 20%**, then a live final for the **top 5 per track**. Exactly five places per track are paid ($25K–$150K Indie, $25K–$250K Startup), so reaching the final is the whole game. Every model your project calls at runtime must be a Meta model. You submit a video of at most 3 minutes that shows live Meta calls, plus a public repo that runs from its README, by **Wed Nov 4, 9:00 PM ET (02:00 UTC, 7:30 AM IST on Thu Nov 5)**. Avoid the kickoff's ten "anti-projects" and the three saturated clusters: agent receipts and verification (~57 repos), photo-to-inspection reports (~16+) and video procedure checkers.

## Four artifacts, one runtime rule and a 30/25/25/20 rubric decide the outcome

### Rules that can disqualify a good project

The binding text is the "Hackathon Terms & Conditions ('Official Rules') and Event Waiver", dated Oct 25, 2026. It renders only in a real browser on the Cerebral Valley waiver page ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). Entrants must be 18 or older. Excluded are anyone under sanctions, anyone located in the listed countries and regions, and Meta or Cerebral Valley staff and their families. Participation is capped at **20,000 accepted applicants** and is virtual only ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). Each participant, and each project, may enter **one track only**. The **Indie** track is open to individuals and students in teams of up to four. The **Startup** track is for "technical founders building a product," and its Representative must be an active employee of the startup ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). Unless you run a real company, enter Indie, which is judged on "creativity, technical ambition, and whether it works." Startup is judged on "technical execution and whether it holds up in production" ([dev.meta.ai event page](https://dev.meta.ai/events/global-hackathon)). You keep your IP, but you grant Meta and Cerebral Valley a perpetual, irrevocable, royalty-free license to use the submission for any purpose, and nothing you share is treated as confidential. Submissions must be original, solely owned and non-infringing. Open-source components are allowed if their licenses are followed and your work builds on them ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)).

The rule most likely to sink a strong project is model purity. The Official Rules require building with Meta AI products, and Stage 1 judging is a pass/fail check on whether the project "use[s] Meta AI products." On Oct 31 an organizer answered on Discord that **"Every model your project calls at runtime must be a Meta model."** The same answer confirmed that coding with Claude, Codex or OpenCode is fine and does not need to be disclosed ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10); [kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)). That rules out ElevenLabs or OpenAI text-to-speech, Whisper, GPT or Claude calls, and non-Meta embedding models. At least one visible entry already uses ElevenLabs for spoken replies and appears to be in violation ([meta-hack](https://github.com/meta-ai-hackathon/meta-hack)).

Our reading, which is not an organizer statement, is that the rule also covers local learned models such as YOLO, MediaPipe or neural OCR. Classical code (OpenCV geometry, ffmpeg, Web Audio) is safe. Meta's API offers speech-to-text (Muse Voice Transcribe) but **no text-to-speech** ([dev.meta.ai Models](https://dev.meta.ai/docs/models)), so any idea that talks back sits in a gray zone. Ask in Discord #questions before relying on browser or operating-system speech. Organizers did confirm that Muse Image output can be used in the video and repo without on-screen credit ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)).

Prior code is not banned outright, but the kickoff told teams to "Show only what your team built during the event; judges score from it." One participant's notes say the submission must state where the new work starts, though that is unverified ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides); [lovinta/asih checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)). Starting a fresh repo now avoids the question.

### What to submit, and when

| Item | What is required | Source |
|---|---|---|
| Cerebral Valley portal entry | Submit at cerebralvalley.ai/e/meta-ai-developer-hackathon/hackathon/submit and list every teammate. Editable until the deadline; no edits after | [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver); [kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides); [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10) |
| Demo video | 3 minutes. Show only work built during the event, and show the working product "with the live Meta model calls visible." Unlisted YouTube is fine | [kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides); [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10) |
| Public GitHub repo | Must be public, must open in a logged-out browser, and must run from its setup instructions. Judges "can test with their own keys." A demo mode is fine if the README explains it and the live path still works | [kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides); [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10) |
| Live URL | Optional: "judging doesn't depend on it" | [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10) |
| Form fields | Team name, members, track, problem statement (theme), Most Viral X post link, description, repo, video, "Use of Meta products," "Why Meta's models matter," feedback on Meta products, and optional partner feedback | [naqsh submission notes](https://github.com/lleoparden/naqsh/blob/main/docs/submission-notes.md) |
| Deadline | Wed Nov 4, 9:00 PM ET. The kickoff advised: "Don't wait for the last hour" | [kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides) |

US daylight saving time ended Nov 1, so 9:00 PM ET is **02:00 UTC, or 7:30 AM IST on Thu Nov 5**. Plan to submit three hours early. Participants are budgeting mid-afternoon ET buffers against portal load from up to 20,000 people ([seeyable plan](https://github.com/nmheinrich/seeyable/issues/25)). The X post for Most Viral must already exist and be linked before you submit, even though engagement keeps counting until Nov 8. The three Meta-specific form fields map directly onto the 25% tooling criterion. The strongest visible entry fills them with each model's role and measured numbers: roughly $0.03 per processed page, recall figures, and an API friction log ([naqsh](https://github.com/lleoparden/naqsh)).

### How judging works and what it pays

| Criterion | Weight | Official wording (excerpt) |
|---|---|---|
| Impact | 30% | "real-world potential … who benefits, how much it matters, whether it could become something people use, and whether it fits one of the problem statements" |
| Use of Meta AI Tooling | 25% | "how creatively the team used Meta's AI tooling, whether they went beyond a basic integration, and whether they surfaced unexpected capabilities" |
| Demo | 25% | "a working, impressive demo, whether the product holds up live, and the quality of the demo video" |
| Technical Depth & Execution | 20% | "whether the engineering is sound and thoughtfully refined and the Project demonstrates real craft" |

Source for the rubric: [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver).

Judging runs in three stages: a pass/fail check that the project fits a theme and uses Meta AI products, then scoring from 0 to 10 on the rubric for every passing project, then a **live final on Nov 9** where judges watch the **top 5 per track** and rank them ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)). Prizes are **Indie $400K (1st $150K, 2nd $100K, 3rd $75K, 4th $50K, 5th $25K)** and **Startup $550K (1st $250K, 2nd $150K, 3rd $75K, 4th $50K, 5th $25K)**. They are paid through Tremendous within 30 days of verification ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). Each track has five paid places and five finalists, so a finalist slot is worth at least $25K. Stage 2 decides the contest, and Stage 2 is judged mostly from the video and the repo. Judges have not been named publicly.

| Bonus prize (up to $50K in total; does not reduce track prizes) | Amount, per participant notes (unverified) | Mechanics |
|---|---|---|
| Most Viral | $20K | Highest likes + reposts + comments on the X post linked in the submission, counted through Nov 8 end of day. No hashtag required |
| Best Build on Open Weight Models | $10K | Muse Glimmer or Muse Spark Open |
| Community Vote | $10K | Public gallery, one vote per verified account, winner announced Nov 16 |
| Best Agentic Use-Case | $5K | Not described |
| Best Creative Build | $5K | "most original use of Muse Image or Muse Wonder" |

The official text says only "up to $50,000 in the aggregate" ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)). The category names and amounts come from one participant guide ([meta-hack grading criteria](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/grading%20criteria.md)), and a second participant's notes confirm the names ([lovinta/asih checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)). The mechanics come from organizer answers ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)).

### What organizers told you not to build

The kickoff slide titled "Anti-projects – Skip these overdone projects" lists ten types to skip: **AI-generated medical advice, simple image analyzers, dashboards as the main feature, AI job-application screeners, personality analyzers, basic RAG apps, Streamlit apps, "AI for Education" chatbots, AI nutrition coaches, and sports analyzers or coaches** ([kickoff slides](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)). A footnote says the list is not complete and that medical advice includes mental-health advisors and skin-blemish detectors. One participant's copy adds "anything political or involving war," an item that is not on the slide and is unverified ([meta-hack restrictions](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/restrictions.md)). The two themes, as copied from the signed-in details page, are **Build for Your World** ("Solve a problem you know firsthand, free up time and mental space, and make something possible that wasn't before") and **Push the Frontier** ("Give a machine a new capability, accelerate a scientific experiment, or unlock a better way to understand and control a physical system") ([details-page copy](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/details-page-full.md)).

Workshops covered building a multimodal agent, "verifiable agent best practices," and specialized intelligence on Fireworks ([meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md)). Meta's official legal-agent workshop repo builds a verification layer that runs "outside the agent's control" ([meta-models/legal-agent-workshop](https://github.com/meta-models/legal-agent-workshop)). The signal is consistent: multimodal, agentic, verifiable and physical-world, and never a thin wrapper.

Each participant gets **$150 in Model API credits**. Claim them before the deadline, with a credit card on the account ([Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver); [lovinta/asih checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)). Partner credits are inconsistent across sources. Fireworks appears as $100 on the public page and $25 on the signed-in page. Baseten ($100) and Modal ($100) are reportedly limited to the first 2,000 and first 1,000 participants respectively, requested through Discord #resources ([CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon); [details-page copy](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/details-page-full.md); [rules summary](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/rules-summary.md)). Three things remain unconfirmed and are worth two minutes of a signed-in check: the exact problem-statement wording that Impact scoring refers to, the bonus amounts, and any last-minute change posted in Discord #announcements.

## Meta's stack rewards chaining SAM 3.1, Muse Spark and Muse Image, not single calls

One naming fact shapes every plan. **Muse Wonder is a frontier agentic model that outputs text. It is not a video or world model.** Muse Image is Meta's only image generator, and Meta offers no generative video model on its API ([dev.meta.ai Models](https://dev.meta.ai/docs/models)).

| Model (API ID) | Input → output | Price | Why it matters for a winning build | Watch out for |
|---|---|---|---|---|
| Muse Spark 1.3 (`muse-spark-1.3`) | Text, image, video, audio, PDF → text; 1,048,576-token context | $1.25 in / $0.15 cached / $4.25 out per M tokens | Default model. Near-lossless long-context retrieval: MRCR 98.1 at 512K–1M tokens, vs 73.8 for GPT-5.6 Sol. Takes video with its soundtrack in one call. Tool calling, structured output, search grounding, and point/box grounding on a 0–1000 grid | At max effort, ~48.5 s before the first answer token. Audio is "not fully supported" (use 1.2 for audio) |
| Spark 1.3 Contributor | Same | $0.10 / $0.002 / $0.20 | About 12x cheaper | 150 requests per minute (RPM). Your content may be used to train Meta models. No max effort |
| Muse Wonder (`muse-wonder-1.0`) | Same → text | $4 / $0.20 / $20 | Frontier agentic model; Meta's recommended model for computer use; leads on legal and long-horizon software-engineering benchmarks | Preview. The API model is not Wonder Full, which is available only in Muse Code. Not available in South Korea |
| Muse Image (`muse-image-1.0`) | Text + images → image | $0.01 per image | Edits, multi-turn refinement, multi-image composition, series consistency. Agentic: runs image search, web search and a shell before rendering | 150 RPM. No masks, seeds or partial images. `size` sets aspect ratio only |
| SAM 3.1 (`sam-3.1`) | Noun phrase, or box/point prompts, plus image or video → boxes + masks | $2.50 per 1K images; $0.20 per 1K video frames (50-frame minimum) | Open-vocabulary segmentation. Tracks objects with persistent IDs across up to ~10 minutes of video. "Object Multiplex" is ~7x faster at 128 objects | One noun phrase per request. At most 16 objects with box/point prompts. Video must be MP4/MOV encoded as H.264/H.265 |
| Muse Voice Transcribe (`muse-voice-transcribe-1.0`) | Audio → text | $0.18 per audio hour | 25 languages, handles mixed-language speech, realtime WebSocket with speaker turns | No text-to-speech, no word-level timestamps |
| Muse Spark Open (open weights) | Text, image, video, audio → text; 1M context | ~$1.25 / $4.25 via hosted providers | Supports an open-weights story via Fireworks, Baseten or Together | The 816B mixture-of-experts model needs ≥700 GB of GPU memory to self-host. Requires "Built with Muse Spark Open" attribution |
| Muse Glimmer (open weights) | Text + image → text; 128K context | Self-hosted; Together charges $0.35 / $1.50 | Apache 2.0, 30B dense. Runs on one GPU or a Mac Mini (~18 GB at 4-bit) | Not on the Meta API. No video input. One reviewer called it underwhelming |
| Muse Code | Terminal coding agent | API key or subscription | Multi-agent, headless `muse exec`, TypeScript SDK | Uses the `META_API_KEY` variable, not `MODEL_API_KEY` |

Sources: [Models](https://dev.meta.ai/docs/models); [Pricing](https://dev.meta.ai/docs/pricing-rate-limits); [DataCamp](https://www.datacamp.com/blog/muse-spark-1-3); [Artificial Analysis](https://artificialanalysis.ai/models/muse-spark-1-3/providers); [VentureBeat on Wonder](https://venturebeat.com/technology/metas-new-muse-wonder-and-muse-wonder-full-models-achieve-frontier-performance-but-only-the-weaker-one-is-available-via-api); [Image generation](https://dev.meta.ai/docs/image-generation.md); [SAM overview](https://dev.meta.ai/docs/sam/overview.md); [SAM 3.1 release notes](https://raw.githubusercontent.com/facebookresearch/sam3/main/RELEASE_SAM3p1.md); [Spark Open model card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B); [VentureBeat on Spark Open](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops); [Glimmer docs](https://dev.meta.ai/docs/muse-glimmer/); [The Register](https://www.theregister.com/a/5285666); [Muse Code docs](https://dev.meta.ai/docs/muse-code.md).

The rubric explicitly rewards having "surfaced unexpected capabilities." The platform has five that a single chat call never shows: **retrieval over a million tokens**, so a whole manual plus a long video fit in one call; **native video understanding with its soundtrack** in one Spark request; **search-grounded image rendering**, where Muse Image looks things up before it paints; **pixel-exact, identity-stable tracking from a noun phrase**, as SAM 3.1 follows each named object through a video; and **coarse grounding refined into exact masks**, where Spark's 0–1000 grid gives a rough location and SAM sharpens it to the pixel. Meta's own launch demos follow the same arc from perception to structured understanding to action: a Facebook Marketplace listing built from a smartphone video, and computer use that plans a dinner party ([Meta AI blog](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)). Spark 1.3 is "trained to report hitting hurdles rather than fabricating outcomes" ([Meta research blog](https://research.meta.ai/blog/introducing-muse-spark-1-3)). Meta's cookbook already validates several combinations: SAM with Voice Transcribe for headlocked captions, pet video turned into stickers, overlays pinned to object locations ("perception grounding"), and a local Glimmer agent that asks before calling Spark ([Cookbook](https://dev.meta.ai/docs/cookbook.md)).

| Gotcha | Consequence | Workaround |
|---|---|---|
| `tool_choice` accepts only "auto" | "required", "none" or a named tool returns HTTP 400 | Use a `text.format` JSON schema for deterministic steps; handle plain-text replies |
| Reasoning tokens count toward `max_output_tokens` | Visible output is truncated or empty | Set the output limit to at least 4,000 tokens |
| Effort `none` returns 400; `max`/`xhigh` take 40+ s before the first token | The UI freezes | Use `low` or `medium` on interactive paths, and stream |
| The SDKs do not read `MODEL_API_KEY` | Authentication errors | Pass `api_key=` explicitly, with base URL `https://api.meta.ai/v1` |
| Using the Anthropic SDK | Wrong base URL, or empty text | Use base `https://api.meta.ai` (no /v1), pass the key as `auth_token`, and skip the `redacted_thinking` block |
| Strict schemas | 400 on recursion, `allOf` or `oneOf` | Keep schemas flat, make every key required, set `additionalProperties:false` |
| Images outside the `user` role are ignored; at most 50 per request | Context is silently lost | Put images in user turns; keep batches of example images at 50 or fewer |
| Spark accepts MP4 video only; SAM accepts MP4/MOV in H.264/H.265, with no VP9 or WebM | Browser MediaRecorder output (WebM) fails | Transcode with ffmpeg `-movflags +faststart`, or send JPEG frames instead |
| SAM takes one noun phrase per request; commands, lists and negation are unreliable | Objects are missed | Send one request per concept; fall back to box or point prompts |
| SAM coordinates are in pixels after EXIF rotation; an aspect-ratio mismatch returns 400 | Phone photos break | Normalize EXIF orientation before sending |
| SAM returns empty output when nothing matches; frame order is not guaranteed for box/point prompts | Crashes, or overlays in the wrong order | Treat empty output as "not found"; key results by the frame marker |
| Muse Image rejects `mask`, `seed` and `partial_images`; passing `web_search` as a tool returns 400 | No inpainting, no reproducibility | Crop a patch, edit it, paste it back, compositing through SAM masks; pass the search flags via `extra_body` |
| The 0–1000 grounding grid can return 1001 | Overlays are off by one | Clamp values; divide by 10 to get CSS percentages |
| Rate limits are per team and per model (Muse Image is 150 RPM) | 429 errors under batch load | Back off with jitter from ~500 ms and honor `Retry-After` |
| Computer use: Meta hosts no virtual machine | You must run Playwright or pyautogui yourself | Keep computer-use flows scripted and short |
| Uploaded files never expire by default | User data lingers | Set `expires_after` |
| Omitting `model` may silently fall back to 1.1 | Silent downgrade | Always pin the model ID |

Sources: [Tool calling](https://dev.meta.ai/docs/tool-calling); [Reasoning](https://dev.meta.ai/docs/reasoning); [Structured output](https://dev.meta.ai/docs/structured-output); [SDKs](https://dev.meta.ai/docs/sdks); [Image understanding](https://dev.meta.ai/docs/image-understanding.md); [Video understanding](https://dev.meta.ai/docs/video-understanding.md); [SAM segmenting](https://dev.meta.ai/docs/sam/segmenting.md); [Image generation](https://dev.meta.ai/docs/image-generation.md); [Pricing](https://dev.meta.ai/docs/pricing-rate-limits); [Computer use](https://dev.meta.ai/docs/computer-use.md); [File handling](https://dev.meta.ai/docs/file-handling.md); [promptfoo](https://www.promptfoo.dev/docs/providers/meta/).

Credits are not the constraint. By our arithmetic from the price sheet, $150 buys roughly 120M Spark input tokens, or 15,000 Muse Image generations, or 750,000 SAM video frames, or 7.5M Wonder output tokens. Rate limits are the real constraint, especially Muse Image's 150 RPM. For the open-weights bonus, self-hosting Spark Open (≥700 GB of GPU memory) is unrealistic in a day, which leaves two realistic routes: calling Spark Open through Fireworks, Baseten or Together by changing the base URL, or running Glimmer locally through Ollama or llama.cpp, the pattern Meta's own "local agent that asks first" cookbook models ([VentureBeat on Spark Open](https://venturebeat.com/technology/meta-unveils-muse-spark-open-the-new-top-u-s-open-weights-model-and-it-runs-on-two-paired-mac-desktops); [Cookbook](https://dev.meta.ai/docs/cookbook.md)). Only about three visible entrants have done a genuine fine-tune, one of them a QLoRA of Glimmer 30B on Modal ([natanr123/preflight](https://github.com/natanr123/preflight)), and past Meta winners show that fine-tuning is not needed to place.

The fastest wiring is the OpenAI SDK pointed at `https://api.meta.ai/v1`, using the Responses API with `muse-spark-1.3`, `reasoning.effort` set to low or medium, streaming, and a `text.format` schema. Add Meta's `meta_sam_parser` (pip) or `@meta-sam/parser` (npm) to read SAM output ([Quickstart](https://dev.meta.ai/docs/quickstart); [SDKs](https://dev.meta.ai/docs/sdks)). Muse Spark 1.3 itself carries one oddity: Artificial Analysis lists it as deprecated, while Meta's docs still call it "recommended for new work." Pin the model ID either way ([Artificial Analysis](https://artificialanalysis.ai/models/muse-spark-1-3/providers)).

## Past winners were domain insiders shipping multimodal agents with a measured number

Meta's own developer hackathons rewarded technical ambition delivered through vision, voice and agents. At the May 2024 Llama 3 hackathon with Cerebral Valley (354 attendees, 51 projects), first place went to **OpenGlass**, smart glasses costing roughly $20 that identify what the wearer sees, ahead of a multi-agent debate arena and an activation-ablation jailbreak ([Meta AI blog](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/)). At LlamaCon 2025 (44 projects, two judging rounds down to a top six), **OrgLens** won with a knowledge graph and "digital twins" of colleagues built from Jira, GitHub and internal docs; **Compliance Wizards** combined fraud analysis with a voice assistant; and **Llama CCTV Operator** detected video events defined in plain language "with no fine-tuning." The "Best Llama API usage" award went to **Geo-ML**, a geologist's tool that turns geology reports of about 400 pages into 3D subsurface models using long context plus multimodality, while the team that fine-tuned Llama 4 Maverick did not place ([Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/)). Meta's "Impact" events went to health, public services and accessibility: Guardian for NHS triage, Gripmind's robotic arm controlled by brain signals or voice, and Adapt.AI for neurodivergent learners ([Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/); [Meta Newsroom Brazil](https://about.fb.com/br/news/2024/11/primeiro-llama-impact-hackathon-no-brasil-reforca-a-importancia-do-codigo-aberto-para-ia)). The 2026 anti-project list now closes the medical-advice and education-chatbot lanes, so those precedents carry over only through accessibility and physical-world builds.

The single best predictor is Cerebral Valley's own recent virtual events for Anthropic, because Meta's rubric visibly uses the same template. The "Built with Opus 4.6" Stage 1 rubric weighted **Demo 30%, Impact 25%, model use 25% and Depth 20%**. It asked for "going beyond basic integration" and "surfacing surprising capabilities" ([rules copy](https://huggingface.co/datasets/introvoyz041/postvisit/blob/main/data/docs/hackathon-rules.md)). Meta's version swaps the Impact and Demo weights and keeps nearly identical language.

The two Anthropic rounds were similar in scale to this one. Opus 4.6 went from 13,000+ applicants to 227 projects to 6 finalists ([Cerebral Valley on X](https://x.com/cerebral_valley/status/2026066211482857844)). Opus 4.7 drew 20,000+ applicants and about 250 projects ([EdTech Innovation Hub](https://www.edtechinnovationhub.com/news/a-doctor-a-carpenter-and-a-teacher-win-anthropics-global-opus-47-hackathon)).

Their winners share one shape: a domain insider builds a multi-step agent that does a professional's job on real artifacts, then proves it with a number. In the Opus 4.6 round, **CrossBeam**, built by a personal-injury lawyer, turned blueprints and correction letters into permit action plans; **Elisa** shipped 76 commits, 39,000+ lines and 1,500+ tests in 30 hours; and **TARA** turned dashcam footage into a road-investment appraisal, claiming it compressed weeks of work into about 5 hours ([Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon)). In the Opus 4.7 round, **MedKit**'s agentic grader scored simulated patient encounters against clinical guidelines and arrived with pilot plans from three medical faculties; **Wrench Board** diagnosed circuit boards from schematics; and **MaestrIA** raised its eval score from **74% to 81% against a master carpenter's judgment** ([Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)). Side prizes went to real-time, playful instruments such as Conductr, which generates musical notes every 15 ms, and Virtual Puppet Theater. That creative archetype wins bonuses more often than main places.

Google's events add two consistent signals. First, accessibility and perception win every year. Vite Vere won twice, Gaze Link won for ALS patients, and in 2025 **Gemma Vision**, an assistant for blind users built on a chest-mounted phone, took first in the Gemma 3n challenge ([Google Developers Blog](https://developers.googleblog.com/en/announcing-the-winners-of-the-gemini-api-developer-competition/); [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/)). Second, judges reward closed loops and quantified proof. The Aug 2026 Gemma 4 Good winner was praised for its "closed-loop data engine," and a category winner reported a **19.0% word error rate against a 32.7% baseline** ([Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/)).

| Pattern | Evidence | What it means for this build |
|---|---|---|
| A domain artifact, not a chat | CrossBeam, TARA, Geo-ML, Wrench Board ([Claude blog](https://claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon); [Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/)) | Output a professional deliverable: a dataset, report or work order |
| One measured number | MaestrIA 74% → 81%; Gem-Care word error rate 19.0% vs 32.7% ([Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon); [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/)) | Build an eval of 20–40 items by D−14 (14 hours before the deadline) |
| Show off the newest model's headline capability | Geo-ML's long context; CCTV Operator's zero-shot video ([Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/)) | Feature SAM 3.1 video tracking, Muse Image's agentic editing, or Spark's 1M context |
| Physical-world builds place high | OpenGlass 1st; Gripmind 2nd; GEM-4 1st ([Meta AI blog](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/); [Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/); [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/)) | Put real objects or real footage on screen |
| Fine-tuning is optional | CCTV Operator won with no fine-tuning; the fine-tuning team (Concierge) did not place ([Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/)) | Spend your hours on the loop and the eval, not on training |
| Screening is video-first | "The video demo is the primary lens"; the aha should land about 30 s into the demo ([Kaggle rules copy](https://gist.github.com/bigsnarfdude/19be893b58c844cb43b2d30d07f31af0); [Nebius updates](https://nebiusglobalaihackathon.devpost.com/updates)) | Script the video before writing code |

The same sources name how strong teams lose: pivoting after hour 12, building without deploying, leaving the repo empty until a final push, chaining five LLM calls where one would do, building authentication and settings before the core loop works, and recording the video too late to re-record ([lablab.ai](https://lablab.ai/guide/how-to-win-an-ai-hackathon)). Many events also tell judges to stop watching at 3:00 ([UniHack](https://unihack.notion.site/How-to-submit-your-project-2e05dc7357fb4d3ba3e23f51207f996a)). With about 30 hours left, the most likely failure is overscoping until the work eats the time reserved for the video.

## Receipts and photo-reports are saturated; manufacturing, Muse Image and glasses are wide open

A GitHub scan on Nov 3 found **329 repos created since Oct 20** that mention the hackathon or Meta's new models. 305 of them have descriptions, and the muse-spark topic alone lists 153 repos ([GitHub muse-spark topic](https://github.com/topics/muse-spark)). Model usage is lopsided: 64 descriptions mention SAM 3.1 and 36 mention voice, but only **14 mention open weights, 8 mention Muse Wonder and 5 mention Muse Image**. With up to 20,000 participants, this visible sample is probably well under 10% of final submissions. Treat the shares as a signal of crowding, not a census. The public gallery was still empty on Nov 3.

| Cluster | Visible count | Examples | Verdict |
|---|---|---|---|
| Agent verification, receipts, guardrails | ~57, plus ~22 on guards and prompt injection | [attest](https://github.com/Master07/attest), [sparkguard](https://github.com/ReARCLabs/sparkguard), [witness-agent-receipts](https://github.com/yatharthchopra2424/witness-agent-receipts) | Most saturated; inward-facing, so Impact is weak |
| Photo → inspection, hazard or repair report (SAM 3.1 + Spark) | ~16+, including duplicates | [aegis-home](https://github.com/KarlaPocasangre/aegis-home) vs [AgeProof-AI](https://github.com/taeefnajib/AgeProof-AI); [viaguard](https://github.com/Foxcrack/viaguard); [fieldfix](https://github.com/mangeshraut712/fieldfix) | Crowded, and close to the "simple image analyzer" anti-project |
| Video → learn a procedure, then verify the steps | Several, including duplicates | [processlens](https://github.com/DravenDou/processlens), [proofstep](https://github.com/desilva23/proofstep), [backstep](https://github.com/PhiBao/backstep) vs [rewind](https://github.com/tejaschaudhari131/rewind) | Crowded |
| Robotics and physical systems | ~14 | [athlete2humanoid](https://github.com/PandaGrdn/athlete2humanoid), [video2urdf](https://github.com/SungHyunC/video2urdf), [muse-qc-cell](https://github.com/StefanRohringer/muse-qc-cell) | Ambitious competitors |
| Science agents | ~18 | [musecell](https://github.com/aleksandrahodzzik/musecell), [cellproof](https://github.com/scoobydoobydrew/cellproof) | Moderately crowded |
| Informal-merchant commerce | ~13 | [listsnap](https://github.com/bhoot-biswas/listsnap), [kadai-khata](https://github.com/silambarasan-sh/kadai-khata) | Crowded; mirrors Meta's own Marketplace demo |
| Still in anti-project lanes | Medical ~16, education ~17, sports 5 | [tabibu](https://github.com/Wauguzi/tabibu), [TYSA](https://github.com/Akas333/TYSA) | Penalized by the kickoff slide |
| Energy | ~5 | [wellpilot](https://github.com/EmilJaf/wellpilot), [mechanical-muse](https://github.com/jscott3201/mechanical-muse) | Open |
| Manufacturing and materials | ~9 | [clearline](https://github.com/WaleedOH/clearline), [CircuitGuard-AI](https://github.com/facunahuel420/CircuitGuard-AI) | Open |
| Legacy-code modernization | 4 | [Diocle](https://github.com/Nivetha200111/Diocle), [f2j](https://github.com/Mrabbi3/f2j) | Open, but text-only |
| AI glasses and wearables | ~5 | [beacon-glasses-demo](https://github.com/xdleet/beacon-glasses-demo) | Open and aligned with Meta |
| Genuine open-weights fine-tunes | ~3 | [preflight](https://github.com/natanr123/preflight) | Open; matches a bonus category |
| Disaster and search-and-rescue | ~5 | [SAHARA_MetaAI](https://github.com/Heet-P/SAHARA_MetaAI), [lastseen](https://github.com/h-a-forster/lastseen) | Open |

Few entries in the sample are labeled for the Startup track, which makes that track look less contested for teams that qualify ([reflow-studio](https://github.com/GuiderCoLtd/reflow-studio-hackathon)). The quality bar for depth is set by **Naqsh**, which chains Spark, SAM 3.1 and Muse Image and logs per-call costs of about $0.03 per page, recall evals, failure rates and an API friction log, and by **meta-hack**, with 770 commits and 128 of 128 validation assertions passing ([naqsh](https://github.com/lleoparden/naqsh); [meta-hack](https://github.com/meta-ai-hackathon/meta-hack)). The field has crowded into the verification framing that one workshop promoted, while the gaps line up with official tailwinds: physical systems, which the Push the Frontier theme names; the AI-glasses use cases Meta highlighted at Connect ([Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)); the open-weights partners; and a Best Creative Build bonus for Muse Image or Muse Wonder that almost nobody is chasing. The cheapest available gain on the 25% tooling criterion is to give Muse Image or Muse Wonder a central role. Verification should live inside a compelling domain outcome, not be the product itself.

## Three builds that fit the remaining ~30 hours, ranked

### One scaffold serves all three

All three plans share the same structure, counted backward from the deadline D (Wed Nov 4, 9:00 PM ET). "D−30" means 30 hours before the deadline.

**Team and timing.** The plans assume you start around D−30, with one or two people running parallel AI-coding sessions split by subsystem, the way MedKit ran four concurrent sessions ([Claude winners page](https://claude.com/resources/articles/meet-the-winners-of-built-with-opus-4-7-claude-code-hackathon)). If you start later, cut the nice-to-haves first and never the video block. Put the five-hour sleep block wherever your night falls; the order of the blocks matters more than clock time.

**Build order.** Build the golden path on cached real inputs first. Then add a `DEMO_MODE` that replays cached responses, while the README's default path still runs live. Organizers explicitly allow this ([naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)).

**Visible calls.** Keep a call-log panel in the UI that shows the model ID, latency and cost of each call. It satisfies the requirement that live Meta model calls be visible, and it doubles as a depth signal.

**Frontend.** Use a real web frontend (React/Vite or Next.js), because Streamlit is on the anti-project list.

**Form fields.** If you used Muse Code for part of the build, say so in the "Use of Meta products" field; it plausibly counts toward tooling (our inference). Paste your API friction log into "Feedback on Meta products."

| Milestone | Relative | ET | IST |
|---|---|---|---|
| Riskiest API call proven | D−28 | Tue Nov 3, 5:00 PM | Wed Nov 4, 3:30 AM |
| Golden path end-to-end on cached data | D−20 | Wed 1:00 AM | Wed 11:30 AM |
| Eval number in hand | D−14 | Wed 7:00 AM | Wed 5:30 PM |
| Code freeze, README done | D−8 | Wed 1:00 PM | Wed 11:30 PM |
| Final video uploaded | D−5 | Wed 4:00 PM | Thu 2:30 AM |
| X post live with the video | D−4 | Wed 5:00 PM | Thu 3:30 AM |
| Submitted | D−3 | Wed 6:00 PM | Thu 4:30 AM |
| Hard deadline | D | Wed 9:00 PM | Thu 7:30 AM |

Every video follows the same skeleton, compressed from lablab's guidance ([lablab.ai](https://lablab.ai/guide/how-to-win-an-ai-hackathon)):

| Time | Content |
|---|---|
| 0:00–0:30 | The output artifact, who hurts, and the aha |
| 0:30–1:50 | A live run with the model steps visible |
| 1:50–2:20 | The Meta architecture and the unexpected capability |
| 2:20–2:45 | The measured number and the cost |
| By 2:50 | End |

### The three at a glance

| | #1 Defect Forge | #2 DemoScribe | #3 Find-and-Guide |
|---|---|---|---|
| One line | Five photos of a good part plus your spec in; a pixel-labeled defect dataset and an inspector measured on real defects out | Raw robot demonstration videos in; object tracks, subtasks, failure labels and success verdicts out, exported for training | Say "find my keys"; a SAM-tracked audio cue steers a blind user's hand to them |
| Track / theme | Indie (Startup if you are founders) / Push the Frontier | Indie or Startup / Push the Frontier | Indie / Build for Your World |
| Meta models doing real work | Muse Image, SAM 3.1, Muse Spark (+ Wonder as planner) | SAM 3.1 video, Muse Spark video (+ Spark Open for bulk labeling) | SAM 3.1, Muse Spark, Voice Transcribe (+ Meta glasses toolkit) |
| Under-used Meta surface featured | Muse Image (in 5 of 305 descriptions) | None | Glasses toolkit (~5 builds) |
| Hard number | Recall on real defects, zero-shot vs with forged examples | Agreement with 30 human labels; cost per episode | Time to touch the object vs a describe-only baseline |
| Weighted score if it works | 7.8 | 7.7 | 8.1 |
| Chance the golden path works by D−8 (our judgment) | ~80% | ~70% | ~50% |
| Risk-adjusted score | ~7.5 | ~7.2 | ~6.8 |
| Biggest risk | Muse Image's fidelity on small defects | Data wrangling; flashy robotics rivals | Live latency; no text-to-speech under the rule; needs a real user |
| Bonus targets | Creative Build, Agentic | Agentic, Open Weights | Most Viral, Community Vote |
| Best if your team… | likes pipelines and evals | has a robotics or ML-data background | has a blind or low-vision connection, or mobile skills |

How the risk-adjusted score is computed: the chance of success times the score if it works, plus the chance of failure times a cached-demo-only fallback score. The fallback scores are 6.0 for Defect Forge, 6.0 for DemoScribe and 5.5 for Find-and-Guide. All scores are our estimates on the official 0–10 scale.

### #1 Defect Forge: Muse Image manufactures the defects a new production line has never seen

**Track and theme.** Defect Forge belongs in **Indie**, under **Push the Frontier**: it gives an inspection system a capability it could not have before, which is seeing a defect class it has no real examples of. Pick Push the Frontier as the form's problem statement. Move to Startup only if you are an actual startup; synthetic inspection data is a credible wedge there.

**User and pain.** The user is a quality or vision engineer at a small or mid-size manufacturer who is setting up visual inspection for a new part. Defects are rare by design, so the inspector starts blind exactly when it matters. Vendor-relayed figures put the cost of poor quality at **15–20% of revenue** and say manual inspection catches roughly 60–90% of defects ([Oxmaint](https://oxmaint.com/industries/manufacturing-plant/manual-vs-automated-quality-inspection-manufacturing)). Only **8.2% of manufacturers are actively scaling AI** ([Amper](https://www.amper.xyz/post/manufacturing-in-the-age-of-ai-part-4)), yet about 7 in 10 would consider a structured pilot ([FME assessment](https://norfolkdailynews.com/online_features/press_releases/national-assessment-identifies-a-practical-path-for-ai-adoption-in-manufacturing/article_14856071-4f70-58b8-bca9-af4917332a5a.html)). Generic SAM-based auto-labeling "cannot distinguish different kinds of cracks or identify defects specific to electronics" ([Roboflow docs](https://docs.roboflow.com/datasets/ko/annotate/annotate/ai-labeling/auto-label.md)), which is exactly the gap a reasoning layer fills.

**Why Meta's models are essential.** Each flagship model does work the others cannot, and the loop between them is the unexpected capability. **Muse Image** edits photos for $0.01 each and by default runs image search, web search and a shell before rendering ([Image generation docs](https://dev.meta.ai/docs/image-generation.md)), so it can look up what fretting corrosion or thread damage really looks like before painting it on; run the live hero shot through the Responses API, which returns a short reasoning summary, so viewers can see whether it searched. **SAM 3.1** turns each forged region into a pixel mask from a box prompt, so the labels come free ([SAM overview](https://dev.meta.ai/docs/sam/overview.md)). **Muse Spark 1.3** reads the spec PDF into a defect taxonomy using constrained JSON, critiques each sample's realism, and then acts as the inspector, taking up to 50 images per request and returning boxes on the 0–1000 grid ([Image understanding](https://dev.meta.ai/docs/image-understanding.md); [Structured output](https://dev.meta.ai/docs/structured-output)). Optionally, **Muse Wonder** plans the generation from the spec, which puts Meta's second-least-used model to work. The result is a Meta image generator manufacturing training data for a Meta segmenter, checked by a Meta reasoner: a closed loop few judges will have seen. Everything else, such as image diffs and feathering, is classical OpenCV, so runtime purity holds.

| Feature | Priority | Meta model |
|---|---|---|
| Spec ingest: a PDF or text spec plus 3–5 good-part photos → defect taxonomy JSON (clause, defect type, size, allowed zone) | Must | Muse Spark 1.3 |
| Locator: segment the part and sample patch locations that lie on it | Must | SAM 3.1 (concept prompt; box fallback from Spark grounding) |
| Forge: crop a ~512 px patch, give an edit instruction ("add a 3 mm dent per clause 4.2"), and feather-paste it back so the rest of the image stays pixel-identical | Must | Muse Image `/v1/images/edits` |
| Auto-label: diff the patch before and after the edit → box → SAM box prompt → clean mask. Export COCO JSON, PNG masks and provenance | Must | SAM 3.1 |
| Critic loop: score realism 1–5 and check the clause match; regenerate rejected samples up to twice | Must | Muse Spark 1.3 (low effort) |
| Inspector and eval: 40 held-out real images (20 defective, 20 good); zero-shot vs 8 forged examples in context; precision, recall, confusion matrix | Must | Muse Spark 1.3 |
| Web UI: upload → plan → live forge grid → before/after slider with mask → export → eval tab. Includes the call-log panel and `DEMO_MODE` | Must | None |
| Run the planner on Wonder instead of Spark | Nice | Muse Wonder 1.0 |
| Phone-capture page: photograph a real bolt on your desk and forge defects onto it | Nice | All |
| Multi-turn refinement ("deeper," "more rust") via `previous_response_id` | Nice | Muse Image |
| Blind realism test (real vs forged) to produce a second number | Nice | None |
| Local pre-screen critic on Glimmer, as the open-weights angle | Nice | Muse Glimmer |

```
spec.pdf + 5 good-part photos
        │
        ▼
 Planner ── Muse Spark 1.3 (or Wonder), text.format strict JSON
        │      → [{clause, defect_type, size_mm, zone}]
        ▼
 Locator ── SAM 3.1 image, prompt "metal nut" → part mask → on-part patch centers
        ▼
 Forge ──── Muse Image /v1/images/edits on a 512 px patch (reasoning_strength=low)
        │      → OpenCV feather-paste back into the original (no ML)
        ▼
 Labeler ── |patch_after − patch_before| → bbox → SAM 3.1 box prompt → defect mask (RLE)
        ▼
 Critic ─── Muse Spark 1.3, effort=low: realism 1–5, matches the clause? → retry up to 2 times
        ▼
 Dataset ── COCO JSON + masks + provenance (prompt, response IDs, cost, latency)
        ▼
 Inspector ─ Muse Spark 1.3: spec + 8 forged examples + one real image
        │      → {defect, type, box_0_1000}
        ▼
 Eval ───── precision / recall on held-out real defects (one MVTec AD or VisA category)

Stack: FastAPI + asyncio queue (≤2 Image calls/s, jittered backoff), OpenAI SDK
(base_url https://api.meta.ai/v1), meta_sam_parser, React/Vite front end, local disk cache.
```

| Hours | Work | Exit criterion |
|---|---|---|
| D−30 → D−28 | Claim credits and a key. Prove one Muse Image patch edit and one SAM 3.1 box-prompt call parsed with `meta_sam_parser`. Pick one public category (MVTec AD or VisA; check the license, since several defect datasets are non-commercial) and one desk object you can photograph. Write the 150-word description and the video script | One forged defect with its mask on screen |
| D−28 → D−25 | Pipeline v1 as a CLI: spec → taxonomy JSON, part mask and patch sampler, patch edit, feather-paste, diff → SAM mask, COCO export | 10 labeled samples of one defect type |
| D−25 → D−22 | Critic loop with up to two retries. Async batch runner with 429 backoff, plus provenance and per-call cost/latency logging. Start a background batch of 3 defect types × 60 samples | Batch running; rejection rate logged |
| D−22 → D−19 | Inspector and eval harness on 40 real held-out images, zero-shot vs 8 forged examples; save the results as JSON | First precision/recall numbers |
| D−19 → D−14 | Sleep while the batch runs | None |
| D−14 → D−10 | React/Vite UI along the golden path, live call-log panel, `DEMO_MODE` cached replay. With two people, one builds the UI while the other tunes prompts and reruns the eval | Golden path clickable end to end |
| D−10 → D−8 | Fix golden-path bugs only. If everything is working, add one nice-to-have (photos of your own part, or the Wonder planner). Write the README: one-command setup, `.env.example`, architecture diagram, eval table, costs, friction log | Code freeze; repo runs from a clean clone |
| D−8 → D−5 | Record live takes that show api.meta.ai calls; cut to under 2:50; add captions; re-record weak scenes | Final video uploaded as unlisted |
| D−5 → D−3 | Post the video natively on X. Fill in the form with each model's role and the numbers. Check everything in a logged-out browser. Submit | Submitted |
| D−3 → D | Buffer; no code changes | None |

| Time | On screen | Voiceover or caption | Rubric hit |
|---|---|---|---|
| 0:00–0:10 | A grid of 48 photoreal scratches, dents and contamination spots on a metal part fills in, each outlined by a mask | "This part has never failed inspection. That's the problem: with no defects, there's nothing to teach an inspector." | Impact |
| 0:10–0:30 | The spec PDF is dropped in and taxonomy cards appear. One sample opens in a before/after slider with its SAM mask and the tag "$0.01, n seconds" | **Aha:** "Defect Forge reads your spec, then forges the defects it describes, labeled to the pixel." | Demo, Tooling |
| 0:30–1:20 | Live run: type "thread damage per clause 4.2." Muse Image's reasoning summary appears, the patch is edited, SAM draws the mask, and Spark's critic rejects one sample as unrealistic and regenerates it. The call log shows the model IDs | "Four Meta models, one loop." | Demo, Depth |
| 1:20–1:55 | Inspector on real defects: zero-shot recall X% rises to Y% with forged examples; precision; cost per 100 samples | "Measured on 40 real defects it never saw." | Depth, Impact |
| 1:55–2:25 | Architecture graphic naming each Meta model and its role, with the line "every runtime model is Meta's" | The unexpected capability: an image model as a data factory | Tooling |
| 2:25–2:50 | COCO export opens; who adopts it next (job shops, QA integrators); repo link | Call to action | Impact |

| Criterion (weight) | Score | Rationale |
|---|---|---|
| Impact (30%) | 7.0 | Clear economic pain and a clear buyer; less visceral than accessibility |
| Use of Meta AI Tooling (25%) | 9.0 | Three or four Meta models in one loop; rare use of Muse Image; search-grounded rendering shown on screen |
| Demo (25%) | 7.5 | The grid and the before/after slider are instantly legible; the work is mostly batch, so "live" is a single forge run |
| Technical Depth (20%) | 8.0 | Diff-plus-SAM labeling, critic loop, eval on real data, cost log |
| Weighted | 7.8 | |

**Bonus prizes.** Best Creative Build is the natural target, since it is literally for the "most original use of Muse Image or Muse Wonder." The planner → forge → critic loop makes a credible Best Agentic Use-Case entry. Before/after grids are shareable enough to post for Most Viral and Community Vote. A Glimmer critic is the only route to the open-weights bonus, and it is a stretch.

| Risk | Mitigation |
|---|---|
| Muse Image edits look fake on small defects, or re-render the whole patch. Its edit quality relative to rivals is known only from Meta-internal tests relayed by third parties ([Flowith](https://flowith.io/ai-models/meta-muse-image/)) | Test three defect types in the first two hours and keep the most convincing. Prefer dents, contamination and cracks over hairlines. Paste back only the changed region |
| Forged examples do not lift the inspector's recall | Report that honestly, and make the headline number label quality instead (SAM mask IoU against the diff ground truth) plus the blind realism test |
| Muse Image is limited to 150 RPM, and its latency is unknown | Batch overnight; cache everything; replay with `DEMO_MODE` |
| SAM misses the part with a concept prompt | Use a box prompt from Spark's 0–1000 grounding |
| Dataset license (several defect sets are non-commercial) | Use the dataset only for evaluation and cite it, or photograph your own parts |
| The safety filter refuses an edit | Failed and filtered images are not billed; rephrase and retry |
| Judges read it as another "photo → inspection report" | Open the video on generation, not inspection; the inspector appears only as proof |
| Training a non-Meta detector on the forged data would break the runtime rule | Keep the inspector a Meta model, and export the dataset only as an artifact |

**How it avoids crowded and anti-project categories.** Manufacturing and materials have about nine visible entries, and none appears to generate defect data. Muse Image appears in five descriptions in total. Defect Forge is a generator, labeler and evaluator. It is not a simple image analyzer, not a dashboard, not RAG and not Streamlit, and it gives no medical, educational or sports advice. The one adjacency to watch is the crowded photo-to-report cluster. The storyboard avoids it by leading with forged data.

### #2 DemoScribe: SAM 3.1 turns raw robot episodes into labeled, refereed training data

**Track and theme.** DemoScribe fits **Indie** under **Push the Frontier**: it gives robots a better route to new capabilities by fixing their data. It has an obvious Startup path as a data-engine API. YC's Fall 2026 requests explicitly include "Data for the Real World" ([explainx summary of YC RFS](https://explainx.ai/blog/yc-requests-for-startups-fall-2026)).

**User and pain.** The users are robot-learning teams and data vendors. A single teleoperation rig can cost $40,000+, with one operator per robot ([AXIS Robotics](https://axisrobotics.ai/resources/blog/best-robot-training-data-companies)). **59% of physical-AI teams struggle with poor labels, and 47% cannot identify which data hurts their models** (a Voxel51 report, via [Pebblous](https://blog.pebblous.ai/blog/agibot-world-failure-annotation/en/)). Manual annotation is "expensive and poorly scalable" ([RoboAnnotatorX](https://openaccess.thecvf.com/content/ICCV2025/html/Kou_RoboAnnotatorX_A_Comprehensive_and_Universal_Annotation_Framework_for_Accurate_Understanding_ICCV_2025_paper.html)), dense language re-annotation of existing demonstrations matched a no-annotation baseline with about 62% less compute at a scale of 1M clips ([DeMiAn](https://arxiv.org/pdf/2605.17077)), and failure annotation is becoming a prerequisite as datasets keep their failed demonstrations ([Pebblous](https://blog.pebblous.ai/blog/agibot-world-failure-annotation/en/)). Raw data is plentiful. Open X-Embodiment has 1M+ trajectories across 22 robot types ([OXE](https://arxiv.org/pdf/2310.08864)), and DROID is cited at 76K–92K trajectories ([RLDX-1](https://arxiv.org/pdf/2605.03269)).

**Why Meta's models are essential.** SAM 3.1 tracks every manipulated object through an episode with persistent IDs: up to 16 objects per frame, up to ~10 minutes of video, at $0.20 per 1,000 frames ([SAM overview](https://dev.meta.ai/docs/sam/overview.md)). Spark 1.3 watches the whole episode, even several camera views in one 1M-token call, and returns subtasks, language instructions and failure reasons as structured output ([Video understanding](https://dev.meta.ai/docs/video-understanding.md)).

The unexpected capability is that mask geometry becomes a dense, interpretable progress signal: whether the gripper touches the object, whether the object sits inside its container, how high it has been lifted. Spark then referees that signal and catches "fake successes," where the gripper hovers but never places the object. Earlier work found zero-shot vision-language success detection unreliable on its own ([arXiv 2303.07280](https://arxiv.org/pdf/2303.07280)), and that is exactly why combining geometry with reasoning is the pitch. Current 2026 reward-model research shows the problem is live ([TOPReward](https://arxiv.org/html/2602.19313); [RoboReward](https://arxiv.org/pdf/2601.00675v1)).

| Feature | Priority | Meta model |
|---|---|---|
| Ingest: episode MP4 plus task description; ffmpeg to H.264 with faststart, at most 15 fps | Must | None |
| First pass: objects (as noun phrases), subtask segments with timestamps, success or failure plus the reason (JSON) | Must | Spark 1.3 video |
| Tracking: one SAM request per noun phrase; the gripper via a box prompt on frame 0 | Must | SAM 3.1 video |
| Geometry: centroids, gripper–object overlap (contact), containment, lift → progress curve | Must | None (numpy/OpenCV) |
| Referee: progress curve + 6 keyframes + first-pass JSON → verdict plus flags where the two disagree | Must | Spark 1.3 |
| Export: LeRobot-style annotation JSON, run-length-encoded masks, provenance | Must | None |
| Eval: 30 hand-labeled episodes → success agreement, subtask-boundary error in seconds, cost and time per episode | Must | None |
| Viewer: video with mask overlays, subtask timeline, red failure flags, export button | Must | `@meta-sam/parser` |
| Curation query: "episodes where the grasp slipped," across 100 episodes | Nice | Spark 1.3 |
| Multiple views: wrist and external cameras in one call | Nice | Spark 1.3 |
| Bulk first pass on Spark Open via Fireworks or Baseten (video support there is unverified) | Nice | Muse Spark Open |
| External ground truth from RoboReward labels, if they can be downloaded | Nice | None |

```
episode MP4s (small LeRobot / DROID subset)
   │ ffmpeg: H.264, +faststart, ≤15 fps
   ▼
 Pass 1 ─── Muse Spark 1.3 video, effort=medium, text.format JSON
   │          → {objects[], subtasks[{t0,t1,label,instruction}], success, failure_reason}
   ▼
 Track ──── SAM 3.1 video, one request per noun phrase; gripper box prompt @ frame 0
   │          → per-frame masks + persistent IDs
   ▼
 Geometry ─ numpy/OpenCV: centroids, IoU(gripper,obj), containment(obj,container), lift → progress(t)
   ▼
 Referee ── Muse Spark 1.3: progress(t) + 6 keyframes + pass-1 JSON → verdict + disagreement flags
   ▼
 Export ─── LeRobot-style annotations + RLE masks + provenance
   ▼
 Eval ───── vs 30 hand labels → agreement %, boundary MAE (s), $/episode, s/episode
Viewer: React + @meta-sam/parser overlays; FastAPI job runner with cache
```

| Hours | Work | Exit criterion |
|---|---|---|
| D−30 → D−28 | Download a small episode subset from Hugging Face (LeRobot or DROID; check availability first). Transcode with ffmpeg. Make one SAM 3.1 video call for "mug" and parse it; make one Spark video call with a JSON schema. Count video tokens with `/v1/responses/input_tokens`. Check [DemoDoctor](https://github.com/est4ever/DemoDoctor) and the other robotics repos for overlap | Masks over one episode; Spark JSON returned |
| D−28 → D−24 | Pipeline v1: first pass, SAM tracks per noun phrase plus the gripper box, geometry features, progress curve | One episode fully annotated |
| D−24 → D−21 | Referee and disagreement flags; LeRobot-style export; start a background batch of 50–100 episodes | Batch running |
| D−21 → D−19 | Hand-label 30 episodes while the batch runs; write the eval script | First agreement and cost numbers |
| D−19 → D−14 | Sleep | None |
| D−14 → D−10 | Viewer UI (overlays, timeline, flags, episode list, export), curation query, `DEMO_MODE` | Golden path clickable |
| D−10 → D−8 | Fix golden-path bugs; README with an eval table and cost per episode. If everything is working, add the Spark Open bulk pass | Code freeze |
| D−8 → D−5 | Record, cut and re-record the video | Video uploaded |
| D−5 → D−3 | X post, form, checks in a logged-out browser, submit | Submitted |
| D−3 → D | Buffer | None |

| Time | On screen | Voiceover or caption | Rubric hit |
|---|---|---|---|
| 0:00–0:12 | A raw robot episode plays. Masks snap onto the mug, the drawer and the gripper. The timeline splits into reach, grasp, lift and place, and a red flag appears: "0:14 grasp slipped, re-grasped" | "Robots learn from demonstrations, and every second of every demo needs a label." | Demo |
| 0:12–0:30 | A counter reads "100 episodes · N minutes · $X." The export opens as LeRobot-format JSON | **Aha:** "DemoScribe labels and referees them automatically, down to the failure." | Impact, Tooling |
| 0:30–1:20 | Live run on a new episode: Spark's first-pass JSON streams in, SAM tracks the objects, the progress curve rises, and the referee catches a gripper hovering without placing | "Geometry plus reasoning: a success detector with no training." | Depth, Tooling |
| 1:20–1:50 | The query "show episodes where the grasp slipped" returns 6 clips | Data curation | Impact |
| 1:50–2:20 | Agreement with 30 human labels, subtask-boundary error, cost per episode vs human minutes | The number | Depth |
| 2:20–2:50 | Architecture; who adopts it next; repo | Call to action | Tooling, Impact |

| Criterion (weight) | Score | Rationale |
|---|---|---|
| Impact (30%) | 7.5 | Targets a frontier bottleneck; the buyer group is narrow but valuable; resonates with Meta's research audience |
| Use of Meta AI Tooling (25%) | 8.0 | SAM 3.1 video tracking is the hero; Spark handles video over a 1M context; no Muse Image |
| Demo (25%) | 7.0 | Masks on robot video are striking, but read as technical to generalist judges |
| Technical Depth (20%) | 8.5 | Geometry features, referee, eval against human labels, a real export format |
| Weighted | 7.7 | |

**Bonus prizes.** Best Agentic Use-Case is plausible if the curation step becomes an agent that re-checks flagged episodes on its own. The open-weights bonus is plausible if Spark Open runs the bulk first pass, though whether hosted providers accept video is unverified. The robotics community on X gives Most Viral a fair shot. Creative Build is out of reach.

| Risk | Mitigation |
|---|---|
| SAM 3 handles articulated robot geometry and arm–gripper separation poorly ([RobotSeg](https://arxiv.org/pdf/2511.22950)) | Track the manipulated objects, box-prompt the gripper once, and never prompt for arm links |
| Downloading and formatting the dataset eats hours | Settle on a small subset in the first two hours; 20 episodes are enough for the demo |
| The precision of Spark's timestamps is unknown | Snap subtask boundaries to geometry events such as the start of contact or the start of a lift |
| SAM video latency and Spark video token counts are unknown | Process offline; count tokens during the first two hours |
| Robotics rivals with real hardware ([athlete2humanoid](https://github.com/PandaGrdn/athlete2humanoid), [video2urdf](https://github.com/SungHyunC/video2urdf), [muse-qc-cell](https://github.com/StefanRohringer/muse-qc-cell)) | Position DemoScribe as the data layer every one of those teams needs |
| The viewer reads as "dashboard as the main feature" | Make the exported dataset the hero; the viewer is only quality control for it |

**How it avoids crowded and anti-project categories.** The roughly fourteen visible robotics entries focus on policies, robot descriptions (URDF) and physical arms. None visibly does demonstration annotation and refereeing, though DemoDoctor's scope should be checked first. Nothing here touches the anti-project list.

### #3 Find-and-Guide: continuous SAM tracking steers a blind user's hand to the object

**Track and theme.** Find-and-Guide fits **Indie** under **Build for Your World**. It is strongest if a teammate or family member is blind or has low vision, because winners at these events are usually domain insiders.

**User and pain.** The WHO counts at least **2.2 billion people with near or distance vision impairment**. At least 1 billion of those cases are preventable or unaddressed, and the productivity loss is about $411B a year ([WHO](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment)). Scene-description tools are popular: 98.7% of Be My Eyes users who gave an opinion were positive about Be My AI ([AFB](https://afb.org/aw/fall2024/ai-usage-research)). But describing a room is not the same as getting your hand onto the keys. Guidance that stays locked on a target is the underserved step; that is our inference from the competitive scan, not a measured gap.

**Why Meta's models are essential.** **SAM 3.1** segments the named object in every frame, so the cue updates as the camera moves; the target persists, which a one-shot description cannot do. **Spark 1.3** at low effort parses a request like "my blue bottle, not the glass one" into a single noun phrase plus attributes, and gives a fast first lock through 0–1000 box grounding ([Image understanding](https://dev.meta.ai/docs/image-understanding.md)). **Muse Voice Transcribe**'s realtime WebSocket handles spoken, mixed-language requests in 25 languages ([Models](https://dev.meta.ai/docs/models)). **Meta's Wearables Device Access Toolkit 1.0** adds camera capture and voice streaming from Meta's AI glasses ([Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)), and Meta's cookbook already includes a smart-glasses recipe ([Cookbook](https://dev.meta.ai/docs/cookbook.md)). The unexpected capability is open-vocabulary segmentation used as a closed-loop guidance sensor. Runtime purity is designed in, because no text-to-speech model is called. Direction is turned into sound with Web Audio: stereo pan for left and right, pitch for up and down, click rate for distance. Short text goes into an `aria-live` region, which the user's own screen reader speaks aloud. Confirm this approach with organizers on Discord.

| Feature | Priority | Meta model |
|---|---|---|
| Phone web app, chest-mounted or handheld; sends 640 px JPEG frames (which avoids WebM) | Must | None |
| Request by voice or text → `{noun_phrase, attributes}` | Must | Voice Transcribe, Spark 1.3 |
| First lock: Spark box → SAM 3.1 box or concept prompt → mask | Must | Spark 1.3, SAM 3.1 |
| Guidance loop at 1–2 Hz: mask centroid → direction; mask area → distance; sound cues; "got it" once the target is centered and large | Must | SAM 3.1 |
| Dead reckoning from the phone's orientation sensor between updates; re-lock if the target is lost | Must | None |
| UI fully usable with a screen reader, plus haptics and `aria-live` text | Must | None |
| Eval: 10 objects × 3 scenes; time to touch the object vs a describe-only baseline; latency log | Must | Spark 1.3 (for the baseline) |
| Recorded-clip fallback mode for judges | Must | None |
| Capture from Ray-Ban Meta glasses through the Device Access Toolkit | Nice | Glasses toolkit |
| "Where did I leave my keys?" answered from recent frames | Nice | Spark 1.3 |
| Commands in Hindi or Spanish | Nice | Voice Transcribe |

```
phone camera (getUserMedia) ── 1–2 fps, 640 px JPEG ──► FastAPI WebSocket backend
mic ──► Muse Voice Transcribe realtime (wss://api.meta.ai/v1/asr/realtime) ──► text
text ──► Muse Spark 1.3 (effort=low, JSON) ──► {noun_phrase, attributes}
frame ──► Spark grounding box (0–1000, first lock) ──► SAM 3.1 image (box/concept) ──► mask
mask ──► centroid, area ──► guidance vector {dx, dy, proximity, locked}
client: Web Audio pan/pitch/click rate + navigator.vibrate + aria-live text (user's own screen reader)
DeviceOrientation ──► dead-reckon the cue between server updates (no ML)
```

| Hours | Work | Exit criterion |
|---|---|---|
| D−30 → D−28 | Measure latency first: phone browser camera → backend → SAM 3.1 image call at 640 px, recording median (p50) and 90th-percentile (p90) round trips. Time Spark grounding at minimal and low effort. Test the realtime Voice Transcribe connection. Ask Discord #questions about screen-reader and sound-cue output. Contact a blind or low-vision tester through a local association or campus disability office | Median round trip known; decide whether a live loop is feasible |
| D−28 → D−24 | Loop v1: request → noun phrase → first lock → mask → guidance vector → Web Audio cues | The tone follows a mug on a table |
| D−24 → D−21 | Smoothing, dead reckoning, re-locking a lost target, "got it" detection, haptics, a screen-reader-operable UI | A hand reaches the target in under 20 s on 3 tries |
| D−21 → D−19 | Eval protocol: 10 objects × 3 scenes, timed against a describe-only baseline; latency log | First timing numbers |
| D−19 → D−14 | Sleep | None |
| D−14 → D−11 | Session with the tester, recorded with consent, or chest-mounted point-of-view runs; fix what breaks | Real-user footage |
| D−11 → D−8 | Recorded-clip fallback mode; README. If everything is working, add glasses capture or multilingual commands | Code freeze |
| D−8 → D−5 | Record, cut and re-record the video | Video uploaded |
| D−5 → D−3 | X post, form, checks in a logged-out browser, submit | Submitted |
| D−3 → D | Buffer | None |

| Time | On screen | Voiceover or caption | Rubric hit |
|---|---|---|---|
| 0:00–0:15 | Point-of-view shot from a chest-mounted phone over a cluttered counter. The user says "find my keys." A tone pans left, rises, and clicks faster as the hand closes on the keys | Captions only; no voiceover for the first 8 s | Demo |
| 0:15–0:30 | Split screen: what the phone sees (SAM mask locked on the keys) next to what the user hears (a stereo pan meter) | **Aha:** "Describing a room isn't the same as finding your keys." The WHO figure of 2.2 billion appears | Impact, Tooling |
| 0:30–1:30 | Three more finds: a door handle; the chipped mug among several white mugs; an empty seat. The tracker loses the target and recovers it | "SAM 3.1 keeps the target locked while you move." | Demo, Depth |
| 1:30–2:00 | The tester's own words; time to touch vs a describe-only app | The number | Impact, Depth |
| 2:00–2:30 | Architecture: Voice Transcribe → Spark → SAM 3.1 → sound cues; "no text-to-speech model, the user's own screen reader" | Runtime purity and the unexpected capability | Tooling |
| 2:30–2:50 | Glasses teaser if built; repo link | Call to action | Impact |

| Criterion (weight) | Score | Rationale |
|---|---|---|
| Impact (30%) | 8.5 | Huge population; emotionally clear; fits Build for Your World; aligned with Meta's glasses |
| Use of Meta AI Tooling (25%) | 8.0 | SAM as a live sensor, Spark grounding, Voice Transcribe, glasses toolkit; no Muse Image |
| Demo (25%) | 8.5 | The point-of-view shot of a hand reaching the keys is the most watchable aha of the three, provided it works live |
| Technical Depth (20%) | 7.0 | Latency engineering, dead reckoning, sound cues; only a small eval |
| Weighted | 8.1 | |

**Bonus prizes.** This is the strongest of the three for Most Viral and Community Vote, because the footage is emotional and easy to understand. It is weak for Best Agentic, and it does not qualify for Creative Build or the open-weights bonus.

| Risk | Mitigation |
|---|---|
| SAM API latency is unverified; one third party lists about 0.4 s per frame ([Reka](https://infer.reka.ai/models/sam-3-1)) | Measure it in the first two hours. Downscale frames, lock with Spark grounding and refine with SAM, and dead-reckon between updates. If the p90 round trip exceeds 1.5 s, demo on recorded clips and say so |
| Meta has no text-to-speech model, and the runtime rule bars third-party ones | Use sound cues plus the user's own screen reader; ask organizers before using any speech synthesis |
| Setting up the glasses toolkit can eat a day | Build on the phone first; Gemma Vision won with a chest-mounted phone ([Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/)). Add glasses only if everything else works at D−11 |
| No real blind or low-vision tester | Reach out in the first hour. A blindfolded sighted tester is a weak substitute, and should be labeled as one |
| Safety and liability | Scope to finding objects indoors; make no navigation or obstacle-avoidance claims |
| The category is familiar (Netra placed 3rd at the Gemini 3 hackathon, per [Devpost updates](https://gemini3.devpost.com/updates); Gemma Vision) and could drift toward "simple image analyzer" | Never make a describe-the-scene mode the hero; the tracked lock is the product |
| Phone EXIF rotation or an aspect-ratio mismatch makes SAM return 400 | Normalize frames on the client |

**How it avoids crowded and anti-project categories.** About five visible builds target AI glasses. Voice assistants are crowded (36 descriptions mention voice), so the guidance here relies on sound cues rather than speech. The app diagnoses and treats nothing, so it stays clear of the medical-advice anti-project. Keep all health claims out of the pitch.

### Why this order, and what would flip it

**Defect Forge ranks first** because it has the best ratio of score to risk. Every step can be batched and cached, so the demo cannot fail live. It is also the only one of the three that gives Muse Image real work, and that is the clearest route both to the "surfaced unexpected capabilities" clause and to the Creative Build bonus.

**DemoScribe ranks second.** It arguably has the deepest engineering, and it matters most to Meta's research judges. But robotics is where the field's most ambitious entries already cluster, and its aha needs a sentence of explanation for non-roboticists.

**Find-and-Guide ranks third** despite having the highest ceiling on Impact and Demo, which together carry 55% of the score. Its core moment depends on live latency nobody has measured, on a rules gray zone around speech output, and on finding a real user within a day.

Someone maximizing Impact could fairly argue that the 30% weight, plus accessibility's repeated wins, makes Find-and-Guide the rational pick. We discount that argument because the video must show live Meta calls, and Find-and-Guide is the only one of the three whose key moment depends on real-time network latency.

Three conditions would flip the order. If your team has a blind or low-vision connection and mobile skills, move Find-and-Guide to first. If your team has a robotics or ML-data background, move DemoScribe to first, because judges reward domain insiders. If you are a registered startup, enter Defect Forge on the Startup track, which has few labeled entries and pays $250K for first place.

### Ideas considered and cut

| Idea | Why it was attractive | Why it was cut |
|---|---|---|
| Inspector-in-a-Phone (visual QA driven by a spec PDF) | Spec PDF and video fit in one context; clear buyer | On its own it sits in the crowded photo-to-report cluster; folded into Defect Forge as the inspector |
| Legacy-code modernization with compiled-equivalence checks | Only 4 entries; shows off 1M-context retrieval ([f2j](https://github.com/Mrabbi3/f2j); [Diocle](https://github.com/Nivetha200111/Diocle)) | Text-only demo, saturated verification framing, and both of those projects already exist |
| TrapTales (camera-trap video → species, counts, behavior) | Lowest build risk; public data; strong visuals | Narrower impact, and it reads as an analyzer; the best fallback if all three fail |
| Watch-and-Do (human video → simulated robot program) | Highest wow factor | Lifting 2D video into 3D is high-risk in a day; [video2urdf](https://github.com/SungHyunC/video2urdf) already occupies the space |
| Second Pair of Hands (glasses copilot that checks a field technician's steps) | Fits Meta's glasses; matches a YC request | Video procedure checking is crowded |
| Solar Fault Hunter / LineSight (energy inspection) | Energy has only ~5 entries | Funded incumbents (Buzz Solutions raised $20M, per [Axios](https://www.axios.com/pro/climate-deals/2026/08/04/buzz-solutions-20m-grid-ai)), thermal-imaging domain shift, photo-to-report shape |
| Site Replay (construction safety from video) | Severe pain: 1,034 private-sector construction deaths in 2024 ([BLS](https://www.bls.gov/opub/ted/2026/national-safety-stand-down-highlights-fall-hazards-in-construction.htm)) | The hazard cluster is crowded, and incumbents such as Voxel are well funded ([Shopifreaks](https://www.shopifreaks.com/voxel-raises-44m-series-b-to-expand-ai-powered-workplace-safety-tech/)) |
| Sideline (tactics for amateur sports) | Shows off SAM's multi-object tracking | Sports analyzers are an anti-project |
| OR Rewind (surgical video review) | Strong evidence for SAM 3 on surgical benchmarks ([arXiv 2512.07596](https://arxiv.org/abs/2512.07596v1)) | Medical-advice anti-project risk; dataset access takes time |
| Leaf-Level Scout (crop scouting) | Huge pain; multilingual | Drifts into giving advice; no Meta text-to-speech for low-literacy users |
| Aisle Walk / merchant listings | Clear retail return on investment | The commerce cluster has ~13 entries, and it mirrors Meta's own demo |
| SAM + Muse Image video-remix toy | Viral; fits the Creative bonus | Weak Impact; with no seeds or masks, frames flicker |
| Visual QA agent for XR apps | Aligned with Meta's XR Operator ([Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)) | Access to XR Operator is unverified, and so is SAM's accuracy on UI imagery |
| Another agent-receipts layer | Endorsed by a workshop | The most saturated cluster (~57 repos) |

### A seven-question filter for your own ideas

| Question | Passes if… |
|---|---|
| Is it runtime-pure? | Every learned model called at runtime is Meta's: no third-party text-to-speech, speech-to-text, LLM, embeddings or local vision networks |
| Are two or more Meta models in a loop? | At least two Meta models each do work the other cannot, and one does something a judge won't expect |
| Is it off the lists? | It is not on the kickoff's anti-project slide, and not in the receipts, photo-to-report or procedure-checker clusters |
| Does a real input become a professional artifact? | A real file, photo or video goes in; a dataset, report, work order or action comes out |
| Can you have one number by D−14? | A 20–40-item eval or a timed trial can be finished before the code freeze |
| Is the aha clear without narration by 0:30? | A viewer with the sound off would understand the first 30 seconds |
| Is the golden path cacheable? | The demo can replay cached Meta responses if the network fails or a rate limit hits |

## Conclusion

This contest is more predictable than its 20,000-person scale suggests. Cerebral Valley reused its Anthropic rubric almost word for word. That makes the Opus 4.6 and 4.7 winners the template: domain insiders, real artifacts, a measured number and a clean three-minute video. The field has also misallocated itself. Dozens of teams are building verification layers, while only a handful use Muse Image or Muse Wonder, the two models that a dedicated bonus and the "unexpected capabilities" clause reward most. A team that gives an under-used Meta model a central job in an uncrowded physical domain starts with a scoring edge before writing any code.

The runtime-purity rule is the quiet decider. Meta has no text-to-speech model, and the rule bars third-party models, so voice-first and accessibility ideas carry structural risk. Pipelines that output artifacts (datasets, masks, reports) are compliant by construction and can be cached, which also protects the 25% Demo score. That is the deepest reason Defect Forge ranks first. When you add your own ideas, run each through the seven-question filter. An idea that passes all seven and draws on your team's firsthand experience deserves to compete head to head with these three, and it may well beat them, because winners at events like this are usually insiders.
