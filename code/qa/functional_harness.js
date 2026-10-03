#!/usr/bin/env node
/* functional_harness.js — engine-level functional exercise of SigArt (assets/engine.js).
   Drives the REAL shipped engine functions against REAL data, no mocks.
   Exit 0 = all PASS. Run: node code/qa/functional_harness.js
   (Llama-enhancement fallback is exercised here; browser-only raster/export
   paths are exercised in page_harness.js where the DOM can be stubbed.) */
"use strict";
var path = require("path");
var REPO = path.resolve(__dirname, "..", "..");
var SigArt = require(path.join(REPO, "assets", "engine.js"));

var pass = 0, fail = 0, results = [];
function check(name, cond, extra) {
  if (cond) { pass++; results.push("PASS " + name); }
  else { fail++; results.push("FAIL " + name + (extra ? " — " + extra : "")); }
}

/* ---------- 1. image generation (fix-list #2, #14) ---------- */
var art = SigArt.composeImage("a lighthouse on a cliff at dusk, waves crashing below", { style: "auto" });
check("image generation returns svg", art && typeof art.svg === "string" && art.svg.indexOf("<svg") >= 0);
check("image generation exposes seedHex", typeof art.seedHex === "string" && /^[0-9A-F]{8}$/.test(art.seedHex), art && art.seedHex);
check("image generation exposes palette/scene/description", !!(art.palette && art.scene && art.description));
check("image generation validates as safe svg", SigArt.validateSVG(art.svg).ok === true);

/* ---------- 2. determinism: same prompt+settings => same art ---------- */
var art2 = SigArt.composeImage("a lighthouse on a cliff at dusk, waves crashing below", { style: "auto" });
check("determinism: identical SVG for identical input", art.svg === art2.svg);

/* ---------- 3. style selector (fix-list #9) ---------- */
check("PALETTES non-empty", Array.isArray(SigArt.PALETTES) && SigArt.PALETTES.length >= 8,
  "got " + SigArt.PALETTES.length);
var styleOk = true, styleNames = [];
SigArt.PALETTES.forEach(function (p) {
  var a = SigArt.composeImage("a fox in a neon forest", { style: p.name });
  styleNames.push(p.name);
  if (a.palette !== p.name) styleOk = false;
});
check("every style selector option honored by engine", styleOk, styleNames.join(","));
var autoA = SigArt.composeImage("a fox in a neon forest", { style: "auto" });
check("style=auto resolves a real palette", styleNames.indexOf(autoA.palette) >= 0, autoA.palette);

/* ---------- 4. caption (fix-list #10) ---------- */
var capArt = SigArt.composeImage("a poster scene", { style: "auto", caption: "GRAND SALE <today>" });
check("caption embedded + HTML-escaped in SVG", capArt.svg.indexOf("GRAND SALE &lt;TODAY&gt;") >= 0, "caption is uppercased+escaped by engine");
var noCap = SigArt.composeImage("a poster scene", { style: "auto" });
check("blank caption does not inject caption text", noCap.svg.indexOf("undefined") < 0);

/* ---------- 5. trademark guard (fix-list implied) ---------- */
var g = SigArt.guard("a batman adventure in gotham");
check("guard flags trademarked prompt", g.clean === false && g.hits.length > 0, JSON.stringify(g.hits));
check("guard rewrites cleanPrompt", g.cleanPrompt.toLowerCase().indexOf("batman") < 0, g.cleanPrompt);
check("guard note explains abstraction", typeof g.note === "string" && g.note.length > 40);
var gClean = SigArt.guard("a lighthouse on a cliff at dusk");
check("guard passes original prompt clean", gClean.clean === true && gClean.hits.length === 0);
var gArt = SigArt.composeImage("a batman adventure in gotham", { style: "auto" });
check("composeImage marks guarded art + guardNote", gArt.guarded === true && typeof gArt.guardNote === "string" && gArt.guardNote.length > 0);

/* ---------- 6. validateSVG gate ---------- */
check("validateSVG rejects <script>", SigArt.validateSVG("<svg><script>alert(1)</script></svg>").ok === false);
check("validateSVG rejects external href", SigArt.validateSVG('<svg><image href="https://x.evil/a.png"/></svg>').ok === false);
check("validateSVG rejects event handlers", SigArt.validateSVG('<svg><rect onload="x"/></svg>').ok === false);

/* ---------- 7. goods mockups (fix-list #4) ---------- */
check("GOOD_CATS non-empty", Array.isArray(SigArt.GOOD_CATS) && SigArt.GOOD_CATS.length > 10);
var mockOk = true, mockBad = [];
SigArt.GOOD_CATS.forEach(function (c) {
  var svg = SigArt.mockupSVG(c, art, 12345);
  var v = SigArt.validateSVG(svg);
  if (svg.indexOf("<svg") < 0 || !v.ok) { mockOk = false; mockBad.push(c + ":" + v.issues.join(",")); }
});
check("mockupSVG renders + validates for every category", mockOk, mockBad.join(" | "));

