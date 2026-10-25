#!/usr/bin/env python3
"""Rebuilds manifest.json from everything under images/ (run by .github/workflows/manifest.yml).

Each picture's key is its path under images/ without the extension ("tos/platform_rules"); the app
asks for keys, reads the file's path from here, and re-downloads it when its sha256 changes.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "images")
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

entries = {}
for dirpath, _, files in os.walk(IMAGES):
    for f in sorted(files):
        base, ext = os.path.splitext(f)
        if ext.lower() not in EXTS:
            continue
        full = os.path.join(dirpath, f)
        rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
        key = os.path.relpath(os.path.join(dirpath, base), IMAGES).replace(os.sep, "/")
        if key in entries:
            sys.exit(f"two pictures share the key {key!r}: {entries[key]['path']} and {rel}")
        with open(full, "rb") as fh:
            data = fh.read()
        entries[key] = {"path": rel, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}

manifest = {"version": 1, "images": dict(sorted(entries.items()))}
out = json.dumps(manifest, indent=2) + "\n"
path = os.path.join(ROOT, "manifest.json")
old = open(path).read() if os.path.exists(path) else ""
if out != old:
    open(path, "w").write(out)
    print(f"manifest.json updated ({len(entries)} pictures)")
else:
    print("manifest.json already up to date")
