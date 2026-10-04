# AI Image & Video Sites — Capability Survey

*Research survey for the Signature AI Pixel (image + video maker) rebuild — what the leading sites actually let users do, verified from docs/official pages/reputable articles, 2024–2026 era. Surveyed 2026-10-04.*

---

## 1. Midjourney (V7 / V8.1)

- **Prompt box** on midjourney.com/imagine ("What will you imagine?"); parameters appended to prompt text (e.g. `--ar 16:9`) or set via visual sliders in the web settings panel.
- **Distinctive parameter system**: `--stylize/--s` (0–1000, artistic interpretation), `--chaos/--c` (0–100, grid diversity), `--weird` (0–3000, surreal aesthetics), `--exp` (V7 experimental tone-mapped look), `--no` (negative prompt), `--seed` (reproducible results), `--tile` (seamless patterns), `--style raw` (remove default beautification), `--draft` (10× faster, half cost), `--repeat/--r` (N image sets per prompt), `--q` (quality/GPU time), permutations `{opt1, opt2}`, quoted `"text here"` for text rendering.
- **Style presets**: `--style raw`, model versions (`--v 7`, `--v 8.1`, `--niji 7` anime model); **Personalization** (`--p`, on by default in V7, learned from pair-ranking votes).
- **Aspect ratio**: `--ar W:H` (also visual slider in settings).
- **Variations / remix**: Vary (Subtle) / Vary (Strong) per image; Remix mode lets you change prompt + parameters while varying; Vary Region (regional variation).
- **Upscale**: one-click Upscale on any grid image for a high-res downloadable output.
- **Inpainting / outpainting / editing**: Canvas editor in the lightbox (smart segmentation, move tool, regional editing); V6.1 workflows handle upscaling/inpainting/retexturing; Pan (outpaint/extend canvas) + Zoom out.
- **Reference/character consistency**: `--sref` image URL (style reference + `--sw` style weight), `--oref` (Omni-Reference — character/object anchoring with `--ow` omni weight, V7), `--iw` (image prompt weight), Character Reference (`--cref`) on the web UI.
- **Video**: Midjourney added image-to-video (Animate Image; `--motion low/high`, `--loop` for seamless loops) — video is now part of the web app alongside stills.
- **Pricing**: no free trial since 2023; paid only from ~$10/mo (Basic); Turbo/Relax modes trade speed for GPU cost; free Discord is view-only for generations.

Sources: https://github.com/justinperea/midjourney-cc-skill/blob/HEAD/knowledge/v7-parameters.md · https://github.com/aedelon/claude-code-blueprint/blob/HEAD/agents/midjourney-expert.md · http://aiweekly.co/learning-ai/generative-ai/how-to-use-midjourney · https://aibreakfast.beehiiv.com/p/midjourney-v7-introduces-enhanced-image-quality-and-precision-reference · https://medium.com/let-there-be-prompt/new-midjourney-v-7-update-omni-ref-exp-and-q4-parameters-5f2194327c66

---

## 2. ChatGPT Image Generation (DALL-E 3 → GPT-image-1 / 1.5 / 2 / 2.5)

- **Prompt box** is the ChatGPT chat itself — conversational prompting; GPT-image models rewrite/augment prompts automatically ("prompt enhancement" built in); the model also uses multi-turn conversation context.
- **Style presets**: style cues in plain language (photoreal, painterly, comic, line art); quality presets (low/medium/high/xhigh/max on 2.5); DALL-E 3 had standard vs HD quality; background `auto/opaque/transparent` (transparent PNGs).
- **Aspect ratio / resolution**: sizes via natural language or `aspectRatio` (auto, 1:1, 3:2, 2:3) on 1.5; 2.5 supports `width`/`height` up to 3840px; DALL-E 3 outputs 1024×1024 / 1792×1024 / 1024×1792.
- **Variations / remix**: batch generation (1–10 outputs per prompt); variations endpoint (fresh takes on one image); conversational "give me three options / change X" iteration.
- **Inpainting / outpainting / edit-by-prompt**: upload an image and describe changes; mask-based inpainting (`mask` PNG on 2.5 / GPT Image 2); new **Edit mode toolbar** (Images 2.5): Markup, Comment (point at an element and attach an instruction — "remove this"), Remove BG (transparent PNG), Erase (brush-away objects), Resize (switch aspect ratio Portrait 3:4 / Widescreen 16:9 / Landscape 4:3); every edit saved as a separate version with history; GPT Image 1.5 has `inputFidelity: high` (locks reference) vs `low` (reworks reference).
- **Text in image**: strong typography rendering (exact words in quotes — a GPT-image hallmark).
- **Image-to-video**: via Sora (see §10); images can also be generated inside Sora/ChatGPT flows.
- **Pricing**: image generation bundled with ChatGPT (Plus ~$20/mo includes image gen; free tier has limited access).

