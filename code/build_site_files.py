#!/usr/bin/env python3
"""build_site_files.py — rebuild sitemap.xml, api.json from data state."""
import json, os, gzip

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://justinahiggins614-cmyk.github.io/signature-ai-image-video-maker/"
MAXURL = 45000

def goods_ids():
    ids = []
    d = os.path.join(BASE, "data", "goods")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".jsonl.gz"):
                with gzip.open(os.path.join(d, fn), "rt") as f:
                    for line in f:
                        ids.append(json.loads(line)["id"])
    return ids

def ads_ids():
    ids = []
    d = os.path.join(BASE, "data", "ads")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".jsonl.gz"):
                with gzip.open(os.path.join(d, fn), "rt") as f:
                    for line in f:
                        ids.append(json.loads(line)["id"])
    return ids

def write_sitemap(urls, path):
    with open(path, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"<url><loc>{u}</loc></url>\n")
        f.write("</urlset>\n")

def main():
    goods = goods_ids()
    ads = ads_ids()
    pages = [SITE, SITE + "?tab=image", SITE + "?tab=video", SITE + "?tab=goods",
             SITE + "?tab=ads", SITE + "?tab=take"]
    # goods sitemaps, chunked
    sm_files = ["sitemap-pages.xml"]
    write_sitemap(pages, os.path.join(BASE, "sitemap-pages.xml"))
    for i in range(0, len(goods), MAXURL):
        name = f"sitemap-goods-{i//MAXURL+1}.xml"
        write_sitemap([SITE + f"?goods={g}" for g in goods[i:i+MAXURL]], os.path.join(BASE, name))
        sm_files.append(name)
    for i in range(0, len(ads), MAXURL):
        name = f"sitemap-ads-{i//MAXURL+1}.xml"
        write_sitemap([SITE + f"?ad={a}" for a in ads[i:i+MAXURL]], os.path.join(BASE, name))
        sm_files.append(name)
    with open(os.path.join(BASE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for s in sm_files:
            f.write(f"<sitemap><loc>{SITE}{s}</loc></sitemap>\n")
        f.write("</sitemapindex>\n")
    with open(os.path.join(BASE, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    st = json.load(open(os.path.join(BASE, "data", "state.json"))) if os.path.exists(os.path.join(BASE, "data", "state.json")) else {"goods_total": 0}
    ast = json.load(open(os.path.join(BASE, "data", "ads_state.json"))) if os.path.exists(os.path.join(BASE, "data", "ads_state.json")) else {"ads_total": 0}
    api = {
        "site": "The Signature AI Image And Video Maker",
        "site_url": SITE,
        "free_and_unlimited": True,
        "goods_total": st.get("goods_total", 0),
        "goods_goal": 1000000,
        "ads_total": ast.get("ads_total", 0),
        "engine": {"js": SITE + "assets/engine.js", "py": SITE + "assets/sigart.py",
                   "deterministic": True, "offline_capable": True},
        "deep_links": {"goods": SITE + "?goods=JAH-GOODS-000001", "ad": SITE + "?ad=JAH-AD-000001"},
        "network": "THE JAH NETWORK — 24 sites",
    }
    json.dump(api, open(os.path.join(BASE, "api.json"), "w"), indent=1)
    print(f"sitemap: {len(pages)} pages + {len(goods)} goods + {len(ads)} ads | api.json written")

if __name__ == "__main__":
    main()
