# AI Studio request queue

This is where real AI image/video requests live.

**How a request flows (honest version — this site is static, so there is no server):**

1. The visitor fills in the form on `generate.html` (prompt, image/video, style, aspect ratio, variations).
2. The page opens a pre-filled **GitHub issue** on this repo with the label `gen-request`.
   The issue body carries the request in a fixed machine-readable format:
   `PROMPT:`, `TYPE:`, `STYLE:`, `ASPECT:`, `DURATION:`, `VARIATIONS:`.
3. Every ~30 minutes the `jah-pixel-ai-studio` worker reads all open `gen-request`
   issues (oldest first) and generates each one with a real image/video model —
   photorealistic images, movie-quality video. No procedural art is ever passed
   off as AI generation.
4. The finished file lands in `gallery/ai-studio/JAH-GEN-######.{webp,mp4}` and is
   recorded in `data/ai-gallery.json` (the on-site "Made by your AI" gallery) with
   its prompt, style, "made by your AI" attribution, and download links.
5. The worker comments the gallery link on the issue and closes it.

**Files here:**
- `state.json` — next JAH-GEN ID counter (worker increments, never reuses).
- `JAH-GEN-######.json` — one fulfilled-request record per finished piece
  (prompt, settings, issue number, file path, timestamp).

Growth is sideways: finished media stays in `gallery/ai-studio/`; records stay tiny.
Never delete fulfilled records.
