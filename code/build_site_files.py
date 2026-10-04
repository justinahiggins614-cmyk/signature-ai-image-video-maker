#!/usr/bin/env python3
"""build_site_files.py — rebuild sitemap.xml, api.json from data state."""
import json, os, re, gzip, sys
from datetime import date
try:
    from zoneinfo import ZoneInfo
    LOCAL = ZoneInfo("America/New_York")
except Exception:
    LOCAL = None

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://justinahiggins614-cmyk.github.io/signature-ai-image-video-maker/"
MAXURL = 45000

def local_today():
    if LOCAL:
        from datetime import datetime
        return datetime.now(LOCAL).date().isoformat()
    return date.today().isoformat()

def cat_slug(cat):
    return re.sub(r"[^a-z0-9]+", "-", (cat or "misc").lower()).strip("-") or "misc"

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
        "network": "THE JAH NETWORK — 27 sites",
    }
    p = os.path.join(BASE, "data", "pixel-catalog.json")
    with open(p, "w") as f:
        json.dump(feed, f, separators=(",", ":"))
    print(f"feed: {p} ({len(goods)} goods, {len(ads)} ads)")

def write_goods_cat_files(cats):
    """data/goods-cat/<slug>.json.gz — per-category compact rows [id,name,desc],
    fetched lazily by goods-catalog.html (never load all at once)."""
    d = os.path.join(BASE, "data", "goods-cat")
    os.makedirs(d, exist_ok=True)
    for c, rows in cats.items():
        rows_sorted = sorted(rows, key=lambda r: (r[1] or "").lower())
        p = os.path.join(d, cat_slug(c) + ".json.gz")
        with gzip.open(p, "wt", encoding="utf-8") as f:
            json.dump([[i, n, ds] for (i, n, ds) in rows_sorted], f,
                      separators=(",", ":"))
    print(f"category lazy files: {d} ({len(cats)} categories)")

