#!/usr/bin/env python3
"""build_manifest.py — authoritative Pixel manifest + instant counts + QA gates.

Reads the sealed data chunks (source of truth), validates everything, then writes:
  pixel-manifest.json  — the ONE authoritative count/identity/version source
  data/counts.json     — tiny instant-load file for the homepage counters
  api.json             — regenerated from the manifest (never hand-edited)

QA gates (exit 1 on failure — the drip must not publish a broken build):
  G1 duplicate IDs          G2 ID contiguity        G3 index row agreement
  G4 manifest/index/chunk/API count agreement
  G5 chunk presence for every index row
"""
import gzip, hashlib, json, os, sys, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://justinahiggins614-cmyk.github.io/signature-ai-image-video-maker/"
ENGINE_VERSION = "SIGART-V1"
SCHEMA_VERSION = "JAH-PIXEL-RECORD/1.0"
MANIFEST_VERSION = "JAH-PIXEL-MANIFEST/1.0"
GOODS_GOAL = 1_000_000

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def read_chunks(sub):
    """id -> (record, chunkfile) for a chunk dir."""
    d = os.path.join(BASE, "data", sub)
    out = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".jsonl.gz"):
            continue
        with gzip.open(os.path.join(d, fn), "rt") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                out[r["id"]] = (r, fn)
    return out

def read_idx(name):
    p = os.path.join(BASE, "data", "index", name)
    rows = []
    with gzip.open(p, "rt") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def num_of(prefix, id_):
    return int(id_.replace(prefix, ""))

def stamp_homepage_counts(goods_total, ads_total):
    """Re-stamp the homepage count chips with real counts (idempotent)."""
    import re
    p = os.path.join(BASE, "index.html")
    t = open(p, encoding="utf-8").read()
    gf = f"{goods_total:,}"
    af = f"{ads_total:,}"
    t2, n1 = re.subn(r'<b id="cGoods">[^<]*</b>', f'<b id="cGoods">{gf}</b>', t)
    t2, n2 = re.subn(r'<b id="cAds">[^<]*</b>', f'<b id="cAds">{af}</b>', t2)
    if n1 != 1 or n2 != 1:
        print(f"COUNT-STAMP FAILED: cGoods replacements={n1}, cAds replacements={n2} (expected 1 each)",
              file=sys.stderr)
        sys.exit(1)
    if t2 != t:
        open(p, "w", encoding="utf-8").write(t2)
        print(f"stamped homepage chips: {gf} goods / {af} ads")
    else:
        print(f"homepage chips already stamped: {gf} goods / {af} ads")

