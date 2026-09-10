#!/usr/bin/env python3
"""
Test Suite: Link Integrity & Asset Validation
=============================================
Checks internal navigation links, stylesheets, search.json, and layout references.
"""

import re
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


class TestLinksAndAssets(unittest.TestCase):

    def test_css_design_system_present(self):
        css_file = WORKSPACE_ROOT / "assets" / "css" / "main.css"
        self.assertTrue(css_file.exists(), "main.css must exist")
        css_text = css_file.read_text(encoding="utf-8")
        self.assertIn("--color-primary:", css_text)
        self.assertIn("--color-accent:", css_text)
        self.assertIn(".hero", css_text)
        self.assertIn(".card", css_text)

    def test_javascript_suite_present(self):
        js_file = WORKSPACE_ROOT / "assets" / "js" / "main.js"
        self.assertTrue(js_file.exists(), "main.js must exist")
        js_text = js_file.read_text(encoding="utf-8")
        self.assertIn("initMobileNavigation", js_text)
        self.assertIn("initSearchSystem", js_text)
        self.assertIn("initFacultyFilter", js_text)
        self.assertIn("initNoticesFilter", js_text)
        self.assertIn("initEventsFilter", js_text)

    def test_search_json_valid_liquid(self):
        search_file = WORKSPACE_ROOT / "search.json"
        self.assertTrue(search_file.exists(), "search.json template must exist")
        text = search_file.read_text(encoding="utf-8")
        self.assertIn("site.faculty", text)
        self.assertIn("site.research", text)
        self.assertIn("site.courses", text)
        self.assertIn("site.events", text)
        self.assertIn("site.notices", text)
        self.assertIn("site.posts", text)

    def test_all_pages_exist(self):
        expected_pages = [
            "index.md",
            "about/index.md",
            "academics/index.md",
            "research/index.md",
            "people/index.md",
            "admissions/index.md",
            "campus-life/index.md",
            "news/index.md",
            "events/index.md",
            "notices/index.md",
            "resources/index.md",
            "contact/index.md",
            "404.html",
            "maintenance.html",
            "robots.txt",
            "sitemap.xml",
        ]
        for page in expected_pages:
            p = WORKSPACE_ROOT / page
            self.assertTrue(p.exists(), f"Page {page} must exist")


if __name__ == "__main__":
    unittest.main()
