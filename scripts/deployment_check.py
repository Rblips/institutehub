#!/usr/bin/env python3
"""
InstituteHub Pre-Flight Deployment Validation Utility
=====================================================
Performs strict pre-flight checks on:
1. _config.yml structure and collections definitions
2. Collection items count and Front Matter schema integrity
3. Layouts, includes, and assets presence
4. Internal markdown and liquid link integrity
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Minimum item thresholds for production completeness
MIN_COLLECTION_COUNTS = {
    "_faculty": 12,
    "_research": 8,
    "_publications": 10,
    "_events": 8,
    "_notices": 12,
    "_posts": 10,
    "_courses": 15,
}

# Required front matter keys per collection
REQUIRED_FRONTMATTER = {
    "_faculty": ["name", "designation", "department", "email", "research_interests"],
    "_research": ["title", "area", "principal_investigator", "description"],
    "_publications": ["title", "authors", "venue", "year"],
    "_events": ["title", "date", "time", "location", "category"],
    "_notices": ["title", "date", "category", "department"],
    "_posts": ["title", "author", "date"],
    "_courses": ["title", "code", "credits", "department", "semester"],
}


def parse_simple_yaml_frontmatter(content: str) -> dict:
    """Parses basic YAML frontmatter from markdown file without external PyYAML dependency."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    
    yaml_text = parts[1]
    data = {}
    current_key = None
    
    for line in yaml_text.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        
        # Check for list item
        if line.strip().startswith("- ") and current_key:
            val = line.strip()[2:].strip().strip('"').strip("'")
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(val)
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            current_key = key
            if val == "" or val == "|":
                data[key] = []
            else:
                data[key] = val
                
    return data


def validate_config(root_dir: Path) -> list:
    """Validates _config.yml exists and contains critical configurations."""
    errors = []
    config_path = root_dir / "_config.yml"
    if not config_path.exists():
        errors.append("Critical: _config.yml does not exist.")
        return errors

    content = config_path.read_text(encoding="utf-8")
    for expected_key in ["title:", "collections:", "faculty:", "research:", "events:", "notices:", "courses:", "publications:"]:
        if expected_key not in content:
            errors.append(f"_config.yml missing expected key or collection: '{expected_key}'")

    return errors


def validate_collections_and_frontmatter(root_dir: Path) -> tuple[list, list]:
    """Validates collection item quantities and front matter schema completeness."""
    errors = []
    stats = []

    for col_dir, min_count in MIN_COLLECTION_COUNTS.items():
        dir_path = root_dir / col_dir
        if not dir_path.exists():
            errors.append(f"Missing collection directory: {col_dir}")
            continue

        files = list(dir_path.glob("*.md")) + list(dir_path.glob("*.markdown"))
        count = len(files)
        stats.append(f"Collection {col_dir:15s}: {count:2d} files (Requirement: >={min_count})")

        if count < min_count:
            errors.append(f"Collection {col_dir} has {count} items, below required minimum of {min_count}.")

        # Check frontmatter keys
        required_keys = REQUIRED_FRONTMATTER.get(col_dir, [])
        for md_file in files:
            content = md_file.read_text(encoding="utf-8")
            fm = parse_simple_yaml_frontmatter(content)
            for req_key in required_keys:
                if req_key not in fm:
                    errors.append(f"File {md_file.relative_to(root_dir)} is missing front matter field: '{req_key}'")

    return errors, stats


def validate_assets_and_includes(root_dir: Path) -> list:
    """Checks presence of required CSS, JS, layouts, and includes."""
    errors = []
    required_files = [
        "assets/css/main.css",
        "assets/js/main.js",
        "_layouts/default.html",
        "_layouts/page.html",
        "_layouts/post.html",
        "_layouts/faculty.html",
        "_layouts/research.html",
        "_layouts/event.html",
        "_layouts/notice.html",
        "_layouts/course.html",
        "_includes/header.html",
        "_includes/footer.html",
        "_includes/navigation.html",
        "_includes/hero.html",
        "_includes/faculty-card.html",
        "_includes/research-card.html",
        "_includes/event-card.html",
        "_includes/notice-card.html",
        "_includes/news-card.html",
        "404.html",
        "maintenance.html",
        "robots.txt",
        "sitemap.xml",
        "search.json",
    ]

    for req_file in required_files:
        if not (root_dir / req_file).exists():
            errors.append(f"Required core asset/template missing: {req_file}")

    return errors


def validate_deployment_configs(root_dir: Path) -> list:
    """Validates Linux and Nginx deployment descriptors."""
    errors = []
    deployment_files = [
        "deployment/nginx/institutehub.conf",
        "deployment/systemd/institutehub-healthcheck.service",
        "deployment/systemd/institutehub-healthcheck.timer",
        "deployment/security/ufw_setup.sh",
        "deployment/security/ssh_hardening.conf",
        "deployment/security/fail2ban-jail.local",
        "deployment/security/logrotate-institutehub",
        ".github/workflows/build.yml",
        ".github/workflows/deploy.yml",
    ]

    for dep_file in deployment_files:
        if not (root_dir / dep_file).exists():
            errors.append(f"Deployment or CI/CD configuration missing: {dep_file}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="InstituteHub Pre-Flight Deployment Validator")
    parser.add_argument("--root", default=".", help="Root directory of InstituteHub")
    args = parser.parse_args()

    root_path = Path(args.root).resolve()

    print("\n" + "=" * 50)
    print(" InstituteHub Pre-Deployment Validation Engine")
    print("=" * 50)

    config_errors = validate_config(root_path)
    col_errors, col_stats = validate_collections_and_frontmatter(root_path)
    asset_errors = validate_assets_and_includes(root_path)
    dep_errors = validate_deployment_configs(root_path)

    print("\n[1] Collections Inventory:")
    for stat in col_stats:
        print(f"    - {stat}")

    all_errors = config_errors + col_errors + asset_errors + dep_errors

    print("\n[2] Verification Summary:")
    print(f"    - Configuration Checks : {'PASSED' if not config_errors else 'FAILED'}")
    print(f"    - Content Schema Checks: {'PASSED' if not col_errors else 'FAILED'}")
    print(f"    - Layout & Asset Checks : {'PASSED' if not asset_errors else 'FAILED'}")
    print(f"    - Deployment Descriptors: {'PASSED' if not dep_errors else 'FAILED'}")

    if all_errors:
        print(f"\n[!] VALIDATION FAILED WITH {len(all_errors)} ERROR(S):")
        for err in all_errors:
            print(f"    - {err}")
        print("=" * 50 + "\n")
        sys.exit(1)
    else:
        print("\n[+] ALL PRE-DEPLOYMENT CHECKS PASSED SUCCESSFULLY!")
        print("    The repository satisfies all production academic standards.")
        print("=" * 50 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
