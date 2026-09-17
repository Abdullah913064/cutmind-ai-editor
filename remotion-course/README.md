# Algebra from Zero to Confidence — semantic video renderer

This is **not a slide/explainer template**. Narration is split into semantic speech chunks first. Every speech chunk receives a visual key, is synthesized separately, and its measured audio duration becomes the video timing. The result is audio-first synchronization: when the narration reaches an object or operation, the corresponding object/animation begins on that chunk boundary.

## Course
- 1920×1080, 30fps
- 10 modules, 60 scenes
- ~62 minutes using the current narration
- 820 semantic speech/visual chunks in the fallback manifest
- every practice scene contains a real 20-second silent solve period before the answer
- object-based visuals: boxes, jerseys, bills/taxi/rates, fruit/like terms, balance scales, teams/brackets, fractions, word-to-equation translation, money, graphs, cricket/shop workflow

## Audio-first render flow
1. `scripts/build_manifest.py` parses the full course and creates a fallback semantic timeline.
2. `scripts/generate_audio.py` uses Kokoro (`af_heart` by default) to synthesize each semantic chunk separately.
3. The script measures the *real* duration of every generated chunk and rewrites `src/generatedManifest.ts`.
4. `SemanticScene` reads the active audio segment at the current frame and displays the matching visual.
5. Remotion renders each scene/chapter using those exact timings.

This avoids guessing timestamps after TTS generation and avoids a slideshow timeline.

## Local setup
```bash
npm install
python -m pip install 'kokoro>=0.9.4' soundfile numpy
sudo apt-get install ffmpeg espeak-ng libsndfile1   # Linux
```

Generate all narration:
```bash
npm run audio
```

Preview:
```bash
npm start
```

Render the whole course:
```bash
npm run render:video
```

For development, generate/render just Module 1:
```bash
python scripts/generate_audio.py --chapter 1
npm run render:chapter1
```

## Important files
- `scripts/course_content.py` — source-of-truth for all 10 modules and narration templates
- `src/generatedManifest.ts` — semantic visual timeline; overwritten with measured audio timings after TTS
- `src/Scene.tsx` — semantic animation system
- `src/Course.tsx` — scene/audio sequencing
- `scripts/generate_audio.py` — narration generation + exact sync manifest
