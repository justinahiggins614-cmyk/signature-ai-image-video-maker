#!/usr/bin/env python3
"""drip.py — 2h drip for Signature AI Pixel (image side).
+1,000 goods + 250 ads per run toward 1,000,000 goods. Silent unless failure.
800MB repo-size guard (sideways sharding would go here; data is tiny).
"""
import os, sys, subprocess, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
sys.path.insert(0, os.path.join(BASE, "code"))
from gen_goods import gen as gen_goods, rebuild_index as ri_goods
from gen_ads import gen as gen_ads, rebuild_index as ri_ads

GUARD = 800 * 1024 * 1024

def data_size():
    total = 0
    for dp, dn, fn in os.walk(os.path.join(BASE, "data")):
        for f in fn:
            total += os.path.getsize(os.path.join(dp, f))
    return total

def main():
    n_goods = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    n_ads = int(sys.argv[2]) if len(sys.argv) > 2 else 250
    if data_size() > GUARD:
        print("STATUS: drip paused — 800MB guard tripped", flush=True)
        sys.exit(2)
    gs, gm = gen_goods(n_goods)
    astart, am = gen_ads(n_ads)
    # rebuild sitemap + api counts
    subprocess.run([sys.executable, os.path.join(BASE, "code", "build_site_files.py")], check=False)
    subprocess.run(["git", "add", "-A"], check=False)
    st = json.load(open(os.path.join(BASE, "data", "state.json")))
    msg = f"Goods drip: +{gm} goods ({st['goods_total']} total), +{am} ads"
    r = subprocess.run(["git", "commit", "-qm", msg])
    if r.returncode == 0:
        subprocess.run(["git", "push", "-q", "origin", "main"], check=False)
    print(f"STATUS: +{gm} goods, +{am} ads | goods total {st['goods_total']}")

if __name__ == "__main__":
    main()