def write_goods_catalog_html(goods, ads, goods_total, ads_total):
    """goods-catalog.html — the full A–Z goods archive (Manon's network-wide order):
    per-category collapsible <details> with A–Z letter sub-lists, lazily loaded
    from data/goods-cat/*.json.gz; client-side search over data/index/goods.idx.json.gz;
    count header stamped from data/state.json + data/ads_state.json (fail loud on mismatch)."""
    assert len(goods) == goods_total, f"scan {len(goods)} != state goods_total {goods_total}"
    assert len(ads) == ads_total, f"scan {len(ads)} != state ads_total {ads_total}"
    cats = {}
    for (i, n, c, d) in goods:
        cats.setdefault(c or "misc", []).append((i, n, d))
    ncat = len(cats)
    today = local_today()
    cat_details = []
    for c in sorted(cats):
        n = len(cats[c])
        cat_details.append(
            f'<details class="cat" data-slug="{esc_h(cat_slug(c))}">'
            f'<summary><b>{esc_h(c)}</b> <span class="n">{n:,} goods — tap to browse A–Z</span></summary>'
            f'<div class="catbody"><p class="loading">Loading {esc_h(c)} goods…</p></div></details>')
    js = '''
(function(){
var SITE=%%SITEJS%%, loaded={}, searching=false, sidx=null;
function gz(path){return fetch(path).then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r;})
 .then(function(r){return new Response(r.body.pipeThrough(new DecompressionStream("gzip"))).text();});}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function letterOf(name){var ch=(name||"?").charAt(0).toUpperCase();return (ch>="A"&&ch<="Z")?ch:"#";}
function renderCat(det,rows){
  var by={};rows.forEach(function(r){var L=letterOf(r[1]);(by[L]=by[L]||[]).push(r);});
  var letters=Object.keys(by).sort(function(a,b){if(a==="#")return 1;if(b==="#")return -1;return a<b?-1:1;});
  var html="";
  letters.forEach(function(L){
    html+='<details class="let"><summary><b>'+L+'</b> <span class="n">'+by[L].length+' goods</span></summary><ul>';
    by[L].forEach(function(r){
      html+='<li><a href="'+SITE+'?goods='+encodeURIComponent(r[0])+'"><b>'+esc(r[0])+'</b></a> '
        +'<span class="gname">'+esc(r[1])+'</span>'
        +'<span class="gdesc">'+esc(r[2])+' — DESIGN MOCKUP</span></li>';
    });
    html+='</ul></details>';
  });
  det.querySelector(".catbody").innerHTML=html||"<p>No goods in this category yet.</p>";
}
document.querySelectorAll("details.cat").forEach(function(det){
  det.addEventListener("toggle",function(){
    if(!det.open||loaded[det.dataset.slug])return;
    loaded[det.dataset.slug]=true;
    var body=det.querySelector(".catbody");
    if(typeof DecompressionStream==="undefined"){body.innerHTML="<p>Your browser can't unzip the catalog data. Try Chrome or Edge.</p>";return;}
    gz("data/goods-cat/"+det.dataset.slug+".json.gz").then(function(t){
      renderCat(det,JSON.parse(t));
    }).catch(function(e){body.innerHTML="<p>Couldn't load this category ("+esc(e.message)+"). Try again.</p>";loaded[det.dataset.slug]=false;});
  });
});
var box=document.getElementById("q"),res=document.getElementById("results");
function ensureIdx(){if(searching||sidx)return Promise.resolve();
  searching=true;
  if(typeof DecompressionStream==="undefined"){res.innerHTML="<p>Search needs a modern browser (Chrome/Edge).</p>";return Promise.resolve();}
  res.innerHTML="<p>Loading search index…</p>";
  return gz("data/index/goods.idx.json.gz").then(function(t){
    sidx=t.trim().split("\\n").map(JSON.parse);searching=false;
  }).catch(function(){res.innerHTML="<p>Couldn't load the search index.</p>";searching=false;});}
box.addEventListener("input",function(){
  var q=box.value.trim().toLowerCase();
  if(q.length<2){res.innerHTML="";return;}
  ensureIdx().then(function(){
    if(!sidx)return;
    var hits=[],i,r;
    for(i=0;i<sidx.length&&hits.length<25;i++){r=sidx[i];
      if(r[0].toLowerCase().indexOf(q)>-1||r[1].toLowerCase().indexOf(q)>-1||r[2].toLowerCase().indexOf(q)>-1)hits.push(r);}
    if(!hits.length){res.innerHTML="<p>No goods match \\u201c"+esc(q)+"\\u201d.</p>";return;}
    var html="<ul>";
    hits.forEach(function(r){html+='<li><a href="'+SITE+'?goods='+encodeURIComponent(r[0])+'"><b>'+esc(r[0])+'</b></a> <span class="gname">'+esc(r[1])+'</span> <span class="gcat">'+esc(r[2])+'</span></li>';});
    res.innerHTML=html+"</ul><p>"+hits.length+(hits.length===25?" (top 25)":"")+" match"+(hits.length===1?"":"es")+".</p>";
  });
});
})();
'''
    js = js.replace("%%SITEJS%%", json.dumps(SITE))
    parts = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Signature AI Pixel — Goods Catalog (A–Z archive)</title>',
             '<meta name="description" content="The full A–Z Signature AI Pixel goods archive: every good, searchable, grouped by category. Design mockups — printable art, not manufactured products.">',
             f'<link rel="canonical" href="{SITE}goods-catalog.html">',
             '<style>body{background:#0a0618;color:#f2ecff;font-family:Verdana,system-ui,sans-serif;'
             'margin:0;padding:24px;max-width:1100px}a{color:#00f0ff}h1{font-size:26px}'
             'h2{margin-top:34px;color:#ffd166}.stat{font-size:15px;color:#b9a8e0}.stat b{color:#ffd166}'
             '.searchbar{margin:18px 0}.searchbar input{width:100%;max-width:520px;padding:10px 12px;'
             'font-size:15px;background:#1a1038;border:1px solid #3a2568;color:#f2ecff;border-radius:8px}'
             '#results ul{list-style:none;padding:0}#results li{padding:8px 0;border-bottom:1px solid #241545}'
             '.gname{color:#ffd166}.gcat{color:#b9a8e0;font-size:12px;margin-left:6px}'
             '.gdesc{display:block;font-size:12px;color:#b9a8e0;margin-top:2px}'
             'details.cat{border:1px solid #3a2568;border-radius:10px;margin:10px 0;background:#120b2a}'
             'details.cat>summary{cursor:pointer;padding:14px 16px;font-size:16px;list-style:none}'
             'details.cat>summary::-webkit-details-marker{display:none}'
             'details.cat>summary b{color:#ffd166}details.cat>summary .n{color:#b9a8e0;font-size:13px;margin-left:8px}'
             'details.cat[open]>summary{border-bottom:1px solid #3a2568}'
             '.catbody{padding:6px 16px 14px}details.let{margin:8px 0;border-left:3px solid #3a2568;padding-left:10px}'
             'details.let>summary{cursor:pointer;padding:6px 0;color:#00f0ff}details.let>summary .n{color:#b9a8e0;font-size:12px;margin-left:6px}'
             'details.let ul{list-style:none;padding:0;margin:6px 0}details.let li{padding:7px 0;border-bottom:1px solid #241545;font-size:14px}'
             '.loading{color:#b9a8e0}footer{margin-top:40px;font-size:12px;color:#b9a8e0;border-top:1px solid #3a2568;padding-top:12px}</style>',
             '</head><body>',
             '<h1>\U0001f6cd\ufe0f Signature AI Pixel — Goods Catalog</h1>',
             f'<p class="stat" id="statline" data-goods="{goods_total}" data-ads="{ads_total}">'
             f'\U0001f6cd\ufe0f <b>{goods_total:,}</b> goods across <b>{ncat}</b> categories '
             f'· \U0001f4e3 <b>{ads_total:,}</b> product ads · marching to <b>1,000,000</b> goods '
             f'· stamped {today}</p>',
             '<p>Every way an image can live in the world: posters, stickers, shirts, surfboards and more. '
             'Each good carries original Signature art as a <b>DESIGN MOCKUP</b> — a generated printable design, '
             'not a physically manufactured product.</p>',
             f'<p>Interactive studio: <a href="{SITE}">Signature AI Pixel</a> · '
             f'<a href="{SITE}?tab=goods">Goods Catalog tab</a> · '
             f'<a href="{SITE}?tab=ads">Ad archive</a> · '
             f'<a href="{SITE}ads-catalog.html">A–Z ad archive</a> · '
             f'Machine feed: <a href="{SITE}data/pixel-catalog.json">pixel-catalog.json</a></p>',
             '<div class="searchbar"><input id="q" type="search" placeholder="Search all goods… (try \\u201csticker\\u201d)" '
             f'aria-label="Search all {goods_total:,} goods"><div id="results" role="status" aria-live="polite"></div></div>',
             '<h2>Browse by category (A–Z)</h2>',
             '<div id="cats">']
    parts.extend(cat_details)
    parts.append('</div>')
    parts.append(f'<noscript><p>No JavaScript? The full machine-readable catalog is at '
                 f'<a href="{SITE}data/pixel-catalog.json">pixel-catalog.json</a>, and every good '
                 f'is listed in the <a href="{SITE}sitemap-goods-1.xml">goods sitemap</a>.</p></noscript>')
    parts.append('<footer><p><b>SIGNATURE AI PIXEL</b> — the full goods archive. '
                 'Catalog loads category data lazily: nothing downloads until you open a category.</p>'
                 f'<p><a href="{SITE}">← back to Signature AI Pixel</a></p></footer>')
    parts.append('<script>' + js + '</script>')
    parts.append('</body></html>')
    p = os.path.join(BASE, "goods-catalog.html")
    with open(p, "w") as f:
        f.write("\n".join(parts))
    print(f"A–Z archive: {p} ({goods_total:,} goods, {ncat} categories, stamped {today})")

