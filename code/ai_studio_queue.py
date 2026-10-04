#!/usr/bin/env python3
"""AI Studio queue reader for the Signature AI Pixel worker.

Lists open GitHub issues labeled `gen-request` on
justinahiggins614-cmyk/signature-ai-image-video-maker, parses the
machine-readable request body written by generate.html, and prints the
oldest-first queue as JSON.

Body format (written by generate.html):
    PROMPT:
    <verbatim prompt, possibly multi-line>

    TYPE: image|video
    STYLE: <style>
    ASPECT: 16:9|1:1|9:16|4:3|-
    DURATION: <text>|-
    VARIATIONS: <1-4>

Usage:
    python3 code/ai_studio_queue.py           # prints JSON array, oldest first
    python3 code/ai_studio_queue.py --count   # prints just the count
"""
import json
import subprocess
import sys

REPO = "justinahiggins614-cmyk/signature-ai-image-video-maker"
LABEL = "gen-request"
KEYS = ("TYPE:", "STYLE:", "ASPECT:", "DURATION:", "VARIATIONS:")


def gh_issues():
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", REPO, "--label", LABEL,
         "--state", "open", "--limit", "100",
         "--json", "number,title,body,createdAt,author"],
        capture_output=True, text=True, check=True, timeout=60).stdout
    return json.loads(out)


def parse_body(body):
    """Extract the structured fields from a generate.html request body."""
    req = {"prompt": "", "type": "image", "style": "photorealistic",
           "aspect": "16:9", "duration": "-", "variations": "1"}
    if not body:
        return req
    lines = body.replace("\r", "").split("\n")
    # PROMPT: runs until a blank line or the next KEY:
    if lines and lines[0].strip() == "PROMPT:":
        prompt_lines = []
        for ln in lines[1:]:
            s = ln.strip()
            if s == "" or any(s.startswith(k) for k in KEYS):
                break
            prompt_lines.append(ln)
        req["prompt"] = "\n".join(prompt_lines).strip()
    for ln in lines:
        s = ln.strip()
        for k in KEYS:
            if s.startswith(k):
                req[k[:-1].lower()] = s[len(k):].strip()
                break
    # sanitize
    if req["type"] not in ("image", "video"):
        req["type"] = "image"
    try:
        v = int(req["variations"])
    except ValueError:
        v = 1
    req["variations"] = str(max(1, min(4, v)))
    return req


def queue():
    issues = gh_issues()
    # oldest first
    issues.sort(key=lambda i: i.get("createdAt", ""))
    out = []
    for i in issues:
        req = parse_body(i.get("body") or "")
        req["issue"] = i["number"]
        req["title"] = i.get("title", "")
        req["author"] = (i.get("author") or {}).get("login", "")
        req["created_at"] = i.get("createdAt", "")
        out.append(req)
    return out


def main():
    if "--count" in sys.argv:
        print(len(queue()))
        return
    print(json.dumps(queue(), indent=2))


if __name__ == "__main__":
    main()
