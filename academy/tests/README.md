# Module 1 QA reproduction

Run from repository root. Python 3 with BeautifulSoup4 supports remediation; static checks use the standard library. Browser tests need Node.js, Playwright and axe-core. No production deployment is performed by these scripts.

- `node validate-site.cjs`
- `python academy/tests/module1-static.py`
- `AXE_PATH=/path/to/axe.min.js CHROME_PATH=/path/to/chromium MEDIA_DIR=/path/to/downloaded-media node academy/tests/module1-browser.cjs`

The browser harness serves local repository bytes through Playwright routes at `http://academy.test`; it does **not** test deployed HTTP headers/CDN behavior. Downloaded files are named `lesson-1.mp4` through `lesson-10.mp4` and mapped only inside the test harness.

This execution used Chromium headless shell 134.0.6998.35 and axe-core 4.10.3. Its `canPlayType` response for H.264/AAC MP4 was empty, while VP8/Vorbis WebM returned `probably`. Original-media browser results retain these failures. To isolate player JavaScript from this codec limitation, a separate run used a synthetic 600-second black VP8 video, generated with:

```sh
ffmpeg -f lavfi -i color=c=black:s=160x90:r=1:d=600 -c:v libvpx -b:v 20k player-fixture.webm
```

Set `MEDIA_FIXTURE=/path/to/player-fixture.webm` to run that isolated test. The separate `browser-fixture-results.json` file explicitly records synthetic media. Never describe it as playback/synchronization verification of the real MP4s.

`transcribe-media.py` uses faster-whisper base.en, CPU int8, beam size 5 and word timestamps. This run used av 16.1.0; audio is 16 kHz mono WAV. Set `MEDIA_DIR` for the downloaded/decoded media directory. All ten resulting ASR word/segment JSON files are retained in the evidence folder.

`remediate-captions.py` reads the retained original captions and ASR evidence, then updates VTT, embedded fallback cues and transcripts. It uses matched word boundaries for long-cue splitting and Lesson 1.1 timing correction, avoiding blind ASR text replacement. It is a remediation utility, not a test or evidence of human synchronization acceptance. Inspect its diff before use on future edited content.
