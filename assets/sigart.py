#!/usr/bin/env python3
"""sigart.py — The Signature AI Image And Video Maker engine (Python port).

Deterministic, offline, no API keys. Same prompt => same artwork, forever.
Original generative art — trademark-safe (abstractions only, never reproductions).

Usage:
    python3 sigart.py "a lighthouse at dusk" out.svg
    python3 sigart.py "a lighthouse at dusk" out.svg --style "Ocean Deep" --caption "BEACON"
"""
import sys, math, html, argparse

PALETTES = [
    ("Neon Night",    ("#0b0620","#2b0a54"), ("#3b1d7a","#1d2b6b"), "#00f0ff", "#ff2fb3", "#12082e"),
    ("Sunset Ember",  ("#2b0f2e","#a83232"), ("#7a2a3a","#4a1e3f"), "#ffb347", "#ffe29a", "#1d0a20"),
    ("Ocean Deep",    ("#02141f","#0a3b54"), ("#0e5a7a","#134e5e"), "#7ff0d4", "#d8fbff", "#010d14"),
    ("Forest Dawn",   ("#0c1f16","#1e4d2b"), ("#2e6b3a","#1a3d24"), "#d4f79a", "#f4ffe0", "#07130c"),
    ("Cosmic Violet", ("#12041f","#3d1663"), ("#5b2a86","#2c1a4d"), "#c99aff", "#f3e8ff", "#0b0213"),
    ("Desert Gold",   ("#241304","#7a4a12"), ("#a8711f","#5c3a0e"), "#ffe08a", "#fff6d8", "#170c02"),
    ("Arctic Mint",   ("#0a1c22","#1e5a66"), ("#2e7f8f","#17424c"), "#b8fff1", "#f0ffff", "#061216"),
    ("Crimson Pulse", ("#1f060a","#5c0f1c"), ("#8f1f2e","#47101b"), "#ff8a7a", "#ffe8e0", "#120307"),
    ("Royal Indigo",  ("#080b24","#1d2a6e"), ("#2c3f8f","#141c4d"), "#9ab8ff", "#eef2ff", "#04061a"),
    ("Meadow Pastel", ("#f7e8f0","#cfe8d8"), ("#a8d5ba","#e8c8d8"), "#5b8f6b", "#2e4a38", "#e8d8e0"),
    ("Mono Ink",      ("#0d0d0f","#2a2a30"), ("#3d3d46","#1a1a1e"), "#ffffff", "#e8e8e8", "#060607"),
    ("Candy Pop",     ("#2b0a2e","#6e1e5e"), ("#93387f","#4a1545"), "#7dffea", "#ffe3f7", "#1c061d"),
]

SCENES = {
    "space":     ["star","planet","galaxy","moon","cosmos","rocket","alien","nebula","astronaut","satellite","ufo","comet","orbit"],
    "ocean":     ["ocean","sea","wave","beach","surf","fish","boat","underwater","coral","whale","shark","sail","tide","diver"],
    "landscape": ["mountain","forest","tree","desert","valley","hill","meadow","jungle","canyon","waterfall","lake","river","field","garden"],
    "city":      ["city","town","building","street","tower","skyline","bridge","village","castle","skyscraper","downtown"],
    "creature":  ["dragon","robot","cat","dog","bird","lion","monster","hero","face","knight","wolf","bear","owl","fox","tiger","beast","pet"],
    "object":    ["car","house","ship","guitar","flower","crown","sword","phone","lamp","book","key","clock","chair","cup","hat"],
}

TM_BLOCK = ["mickey","disney","marvel","spider-man","spiderman","batman","superman","pokemon","pikachu",
    "nintendo","mario","zelda","sonic","hello kitty","coca-cola","coke","pepsi","nike","adidas","apple logo",
    "mcdonald","star wars","darth vader","jedi","harry potter","hogwarts","minion","shrek","toy story",
    "frozen","elsa","barbie","lego","transformer","x-men","wolverine","avenger","iron man","thor","hulk",
    "deadpool","jurassic","godzilla","king kong","tetris","minecraft","fortnite","playstation","xbox",
    "iphone","samsung","tesla","ferrari","porsche","gucci","louis vuitton","supreme","starbucks","kfc"]

