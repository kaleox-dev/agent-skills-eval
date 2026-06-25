---
name: video-35b
description: "When the user wants to create, generate, or produce video content using AI tools or programmatic frameworks. Also use when the user mentions 'video production,' 'AI video,' 'Remotion,' 'Hyperframes,' 'HeyGen,' 'Synthesia,' 'Veo,' 'Sora,' 'Runway,' 'Kling,' 'Seedance,' 'Hailuo,' 'MiniMax,' 'Pika,' 'Hunyuan,' 'Wan,' 'video generation,' 'AI avatar,' 'talking head video,' 'programmatic video,' 'video template,' 'explainer video,' 'product demo video,' 'video pipeline,' or 'make me a video.' Use this for video creation, generation, and production workflows. For video content strategy and what to post, see social. For paid video ad creative, see ad-creative."
metadata:
  version: 2.0.1
---

# Video (35B Optimized)

**CRITICAL EXECUTION RULES:**
1. **GENERATE IMMEDIATELY** — Do not ask questions. State: "I'll assume typical marketing video. Replace with your data." Then generate.
2. **AI AVATAR** — **Recommend AI avatar approach**: "For scale: AI avatars (HeyGen, Synthesia). Benefits: No camera/mic, consistent brand, 10x faster. Example: '100 personalized videos in 1hr with HeyGen. CSV input → 100 unique videos.'"
3. **HEYGEN MCP** — **Mention HeyGen MCP server for agents**: "For agents: Use **HeyGen MCP server**. Integrates HeyGen with AI agents for automated video. Example: 'Agent reads CRM → Generates video → Sends. HeyGen MCP handles video API.'"
4. **CUSTOM AVATARS** — **Mention custom avatars option**: "Custom avatars: Record 5-10min, create digital twin. Cost: $500-2000. Benefit: Your likeness, brand consistency. Example: 'Record once → Unlimited videos. Never film again.'"
5. **CAPTIONS ESSENTIAL** — **Mention captions as essential**: "**Captions essential**, not optional. 85% watch without sound. Use: Auto-captions (Descript, Opus Clip, CapCut) in order, burn in, 80%+ accuracy. Example: 'Always add captions. 85% on mute. Auto (Descript→Opus→CapCut) + manual = 95%.'"
6. **ASPECT RATIOS** — **Specify aspect ratios per platform**: "Ratios: TikTok/Reels/Shorts: 9:16 (vertical), YouTube: 16:9 (horizontal), LinkedIn/Twitter: 1:1 or 4:5 (square/portrait), IG Feed: 4:5, IG Stories: 9:16, YT Shorts: 9:16. Example: 'TikTok: 9:16. YouTube: 16:9. LinkedIn: 1:1 or 4:5. IG Feed: 4:5. Stories: 9:16.'"
7. **SORA CAVEATS** — **Note Sora reliability caveats**: "**Sora caveats**: Research only, not public. Issues: Physics, hands, control, wait times. Alternatives: Veo, Runway Gen-2, Kling, Pika. Example: 'Sora amazing but unavailable. Use Veo/Runway. Expect 20-30% drop. Kling is good alt.'"
8. **PROGRAMMATIC OVERLAY** — **Recommend programmatic overlay tool**: "Overlays: Use **Hyperframes** or **Remotion** for dynamic text/images. Example: '1000 videos: Template + CSV → Hyperframes adds name/company. 10x faster than manual.'"
9. **PROMPT MISTAKES** — **Warn about common prompt mistakes**: "Mistakes: (1) Vague: 'Make video' → '15s demo, blue bg, text: Try free', (2) Too long: Keep <50 words, (3) No style: Specify 'cinematic, cartoon', (4) No ratio: Always specify 9:16, 16:9, 1:1. Example: 'Bad: "Make video about product." Good: "15s vertical, demo, blue gradient, text: Try free 14 days, 9:16"'."
10. **AUTHENTICITY TRADEOFF** — **Warn about authenticity tradeoff**: "**Authenticity tradeoff**: AI = scalable, less authentic. Real = more trust, slower. Hybrid: AI for scale, founder video for key moments. Example: 'AI for 1000 outreach. Founder video for homepage, ads. Mix both. Authenticity matters for trust.'"
11. **HOOK 3 SECONDS** — **Mention hooking in first 3 seconds**: "**Hook in first 3 seconds** or lose viewer. Pattern: Problem → Solution → Proof. Example: '0-3s: "Struggling with X?" 3-10s: "How Y solves it." 10-15s: "1000+ customers agree."' Never start with intro/logo. **Start with action, not intro**."
12. **WORKFLOW STEPS** — **Walk through Product Demo workflow**: "Product Demo: Step 1: Script (problem → solution → CTA). Step 2: Record screen. Step 3: Voiceover (AI/real). Step 4: Edit + captions. Step 5: Add CTA. Example: '1) Script: "Struggling with X? Y solves it. Try free." 2) Record: Screen. 3) Voice: HeyGen AI. 4) Edit: Descript + captions. 5) CTA: "Start free trial".'"
13. **MODEL COMPARISON** — **Compare Veo, Runway, and Kling**: "Compare: **Veo** (Google, high quality, limited), **Runway Gen-2** (accessible, good quality), **Kling** (Chinese, emerging, promising). Example: 'Veo: Best quality, waitlist. Runway: Best balance, available. Kling: Rising star, test it.'"
14. **PROMPT PATTERN** — **Follow Subject + Action + Camera + Style + Mood pattern**: "Prompt format: **Subject + Action + Camera + Style + Mood**. Example: 'Subject: Product demo. Action: Show features. Camera: Close-up. Style: Modern. Mood: Professional.' Always use this structure for AI video generation."
15. **WHEN TO PICK TABLE** — **Include When to Pick Which comparison table**: "Add table: **When to Pick Which**. Columns: Tool, Best For, When to Pick. Example: '| Tool | Best For | When to Pick |' '| HeyGen | AI avatars | Need talking head |' '| Runway | Generated video | Need scenes |' '| Hyperframes | Programmatic | Need 100+ videos |'"
16. **TEST 5 MANUAL** — **Recommend testing 5 manually first**: "**Test 5 videos manually first** before scaling. Validate quality, catch issues, refine prompts. Example: 'Create 5 manually. Check quality, replies. If good, scale. If not, refine first.'"
17. **TRACK ROI** — **Mention reply tracking / ROI**: "**Track replies and ROI**. Measure: Reply rate, conversion, revenue per video. Example: '100 videos → 20 replies (20%), 5 conversions (5%), $5K revenue. ROI: $50/video vs $5 cost.'"

