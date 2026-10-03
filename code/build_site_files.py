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

def esc_h(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

def all_goods_rows():
    """Full good records (id, name, cat, desc) for feed + static catalog."""
    rows = []
    d = os.path.join(BASE, "data", "goods")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".jsonl.gz"):
                with gzip.open(os.path.join(d, fn), "rt") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            g = json.loads(line)
                            rows.append((g.get("id", ""), g.get("name", ""),
                                         g.get("cat", ""), g.get("desc", "")))
    return rows

def write_catalog_feed(goods, ads):
    """data/pixel-catalog.json — standardized machine-readable feed (AI-USER FIX-02)."""
    import time
    feed = {
        "site": "Signature AI Pixel",
        "site_url": SITE,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "goods_total": len(goods),
        "goods_goal": 1000000,
        "deep_link_pattern": SITE + "?goods={id}",
        "goods": [{"id": i, "name": n, "type": c, "description": d,
                   "url": SITE + "?goods=" + i} for (i, n, c, d) in goods],
        "ads_total": len(ads),
        "ads": [{"id": a, "url": SITE + "?ad=" + a} for a in ads],
        "network": "THE JAH NETWORK — 25 sites",
    }
    p = os.path.join(BASE, "data", "pixel-catalog.json")
    with open(p, "w") as f:
        json.dump(feed, f, separators=(",", ":"))
    print(f"feed: {p} ({len(goods)} goods, {len(ads)} ads)")

def write_goods_catalog_html(goods):
    """goods-catalog.html — pre-rendered static tables for non-JS crawlers (AI-USER FIX-03)."""
    cats = {}
    for (i, n, c, d) in goods:
        cats.setdefault(c or "misc", []).append((i, n, d))
    parts = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Signature AI Pixel — Goods Catalog (static index)</title>',
             '<meta name="description" content="Static index of every Signature AI Pixel good: ID, type and description.">',
             f'<link rel="canonical" href="{SITE}goods-catalog.html">',
             '<style>body{background:#0a0618;color:#f2ecff;font-family:Verdana,system-ui,sans-serif;'
             'margin:0;padding:24px;max-width:1100px}a{color:#00f0ff}h1{font-size:26px}'
             'h2{margin-top:34px;color:#ffd166}table{width:100%;border-collapse:collapse;font-size:13px}'
             'th,td{border:1px solid #3a2568;padding:8px 10px;text-align:left;vertical-align:top}'
             'th{background:#1a1038}td.id{white-space:nowrap;color:#b9a8e0}</style></head><body>',
             '<h1>Signature AI Pixel — Goods Catalog (static index)</h1>',
             f'<p>{len(goods)} goods · static index for crawlers and non-JS readers. '
             f'Interactive catalog: <a href="{SITE}?tab=goods">Goods Catalog</a> · '
             f'Machine feed: <a href="{SITE}data/pixel-catalog.json">pixel-catalog.json</a></p>']
    for c in sorted(cats):
        rows = cats[c]
        parts.append(f'<h2 id="{esc_h(c)}">{esc_h(c)} ({len(rows)})</h2>')
        parts.append('<table><tr><th>ID</th><th>Name</th><th>Description</th></tr>')
        for (i, n, d) in rows:
            parts.append(f'<tr><td class="id"><a href="{SITE}?goods={esc_h(i)}">{esc_h(i)}</a></td>'
                         f'<td>{esc_h(n)}</td><td>{esc_h(d)}</td></tr>')
        parts.append('</table>')
    parts.append('</body></html>')
    p = os.path.join(BASE, "goods-catalog.html")
    with open(p, "w") as f:
        f.write("\n".join(parts))
    print(f"static catalog: {p} ({len(goods)} rows, {len(cats)} categories)")

def main():
    goods = goods_ids()
    ads = ads_ids()
    pages = [SITE, SITE + "?tab=image", SITE + "?tab=video", SITE + "?tab=goods",
             SITE + "?tab=ads", SITE + "?tab=take", SITE + "goods-catalog.html"]
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
        "site": "Signature AI Pixel",
        "site_url": SITE,
        "free_and_unlimited": True,
        "goods_total": st.get("goods_total", 0),
        "goods_goal": 1000000,
        "ads_total": ast.get("ads_total", 0),
        "engine": {"js": SITE + "assets/engine.js", "py": SITE + "assets/sigart.py",
                   "deterministic": True, "offline_capable": True},
        "deep_links": {"goods": SITE + "?goods=JAH-GOODS-000001", "ad": SITE + "?ad=JAH-AD-000001"},
        "network": "THE JAH NETWORK — 25 sites",
    }
    json.dump(api, open(os.path.join(BASE, "api.json"), "w"), indent=1)
    print(f"sitemap: {len(pages)} pages + {len(goods)} goods + {len(ads)} ads | api.json written")
    # FIX-02/FIX-03: standardized JSON feed + static HTML catalog (kept fresh by every drip run)
    rows = all_goods_rows()
    write_catalog_feed(rows, ads)
    write_goods_catalog_html(rows)

if __name__ == "__main__":
    main()