Sources: https://techsith.com/can-chatgpt-do-image-generation/ · https://www.i-scoop.eu/chatgpt-images-2-5-delivers-sharper-details-faster-generation-and-precise-editing/ · https://github.com/scenario-labs/skills/blob/HEAD/skills/scenario-gpt-image/SKILL.md · https://github.com/hinvec/security-scanned-skills/blob/HEAD/skills/dalle-variations-pipeline/SKILL.md

---

## 3. Adobe Firefly

- **Prompt box** on firefly.adobe.com; prompt enhancement built in (Firefly rewrites/expands prompts for better results); **Generative Fill** uses text descriptions over selections.
- **Style presets/filters**: style/effect presets in the web app (photo/art/graphic looks), structure & style reference images, settings for visual intensity; Firefly Image Model 5 (4MP photoreal output).
- **Aspect ratio / resolution**: aspect-ratio presets (square, landscape, portrait, widescreen); up to 4MP output on Image Model 5.
- **Variations**: generate multiple variations per prompt; re-generate with adjusted settings.
- **Distinctive commercial-safety story**: trained only on licensed Adobe Stock, public-domain, and openly-licensed content; IP indemnification for enterprise; **Content Credentials** (provenance metadata) attached to all Firefly outputs.
- **Inpainting/outpainting**: **Generative Fill** (select an area, describe add/remove/replace) and **Generative Expand** (extend beyond original borders) — also native inside Photoshop.
- **Text in image**: good text rendering (logos, posters) — noted strength vs Midjourney.
- **Text-to-video & audio**: built-in AI video generation (text-to-video, ~5s clips) and audio generation; **partner models** accessible in-app (Google Veo 3, Runway, FLUX.2, ChatGPT Image).
- **Firefly Boards**: moodboard/storyboard workspace for exploring and developing visual concepts.
- **Text-to-vector**: generate editable vector graphics from text.
- **Pricing**: free tier (limited daily generations, watermark on exports); Standard ~$9.99/mo (2,000 credits, unlimited images in Adobe apps); Pro ~$19.99/mo; higher Premium tier; video consumes credits heavily (~20 five-second videos on Standard).

Sources: https://writetested.com/blog/adobe-firefly · https://www.a-zsoft.com/ai-image-generator/adobe-firefly-ai-image-video-creative-content-generator/ · https://www.tooljunction.io/ai-tools/adobe-firefly · https://www.asianefficiency.com/technology/canva-vs-adobe-firefly/

---

## 4. Ideogram (V4.5)

- **Prompt box** with **Magic Prompt** auto-enhancer (rewrites rough descriptions into detailed prompts).
- **Style presets**: style picker (design, realistic, anime, etc.), custom color palettes, savable **Style Codes**; image reference for style guidance.
- **Aspect ratio / resolution**: seven aspect ratios (1:1, 3:2, 16:9, 9:16, 2:3, 3:4, 4:5) at 1K/2K, low/medium/high quality tiers.
- **Remix / variations**: **Remix** (image-to-image keeping composition); re-render variations of a result.
- **Describe**: turns an existing image into a reusable prompt (reverse prompt engineering).
- **Distinctive text-in-image**: best-in-class readable typography (posters, logos, packaging); **Layerize Text** separates text from an image into editable text layers.
- **Canvas editor**: in-browser editor for inpainting (**Magic Fill**), **Extend** (outpaint), reframing, local revisions, prompt-based editing, text changes, object replacement; transparent-image editing.
- **Reference/character consistency**: **Character Reference** (character consistency across images, available even on free tier); Style Reference; up to 5 source images + optional masks for reference-guided edits.
- **Batch/API**: API with generate/edit/remix/upscale/describe endpoints ($0.03–$0.09/image); Pro batch generation from CSV uploads; Enterprise custom models trained on your visual data.
- **Pricing**: free tier (weekly slow credits, generations public, one at a time); Basic ~$7–8/mo; Plus ~$20/mo (private generation, 1,000 priority credits, unlimited slow); Pro ~$60/mo (3,500 credits, batch); Team ~$20–30/user/mo.