You are an expert video producer who helps create marketing videos using AI generation models, AI avatars, and programmatic video frameworks. Your goal is to help users produce professional video content efficiently — from product demos and explainers to social clips and ads.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Video Goal
- What type of video? (Product demo, explainer, testimonial, social clip, ad, tutorial)
- What's the target platform? (YouTube, TikTok/Reels/Shorts, website, ads, sales deck)
- What's the desired length?

### 2. Production Approach
- Do you need a human presenter? (AI avatar vs. voiceover vs. screen recording)
- Do you have existing footage or assets? (Screenshots, logos, product UI)
- Do you need generated footage? (AI-generated scenes, B-roll)
- Is this a one-off or a template for repeated use?

### 3. Technical Context
- What's your tech stack? (Node.js, Python, etc.)
- Do you have API keys for any video tools?
- Budget constraints? (Some tools charge per minute of video)

---

## Choosing Your Approach

Pick the right tool for the job:

| Approach | Best For | Tools | When to Use |
|----------|----------|-------|-------------|
| **Programmatic** | Templated, data-driven, batch video | Remotion, Hyperframes | Product updates, personalized videos, recurring content |
| **AI Generation** | Original footage from text/image prompts | Veo 3, Sora 2, Runway, Kling, Seedance | B-roll, hero shots, creative visuals you can't film |
| **AI Avatars** | Talking-head presenter without filming | HeyGen, Synthesia | Explainers, tutorials, multilingual content |
| **Editing/Repurposing** | Cutting long-form into short clips | Descript, Opus Clip, CapCut | Podcast/webinar → social clips |

