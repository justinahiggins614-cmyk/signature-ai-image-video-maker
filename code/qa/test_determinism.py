#!/usr/bin/env python3
"""test_determinism.py — QA gate: SigArt determinism + JS/PY parity.

Asserts on the published test vectors (docs/DETERMINISM.md):
  - Python engine self-deterministic (repeat => identical SVG)
  - Python seed/palette/scene/guarded match the vectors
  - Node engine agrees with Python on seed/palette/scene/guarded
Exit 0 = all pass, 1 = any failure.
"""
import json, subprocess, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE, "assets"))
import sigart

VECTORS = [
    # prompt, style, seedHex, palette, scene, guarded
    ("a lighthouse at dusk", "auto", "A8238497", "Forest Dawn", "object", False),
    ("neon fox sticker", "auto", "0450B996", "Ocean Deep", "creature", False),
    ("mickey mouse poster", "auto", "C277C8C0", "Neon Night", "creature", True),
    ("grand opening sale", "auto", "81C342D1", "Desert Gold", "abstract", False),
]

fails = []

def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not cond:
        fails.append(name)

# 1. Python self-determinism + vector agreement
for prompt, style, seed_hex, palette, scene, guarded in VECTORS:
    s1, m1 = sigart.compose(prompt, style=style)
    s2, m2 = sigart.compose(prompt, style=style)
    check(f"py self-deterministic [{prompt[:24]}]", s1 == s2)
    check(f"py seed [{prompt[:24]}]", m1["seedHex"] == seed_hex,
          f"{m1['seedHex']} vs {seed_hex}")
    check(f"py palette [{prompt[:24]}]", m1["palette"] == palette)
    check(f"py scene [{prompt[:24]}]", m1["scene"] == scene)
    check(f"py guard [{prompt[:24]}]", m1["guarded"] == guarded)

# 2. Node parity
node_script = """
const SigArt = require(%s);
const out = %s.map(([p, st]) => {
  const a = SigArt.composeImage(p, {style: st});
  return {seed: a.seedHex, palette: a.palette, scene: a.scene, guarded: !!a.guarded};
});
console.log(JSON.stringify(out));
""" % (json.dumps(os.path.join(BASE, "assets", "engine.js")),
       json.dumps([[v[0], v[1]] for v in VECTORS]))
try:
    r = subprocess.run(["node", "-e", node_script], capture_output=True, text=True,
                       timeout=60)
    js = json.loads(r.stdout)
    for (prompt, _st, seed_hex, palette, scene, guarded), j in zip(VECTORS, js):
        check(f"js==py seed [{prompt[:24]}]", j["seed"] == seed_hex,
              f"js {j['seed']} vs {seed_hex}")
        check(f"js==py palette [{prompt[:24]}]", j["palette"] == palette,
              f"js {j['palette']} vs {palette}")
        check(f"js==py scene [{prompt[:24]}]", j["scene"] == scene)
        check(f"js==py guard [{prompt[:24]}]", j["guarded"] == guarded)
except Exception as e:
    check("node parity ran", False, str(e))

print("DETERMINISM: " + ("ALL PASS" if not fails else f"{len(fails)} FAILURES"))
sys.exit(1 if fails else 0)
