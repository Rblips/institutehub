#!/usr/bin/env python3
"""
InstituteHub Automated Backup Utility
====================================
Safely creates timestamped, compressed, and SHA256-checksummed archives
of Jekyll source code, configuration files, and deployment descriptors.
"""

import argparse
import hashlib
import logging
import os
import shutil
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("InstituteHub-Backup")

# Directories and files critical to back up
INCLUDE_TARGETS = [
    "_config.yml",
    "Gemfile",
    "Gemfile.lock",
    "index.md",
    "404.html",
    "maintenance.html",
    "robots.txt",
    "sitemap.xml",
    "search.json",
    "_layouts",
    "_includes",
    "_faculty",
    "_research",
    "_events",
    "_notices",
    "_publications",
    "_courses",
    "_posts",
    "about",
    "academics",
    "research",
    "people",
    "admissions",
    "campus-life",
    "news",
    "events",
    "notices",
    "resources",
    "contact",
    "assets",
    "deployment",
    "scripts",
]

EXCLUDE_PATTERNS = [
    "_site",
    ".jekyll-cache",
    ".sass-cache",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "backups",
    "*.tar.gz",
    "*.pyc",
    ".DS_Store",
]


def calculate_sha256(file_path: Path) -> str:
    """Computes SHA256 checksum for an archive file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def should_exclude(tarinfo: tarfile.TarInfo) -> bool:
    """Filter callback to exclude cache and temporary build directories."""
    name = tarinfo.name
    for pattern in EXCLUDE_PATTERNS:
        if pattern.replace("*", "") in name:
            return None
    return tarinfo


def create_backup(source_dir: Path, output_dir: Path, dry_run: bool = False) -> dict:
    """Executes backup compression and verification."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive_name = f"institutehub_backup_{timestamp}.tar.gz"
    archive_path = output_dir / archive_name
    checksum_path = output_dir / f"{archive_name}.sha256"

    logger.info(f"Preparing backup from: {source_dir}")
    logger.info(f"Target archive: {archive_path}")

    if dry_run:
        logger.info("[DRY-RUN] Simulating backup creation...")
        total_items = 0
        for target in INCLUDE_TARGETS:
            p = source_dir / target
            if p.exists():
                total_items += 1
        logger.info(f"[DRY-RUN] Verified {total_items} targets ready for archiving.")
        return {
            "archive_path": str(archive_path),
            "sha256": "DRY_RUN_CHECKSUM",
            "size_bytes": 0,
            "status": "SUCCESS (DRY-RUN)",
        }

    output_dir.mkdir(parents=True, exist_ok=True)

    # Build tar.gz
    with tarfile.open(archive_path, "w:gz") as tar:
        for target in INCLUDE_TARGETS:
            target_path = source_dir / target
            if target_path.exists():
                tar.add(target_path, arcname=target, filter=should_exclude)
            else:
                logger.warning(f"Target not found, skipping: {target}")

    # Calculate and store checksum
    checksum = calculate_sha256(archive_path)
    with open(checksum_path, "w", encoding="utf-8") as f:
        f.write(f"{checksum}  {archive_name}\n")

    size_mb = round(archive_path.stat().st_size / (1024 * 1024), 2)
    logger.info(f"Backup created successfully: {size_mb} MB")
    logger.info(f"SHA256: {checksum}")

    return {
        "archive_path": str(archive_path),
        "checksum_path": str(checksum_path),
        "sha256": checksum,
        "size_mb": size_mb,
        "status": "SUCCESS",
    }


def enforce_retention(output_dir: Path, keep_count: int = 5, dry_run: bool = False):
    """Enforces backup retention by removing older archives exceeding keep_count."""
    if keep_count <= 0 or not output_dir.exists():
        return

    archives = sorted(
        output_dir.glob("institutehub_backup_*.tar.gz"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if len(archives) > keep_count:
        to_delete = archives[keep_count:]
        for arch in to_delete:
            sha_file = arch.with_suffix(".tar.gz.sha256")
            if dry_run:
                logger.info(f"[DRY-RUN] Would prune old archive: {arch.name}")
            else:
                logger.info(f"Pruning older archive: {arch.name}")
                arch.unlink(missing_ok=True)
                sha_file.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description="InstituteHub Production Backup Manager")
    parser.add_argument("--source", default=".", help="Root directory of InstituteHub")
    parser.add_argument("--output", default="./backups", help="Directory where backups are saved")
    parser.add_argument("--keep", type=int, default=7, help="Number of recent backups to retain")
    parser.add_argument("--dry-run", action="store_true", help="Simulate backup without writing files")

    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()

    try:
        result = create_backup(source_path, output_path, dry_run=args.dry_run)
        enforce_retention(output_path, keep_count=args.keep, dry_run=args.dry_run)
        print("\nBackup Operation Summary:")
        print(f"Status      : {result['status']}")
        print(f"Archive     : {result['archive_path']}")
        print(f"SHA256 Hash : {result['sha256']}\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Backup failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
