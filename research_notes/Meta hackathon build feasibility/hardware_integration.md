# Hardware integration for a 1-day Meta hackathon build: phone and webcam first

Confirmed team profile (from the coordinator):
- Track: Indie.
- People: 2, with web/full-stack, dataset-labeling and computer-vision backgrounds. No robot-learning or native-mobile experience is stated.
- Hardware owned: one phone (OS unknown), a laptop (the workspace is Windows 11) and a webcam. No Meta glasses, Quest or robot arm.
- Time left: about 31 hours (18:40 UTC Nov 3 to 02:00 UTC Nov 5). The team is in India.
- Runtime rule: every model called at runtime must be a Meta model.

"Inferred" marks anything not directly stated by a source.

## Q1. Phone as the camera through a web app (getUserMedia, the HTML `capture` attribute): what works, what it takes, and what breaks

### Takeaway
A web-team-friendly phone path needs no app store and no native code, and it covers all three ideas.
- **Still photos (Defect Forge):** use `<input type="file" accept="image/*" capture="environment">`. It hands off to the phone's native camera, so you get full-resolution photos and the phone's own macro mode.
- **Live frames (Find-and-Guide, live DemoScribe capture):** use `getUserMedia({video:{facingMode:"environment"}})` and upload a JPEG every 200–500 ms.
- **The trap:** the page must be HTTPS (localhost works only on the device itself). A phone opening `http://<laptop-LAN-IP>` gets no camera at all. Use a tunnel or a hosted frontend from hour 1.

### Cited Findings
- getUserMedia "is available only in secure contexts (HTTPS)". A secure context means HTTPS, `file:///`, or "a page loaded from `localhost`". "In insecure contexts, `navigator.mediaDevices` is `undefined`". — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- Permission: "user permission is always required". The promise may "neither resolve nor reject" if the user ignores the prompt. Iframes need `allow="camera"`, which matters if the UI is embedded. — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- Constraints:
  - Rear camera: `facingMode: { exact: "environment" }`.
  - Resolution and frame rate: `width: { ideal: 1280 }` and `frameRate: { ideal: 10, max: 15 }`.
  - Using `min` constraints can fail with `OverconstrainedError`.
  - To switch cameras reliably, call `stop()` on the current track first.

  — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)
- The `capture` attribute on `<input type="file">` takes `user` or `environment`. It makes the OS "display a user interface allowing the selection from an existing file or the creating of a new one". It works "better on mobile devices; if your device is a desktop computer, you'll likely get a typical file picker". MDN marks it "not Baseline". — [MDN capture attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/capture)

### Inferences
- **Hosting the phone page over HTTPS (inferred; pick one):**
  - Deploy the frontend to a static host such as Vercel and point it at a tunneled backend. This is the most robust option, and it is also the URL judges will open.
  - Run a tunnel (Cloudflare Tunnel or ngrok) to the laptop dev server.
  - Self-signed LAN certs are painful on iOS. Avoid them.
- **Time estimates (inferred, for a web team):**
  - `capture`-attribute photo upload to the backend: 15–30 min.
  - getUserMedia live preview plus canvas-to-JPEG frame upload at 2–5 fps, including tunnel setup: 1–2 h.
  - WebSocket streaming instead of POST: +30–60 min. Only worth it if latency matters, as in Find-and-Guide.
- **Quality:**
  - The native camera through `capture` gives the best stills: autofocus, HDR, macro mode, full sensor resolution.
  - getUserMedia frames are typically 720p–1080p video frames, which is fine for SAM 3.1 and Muse Spark grounding (inferred). Browsers do not expose lens choice (ultrawide or macro) reliably.
- **Failure risks:**
  - Camera permission denied, or a stale denial cached for the origin. Test on a fresh browser profile.
  - The phone sleeps or locks the screen mid-demo. Keep the screen awake, for example with the Screen Wake Lock API (background knowledge, not verified this session) or a phone setting.
  - Venue Wi-Fi or tunnel latency. Keep a mobile hotspot as a fallback.
  - iOS Safari quirks (autoplay of `<video>` needs `playsinline muted`; background knowledge, not verified).

### Gaps
- MDN's compatibility table for the `capture` attribute did not render. iOS Safari and Chrome Android support is from background knowledge only (both open the camera), not verified this session.
- No source collected on typical getUserMedia max resolution on current iPhones or Android phones.

