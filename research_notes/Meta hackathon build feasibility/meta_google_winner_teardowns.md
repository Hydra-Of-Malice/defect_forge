# Implementation teardowns: Meta/Llama and Google Gemini/Gemma hackathon winners, and code we can reuse for Defect Forge, DemoScribe and Find-and-Guide

Scope note: research ran Nov 3–4, 2026. Repos were read with `gh api` (nothing cloned or executed). Devpost pages were fetched with curl because WebFetch returned 403. YouTube data (title, length, description) came from page metadata; **no video was watched**, so demo structure is only known where a description or title states it. Kaggle write-ups render client-side and could not be read. Licenses come from the GitHub API (`license.spdx_id`) or the LICENSE file. "No license" means GitHub reports none, so default copyright applies: read for patterns, don't copy. Anything marked **[inferred]** is our reasoning, not a source claim.

---

## Q1. Per-project teardowns: repo, license, stack, model use, hardware, proof, depth signals, demo video, reusable code

### Takeaway
Repos were found for 14 of the 15 named projects (all except Gaze Link and Jayu, plus Gripmind, which has only Hugging Face artifacts). Four are directly reusable and permissively licensed:
- **Llama CCTV Operator** (Apache-2.0)
- **OpenGlass** (MIT)
- **Gemma Vision** (MIT)
- **GEM-4's MimicAnno and MimicRec** (Apache-2.0)

Two of the most relevant pieces have **no license**: **Netra**, the closest prior art to Find-and-Guide, and Aegis.

GEM-4's MimicAnno is almost exactly DemoScribe: signal-based subtask boundaries, VLM phase labels with JSON validation, SAM 3 object tracking and a review UI. It was part of the Gemma 4 Good 1st-place entry.

### Cited Findings

#### LlamaCon Hackathon 2025 (SF, May 3–4, 2025; 24 h)

