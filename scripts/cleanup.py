#!/usr/bin/env python3
"""
InstituteHub Safe Workspace Cleanup Utility
==========================================
Safely removes transient build artifacts, intermediate compiler caches,
and temporary files while strictly preserving source and configuration assets.
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("InstituteHub-Cleanup")

# Directories safe to completely remove
CACHE_DIRECTORIES = [
    "_site",
    ".jekyll-cache",
    ".sass-cache",
    ".jekyll-metadata",
    ".pytest_cache",
    "htmlcov",
    ".coverage",
]

# File pattern suffixes safe to prune
TEMP_FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*~",
    "*.swp",
    ".DS_Store",
    "Thumbs.db",
]


def clean_workspace(root_dir: Path, dry_run: bool = False, force: bool = False) -> tuple[int, int]:
    """Scans and cleans transient caches and temporary files."""
    removed_dirs = 0
    removed_files = 0

    logger.info(f"Scanning workspace: {root_dir}")
    if dry_run:
        logger.info("[DRY-RUN] Simulating workspace cleanup...")

    # 1. Prune Cache Directories
    for cache_name in CACHE_DIRECTORIES:
        cache_path = root_dir / cache_name
        if cache_path.exists():
            if dry_run:
                logger.info(f"[DRY-RUN] Would remove directory: {cache_path}")
            else:
                logger.info(f"Removing directory: {cache_path}")
                if cache_path.is_dir():
                    shutil.rmtree(cache_path, ignore_errors=True)
                else:
                    cache_path.unlink(missing_ok=True)
            removed_dirs += 1

    # 2. Prune __pycache__ subdirectories recursively
    for pycache_dir in root_dir.rglob("__pycache__"):
        if pycache_dir.exists():
            if dry_run:
                logger.info(f"[DRY-RUN] Would remove __pycache__: {pycache_dir}")
            else:
                logger.info(f"Removing __pycache__: {pycache_dir}")
                shutil.rmtree(pycache_dir, ignore_errors=True)
            removed_dirs += 1

    # 3. Prune Temporary Files
    for pattern in TEMP_FILE_PATTERNS:
        for temp_file in root_dir.rglob(pattern):
            if temp_file.is_file():
                if dry_run:
                    logger.info(f"[DRY-RUN] Would delete file: {temp_file}")
                else:
                    logger.info(f"Deleting file: {temp_file}")
                    temp_file.unlink(missing_ok=True)
                removed_files += 1

    return removed_dirs, removed_files


def main():
    parser = argparse.ArgumentParser(description="InstituteHub Safe Build & Cache Cleanup")
    parser.add_argument("--root", default=".", help="Root directory of InstituteHub")
    parser.add_argument("--dry-run", action="store_true", help="Report what would be deleted without deleting")
    parser.add_argument("--force", action="store_true", help="Force cleanup without interactive prompt")

    args = parser.parse_args()
    root_path = Path(args.root).resolve()

    dirs_cleaned, files_cleaned = clean_workspace(root_path, dry_run=args.dry_run, force=args.force)

    print("\nCleanup Summary:")
    print(f"Directories removed: {dirs_cleaned}")
    print(f"Files removed      : {files_cleaned}")
    if args.dry_run:
        print("[!] Dry run complete. No files were altered.")
    else:
        print("[+] Workspace is clean.")
    print("")
    sys.exit(0)


if __name__ == "__main__":
    main()