def letter_group(name):
    ch = (name or "").strip()[:1].upper()
    return ch if "A" <= ch <= "Z" else "#"

def write_ads_archive(ads_total):
    """ads-catalog.html — the full A–Z ad archive (Manon's network-wide order):
    per-letter collapsible <details> lazily loaded from data/index/ads-az/<L>.json.gz
    (rows [id, name, site] sorted by name, 250/page + Show more); count header
    stamped from data/ads_state.json (fail loud on mismatch)."""
    rows = []
    idx_p = os.path.join(BASE, "data", "index", "ads.idx.json.gz")
    with gzip.open(idx_p, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                rows.append((r[0], r[1] or "", r[2] or ""))
    assert len(rows) == ads_total, f"ads idx {len(rows)} != state ads_total {ads_total}"
    groups = {}
    for (i, n, s) in rows:
        groups.setdefault(letter_group(n), []).append((i, n, s))
    order = [chr(c) for c in range(ord("A"), ord("Z") + 1)] + ["#"]
    counts = {}
    d = os.path.join(BASE, "data", "index", "ads-az")
    os.makedirs(d, exist_ok=True)
    for L in order:
        g = sorted(groups.get(L, []), key=lambda r: (r[1] or "").lower())
        counts[L] = len(g)
        with gzip.open(os.path.join(d, L + ".json.gz"), "wt", encoding="utf-8") as f:
            json.dump([[i, n, s] for (i, n, s) in g], f, separators=(",", ":"))
    with open(os.path.join(BASE, "data", "index", "ads-az-manifest.json"), "w") as f:
        json.dump({"total": ads_total, "built": local_today(), "counts": counts}, f, indent=1)
    print(f"ads-az lazy files: {d} ({ads_total:,} ads)")
    today = local_today()
    details = []
    for L in order:
        details.append(
            f'<details class="let" data-letter="{esc_h(L)}">'
            f'<summary><b>{esc_h(L)}</b> <span class="n">{counts[L]:,} ads — tap to browse</span></summary>'
            f'<div class="lbody"><p class="loading">Loading {esc_h(L)} ads…</p></div></details>')
    js = '''
(function(){
var SITE=%%SITEJS%%, PAGE=250, loaded={};
function gz(path){return fetch(path).then(function(r){if(!r.ok)throw new Error("HTTP "+r.status);return r;})
 .then(function(r){return new Response(r.body.pipeThrough(new DecompressionStream("gzip"))).text();});}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function adLink(r){return '<li><a href="'+SITE+'?ad='+encodeURIComponent(r[0])+'"><b>'+esc(r[0])+'</b></a> '
  +'<span class="gname">'+esc(r[1])+'</span> <span class="gcat">'+esc(r[2])+'</span></li>';}
function render(det,rows){
  var body=det.querySelector(".lbody");
  function page(shown){
    var next=Math.min(shown+PAGE,rows.length);
    body.innerHTML='<ul>'+rows.slice(0,next).map(adLink).join("")+'</ul>'+
      (next<rows.length?'<p><button class="mbtn" type="button">Show more ('+(rows.length-next).toLocaleString()+' left)</button></p><p class="capnote">Showing '+next.toLocaleString()+' of '+rows.length.toLocaleString()+' ads.</p>':'');
    var b=body.querySelector(".mbtn");
    if(b)b.addEventListener("click",function(){page(next);});
  }
  page(0);
}
document.querySelectorAll("details.let").forEach(function(det){
  det.addEventListener("toggle",function(){
    var L=det.dataset.letter;
    if(!det.open||loaded[L])return;
    loaded[L]=true;
    var body=det.querySelector(".lbody");
    if(typeof DecompressionStream==="undefined"){body.innerHTML="<p>Your browser can't unzip the archive data. Try Chrome or Edge.</p>";return;}
    gz("data/index/ads-az/"+encodeURIComponent(L)+".json.gz").then(function(t){
      render(det,JSON.parse(t));
    }).catch(function(e){body.innerHTML="<p>Couldn't load this letter ("+esc(e.message)+"). Try again.</p>";loaded[L]=false;});
  });
});
})();
'''
    js = js.replace("%%SITEJS%%", json.dumps(SITE))
    parts = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>Signature AI Pixel — Ad Catalog (A–Z archive)</title>',
             '<meta name="description" content="The full A–Z Signature AI Pixel ad archive: every product ad, searchable, grouped by product name. Auto-made creative mockups — nothing is for sale.">',
             f'<link rel="canonical" href="{SITE}ads-catalog.html">',
             '<style>body{background:#0a0618;color:#f2ecff;font-family:Verdana,system-ui,sans-serif;'
             'margin:0;padding:24px;max-width:1100px}a{color:#00f0ff}h1{font-size:26px}'
             '.stat{font-size:15px;color:#b9a8e0}.stat b{color:#ffd166}'
             'details.let{margin:8px 0;border:1px solid #3a2568;border-radius:10px;background:#120b2a}'
             'details.let>summary{cursor:pointer;padding:14px 16px;font-size:16px;list-style:none}'
             'details.let>summary::-webkit-details-marker{display:none}'
             'details.let>summary b{color:#ffd166;font-size:20px}details.let>summary .n{color:#b9a8e0;font-size:13px;margin-left:8px}'
             'details.let[open]>summary{border-bottom:1px solid #3a2568}'
             '.lbody{padding:6px 16px 14px}.lbody ul{list-style:none;padding:0;margin:6px 0}'
             '.lbody li{padding:7px 0;border-bottom:1px solid #241545;font-size:14px}'
             '.gname{color:#ffd166}.gcat{color:#b9a8e0;font-size:12px;margin-left:6px}'
             '.mbtn{background:transparent;color:#00f0ff;border:1px solid #00f0ff;border-radius:10px;'
             'padding:10px 18px;font-size:14px;cursor:pointer;font-family:inherit}'
             '.capnote{color:#b9a8e0;font-size:12px}.loading{color:#b9a8e0}'
             'footer{margin-top:40px;font-size:12px;color:#b9a8e0;border-top:1px solid #3a2568;padding-top:12px}</style>',
             '</head><body>',
             '<h1>\U0001f4e2 Signature AI Pixel — Ad Catalog</h1>',
             f'<p class="stat" id="statline" data-ads="{ads_total}">'
             f'\U0001f4e2 <b>{ads_total:,}</b> product ads · marching to <b>1,000,000</b> goods '
             f'· stamped {today}</p>',
             '<p>The engine watches the catalogs and makes an image ad and a video ad for every '
             'Signature product — stored as made. Each ad is a <b>GENERATED CREATIVE MOCKUP</b> '
             'for a Signature product, not a live commercial listing. Nothing here is for sale.</p>',
             f'<p>Interactive studio: <a href="{SITE}">Signature AI Pixel</a> · '
             f'<a href="{SITE}?tab=ads">Ad archive tab</a> · '
             f'<a href="{SITE}goods-catalog.html">A–Z goods archive</a> · '
             f'Machine feed: <a href="{SITE}data/pixel-catalog.json">pixel-catalog.json</a></p>',
             '<h2 style="color:#ffd166">Browse by product name (A–Z)</h2>',
             '<div id="letters">']
    parts.extend(details)
    parts.append('</div>')
    parts.append(f'<noscript><p>No JavaScript? Every ad is listed in the '
                 f'<a href="{SITE}sitemap-ads-1.xml">ad sitemap</a>, and records open at '
                 f'{SITE}?ad=JAH-AD-000001.</p></noscript>')
    parts.append('<footer><p><b>SIGNATURE AI PIXEL</b> — the full ad archive. '
                 'Each letter loads lazily: nothing downloads until you open it.</p>'
                 f'<p><a href="{SITE}">← back to Signature AI Pixel</a></p></footer>')
    parts.append('<script>' + js + '</script>')
    parts.append('</body></html>')
    p = os.path.join(BASE, "ads-catalog.html")
    with open(p, "w") as f:
        f.write("\n".join(parts))
    print(f"A–Z archive: {p} ({ads_total:,} ads, stamped {today})")