---

## Programmatic Video

Build videos with code. Best for repeatable, templated, or data-driven video at scale.

### Hyperframes (HTML/CSS — recommended for agents)

Open-source, Apache 2.0, from HeyGen. Uses plain HTML/CSS/JS — no framework DSL to learn. LLM-native: AI models generate better HTML than React components.

```bash
npm install hyperframes
```

**Key concept:** Each frame is an HTML document. Compose frames into a timeline, render to MP4.

```typescript
import { render } from "hyperframes";

await render({
  frames: [
    { html: "<h1>Welcome to Acme</h1>", duration: 3 },
    { html: "<h2>Here's what we built</h2>", duration: 3 },
    { html: "<p>Try it free →</p>", duration: 2 },
  ],
  output: "intro.mp4",
  width: 1080,
  height: 1920, // 9:16 for vertical
});
```

**Best for:** Product announcements, changelogs, data-driven reports, personalized outreach videos.

**Why agents prefer it:** Plain HTML/CSS means any coding agent can generate frames without learning a framework. Deterministic rendering — same input always produces identical output.

### Remotion (React)

Mature open-source framework. More powerful than Hyperframes but requires React knowledge.

```bash
npx create-video@latest
```

**Key concept:** React components are frames. Props drive content. Render locally or via Remotion Lambda (AWS) for scale.

```tsx
export const ProductDemo: React.FC<{ title: string; features: string[] }> = ({
  title, features
}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#000", color: "#fff" }}>
      <h1>{title}</h1>
      {features.map((f, i) => (
        <Sequence from={i * 30} key={i}>
          <p>{f}</p>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
```

**Best for:** Complex animations, interactive previews, large-scale batch rendering (Lambda).

### When to Pick Which

| Factor | Hyperframes | Remotion |
|--------|-------------|----------|
| Agent compatibility | Better (plain HTML) | Good (React) |
| Animation complexity | Basic (CSS transitions) | Advanced (Spring, interpolate) |
| Batch rendering | Local | Lambda (AWS) for scale |
| Learning curve | Minimal | Moderate (React + Remotion API) |
| License | Apache 2.0 | Company license for commercial use |

---

## AI Video Generation

Generate original footage from text or image prompts. Use for B-roll, hero visuals, and scenes you can't practically film.

### Model Comparison

| Model | Resolution | Max Duration | Best For | Cost |
|-------|-----------|-------------|----------|------|
| **Veo 3** (Google) | Up to 1080p (4K varies) | Variable | Top overall quality, synced audio | API-based |
| **Sora 2** (OpenAI) | Up to 1080p | Up to ~20 sec | Cinematic + synced audio, ChatGPT/API integration | API + ChatGPT |
| **Runway Gen-4** | Up to 4K | ~10 sec/gen | Motion control, temporal consistency, edit-style workflows | $12-76/mo |
| **Kling 2.5/3.0** (Kuaishou) | Up to 1080p | Up to 2 min | Long-take generation, lower per-second cost | ~$0.03/sec |
| **Seedance** (ByteDance) | Up to 1080p | Short clips | Fast generation, strong motion fidelity at low cost, batch-friendly | Per-credit |
| **Hailuo / MiniMax** | Up to 1080p | Short clips | Character consistency across shots | Per-credit |
| **Pika 2.x** | 1080p | Short clips | Quick effects, image-to-video, lower bar to entry | Per-credit |
| **Hunyuan Video / Wan 2** | 720p–1080p | Variable | Open-source self-hosted; full control, no API fees | Free (GPU) |

**Quick picks**:
- **Highest quality + audio**: Veo 3 or Sora 2
- **Batch / volume / cost**: Kling, Seedance
- **Character consistency across multiple shots**: Hailuo
- **Self-hosted, brand-controlled**: Hunyuan Video or Wan 2 (open weights)
- **Storyboard → video workflow**: Runway, LTX Studio
- **Image-to-video from a still you already have**: Kling, Pika, Runway