/* ---------- 8. product ads (fix-list #5) ---------- */
var fs = require("fs"), zlib = require("zlib");
var adChunks = {};
var adIdx = zlib.gunzipSync(fs.readFileSync(path.join(REPO, "data/index/ads.idx.json.gz")))
  .toString().trim().split("\n").map(JSON.parse).slice(0, 5);
var adOk = true, adBad = [];
adIdx.forEach(function (row) {
  var chunkFn = row[3];
  if (!adChunks[chunkFn]) {
    var t = zlib.gunzipSync(fs.readFileSync(path.join(REPO, "data/ads", chunkFn))).toString().trim().split("\n");
    adChunks[chunkFn] = {}; t.forEach(function (l) { var a = JSON.parse(l); adChunks[chunkFn][a.id] = a; });
  }
  var a = adChunks[chunkFn][row[0]];
  if (!a) { adOk = false; adBad.push(row[0] + ":missing"); return; }
  var svg = SigArt.adCreative(a), v = SigArt.validateSVG(svg);
  if (svg.indexOf("<svg") < 0 || !v.ok || svg.indexOf(SigArt.esc(a.product.name.slice(0, 30))) < 0) {
    adOk = false; adBad.push(a.id + ":" + v.issues.join(","));
  }
});
check("adCreative renders+validates 5 REAL archived ads", adOk, adBad.join(" | "));

/* ---------- 9. video planning (fix-list #3) ---------- */
var plan = SigArt.planVideo("flying over a neon city at night", { seconds: 6, caption: "NEON" });
check("planVideo honors seconds", plan.seconds === 6, "got " + plan.seconds);
check("planVideo exposes seedHex+palette", /^[0-9A-F]{8}$/.test(plan.seedHex) && !!plan.palette);
var plan2 = SigArt.planVideo("flying over a neon city at night", { seconds: 6, caption: "NEON" });
check("planVideo deterministic", plan.seedHex === plan2.seedHex);
check("planVideo caption flows to plan", plan.caption === "NEON");

/* ---------- 10. drawVideoFrame with a stub ctx (no throw) ---------- */
/* stub: callable proxy — property reads return the proxy, calls return it too */
function makeCtxStub() {
  var p = new Proxy(function () {}, {
    get: function (t, k) {
      if (k === Symbol.toPrimitive) return function () { return 0; };
      return p;
    },
    set: function () { return true; },
    apply: function () { return p; }
  });
  return p;
}
var ctxStub = makeCtxStub();
var frameOk = true, frameErr = "";
try {
  for (var f = 0; f < 5; f++) SigArt.drawVideoFrame(ctxStub, plan, f * 1.2);
} catch (e) { frameOk = false; frameErr = String(e && e.message || e); }
check("drawVideoFrame renders 5 frames without throwing", frameOk, frameErr);

/* ---------- 11. exportWebm graceful failure without browser APIs ---------- */
var pending = 2; /* webm callback + expandPrompt promise */
function maybeFinish() { if (--pending <= 0) finish(); }
SigArt.exportWebm({}, plan, function (blob, err) {
  check("exportWebm fails gracefully (no MediaRecorder in Node)", blob === null && typeof err === "string" && err.length > 10, String(err));
  maybeFinish();
});
setTimeout(function () {
  if (pending === 2) { check("exportWebm callback fires", false, "timed out"); pending = 0; finish(); }
}, 5000);

/* ---------- 12. Llama enhancement ON but Llama unreachable (fix-list #11/#13) ---------- */
global.document = {  /* stub: script tag injection fails -> onerror -> fallback */
  createElement: function () { return {}; },
  head: { appendChild: function (s) { if (s.onerror) s.onerror(); } }
};
SigArt.expandPrompt("a lighthouse at dusk").then(function (exp) {
  check("expandPrompt never silent: resolves with labeled source", !!exp && typeof exp.text === "string" && typeof exp.source === "string", JSON.stringify(exp));
  check("expandPrompt falls back to on-device engine with visible label",
    exp.source === "Signature Engine (on-device deterministic)", exp.source);
  check("expandPrompt keeps original prompt text", exp.text.indexOf("a lighthouse at dusk") === 0);
  maybeFinish();
}, function (e) {
  check("expandPrompt resolves (never rejects silently)", false, String(e));
  maybeFinish();
});

/* ---------- 13. copy-text fields all present (fix-list #19 basis) ---------- */
check("copy fields: art.prompt/scene/palette/seedHex", !!(art.prompt && art.scene && art.palette && art.seedHex));

function finish() {
  results.forEach(function (r) { console.log(r); });
  console.log("\nENGINE HARNESS: " + pass + " PASS, " + fail + " FAIL");
  process.exit(fail ? 1 : 0);
}