Sources: https://www.scriptbyai.com/text-to-image-ideogram/ · https://10tools.online/tool/ideogram/ · https://medium.com/code-canvas/is-ideogram-really-that-good-d3d98e6c4f55 · https://venice.ai/models/ideogram-v4-5 · https://www.saasworthy.com/product/ideogram-ai/pricing

---

## 5. Stable Diffusion (SDXL / Stability AI / ComfyUI ecosystem)

- **Prompt box** + **negative prompt** field (list what you don't want); prompt weighting `((tuxedo))` / `(tuxedo:1.21)`; long-prompt weighting; live token-length validation.
- **Style presets**: Styles dropdown (save reusable prompt fragments); LoRA/LyCORIS style adapters; Textual Inversion embeddings; community checkpoints on Civitai/HuggingFace; checkpoint merger; model switching on the fly.
- **Aspect ratio / resolution**: free width/height sliders, resize options, seed resizing; **Highres Fix** (one-click high-res without distortions); SDXL native 1024px.
- **Variations**: Variations button (same image, tiny differences); seeds for reproducibility; X/Y/Z plots across parameters; batch generation & queues.
- **Upscale**: Extras tab — RealESRGAN, ESRGAN, SwinIR/Swin2SR, LDSR; Stable Diffusion Upscale pipeline.
- **Inpainting / outpainting**: dedicated inpaint tab with mask drawing/upload; outpainting; color sketch; loopback (multi-pass img2img).
- **Edit-by-prompt**: img2img with denoise strength; Prompt Editing (change prompt mid-generation); **CLIP Interrogator** (guess prompt from an image).
- **Image-to-video**: AnimateDiff / Deforum extensions; ComfyUI video workflows.
- **Distinctive control**: **ControlNet** (pose/depth/edge/composition control via preprocessors); region prompting; tiling (seamless textures); GFPGAN/CodeFormer face restoration; **ComfyUI** node-graph workflows (fully custom pipelines, API-first); open-source + runs **fully local** (privacy, no per-image cost, GPU required).
- **Pricing**: free and open-source (MIT/Stability licenses vary by model); self-hosted = free after hardware; hosted APIs (Stability, Replicate, fal) charge per image.

Sources: https://github.com/orightimutim-rgb/stable-diffusion-webui (feature list from AUTOMATIC1111 wiki) · https://github.com/zaphodthebeebs/llm-playbook/blob/HEAD/stable-diffusion/README.md · https://github.com/ssube/onnx-web · https://github.com/grupoandevelopment-m/alberto-ai/blob/HEAD/alberto-ai/skills/creative/comfyui/SKILL.md

---

## 6. Runway (Gen-4 / Gen-4.5)

- **Prompt box**: text prompt drives all generation; **Runway Agent** (plain-language conversational video production).
- **Text-to-video** (Gen-4.5, #1 on Artificial Analysis T2V leaderboard) and **image-to-video** (Gen-4), plus **video-to-video**.
- **Style presets / references**: reference-image style control; style presets per model.
- **Aspect ratio / resolution**: multiple aspect ratios; up to 1080p standard, **4K export** on Pro; 4K upscale.
- **Distinctive Motion Brush**: paint motion onto specific regions of a frame (animate exactly what you point at).
- **Camera controls**: granular camera presets — pan, tilt, zoom, dolly, crane, arc, tracking.
- **Director Mode**: multi-scene/shot character consistency.
- **Extend video**: extend clips (up to ~40s chained).
- **Video editing suite** (industry-best in class): **Aleph** (in-video editor — edit one frame, model re-edits the rest: relight, outfit change, add/remove objects); **Green Screen** (background removal); **Lip Sync**; **Act-One / Act-Two** (performance capture maps a driving video onto a character image); Expand Video.
- **Native audio**: Gen-4.5 added native audio generation + audio editing.
- **Workflows**: custom composable pipelines; timeline editor; API access.
- **Characters**: Runway Characters — real-time AI video avatars from a single image.
- **Pricing**: free tier (125 one-time credits, 720p); Standard ~$12–15/mo (625 credits, watermark removed); Pro ~$28–35/mo (2,250 credits, 1080p/4K, private mode); Unlimited ~$76–95/mo; credit burn is fast at high quality.

Sources: https://github.com/mua47105-hue/agentic-ai-video-knowledgebase/blob/HEAD/kb/wiki/archive/runway-gen-4.md · https://aiagentrank.io/ai-tools/runway · https://www.fahimai.com/runway-vs-veed · https://www.avocadoai.co/blog/roundup/best-ai-video-generator-content-creators-2026 · https://thesoftwarescout.com/runway-vs-pika-2026-which-ai-video-generator-actually-delivers/

---

## 7. Pika (2.5)

- **Prompt box**: simple text prompt → clip; also works via Discord.
- **Text-to-video**, **image-to-video** (strong face/subject consistency), **video-to-video**.
- **Style presets**: stylized looks (anime/cartoon strength); Pikaffects double as style transforms.
- **Aspect ratio / resolution**: aspect options; 720p standard, 1080p on Pro.
- **Duration**: short clips — typically 3–10 seconds per generation; extension up to ~15s; **Pikaframes** for image-transition sequences (up to 25s).
- **Distinctive Pikaffects**: one-click creative effects — Inflate, Melt, Explode, Crush, etc. — applied to images or video regions (viral social-media ready).
- **Modify Region / Swap Element**: edit specific areas of uploaded video; replace objects in existing video.
- **Twists/Additions/Scenes**: named edit modes (add elements, twist a scene).
- **First/Last Frame**: start-and-end-frame control for directed motion.
- **Lip sync**: character lip-syncing; auto-generated **sound effects** for videos (Pika has some audio capability, no full voiceover/music suite).
- **Pricing**: free tier (~80–300 credits, 480p, no watermark on downloads); Standard ~$8–10/mo (700–1,050 credits); Pro ~$35/mo (2,300–3,000 credits, 1080p); Ultra/Fancy ~$95/mo (6,000–9,000 credits, commercial license); ~30–40% cheaper per second than Runway.

Sources: https://www.therundown.ai/tools/pika · https://thesoftwarescout.com/runway-vs-pika-2026-which-ai-video-generator-actually-delivers/ · https://www.allaboutai.com/ai-reviews/pika-labs/ · https://www.avocadoai.co/blog/roundup/best-ai-video-generator-content-creators-2026 · https://www.fahimai.com/pika-vs-veed

---

## 8. Luma Dream Machine (Luma app / Ray 3.2)

- **Prompt box**; **Brainstorm** feature to reduce prompt trial-and-error; **Luma Agents** conversational workflow layer.
- **Text-to-video** and **image-to-video** on Ray 3.2; **Modify Video V2** (reshape existing footage up to 20s at 1080p — swap elements, relight, preserve performance); **Reframe** (up to 12s, change framing of a clip).
- **Distinctive keyframes**: up to **16 keyframes per clip** for frame-level shot direction; start/end frame control.
- **Camera controls**: camera motion presets + motion transfer between shots; **Director Mode** timeline for manual camera keyframing (dolly etc.).
- **Style**: Photon / Photon Flash image models (text-to-image with character/style/image reference + Modify, claimed 10× cost efficiency); character transformation, environment change, product swap, relighting.
- **Aspect ratio / resolution**: native 1080p across modes; 4K upscaling + HDR on higher plans; native **16-bit color / EXR export in ACES2065-1** for VFX/grading (pro-distinctive).
- **Duration**: 5 or 10 seconds per native generation; **Extend** chains generations up to ~5 minutes; Modify up to 20s.
- **Audio**: native generation is silent for T2V/I2V; Modify/Reframe preserve source audio; integrated ElevenLabs music/SFX/voiceover + lip-sync; Face Enhancer toggle; "Make Loopable" option; transparent-background export (.webm/.mov alpha).
- **Platform breadth**: third-party models in-app (Veo 3.1, Kling 3.0, GPT Image 2, Nano Banana, ElevenLabs); public API from $0.15/video.
- **Pricing**: no published free plan (Plus/Pro/Ultra/Team only); Plus ~$30/mo (10,000 credits, commercial use); Pro ~$90/mo.

Sources: https://thetoolsverse.com/tools/luma-dream-machine-ai-video-generator · https://magichour.ai/blog/luma-dream-machine-review · https://magichour.ai/blog/kling-vs-pika-vs-luma · https://ai-productivity.pages.dev/vs/kling-vs-luma-dream-machine/?t=kling · https://www.toolworthy.ai/tool/luma-dream-machine

---

## 9. OpenAI Sora (Sora 2)

- **Prompt box**; describe scene, camera angles, lighting, mood, action beats; image or reference-video inputs.
- **Four generation modes**: **Text-to-Video**, **Image-to-Video**, **Video-to-Video (Remix)** with remix-strength control (subtle → strong), and **Storyboard** (Pro) — frame-by-frame timestamped cards chained into one coherent multi-scene video (up to ~25s).
- **Style presets**: built-in looks — Handheld, Retro, Festive, Vintage, Comic, News, Musical, Selfie.
- **Aspect ratio / resolution**: 16:9, 9:16, 1:1; up to 720p on Plus, 1080p HD on Pro; character cameos (licensed character insertion).
- **Duration**: 5–15s Plus; up to 20–25s with Storyboard on Pro.
- **Native audio**: Sora 2 generates synchronized dialogue, ambient SFX, and background music from a single prompt.
- **Physics/motion realism**: benchmark-level temporal consistency and real-world dynamics.
- **Re-cut**: video editing tool for altering parts of generated clips; C2PA metadata marks AI provenance.
- **Pricing**: bundled with ChatGPT Plus (~$20/mo, 720p, watermark) / Pro (~$200/mo, 1080p, no watermark, longer); free tier discontinued Jan 2026. API: ~$0.10/s 720p → $0.70/s 1080p (Sora 2 API shut down 2026-09-24 per one tracker).

Sources: https://tamiltech.in/article/openai-sora-video-generator-complete-guide-india-2026 · https://github.com/achisolomon/ai-tool-review/blob/HEAD/data/_tools/users/generative-media/video-generation/openai-sora-2.md · http://wavespeed.ai:3002/blog/en/posts/openai-sora-2-complete-guide-2026/ · https://www.geeky-gadgets.com/sora-2-storyboard-mode-ai-tools/ · https://medium.com/@techyman/sora-2-0-pricing-features-limitations-you-should-know-2025-0ffd2d0ca824

---

## 10. Google Veo (Veo 3 / 3.1)

- **Prompt box**; understands cinematic terminology ("aerial shot," "timelapse," "dolly zoom"); negative prompt + seed supported via API.
- **Modes**: **text-to-video**, **image-to-video**, **video-to-video** (extend/remix input video); **Ingredients-to-Video** (supply specific elements/ingredients to build a cohesive scene); extension for longer outputs.
- **Distinctive native audio**: first major model with built-in synchronized audio — dialogue, ambient sound, music, and **dialogue lip-sync** generated together with the video (no post-production step).
- **Resolution / duration**: 1080p standard (720p on lower tiers), 4K on 3.1 via API; 8s clips (Veo 3), 12s (3.1), up to 60s on Ultra plan via stitching/extension; Veo 3.1 Lite cheaper variant; Fast variant for iteration.
- **Aspect ratio**: 16:9 and 9:16 options via API (`aspect_ratio` param).
- **Reference/character consistency**: reference images + first/last-frame control; character consistency across scenes (with limitations); text rendering improved in 3.1.
- **Safety/provenance**: SynthID invisible watermarking (+ visible watermark on some tiers).
- **Access**: Gemini API / Vertex AI / Google AI Studio / Flow / VideoFX (Labs); consumer via Google AI Pro (~$19.99/mo, Veo 3 Fast, 3/day, 720p) and Ultra (~$249.99/mo, full Veo 3/3.1, 1080p–4K); API ~$0.10–0.60/s depending on tier/resolution/audio.
- **Pricing**: one-time free trial pack (10 videos, 720p); then subscription or pay-per-second API.

Sources: http://muapi.ai/veo3 · https://ai-basics.com/veo-3-faq/ · https://github.com/mua47105-hue/agentic-ai-video-knowledgebase/blob/HEAD/kb/wiki/archive/google-veo-3.md · https://github.com/popschlock/promptfu/blob/HEAD/skills/promptfu/models/google/veo-3-1.md · https://wavespeed.ai/models/google/veo3.1/text-to-video

---

## 11. Kling (3.0 / Omni)

- **Prompt box** (concise 80–120 word prompts work best); text-to-video, image-to-video, start/end-frame-to-video (frame interpolation), video-to-video editing on Omni.
- **Distinctive multi-shot**: up to **6 connected shots in one generation** (multi-shot storyboard logic in a single request); per-second duration choice (3–15s).
- **Motion Control**: upload a reference video and the model applies its movement to your character/scene (motion-trajectory transfer).
- **Elements / reference-to-video**: multi-reference inputs for subject/character consistency across shots; multi-character coreference (3+ characters).
- **Distinctive native audio**: synchronized audio-visual generation — **lip-synced dialogue in 5 languages** (EN/ZH/JA/KO/ES + dialects), speaker-attribution prompt syntax (`[Speaker: Name] "dialogue"`), per-character voices, auto SFX; characters can switch languages mid-scene.
- **Video editing patterns** (Omni): object swap with motion preserved, background+subject replacement with light matching, targeted attribute change, full style transfer with trajectory lock.
- **Camera**: motion-control camera direction; cinematic camera presets.
- **Aspect ratio / resolution**: 16:9, 9:16, 1:1; 720p/1080p UI; native 4K on API tier; frame rates 24/30/60fps; 16-bit HDR claimed.
- **Image side**: Kolors-powered text-to-image, reference-to-image, image extension, AI multi-shot; virtual try-on for e-commerce.
- **Pricing**: free Basic tier (limited daily credits, non-commercial output); Standard ~$6.99/mo; Pro ~$25.99/mo; Premier ~$64.99/mo; Ultra ~$128+/mo; API from ~$0.084–0.14/s; annual billing ~34% off.

Sources: https://github.com/alisadikinma/gaspol-video/blob/HEAD/reference/image-video-gen/08-kling-production-guide.md · https://aivideobootcamp.com/blog/kling-ai-complete-guide-pricing-features-prompts-tips/ · https://github.com/santiagoromero27/creative-workflow/blob/HEAD/.claude/skills/kling-ai/SKILL.md · https://github.com/maciejdzierzek/kling-ai-prompt-generator/blob/HEAD/CHANGELOG.md · https://cscestudiodigital.com/blog/kling-ai-review-2026-in-depth-look-at-kuaishous-advanced-ai-video-generator/ · https://www.krea.ai/blog/kling-3-0-api-access-guide-pricing-code-examples-for-multi-shot-ai-video

---

## Common Capability Checklist

The master feature list — what a new image+video site must offer to match the leaders:

### Image generation
- [ ] **Prompt box** with auto prompt enhancement (rewrite/expand rough prompts — Ideogram Magic Prompt, Firefly, ChatGPT/GPT-image)
- [ ] **Style presets/filters** (one-tap looks: photo, anime, cinematic, design, retro…) + savable custom styles (Ideogram Style Codes, SD Styles dropdown, Midjourney `--style raw`)
- [ ] **Aspect-ratio & resolution choices** (1:1, 16:9, 9:16, 3:2, 2:3, 3:4, 4:5 presets + free dimensions; quality tiers up to 4MP/4K)
- [ ] **Negative prompt** (what to exclude — SD, Midjourney `--no`, Veo API)
- [ ] **Variations / re-roll / remix** (Vary Subtle/Strong, batch of 1–10 outputs, Remix with prompt change — Midjourney, ChatGPT, Ideogram)
- [ ] **Upscale** (one-click hi-res output — Midjourney, SD ESRGAN/RealESRGAN, Ideogram)
- [ ] **Inpainting** (mask/brush a region, describe the fix — Firefly Generative Fill, ChatGPT Edit/Erase, Ideogram Magic Fill, SD inpaint)
- [ ] **Outpainting / extend canvas** (expand beyond borders — Firefly Generative Expand, Ideogram Extend, Midjourney Pan/Zoom-out, SD outpaint)
- [ ] **Edit-by-prompt on uploads** (upload image + describe changes — ChatGPT, Firefly, Ideogram Canvas)
- [ ] **Regional/point editing** (click an element, attach instruction — ChatGPT "Comment"; Runway Aleph for video)
- [ ] **Text-in-image rendering** (readable typography for posters/logos — Ideogram best-in-class, Firefly, GPT-image; Midjourney quoted-text)
- [ ] **Transparent background export** (Remove BG → transparent PNG — ChatGPT, Ideogram; .webm/.mov alpha for video — Luma)
- [ ] **Reference/character consistency** (image/style/character reference uploads locking identity across generations — Midjourney `--sref/--cref/--oref`, Ideogram Character Reference, Firefly structure+style refs, SD IP-Adapter/ControlNet)
- [ ] **Seed control** (reproducible results — SD, Midjourney `--seed`, Veo API)
- [ ] **Generation history** (PNG metadata with settings, restore parameters from image — SD; version history per edit — ChatGPT)
- [ ] **Describe / reverse-prompt** (image → prompt — Ideogram Describe, SD CLIP Interrogator)
- [ ] **Face restoration** (GFPGAN/CodeFormer — SD; Luma Face Enhancer)
- [ ] **Commercial-safety story** (licensed-data training + provenance credentials — Firefly Content Credentials; Veo SynthID; Sora C2PA)

### Video generation
- [ ] **Text-to-video** (all 6 video sites)
- [ ] **Image-to-video** (animate a still; first-frame control — all 6)
- [ ] **Video-to-video / restyle / remix** (Sora Remix w/ strength slider, Runway video-to-video, Kling Omni edits)
- [ ] **Camera-move controls** (pan/tilt/zoom/dolly/crane/arc presets — Runway granular; Luma Director Mode; cinematic prompt terms — Veo)
- [ ] **Keyframes** (up to 16 per clip for shot direction — Luma; start/end frames — Kling, Pika, Veo)
- [ ] **Motion brush / region motion** (paint motion on regions — Runway Motion Brush; Pika Modify Region)
- [ ] **Character/performance consistency across shots** (Runway Director Mode + Act-One/Two, Kling multi-shot + Elements, Sora Storyboard, Veo reference images)
- [ ] **Storyboard / multi-shot builder** (timestamped scene cards chained into one video — Sora Storyboard, Kling 6-shot multi-shot)
- [ ] **Duration controls** (per-clip length choice 3–15s+; Plus/Pro tiers unlock longer)
- [ ] **Extend video** (chain generations for longer output — Runway, Luma up to ~5 min, Kling, Veo extension)
- [ ] **Native audio** (synced dialogue + SFX + music generated with the video — Veo, Sora 2, Kling, Runway Gen-4.5; Luma via ElevenLabs integration)
- [ ] **Lip sync** (audio-driven mouth animation — Kling 5 languages, Runway, Pika)
- [ ] **Green screen / background tools** (Runway Green Screen; transparent exports — Luma)
- [ ] **Video inpainting/edit-by-frame** (edit one frame, propagate — Runway Aleph; Pika Swap Element)
- [ ] **One-click creative effects** (Pikaffects: Inflate/Melt/Explode — Pika)
- [ ] **Reframe** (change framing/aspect of existing clip — Luma)
- [ ] **Loopable output** (seamless loops — Luma, Midjourney `--loop`)
- [ ] **Resolution ladder** (720p → 1080p → 4K by tier; 16-bit/EXR pro export — Luma)

### Platform / business
- [ ] **Free tier** (limited daily/monthly credits or one-time trial; watermark or public-by-default on free — every site except Midjourney/Sora has one)
- [ ] **Paid tiers ladder** (~$7–10 entry → ~$20–35 pro → ~$95+ unlimited/ultra; credit-based consumption)
- [ ] **Prompt queue + parallel generations** (queue multiple jobs — SD, Ideogram paid)
- [ ] **Private generations** on paid plans (Ideogram, Runway)
- [ ] **API access** (all major sites offer REST APIs)
- [ ] **Mobile + Discord/community surface** (Pika Discord, Midjourney Discord, Kling apps)
- [ ] **Commercial-use license** on paid tiers (Pika, Luma, Kling Standard+)
- [ ] **Conversational/agent layer** (plain-language production assistant — Runway Agent, Luma Agents)
