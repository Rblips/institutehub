#!/usr/bin/env python3
"""
Verify site links and asset paths for GitHub Pages project-site baseurl compatibility.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"

def audit_site():
    broken = []
    # Match href="/..." or src="/..." that doesn't start with /institutehub
    pattern = re.compile(r'''(?:href|src|action)\s*=\s*["'](/[^"']+)["']''', re.IGNORECASE)
    
    files_checked = 0
    for f in SITE_DIR.rglob("*.*"):
        if f.suffix in [".html", ".xml", ".txt", ".json"]:
            files_checked += 1
            content = f.read_text(encoding="utf-8", errors="ignore")
            for match in pattern.finditer(content):
                target = match.group(1)
                # Ignore protocol-relative '//', external or baseurl paths
                if target.startswith("//"):
                    continue
                if not (target.startswith("/institutehub/") or target == "/institutehub" or target.startswith("/institutehub?")):
                    # Exclude standard robots disallow / or search query if any
                    broken.append((str(f.relative_to(SITE_DIR)), target, match.group(0)))

    print(f"Checked {files_checked} generated files in _site/")
    if broken:
        print(f"Found {len(broken)} root-relative paths missing /institutehub baseurl:")
        for file_rel, target, raw in broken:
            print(f"  {file_rel}: {raw}")
    else:
        print("SUCCESS: All internal links, stylesheets, scripts, and asset references correctly use /institutehub baseurl!")
    
    return len(broken)

if __name__ == "__main__":
    audit_site()