def xfnv1a(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h

def mulberry32(seed):
    a = seed & 0xFFFFFFFF
    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = (a ^ (a >> 15)) & 0xFFFFFFFF
        t = (t * (1 | a)) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t ^= t >> 14
        return (t & 0xFFFFFFFF) / 4294967296
    return rnd

def classify(prompt):
    p = " " + prompt.lower() + " "
    best, bestn = "abstract", 0
    for s, words in SCENES.items():
        n = sum(1 for w in words if w in p)
        if n > bestn: best, bestn = s, n
    return best

def guard(prompt):
    import re
    p = prompt.lower(); hits = []
    for t in TM_BLOCK:
        if re.search(r"\b" + re.escape(t) + r"s?\b", p): hits.append(t)
    if not hits: return prompt, None
    cp = prompt
    for t in hits: cp = re.sub(re.escape(t), "hero", cp, flags=re.I)
    return cp, ("Trademark-safe abstraction: original Signature-style archetype instead of "
                + ", ".join(hits) + " — not affiliated with any brand.")

def compose(prompt, style="auto", caption=None):
    clean, note = guard(prompt)
    seed = xfnv1a(prompt + "|" + style + "|")
    r = mulberry32(seed)
    pal = next((p for p in PALETTES if p[0] == style), PALETTES[seed % len(PALETTES)])
    name, bg, mid, accent, fg, deep = pal
    scene = classify(clean)
    W, H = 1200, 800
    s = []
    A = lambda x: s.append(x)
    A(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{bg[0]}"/><stop offset="1" stop-color="{bg[1]}"/></linearGradient></defs>')
    A(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    def stars(n, ymax):
        for _ in range(n):
            A(f'<circle cx="{r()*W:.1f}" cy="{r()*ymax:.1f}" r="{0.6+r()*2:.1f}" fill="{fg}" opacity="{0.25+r()*0.7:.2f}"/>')
    stars(90, H*0.7)
    # celestial
    cx, cy, rad = W*(0.15+r()*0.7), H*(0.12+r()*0.28), 40+r()*55
    A(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad*1.7:.0f}" fill="{accent}" opacity="0.18"/>')
    A(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.0f}" fill="{accent}" opacity="0.92"/>')
    base = H*0.78
    if scene in ("landscape","creature","object"):
        for L in range(3):
            y0 = base - L*H*0.09; pts = f"0,{H}"
            x = 0
            while x <= W:
                pts += f" {x:.0f},{y0-r()*H*0.2-H*0.04:.0f}"; x += W/7
            A(f'<polygon points="{pts} {W},{H}" fill="{mid[L%len(mid)]}" opacity="{0.55+L*0.18:.2f}"/>')
    elif scene == "ocean":
        for L in range(4):
            y = base + L*34; d = f"M0,{y:.0f}"
            x = 0
            while x <= W:
                d += f" q30,{r()*52-26:.0f} 60,0"; x += 60
            A(f'<path d="{d} L{W},{H} L0,{H} Z" fill="{mid[L%2]}" opacity="{0.5+L*0.14:.2f}"/>')
    elif scene == "city":
        x = 0
        while x < W:
            bw, bh = 50+r()*80, H*(0.15+r()*0.35)
            A(f'<rect x="{x:.0f}" y="{base-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{deep}" opacity="0.9"/>')
            x += bw + 4 + r()*22
    # subject: bloom
    sx, sy, pr, petals = W/2+(r()-0.5)*W*0.24, H*0.58, 70+r()*50, 6+int(r()*5)
    for pi in range(petals):
        ang = pi/petals*2*math.pi
        px, py = sx+math.cos(ang)*pr*1.5, sy+math.sin(ang)*pr*1.5
        A(f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{pr*0.85:.0f}" ry="{pr*0.5:.0f}" fill="{fg}" opacity="0.9" transform="rotate({ang*180/math.pi:.0f} {px:.0f} {py:.0f})"/>')
    A(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{pr*0.62:.0f}" fill="{accent}"/>')
    cap = caption or (" ".join(prompt.strip().split()[:6]).upper() if any(k in prompt.lower() for k in ["poster","sale","party","event","ad"]) else None)
    if cap:
        A(f'<rect x="60" y="{H-150}" width="{W-120}" height="96" rx="14" fill="{deep}" opacity="0.82"/>')
        A(f'<text x="{W/2}" y="{H-86}" text-anchor="middle" font-family="Verdana,sans-serif" font-weight="bold" font-size="52" fill="{accent}">{html.escape(cap[:42])}</text>')
    A(f'<text x="{W-24}" y="{H-22}" text-anchor="end" font-family="monospace" font-size="20" fill="{fg}" opacity="0.6">SIG-ART · {seed:08X}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(s) + "</svg>"
    meta = {"seed": seed, "seedHex": f"{seed:08X}", "palette": name, "scene": scene,
            "guarded": note is not None, "guardNote": note or ""}
    return svg, meta

def main():
    ap = argparse.ArgumentParser(description="SigArt — deterministic Signature art engine")
    ap.add_argument("prompt"); ap.add_argument("out")
    ap.add_argument("--style", default="auto"); ap.add_argument("--caption", default=None)
    a = ap.parse_args()
    svg, meta = compose(a.prompt, a.style, a.caption)
    open(a.out, "w").write(svg)
    print(f"wrote {a.out} | seed {meta['seedHex']} | {meta['palette']} / {meta['scene']}" +
          (" | TRADEMARK-SAFE ABSTRACTION" if meta["guarded"] else ""))

if __name__ == "__main__":
    main()
