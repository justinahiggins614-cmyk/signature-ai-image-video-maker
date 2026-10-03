#!/usr/bin/env python3
"""gen_goods.py — generate JAH-GOODS-###### records for the goods catalog.
Deterministic: same index => same good, forever. Goods never regenerated.
"""
import json, gzip, os, sys, hashlib, random

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
CHUNK = 250

CATS = [
    "room poster", "sticker", "t-shirt", "number sticker", "surfboard", "mug",
    "phone case", "hat", "banner", "tote bag", "hoodie", "mousepad",
    "notebook", "flag", "wall decal", "keychain", "water bottle", "backpack",
    "calendar", "puzzle", "lunchbox", "beach towel", "socks", "playing cards",
]

ADJ = ["Neon", "Cosmic", "Ember", "Tidal", "Solar", "Lunar", "Crimson", "Azure",
       "Golden", "Violet", "Thunder", "Silent", "Blazing", "Frozen", "Radiant",
       "Mystic", "Iron", "Velvet", "Storm", "Drift", "Nova", "Echo", "Prime", "Wild"]
NOUN = ["Horizon", "Voyager", "Falcon", "Comet", "Reef", "Summit", "Drift",
        "Beacon", "Surge", "Meadow", "Canyon", "Harbor", "Zephyr", "Onyx",
        "Pioneer", "Ranger", "Sable", "Talon", "Vista", "Warden", "Yonder", "Bolt"]

PALETTES = ["Neon Night", "Sunset Ember", "Ocean Deep", "Forest Dawn", "Cosmic Violet",
            "Desert Gold", "Arctic Mint", "Crimson Pulse", "Royal Indigo",
            "Meadow Pastel", "Mono Ink", "Candy Pop"]
SCENES = ["space", "ocean", "landscape", "city", "creature", "object", "abstract"]

DESC_T = [
    "A {adj} {noun} design rendered as a {cat} — original Signature generative art, ready to print.",
    "Signature-line {cat} artwork: {adj} {noun}, composed by the deterministic SigArt engine.",
    "Wear it, hang it, gift it — {adj} {noun} as a premium {cat} design, free and unlimited.",
]

def rng_for(idx):
    h = int(hashlib.sha256(f"goods:{idx}".encode()).hexdigest()[:16], 16)
    return random.Random(h)

def make_good(idx):
    r = rng_for(idx)
    cat = CATS[idx % len(CATS)]
    adj, noun = r.choice(ADJ), r.choice(NOUN)
    name = f"{adj} {noun} {cat.title()}"
    prompt = f"{adj.lower()} {noun.lower()} {cat} artwork"
    return {
        "id": f"JAH-GOODS-{idx:06d}",
        "name": name,
        "cat": cat,
        "desc": r.choice(DESC_T).format(adj=adj, noun=noun, cat=cat),
        "prompt": prompt,
        "seed": int(hashlib.sha256(f"art:{prompt}".encode()).hexdigest()[:8], 16),
        "palette": PALETTES[int(hashlib.sha256(f"pal:{idx}".encode()).hexdigest()[:8], 16) % len(PALETTES)],
        "scene": SCENES[int(hashlib.sha256(f"scn:{idx}".encode()).hexdigest()[:8], 16) % len(SCENES)],
        "kw": [adj.lower(), noun.lower(), cat],
        "good_status": "DESIGN MOCKUP",
        "mockup_note": "A generated design mockup, not a physically manufactured product.",
    }

def state():
    p = os.path.join(DATA, "state.json")
    if os.path.exists(p):
        return json.load(open(p))
    return {"next_index": 1, "goods_total": 0}

def save_state(s):
    json.dump(s, open(os.path.join(DATA, "state.json"), "w"), indent=1)

def chunk_path(n):
    d = os.path.join(DATA, "goods")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"c{n:04d}.jsonl.gz")

def gen(n):
    s = state()
    start = s["next_index"]
    made = 0
    buf = []
    for idx in range(start, start + n):
        buf.append(make_good(idx))
        made += 1
        if len(buf) >= CHUNK:
            cn = (idx - 1) // CHUNK + 1
            p = chunk_path(cn)
            mode = "at" if os.path.exists(p) else "wt"
            with gzip.open(p, mode) as f:
                for g in buf:
                    f.write(json.dumps(g) + "\n")
            buf = []
    if buf:
        cn = (start + n - 1) // CHUNK + 1
        p = chunk_path(cn)
        mode = "at" if os.path.exists(p) else "wt"
        with gzip.open(p, mode) as f:
            for g in buf:
                f.write(json.dumps(g) + "\n")
    s["next_index"] = start + n
    s["goods_total"] = s.get("goods_total", 0) + n
    save_state(s)
    rebuild_index()
    return start, n

def rebuild_index():
    idx_dir = os.path.join(DATA, "index")
    os.makedirs(idx_dir, exist_ok=True)
    rows = []
    d = os.path.join(DATA, "goods")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".jsonl.gz"):
                continue
            with gzip.open(os.path.join(d, fn), "rt") as f:
                for line in f:
                    g = json.loads(line)
                    rows.append([g["id"], g["name"], g["cat"], fn])
    with gzip.open(os.path.join(idx_dir, "goods.idx.json.gz"), "wt") as f:
        for r_ in rows:
            f.write(json.dumps(r_) + "\n")
    return len(rows)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    start, made = gen(n)
    print(f"+{made} goods (JAH-GOODS-{start:06d}..JAH-GOODS-{start+made-1:06d})")
