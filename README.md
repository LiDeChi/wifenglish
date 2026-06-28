# WifEnglish — 家具销售情景对话 (Furniture Shop Dialogues)

Progressive, level-based English learning scenarios built from the original bilingual lesson sheets in the `家具/` folder.

## Design Principles
- **关卡式由浅入深**: 6 levels from simple greeting → complex negotiation + after-sales.
- **串联内容**: Later levels reference items and phrases introduced earlier.
- **真实情景**: Customer + Sales (variable 1-3 people, including couples).
- **画面 + 声音**:
  - Visuals: generated via APIMart GPT-Image-2 (or fallback)
  - Sound: Boson AI Higgs TTS with emotion tags (`<|emotion:friendly|>`)
- **语言顺序**: English (clear/slow) → English (natural) → 中文
- **字幕**: Bilingual always visible in the player

## Project Structure
- `scenes/scenarios.json` — full structured dialogues
- `audio/` — generated .mp3 (Boson)
- `visuals/` — scene images
- `web/` — ready-to-deploy static site (Tailwind + JS player)
- `scripts/tts_boson.py` — the TTS skill / helper (emotion injection)
- `furniture_lessons/` — raw extracted pages (Gemma4 vision OCR)

## How to Run Locally
```bash
cd web
python3 -m http.server 5173
# open http://localhost:5173
```

## Audio Generation (Boson Higgs)
```bash
export BOSON_API_KEY=bai-MvuD-6LzgliIUQAxQ007pRyOfVPBfuM6qymny_nKlsE1sPNF
python3 scripts/tts_boson.py \
  --text "<|emotion:friendly|><|style:professional|>Hello, welcome..." \
  --out audio/greet.mp3
```

## Generate Images (APIMart)
Use the bundled helper (requires APIMART_API_KEY):
```bash
python3 /path/to/apimart/scripts/generate_image.py \
  --prompt "..." --out visuals/levelX.jpg --resolution 1k
```

## Deploy

**GitHub**: https://github.com/LiDeChi/wifenglish

**Live site**: https://wifenglish.wordm.us (or https://wifenglish.pages.dev)

This site is deployed to **Cloudflare Pages** from the `web/` folder (pure static site, no build step required).

### Automatic deployment (push to GitHub = auto update)

We've prepared the project for Cloudflare-native Git integration (so deploys happen on Cloudflare's side without using GitHub Actions quota).

**Setup steps (Method 1 - for existing project):**

1. Go to [Cloudflare Dashboard → Pages](https://dash.cloudflare.com) → select the `wifenglish` project.
2. Go to **Settings → Build & deployments**.
3. In the **Git integration** section, connect your GitHub account and select the `wifenglish` repo (LiDeChi/wifenglish).
4. Configure:
   - Production branch: `main`
   - Build command: **(leave empty)**
   - Build output directory: `web`
5. Save / Connect.

Once connected, every push to `main` on GitHub will automatically trigger a deploy on Cloudflare.

**Note:** The project was originally created via direct upload, so the Git connection may require confirming in the UI. The build settings have already been pre-configured via API (build_command empty, destination `web`).

The GitHub Actions workflow has been switched to manual-only (`workflow_dispatch`) to avoid consuming Actions minutes while setting up the native integration.

### Manual / one-off deploy (from local)

```bash
cd web
npx wrangler pages deploy . --project-name=wifenglish --commit-dirty=true
```

(Requires `CLOUDFLARE_API_TOKEN` with Pages:Edit.)

Custom domain `wifenglish.wordm.us` is already configured on the project.

### Manual deploy (from local)

```bash
cd web
npx wrangler pages deploy . --project-name=wifenglish --commit-dirty=true
```

Custom domain `wifenglish.wordm.us` is already added (DNS + Pages project).

All dialogues are designed to be educational, natural, and chained across levels.

Generated with care using best-in-class local vision (Gemma4) + Boson TTS + modern tooling.