def main():
    goods = goods_ids()
    ads = ads_ids()
    pages = [SITE, SITE + "?tab=image", SITE + "?tab=video", SITE + "?tab=goods",
             SITE + "?tab=ads", SITE + "?tab=take", SITE + "goods-catalog.html",
             SITE + "ads-catalog.html",
             SITE + "edit-video.html", SITE + "edit-photo.html",
             SITE + "pixel-manifest.json", SITE + "ai-manifest.json", SITE + "llms.txt",
             SITE + "api.json", SITE + "data/counts.json", SITE + "data/pixel-catalog.json",
             SITE + "docs/DETERMINISM.md"]
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
        "network": "THE JAH NETWORK — 27 sites",
    }
    json.dump(api, open(os.path.join(BASE, "api.json"), "w"), indent=1)
    print(f"sitemap: {len(pages)} pages + {len(goods)} goods + {len(ads)} ads | api.json written")
    # FIX-02/FIX-03: standardized JSON feed + A–Z archive page (kept fresh by every drip run)
    rows = all_goods_rows()
    write_catalog_feed(rows, ads)
    cats = {}
    for (i, n, c, d) in rows:
        cats.setdefault(c or "misc", []).append((i, n, d))
    write_goods_cat_files(cats)  # lazy per-category data, BEFORE the page that references it
    write_goods_catalog_html(rows, ads, st.get("goods_total", 0), ast.get("ads_total", 0))
    write_ads_archive(ast.get("ads_total", 0))  # per-letter lazy data + ads-catalog.html
    # authoritative manifest + instant counts + QA gates (fails the build on disagreement)
    import subprocess as _sp
    _r = _sp.run([sys.executable, os.path.join(BASE, "code", "build_manifest.py")])
    if _r.returncode != 0:
        print("build_manifest.py FAILED — build gates did not pass", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
