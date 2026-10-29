# WifEnglish Agent Notes

## Voice Consistency Is Mandatory

For dialogue lesson audio, always use reusable Boson custom voices through:

```bash
python3 scripts/generate_lesson_audio_ref.py --lesson-number 01 --force
```

or for every configured lesson:

```bash
python3 scripts/generate_lesson_audio_ref.py --all --force
```

Do not use `scripts/generate_lesson_audio.py` or `scripts/tts_boson.py` for final
dialogue lesson audio where the same speaker must remain consistent across lines.
Those helpers are only for one-off clips or legacy assets.

## Environment And Secrets

- Read `BOSON_API_KEY` from the project-root `.env.local`; the scripts load it automatically.
- Never hardcode API keys in source files, README examples, generated logs, or conversation transcript files.
- `audio/voices.json` is a local cache of reusable Boson voice IDs and must stay untracked.

## Required Workflow

1. Keep reference audio and transcript aligned:
   - `audio/ref_liwei.mp3` -> `"Hello, welcome to our showroom. My name is Li Wei."`
   - `audio/ref_zhang.mp3` -> `"Hi, I'm looking for a sofa set for my new apartment."`
2. Generate lesson audio with `scripts/generate_lesson_audio_ref.py`.
3. Sync generated files to the matching `web/audio/lessonXX` directory.
4. Run status/verification before reporting completion:

```bash
python3 scripts/generate_lesson_audio_ref.py --all --status
python3 scripts/generate_lesson_audio_ref.py --all --verify-web
```

The expected result is no missing files, no suspicious tiny files, and source/web
audio files matching byte-for-byte.