## Q2. Phone as an IP or USB webcam to the laptop, and the team's USB webcam

### Takeaway
To the laptop, a USB webcam or phone-as-webcam is "just a camera". A laptop page on `localhost` can use getUserMedia without HTTPS, and OpenCV can read it with `VideoCapture(index)`.
- **Android phones:** Windows 11's built-in "connected camera" feature, or DroidCam over Wi-Fi or USB, turns the phone into a laptop webcam in about 15–30 minutes.
- **Best use:** a fixed desk rig for the Defect Forge "inspect a real part live" moment, and for screen-recorded demos where the laptop UI and the camera feed sit in one window.

### Cited Findings
- Windows 11 can use an Android phone as a webcam. Requirements: Android 9+, the Link to Windows app at version 1.24012 or later, and signing in with the same Microsoft account. Setup is under Settings > Bluetooth & devices > Mobile devices, then "Use a connected camera". Sources disagree on the minimum Windows build (Insider, Moment 5, or 24H2). One unverified 2026 guide claims iPhone support. — [Microsoft Support](https://support.microsoft.com/da-DK/Windows/apps/phonelink/use-your-mobile-device-s-camera); [Android Authority](https://www.androidauthority.com/android-phone-webcam-phone-link-3421537/); [Pureinfotech](https://pureinfotech.com/use-phone-camera-as-webcam-windows-11/)
- DroidCam: the app is for "Android & iOS" (Classic is Android only), with Windows and Linux clients. It can "Connect over WiFi or USB cable". "Unlimited free usage at standard definition." It shows up as a "DroidCam Webcam" device to Zoom, Teams and Skype. — [DroidCam (dev47apps)](https://www.dev47apps.com/)
- localhost counts as a secure context for getUserMedia. — [MDN getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)

### Inferences
- **USB webcam (already owned):** 15–30 min to integrate in the browser (`navigator.mediaDevices.enumerateDevices()`, then pick the device by `deviceId`) or in OpenCV (inferred).
  - It is the most reliable live source because it has no network hop.
  - Weaknesses: fixed focus, small sensor and poor close-up quality. Most 720p/1080p webcams cannot focus closer than about 20–30 cm (inferred, not verified).
  - Fine for "part on a desk, viewed from above", not for millimetre-scale defects.
- **Phone-as-webcam (Windows connected camera or DroidCam):** better optics than a webcam, but it adds a pairing step and Wi-Fi dependence. Free DroidCam is limited to standard definition (per the vendor page). Use USB mode to cut lag (inferred).
- **Failure risks:**
  - Windows build mismatch for the connected-camera feature.
  - Microsoft account sign-in friction.
  - DroidCam driver install on Windows.
  - The camera index changes between reboots in OpenCV. Select the device by name or ID in the browser.
- A phone IP camera app that exposes an MJPEG URL is another option for an OpenCV backend. No source was collected on specific apps.

### Gaps
- Not verified: the exact Windows 11 build the team needs, and whether the connected-camera feature appears to browsers as a normal webcam (most coverage implies it does, but nothing confirms it directly).
- DroidCam paid-tier resolution and pricing not collected.

## Q3. Clip-on macro lens and close-up capture for Defect Forge

### Takeaway
For Defect Forge's live moment ("photograph a real bolt, forge defects, inspect"), image quality comes mostly from close focus and diffuse light, not from the camera brand.
1. Try the phone's built-in macro or ultrawide-macro mode through the native camera (`capture` attribute).
2. If that is not enough, a cheap clip-on macro lens is a zero-integration upgrade.

No verified Indian rupee price was found.

### Cited Findings
- A blogger in India bought a "Skyvik Signi Macro 20x Mobile Phone Lens" from Amazon India (no price given). — [naina.co](https://naina.co/2019/06/the-macro-lens-im-using-on-my-pixel-3-xl-smartphone)
- For scale only (US): a 0.45x wide-angle plus macro clip-on was $7.49 at Walmart. Apexel sells 10x–20x clip-on macro lenses. — [Walmart](https://www.walmart.com/ip/18133261087); [YPC Apexel 10x-20x](https://www.ypc.co.uk/product/apexel-10x-20x-hd-zoom-macro-lens-with-universal-phone-clip-smartphone-macro-lens-mobile-phone-lens-fits-all-mobile-phones/)

### Inferences
- **Integration time:** 0 code. Plan 15–30 min of tuning: fixed working distance, a desk lamp with a diffuser such as tracing paper, and a matte grey or black background (inferred).
- **Risks:**
  - Clip-on lenses have very shallow depth of field and soft edges, and need a fixed distance.
  - They can block the phone's other lenses, or the phone switches lenses on its own. Lock to the main camera.
  - Glare on metal parts.
  - Very close macro shots may not resemble the training or eval images, which hurts the measured recall (inferred).
- **For the eval set:** shoot the 40 held-out real images with the same rig and distance as the live demo, so live and eval conditions match (inferred).
- **Buying in hours:** clip-on lenses are common low-cost accessories in India. Quick-commerce apps or Amazon same-day delivery in metros are plausible, but no listing or price was verified. Treat this as optional (inferred).

### Gaps
- No Amazon.in or Flipkart rupee price or delivery time for clip-on macro lenses was found.

## Q4. Chest mounts and phone sensors (DeviceOrientation, vibration) for Find-and-Guide

### Takeaway
A ₹300–500 chest strap turns the phone into a body-worn camera, so the image's horizontal axis equals the user's body heading. SAM 3.1's mask centroid offset alone then gives "turn left or right" with no sensor fusion.
- **Haptics:** `navigator.vibrate` works on Chrome for Android but not on any iOS Safari version. On an iPhone, the cues must be audio (WebAudio stereo panning or beep rate).
- **DeviceOrientation:** supported on iOS 17+ and Chrome Android. It needs a button-click permission request and HTTPS.

### Cited Findings
- Vibration API: "not supported" in every iOS Safari version listed (3.2 through 27.x). Supported in current Chrome for Android. — [caniuse: Vibration](https://caniuse.com/vibration)
- DeviceOrientation events: iOS Safari has supported them since 17.0 (partial support 4.2–16.7). They are supported in current Chrome for Android. — [caniuse: deviceorientation](https://caniuse.com/deviceorientation)
- `DeviceOrientationEvent.requestPermission()` "requires transient activation, meaning that it must be triggered by a UI event such as a button click". It is "available only in secure contexts (HTTPS)" and "not Baseline". Passing `true` requests magnetometer access for `deviceorientationabsolute`. — [MDN requestPermission](https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/requestPermission_static). MDN's own page does not name which browsers need the call. That iOS Safari requires it is from MDN's helper summary and general knowledge, so verify on the target phone.
- India chest-mount prices (snapshots):
  - SUBTON chest belt plus J-mount plus 360° phone holder kit: ₹474 (MRP ₹799). — [DealsMagnet](https://www.dealsmagnet.com/deal/subton-mobile-camera-mount-17oMTgoA)
  - GoPro Chesty GCHM30-001 (needs a phone clip adapter): ₹3,249 on Amazon. — [MySmartPrice](https://www.mysmartprice.com/camera/gopro-chesty-gchm30-001-chest-mount-harness-msf216017)
  - FishPod smartphone harness: ₹1,910 plus import charges. — [Ubuy India](https://www.ubuy.co.in/product/87P2GXCL0-fishpod-smartphone-chest-mount-harness)
  - MB Trade phone chest strap on Meesho (price not shown). — [Meesho](https://www.meesho.com/mb-trade-mobile-phone-chest-mount-strap-holder-helmet-mount-for-action-camera-for-po-v-gopro-akaso-all-smartphone-black/p/9kea3a)
  - A "Sounce" universal phone chest strap at ₹299 on Amazon.in appeared in a search summary, but its source page was unclear (low confidence).

### Inferences
- **Guidance loop on a chest-mounted phone (inferred design):**
  1. Every 300–500 ms, upload a frame.
  2. SAM 3.1 tracks the target object from a Muse Spark grounding box.
  3. The backend returns the centroid x-offset and the mask area.
  4. The phone maps the x-offset to WebAudio stereo pan (or beep pitch) and the mask area or proximity to beep rate.
  5. On Android, it also pulses `navigator.vibrate`.

  Build time on top of the frame stream: 2–3 h. Testing with a blindfolded teammate: 1 h.
- **DeviceOrientation:** optional. Use it to smooth the cue between frames, or to keep pointing toward an object that left the frame. Adds +1–2 h and iOS permission friction (inferred).
- **Mount alternatives:** with no purchase, a lanyard plus a phone pouch, or a phone clipped into a shirt pocket with the camera exposed. Each costs 15 min of rig time, with less stable framing (inferred).
- **Failure risks:**
  - Round-trip latency from the tunnel plus SAM plus Spark. Keep the cue logic local and run the model asynchronously.
  - Motion blur from a moving chest. Ask the user to move slowly.
  - Audio through the phone speaker in a noisy room. Use wired or BT earphones.
  - Demoing with a real blind or low-vision user needs consent and rehearsal (inferred).

### Gaps
- Not verified: Amazon.in same-day availability for the user's pincode.
- The ₹299 Sounce listing could not be traced to a source page.

## Q5. Per-idea recommended setup, integration time, failure risk, and Demo/Tooling lift (phone, laptop and webcam only)

### Takeaway
For this team, the right tier is "phone-only, plus the webcam where it helps" for all three ideas. Optional purchases are a chest strap (₹300–500, Find-and-Guide) and a clip-on macro lens (Defect Forge, price unverified). Phone and webcam add **no Tooling points by themselves**; Tooling must come from the Meta models, plus naming Muse Code if used. Live real-world input mainly lifts **Demo**.

### Cited Findings
- Facts in the table come from the Q1–Q4 citations: secure-context rules, `capture` attribute behavior, Vibration and DeviceOrientation support, and phone-as-webcam requirements.

### Inferences (all estimates are our judgment)

| Idea | Recommended rig | Integration time | Main failure risks | Demo lift | Tooling lift |
|---|---|---|---|---|---|
| #1 Defect Forge | Phone with native camera via a `capture="environment"` upload page for photos of a real part on a desk. Desk lamp plus matte background. USB webcam on the laptop as a fixed live view. Optional clip-on macro lens. | 30–60 min photo upload; 15–30 min webcam; 15–30 min rig and lighting | Glare or small defects not visible; live photo differs from the eval set | +0.5 to +1 (a real part forged live beats canned images) | 0 directly |
| #2 DemoScribe | None needed for the core: public LeRobot or HF episodes. For a live moment, film a 20–30 s tabletop "demonstration" of a hand doing a pick-and-place with the phone (rear camera, tripod or chest mount), upload it, and annotate it on stage. Frame it as human-demo annotation, not robot data. | 30–60 min upload path (reuse the Defect Forge uploader) | Robot-data judges may discount human video; long video processing time on stage, so pre-trim to under 30 s | +0.5 | 0 |
| #3 Find-and-Guide | Android phone (for vibration) on a chest strap running an HTTPS web app with getUserMedia, frames every 300–500 ms, WebAudio stereo-pan beeps plus haptics. iPhone: audio-only cues. | 1–2 h stream; 2–3 h cue loop; 1 h blindfold testing | Latency; motion blur; iOS haptics unavailable; noisy-room audio | +1 to +1.5 (a blindfolded or real user touching the object live is the strongest moment of the three) | 0 directly; loses the "Meta glasses toolkit" angle in the original plan |

- **Rule for all three:** build the backend against a "frame source" abstraction (file upload, phone stream, webcam). Hardware problems then cost a demo moment, not the submission. Keep `DEMO_MODE` cached replays as a fallback (inferred).
- **Tooling compensation:** without Meta hardware, Find-and-Guide's tooling story rests on SAM 3.1 video tracking, Muse Spark grounding and Muse Voice Transcribe for "find my keys". If Muse Code is used to build, say so in the "Use of Meta products" field (inferred).

### Gaps
- Not known: the team's phone OS. That decides haptics (Android only) and the Windows phone-as-webcam path (Android 9+).

## Q6. Not recommended unless obtainable today in India: Meta glasses (DAT), Quest 3/3S, robot arms, ESP32 or OpenGlass

### Takeaway
None of these is worth buying for this deadline given the team's web/CV skills.
- **Meta glasses:** the only one with real upside (Tooling and Demo for Find-and-Guide). It needs a native Android (Kotlin) or iOS (Swift) app, roughly 6–10 h for a team new to native mobile, plus same-day delivery of a ₹22k–46k device.
- **Quest, SO-101 and ESP32:** no.

### Cited Findings
**Meta glasses and the Wearables Device Access Toolkit (DAT) 1.0**
- *Cost and time, one line (inferred):* about ₹22k (Gen 1) to ₹32k–46k (Gen 2) on Amazon.in, plus 6–10 h integration for this team. Consider it only if same-day delivery is confirmed and Find-and-Guide is chosen.
- Supported glasses: Ray-Ban Meta Gen 1 and Gen 2, Ray-Ban Meta Optics, Meta glasses, Meta Ray-Ban Display, Oakley Meta HSTN, Oakley Meta Vanguard. Platforms: iOS 17.2+ and Android 10+. Developer mode is enabled by tapping the version number in the Meta AI app 5 times. — [DAT docs](https://wearables.developer.meta.com/docs/develop/)
- SDK 1.0.1 requires firmware V128 and Meta AI app V292. Some capabilities are "gated server-side per user". — [Version dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/)
- The SDK is native only: Maven Central on Android with no token needed, plus an iOS repo. Samples are CameraAccess, DisplayAccess and BirdSpotter. The sample needs an app ID and client token from the Wearables Developer Center. Muse Code plugin and a no-auth MCP server (`mcp.developer.meta.com/wearables`) are available. — [meta-wearables-dat-android](https://github.com/meta/meta-wearables-dat-android); [CameraAccess sample](https://github.com/meta/meta-wearables-dat-android/tree/main/samples/CameraAccess)
- Stream: max 720p at 30 fps over Bluetooth, degrading to no lower than 15 fps. — [UploadVR](https://www.uploadvr.com/meta-wearables-device-access-toolkit-public-preview/). Frames can go to your own backend: "developers can process data locally or via cloud/edge platforms". Full capabilities are limited to "AI glasses supported countries"; India is not named. — [DAT FAQ](https://developers.meta.com/wearables/faq)
- 1.0 adds experimental Motion (head orientation), Speech (on-device transcription), Inputs and photo capture. MockDeviceKit can feed the phone camera into a fake glasses session. — [Android CHANGELOG](https://github.com/meta/meta-wearables-dat-android/blob/main/CHANGELOG.md)
- Cross-platform community wrappers exist: Expo/React Native ([circus-kitchens/expo-meta-wearables-dat](https://github.com/circus-kitchens/expo-meta-wearables-dat)) and Flutter ([rodcone/flutter_meta_wearables_dat](https://github.com/rodcone/flutter_meta_wearables_dat)). Their maturity is unknown.
- India pricing:
  - Gen 2 launched in India Dec 4, 2025 at ₹39,900. — [Meta Newsroom](https://about.fb.com/news/2025/12/ray-ban-meta-gen-2-launch-in-india-2x-battery-life-better-video-capture/)
  - Amazon.in snapshots: Gen 2 at ₹31,920 in Oct 2026, and Gen 1 at ₹22,425 in June 2026. — [pricehistory.app](https://pricehistory.app/p/ray-ban-meta-gen-2-wayfarer-shiny-aR6jmrG5); [Zoutons](https://zoutons.com/news/ray-ban-meta-glasses-price-amazon-india-october-2026); [TechStoriesIndia](https://techstoriesindia.in/2026/06/meta-ai-smart-glasses-ray-ban-oakley-price-india-amazon/)
  - Also sold on Flipkart. — [t2online](https://t2online.in/tech/tech-news/oakley-meta-vanguard-and-ray-ban-meta-gen-2-now-available-via-amazon--flipkart/2003833)

**Quest 3/3S Passthrough Camera API**
- *Cost and time, one line (inferred):* about ₹16k (unverified) plus 10+ h for a team without Unity experience. Not recommended.
- Needs Horizon OS v74+, passthrough enabled and a camera permission. It does not run in the XR Simulator. Specs: 20–40 ms capture latency, max 1280x1280, accessed through Unity `WebCamTexture`. — [Unity PCA overview](https://developers.meta.com/horizon/documentation/unity/unity-pca-overview/)
- Smartprix lists Quest 3S at ₹15,999 (undated, unverified). — [Smartprix](https://www.smartprix.com/vr_headsets/meta-brand)

**LeRobot SO-100/SO-101 (Koch not researched)**
- *Cost and time, one line (inferred):* ₹28k–69k, often sold out or imported (days), plus 3–4 h assembly and teleop setup with no robot-learning background. Not recommended.
- SO-101 base about $100 in the US. — [TechCrunch](https://techcrunch.com/2025/04/28/hugging-face-releases-a-3d-printed-robotic-arm-starting-at-100)
- India listings: ThinkRobotics ₹27,999.99 (sold out). Seeed SO-ARM101 Pro kit ₹42,422 on Ubuy, without printed parts. — [ThinkRobotics](https://thinkrobotics.com/products/so-arm101-hugging-face-lerobot); [Ubuy India](https://www.ubuy.co.in/product/U0PNQWHNU-so-arm101-low-cost-ai-arm-3d-printed-skeleton)
- Assembly: about 3.5 h for a leader-plus-follower pair. — [Classmethod](https://dev.classmethod.jp/en/articles/lerobot-so-arm101-assembly-teleop/). First data collection: about 3–4 h. — [roboticscenter.ai setup](https://roboticscenter.ai/hardware/so-101/setup)

**ESP32 / XIAO ESP32S3 Sense (OpenGlass-style) and Raspberry Pi camera**
- *Cost and time, one line (inferred):* ₹1,242 at Robu.in (Pune, likely next-day), plus 5–8 h for a first-time ESP32 team, with poor image quality. It earns no Meta Tooling credit and competes with Meta's own glasses. Not recommended.
- Robu.in lists the XIAO ESP32S3 Sense at ₹1,242 incl. GST, in stock (undated). — [Robu.in (cached)](https://st.robu.in/?p=1587654)
- Raspberry Pi camera: not researched. It offers no advantage over the phone (inferred).

### Inferences
- The only purchase that could change the outcome is Meta glasses, and only for Find-and-Guide. Even then, the team's web background makes the native DAT app the riskiest item on the critical path. Defer it until the phone version works end to end (inferred).

### Gaps
- Not verified for any of these items: live Amazon.in stock or same-day delivery for the user's pincode.
- No published DAT stream latency figure.
- No hackathon participant report of DAT setup time.

## Q7. Does Meta hardware or SDK use count toward "Use of Meta AI Tooling", and what hardware demos won before (and how were they filmed)?

### Takeaway
Under the rubric as relayed ("Meta products count"), Meta glasses plus DAT would plausibly count toward Tooling, but this team won't have them. Phone, webcam and third-party hardware earn no Tooling credit (inferred). Meta's past hardware placings were OpenGlass (1st, Llama 3 hackathon, SF, May 2024) and Gripmind (2nd, Llama Impact Hackathon, London, Nov 2024). These were separate events. No source on how they filmed their demos was found.

### Cited Findings
- OpenGlass: first place at the Llama 3 hackathon, "$20 USD" smart glasses that answer questions about what the wearer sees. — [Meta AI blog](https://ai.meta.com/blog/llama-3-hackathon-recap-cerebral-valley/); [Hackster.io](https://www.hackster.io/news/hacking-on-llama3-9af53ff8c520)
- Gripmind: second place at Meta's Llama Impact Hackathon London (Nov 2024), "robotics in assisted living". Meta's summary does not say it was an arm. — [Meta Newsroom](https://about.fb.com/news/2024/11/metas-llama-impact-hackathon-pioneering-ai-solutions-for-public-good/)
- DAT 1.0 ships Muse Code support and a Wearables MCP server, which are Meta developer products. — [meta-wearables-dat-android README](https://github.com/meta/meta-wearables-dat-android)

### Inferences
- **Filming practice for a phone-and-webcam demo (inferred):** use three feeds.
  1. A phone screen recording: the app UI with live cues.
  2. A second phone on a tripod in third person, showing the user and the object, or the part on the desk.
  3. A laptop screen capture of the call-log panel with Meta model IDs and latency.

  Edit them picture-in-picture with a visible clock so it reads as live. Take multiple takes. For Find-and-Guide, overlay the time-to-touch number against the describe-only baseline.
- The "hardware wins" pattern suggests judges reward physical, real-world interaction. A blindfolded user guided to real keys, or a real bolt photographed and inspected on camera, gets much of that effect without buying hardware (inferred).

### Gaps
- No official hackathon text found on whether hardware or SDK use (as opposed to model calls) is scored under Tooling. Confirm on the hackathon FAQ or Discord.
- No primary source on how past hardware winners filmed their demos.
