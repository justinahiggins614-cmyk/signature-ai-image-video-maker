# The Signature AI Image And Video Maker

**FREE AND UNLIMITED** AI image + video generation — site 24 of THE JAH NETWORK.

Live: https://justinahiggins614-cmyk.github.io/signature-ai-image-video-maker/

## What it is
- **Image Studio** — type a prompt, get a finished 1200×800 original artwork (deterministic seeded SVG composition). Download SVG/PNG, copy settings, read-aloud description.
- **Video Studio** — type a prompt, get a live canvas animation preview (3/6/10s @ 15fps), export a real `.webm`.
- **Powered by his AI** — prompt enhancement goes through Signature Llama (loaded live from the Signature Backend) with quiet deterministic on-device fallback; the page says which path was used.
- **Take the AI** — the whole generator is two files (`assets/engine.js`, `assets/sigart.py`), downloadable/copyable, offline, no keys.
- **Goods Catalog** — JAH-GOODS-###### records marching to 1,000,000 across 24 product categories (posters, stickers, shirts, surfboards…), each with a deterministic design mockup.
- **Product Ads** — JAH-AD-###### records auto-made for products across the Signature network (mall, books, comics), each with image + video creative, stored as made.

## Data layout
- `data/state.json` — goods next_index/total
- `data/ads_state.json` — ads next_index/total + product rotation cursor
- `data/goods/cNNNN.jsonl.gz` — 250 goods/chunk
- `data/ads/cNNNN.jsonl.gz` — 250 ads/chunk
- `data/index/goods.idx.json.gz` / `ads.idx.json.gz` — compact search indexes

## Drip
`python3 code/drip.py [n_goods=1000] [n_ads=250]` — every 2h via `jah-imagevideo-drip` cron (silent). 800MB guard.

## Honesty notes
- All art is original and deterministic; nothing reproduces trademarked characters/logos/brands — trademarked prompt terms render as original Signature-style abstractions, disclosed on the provenance line.
- "Free and unlimited" applies to this generator. Llama copy follows the house rule ("currently free for all internet tasks").
