# Meta Global AI Developer Hackathon (Meta + Cerebral Valley, Oct 26 – Nov 4, 2026): Rules, Judging, Submission Requirements and Competitive Intel

Research date: Nov 3, 2026. The Official Rules are public on the Cerebral Valley "waiver" page, which only renders in a real browser; I read it there. The participant "details" page, the submit form and Discord all require a Cerebral Valley login, which I did not use. Details from those come from participants' verbatim copies on GitHub (kickoff-slide screenshots, organizer Discord answers) and are labeled as such. The user can sign in to confirm them.

## Q1. What do the Official Rules say? (eligibility, team size, IP, required Meta model use, prohibited content, pre-existing code)

### Takeaway
The Official Rules are binding and public. They set up two tracks with one track per project. The Indie track allows teams of up to 4; the Startup track is for technical founders and its Representative must be a startup employee. The entrant keeps IP but gives Meta and Cerebral Valley a broad perpetual license. Using Meta models is mandatory, and organizers clarified on Discord that **every model the project calls at runtime must be a Meta model**. Outside AI coding tools are fine. Pre-existing code is not banned outright, but only work built during the event is scored, and the kickoff warned against a list of "overdone" project types.

### Cited Findings
**Where the rules live**
- The Official Rules are titled "Hackathon Terms & Conditions ('Official Rules') and Event Waiver", dated Oct 25, 2026. They sit at the waiver URL, which is JS-rendered (WebFetch only sees "Loading..."). — [CV Official Rules / Waiver](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- The public event pages still say "Official Rules will be published before the Hackathon begins on October 26, 2026", which is now stale. — [dev.meta.ai event page](https://dev.meta.ai/events/global-hackathon); [CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon)

**Eligibility**
- Entrants must be 18+ and of the age of majority where they live.
- Not eligible:
  - anyone targeted by US/EU/UN/UK sanctions or export controls, or acting for someone who is
  - anyone organized or located in Belarus, China, Russia, Ukraine or Syria
  - anyone in Crimea, Donetsk, Luhansk, Cuba, North Korea or Iran
  - employees, contractors and interns of Meta and Cerebral Valley, government-affiliated individuals, their immediate families and their household members
  
  — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Participation is capped at 20,000 accepted applicants and is virtual only. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)

**Tracks and team size**
- "A participant may apply for one (1) track only, and a project submission may be entered in one (1) track only."
- Each team appoints one "Representative" who enters the submission and warrants that every member has read the rules.

  — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- **Indie Developer track:** "Open to individual builders and students, teams of up to four (4)". The Representative must name all other team members in the submission. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- **Startup track:** "Open to technical founders building a product." The startup Representative "must be an active employee of the startup" and is authorized to receive prize payment. No team-size cap is stated for this track. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Track judging lenses (event page): Indie is judged on "creativity, technical ambition, and whether it works". Startup is judged on "technical execution and whether it holds up in production". — [dev.meta.ai](https://dev.meta.ai/events/global-hackathon)

**IP ownership and licensing**
- "the entrant retains ownership of all intellectual and industrial property rights (including moral rights) in and to the Submission."
- The entrant grants Organizers "a perpetual, irrevocable, worldwide, royalty-free, and non-exclusive license" to use, modify, publish and otherwise exploit the Submission "for any purpose without restriction", including marketing.

  — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Nothing shared is confidential. Organizers "can[not] agree to obligations of confidentiality", and all "Materials" get a royalty-free, transferable, sub-licensable, perpetual license. This matters for Startup-track teams showing proprietary code. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- The Submission must be: (a) original work; (b) solely owned by the participant, team or organization; and (c) non-infringing. "Participants may contract with a third party for technical assistance" if they keep ownership. Open source is allowed "provided applicable open source licenses are followed and the Submission enhances or builds upon the underlying open source product." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Winners' name, likeness and statements may be used in publicity in perpetuity without compensation. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)

**Required use of Meta models**
- Official Rules: "Participants build with Meta AI products, including Muse Spark, Glimmer, SAM 3, and any other Meta AI products identified on the Event page." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Judging Stage 1 is a pass/fail check: "Does the project reasonably fit a theme and use Meta AI products?" — [Kickoff livestream slide "Judging process", screenshot in participant repo](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)
- Organizer answer on Discord #questions, Oct 31, recorded verbatim by a participant: "Yes, you can build with other AI coding tools such as OpenCode, Claude or Codex, and you don't need to use Muse Code or disclose them. **Every model your project calls at runtime must be a Meta model**, and this won't affect your eligibility as long as that holds." — [lleoparden/naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Organizer answer, Oct 28: Muse Image is an allowed model, so assets generated with it may be used in the video and repo. No on-screen credit is needed; describe the use in the "use of Meta products" field. — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Model menu on the event pages:
  - Meta Model API: Muse Spark series, Muse Wonder, Muse Image, SAM 3.1
  - Meta open-weights models
  - Muse Code
  
  The dev.meta.ai page also lists Muse Glimmer, Muse Spark Open and Muse Voice Transcribe model pages. — [CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon); [dev.meta.ai](https://dev.meta.ai/events/global-hackathon)
- A participant guide summary lists the allowed models as Meta Model API (Muse Spark series, Muse Wonder, Muse Image, Muse Voice Transcribe, SAM 3.1), open weights (Muse Glimmer, Muse Spark Open) and Muse Code. — [meta-ai-hackathon/meta-hack "event guide"](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md)

**Pre-existing code**
- The Official Rules do not explicitly ban prior code. They require original, solely-owned work and allow open-source building blocks. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Kickoff slide, demo-video requirement: "Show only what your team built during the event; judges score from it." — [Kickoff slide "Submissions", screenshot](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)
- One participant's kickoff notes: "The code must be open source, and the submission must say where the new work starts." That participant flagged it as unverified against a recording. — [lovinta/asih submission checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)
- Another participant guide says "New work only" and that unclear contribution means disqualification. It cites no source. — [meta-hack README / event guide](https://github.com/meta-ai-hackathon/meta-hack)
- Some entrants openly build on prior work and claim only the new layer. Pocket Muse, for example, says its hardware and firmware predate the event. — [SaintSinC/pocket-muse](https://github.com/SaintSinC/pocket-muse) (via search summary)

**Prohibited / discouraged content**
- Kickoff slide "Rules: Anti-projects – Skip these overdone projects":
  - AI-generated medical advice
  - Simple image analyzers
  - Dashboards as the main feature
  - AI job application screeners
  - Personality analyzers
  - Basic RAG apps
  - Streamlit apps
  - "AI for Education" chatbots
  - AI nutrition coaches
  - Sports analyzers or coaches
  
  Footnote: "Not a complete list. Medical advice includes tools like AI mental health advisors and skin blemish detectors." — [Kickoff slide screenshot](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)
- One participant's copy of the list adds "anything political or involving war". This does not appear on the kickoff slide; it may come from the signed-in details page or problem statements, but that is unverified. — [meta-hack restrictions.md](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/restrictions.md)
- The Code of Conduct allows disqualification for disruptive, abusive or harassing behavior. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)

**Credits**
- $150 in Meta Model API credits per participant, "valid for a 10-day development window". — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Per the host email quoted by a participant: claim by Nov 4, 9:00 PM ET; a credit card must be on the account to make calls; each participant claims individually. — [lovinta/asih checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)
- Partner credit amounts conflict:
  - The public CV page says Fireworks gives $100. — [CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon)
  - The signed-in details page text, as copied Oct 26, says Fireworks gives "$25 in credits". — [details-page-full.md copy](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/details-page-full.md)
  - A participant summary says Baseten's $100 + 2M TPM goes to the first 2,000 participants and Modal's $100 to the first 1,000, requested via Discord #resources. — [rules-summary.md](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/rules-summary.md)

### Inferences
- **Runtime purity is a real disqualification risk.** Any non-Meta model at runtime could fail Stage 1: ElevenLabs/OpenAI TTS, Whisper, Claude/GPT calls, non-Meta embedding models. At least one visible entry (meta-hack, which uses ElevenLabs for spoken replies) appears to violate this. Use Muse Voice Transcribe for speech-to-text. Inferred from the organizer's answer, not checked: the TTS gap would need a Meta option or browser-native speech, and a browser speech API is not a "model call" in the usual sense but is still a gray area.
- With 1–1.5 days left, reusing a prior codebase is legally allowed. The video and write-up should still clearly separate what was new this week, because judges "score from" what was built during the event.
- Startup-track teams should assume anything they submit can be reused by Meta, under a non-exclusive license.

### Gaps
- The exact text of the "problem statements" on the signed-in details page is not public. Impact scoring includes "whether it fits one of the problem statements". The participant copies paraphrase them as the two themes. The user can sign in to the details page to confirm.
- No official statement on a Startup-track team-size cap, or on whether students can enter the Startup track.

## Q2. What exactly must be submitted? (video, repo, live URL, write-up fields, platform, track selection)

### Takeaway
Submit on the Cerebral Valley portal by **Wed Nov 4, 9:00 PM ET** (= 02:00 UTC Nov 5, since the US is on EST after Nov 1). The four kickoff requirements are:
1. The CV submission, listing every teammate
2. A **3-minute demo video** that shows only work done during the event
3. A **public GitHub repo** that runs from its setup instructions
4. Submission before the deadline

A live URL is optional. The form also asks for track, problem statement, an X post link (for Most Viral), a description, "Use of Meta products", "Why Meta's models matter", and feedback fields. Submissions are editable until the deadline.

### Cited Findings
- Official Rules: "Participants will submit their project to Cerebral Valley's portal at https://cerebralvalley.ai/e/meta-ai-developer-hackathon/hackathon/submit." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Kickoff slide "Submit four things by Nov 4, 9:00 PM ET":
  1. "Submit on the CV platform, with every teammate"
  2. "A 3-minute demo video – Show only what your team built during the event; judges score from it."
  3. "A public GitHub repo – Check that it opens in a logged-out browser before you submit."
  4. "Before the deadline – Wednesday, Nov 4 at 9:00 PM ET. Don't wait for the last hour."
  
  — [Kickoff slide screenshot (submissions.png)](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)
- Submission form fields, as recorded by a participant filling the form:
  - Team name
  - Team member(s)
  - Track
  - Problem statement (theme)
  - "Most Viral Track (X post link)"
  - Project description
  - Public GitHub repo
  - 3-minute demo video
  - Use of Meta products
  - Why Meta's models matter
  - Feedback on Meta products
  - Feedback on partner technologies (optional)
  
  — [lleoparden/naqsh submission-notes.md](https://github.com/lleoparden/naqsh/blob/main/docs/submission-notes.md)
- Organizer answers on Discord #questions (verbatim, via participant):
  - Oct 27: "any accessible link that lets judges watch works (unlisted YouTube is fine)". Submissions "can be edited until the deadline, so the X post link can be added later."
  - Oct 28: "The repo must be public." There are no edits after the deadline.
  
  — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Organizer answer, Oct 31, on the live URL: "A public live URL is not required. Judges need a project that runs from the public repo's setup instructions, plus the 3-minute demo video. A hosted version is optional, so you can deploy it, but judging doesn't depend on it." An earlier answer (Oct 28) said "a hosted URL is better for judges". — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Organizer answer, Oct 31, on the video: "The demo video should show the working product with the **live Meta model calls visible**, and judges can test with their own keys if needed. Recorded sample runs are only a fallback, so if your public deployment runs in demo mode, make sure the repo still runs live from its setup instructions and the README explains how to use the demo mode." — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Track selection: one track per project, chosen in the form. The Indie Representative lists all teammates. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Participants report the 3-minute video as the "main judging artifact". — [meta-hack README](https://github.com/meta-ai-hackathon/meta-hack)
- Example participant plan: ≤3:00, English, AI narration, burned-in captions, scenes mapped to rubric criteria (Impact → Demo → Meta AI → Depth). — [manueljpconde issue #36](https://github.com/manueljpconde/meta-ai-developer-hackathon/issues/36)

### Inferences
- The "Use of Meta products" and "Why Meta's models matter" fields map directly onto the 25% "Use of Meta AI Tooling" criterion. Strong entries (e.g., Naqsh) fill them with per-model roles plus *measured* numbers: latency, cost per run, recall, failure rates. The "Feedback on Meta products" field is a cheap place to show API depth, such as documenting quirks.
- The X post link must exist in the form by 9 PM ET Nov 4, though engagement keeps counting through Nov 8. So the X post should go out *before* submitting.
- Leave 3+ hours before 9 PM ET for submission. Participants plan "mid-afternoon ET" buffers, and portal load near a 20,000-person deadline is a plausible risk. — [nmheinrich/seeyable issue #25](https://github.com/nmheinrich/seeyable/issues/25) (participant plan, not official)

### Gaps
- Description length and character limits for the form fields are unknown, since the form is visible only when signed in.
- Whether the 3-minute limit is a hard cap (auto-reject) or a guideline is not stated.

## Q3. Judging rubric, rounds, finalist selection, judges, prize breakdown, bonus prizes

### Takeaway
There is one weighted rubric for both tracks:
- **Impact 30%**
- **Use of Meta AI Tooling 25%**
- **Demo 25%**
- **Technical Depth & Execution 20%**

Scoring runs in three stages: pass/fail, then 0–10 rubric scoring, then a live final of the **top 5 per track** on Nov 9, ranked by judges. Prizes:
- Indie: $400K total, paid as $150K / $100K / $75K / $50K / $25K
- Startup: $550K total, paid as $250K / $150K / $75K / $50K / $25K
- Bonus: up to $50K. Participant notes name the categories as Most Viral (X engagement), Best Build on Open Weight Models, Community Vote, Best Agentic Use-Case and Best Creative Build (Muse Image/Wonder).

No judges are named publicly.

### Cited Findings
- Official rubric, verbatim excerpts:
  - "**Impact (30%)** — the real-world potential of the Project, who benefits, how much it matters, whether it could become something people use, and whether it fits one of the problem statements"
  - "**Use of Meta AI Tooling (25%)** — how creatively the team used Meta's AI tooling, whether they went beyond a basic integration, and whether they surfaced unexpected capabilities"
  - "**Technical Depth & Execution (20%)** — whether the engineering is sound and thoughtfully refined and the Project demonstrates real craft"
  - "**Demo (25%)** — whether the Project has a working, impressive demo, whether the product holds up live, and the quality of the demo video."
  
  — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Kickoff slide "Three stages from submission to winners":
  - Stage 1, Pass/fail: "Does the project reasonably fit a theme and use Meta AI products?"
  - Stage 2, Rubric scoring: "Judges score every passing project from 0 to 10 on the rubric."
  - Stage 3, Live final round: "Top 5 per track. Judges watch the demos live on Nov 9 and rank them."
  
  — [Kickoff slide screenshot (judging-process.png)](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)
- "Finalists will be chosen by a panel of Organizers selected judges ('Judges'). The judges' selections are final and binding." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Prize tables, verbatim: "Indie Developer Track, total $400,000: 1st $150,000; 2nd $100,000; 3rd $75,000; 4th $50,000; 5th $25,000. Startup Track, total $550,000: 1st $250,000; 2nd $150,000; 3rd $75,000; 4th $50,000; 5th $25,000." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver); corroborated by [madrobot.blog](https://madrobot.blog/2026/10/03/meta-global-ai-developer-hackathon-1-million-prizes-muse-model-api/)
- Bonus prizes in the Official Rules: "up to $50,000 in the aggregate … may include, without limitation, a community vote award, most viral project award, or other unique or notable project categories". Bonus prizes are "announced on or about November 10, 2026", and "Additional prizes do not reduce the track prizes." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- Bonus categories and amounts per a participant guide; amounts not verified in official text:
  - Most Viral Project: $20K, "highest X engagement on the demo post through Nov 8"
  - Best Build on Open Weight Models: $10K
  - Community Vote: $10K
  - Best Agentic Use-Case: $5K
  - Best Creative Build: $5K, "most original use of Muse Image or Muse Wonder"
  
  — [meta-hack grading criteria.md](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/grading%20criteria.md)
- A second participant's kickoff notes independently list the same five category names: "Most Viral, Best build on Meta open weights, Community Vote, Best Agentic Use-Case, Best Creative Build". — [lovinta/asih checklist](https://github.com/lovinta/asih/blob/main/docs/SUBMISSION_CHECKLIST.md)
- Organizer answer on bonus mechanics:
  - Most Viral = "highest total likes + reposts + comments on the X post linked in the submission, counted through Nov 8 EOD"; no hashtag is required; build-in-public posts are fine.
  - Community Vote happens "on the public gallery, one vote per verified account, winner announced Nov 16."
  
  — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Judges: not named in the Official Rules, the event pages or any source found. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver); [madrobot.blog](https://madrobot.blog/2026/10/03/meta-global-ai-developer-hackathon-1-million-prizes-muse-model-api/)
- Payout: Cerebral Valley administers prizes via Tremendous bank payouts, in USD. A W-9 or W-8BEN is required. Winners pay taxes and wire/FX fees. Payment arrives within 30 days of verification. Teams can take one payment to the Representative or split it. — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)

### Inferences
- There are 5 paid places per track and 5 finalists per track. So, inferred, **reaching the live final appears to guarantee at least $25K**, and the whole game is getting into each track's top 5 from Stage 2 scores.
- Stage 2 is judged mainly from the video plus the repo, possibly with judges running it using their own keys. The Demo (25%) and Impact (30%) criteria therefore have to land in the first ~30 seconds of the video.
- "Surfaced unexpected capabilities" rewards showing a model doing something non-obvious, such as SAM 3.1 video tracking feeding a measurement, or Muse Spark verifying its own output visually. A single chat call does not qualify.
- Bonus stacking: an Indie project that uses open-weights models (Glimmer/Spark Open via Baseten/Modal/Fireworks), is agentic, and uses Muse Image/Wonder creatively could be eligible for 3 bonus categories at once. Few visible competitors use Muse Wonder or Muse Image (see Q5). The Most Viral prize ($20K, if that amount is correct) is the largest bonus and depends purely on X engagement through Nov 8.
- The Startup track lens ("holds up in production") rewards reliability evidence: tests, eval numbers, cost/latency receipts, rollback/guardrails. The Indie lens rewards creativity and ambition.

### Gaps
- No public names for judges or finals hosts.
- The bonus prize dollar split comes only from one participant's notes. The official text says only "up to $50,000 in the aggregate".
- Date conflict: the Official Rules say bonus prizes are announced "on or about November 10", but an organizer said the Community Vote winner will be announced Nov 16. The time of the Nov 9 ceremony was not found; one participant guide says 12 PM ET. — [meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md)
- Unknown whether finalists must be available live on Nov 9, or whether a no-show forfeits.

## Q4. What have workshops, the kickoff livestream, and Meta/CV social posts said about what judges want?

### Takeaway
The official signals all point toward:
- **multimodal, agentic and verifiable** systems
- builds that go "beyond a basic integration"
- physical-world use cases (Push the Frontier)
- open-weights usage through the partners

The kickoff explicitly penalizes thin wrappers: simple image analyzers, basic RAG, Streamlit, dashboards-as-product. It also penalizes medical, education, nutrition, sports and HR-screening apps.

### Cited Findings
- Workshop schedule per a participant guide:
  - Tue Oct 27: "Agents 101, building a multimodal agent" (Suraj Subramanian)
  - Wed Oct 28: "Agents 102, verifiable agent best practices" (Yash Khare)
  - Fri Oct 30: "Specialized intelligence on Fireworks" (Sinan Ozdemir)
  - Weekday text office hours, 10–11 AM ET, in Discord #office-hours
  
  — [meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md). The Fireworks workshop by Sinan Ozdemir is also confirmed on the public page. — [CV event page](https://cerebralvalley.ai/e/meta-ai-developer-hackathon)
- An official Meta workshop repo was created Oct 27: "Legal Agent Workshop – Code for building an AI legal agent using Muse Code and Muse Spark". Its Session 2 is "Make it trustworthy". It builds "a verification layer" that "the kit runs outside the agent's control", with refusals, escalation, evidence release, resume and attorney sign-off. — [meta-models/legal-agent-workshop](https://github.com/meta-models/legal-agent-workshop)
- Other official Meta repos useful for building:
  - meta-sam: SAM 3.1 streaming segmentation clients for TS and Python
  - muse-code-sdk
  - meta-model-cookbook: "agentic workflows, multi-agent orchestration patterns … with cost comparisons"
  - meta-oss-cookbook
  
  — [github.com/meta-models](https://github.com/meta-models)
- Theme text, signed-in details page: Build for Your World means "Solve a problem you know firsthand, free up time and mental space, and make something possible that wasn't before." Push the Frontier means "Give a machine a new capability, accelerate a scientific experiment, or unlock a better way to understand and control a physical system. Show us what becomes possible when these models meet the real world." — [details-page-full.md copy](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/details-page-full.md)
- Meta for Developers on X: "Open weights, meet your favorite stack. We're teaming up with @FireworksAI_HQ, @baseten and @modal … so you can run Muse Glimmer and Muse Spark Open on the tools you already build with." — [X post (title via search; page returned HTTP 402)](https://x.com/MetaforDevs/status/2112971571321332179)
- Meta Connect 2026 recap: Muse Spark 1.3 "brings frontier-level reasoning to complex coding and agentic workflows". Muse Glimmer is a 30B open-weights model "designed to run on a single GPU or Mac Mini". Highlighted use cases include AI glasses for hands-free work ("cataloguing inventory", "documenting a repair with both hands on the tool") and on-device agents. — [Meta Connect recap](https://developers.meta.com/blog/meta-connect-recap/)
- Kickoff anti-projects slide (see Q1): wrappers and the medical, education, nutrition, sports, HR and personality categories are "overdone". — [Kickoff slide screenshot](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/tree/main/docs/hackathon/kickoff-slides)

### Inferences
- The "verifiable agent" thread is very likely why so many competitor repos frame themselves around "receipts", "proof" and "evidence", but that framing is now saturated (see Q5). Winning entries likely need verification *inside a compelling domain outcome*, not verification as the product itself.
- The Fireworks "specialized intelligence" workshop and the open-weights partner push suggest Meta wants to see Glimmer or Spark Open fine-tuned or self-hosted. That ties to the open-weights bonus.
- The AI-glasses use cases from Connect (hands-free repair documentation, inventory) are an officially blessed Meta narrative with few competitors (see Q5).

### Gaps
- No recording or transcript of the kickoff livestream was found, only 3 slide screenshots. The kickoff presenter is unnamed.
- Workshop recordings and slides were not found publicly.
- X, LinkedIn and YouTube posts from @AIatMeta, @MetaforDevs and @cerebral_valley could not be read: X returns HTTP 402, and no YouTube kickoff VOD surfaced in search.

## Q5. What are participants publicly building? Which ideas are crowded and which gaps stand out?

### Takeaway
GitHub search (gh CLI) found **329 unique repos created since Oct 20** that mention the hackathon or Muse/SAM 3.1/Meta Model API; 305 have descriptions. This sample is heavily skewed toward:
1. "verification / receipts / proof-of-work" layers for AI agents and coding agents
2. SAM 3.1 + Muse Spark "photo → inspection/hazard report" apps
3. "video → procedure step-checker" apps
4. voice assistants

Underserved areas:
- energy
- manufacturing/materials
- legacy-code modernization
- genuine open-weights fine-tunes
- Muse Wonder and Muse Image creative uses
- Ray-Ban/AI-glasses builds

Many entrants are still building in categories the kickoff called overdone (medical, education, sports).

### Cited Findings
Source for all counts: `gh search repos` across 8 keyword queries and 6 topics (meta-hackathon-2026, meta-ai-hackathon, meta-hackathon, muse-spark, sam-3-1, meta-model-api), filtered to repos created after 2026-10-20, run Nov 3, 2026. Examples are linked. Keyword counts are approximate, since one repo can match several clusters. The [muse-spark GitHub topic](https://github.com/topics/muse-spark) alone lists 153 repos.

- **Model usage across 305 descriptions:**
  - 64 mention SAM 3.1
  - 36 mention voice/transcription
  - 14 mention open weights, Glimmer, Spark Open or fine-tuning
  - only **8 mention Muse Wonder** and **5 mention Muse Image**
- **Crowded #1: agent verification, receipts and guardrails** (~57 descriptions match verify/proof/receipt/evidence/audit; ~22 match guard/injection/safe). Examples:
  - [Master07/attest](https://github.com/Master07/attest) (proof-of-fix for AI PRs)
  - [FrankieBiz/Faultline](https://github.com/FrankieBiz/Faultline)
  - [momoikura/The-Polisher](https://github.com/momoikura/The-Polisher)
  - [Kylne700/torpor-muse](https://github.com/Kylne700/torpor-muse)
  - [ReARCLabs/sparkguard](https://github.com/ReARCLabs/sparkguard)
  - [yatharthchopra2424/witness-agent-receipts](https://github.com/yatharthchopra2424/witness-agent-receipts)
  - [DrVelvetFog/agent-andy](https://github.com/DrVelvetFog/agent-andy) (hash-chained receipts)
  - [Dominic-Pi-Sunyer/munix](https://github.com/Dominic-Pi-Sunyer/munix) (prompt-injection runtime)
  - [Hisernberg/spanguard](https://github.com/Hisernberg/spanguard)
  - [OmChauhan9/dualprivilege-airgap](https://github.com/OmChauhan9/dualprivilege-airgap)
  - [AgentSafeLabs/safelabs-guard](https://github.com/AgentSafeLabs/safelabs-guard)
  - [demonjd2026-afk/spark-gate](https://github.com/demonjd2026-afk/spark-gate)
  - [Anxy/rouvr](https://github.com/Anxy/rouvr)
  - [Ataraxiainc2/ISSAAS](https://github.com/Ataraxiainc2/ISSAAS)
  - [Bhav-ikkk/spectra](https://github.com/Bhav-ikkk/spectra)
  - [ChinmayBitne/GoalFault-AI](https://github.com/ChinmayBitne/GoalFault-AI)
  - [terrizoaguimor/hyphae-consensus](https://github.com/terrizoaguimor/hyphae-consensus)
  - [poferraz/vibe-fence](https://github.com/poferraz/vibe-fence)
- **Crowded #2: photo → inspection/hazard/repair report with SAM 3.1 + Muse Spark** (~16+), including direct duplicates:
  - Older-adult home fall hazards: [KarlaPocasangre/aegis-home](https://github.com/KarlaPocasangre/aegis-home) and [taeefnajib/AgeProof-AI](https://github.com/taeefnajib/AgeProof-AI)
  - Packing/unboxing evidence: [JamS1t/proofbox](https://github.com/JamS1t/proofbox) and [jeejak/proofmuse](https://github.com/jeejak/proofmuse)
  - Warehouse safety: [sagar-das01/AIsleEye](https://github.com/sagar-das01/AIsleEye) and [khpartha/Meta-Hack](https://github.com/khpartha/Meta-Hack)
  - Roads/civic: [Foxcrack/viaguard](https://github.com/Foxcrack/viaguard) (13 stars), [bhuneshwarsunhale-ux/CivicLens-AI](https://github.com/bhuneshwarsunhale-ux/CivicLens-AI), [kevalhirani2003/streetops-ai](https://github.com/kevalhirani2003/streetops-ai)
  - Repair: [mangeshraut712/fieldfix](https://github.com/mangeshraut712/fieldfix), [phil10xs/vergecare-meta](https://github.com/phil10xs/vergecare-meta)
- **Crowded #3: video → learn a physical procedure, then verify steps:**
  - [DravenDou/processlens](https://github.com/DravenDou/processlens)
  - [desilva23/proofstep](https://github.com/desilva23/proofstep)
  - [ryanfer123/Meta-Hackathon](https://github.com/ryanfer123/Meta-Hackathon) ("Apprentice")
  - Teardown → reassembly (duplicates): [PhiBao/backstep](https://github.com/PhiBao/backstep) and [tejaschaudhari131/rewind](https://github.com/tejaschaudhari131/rewind)
  - Phone-video physics labs (duplicates): [Giochvanno/hackathon-meta-galileo](https://github.com/Giochvanno/hackathon-meta-galileo) and [setiani/framelab](https://github.com/setiani/framelab)
- **Robotics / Push the Frontier** (~14), the most technically ambitious visible:
  - [PandaGrdn/athlete2humanoid](https://github.com/PandaGrdn/athlete2humanoid): phone video → Unitree G1 policy via SAM 3.1 + SAM 3D Body + V-JEPA 2
  - [SungHyunC/video2urdf](https://github.com/SungHyunC/video2urdf): video → URDF/MJCF validated in MuJoCo
  - [StefanRohringer/muse-qc-cell](https://github.com/StefanRohringer/muse-qc-cell): real robot arm sorting molded parts
  - [Volgat/foros-meta-hackathon](https://github.com/Volgat/foros-meta-hackathon)
  - [tamzid2001/sceneproof](https://github.com/tamzid2001/sceneproof)
  - [est4ever/DemoDoctor](https://github.com/est4ever/DemoDoctor)
  - [mary-jeon/realcad](https://github.com/mary-jeon/realcad): prompt → CAD verified by OpenCascade
- **Science agents** (~18):
  - [aleksandrahodzzik/musecell](https://github.com/aleksandrahodzzik/musecell): blinded MoA screening on BBBC021
  - [scoobydoobydrew/cellproof](https://github.com/scoobydoobydrew/cellproof)
  - [moayadMoatamed/Orchanium](https://github.com/moayadMoatamed/Orchanium)
  - [Jaycee871/FrontierLab-Meta-Hackathon-2026](https://github.com/Jaycee871/FrontierLab-Meta-Hackathon-2026)
  - [Collistus-Kibe/STEM-Claw](https://github.com/Collistus-Kibe/STEM-Claw)
  - [jerrydjin/malleable](https://github.com/jerrydjin/malleable) (ChemStation)
- **Informal-merchant commerce** (~13):
  - [bhoot-biswas/listsnap](https://github.com/bhoot-biswas/listsnap)
  - [Fatdrfrog/meta-ai-hackathon](https://github.com/Fatdrfrog/meta-ai-hackathon) ("film your shelf → catalog")
  - [libertyfidja-bit/kuracommerce-meta](https://github.com/libertyfidja-bit/kuracommerce-meta)
  - [silambarasan-sh/kadai-khata](https://github.com/silambarasan-sh/kadai-khata)
- **Still in "overdone" categories:**
  - Medical/health (~16): e.g. [Wauguzi/tabibu](https://github.com/Wauguzi/tabibu) pathology pre-reads, [mbyo2/doc0clock-ai-triage](https://github.com/mbyo2/doc0clock-ai-triage), [ashrafulislamse/renalradar](https://github.com/ashrafulislamse/renalradar)
  - Education/tutor (~17): e.g. [Akas333/TYSA](https://github.com/Akas333/TYSA) (20 stars), [nema1502/nemi](https://github.com/nema1502/nemi), [laxmanshah45/chalk-talk](https://github.com/laxmanshah45/chalk-talk)
  - Sports (5): [EmirCobanOfficial/courtsense-site](https://github.com/EmirCobanOfficial/courtsense-site), [SLIPPECAT/tap-me-volleyball](https://github.com/SLIPPECAT/tap-me-volleyball), [newmachinesph/hoopscliniq-demo](https://github.com/newmachinesph/hoopscliniq-demo)
- **Thin areas from manual review of the 305 descriptions:**
  - **Energy (~5):** [EmilJaf/wellpilot](https://github.com/EmilJaf/wellpilot) (oil & gas well analysis on Spark Open), [EcoPrism/whos-on-my-grid](https://github.com/EcoPrism/whos-on-my-grid), [jscott3201/mechanical-muse](https://github.com/jscott3201/mechanical-muse) (building control sequences → tested controller), [dangkhoa241/ClimateGuard](https://github.com/dangkhoa241/ClimateGuard), [xFalzz/verdara](https://github.com/xFalzz/verdara)
  - **Manufacturing/materials (~9):** [WaleedOH/clearline](https://github.com/WaleedOH/clearline) (pharma line clearance), [facunahuel420/CircuitGuard-AI](https://github.com/facunahuel420/CircuitGuard-AI), [nikunjtrehan/remnant-x](https://github.com/nikunjtrehan/remnant-x) (CNC nesting), [TsilavinaZh/RecupBuild](https://github.com/TsilavinaZh/RecupBuild)
  - **Legacy code modernization (4):** [Nivetha200111/Diocle](https://github.com/Nivetha200111/Diocle) (COBOL→Java), [Mrabbi3/f2j](https://github.com/Mrabbi3/f2j) (Fortran→JAX, verified against compiled original), [rockyru/regov](https://github.com/rockyru/regov)
  - **AI glasses/wearables (~5):** [xdleet/beacon-glasses-demo](https://github.com/xdleet/beacon-glasses-demo), [Dongckim/Meta-Global-AI-Developer-Hackathon](https://github.com/Dongckim/Meta-Global-AI-Developer-Hackathon) (lab glasses → robot protocols), [ohistudio/fursight](https://github.com/ohistudio/fursight)
  - **Genuine open-weights fine-tunes (only ~3):** [natanr123/preflight](https://github.com/natanr123/preflight) (QLoRA of Muse Glimmer 30B on Modal), [Hisernberg/spanguard](https://github.com/Hisernberg/spanguard), [MaheswarPraveen/data-refinery](https://github.com/MaheswarPraveen/data-refinery)
  - **Disaster/SAR (~5):** [Heet-P/SAHARA_MetaAI](https://github.com/Heet-P/SAHARA_MetaAI), [h-a-forster/lastseen](https://github.com/h-a-forster/lastseen), [anbestephen/FirstLight](https://github.com/anbestephen/FirstLight)
- **Labeled Startup-track entries are few.** Examples: [GuiderCoLtd/reflow-studio-hackathon](https://github.com/GuiderCoLtd/reflow-studio-hackathon) (Muse Spark 1.3 computer use → guides), [ta-amps/ta-amps-hackathon](https://github.com/ta-amps/ta-amps-hackathon), [dayplayTeam/dayplay-ar-hackathon](https://github.com/dayplayTeam/dayplay-ar-hackathon), [tamzid2001/frontiersight-ai](https://github.com/tamzid2001/frontiersight-ai)
- **Quality bar of a well-run Indie entry:** [lleoparden/naqsh](https://github.com/lleoparden/naqsh) (Arabic comic/menu localizer using Spark + SAM 3.1 + Muse Image) logs per-call costs (~$0.03 per page), recall evals, failure rates and an API friction log. [meta-ai-hackathon/meta-hack](https://github.com/meta-ai-hackathon/meta-hack) shows 770 commits and 128/128 validation assertions.
- Most repos have 0–2 stars. The top-starred items are mostly not entries:
  - [HarjjotSinghh/helicon](https://github.com/HarjjotSinghh/helicon) (Muse Code desktop GUI, 109★) is tooling
  - [lucataco/open-source-higgsfield](https://github.com/lucataco/open-source-higgsfield) (64★) is a different hackathon (#OpenSourceHiggsfield)
  
  — [muse-spark topic](https://github.com/topics/muse-spark)

### Inferences
- With ~20,000 accepted participants, the GitHub-visible sample is probably well under 10% of final submissions. Cluster *shares* are a rough signal of what is crowded, not absolute counts.
- "Verification layer for AI agents" as the product is the most saturated pitch in the field. It is also a meta, inward-facing topic that tends to score weaker on Impact (30%) than a concrete real-world beneficiary.
- SAM 3.1 + Spark "photo → report" with one image and one report risks the kickoff's "simple image analyzers" label unless it adds video tracking, measurement, actuation or a closed loop.
- Gaps with official tailwind:
  - Energy and materials, explicitly named in Push the Frontier, have very few entries.
  - Open-weights fine-tuning has a dedicated bonus and partner credits, but only ~3 visible real fine-tunes.
  - Muse Wonder and Muse Image are barely used, despite a Best Creative Build bonus and the rubric's "surfaced unexpected capabilities".
  - AI-glasses hands-free workflows are a Meta Connect narrative.
  - Legacy-code modernization with compiled-equivalence verification fits "technical depth" and "holds up in production".

### Gaps
- X, LinkedIn, Reddit and dev.to were not searchable in a useful way. X fetch returns HTTP 402, and search surfaced no participant threads. The public CV gallery shows no projects yet (checked Nov 3); it likely populates after the deadline for the Community Vote.
- Repo descriptions are self-reported. I did not check which projects actually work.

## Q6. Any FAQ or announcements changing dates or rules?

### Takeaway
No date change was found. The deadline is still **Nov 4, 9:00 PM ET**, judging runs Nov 4/5–8, and finals are Nov 9. Clarifications came through Discord #questions rather than formal amendments. They cover the runtime model rule, outside coding tools, live URL, unlisted video and the bonus mechanics. The rules reserve the right to modify terms, with significant changes communicated to registered participants.

### Cited Findings
- Key dates, unchanged on the official page as of Nov 3:
  - Nov 4: "Project submissions due by 9:00 PM ET"
  - Nov 4 – Nov 8: Judging
  - Nov 9: "Closing ceremony - live finals and winners announced"
  - "Dates may be subject to change at Meta's sole discretion. Any change will be posted on this page."
  
  — [dev.meta.ai](https://dev.meta.ai/events/global-hackathon)
- The Official Rules say: "The Organizers reserve the right to modify these terms at any time. Significant changes will be communicated to registered participants." — [Official Rules](https://cerebralvalley.ai/e/meta-ai-developer-hackathon/waiver)
- A participant guide's timeline:
  - Kickoff Mon Oct 26, 12 PM ET
  - Judging Nov 5–8
  - Closing ceremony Mon Nov 9, 12 PM ET
  - Community vote winner Mon Nov 16
  - API credits must be claimed by Nov 4, 9 PM ET
  
  — [meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md)
- Organizer Discord clarifications (Oct 27, Oct 28 and Oct 31) are listed in Q1–Q3. — [naqsh issue #10](https://github.com/lleoparden/naqsh/issues/10)
- Discord channels: #announcements, #questions (CV team), #office-hours (Meta team), #team-search and #resources (partner credit forms). — [meta-hack event guide](https://github.com/meta-ai-hackathon/meta-hack/blob/main/info/event%20guide.md); [rules-summary.md](https://github.com/TimurSalakhetdinov/meta-ai-hackathon/blob/main/docs/hackathon/rules-summary.md)

### Inferences
- 9:00 PM ET on Nov 4 is EST (UTC-5) because US DST ended Nov 1, so the deadline is **02:00 UTC Thu Nov 5** (7:30 AM IST Nov 5).
- #announcements on Discord, which needs login, is the most likely place for any last-minute change. The user should check it before submitting.

### Gaps
- Discord #announcements could not be read without login, so a last-minute change posted only there cannot be ruled out.