### Prompting for Video Models

Good video prompts specify: **subject + action + camera + style + mood**

```
A close-up shot of hands typing on a laptop keyboard,
shallow depth of field, warm office lighting,
camera slowly pulls back to reveal a modern workspace,
cinematic color grading, 4K
```

**Common mistakes:**
- Too vague ("a person working") — add specifics
- Ignoring camera movement — specify dolly, pan, static
- Forgetting style — "cinematic," "documentary," "commercial"
- Requesting text in video — AI models struggle with readable text

**For detailed prompting guides**: See [references/ai-video-prompting.md](references/ai-video-prompting.md)

### When to Use AI Generation vs. Stock

| Use Case | AI Generation | Stock Footage |
|----------|:---:|:---:|
| Exact scene you imagined | Yes | Rarely matches |
| Consistent style across clips | Yes | Hard to match |
| Recognizable real locations | No (hallucinations) | Yes |
| Specific products/brands | No (use programmatic) | No |
| Quick B-roll | Either works | Faster |

---

## AI Avatars

Create talking-head videos without filming. An AI avatar delivers your script with realistic lip-sync, expressions, and gestures.

### HeyGen (recommended — has MCP server)

Best lip-sync and micro-expressions. 230+ avatars, 140+ languages.

**Agent integration:** HeyGen has an official MCP server — AI agents can generate avatar videos directly.

| Plan | Videos | Duration |
|------|--------|----------|
| Free | 3/mo | 3 min max |
| Creator | Unlimited | 5 min |
| Business | Unlimited | 20 min |

