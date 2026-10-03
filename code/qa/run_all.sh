#!/usr/bin/env bash
# run_all.sh — Pixel fix-wave QA gates. Exit 0 = all pass.
set -u
cd "$(dirname "$0")/../.."
fails=0

echo "=== [1/5] manifest QA gates (G1-G5) ==="
python3 code/build_manifest.py || fails=$((fails+1))

echo "=== [2/5] determinism + JS/PY parity ==="
python3 code/qa/test_determinism.py || fails=$((fails+1))

echo "=== [3/5] JS syntax (touched files) ==="
node --check assets/engine.js || fails=$((fails+1))
python3 - << 'EOF' || fails=$((fails+1))
import re
t = open('index.html', encoding='utf-8').read()
blocks = re.findall(r'<script>([\s\S]*?)</script>', t)
open('/tmp/pxcheck.js','w').write('\n;\n'.join(blocks))
EOF
node --check /tmp/pxcheck.js || fails=$((fails+1))

echo "=== [4/5] sitemap validity ==="
python3 - << 'EOF' || fails=$((fails+1))
import xml.etree.ElementTree as ET, glob
ok = True
for f in ["sitemap.xml"] + glob.glob("sitemap-*.xml"):
    try:
        ET.parse(f)
        print("PASS xml", f)
    except Exception as e:
        print("FAIL xml", f, e); ok = False
raise SystemExit(0 if ok else 1)
EOF

echo "=== [5/5] schema sanity (all schema files parse + manifest validates) ==="
python3 - << 'EOF' || fails=$((fails+1))
import json, glob, re
ok = True
for f in glob.glob("data/schemas/*.schema.json"):
    try:
        s = json.load(open(f))
        assert "$id" in s and "properties" in s, "missing $id/properties"
        print("PASS schema", f)
    except Exception as e:
        print("FAIL schema", f, e); ok = False
m = json.load(open("pixel-manifest.json"))
need = ["manifest_version","site_id","counts","engine","index","qa","generated_at"]
for k in need:
    if k not in m: print("FAIL manifest missing", k); ok = False
# counts must agree with the manifest's own index-row counts (never hard-coded)
if m["counts"]["goods_total"] != m["index"]["goods_index_rows"]:
    print("FAIL goods_total vs index rows"); ok = False
if m["counts"]["ads_total"] != m["index"]["ads_index_rows"]:
    print("FAIL ads_total vs index rows"); ok = False
print("PASS manifest keys + counts")
raise SystemExit(0 if ok else 1)
EOF

echo ""
if [ $fails -eq 0 ]; then echo "QA: ALL PASS"; else echo "QA: $fails FAILURES"; fi
exit $fails
