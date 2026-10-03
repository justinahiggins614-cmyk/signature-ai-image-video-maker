# SigArt Determinism Specification — SIGART-V1

**Engine version:** SIGART-V1 (immutable — this behavior is preserved forever; changes ship as SIGART-V2).
**Engines:** `assets/engine.js` (browser) and `assets/sigart.py` (Python CLI port).
**Status:** deterministic, offline-capable, no API keys, no accounts.

## The reproducibility record

"Same prompt → same art" is defined as this exact chain:

```
ORIGINAL-PROMPT
  → NORMALIZED-PROMPT   (trim; collapse whitespace; case preserved for display,
                         lowercased for classification/guard matching)
  → TRADEMARK GUARD     (TM_BLOCK word-boundary match → replace hit with "hero";
                         recorded as ORIGINAL-PROMPT / TRADEMARK-DETECTED /
                         TRANSFORMED-PROMPT / FINAL-PROMPT)
  → SEED-STRING         = prompt + "|" + style + "|" + scene-override
  → SEED                = xfnv1a(seed-string)        (FNV-1a 32-bit)
  → RNG                 = mulberry32(seed)
  → PALETTE             = style choice, else PALETTES[seed % 12]   (SIGART-PALETTES-V1)
  → SCENE               = override, else classify(clean prompt)    (keyword count;
                         space|ocean|landscape|city|creature|object|abstract)
  → SVG                 = deterministic draw calls consuming the RNG stream
  → OUTPUT-HASH         = SHA-256 of the SVG bytes
```

"Same" is guaranteed at the level of **identical SVG bytes from the same engine +
same engine version + same settings**. Across engines (JS vs Python) the guarantee is
**identical seed + identical palette + identical scene + identical guard decision**
(visually equivalent family; drawing routines differ in detail — see parity below).

## What is NOT part of the guarantee

- PNG export: pixel-identical only given the same renderer (browser canvas vs
  Python rasterizer differ). SVG is the canonical reproducible artifact.
- Video: same prompt + settings + engine version + seed reproduces the same
  animation plan and frames on the same engine; `.webm` bytes depend on the
  browser's MediaRecorder.
- Fonts: caption text uses the system Verdana stack (`font_version:
  system-verdana-stack`); glyph shapes follow the platform.
- Llama prompt enhancement is intentionally NON-deterministic (temperature 0.7);
  the original prompt is always preserved and the enhancement source is shown.

## Versioning

- `SIGART-V1`: current. Palettes `SIGART-PALETTES-V1` (12), styles `SIGART-STYLES-V1`.
- Old engine versions remain available and reproducible; a V2 would add new
  behavior without rewriting V1 outputs.
- Every archived artwork records `engine_version`, `seed`, `seed_algorithm`,
  `palette_version`, `style_version`.

## Browser ↔ Python parity (measured 2026-10-03)

| prompt | JS seed | PY seed | palette | scene | guard |
|---|---|---|---|---|---|
| a lighthouse at dusk | A8238497 | A8238497 | Forest Dawn | object | no |
| neon fox sticker | 450B996 | 450B996 | Ocean Deep | creature | no |
| mickey mouse poster | C277C8C0 | C277C8C0 | Neon Night | creature | YES |
| grand opening sale | 81C342D1 | 81C342D1 | Desert Gold | abstract | no |

Result: **seed-identical, palette-identical, scene-identical, guard-identical**.
Both engines are self-deterministic (same input → byte-identical SVG on repeat runs).
The SVGs are not byte-identical across engines (drawing detail differs);
they are visually equivalent members of the same seed family.

Parity test: `code/qa/test_determinism.py` (runs both engines, asserts seed/palette/
scene/guard agreement on the vectors below).

## Test vectors

Each vector: prompt, style, expected seedHex, expected palette, expected scene,
expected guarded. Verified against both engines 2026-10-03.

1. `a lighthouse at dusk` / auto → seed `A8238497`, palette `Forest Dawn`, scene `object`, guarded false
2. `neon fox sticker` / auto → seed `0450B996`, palette `Ocean Deep`, scene `creature`, guarded false
3. `mickey mouse poster` / auto → seed `C277C8C0`, palette `Neon Night`, scene `creature`, guarded true (hit: mickey)
4. `grand opening sale` / auto → seed `81C342D1`, palette `Desert Gold`, scene `abstract`, guarded false

## Trademark guard (machine-readable)

Every render records: `ORIGINAL-PROMPT`, `TRADEMARK-DETECTED` (bool),
`TRANSFORMED-PROMPT` (hits replaced with "hero"), `FINAL-PROMPT` (what was drawn).
Design intent: the engine is *designed not to reproduce* trademarked characters,
logos, or brands — an abstraction renders instead, and the artwork says so.
This describes system behavior, not a legal guarantee.