def main():
    fails = []
    def gate(name, ok, detail=""):
        print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
        if not ok:
            fails.append(name)

    goods = read_chunks("goods")
    ads = read_chunks("ads")
    g_idx = read_idx("goods.idx.json.gz")
    a_idx = read_idx("ads.idx.json.gz")

    # G1: duplicate IDs — impossible via dict, but verify chunk files have no dup lines
    gate("G1 no duplicate good IDs", len(goods) == sum(
        1 for fn in sorted(os.listdir(os.path.join(BASE, "data", "goods")))
        if fn.endswith(".jsonl.gz") for _ in gzip.open(
            os.path.join(BASE, "data", "goods", fn), "rt")),
        f"{len(goods)} unique")

    # G2: contiguity JAH-GOODS-000001..N
    g_nums = sorted(num_of("JAH-GOODS-", i) for i in goods)
    a_nums = sorted(num_of("JAH-AD-", i) for i in ads)
    gate("G2 goods IDs contiguous 1..N",
         g_nums == list(range(1, len(g_nums) + 1)),
         f"1..{len(g_nums)}" if g_nums == list(range(1, len(g_nums) + 1))
         else f"break at {[n for n in range(1, len(g_nums)+1) if n not in set(g_nums)][:5]}")
    gate("G2 ads IDs contiguous 1..N",
         a_nums == list(range(1, len(a_nums) + 1)),
         f"1..{len(a_nums)}")

    # G3: index agreement
    gate("G3 goods index rows == chunk records", len(g_idx) == len(goods),
         f"idx {len(g_idx)} vs chunks {len(goods)}")
    gate("G3 ads index rows == chunk records", len(a_idx) == len(ads),
         f"idx {len(a_idx)} vs chunks {len(ads)}")

    # G5: every index row points at a real chunk file with that ID
    g_missing = [r[0] for r in g_idx if r[0] not in goods]
    a_missing = [r[0] for r in a_idx if r[0] not in ads]
    gate("G5 every goods index row resolves", not g_missing, f"{len(g_missing)} missing")
    gate("G5 every ads index row resolves", not a_missing, f"{len(a_missing)} missing")

    # categories
    cats = {}
    for _id, (r, _fn) in goods.items():
        c = r.get("cat", "misc")
        cats[c] = cats.get(c, 0) + 1

    # engine + index hashes
    eng_js = os.path.join(BASE, "assets", "engine.js")
    eng_py = os.path.join(BASE, "assets", "sigart.py")
    gidx_p = os.path.join(BASE, "data", "index", "goods.idx.json.gz")
    aidx_p = os.path.join(BASE, "data", "index", "ads.idx.json.gz")

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest = {
        "manifest_version": MANIFEST_VERSION,
        "site_id": "SIGNATURE-AI-PIXEL",
        "site_name": "Signature AI Pixel",
        "site_url": SITE,
        "canonical_url": SITE,
        "network": {"name": "THE JAH NETWORK", "site_number": 22, "site_count": 27},
        "generated_at": now,
        "counts": {
            "goods_total": len(goods),
            "goods_goal": GOODS_GOAL,
            "goods_progress": f"{len(goods)} / {GOODS_GOAL} GOODS",
            "ads_total": len(ads),
            "categories": len(cats),
            "category_counts": dict(sorted(cats.items())),
            "earliest_good_id": f"JAH-GOODS-{g_nums[0]:06d}" if g_nums else None,
            "latest_good_id": f"JAH-GOODS-{g_nums[-1]:06d}" if g_nums else None,
            "earliest_ad_id": f"JAH-AD-{a_nums[0]:06d}" if a_nums else None,
            "latest_ad_id": f"JAH-AD-{a_nums[-1]:06d}" if a_nums else None,
        },
        "identity": {
            "good_id_pattern": "JAH-GOODS-###### (contiguous from 000001, never reused)",
            "pixel_id_pattern": "JAH-PIXEL-###### (artwork identity, numerically aligned with JAH-GOODS-######)",
            "ad_id_pattern": "JAH-AD-###### (contiguous from 000001, never reused)",
            "video_id_pattern": "JAH-PIXEL-VIDEO-###### (video creative of the same-numbered JAH-AD)",
        },
        "engine": {
            "engine_version": ENGINE_VERSION,
            "schema_version": SCHEMA_VERSION,
            "js_url": SITE + "assets/engine.js",
            "js_sha256": sha256_file(eng_js),
            "py_url": SITE + "assets/sigart.py",
            "py_sha256": sha256_file(eng_py),
            "deterministic": True,
            "offline_capable": True,
            "seed_algorithm": "xfnv1a(prompt|style|scene) -> mulberry32",
            "reproducibility": "PROMPT + NORMALIZED-PROMPT + ENGINE-VERSION + STYLE-VERSION + SEED + SETTINGS => identical output",
        },
        "index": {
            "index_version": "JAH-PIXEL-INDEX/1.0",
            "goods_index": "data/index/goods.idx.json.gz",
            "goods_index_rows": len(g_idx),
            "goods_index_sha256": sha256_file(gidx_p),
            "ads_index": "data/index/ads.idx.json.gz",
            "ads_index_rows": len(a_idx),
            "ads_index_sha256": sha256_file(aidx_p),
        },
        "deep_links": {
            "goods": SITE + "?goods=JAH-GOODS-000001",
            "pixel": SITE + "?pixel=JAH-PIXEL-000001",
            "ad": SITE + "?ad=JAH-AD-000001",
            "catalog": SITE + "goods-catalog.html",
            "feed": SITE + "data/pixel-catalog.json",
        },
        "honesty": {
            "free_and_unlimited": "image/video GENERATION is free and unlimited; archive STORAGE is bounded by the catalog",
            "mockup_vs_manufactured": "goods are DESIGN MOCKUPS (printable design mockups), not physically manufactured products",
            "commerce": "product ads are creative records; an ad does not mean a product is manufactured, stocked, or for sale",
            "trademark": "engine is designed not to reproduce trademarked characters/logos/brands (abstraction, not a legal guarantee)",
        },
        "qa": {"gates": "G1..G5", "status": "PASS" if not fails else "FAIL",
               "failed": fails},
    }

    # G4: cross-source agreement (state files vs chunk scan)
    st = json.load(open(os.path.join(BASE, "data", "state.json")))
    ast = json.load(open(os.path.join(BASE, "data", "ads_state.json")))
    gate("G4 state.json agrees with chunk scan",
         st.get("goods_total") == len(goods), f"state {st.get('goods_total')} vs {len(goods)}")
    gate("G4 ads_state.json agrees with chunk scan",
         ast.get("ads_total") == len(ads), f"state {ast.get('ads_total')} vs {len(ads)}")

    if fails:
        print("MANIFEST NOT WRITTEN — gates failed")
        return 1

    with open(os.path.join(BASE, "pixel-manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    counts = {
        "generated_at": now,
        "goods_total": len(goods),
        "goods_goal": GOODS_GOAL,
        "ads_total": len(ads),
        "manifest": "pixel-manifest.json",
        "manifest_sha256": sha256_file(os.path.join(BASE, "pixel-manifest.json")),
    }
    with open(os.path.join(BASE, "data", "counts.json"), "w") as f:
        json.dump(counts, f, indent=1)
    # G6 universal loading pattern: stamp the last-known real counts into the raw
    # HTML chips (never bare "…" on first paint); the drip re-stamps every run,
    # and the page JS overwrites these live once data/counts.json loads.
    stamp_homepage_counts(len(goods), len(ads))
    api = {
        "site": "Signature AI Pixel",
        "site_url": SITE,
        "free_and_unlimited": True,
        "goods_total": len(goods),
        "goods_goal": GOODS_GOAL,
        "ads_total": len(ads),
        "manifest": SITE + "pixel-manifest.json",
        "engine": {"js": SITE + "assets/engine.js", "py": SITE + "assets/sigart.py",
                   "version": ENGINE_VERSION, "deterministic": True,
                   "offline_capable": True},
        "deep_links": manifest["deep_links"],
        "network": "THE JAH NETWORK — 27 sites",
    }
    with open(os.path.join(BASE, "api.json"), "w") as f:
        json.dump(api, f, indent=1)
    print(f"wrote pixel-manifest.json + data/counts.json + api.json "
          f"({len(goods)} goods, {len(ads)} ads)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
