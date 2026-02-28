#!/usr/bin/env python3
"""
Generate the Mycal Terms page plus machine-consumable exports.

Usage:
    python3 generate_terms.py

Outputs:
- index.html (terms index)
- <slug>/index.html (canonical per-term pages)
- <alias>/index.html (alias redirects)
- terms.json
- terms.ndjson
- sitemap-terms.xml
"""

import json
import re
import sys
import uuid
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Dict, List

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_FILE = SCRIPT_DIR / "index.html"
TERMS_JSON_FILE = SCRIPT_DIR / "terms.json"
TERMS_NDJSON_FILE = SCRIPT_DIR / "terms.ndjson"
SITEMAP_TERMS_FILE = SCRIPT_DIR / "sitemap-terms.xml"

CANONICAL_BASE_URL = "https://www.mycal.net/terms/"
TERM_ID_RE = re.compile(r"^urn:uuid:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def canonical_term_url(slug: str) -> str:
    return f"{CANONICAL_BASE_URL}{slug}/"


def parse_iso_date(value: str, field: str, filename: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        fail(f"{filename} has invalid {field} '{value}' (expected YYYY-MM-DD)")


def validate_term_types(data: dict, filename: str) -> None:
    for field in ("name", "date", "description", "links"):
        if field not in data:
            fail(f"{filename} missing required field '{field}'")

    if not isinstance(data["name"], str) or not data["name"].strip():
        fail(f"{filename} field 'name' must be a non-empty string")
    if not isinstance(data["date"], str) or not data["date"].strip():
        fail(f"{filename} field 'date' must be a non-empty string")
    if not isinstance(data["description"], str) or not data["description"].strip():
        fail(f"{filename} field 'description' must be a non-empty string")

    links = data["links"]
    if not isinstance(links, list) or not links:
        fail(f"{filename} field 'links' must be a non-empty array")
    for i, link in enumerate(links):
        if not isinstance(link, dict):
            fail(f"{filename} links[{i}] must be an object")
        if "url" not in link or "label" not in link:
            fail(f"{filename} links[{i}] must include 'url' and 'label'")
        if not isinstance(link["url"], str) or not link["url"].strip():
            fail(f"{filename} links[{i}].url must be a non-empty string")
        if not isinstance(link["label"], str) or not link["label"].strip():
            fail(f"{filename} links[{i}].label must be a non-empty string")

    if "sameAs" in data:
        if not isinstance(data["sameAs"], list) or not all(isinstance(s, str) and s.strip() for s in data["sameAs"]):
            fail(f"{filename} field 'sameAs' must be an array of non-empty strings")

    if "aliases" in data:
        if not isinstance(data["aliases"], list) or not all(isinstance(a, str) and a.strip() for a in data["aliases"]):
            fail(f"{filename} field 'aliases' must be an array of non-empty strings")

    if "termId" in data and (not isinstance(data["termId"], str) or not TERM_ID_RE.match(data["termId"])):
        fail(f"{filename} field 'termId' must match urn:uuid:<uuid-v4-like-format>")

    if "temporalCoverage" in data and (not isinstance(data["temporalCoverage"], str) or not data["temporalCoverage"].strip()):
        fail(f"{filename} field 'temporalCoverage' must be a non-empty string")
    if "startDate" in data:
        if not isinstance(data["startDate"], str):
            fail(f"{filename} field 'startDate' must be a string")
        parse_iso_date(data["startDate"], "startDate", filename)
    if "endDate" in data:
        if not isinstance(data["endDate"], str):
            fail(f"{filename} field 'endDate' must be a string")
        parse_iso_date(data["endDate"], "endDate", filename)
    if "dateISO" in data:
        if not isinstance(data["dateISO"], str):
            fail(f"{filename} field 'dateISO' must be a string")
        parse_iso_date(data["dateISO"], "dateISO", filename)


def write_json_file(filepath: Path, data: dict) -> None:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except OSError as e:
        fail(f"could not write {filepath.name} while assigning termId: {e}")


def normalize_term_file(filepath: Path, data: dict) -> str:
    term_id = data.get("termId")
    if term_id:
        return term_id

    term_id = f"urn:uuid:{uuid.uuid4()}"
    data["termId"] = term_id
    write_json_file(filepath, data)
    return term_id


def load_terms() -> List[dict]:
    """Load all term JSON files from data/ directory and assign missing termIds."""
    if not DATA_DIR.exists():
        fail(f"data directory not found at {DATA_DIR}")

    terms = []
    for filepath in sorted(DATA_DIR.glob("*.json")):
        slug = filepath.stem
        try:
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            fail(f"parsing {filepath.name}: {e}")
        except OSError as e:
            fail(f"reading {filepath.name}: {e}")

        validate_term_types(data, filepath.name)
        term_id = normalize_term_file(filepath, data)

        terms.append(
            {
                "slug": slug,
                "name": data["name"],
                "date": data["date"],
                "description": data["description"],
                "links": [{"url": l["url"], "label": l["label"]} for l in data["links"]],
                "sameAs": data.get("sameAs", []),
                "aliases": data.get("aliases", []),
                "termId": term_id,
                "temporalCoverage": data.get("temporalCoverage"),
                "startDate": data.get("startDate"),
                "endDate": data.get("endDate"),
                "dateISO": data.get("dateISO"),
                "source_mtime": datetime.fromtimestamp(filepath.stat().st_mtime, tz=timezone.utc),
            }
        )

    terms.sort(key=lambda t: t["slug"])
    return terms


def build_alias_map(terms: List[dict]) -> Dict[str, str]:
    canonical_slugs = {t["slug"] for t in terms}
    alias_map: Dict[str, str] = {}

    for t in terms:
        for alias in t["aliases"]:
            if alias in canonical_slugs:
                fail(f"alias collision: '{alias}' is also a canonical slug")
            existing = alias_map.get(alias)
            if existing and existing != t["slug"]:
                fail(f"alias collision: '{alias}' maps to both '{existing}' and '{t['slug']}'")
            alias_map[alias] = t["slug"]

    return alias_map


def apply_machine_dates(node: dict, term: dict) -> None:
    if term.get("temporalCoverage"):
        node["temporalCoverage"] = term["temporalCoverage"]
    if term.get("startDate"):
        node["startDate"] = term["startDate"]
    if term.get("endDate"):
        node["endDate"] = term["endDate"]
    if term.get("dateISO"):
        node["datePublished"] = term["dateISO"]


def build_defined_term_node(term: dict) -> dict:
    node = {
        "@type": "DefinedTerm",
        "@id": f"{CANONICAL_BASE_URL}#{term['slug']}",
        "name": term["name"],
        "termCode": term["slug"],
        "description": term["description"],
        "inDefinedTermSet": {"@id": f"{CANONICAL_BASE_URL}#termset"},
        "url": canonical_term_url(term["slug"]),
        "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
        "dateCreated": term["date"],
        "identifier": {
            "@type": "PropertyValue",
            "propertyID": "term-uuid",
            "value": term["termId"],
        },
    }

    no_defined_in = {
        "https://blog.mycal.net/",
        "https://nobgp.com/",
        "https://anchorid.net/",
        "https://music.mycal.net/",
    }
    first_url = term["links"][0]["url"]
    if first_url not in no_defined_in:
        if "archive.mycal.net" in first_url:
            node["isDefinedIn"] = {"@type": "DiscussionForumPosting", "@id": first_url}
        elif "tag/" in first_url:
            node["isDefinedIn"] = {"@type": "CreativeWorkSeries", "@id": first_url}
        else:
            node["isDefinedIn"] = {"@type": "Article", "@id": f"{first_url}#article"}

    if term["sameAs"]:
        node["sameAs"] = term["sameAs"]

    apply_machine_dates(node, term)
    return node


def build_jsonld(terms: List[dict]) -> str:
    """Build the @graph JSON-LD structure for index.html."""
    graph = [
        {
            "@type": "Person",
            "@id": "https://blog.mycal.net/about/#mycal",
            "name": "Mike Johnson",
            "givenName": "Michael",
            "familyName": "Johnson",
            "alternateName": ["Mycal", "Mike", "マイカル", "mycal"],
            "identifier": [
                {"@type": "PropertyValue", "propertyID": "canonical-uuid", "value": "urn:uuid:4ff7ed97-b78f-4ae6-9011-5af714ee241c"},
                {"@type": "PropertyValue", "propertyID": "AnchorID", "value": "https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c"},
            ],
            "url": "https://www.mycal.net/",
            "sameAs": [
                "https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c",
                "https://www.mycal.net",
                "https://music.mycal.net",
                "https://blog.mycal.net",
                "https://archive.mycal.net",
                "https://github.com/lowerpower",
                "https://www.linkedin.com/in/mycal/",
                "https://x.com/mycal_1",
            ],
        },
        {
            "@type": "Organization",
            "@id": "https://blog.mycal.net/#publisher",
            "name": "Mycal Labs",
            "identifier": [
                {"@type": "PropertyValue", "propertyID": "canonical-uuid", "value": "urn:uuid:bbf7372e-87d3-4098-8e60-f4e24d027a04"},
                {"@type": "PropertyValue", "propertyID": "AnchorID", "value": "https://anchorid.net/resolve/bbf7372e-87d3-4098-8e60-f4e24d027a04"},
            ],
            "url": "https://blog.mycal.net/",
            "founder": {"@id": "https://blog.mycal.net/about/#mycal"},
            "sameAs": ["https://anchorid.net/resolve/bbf7372e-87d3-4098-8e60-f4e24d027a04"],
        },
        {
            "@type": "WebSite",
            "@id": "https://www.mycal.net/#website",
            "name": "Mycal.net",
            "url": "https://www.mycal.net/",
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "mainEntity": {"@id": "https://blog.mycal.net/about/#mycal"},
        },
        {
            "@type": "WebPage",
            "@id": f"{CANONICAL_BASE_URL}#webpage",
            "url": CANONICAL_BASE_URL,
            "name": "Mycal Terms — A Lexicon of Original Concepts",
            "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, and temporal methodology.",
            "isPartOf": {"@id": "https://www.mycal.net/#website"},
            "about": {"@id": f"{CANONICAL_BASE_URL}#termset"},
            "author": {"@id": "https://blog.mycal.net/about/#mycal"},
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "dateCreated": "2026-02-22T00:00:00-08:00",
            "dateModified": "2026-02-22T00:00:00-08:00",
            "inLanguage": "en-US",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        },
        {
            "@type": "DefinedTermSet",
            "@id": f"{CANONICAL_BASE_URL}#termset",
            "name": "Mycal Terms",
            "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, evaluation methodology, and temporal methodology.",
            "url": CANONICAL_BASE_URL,
            "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "inLanguage": "en-US",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            "hasDefinedTerm": [{"@id": f"{CANONICAL_BASE_URL}#{t['slug']}"} for t in terms],
        },
    ]

    for term in terms:
        graph.append(build_defined_term_node(term))

    graph.append(
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mycal.net/"},
                {"@type": "ListItem", "position": 2, "name": "Mycal Terms", "item": CANONICAL_BASE_URL},
            ],
        }
    )

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def build_html_entries(terms: List[dict]) -> str:
    entries = []
    for t in terms:
        links_html = "\n".join(
            [
                f'          <a href="{escape(link["url"])}" class="term-link" data-umami-event="term-{t["slug"]}-{i}">{escape(link["label"])}</a>'
                for i, link in enumerate(t["links"])
            ]
        )
        entries.append(
            f'''      <div class="term-entry" id="{t["slug"]}">
        <div class="term-name">{escape(t["name"])}</div>
        <div class="term-meta"><span>First used: {escape(t["date"])}</span></div>
        <p class="term-definition">{escape(t["description"])}</p>
        <div class="term-links">
{links_html}
        </div>
      </div>'''
        )
    return "\n\n".join(entries)


