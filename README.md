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

## Deploy to Vercel (online)
```bash
cd web
npx vercel --prod
# or use the MCP: deploy_to_vercel
```

All dialogues are designed to be educational, natural, and chained across levels.

Generated with care using best-in-class local vision (Gemma4) + Boson TTS + modern tooling.
