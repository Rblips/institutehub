#!/usr/bin/env python3
"""
Test Suite: Nginx Configuration & Security Headers
===================================================
Verifies presence of mandatory SSL/TLS directives, HSTS, CSP, and compression in Nginx.
"""

import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestNginxConfiguration(unittest.TestCase):

    def setUp(self):
        self.conf_path = WORKSPACE_ROOT / "deployment" / "nginx" / "institutehub.conf"
        self.assertTrue(self.conf_path.exists(), "Nginx config file must exist")
        self.content = self.conf_path.read_text(encoding="utf-8")

    def test_http_to_https_redirect(self):
        self.assertIn("listen 80;", self.content)
        self.assertIn("return 301 https://institutehub.edu$request_uri;", self.content)

    def test_tls_protocols(self):
        self.assertIn("ssl_protocols TLSv1.2 TLSv1.3;", self.content)
        self.assertNotIn("TLSv1.0", self.content)
        self.assertNotIn("TLSv1.1", self.content)
        self.assertNotIn("SSLv3", self.content)

    def test_hsts_header(self):
        self.assertIn("Strict-Transport-Security", self.content)
        self.assertIn("max-age=63072000", self.content)
        self.assertIn("includeSubDomains", self.content)
        self.assertIn("preload", self.content)

    def test_security_headers(self):
        self.assertIn("X-Frame-Options", self.content)
        self.assertIn("X-Content-Type-Options", self.content)
        self.assertIn("Referrer-Policy", self.content)
        self.assertIn("Content-Security-Policy", self.content)
        self.assertIn("Permissions-Policy", self.content)

    def test_gzip_compression(self):
        self.assertIn("gzip on;", self.content)
        self.assertIn("gzip_types", self.content)

    def test_caching_and_error_pages(self):
        self.assertIn("error_page 404 /404.html;", self.content)
        self.assertIn("error_page 503 @maintenance;", self.content)
        self.assertIn("max-age=31536000", self.content)


if __name__ == "__main__":
    unittest.main()
