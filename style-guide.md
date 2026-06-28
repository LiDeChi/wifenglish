# WifEnglish Visual & Audio Style Guide

## Visual Consistency Rules (必须严格遵守)
- **Art style**: Photorealistic commercial lifestyle photography. High detail, natural lighting, clean composition.
- **Color grading**: Bright, warm daylight. Soft natural light from large windows. Light wood tones (#EDE4D7 floors), neutral warm beige walls, accents of sage green plants, blue-gray sofas.
- **Showroom environment** (fixed):
  - Large modern furniture showroom in a Chinese city
  - Floor-to-ceiling windows on one side
  - Light oak wooden flooring
  - High ceilings, recessed lighting + natural daylight
  - Several modern sofas, coffee tables, dining sets visible in background (keep similar positions across images)
  - Indoor plants (fiddle leaf fig, monstera)
- **Characters** (fixed appearance across ALL images):
  - **Li Wei (销售员 / Salesperson)**: 28-year-old Chinese woman, friendly and professional. Shoulder-length straight black hair with slight waves, light makeup, warm genuine smile. Wearing: light blue collared blouse, small silver name tag "Li Wei", dark slim trousers, small pearl earrings.
  - **Mr. Zhang (顾客 / Customer)**: 35-year-old Chinese man, polite and thoughtful. Short neat black hair, light stubble. Wearing: fitted grey polo shirt or light sweater + dark chinos, brown belt, watch on left wrist.
- **Camera**: Eye-level to slightly low, 35-50mm lens feel, good depth of field, subjects occupy 40-60% of frame.
- **Composition rule**: Always show both characters in frame when dialogue happens. Salesperson on left or center-left, customer on right. Clear eye contact or gesture toward furniture.

When generating each new image:
1. Start with the full base description above.
2. Only change: specific action, exact furniture being shown, hand gestures, facial micro-expression matching the line, slight camera angle if needed for drama.
3. Never change character appearance, room architecture, or overall lighting mood.

## Audio Rules
- Clean spoken text only. Never include <|emotion:...|> or style tags in the input text sent to TTS.
- Different voices per role:
  - Salesperson (Li Wei): warm professional female voice (preset "professional_female" or closest available)
  - Customer (Mr. Zhang): clear conversational male voice (preset "jake" or "storyteller_male" or similar)
- Emotion is conveyed by delivery and prosody through the model, NOT by reading tags.
- Natural pace for language learning (not too fast).

## Subtitle & UI Rules
- High contrast: Subtitle panel has dark background (#111827 or darker), large sans-serif text.
- English in white (#FFFFFF), Chinese in light gray or soft yellow for distinction.
- Key vocabulary and sentences: Bold + amber/yellow highlight (#FCD34D or similar).
- Current line: Stronger highlight (amber background + white text).
- Speech bubble: Clean white or light card with speaker name, current spoken line (large), positioned near the image.
- Subtitle list must be vertically scrollable.
- Auto-advance lesson plays images + audio + bubbles + highlights in sequence without user clicks after "Play Lesson".
