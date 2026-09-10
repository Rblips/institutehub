#!/usr/bin/env python3
"""
InstituteHub Local Builder & Development Server
===============================================
Renders the complete Jekyll site using YAML, Markdown, and template compilation,
generating the static `_site` bundle and serving on http://127.0.0.1:4000.
"""

import http.server
import json
import os
import re
import shutil
import socketserver
import sys
from datetime import datetime, timezone
from pathlib import Path
import markdown
import yaml
import jinja2

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"


def load_yaml_frontmatter(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception as e:
        print(f"Error parsing YAML in {file_path}: {e}")
        fm = {}
    return fm, parts[2].strip()


def parse_date(date_val):
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, str):
        try:
            return datetime.strptime(date_val.split()[0], "%Y-%m-%d")
        except:
            pass
    return datetime.now()


def liquid_to_jinja(text: str, includes_dict: dict) -> str:
    """Converts Jekyll Liquid syntax to Jinja2 compatible template string."""
    
    # 1. Convert Liquid assigns: {% assign x = y %} -> {% set x = y %}
    text = re.sub(r"{%\s*assign\s+([a-zA-Z0-9_]+)\s*=\s*(.*?)\s*%}", r"{% set \1 = \2 %}", text)

    # 2. Convert elsif: {% elsif cond %} -> {% elif cond %}
    text = re.sub(r"{%\s*elsif\s+(.*?)\s*%}", r"{% elif \1 %}", text)

    # 3. Convert unless: {% unless cond %} -> {% if not (cond) %}, {% endunless %} -> {% endif %}
    text = re.sub(r"{%\s*unless\s+(.*?)\s*%}", r"{% if not (\1) %}", text)
    text = re.sub(r"{%\s*endunless\s*%}", r"{% endif %}", text)

    # 3. Convert 'contains': a contains b -> b in (a or '')
    def replace_contains(match):
        pre = match.group(1)
        a = match.group(2)
        b = match.group(3)
        post = match.group(4)
        return f"{pre}{b} in ({a} or ''){post}"
    
    text = re.sub(r"({%\s*(?:if|elif)\s+.*?)([a-zA-Z0-9_.]+)\s+contains\s+([a-zA-Z0-9_.\"':\-\/]+)(.*?\s*%})", replace_contains, text)

    # 4. Convert for loops with limit: {% for x in arr limit: 4 %} -> {% for x in arr[:4] %}
    text = re.sub(r"{%\s*for\s+([a-zA-Z0-9_]+)\s+in\s+([a-zA-Z0-9_.]+)\s+limit:\s*(\d+)\s*%}", r"{% for \1 in \2[:\3] %}", text)

    # 5. Handle {% include name.html param=val %}
    def replace_include(match):
        inc_name = match.group(1).strip()
        params_str = match.group(2).strip()
        param_pairs = re.findall(r'([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_."\':\-]+)', params_str)
        set_statements = []
        for k, v in param_pairs:
            set_statements.append(f"{{% set include_{k} = {v} %}}")
        
        inc_content = includes_dict.get(inc_name, f"<!-- Missing include: {inc_name} -->")
        # In the included content, replace include.param with include_param
        inc_processed = re.sub(r"include\.([a-zA-Z0-9_]+)", r"include_\1", inc_content)
        # Transpile the included content
        inc_transpiled = liquid_to_jinja(inc_processed, includes_dict)
        
        return "\n".join(set_statements) + "\n" + inc_transpiled

    text = re.sub(r"{%\s*include\s+([a-zA-Z0-9_\-]+\.html)(.*?)\s*%}", replace_include, text)

    # 6. Transform Liquid filter syntax: | filter: "arg" -> | filter("arg")
    text = re.sub(r'\|\s*date:\s*(".*?"|\'.*?\')', r'| date(\1)', text)
    text = re.sub(r'\|\s*truncatewords:\s*(\d+)', r'| truncatewords(\1)', text)
    text = re.sub(r'\|\s*truncate:\s*(\d+)', r'| truncate(\1)', text)
    text = re.sub(r'\|\s*default:\s*(".*?"|\'.*?\'|[a-zA-Z0-9_.]+)', r'| default(\1)', text)
    text = re.sub(r'\|\s*join:\s*(".*?"|\'.*?\')', r'| join(\1)', text)
    text = re.sub(r'\|\s*slice:\s*(\d+)\s*,\s*(\d+)', r'| slice_str(\1, \2)', text)
    text = re.sub(r'\|\s*size\b', r'| length', text)

    return text


