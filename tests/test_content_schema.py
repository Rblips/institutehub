#!/usr/bin/env python3
"""
Test Suite: Content Collections & Schema Integrity
===================================================
Verifies all front matter schemas, collection counts, and data types
across faculty, research, events, notices, publications, and courses.
"""

import os
import re
import unittest
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(file_path: Path) -> dict:
    content = file_path.read_text(encoding="utf-8")
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


class TestContentSchema(unittest.TestCase):

    def test_faculty_collection(self):
        faculty_dir = WORKSPACE_ROOT / "_faculty"
        self.assertTrue(faculty_dir.exists(), "_faculty directory must exist")
        files = list(faculty_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 12, "Faculty collection must have >= 12 members")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("name", fm, f"Missing name in {f.name}")
            self.assertIn("designation", fm, f"Missing designation in {f.name}")
            self.assertIn("department", fm, f"Missing department in {f.name}")
            self.assertIn("email", fm, f"Missing email in {f.name}")
            self.assertIn("@", fm["email"], f"Invalid email format in {f.name}")
            self.assertIn("research_interests", fm, f"Missing research_interests in {f.name}")
            self.assertTrue(isinstance(fm["research_interests"], list), f"research_interests should be list in {f.name}")

    def test_research_collection(self):
        research_dir = WORKSPACE_ROOT / "_research"
        self.assertTrue(research_dir.exists(), "_research directory must exist")
        files = list(research_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 8, "Research collection must have >= 8 projects")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("area", fm, f"Missing area in {f.name}")
            self.assertIn("principal_investigator", fm, f"Missing PI in {f.name}")
            self.assertIn("description", fm, f"Missing description in {f.name}")

    def test_publications_collection(self):
        pub_dir = WORKSPACE_ROOT / "_publications"
        self.assertTrue(pub_dir.exists(), "_publications directory must exist")
        files = list(pub_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 10, "Publications collection must have >= 10 items")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("authors", fm, f"Missing authors in {f.name}")
            self.assertIn("venue", fm, f"Missing venue in {f.name}")
            self.assertIn("year", fm, f"Missing year in {f.name}")

    def test_events_collection(self):
        events_dir = WORKSPACE_ROOT / "_events"
        self.assertTrue(events_dir.exists(), "_events directory must exist")
        files = list(events_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 8, "Events collection must have >= 8 items")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("date", fm, f"Missing date in {f.name}")
            self.assertIn("time", fm, f"Missing time in {f.name}")
            self.assertIn("location", fm, f"Missing location in {f.name}")
            self.assertIn("category", fm, f"Missing category in {f.name}")

    def test_notices_collection(self):
        notices_dir = WORKSPACE_ROOT / "_notices"
        self.assertTrue(notices_dir.exists(), "_notices directory must exist")
        files = list(notices_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 12, "Notices collection must have >= 12 items")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("date", fm, f"Missing date in {f.name}")
            self.assertIn("category", fm, f"Missing category in {f.name}")
            self.assertIn("department", fm, f"Missing department in {f.name}")

    def test_posts_collection(self):
        posts_dir = WORKSPACE_ROOT / "_posts"
        self.assertTrue(posts_dir.exists(), "_posts directory must exist")
        files = list(posts_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 10, "Posts collection must have >= 10 articles")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("author", fm, f"Missing author in {f.name}")
            self.assertIn("date", fm, f"Missing date in {f.name}")

    def test_courses_collection(self):
        courses_dir = WORKSPACE_ROOT / "_courses"
        self.assertTrue(courses_dir.exists(), "_courses directory must exist")
        files = list(courses_dir.glob("*.md"))
        self.assertGreaterEqual(len(files), 15, "Courses collection must have >= 15 items")

        for f in files:
            fm = parse_frontmatter(f)
            self.assertIn("title", fm, f"Missing title in {f.name}")
            self.assertIn("code", fm, f"Missing code in {f.name}")
            self.assertIn("credits", fm, f"Missing credits in {f.name}")
            self.assertIn("department", fm, f"Missing department in {f.name}")
            self.assertIn("semester", fm, f"Missing semester in {f.name}")


if __name__ == "__main__":
    unittest.main()