**OrgLens (1st)**
- Repo: [TheCl3m/llama-hack](https://github.com/TheCl3m/llama-hack), licensed **CC BY-NC 4.0** (non-commercial; the API reports NOASSERTION). Video: [YouTube 8OmMnODOyLw](https://www.youtube.com/watch?v=8OmMnODOyLw), **78 s**. Links: [Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/).
- Stack: Django backend and React frontend, with `OrganizationGraph.jsx`, `ContributorNode.jsx` and `LlamaChat.jsx` components. The backend ships precomputed GitHub contributor JSON dumps (`github_contributors_simplified_issues_commits_v4.json`) and a `create_summaries` management command — [repo tree](https://github.com/TheCl3m/llama-hack).
- Model use: the OpenAI SDK with `base_url="https://api.llama.com/compat/v1/"`, model `Llama-4-Maverick-17B-128E-Instruct-FP8`, `stream=True`, served through a Django `StreamingHttpResponse` — [backend/api/views.py](https://github.com/TheCl3m/llama-hack/blob/HEAD/backend/api/views.py).
- Hardware: none. Eval: none found.
- Reuse: low, because the license is non-commercial and the project is unrelated to our ideas.

**Compliance Wizards (2nd)**
- Repo: [michaelwaves/llamacon-hackathon](https://github.com/michaelwaves/llamacon-hackathon), **no license**. Video: [YouTube JgZQ6XJXBhE](https://youtu.be/JgZQ6XJXBhE), **166 s**.
- Stack: a FastAPI backend with separate "agents" (`agent_kyc.py`, `agent_transactions.py`, `agent_communications.py`), an OFAC sanctions CSV and a CourtListener lookup, plus a Next.js/shadcn frontend — [repo tree](https://github.com/michaelwaves/llamacon-hackathon).
- Model use: raw HTTP POSTs to `https://api.llama.com/v1/chat/completions` with Llama-4-Maverick, for example to generate fraud-notification emails. KYC uploads an image as a base64 data URL to `kyc_agent_multimodal` — [backend/agent_communications.py](https://github.com/michaelwaves/llamacon-hackathon/blob/HEAD/backend/agent_communications.py); [backend/main.py](https://github.com/michaelwaves/llamacon-hackathon/blob/HEAD/backend/main.py).
- The "AI voice assistant" is the third-party **Bland AI** phone-call API (`send_prompt_to_bland_ai`, voice "June"), plus Toolhouse — [agent_communications.py](https://github.com/michaelwaves/llamacon-hackathon/blob/HEAD/backend/agent_communications.py). The 2025 rules evidently allowed non-Llama runtime components **[inferred]**.
- Reuse: none (no license, off-topic).

**Llama CCTV Operator (3rd; Agajan Torayev)**
- Repo: [torayeff/llamacon-hackathon-2025-sf](https://github.com/torayeff/llamacon-hackathon-2025-sf), **Apache-2.0**. Video: [YouTube 4YaZe4Gbt1g](https://youtu.be/4YaZe4Gbt1g), **55 s**.
- Stack: Python FastAPI backend, Next.js frontend, and go2rtc restreaming a local MP4 as RTSP for the demo (`streams: hackathon: ffmpeg:../../localdata/hackathon_demo_short.mp4#video=h264`) — [streamer/go2rtc.yaml](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/streamer/go2rtc.yaml).
- The pipeline is detailed in Q3.
- Hardware: none. Any RTSP camera would work; the demo used a replayed file — [streamer/README.md](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/streamer/README.md).
- Eval: none in the repo or README. The README walks through the UI in 5 screenshots — [README](https://github.com/torayeff/llamacon-hackathon-2025-sf).
- Builder background: Torayev also maintains `fanucpy` (337★, a Python interface for FANUC robots) and `mfgrl` (a manufacturing RL environment), so he is a manufacturing and robotics domain insider — [github.com/torayeff](https://github.com/torayeff?tab=repositories).

**Geo-ML / geo-lm (Best Llama API Usage; geologist William Davis)**
- Repo: [williamjsdavis/geo-lm](https://github.com/williamjsdavis/geo-lm), **MIT**, 96★, still developed into 2026. Video: [YouTube U1fDn1C3DJA](https://youtu.be/U1fDn1C3DJA), **187 s**, titled "(demo @ 2:07)".
- Architecture: a FastAPI `api/` with `documents`, `dsl`, `models` and `workflows` routers. `geo_lm/parsers/dsl/ast.py` parses a geology DSL, and `geo_lm/gempy/{builder,validator,transformer,exporter}.py` turn it into 3D GemPy models — [repo tree](https://github.com/williamjsdavis/geo-lm).
- Its OpenAI provider accepts an optional `base_url` for OpenAI-compatible endpoints. `.env.example` lists `LLAMA_API_KEY`, but the current defaults are Claude Sonnet 4 — [providers/openai.py](https://github.com/williamjsdavis/geo-lm/blob/HEAD/geo_lm/ai/providers/openai.py); [.env.example](https://github.com/williamjsdavis/geo-lm/blob/HEAD/.env.example).
- Meta's write-up: it converts ~400-page reports into a structured geology DSL and then into 3D subsurface models, using Llama 4 Maverick and GemPy. Davis said: "I spend most of my time reading through geology documents" — [Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/).
- Reuse: the pattern of an LLM emitting a constrained DSL, a validator, then a deterministic builder.

#### Meta Llama 3 Hackathon (SF, May 2024; 24 h)

**OpenGlass (1st)**
- Repo: [BasedHardware/OpenGlass](https://github.com/BasedHardware/OpenGlass), **MIT**, 4.2k★. It has since moved to [BasedHardware/omi/omiGlass](https://github.com/BasedHardware/omi/tree/main/omiGlass) (MIT, 13.9k★, active Nov 2026).
- Links: Devpost [openglass](https://devpost.com/software/openglass). Video: [YouTube DsM_-c2e1ew](https://youtu.be/DsM_-c2e1ew), **43 s**, 17.6k views.
- Hardware, stack and model use are covered in Q2.
- Eval: none. The demo described in Meta's recap identified fruit in a bowl and gave calorie counts — [Meta AI blog](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/).

**SixthSense (highlighted; did not place)**
- Repo: [EllAchE/llama-out-loud](https://github.com/EllAchE/llama-out-loud), **no license**.
- Glasses integration: "Because Meta Raybans don't expose an SDK," the team livestreamed from the glasses to a phone. An iOS Shortcut took a screenshot **every 5 s** and POSTed it to a Flask server on the same network — [README](https://github.com/EllAchE/llama-out-loud).
- Stack: Llama 3 on Groq, Brave search, Neurosity EEG, ElevenLabs/Vapi voice. The listed challenge was "Meta Raybans don't have SDK" — [Devpost](https://devpost.com/software/sixthsense-enhance-physical-knowledge-w-neurofeedback).

#### Llama Impact Hackathon London (Nov 2024)

**Gripmind (2nd)**
- Repo: no public GitHub repo was found.
- Meta's description: an open-source robotic arm for assisted living, controlled by brain signals, voice or images, built on Llama 3.2 Vision — [Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/).
- Hardware details are in Q4. Linking the Hugging Face artifacts to Gripmind is **[inferred]**.

#### Google Gemini API Developer Competition (May–Aug 2024; winners Nov 21, 2024)

**Jayu (Best Overall)**
- Repo: no public repo. The developer said he kept his GitHub hidden (seen only as a search snippet of the [AI dev forum thread](https://discuss.ai.google.dev/t/the-stats-behind-the-winning-submission/50664); the page returned 404 when fetched).
- Architecture: a Flash model acts as controller and uses function calling to invoke other Gemini models. Pro models analyze app windows with vision, and object detection lets Jayu click buttons it sees on screen. STT, TTS and gesture recognition are built in — [ai.google.dev project page (search snippet)](https://ai.google.dev/competition/projects/jayu?hl=en).
- Video: [YouTube shnW3VerkiM](https://www.youtube.com/watch?v=shnW3VerkiM), **180 s**, 22k views. The description says he "had to cut over 10 minutes of Demo footage," and that the terminal is shown only for demonstration because Jayu runs in the background — [YouTube](https://www.youtube.com/watch?v=shnW3VerkiM).

**Gaze Link (Best Android App)**
- Repo: none; only a Play Store listing exists (package `com.demo.opencv`) — [Android Developers Blog](https://android-developers.googleblog.com/2024/11/gaze-link-wins-best-android-app-gemini-api-developer-competition.html?hl=en).
- How it works: ML Kit face detection reads eye gestures, and Gemini 1.5 Flash expands keywords plus the caretaker's spoken question into a sentence. For example, the context "Is the room temperature ok?" with keywords "hot AC two" becomes a full request. It supports English, Spanish and Chinese — [Android Developers Blog](https://android-developers.googleblog.com/2024/11/gaze-link-wins-best-android-app-gemini-api-developer-competition.html?hl=en).
- Proof: users type with six eye gestures. The developer claims up to 85% keystroke savings in tests with 30 people and 7x the effectiveness of eye-transfer boards (self-reported) — [ai.google.dev project page (search snippet)](https://ai.google.dev/competition/projects/gaze-link).
- Video: [YouTube y_U1vkEC9PA](https://youtu.be/y_U1vkEC9PA), **133 s**.

**Vite Vere (winner, "Solve real-world problems" group; exact category not verified)**
- Video: [YouTube yul0L5YWBp0](https://youtu.be/yul0L5YWBp0), **180 s**, 20.8k views. The app gives step-by-step guidance for people with intellectual disabilities — [YouTube](https://youtu.be/yul0L5YWBp0); [Google blog](https://blog.google/technology/developers/gemini-api-developer-competition-winners/).
- The original repo was not found. The successor is [guidomarangoni/vite-vere-offline](https://github.com/guidomarangoni/vite-vere-offline) (**MIT**), built with Flutter and flutter_gemma and based on gerfalcon/offline_menu_translator. It moved from cloud Gemini to on-device Gemma 3n — [README](https://github.com/guidomarangoni/vite-vere-offline).

#### Gemma 3n Impact Challenge (Kaggle, 600+ projects)

**Winners** — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/):
- 1st: **Gemma Vision**.
- 2nd: **Vite Vere Offline**.
- 3rd: **3VA** (pictogram AAC, fine-tuned with MLX).
- 4th: **Sixth Sense for Security Guards**. A lightweight YOLO-NAS model flags motion, then hands it to Gemma 3n to separate benign events from threats; it handles 16 cameras.
- Unsloth prize: **Dream Assistant**.
- Ollama prize: **LENTERA**.
- LeRobot prize: Gemma 3n plans while an IGMC model predicts latencies.
- Jetson prize: **My (Jetson) Gemma**.

**Gemma Vision (1st)**
- Repo: [TGTech06/gemma-vision](https://github.com/TGTech06/gemma-vision), **MIT**, 42★, Flutter/Dart.
- The README thanks "my brother Matteo and the blind community" — [README](https://github.com/TGTech06/gemma-vision). Pipeline details are in Q2.
- Write-up (unreadable here): [Kaggle](https://www.kaggle.com/competitions/google-gemma-3n-hackathon/writeups/gemma-vision).

#### Gemma 4 Good Hackathon (Kaggle)

**Winners** — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/):
- 1st: **GEM-4**.
- 2nd: **Trido**.
- 3rd: **PenguinAgent**. It uses Gemma 4 26B, SAM 3 and SigLIP 2 for tracking.
- 4th: **DEMENTOR**. It combines camera feeds, haptic feedback and a sensor network, with Gemma 4 E2B on the edge.
- **Gilbeot**: landmark-based walking navigation with LiteRT-LM.
- **Gem-Care**: dysarthric-speech recognition that cut WER from 32.7% to 19.0%.

**GEM-4 (1st)** — teardown in Q4.

**PenguinAgent (3rd)**
- Repo: [and0sha/PenguinAgent](https://github.com/and0sha/PenguinAgent), **CC-BY-4.0**.
- Pipeline: SAM 3, pinned to commit `847e1a3`, extracts image-space positions, velocities and mask areas into `tracks.json`. SigLIP2 plus a linear probe classify species. `gemma4:26b` on Ollama turns the frames and telemetry into reports — [README](https://github.com/and0sha/PenguinAgent).

#### Gemini 3 Hackathon (Devpost, Google DeepMind; deadline Feb 10, 2026)

**Results**
- Grand Prize **Globot**, 2nd **Aegis**, 3rd **Netra**, plus 10 honorable mentions — [Devpost winners JSON-LD](https://gemini3.devpost.com/project-gallery).
- The submission required a ~200-word description and a **3-minute demo video** — [orendra.com (search snippet)](https://orendra.com/blog/the-gemini-3-hackathon-2026-a-deep-dive-into-deadlines-rules-and-developer-opportunities/).

**Globot (Grand Prize)**
- Repo: [Vector897/Globot](https://github.com/Vector897/Globot), **MIT**, 32★. Video: [YouTube FM2LGhqMnC8](https://youtu.be/FM2LGhqMnC8), **146 s**.
- Design: a "5-Agent AI Reasoning Engine" with these agents:
  - Market Sentinel
  - Risk Hedger
  - Logistics Orchestrator
  - Compliance Manager, which reads 500-page policies
  - Adversarial Debate red-team
- Stack: FastAPI, CrewAI, React/TypeScript, Deck.gl 3D globe, Gemini 3 Flash plus Gemini Vision for satellite imagery, Gemini Embeddings, ChromaDB and Clerk. All critical decisions need human approval.
- Claim: detects port congestion "6 hours before official announcements" (unverified) — [Devpost](https://devpost.com/software/globot-341w9q).

**Aegis (2nd)**
- Repo: [iamdanishm/aegis](https://github.com/iamdanishm/aegis), **no license**. Live demo: [aegis-psi-liart.vercel.app](https://aegis-psi-liart.vercel.app). Video: [YouTube UCYckQYVM2Q](https://youtu.be/UCYckQYVM2Q), **167 s**.
- Design: Next.js 14 server actions run parallel agents (Coordinator, Triage, Surveillance, Logistics, Reporter). Search grounding was added to stop invented locations. A "Spotlight Protocol" shows the reasoning trace only for the top-priority incident, and "Protocol Zero" requires human approval for high-stakes actions.
- Lesson the team stated: "processing incidents sequentially is too slow" — [Devpost](https://devpost.com/software/aegis-autonomous-multi-agent-crisis-command).

**Netra (3rd)**
- Repo: [ZentraHost/netra_project](https://github.com/ZentraHost/netra_project), **no license**, 7★. Video: [YouTube Ax3SkwHOkkk](https://youtu.be/Ax3SkwHOkkk), **179 s**.
- Netra has a "Find My..." mode: active frame-by-frame scanning, then "Micro-Navigation" with audio directions that guide the user's hand to the target — [Devpost](https://devpost.com/software/netra-empowering-the-visually-impaired). Pipeline in Q2.
- The write-up is persuasion-heavy, opening with "A Note to the Judges" and calling Netra "the clear and obvious choice for the Grand Prize." It gives no measured evaluation — [Devpost](https://devpost.com/software/netra-empowering-the-visually-impaired).

### Inferences
- Netra's Micro-Navigation is a direct prior-art match for **Find-and-Guide**: it uses a phone camera, a "find X" command and audio hand guidance, and it placed 3rd in Gemini 3. Find-and-Guide must show what SAM 3.1 adds, namely pixel-accurate per-frame tracking instead of an LLM guessing x/y offsets, plus a measured time-to-touch.
- MimicAnno is a direct prior-art match for **DemoScribe**, as a component of the Gemma 4 Good 1st place. DemoScribe should cite it and differentiate on failure labels, success verdicts and cost per episode, rather than present the concept as new.
- No prior art turned up for **Defect Forge**: none of these winners used generative editing to synthesize training defects.

### Gaps
- Kaggle write-ups (Gemma Vision, GEM-4, DEMENTOR, Sixth Sense for Security Guards) could not be read; they are client-rendered.
- No repo was found for Jayu, Gaze Link, the original Vite Vere, Sixth Sense for Security Guards or DEMENTOR.
- The Gemma 4 Good results announcement date was not confirmed. The GEM-4 write-up ID 1778618527713 decodes to a millisecond epoch of about May 12, 2026, and the video is dated May 17, 2026 — [YouTube](https://www.youtube.com/watch?v=OhaIA3bYwmg). Whether results came out in Aug 2026 is unverified.

---

## Q2. How did OpenGlass, Gemma Vision and Netra handle the camera pipeline, latency and feedback to the user, and is their code reusable?

### Takeaway
The three projects use three different camera architectures:

| Project | Capture | Path | Feedback | License |
|---|---|---|---|---|
| **OpenGlass** | Low-rate photos (one every 5 s) from an ESP32-S3 | BLE into a web app; caption each frame in the background, answer questions from text memory | Spoken answer (cloud TTS) | MIT |
| **Gemma Vision** | Photo on a controller button press, from a chest-mounted phone | On-device Gemma 3n | Streamed TTS plus earcons | MIT |
| **Netra** | Continuous phone video, downscaled 480 px JPEG frames at 1 Hz (200 ms in guidance mode) | WebSocket to a FastAPI server; latest frame wins and stale frames are dropped | Web Audio: stereo-panned pitch tone, Geiger clicks, success chord; speech debouncing | None |

Only Netra attempts real-time hand guidance, and its code is unlicensed, so reimplement the pattern rather than copy it.

### Cited Findings

**OpenGlass: hardware and firmware**
- Parts: Seeed XIAO ESP32-S3 Sense, an EEMB LP502030 3.7 V 250 mAh battery and a 3D-printed mount. The README says under $25 — [README](https://github.com/BasedHardware/OpenGlass); Meta's recap says $20 — [Meta](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/).
- BLE GATT service `19B10000-E8F2-537E-4F6C-D104768A1214` exposes three characteristics:
  - audio data (`…0001`), from a 16 kHz PDM mic with PCM, μ-law or Opus codecs
  - photo data (`…0005`, notify)
  - photo control (`…0006`, write)
  
  Control values: −1 takes one photo, 0 stops, and 5–300 sets the capture interval in seconds, rounded to 5 s — [firmware.ino](https://github.com/BasedHardware/OpenGlass/blob/main/firmware/firmware.ino).
- Camera settings: SVGA JPEG at `jpeg_quality=10`, `CAMERA_GRAB_LATEST`, framebuffer in PSRAM. Each photo is split into BLE notifications that each start with a 2-byte little-endian frame index — [firmware.ino](https://github.com/BasedHardware/OpenGlass/blob/main/firmware/firmware.ino).

**OpenGlass: app and model pipeline**
- The client is a React Native/Expo web app using Web Bluetooth (`navigator.bluetooth.requestDevice({filters:[{name:'OpenGlass'}]})`) — [useDevice.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/modules/useDevice.ts).
- It reassembles chunks until a `0xFF 0xFF` end marker, drops the photo on any out-of-order chunk, rotates it 270°, and writes `0x05` to start capture every 5 s — [DeviceView.tsx](https://github.com/BasedHardware/OpenGlass/blob/main/sources/app/DeviceView.tsx).
- Each photo gets captioned by **Moondream 1.8B on Ollama** ("describe the scene… Transcribe any text"). A question then concatenates all captions and sends them to **Llama 3 70B on Groq** (`llama3-70b-8192`) — [imageDescription.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/agent/imageDescription.ts); [groq-llama3.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/modules/groq-llama3.ts).
- The answer is spoken through OpenAI `tts-1`, voice "nova", via a Web AudioContext — [openai.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/modules/openai.ts).
- Captioning runs in the background on photo arrival (an `InvalidateSync` worker plus an `AsyncLock`), so answering a question is a text-only call — [Agent.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/agent/Agent.ts); [DeviceView.tsx](https://github.com/BasedHardware/OpenGlass/blob/main/sources/app/DeviceView.tsx).
- A Moondream YES/NO "is this image blurry" check exists — [imageBlurry.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/agent/imageBlurry.ts).
- Code quality: `combined + '\n\nImage #' + i + '\n\n'` is a no-op, so image indices never reach the prompt — [Agent.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/agent/Agent.ts).
- Devpost confirms the stack (Moondream on Ollama, Llama 3 on Groq, TTS, TypeScript) and names the main challenge: a mount that fits any glasses — [Devpost](https://devpost.com/software/openglass).

**Gemma Vision**
- Runs `gemma-3n-E2B-it-int4.task` on device through `flutter_gemma` ^0.10.0, with `supportImage: true`, `maxNumImages: 1` and `maxTokens: 8192`. Responses stream via `generateChatResponseAsync()`, and the app records time to first token, prefill speed and decode speed — [gemma_service.dart](https://github.com/TGTech06/gemma-vision/blob/HEAD/lib/chat_page/services/gemma_service.dart).
- The model is a ~3 GB download — [README](https://github.com/TGTech06/gemma-vision).
- Hardware: the phone is strapped to the chest because holding a phone while using a cane is impractical. Input is an 8BitDo Micro controller or voice — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/).
- The controller runs in keyboard mode, with buttons mapped in 8BitDo Ultimate Software. The README advises turning off TalkBack/VoiceOver when using it — [README](https://github.com/TGTech06/gemma-vision).
- `keyboard_handler.dart` dispatches F1–F10, arrows and Enter/Select/Space through `LogicalKeyboardKey` — [keyboard_handler.dart](https://github.com/TGTech06/gemma-vision/blob/HEAD/lib/chat_page/handlers/keyboard_handler.dart).
- Feedback (`StreamingTtsService`):
  - `flutter_tts` speaks streamed tokens as segments, at speech rate 0.5, with markdown stripped.
  - It auto-resumes after TalkBack interruptions (6 s delay, up to 5 attempts).
  - It plays a looping loading sound while waiting for the model.
  
  — [streaming_tts_service.dart](https://github.com/TGTech06/gemma-vision/blob/HEAD/lib/chat_page/services/streaming_tts_service.dart).
- Other dependencies include `camera`, `speech_to_text`, `google_mlkit_text_recognition` (OCR) and `wakelock_plus` — [pubspec.yaml](https://github.com/TGTech06/gemma-vision/blob/HEAD/pubspec.yaml).

**Netra: client**
- Opens the rear camera with `getUserMedia({video:{facingMode:'environment', width:1280}})` — [static/js/main.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/main.js).
- Each tick draws the video to a canvas 480 px wide and sends a JPEG at quality 0.4 as a binary WebSocket message. The tick is 1000 ms in navigation mode and **200 ms in micro (hand-guidance) mode** — [main.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/main.js); [config.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/config.js).
- WebSocket reconnect backs off exponentially (`1000·1.5^n`, capped at 5 s) — [network.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/network.js).

**Netra: server**
- A producer loop receives frames, and a consumer waits on an `asyncio.Event`. While a frame is being processed, new frames overwrite `latest_frame` and count as `frames_skipped`. This "HEAD-OF-LINE BLOCKING STRATEGY" means the model always sees the newest frame and the queue never grows — [app/routes/websocket.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/routes/websocket.py).
- Micro mode resizes frames to 224×224 and calls `gemini-3-flash-preview` with JSON output at temperature 0.1. It returns `{x, y, action, guidance_speech, ms}` — [app/services/processor.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/services/processor.py).
- The micro prompt asks for X and Y in −100…100 relative to image center (plus "Target not visible") — [app/prompts.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/prompts.py).
- Navigation mode resizes to 224×160 and uses a 20 s `asyncio.wait_for` timeout — [config.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/config.py); [processor.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/services/processor.py).

**Netra: audio feedback** (`SpatialAudio`, Web Audio)
- A continuous triangle oscillator runs during guidance:
  - x maps to `StereoPannerNode` pan, as x/20 clamped to ±1.
  - y maps to pitch, 440 Hz ± (y/20)·200, clamped to 100–1000 Hz.
- Geiger clicks repeat every `250 − proximity·200` ms, at 1000 + proximity·800 Hz.
- On `action:'push'`, a C5–E5–G5 chord plays.
- Navigation mode uses a short sonar ping panned toward the object (880 Hz if critical), and speech goes through `window.speechSynthesis`.

— [static/js/audio.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/audio.js); [network.js](https://github.com/ZentraHost/netra_project/blob/HEAD/static/js/network.js).

**Netra: speech control and tracking**
- `SpeechManager`:
  - Critical messages always interrupt.
  - Otherwise there is no interrupt unless priority rises and the object comes ≥0.3 m closer.
  - Per-priority repeat cooldowns are 1/2/4/8 s, with a 3 s global cooldown and a 10 s per-subject cooldown.
  - Speech duration is estimated at 2.5 words/s plus 0.5 s.
  
  — [app/services/speech.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/services/speech.py); [config.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/config.py).
- `VisualTracker` keys tracks by object name. It requires confidence ≥75 and 2 consecutive frames before an object counts as stable, drops tracks after 2 s, and treats the closest stable object as primary — [app/services/tracking.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/services/tracking.py).
- Distances come from the model's JSON output, against thresholds of 0.5, 1.0 and 2.0 m — [config.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/config.py).

### Inferences
- **Latency.** In micro mode Netra's effective guidance rate is capped by Gemini round-trip time, not by the 200 ms tick, because frames are dropped while a call is in flight. The project logs per-call `ms` but publishes no number. With SAM 3.1 video tracking we can do better: run Muse Spark (or a SAM text prompt) once to locate the target, then update the tone from per-frame tracked centroids, smoothly between model calls.
- **x/y scaling quirk.** Netra's pan saturates at |x| ≥ 20 out of ±100, so most of the left-right range sounds hard-panned. Map the full range, or use a nonlinear curve.
- **OpenGlass reusability.** It is MIT, and its firmware and BLE chunk protocol work as a cheap glasses camera. Its fastest capture interval is 5 s, though, which is far too slow for hand guidance. Use a phone or webcam first, or rewrite the firmware for continuous MJPEG over WiFi.
- **Model swaps under the Meta-only rule.**
  - Moondream, Groq-Llama 3 and OpenAI TTS must all be replaced.
  - Muse Spark (OpenAI-compatible `chat.completions` with `image_url`) can take over captioning and Q&A.
  - Speech output is the open question. Netra (browser `speechSynthesis`) and Gemma Vision (`flutter_tts`) both use OS speech engines. Whether an OS engine counts as a "model called at runtime" is unclear, so earcons and tones (Netra-style) are the rule-safe primary channel.
- **Gemma Vision reusability.** It is MIT and on-device. Its reusable parts are the interaction design and Flutter services: controller keymap, streaming TTS segmenter, loading earcon and TalkBack resume. Its inference path (Gemma 3n) is not allowed under our rule.

### Gaps
- No measured end-to-end latency was found for any of the three. Netra's write-up asserts a "0.5-meter safety rule" that only Gemini 3's speed makes possible, but gives no numbers — [Devpost](https://devpost.com/software/netra-empowering-the-visually-impaired).
- No user study or quantitative evaluation was found for Gemma Vision or Netra.
- Netra's `TrackedObject.update` smoothing method was not read in full. The class does keep raw and smoothed distance and direction — [models.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/models.py).
- DEMENTOR's haptic implementation was not found.

---

## Q3. How did Llama CCTV Operator detect video events with zero fine-tuning, and what did the pipeline look like?

### Takeaway
It is a three-thread, two-queue Python pipeline built entirely on prompting:
1. OpenCV records the RTSP stream into **5-second MP4 chunks**.
2. Each chunk is sampled at **1 frame per second**, and the frames go as base64 PNG data URLs in a single OpenAI-SDK `chat.completions` call.
3. That call lists operator-written events as `code: description + detection guidelines` and forces a **JSON schema** of `{event_code, detected, explanation}` per event.
4. Detected events go onto a queue, into a DB, and out to a Next.js dashboard.

It is Apache-2.0 and already parameterized by `base_url` and `model`, so it ports to `https://api.meta.ai/v1` with essentially a config change.

### Cited Findings
- Architecture, per the README's mermaid diagram: RTSP Stream → Video Stream Chunker, which saves N-second files and enqueues their paths → Video Event Detector (Llama 4) → Event Queue → DB Writer → DB. The objectives include "Allow users to define specific events to track" and "detect these events in video chunks" — [README](https://github.com/torayeff/llamacon-hackathon-2025-sf).
- Chunker:
  - It reads the stream with `cv2.VideoCapture` and defaults to `chunk_duration=5` seconds.
  - Files are named `<startYYYYmmddHHMMSS>_<end>.mp4`.
  - Reconnects back off exponentially, capped at 60 s.
  
  — [backend/video_stream_chunker.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_stream_chunker.py).
- Detector:
  - `video_to_frames` takes one frame per second of video, chosen as the first, last or a random frame within that second.
  - Frames are PNG-encoded as `data:image/png;base64,…`.
  - The system prompt reads: "video analytics agent specialized in factual event detection… based strictly on visual and contextual evidence… Do not infer or assume… {context}… Format your response as JSON."
  - The user prompt lists `- {event_code}: {event_description} {detection_guidelines}`, and every frame is appended as an `image_url` part.
  - The call is `client.chat.completions.create(..., response_format={"type":"json_schema","json_schema":{...events[]: event_code, detected(bool), explanation}})`.
  
  — [backend/video_event_detector.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_event_detector.py).
- Orchestration: `app.py` runs three daemon threads (chunker, detector worker and event collector) over `queue.Queue(maxsize=100)`. `/start` takes `model`, `base_url`, `chunk_duration`, `context` and the event list — [backend/app.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/app.py).
- The frontend defaults are `Llama-4-Maverick-17B-128E-Instruct-FP8` and `https://api.llama.com/compat/v1/`, both editable in the UI — [frontend/app/page.tsx](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/frontend/app/page.tsx).
- The UI flow, from the README screenshots: welcome, then stream URLs, then event definition (code, description, guidelines), then a monitoring dashboard with live feed, events and detection log, then event detail — [README](https://github.com/torayeff/llamacon-hackathon-2025-sf).
- Meta described it as sampling "every fifth frame" and checking for movement — [Meta AI blog](https://ai.meta.com/blog/llamacon-hackathon/). **This conflicts with the code**, which sends 1 fps over 5-second chunks, about 5 frames per call. The repo also has no motion-gating code — [video_event_detector.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_event_detector.py).
- Comparable pattern: the Gemma 3n 4th-place "Sixth Sense for Security Guards" put a cheap gate in front of the VLM, using lightweight YOLO-NAS for initial motion before Gemma 3n — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/).

### Inferences
- **Porting to Meta.** Set `base_url=https://api.meta.ai/v1` and `model=<Muse Spark 1.3 id>`. Then check three things against Meta docs: `response_format` `json_schema` support, the data-URL image limit (the earlier report says up to 50 images per request), and the PNG payload size. Switching to JPEG would cut upload size cheaply.
- **For DemoScribe.** The same detector turns robot demo videos into per-chunk failure events with no fine-tuning. Define `event_code`s such as `GRASP_SLIP`, `MISSED_GRASP`, `COLLISION` and `TASK_SUCCESS` with detection guidelines, then run them over 5-second chunks. A SAM 3.1 mask or track overlay can serve as the "context."
- **For Defect Forge.** The `_build_user_message` plus `json_schema` pattern can be reused as the inspector call: spec context, 8 forged examples, a query image, and `{defect, type, box}` output.
- **Fixing its weaknesses.** The pipeline is fully serial: one call per chunk, with no motion gate and no event merging across chunks. Cheap upgrades are classical frame-difference gating (not a model, so the runtime rule holds) and parallel calls. Aegis's team found sequential processing too slow — [Devpost](https://devpost.com/software/aegis-autonomous-multi-agent-crisis-command).

### Gaps
- No accuracy, latency or cost numbers were published for the CCTV Operator.
- The 55-second video's content structure is unknown beyond its title and description — [YouTube](https://youtu.be/4YaZe4Gbt1g).

---

## Q4. How did Gripmind and the Gemma 4 Good VLA robot (GEM-4) integrate hardware within a hackathon timeline?

### Takeaway
- **Gripmind** (24 h) took the LeRobot route. The team recorded teleoperated demonstrations on a low-cost LeRobot arm (named "moss") during the event, trained one **ACT** policy per task, and used Llama 3.2 as a router that picks which policy to run from voice or images. EEG control came from the team's own pre-trained EEG model.
- **GEM-4** was a weeks-long research effort. It pretrained a custom Gemma-4-E2B VLA on Open X-Embodiment (OXE), fine-tuned it on LIBERO and on reBot Arm demonstrations (200–300 episodes per task), and served it from a FastAPI `/predict` endpoint in ~220 ms per call. It also built a data engine: MimicRec for recording and MimicAnno for Gemma-4-31B and SAM 3 annotation.

None of GEM-4's training is reproducible in 31 hours. Its MimicAnno annotation pipeline is reusable, though, and it is DemoScribe-shaped.

### Cited Findings

**Gripmind**
- Meta says it placed 2nd: an open-source robotic arm for assisted living, controlled by brain signals, voice or images, using Llama 3.2 Vision — [Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/).
- A Hugging Face post by Francesco Capuano describes an EEG-controlled arm built at Cerebral Valley's London Llama hackathon (24 h, 200+ participants, 50+ teams). The team "used Llama-3.2 models to handle user interactions and switch between tasks," "trained multiple RL-policies" with LeRobot, and collected "100GB+" of data. Links: policies moss-pills, moss-cup and meta-grasp; datasets pills, cup and cupim; a demo at [x.com/_fracapuano/status/1858102728691458554](https://x.com/_fracapuano/status/1858102728691458554) — [huggingface.co/fracapuano](https://huggingface.co/fracapuano).
- The Hugging Face API shows:
  - `fracapuano/moss-pills`, `moss-cup` and `test-moss-pick`, created **Nov 17, 2024**, and `meta-grasp`, created **Nov 18, 2024**, all tagged `lerobot`, `act` and `robotics`.
  - Datasets `moss_grasping` and `moss_pick` (Nov 16), and `moss_push`, `pills` and `cup` (Nov 17).
  - An EEG model, `EEGViT` (MIT), created Nov 2, 2024, before the event.
  
  — [HF models API](https://huggingface.co/api/models?author=fracapuano&limit=50); [HF datasets API](https://huggingface.co/api/datasets?author=fracapuano&limit=50).
- The post says "RL-policies," but the model tags say `act` (Action Chunking Transformer, an imitation-learning method) — [HF models API](https://huggingface.co/api/models?author=fracapuano&limit=50).

**GEM-4: system and hardware**
- Placed 1st. Judges cited its "closed-loop data engine" and VLA architecture. Gemma 4 31B labels video clips, and a fine-tuned E2B acts as the controller — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/).
- It is a wearable "second arm" for blind or upper-limb-impaired users. "Hey GEM" voice goes through STT, and the text plus camera images and joint states go to the VLA, which outputs the next actions. Average LIBERO success is 74% — [inside.com.tw](https://inside.com.tw/article/42203-google-gemma-4-good-challenge).
- Hardware: reBot Arm, Intel RealSense and GoPro cameras (wrist and chest), with onboard inference on an NVIDIA Jetson AGX Orin and a Raspberry Pi 5 — [YouTube description](https://www.youtube.com/watch?v=OhaIA3bYwmg).
- Video: **178 s**, 46.7k views. Per its description it covers hardware setup, basic manipulation tasks, the VLA architecture, and a continuous-learning workflow with MimicAnno and MimicRec — [YouTube](https://www.youtube.com/watch?v=OhaIA3bYwmg).

**GEM-4: model, training and serving**
- Repo: [takaki-maeda-99/GEM-4-VLA](https://github.com/takaki-maeda-99/GEM-4-VLA), **Apache-2.0**, created Apr 29, 2026.
- Model: SigLIP + Gemma-4-E2B + per-domain projectors + an L1 action head, using a Prismatic-style codebase (`src/prismatic/…`).
- Training: pretrained 100k steps on 9 OXE datasets plus a LIBERO mix, then fine-tuned for 50k steps.
- LIBERO results (10 episodes × 10 tasks = 100 per suite): spatial 72%, object 92%, goal 89%, long 43%, **average 74%**. Checkpoints are on Hugging Face (`takaki99/GEM-4-FT-*`).
- Fine-tune batch: 2–4 GPUs at an effective batch of 32 or 128.
- reBot Arm single-task fine-tunes: "pick up the bottle" (best at step 30k) and "open the jar" (best at step 15k).
- Serving: FastAPI hosts a checkpoint behind MimicRec's `POST /predict` and returns denormalized action chunks, at ~220 ms per request on an RTX 6000 Ada in bf16 (266 ms budget). A separate env targets the Jetson (JetPack 6, sm_87).

— [README](https://github.com/takaki-maeda-99/GEM-4-VLA)

**GEM-4: data engine**
- **MimicRec** ([repo](https://github.com/takaki-maeda-99/MimicRec), **Apache-2.0**) is a local-first web app: React on :5173 and FastAPI with a WebSocket on :8000. It handles teleoperation, hand-teaching, record, review, replay and VLA inference, and exports LeRobot v3 or pushes to the Hugging Face Hub.
  - Verified hardware: SO-101 (LeRobot `SOFollower`), SO Leader, reBot Arm B601-DM, Isaac Sim and a mock adapter.
  - Meta Quest 3/3S teleoperation is implemented, but its hardware integration is still pending.
  
  — [README](https://github.com/takaki-maeda-99/MimicRec)
- **MimicAnno** ([repo](https://github.com/takaki-maeda-99/MimicAnno), **Apache-2.0**) does offline subtask annotation of LeRobot v3 episodes:
  - **Signal-driven boundaries**, with no ML: gripper transitions, end-effector velocity valleys and action-norm change points.
  - **VLM phase labeling** with Gemma 4 "or any image-text-to-text HF model." Labels are enforced against an allowed set and validated with a JSON schema.
  - **SAM3 object tracking** from task-text prompts.
  - Temporal smoothing (merging and an optional Viterbi relabel).
  - SARM-ready export and a React/Vite review UI.
  - Adapters for SO100, Koch and Aloha, plus YAML-configurable ones.
  
  — [README](https://github.com/takaki-maeda-99/MimicAnno).
- MimicAnno internals:
  - Boundary weights are `gripper_transition 0.50` and `eef_velocity_valley 0.25`, and the gripper Δ threshold is 0.30 — [mimicanno/boundaries.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/boundaries.py).
  - The labeler is a `VLMLabeler` Protocol. `parse_and_validate` checks that `phase ∈ allowed ∪ {unknown}` and that `vlm_confidence ∈ [0,1]`.
  - Each failure type gets its own retry instruction (JSON parse error, schema violation, invalid label, confidence out of range, timeout).
  
  — [mimicanno/vlm_labeler.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/vlm_labeler.py); [mimicanno/vlm_prompt.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/vlm_prompt.py).
  - The SAM3 runtime wraps `build_sam3_video_predictor` through a git submodule (a fork of SAM 3, `gayagayataiga/sam3`) — [object_tracker/sam3_runtime.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/object_tracker/sam3_runtime.py); [.gitmodules](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/.gitmodules).
  - `eval/metrics.py` includes `compute_planner_agreement` — [eval/metrics.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/eval/metrics.py).
- Public datasets fetched by MimicAnno: `Gayagaya/SO101_dataset` (33 episodes, 4,960 frames), `takaki99/GEM4_open_the_jar` (~208 episodes), `GEM4_pick_up_bottle` (~304) and `GEM4_replace_the_cookie` (~216), all in LeRobot v3 format — [README](https://github.com/takaki-maeda-99/MimicAnno).
- Gemma 3n's LeRobot prize went to a robotics pipeline in which Gemma 3n plans while an IGMC model predicts latencies — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/).

### Inferences
- **What fits a hackathon clock.** Gripmind shows the 24-hour recipe: an off-the-shelf LeRobot arm, teleoperated data collected on site, ACT policies trained per task, and the LLM used only as a router. The hardware risk is calibration and data collection, not model training. The "moss" naming suggests the Moss v1 arm that LeRobot supports, but that is inferred.
- **GEM-4's timeline.** Repos created Apr 29, 2026, a video on May 17, and multi-GPU OXE pretraining point to a weeks-long Kaggle effort, not a sprint.
- **For DemoScribe.**
  - MimicAnno's `VLMLabeler` Protocol lets us drop in a `MuseSparkLabeler` that uses the OpenAI SDK against `api.meta.ai/v1`.
  - `SAM3Runtime` could be replaced by SAM 3.1 calls, either through the Meta API or local SAM 3.1 weights.
  - The GEM4 and SO101 LeRobot datasets could serve as ready inputs, pending a license check.
- **Novelty risk.** Because MimicAnno exists and was part of the Gemma 4 Good winner, a judge who knows it may see DemoScribe as derivative. The differentiators are failure labels and success verdicts, video-only input (no robot state), a Muse Spark video-understanding comparison, and an agreement number against human labels.

### Gaps
- Gripmind's GitHub repo, its exact arm model, its EEG headset, and how Llama 3.2 Vision was wired in were not found.
- The GEM-4 Kaggle write-up (wearable mount, latency on the Jetson, MimicAnno accuracy) could not be read.
- Licenses of the `takaki99/*`, `Gayagaya/*` and `fracapuano/*` datasets were not checked.

---

## Q5. Which repos are permissively licensed and adaptable to an OpenAI-compatible API (api.meta.ai/v1), and what reusable code maps to each of our three ideas?

### Takeaway
Permissive and directly adaptable:
- **CCTV Operator** (Apache-2.0): already uses the OpenAI SDK with a configurable `base_url`.
- **geo-lm** (MIT): its OpenAI provider takes `base_url`.
- **OpenGlass/omiGlass** (MIT): BLE camera firmware plus a web client. Swap its HTTP model calls.
- **Gemma Vision** and **Vite Vere Offline** (MIT): UI and accessibility services only, since their inference is on-device Gemma.
- **MimicAnno**, **MimicRec** and **GEM-4-VLA** (Apache-2.0): pluggable VLM labeler.
- **Globot** (MIT): CrewAI multi-agent pattern.
- **PenguinAgent** (CC-BY-4.0): attribution required.

Not reusable as code:
- Netra, Aegis, Compliance Wizards and SixthSense: no license.
- OrgLens: CC BY-NC 4.0.

### Cited Findings

License table, from the GitHub API or LICENSE file:

| Repo | License | OpenAI-compatible today? | Source |
|---|---|---|---|
| torayeff/llamacon-hackathon-2025-sf (CCTV) | Apache-2.0 | Yes: `OpenAI(api_key, base_url)`, `chat.completions`, `json_schema` | [video_event_detector.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_event_detector.py) |
| williamjsdavis/geo-lm | MIT | Yes: provider takes `base_url` | [providers/openai.py](https://github.com/williamjsdavis/geo-lm/blob/HEAD/geo_lm/ai/providers/openai.py) |
| BasedHardware/OpenGlass | MIT | Partly: Groq uses an OpenAI-compatible URL; Ollama and OpenAI TTS need swapping | [groq-llama3.ts](https://github.com/BasedHardware/OpenGlass/blob/main/sources/modules/groq-llama3.ts) |
| BasedHardware/omi (omiGlass) | MIT | n/a: maintained firmware and app | [omiGlass](https://github.com/BasedHardware/omi/tree/main/omiGlass) |
| TGTech06/gemma-vision | MIT | No: on-device flutter_gemma | [gemma_service.dart](https://github.com/TGTech06/gemma-vision/blob/HEAD/lib/chat_page/services/gemma_service.dart) |
| guidomarangoni/vite-vere-offline | MIT | No: on-device | [README](https://github.com/guidomarangoni/vite-vere-offline) |
| takaki-maeda-99/MimicAnno | Apache-2.0 | Adapter needed: `VLMLabeler` Protocol, local HF Gemma by default | [vlm_labeler.py](https://github.com/takaki-maeda-99/MimicAnno/blob/HEAD/mimicanno/vlm_labeler.py) |
| takaki-maeda-99/MimicRec | Apache-2.0 | n/a: recorder; HTTP VLA client | [README](https://github.com/takaki-maeda-99/MimicRec) |
| takaki-maeda-99/GEM-4-VLA | Apache-2.0 | n/a: local VLA training and serving | [README](https://github.com/takaki-maeda-99/GEM-4-VLA) |
| Vector897/Globot | MIT | Gemini SDK; CrewAI is provider-agnostic **[inferred]** | [Devpost](https://devpost.com/software/globot-341w9q); [repo](https://github.com/Vector897/Globot) |
| and0sha/PenguinAgent | CC-BY-4.0 | Ollama plus local SAM 3 | [README](https://github.com/and0sha/PenguinAgent) |
| huggingface/lerobot | Apache-2.0 (per GEM-4 author's fork listing) | n/a | [takaki-maeda-99 repos](https://github.com/takaki-maeda-99?tab=repositories) |
| ZentraHost/netra_project | **None** | google-genai | [repo](https://github.com/ZentraHost/netra_project) |
| iamdanishm/aegis | **None** | Gemini | [repo](https://github.com/iamdanishm/aegis) |
| michaelwaves/llamacon-hackathon | **None** | Raw Llama API HTTP | [repo](https://github.com/michaelwaves/llamacon-hackathon) |
| EllAchE/llama-out-loud | **None** | Groq | [repo](https://github.com/EllAchE/llama-out-loud) |
| TheCl3m/llama-hack (OrgLens) | **CC BY-NC 4.0** | Yes, but non-commercial | [LICENSE](https://github.com/TheCl3m/llama-hack/blob/HEAD/LICENSE) |

### Inferences

**Reusable-code map. #1 Defect Forge:**
- **Inspector and critic calls.** Take CCTV's multi-image `chat.completions` plus `response_format: json_schema` builder (Apache-2.0) and point it at Muse Spark.
- **Retry loop.** Lift MimicAnno's `parse_and_validate` and its retry instruction per failure type (Apache-2.0) for the critic and schema retries.
- **Spec to taxonomy.** Copy geo-lm's flow of LLM, then a constrained DSL or JSON, then a validator, then a deterministic builder (MIT). Spec text becomes taxonomy JSON, validated before any Muse Image call.
- **Pre-screen.** OpenGlass's YES/NO quality gate prompt (MIT) can be rewritten as a cheap "is this forged patch plausible?" check.
- **Optional phone capture page.** Reimplement Netra's `getUserMedia` → canvas → JPEG upload yourself (Netra is unlicensed, and it's ~20 lines).
- No hardware is needed.

**Reusable-code map. #2 DemoScribe:**
- **Pipeline skeleton.** MimicAnno (Apache-2.0) covers the LeRobot v3 loader, robot adapters, signal boundaries, labeler Protocol (write a Muse Spark labeler), SAM3 tracker interface (point it at SAM 3.1), smoother, export, review UI and agreement metric.
- **Video-only episodes.** CCTV's chunker and event detector (Apache-2.0) handle episodes with no robot state, emitting failure and success events.
- **Telemetry for the LLM.** Follow PenguinAgent's `tracks.json` pattern (CC-BY-4.0): positions, velocities and mask areas from SAM tracks. Credit it if code is reused.
- **Recording.** MimicRec (Apache-2.0) applies only if you own an SO-101 and want live capture.
- **Credit.** MimicAnno and GEM-4 must be cited as prior art in the README and the video.

**Reusable-code map. #3 Find-and-Guide:**
- **Guidance loop.** Reimplement Netra's design without copying its code: a 200 ms client tick, a backend where the latest frame wins and stale frames drop, per-call ms logging, and a JSON reply of `{x, y, action}`.
- **Audio.** Build the earcon layer (pan for x, pitch for y, Geiger rate for proximity, a success chord) from scratch with the Web Audio API (`StereoPannerNode`, `OscillatorNode`).
- **Accessibility services.** Port Gemma Vision's streaming-speech segmenter, loading earcon, TalkBack resume and 8BitDo keymap (MIT) if the app is built in Flutter.
- **Optional glasses camera.** OpenGlass/omiGlass firmware and the BLE chunk protocol (MIT) work, but the 5 s capture interval needs a firmware change before it can support guidance.
- **Speech output.** Prefer tones over TTS because of the runtime-model rule.

**Reusable-code map. All three ideas:**
- CCTV's threaded queue design and reconnect backoff.
- Aegis's "Spotlight" lesson: show reasoning for the top item only, so the UI stays readable. This is a pattern only; the code is unlicensed.
- Globot's and Aegis's human-in-the-loop approval gates.

### Gaps
- It was not confirmed whether `api.meta.ai/v1` accepts OpenAI-style `response_format: json_schema` and multiple `image_url` data URLs exactly as CCTV sends them. Test that early.
- The Globot repo has `.claude/` and `AGENTS.md` folders but was not read in depth, so its vision-analysis code (`visual_risk_routes.py`) is unreviewed — [repo tree](https://github.com/Vector897/Globot).
- The Hugging Face dataset licenses for possible DemoScribe evaluation inputs were not checked.

---

## Q6. What made these projects win: evaluation, depth signals and demo video structure?

### Takeaway
- **Meta's 24-hour hackathons** rewarded working, zero-fine-tune multimodal demos with almost no evaluation. CCTV and OpenGlass published no numbers, and their videos were 43–187 s long.
- **Google's multi-week competitions** rewarded the same assistive and physical themes, but the top Kaggle entries carried hard numbers: GEM-4's LIBERO 74%, Gem-Care's WER cut from 32.7% to 19.0%, Gaze Link's 85% keystroke saving.
- **Gemini 3's top two** were multi-agent systems with visible reasoning and human approval gates.
- **Accessibility** placed at the top in every Google event examined.

Video lengths cluster at 43–80 s for Meta's 2024–25 winners and 133–187 s (at a 3-minute cap) for Google's.

### Cited Findings

**Accessibility and physical-assist wins**
- Gemma 3n: places 1–3 were Gemma Vision (blind users), Vite Vere Offline (cognitive disability) and 3VA (cerebral palsy AAC) — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/).
- Gemma 4 Good: 1st was GEM-4 (assistive arm), with DEMENTOR 4th — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/).
- Gemini 3: Netra (visually impaired) was 3rd — [Devpost](https://gemini3.devpost.com/project-gallery).
- Gemini API Developer Competition: Gaze Link (ALS) and Vite Vere were winners — [Google blog](https://blog.google/technology/developers/gemini-api-developer-competition-winners/).
- Meta: OpenGlass (1st) and Gripmind (2nd) were the physical builds — [Meta](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/); [Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/).

**Hard numbers in the longer competitions**
- GEM-4 published per-suite LIBERO success rates with reproducible eval configs and Hugging Face checkpoints — [GEM-4-VLA README](https://github.com/takaki-maeda-99/GEM-4-VLA).
- Gem-Care reported WER falling from 32.7% to 19.0% — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/).
- PreVillage reported 7.5 tok/s on a Raspberry Pi 5 — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/).
- Gaze Link claimed an 85% keystroke saving across 30 testers — [ai.google.dev (snippet)](https://ai.google.dev/competition/projects/gaze-link).

**No evaluation in the 24-hour Meta winners**
- CCTV's README has a UI walkthrough but no metrics — [README](https://github.com/torayeff/llamacon-hackathon-2025-sf).
- OpenGlass's demo was a fruit-bowl identification — [Meta](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/).

**Multi-agent systems with humans in the loop (Gemini 3's top two)**
- Globot: 5 CrewAI agents, an adversarial-debate red team, "Every decision shows a transparent Chain-of-Thought," and human approval for critical decisions — [Devpost](https://devpost.com/software/globot-341w9q).
- Aegis: 5 agents, a reasoning trace with a typewriter effect, Search-grounded verification, and the "Protocol Zero" human approval gate — [Devpost](https://devpost.com/software/aegis-autonomous-multi-agent-crisis-command).

**Depth signals found in code**
- Netra: backpressure (latest frame wins), a speech-priority arbiter, a tracker that requires stable detections, and reconnect backoff — [websocket.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/routes/websocket.py); [speech.py](https://github.com/ZentraHost/netra_project/blob/HEAD/app/services/speech.py).
- CCTV: queues and threads, JSON schema output, and stream reconnect — [video_event_detector.py](https://github.com/torayeff/llamacon-hackathon-2025-sf/blob/HEAD/backend/video_event_detector.py).
- Gemma Vision: time-to-first-token and decode-speed instrumentation, plus TalkBack-aware TTS — [gemma_service.dart](https://github.com/TGTech06/gemma-vision/blob/HEAD/lib/chat_page/services/gemma_service.dart).
- MimicAnno: schema validation, retry instructions per failure type, and front-end tests — [MimicAnno](https://github.com/takaki-maeda-99/MimicAnno).
- Geo-ML: a DSL with an AST parser and a validator — [geo-lm](https://github.com/williamjsdavis/geo-lm).

**Demo video lengths** (YouTube metadata)

| Project | Event and place | Length |
|---|---|---|
| OpenGlass | Meta, 1st | 43 s |
| CCTV Operator | Meta, 3rd | 55 s |
| OrgLens | Meta, 1st | 78 s |
| Gaze Link | Gemini API competition | 133 s |
| Globot | Gemini 3, Grand Prize | 146 s |
| Compliance Wizards | Meta, 2nd | 166 s |
| Aegis | Gemini 3, 2nd | 167 s |
| GEM-4 | Gemma 4 Good, 1st | 178 s |
| Netra | Gemini 3, 3rd | 179 s |
| Jayu | Gemini API competition, Best Overall | 180 s |
| Vite Vere | Gemini API competition | 180 s |
| Geo-ML | Meta, Best API | 187 s |

Sources: [OpenGlass](https://youtu.be/DsM_-c2e1ew), [CCTV](https://youtu.be/4YaZe4Gbt1g), [OrgLens](https://www.youtube.com/watch?v=8OmMnODOyLw), [Gaze Link](https://youtu.be/y_U1vkEC9PA), [Globot](https://youtu.be/FM2LGhqMnC8), [Compliance Wizards](https://youtu.be/JgZQ6XJXBhE), [Aegis](https://youtu.be/UCYckQYVM2Q), [GEM-4](https://www.youtube.com/watch?v=OhaIA3bYwmg), [Netra](https://youtu.be/Ax3SkwHOkkk), [Jayu](https://www.youtube.com/watch?v=shnW3VerkiM), [Vite Vere](https://youtu.be/yul0L5YWBp0), [Geo-ML](https://youtu.be/U1fDn1C3DJA).

**What the descriptions reveal about video structure**
- Geo-ML's title says the demo starts at 2:07, so about two-thirds of a 3:07 video is setup — [YouTube](https://youtu.be/U1fDn1C3DJA).
- GEM-4's description lists hardware, then tasks, then architecture, then the data-engine workflow — [YouTube](https://www.youtube.com/watch?v=OhaIA3bYwmg).
- Jayu's description: the creator "had to cut over 10 minutes of Demo footage," and a terminal was kept visible "solely for demonstration purposes" to make the background agent legible — [YouTube](https://www.youtube.com/watch?v=shnW3VerkiM).
- Globot's video opens on a narrative hook: "On a Friday at 4:55 PM, the Red Sea crisis erupts…" — [YouTube](https://youtu.be/FM2LGhqMnC8).

**Builder-user relationship stated by winners**
- Gemma Vision was built with input from the developer's blind brother — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/).
- Geo-ML's builder is a geologist — [Meta](https://ai.meta.com/blog/llamacon-hackathon/).
- CCTV's builder maintains FANUC and manufacturing RL tools — [github.com/torayeff](https://github.com/torayeff?tab=repositories).

### Inferences
- **For our 31-hour, Meta-judged build,** the Meta 24-hour precedent says a short, legible live demo of one capability (43–80 s winners) beats breadth. Adding one measured number, which 24-hour Meta winners lacked, is a cheap way to stand out on Technical Depth (20%).
- **Making the model work visible.** Jayu's always-visible terminal and Aegis's reasoning trace both make the model's work visible on screen. That maps to our call-log panel idea, and it helps the "Use of Meta AI tooling" score.
- **Winning code is not polished code.** The OpenGlass prompt bug, Netra's lack of evaluation and its x/20 pan quirk all show that winners are judged on the demo. Ship the golden path first.
- **The accessibility streak** across Google events favors Find-and-Guide on Impact (30%). Netra's 3rd place, however, shows that judges have already seen the concept, so Find-and-Guide needs the SAM 3.1 tracking difference plus a time-to-touch number.

### Gaps
- No video was watched, so shot-by-shot structure and time spent on live demo versus slides are unknown for every project.
- No judge commentary explaining these rankings was found, except Google's one-line praise for GEM-4's "closed-loop data engine" and VLA architecture — [Google blog](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/).
- Gemini 3 Devpost like counts (Globot 80, Netra 22, Aegis 18) are public, but how much they influenced judging is unknown — [Devpost Globot](https://devpost.com/software/globot-341w9q); [Devpost Netra](https://devpost.com/software/netra-empowering-the-visually-impaired); [Devpost Aegis](https://devpost.com/software/aegis-autonomous-multi-agent-crisis-command).
