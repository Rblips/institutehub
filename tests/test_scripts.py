#!/usr/bin/env python3
"""
Test Suite: Automation Scripts Execution & Logic
================================================
Verifies logic in health_check.py, backup.py, deployment_check.py, and cleanup.py.
"""

import sys
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))

import backup
import cleanup
import deployment_check
import health_check


class TestAutomationScripts(unittest.TestCase):

    def test_health_check_disk_usage(self):
        disk = health_check.check_disk_usage(str(WORKSPACE_ROOT))
        self.assertIn("total_gb", disk)
        self.assertIn("used_gb", disk)
        self.assertIn("free_gb", disk)
        self.assertIn("percent_used", disk)
        self.assertGreater(disk["total_gb"], 0)
        self.assertIn(disk["status"], ["HEALTHY", "WARNING", "CRITICAL"])

    def test_health_check_evaluation_healthy(self):
        http_ok = {"reachable": True, "status_code": 200, "response_time_ms": 120}
        ssl_ok = {"valid": True, "days_remaining": 90, "issuer": "Let's Encrypt"}
        disk_ok = {"percent_used": 45.0}
        status = health_check.evaluate_overall_health(http_ok, ssl_ok, disk_ok, local_only=False)
        self.assertEqual(status, "HEALTHY")

    def test_health_check_evaluation_critical_disk(self):
        http_ok = {"reachable": True, "status_code": 200}
        ssl_ok = {"valid": True, "days_remaining": 90}
        disk_crit = {"percent_used": 95.0}
        status = health_check.evaluate_overall_health(http_ok, ssl_ok, disk_crit, local_only=False)
        self.assertEqual(status, "CRITICAL")

    def test_health_check_evaluation_critical_http(self):
        http_fail = {"reachable": False, "status_code": 500}
        ssl_ok = {"valid": True, "days_remaining": 90}
        disk_ok = {"percent_used": 45.0}
        status = health_check.evaluate_overall_health(http_fail, ssl_ok, disk_ok, local_only=False)
        self.assertEqual(status, "CRITICAL")

    def test_backup_dry_run(self):
        output_dir = WORKSPACE_ROOT / "backups_test"
        res = backup.create_backup(WORKSPACE_ROOT, output_dir, dry_run=True)
        self.assertIn("status", res)
        self.assertTrue("DRY-RUN" in res["status"])

    def test_deployment_check_validation(self):
        config_errs = deployment_check.validate_config(WORKSPACE_ROOT)
        self.assertEqual(len(config_errs), 0, f"Config check errors: {config_errs}")

        col_errs, col_stats = deployment_check.validate_collections_and_frontmatter(WORKSPACE_ROOT)
        self.assertEqual(len(col_errs), 0, f"Collections errors: {col_errs}")

        asset_errs = deployment_check.validate_assets_and_includes(WORKSPACE_ROOT)
        self.assertEqual(len(asset_errs), 0, f"Asset check errors: {asset_errs}")

        dep_errs = deployment_check.validate_deployment_configs(WORKSPACE_ROOT)
        self.assertEqual(len(dep_errs), 0, f"Deployment config errors: {dep_errs}")

    def test_cleanup_dry_run(self):
        dirs_c, files_c = cleanup.clean_workspace(WORKSPACE_ROOT, dry_run=True)
        self.assertIsInstance(dirs_c, int)
        self.assertIsInstance(files_c, int)


if __name__ == "__main__":
    unittest.main()