def build_page(terms: List[dict], jsonld: str, html_entries: str, alias_map: Dict[str, str]) -> str:
    count = len(terms)
    alias_map_json = json.dumps(alias_map, separators=(",", ":"))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mycal Terms — A Lexicon of Original Concepts</title>
  <meta name="description" content="Original terms and concepts coined by Mike Johnson (Mycal) — {count} original frameworks spanning cronofuturist philosophy, AI infrastructure, the Substrate War, and more.">
  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

  <script defer src="https://analytics.mycal.net/script.js" data-website-id="cd13ff4f-ac2e-4f4e-ad21-2ae1a2f83595"></script>

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      line-height: 1.6; color: #e0e0e0;
      background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
      min-height: 100vh; padding: 2rem;
    }}
    .container {{ max-width: 800px; width: 100%; margin: 0 auto; }}
    header {{ text-align: center; margin-bottom: 3rem; }}
    .back-link {{
      display: inline-block; color: #999; text-decoration: none;
      font-size: 0.9rem; margin-bottom: 1.5rem; transition: color 0.3s ease;
    }}
    .back-link:hover {{ color: #f6a441; }}
    h1 {{
      font-size: clamp(2rem, 5vw, 3rem); font-weight: 700; margin-bottom: 0.5rem;
      background: linear-gradient(135deg, #f6a441 0%, #ff6b35 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }}
    .subtitle {{ font-size: clamp(1rem, 2.5vw, 1.15rem); color: #999; margin-bottom: 1rem; }}
    .intro {{ font-size: 1.05rem; color: #ccc; margin-bottom: 2rem; line-height: 1.8; text-align: center; }}
    .search-wrap {{
      position: relative; max-width: 480px; margin: 0 auto 2.5rem;
    }}
    .search-icon {{
      position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
      width: 18px; height: 18px; color: #666; pointer-events: none;
    }}
    #term-search {{
      width: 100%; padding: 0.7rem 2.6rem;
      font-size: 1rem; color: #e0e0e0;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px; outline: none;
      transition: border-color 0.3s ease, background 0.3s ease;
    }}
    #term-search::placeholder {{ color: #666; }}
    #term-search:focus {{
      border-color: rgba(246, 164, 65, 0.5);
      background: rgba(255, 255, 255, 0.07);
    }}
    .search-clear {{
      position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
      width: 20px; height: 20px; border: none; background: none;
      color: #666; cursor: pointer; padding: 0; display: none;
      font-size: 18px; line-height: 1;
    }}
    .search-clear:hover {{ color: #e0e0e0; }}
    .search-clear.visible {{ display: block; }}
    .search-hint {{
      position: absolute; right: 12px; top: 50%; transform: translateY(-50%);
      font-size: 0.75rem; color: #555; pointer-events: none;
      border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 4px;
      padding: 0.1rem 0.4rem; font-family: monospace;
    }}
    .search-hint.hidden {{ display: none; }}
    .search-count {{
      text-align: center; font-size: 0.85rem; color: #666;
      margin-top: 0.5rem; min-height: 1.3em;
    }}
    .term-entry {{
      background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; transition: all 0.3s ease;
    }}
    .term-entry:hover {{ background: rgba(255, 255, 255, 0.06); border-color: rgba(246, 164, 65, 0.3); }}
    .term-entry.hidden {{ display: none; }}
    .term-entry:target {{
      border-color: rgba(246, 164, 65, 0.6);
      animation: target-pulse 2s ease-out;
    }}
    @keyframes target-pulse {{
      0% {{ background: rgba(246, 164, 65, 0.15); border-color: #f6a441; }}
      100% {{ background: rgba(255, 255, 255, 0.03); border-color: rgba(246, 164, 65, 0.6); }}
    }}
    .term-name {{ font-size: 1.35rem; font-weight: 700; color: #f6a441; margin-bottom: 0.25rem; }}
    .term-meta {{ font-size: 0.8rem; color: #777; margin-bottom: 0.75rem; }}
    .term-meta span {{ margin-right: 1rem; }}
    .term-definition {{ font-size: 1rem; color: #ccc; line-height: 1.7; margin-bottom: 0.75rem; }}
    .term-links {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
    .term-link {{
      font-size: 0.8rem; color: #f6a441; text-decoration: none;
      background: rgba(246, 164, 65, 0.08); border: 1px solid rgba(246, 164, 65, 0.2);
      border-radius: 6px; padding: 0.2rem 0.6rem; transition: all 0.3s ease;
    }}
    .term-link:hover {{ background: rgba(246, 164, 65, 0.15); border-color: #f6a441; }}
    .no-results {{
      text-align: center; color: #666; font-size: 1.05rem;
      padding: 3rem 1rem; display: none;
    }}
    footer {{
      text-align: center; color: #666; font-size: 0.875rem;
      padding-top: 2rem; margin-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}
    footer a {{ color: #999; text-decoration: none; transition: color 0.3s ease; }}
    footer a:hover {{ color: #f6a441; }}
    @media (max-width: 480px) {{
      body {{ padding: 1rem; }}
      .term-entry {{ padding: 1.2rem; }}
      .search-hint {{ display: none; }}
    }}
  </style>

<script type="application/ld+json">
{jsonld}
</script>

</head>
<body>
  <div class="container">
    <header>
      <a href="/" class="back-link">← mycal.net</a>
      <h1>Mycal Terms</h1>
      <p class="subtitle">A Lexicon of Original Concepts</p>
      <p class="intro">
        {count} terms and frameworks that emerged from decades of building, writing, and exploring
        at the intersection of infrastructure, philosophy, and culture. Each links back
        to the work where it first appeared.
      </p>
      <div class="search-wrap" role="search">
        <svg class="search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="8.5" cy="8.5" r="6"/>
          <line x1="13" y1="13" x2="18" y2="18"/>
        </svg>
        <input type="text" id="term-search" placeholder="Search terms…" autocomplete="off" spellcheck="false">
        <button class="search-clear" id="search-clear" aria-label="Clear search">×</button>
        <span class="search-hint" id="search-hint">/</span>
        <div class="search-count" id="search-count" aria-live="polite"></div>
      </div>
    </header>

    <main id="terms-list">

{html_entries}

      <div class="no-results" id="no-results">No terms match your search.</div>
    </main>

    <footer>
      <p>© 2025 <a href="/">Mike Johnson (Mycal)</a>. Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>
    </footer>
  </div>

  <script>
  (() => {{
    const input = document.getElementById('term-search');
    const clearBtn = document.getElementById('search-clear');
    const hint = document.getElementById('search-hint');
    const entries = document.querySelectorAll('.term-entry');
    const noResults = document.getElementById('no-results');
    const countEl = document.getElementById('search-count');
    const total = entries.length;
    const aliasMap = {alias_map_json};

    let urlTimer = null;
    let umamiTimer = null;

    function updateClearBtn() {{
      const hasText = input.value.length > 0;
      clearBtn.classList.toggle('visible', hasText);
      hint.classList.toggle('hidden', hasText || document.activeElement === input);
    }}

    function doSearch(updateUrl) {{
      const q = input.value.trim().toLowerCase();
      updateClearBtn();

      if (updateUrl !== false) {{
        clearTimeout(urlTimer);
        urlTimer = setTimeout(() => {{
          const url = new URL(location.href);
          if (q) {{
            url.searchParams.set('q', input.value.trim());
          }} else {{
            url.searchParams.delete('q');
          }}
          if (url.href !== location.href) {{
            history.replaceState(null, '', url);
          }}
        }}, 300);
      }}

      if (!q) {{
        entries.forEach(el => el.classList.remove('hidden'));
        noResults.style.display = 'none';
        countEl.textContent = '';
        return;
      }}
      const words = q.split(/\\s+/);
      let visible = 0;
      entries.forEach(el => {{
        const text = (
          el.querySelector('.term-name').textContent + ' ' +
          el.querySelector('.term-definition').textContent + ' ' +
          el.querySelector('.term-meta').textContent + ' ' +
          (el.querySelector('.term-links') ? el.querySelector('.term-links').textContent : '')
        ).toLowerCase();
        const match = words.every(w => text.includes(w));
        el.classList.toggle('hidden', !match);
        if (match) visible++;
      }});
      noResults.style.display = visible === 0 ? 'block' : 'none';
      countEl.textContent = visible === total ? '' : visible + ' of ' + total + ' terms';

      clearTimeout(umamiTimer);
      if (q.length >= 3 && window.umami) {{
        umamiTimer = setTimeout(() => {{
          try {{
            window.umami.track('Term Search', {{
              query: input.value.trim().slice(0, 100),
              results: visible,
            }});
          }} catch {{}}
        }}, 500);
      }}
    }}

    input.addEventListener('input', () => doSearch());
    input.addEventListener('focus', () => {{ hint.classList.add('hidden'); }});
    input.addEventListener('blur', () => {{ if (!input.value) hint.classList.remove('hidden'); }});

    clearBtn.addEventListener('click', () => {{
      input.value = '';
      doSearch();
      input.focus();
    }});

    document.addEventListener('keydown', (e) => {{
      if (e.key === '/' && document.activeElement !== input &&
          !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {{
        e.preventDefault();
        input.focus();
      }}
      if (e.key === 'Escape' && document.activeElement === input) {{
        input.value = '';
        doSearch();
        input.blur();
      }}
    }});

    const params = new URLSearchParams(location.search);
    const qParam = params.get('q');
    if (qParam) {{
      input.value = qParam;
      doSearch(false);
    }}

    window.addEventListener('popstate', () => {{
      const p = new URLSearchParams(location.search);
      input.value = p.get('q') || '';
      doSearch(false);
    }});

    function resolveAliasHash() {{
      if (!location.hash) return;
      const slug = location.hash.slice(1);
      const canonical = aliasMap[slug];
      if (canonical) {{
        history.replaceState(null, '', '#' + canonical);
      }}
    }}

    function handleHash() {{
      resolveAliasHash();
      if (!location.hash) return;
      const target = document.querySelector(location.hash);
      if (target && target.classList.contains('term-entry')) {{
        if (input.value) {{
          input.value = '';
          doSearch(false);
        }}
        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
      }}
    }}

    handleHash();
    window.addEventListener('hashchange', handleHash);
  }})();
  </script>
</body>
</html>'''


def short_description(text: str, max_len: int = 160) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1].rstrip() + "…"


def build_term_page_jsonld(term: dict) -> str:
    graph = [
        {
            "@type": "WebPage",
            "@id": f"{canonical_term_url(term['slug'])}#webpage",
            "url": canonical_term_url(term["slug"]),
            "name": f"{term['name']} — Mycal Terms",
            "description": short_description(term["description"], 200),
            "isPartOf": {"@id": "https://www.mycal.net/#website"},
            "mainEntity": {"@id": f"{CANONICAL_BASE_URL}#{term['slug']}"},
            "author": {"@id": "https://blog.mycal.net/about/#mycal"},
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "inLanguage": "en-US",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        },
        build_defined_term_node(term),
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def build_term_page(term: dict) -> str:
    term_url = canonical_term_url(term["slug"])
    description = short_description(term["description"], 160)
    links_html = "\n".join(
        [f'          <a href="{escape(link["url"])}" class="term-link">{escape(link["label"])}</a>' for link in term["links"]]
    )
    jsonld = build_term_page_jsonld(term)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mycal Term — {escape(term["name"])}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{term_url}">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      line-height: 1.6; color: #e0e0e0;
      background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
      min-height: 100vh; padding: 2rem;
    }}
    .container {{ max-width: 800px; width: 100%; margin: 0 auto; }}
    .back-link {{ display: inline-block; color: #999; text-decoration: none; margin-bottom: 1.25rem; }}
    .back-link:hover {{ color: #f6a441; }}
    h1 {{ font-size: clamp(1.8rem, 4vw, 2.5rem); color: #f6a441; margin-bottom: 0.35rem; }}
    .meta {{ color: #888; font-size: 0.95rem; margin-bottom: 1.25rem; }}
    .definition {{ color: #ccc; font-size: 1.05rem; line-height: 1.8; margin-bottom: 1.2rem; }}
    .term-links {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
    .term-link {{
      font-size: 0.85rem; color: #f6a441; text-decoration: none;
      background: rgba(246, 164, 65, 0.08); border: 1px solid rgba(246, 164, 65, 0.2);
      border-radius: 6px; padding: 0.25rem 0.65rem;
    }}
    .term-link:hover {{ background: rgba(246, 164, 65, 0.15); border-color: #f6a441; }}
  </style>
  <script type="application/ld+json">
{jsonld}
  </script>
</head>
<body>
  <main class="container">
    <a href="/terms/" class="back-link">← Back to Mycal Terms</a>
    <h1>{escape(term["name"])}</h1>
    <p class="meta">First used: {escape(term["date"])}</p>
    <p class="definition">{escape(term["description"])}</p>
    <div class="term-links">
{links_html}
    </div>
  </main>
</body>
</html>'''


def build_alias_redirect_page(alias: str, canonical_slug: str) -> str:
    canonical = canonical_term_url(canonical_slug)
    title = f"Redirecting to {canonical_slug}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0; url={canonical}">
  <script>location.replace({json.dumps(canonical)});</script>
</head>
<body>
  <p>Redirecting to <a href="{canonical}">{canonical}</a>.</p>
</body>
</html>'''


def write_file(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(contents)


def write_term_pages(terms: List[dict]) -> None:
    for term in terms:
        out = SCRIPT_DIR / term["slug"] / "index.html"
        write_file(out, build_term_page(term))


def write_alias_redirects(alias_map: Dict[str, str]) -> None:
    for alias, canonical_slug in alias_map.items():
        out = SCRIPT_DIR / alias / "index.html"
        write_file(out, build_alias_redirect_page(alias, canonical_slug))


def export_terms(terms: List[dict]) -> None:
    objects = []
    for term in terms:
        obj = {
            "slug": term["slug"],
            "name": term["name"],
            "date": term["date"],
            "description": term["description"],
            "links": term["links"],
            "sameAs": term["sameAs"],
            "aliases": term["aliases"],
            "termId": term["termId"],
            "canonicalUrl": canonical_term_url(term["slug"]),
        }
        for field in ("temporalCoverage", "startDate", "endDate", "dateISO"):
            if term.get(field):
                obj[field] = term[field]
        objects.append(obj)

    with open(TERMS_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(objects, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(TERMS_NDJSON_FILE, "w", encoding="utf-8") as f:
        for obj in objects:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def write_sitemap_terms(terms: List[dict]) -> None:
    index_lastmod = max(t["source_mtime"] for t in terms).date().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url>",
        f"    <loc>{CANONICAL_BASE_URL}</loc>",
        f"    <lastmod>{index_lastmod}</lastmod>",
        "  </url>",
    ]

    for term in terms:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{canonical_term_url(term['slug'])}</loc>",
                f"    <lastmod>{term['source_mtime'].date().isoformat()}</lastmod>",
                "  </url>",
            ]
        )

    lines.append("</urlset>")
    write_file(SITEMAP_TERMS_FILE, "\n".join(lines) + "\n")


def main() -> None:
    terms = load_terms()
    if not terms:
        fail("no term files found in data/")

    alias_map = build_alias_map(terms)
    jsonld = build_jsonld(terms)
    html_entries = build_html_entries(terms)
    page = build_page(terms, jsonld, html_entries, alias_map)

    write_file(OUTPUT_FILE, page)
    write_term_pages(terms)
    write_alias_redirects(alias_map)
    export_terms(terms)
    write_sitemap_terms(terms)

    print(f"Generated {len(terms)} terms -> {OUTPUT_FILE}")
    print(f"Generated per-term pages in {SCRIPT_DIR}")
    print(f"Generated exports -> {TERMS_JSON_FILE}, {TERMS_NDJSON_FILE}")
    print(f"Generated sitemap -> {SITEMAP_TERMS_FILE}")
    print(f"Generated alias redirects -> {len(alias_map)}")


if __name__ == "__main__":
    main()
