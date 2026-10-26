# Recovered media source — 26 October 2026

These scripts were recovered from the existing Higgsfield media workspace. They are historical production evidence, not a clean, portable build system. Absolute `/home/user` paths refer to that workspace. Model weights, voice vectors, original per-scene WAVs and intermediate images are not redistributed in this repository.

`rebuild.py` records the exact two-scene correction procedure used for Lessons 1.4 and 1.5. It reuses original per-scene audio except for scene 8 of Lesson 1.4 and scene 3 of Lesson 1.5, synthesizes those scenes with Kokoro `af_heart`, speed 0.95, `en-us`, then renders the original diagram images with the revised durations. Output files in `assets/academy` are the review artifacts. The original scripts remain unchanged as evidence.

Observed model SHA-256: `7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5` (`kokoro-v1.0.onnx`). Voice archive SHA-256: `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d` (`voices-v1.0.bin`). These identify the observed local files; they are not asserted to be independently verified upstream release checksums.

The [Kokoro publisher model card](https://huggingface.co/hexgrad/Kokoro-82M) and [voice directory](https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices) identify Apache-2.0 licensing and the stock `af_heart` voice. [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx/blob/main/LICENSE) uses the MIT licence. Render scripts draw diagrams with Pillow and use DejaVu Sans/DejaVu Sans Bold. The font notice is retained at `assets/academy/dejavu-font-notice.txt`; see the [official font licence](https://dejavu-fonts.github.io/License.html).

No custom voice cloning, paid voice-generation API or added music was used for this correction. Source inspection reveals no music input in these render paths. That is evidence of the build inputs, not a legal warranty about all upstream training data or every historical asset.

`recovered-source-matches.json` links nine original MP4s to exact recovered file hashes. Lesson 1.1's whole-video hash differs from the recovered `premium_full/full.mp4`, but their decoded mono 16-kHz signed-16-bit PCM hashes both equal `6672cd6bb55857f0b3f4a67aba97174cf7db56e272ca87dd8da999c478d29279`. This establishes the audio match; it does not establish an exact match for the final Lesson 1.1 visual assembly.

## Final Lesson 1.1 assembly recovered

The missing final visual assembly was subsequently located at `fast_reveal/final.mp4`. Its SHA-256 is `7c23b00967139ce5c499eb1f37ec26cfde2a45501d8352c231fa076700dddf9d`, exactly matching the published original and the new repository copy. The final assembly chain is `make_lesson.py` → `premium_full.py` → `visual_enhanced.py` → `animate_align.py` → `rebuild_fast_reveal.py`. The three additional scripts are retained here. They programmatically draw the visual panels, create staged reveal frames, reuse the original Kokoro audio and assemble 36 encoded segments. The final script makes the complete diagram visible within approximately 1.7 seconds and masks the former burned-in explanation strip. No new stock-image or music input appears in that chain.

This supersedes the earlier statement that the final Lesson 1.1 visual assembly was unidentified. All ten original lesson videos now have exact recovered-render matches. Provenance matching is technical evidence, not independent legal clearance or an assertion of exclusive copyright in generated output.