def build_site():
    print("[*] Building InstituteHub static site...")
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir(parents=True)

    # 1. Load _config.yml
    config_data = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8")) or {}
    site = {
        "title": config_data.get("title", "InstituteHub"),
        "tagline": config_data.get("tagline", "Engineering Knowledge. Advancing Tomorrow."),
        "description": config_data.get("description", ""),
        "url": "http://127.0.0.1:4000",
        "baseurl": "",
        "institute": config_data.get("institute", {}),
        "stats": config_data.get("stats", {}),
        "navigation": config_data.get("navigation", []),
        "faculty": [],
        "research": [],
        "publications": [],
        "events": [],
        "notices": [],
        "courses": [],
        "posts": [],
        "pages": [],
        "time": datetime.now(timezone.utc),
    }

    # 2. Load Collections
    for f in sorted((ROOT / "_faculty").glob("*.md")):
        fm, body = load_yaml_frontmatter(f)
        slug = f.stem
        fm["slug"] = slug
        fm["url"] = f"/people/faculty/{slug}/"
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["faculty"].append(fm)

    for f in sorted((ROOT / "_research").glob("*.md")):
        fm, body = load_yaml_frontmatter(f)
        slug = fm.get("slug", f.stem)
        fm["slug"] = slug
        fm["url"] = f"/research/projects/{slug}/"
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["research"].append(fm)

    for f in sorted((ROOT / "_publications").glob("*.md"), reverse=True):
        fm, body = load_yaml_frontmatter(f)
        slug = fm.get("slug", f.stem)
        fm["slug"] = slug
        fm["url"] = f"/research/publications/{slug}/"
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["publications"].append(fm)

    for f in sorted((ROOT / "_events").glob("*.md")):
        fm, body = load_yaml_frontmatter(f)
        slug = fm.get("slug", f.stem)
        fm["slug"] = slug
        fm["url"] = f"/events/{slug}/"
        fm["date_dt"] = parse_date(fm.get("date"))
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["events"].append(fm)
    site["events"].sort(key=lambda x: str(x.get("date")), reverse=True)

    for f in sorted((ROOT / "_notices").glob("*.md"), reverse=True):
        fm, body = load_yaml_frontmatter(f)
        slug = fm.get("slug", f.stem)
        fm["slug"] = slug
        fm["url"] = f"/notices/{slug}/"
        fm["date_dt"] = parse_date(fm.get("date"))
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["notices"].append(fm)
    site["notices"].sort(key=lambda x: str(x.get("date")), reverse=True)

    for f in sorted((ROOT / "_courses").glob("*.md")):
        fm, body = load_yaml_frontmatter(f)
        slug = fm.get("code", f.stem).lower().replace(" ", "-")
        fm["slug"] = slug
        fm["url"] = f"/academics/courses/{slug}/"
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["raw_body"] = body
        site["courses"].append(fm)

    for f in sorted((ROOT / "_posts").glob("*.md"), reverse=True):
        fm, body = load_yaml_frontmatter(f)
        slug = f.stem[11:] if len(f.stem) > 11 and f.stem[:10].replace("-", "").isdigit() else f.stem
        date_obj = parse_date(fm.get("date") or f.stem[:10])
        fm["date_dt"] = date_obj
        fm["slug"] = slug
        fm["url"] = f"/news/{date_obj.strftime('%Y/%m/%d')}/{slug}/"
        fm["content_html"] = markdown.markdown(body, extensions=["extra", "tables"])
        fm["excerpt"] = fm.get("lead") or (body[:180] + "...")
        fm["raw_body"] = body
        site["posts"].append(fm)

    # 3. Load Layouts and Includes
    layouts = {}
    for l_file in (ROOT / "_layouts").glob("*.html"):
        fm, body = load_yaml_frontmatter(l_file)
        layouts[l_file.stem] = (fm, body)

    includes = {}
    for inc_file in (ROOT / "_includes").glob("*.html"):
        includes[inc_file.name] = inc_file.read_text(encoding="utf-8")

    # Template Filters
    def relative_url(url):
        if not url:
            return ""
        if str(url).startswith("/"):
            return site["baseurl"] + str(url)
        return site["baseurl"] + "/" + str(url)

    def date_filter(val, fmt="%B %d, %Y"):
        if isinstance(val, str):
            try:
                val = parse_date(val)
            except:
                return val
        if isinstance(val, datetime):
            return val.strftime(fmt.replace("%e", "%d").replace("%-d", "%d"))
        return str(val or "")

    def truncatewords(val, count=30):
        if not val:
            return ""
        words = str(val).split()
        if len(words) <= count:
            return " ".join(words)
        return " ".join(words[:count]) + "..."

    def strip_html(val):
        return re.sub(r"<[^>]*>", "", str(val or ""))

    def strip_newlines(val):
        return re.sub(r"[\r\n]+", " ", str(val or ""))

    def slice_str(val, start, length):
        s = str(val or "")
        return s[start:start+length]

    env = jinja2.Environment(autoescape=False)
    env.filters["relative_url"] = relative_url
    env.filters["absolute_url"] = lambda u: site["url"] + (u if str(u).startswith("/") else "/" + str(u))
    env.filters["date"] = date_filter
    env.filters["date_to_xmlschema"] = lambda d: parse_date(d).isoformat()
    env.filters["truncatewords"] = truncatewords
    env.filters["truncate"] = lambda val, n: (str(val)[:n] + "...") if len(str(val)) > n else str(val)
    env.filters["strip_html"] = strip_html
    env.filters["strip_newlines"] = strip_newlines
    env.filters["slice_str"] = slice_str
    env.filters["jsonify"] = lambda val: json.dumps(val)
    env.filters["join"] = lambda val, sep=", ": sep.join(val) if isinstance(val, list) else str(val or "")

    def render_layout_chain(layout_name, content_html, page_vars):
        if not layout_name or layout_name not in layouts or layout_name == "null":
            return content_html
        l_fm, l_body = layouts[layout_name]
        parent_layout = l_fm.get("layout")

        j_body = liquid_to_jinja(l_body, includes)
        template = env.from_string(j_body)
        rendered = template.render(
            content=content_html,
            page=page_vars,
            site=site,
        )

        if parent_layout and parent_layout != layout_name and parent_layout != "null":
            return render_layout_chain(parent_layout, rendered, page_vars)
        return rendered

    def write_output(target_url, html_content):
        clean_path = target_url.strip("/")
        if clean_path == "":
            out_file = SITE_DIR / "index.html"
        elif clean_path.endswith(".html") or clean_path.endswith(".xml") or clean_path.endswith(".txt") or clean_path.endswith(".json"):
            out_file = SITE_DIR / clean_path
        else:
            out_file = SITE_DIR / clean_path / "index.html"

        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html_content, encoding="utf-8")

    # 4. Render Top-Level Pages
    pages_to_render = [
        ("index.md", "/", "default"),
        ("about/index.md", "/about/", "page"),
        ("academics/index.md", "/academics/", "page"),
        ("research/index.md", "/research/", "page"),
        ("people/index.md", "/people/", "page"),
        ("admissions/index.md", "/admissions/", "page"),
        ("campus-life/index.md", "/campus-life/", "page"),
        ("news/index.md", "/news/", "page"),
        ("events/index.md", "/events/", "page"),
        ("notices/index.md", "/notices/", "page"),
        ("resources/index.md", "/resources/", "page"),
        ("contact/index.md", "/contact/", "page"),
        ("404.html", "/404.html", "default"),
        ("maintenance.html", "/maintenance.html", None),
    ]

    for rel_path, url, default_layout in pages_to_render:
        p_file = ROOT / rel_path
        if not p_file.exists():
            continue
        fm, body = load_yaml_frontmatter(p_file)
        fm["url"] = url
        layout = fm.get("layout", default_layout)
        
        j_body = liquid_to_jinja(body, includes)
        template = env.from_string(j_body)
        rendered_body = template.render(page=fm, site=site)
        
        if rel_path.endswith(".md"):
            content_html = markdown.markdown(rendered_body, extensions=["extra", "tables"])
        else:
            content_html = rendered_body

        final_html = render_layout_chain(layout, content_html, fm) if layout else content_html
        write_output(url, final_html)

    # 5. Render Collection Single Pages
    for member in site["faculty"]:
        member_vars = dict(member)
        member_vars["collection"] = "faculty"
        final_html = render_layout_chain("faculty", member["content_html"], member_vars)
        write_output(member["url"], final_html)

    for project in site["research"]:
        proj_vars = dict(project)
        proj_vars["collection"] = "research"
        final_html = render_layout_chain("research", project["content_html"], proj_vars)
        write_output(project["url"], final_html)

    for ev in site["events"]:
        ev_vars = dict(ev)
        ev_vars["collection"] = "events"
        final_html = render_layout_chain("event", ev["content_html"], ev_vars)
        write_output(ev["url"], final_html)

    for noti in site["notices"]:
        not_vars = dict(noti)
        not_vars["collection"] = "notices"
        final_html = render_layout_chain("notice", noti["content_html"], not_vars)
        write_output(noti["url"], final_html)

    for course in site["courses"]:
        course_vars = dict(course)
        course_vars["collection"] = "courses"
        final_html = render_layout_chain("course", course["content_html"], course_vars)
        write_output(course["url"], final_html)

    for post in site["posts"]:
        post_vars = dict(post)
        post_vars["collection"] = "posts"
        final_html = render_layout_chain("post", post["content_html"], post_vars)
        write_output(post["url"], final_html)

    # 6. Generate search.json
    search_items = []
    for item in site["faculty"]:
        search_items.append({
            "title": item.get("name"),
            "subtitle": f"{item.get('designation')} - {item.get('department')}",
            "category": "Faculty",
            "department": item.get("department"),
            "url": item.get("url"),
            "summary": ", ".join(item.get("research_interests", [])),
            "content": strip_html(item.get("raw_body"))[:200],
        })
    for item in site["research"]:
        search_items.append({
            "title": item.get("title"),
            "subtitle": f"{item.get('area')} | PI: {item.get('principal_investigator')}",
            "category": "Research",
            "department": item.get("department", "Interdisciplinary"),
            "url": item.get("url"),
            "summary": item.get("description", ""),
            "content": strip_html(item.get("raw_body"))[:200],
        })
    for item in site["courses"]:
        search_items.append({
            "title": f"{item.get('code')}: {item.get('title')}",
            "subtitle": f"{item.get('department')} - {item.get('credits')} Credits",
            "category": "Courses",
            "department": item.get("department"),
            "url": item.get("url"),
            "summary": item.get("description", ""),
            "content": strip_html(item.get("raw_body"))[:200],
        })
    for item in site["events"]:
        search_items.append({
            "title": item.get("title"),
            "subtitle": f"{item.get('category')} | {item.get('location')}",
            "category": "Events",
            "department": "Campus",
            "url": item.get("url"),
            "summary": f"{item.get('date')} - {item.get('time')}",
            "content": strip_html(item.get("raw_body"))[:200],
        })
    for item in site["notices"]:
        search_items.append({
            "title": item.get("title"),
            "subtitle": f"{item.get('category')} Notice | {item.get('ref_no')}",
            "category": "Notices",
            "department": item.get("department"),
            "url": item.get("url"),
            "summary": str(item.get("date")),
            "content": strip_html(item.get("raw_body"))[:200],
        })
    for item in site["posts"]:
        search_items.append({
            "title": item.get("title"),
            "subtitle": f"{item.get('category', 'News')} | {item.get('author')}",
            "category": "News",
            "department": "Institutional",
            "url": item.get("url"),
            "summary": item.get("excerpt", ""),
            "content": strip_html(item.get("raw_body"))[:200],
        })

    (SITE_DIR / "search.json").write_text(json.dumps(search_items, indent=2), encoding="utf-8")
    (SITE_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    # 7. Copy Assets
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", SITE_DIR / "assets", dirs_exist_ok=True)

    print(f"[+] Successfully generated {len(list(SITE_DIR.rglob('*.*')))} static files into _site/")


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE_DIR), **kwargs)

    def log_message(self, format, *args):
        pass


def serve(port=4000):
    build_site()
    
    actual_port = port
    httpd = None
    for p in range(port, port + 10):
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", p), QuietHandler)
            actual_port = p
            break
        except OSError:
            continue

    if not httpd:
        print(f"[!] Could not bind to port in range {port}-{port+10}")
        sys.exit(1)

    url = f"http://127.0.0.1:{actual_port}/"
    print("\n" + "=" * 60)
    print(f" InstituteHub Production Web Server Running Live!")
    print(f" Access URL : {url}")
    print(f" Document Root : {SITE_DIR}")
    print("=" * 60 + "\n")
    sys.stdout.flush()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")
        httpd.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    serve(port_arg)