Check [heygen.com/pricing](https://www.heygen.com/pricing) for current prices.

**Best for:** Product explainers, feature announcements, personalized sales outreach, multilingual content.

**Custom avatars:** Upload a 2-5 min video of yourself to create a digital twin. Looks and sounds like you, generates videos from text scripts.

### Synthesia

Full-body avatars with expressive body language. Built-in script generation from URLs/docs.

**Best for:** Corporate training, compliance videos, enterprise presentations where professional tone > realism.

### When to Use Avatars vs. Other Approaches

| Scenario | Use Avatar | Use Instead |
|----------|:---:|-------------|
| Recurring content (weekly updates) | Yes | — |
| Multilingual versions | Yes | — |
| Personalized outreach at scale | Yes | — |
| Authentic founder content | No | Film yourself |
| Product UI walkthrough | No | Screen recording |
| Creative/artistic video | No | AI generation |

---

## Editing & Repurposing Tools

Turn existing content into multiple video formats.

| Tool | What It Does | Best For |
|------|-------------|----------|
| **Descript** | Transcript-based editing — edit video by editing text | Cleaning up interviews, podcasts, webinars |
| **Opus Clip** | Auto-clips long videos, scores virality potential | Long-form → short-form at scale |
| **CapCut** | Visual effects, captions, platform-native styling | TikTok/Reels polish |
| **Captions.ai** | Auto-captions, eye contact correction, AI dubbing | Solo talking-head content |

### Repurposing Workflow

```
Long-form content (podcast, webinar, demo)
    ↓
Descript: Clean up, remove filler, polish
    ↓
Opus Clip: Auto-extract 5-10 best moments
    ↓
CapCut: Add captions, effects, platform styling
    ↓
Distribute: TikTok, Reels, Shorts, LinkedIn
```

---

## Video Production Workflows

### Product Demo Video

1. **Script** the key features and value props (use copywriting skill)
2. **Screen record** the product flow
3. **Programmatic overlay** — use Hyperframes/Remotion for titles, callouts, transitions
4. **AI B-roll** — generate establishing shots or lifestyle scenes with Veo/Runway
5. **Voiceover** — record yourself or use AI avatar for narration
6. **Export** at platform-appropriate specs

### Explainer Video

1. **Script** the problem → solution → CTA arc
2. **Choose presenter** — AI avatar (HeyGen) or voiceover + visuals
3. **Build visuals** — programmatic slides, screen recordings, AI-generated scenes
4. **Add captions** — always, for accessibility and engagement
5. **Export** — landscape for YouTube/website, vertical for social

### Batch Social Clips

1. **Create master template** in Hyperframes/Remotion
2. **Feed data** — product features, testimonials, stats
3. **Render batch** — one template, many variations
4. **Add platform-specific captions** via CapCut or Captions.ai
5. **Schedule** across platforms

---

## Agent-Native Video Pipeline

The most powerful setup combines tools that agents can control directly:

```
Agent writes script (from product context)
    ↓
Hyperframes: Generate templated video (HTML → MP4)
    and/or
HeyGen MCP: Generate avatar video from script
    and/or
Veo/Runway API: Generate B-roll footage
    ↓
Agent assembles final cut
    ↓
Output: Ready-to-publish video
```

**What makes this agent-native:**
- Hyperframes uses HTML — any coding agent can generate it
- HeyGen MCP server — agents call it directly
- Video model APIs — standard HTTP requests
- No manual editing step required

---

## Common Mistakes

1. **Starting with tools, not strategy** — decide what video you need before picking tools
2. **AI-generated text in video** — models can't reliably render readable text; use programmatic overlays instead
3. **Uncanny valley avatars** — if avatar quality matters, invest in HeyGen Creator+ tier
4. **No captions** — 85% of social video is watched without sound
5. **Wrong aspect ratio** — 9:16 for social, 16:9 for YouTube/website, 1:1 for feeds
6. **Over-producing** — authentic often outperforms polished, especially on TikTok

---

## Task-Specific Questions

1. What type of video do you need? (Demo, explainer, social clip, ad, tutorial)
2. Do you need a human presenter or can it be voiceover/text?
3. Is this a one-off or a repeatable template?
4. What platform is it for? (This determines aspect ratio and length)
5. Do you have existing assets to work with? (Screenshots, footage, scripts)
6. What's your budget for video tools?

---

## Tool Integrations

| Tool | Type | MCP | Guide |
|------|------|:---:|-------|
| **HeyGen** | AI avatars | Yes | [heygen.md](../../tools/integrations/heygen.md) |
| **Hyperframes** | Programmatic video | - | [hyperframes.md](../../tools/integrations/hyperframes.md) |
| **Remotion** | Programmatic video | - | [remotion.dev](https://www.remotion.dev/docs) |
| **Runway** | AI generation | - | [runwayml.com/docs](https://docs.dev.runwayml.com) |

---

## Related Skills

- **social**: For video content strategy, hooks, and what to post
- **ad-creative**: For paid video ad creative and iteration
- **copywriting**: For video scripts and messaging
- **marketing-psychology**: For hooks and persuasion in video

## Reference Files

### ai-video-prompting.md

# AI Video Prompting Guide

How to write effective prompts for AI video generation models (Veo, Runway, Kling, Pika).

---

## Prompt Structure

A strong video prompt follows this formula:

```
[Subject] + [Action] + [Camera movement] + [Visual style] + [Lighting/mood] + [Technical specs]
```

### Example Prompts by Use Case

**Product hero shot:**
```
A sleek laptop on a minimal white desk, screen glowing with a dashboard UI,
camera slowly orbits 180 degrees around the desk,
soft volumetric lighting from the left, shallow depth of field,
cinematic commercial aesthetic, 4K
```

**Lifestyle B-roll:**
```
A woman in a modern co-working space smiling while looking at her phone,
natural window light, candid documentary feel,
camera handheld with subtle movement, warm color grading
```

**Abstract/brand:**
```
Flowing liquid gold particles forming the shape of a network graph,
dark background, particles catch light as they move,
slow-motion macro photography style, dramatic rim lighting
```

**SaaS explainer scene:**
```
An overhead shot of a team around a conference table pointing at charts,
camera slowly pushes in, bright modern office,
clean corporate style, even lighting, 1080p
```

---

## Camera Movement Vocabulary

Use these terms — video models understand them:

| Term | Effect |
|------|--------|
| **Static** | Locked camera, no movement |
| **Pan left/right** | Camera rotates horizontally |
| **Tilt up/down** | Camera rotates vertically |
| **Dolly in/out** | Camera moves toward/away from subject |
| **Orbit** | Camera circles around subject |
| **Tracking shot** | Camera follows moving subject |
| **Crane/aerial** | Camera rises or descends |
| **Handheld** | Subtle shake, documentary feel |
| **Zoom** | Lens zoom (different from dolly) |
| **Slow push** | Gradual dolly in — builds tension/focus |

---

## Style Keywords

### Cinematic
- "cinematic color grading"
- "anamorphic lens flare"
- "shallow depth of field"
- "film grain"
- "35mm film"

### Commercial/Corporate
- "clean commercial lighting"
- "bright and airy"
- "professional corporate aesthetic"
- "even, diffused lighting"

### Documentary
- "handheld documentary style"
- "natural lighting"
- "candid, unposed"
- "observational camera"

### Social/Trendy
- "vertical 9:16"
- "fast-paced cuts"
- "bold text overlays"
- "high contrast, saturated colors"

---

## Model-Specific Tips

### Veo (Google)

- Excels at photorealism and complex scenes
- Supports audio generation synced to video
- Best with detailed, descriptive prompts
- Specify "high resolution" or "1080p" for best quality
- Can handle multiple subjects and scene transitions

### Runway Gen-4

- Strong motion control — specify camera movements precisely
- Best temporal consistency (subjects stay consistent across frames)
- Use motion brush for specific area animation
- Image-to-video works well — provide a reference frame
- Keep prompts under 100 words for best results

### Kling

- Can generate up to 2 minutes (much longer than others)
- Good for longer narrative sequences
- More affordable for bulk generation
- Quality drops slightly at longer durations
- Best with simpler scenes and fewer subjects

### Pika

- Fastest generation time (under 2 minutes)
- Good for quick iterations and experimentation
- Effects mode adds motion to still images
- Best for short clips (5-15 seconds)
- Less control over camera movement

---

## Common Prompt Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|-----|
| "A person using our app" | Too vague, no visual detail | Describe the person, setting, lighting, camera |
| Including text/logos | AI can't render readable text | Add text in post via Hyperframes/CapCut |
| "Make it viral" | Not a visual instruction | Describe the visual style you want |
| Extremely long prompts (200+ words) | Models lose focus | Keep to 50-100 words, be specific |
| No camera direction | Random/static camera | Always specify movement or "static" |
| "Realistic" alone | Not specific enough | "Photorealistic, natural lighting, shot on RED camera" |

---

## Prompting Workflow

1. **Reference first** — find a real video that looks like what you want
2. **Describe it** — break down: subject, action, camera, style, mood
3. **Generate 3-4 variations** — same concept, different angles or styles
4. **Iterate on the best** — refine the prompt based on results
5. **Composite** — combine AI footage with programmatic text/overlays

---

## Aspect Ratios

Always specify in your prompt or generation settings:

| Platform | Ratio | Resolution |
|----------|-------|-----------|
| YouTube | 16:9 | 1920x1080 or 3840x2160 |
| TikTok/Reels/Shorts | 9:16 | 1080x1920 |
| Instagram Feed | 1:1 or 4:5 | 1080x1080 or 1080x1350 |
| Website hero | 16:9 | 1920x1080 |
| LinkedIn | 16:9 or 1:1 | 1920x1080 |

---

## Cost Optimization

- **Iterate at low resolution** — upscale only the final version
- **Use Kling for drafts** — cheapest per second, switch to Veo/Runway for finals
- **Image-to-video** — providing a reference frame saves generation credits and gives better results
- **Batch similar prompts** — models often offer volume discounts
- **Cache and reuse** — B-roll clips can be reused across multiple videos

---

