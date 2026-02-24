#!/usr/bin/env python3
"""
Generate the Mycal Terms page from individual JSON term files.

Usage:
    python3 generate_terms.py

Reads all *.json files from data/ directory, sorts alphabetically by slug
(derived from filename), and generates index.html with consistent HTML
and JSON-LD.

Directory structure:
    terms/
    ├── generate_terms.py    (this script)
    ├── index.html           (generated output)
    ├── README.md            (maintenance guide)
    └── data/
        ├── README.md        (data format docs)
        ├── cronofuturism.json
        ├── lords-of-zero.json
        └── ...
"""
import json
import os
import sys
from pathlib import Path

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
OUTPUT_FILE = SCRIPT_DIR / "index.html"


def load_terms():
    """Load all term JSON files from data/ directory."""
    if not DATA_DIR.exists():
        print(f"Error: data directory not found at {DATA_DIR}", file=sys.stderr)
        sys.exit(1)

    terms = []
    for filepath in sorted(DATA_DIR.glob("*.json")):
        slug = filepath.stem  # filename minus .json
        with open(filepath) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing {filepath.name}: {e}", file=sys.stderr)
                sys.exit(1)

        # Validate required fields
        for field in ("name", "date", "description", "links"):
            if field not in data:
                print(f"Error: {filepath.name} missing required field '{field}'", file=sys.stderr)
                sys.exit(1)

        terms.append({
            "slug": slug,
            "name": data["name"],
            "date": data["date"],
            "description": data["description"],
            "links": [(l["url"], l["label"]) for l in data["links"]],
            "sameAs": data.get("sameAs", []),
        })

    # Sort alphabetically by slug
    terms.sort(key=lambda t: t["slug"])
    return terms


def build_jsonld(terms):
    """Build the @graph JSON-LD structure."""
    graph = [
        # Person
        {
            "@type": "Person",
            "@id": "https://blog.mycal.net/about/#mycal",
            "name": "Mike Johnson",
            "givenName": "Michael",
            "familyName": "Johnson",
            "alternateName": ["Mycal", "Mike", "\u30de\u30a4\u30ab\u30eb", "mycal"],
            "identifier": [
                {"@type": "PropertyValue", "propertyID": "canonical-uuid", "value": "urn:uuid:4ff7ed97-b78f-4ae6-9011-5af714ee241c"},
                {"@type": "PropertyValue", "propertyID": "AnchorID", "value": "https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c"},
            ],
            "url": "https://www.mycal.net/",
            "sameAs": [
                "https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c",
                "https://www.mycal.net", "https://music.mycal.net", "https://blog.mycal.net",
                "https://archive.mycal.net", "https://github.com/lowerpower",
                "https://www.linkedin.com/in/mycal/", "https://x.com/mycal_1",
            ],
        },
        # Organization
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
        # WebSite
        {
            "@type": "WebSite",
            "@id": "https://www.mycal.net/#website",
            "name": "Mycal.net",
            "url": "https://www.mycal.net/",
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "mainEntity": {"@id": "https://blog.mycal.net/about/#mycal"},
        },
        # WebPage
        {
            "@type": "WebPage",
            "@id": "https://www.mycal.net/terms/#webpage",
            "url": "https://www.mycal.net/terms/",
            "name": "Mycal Terms \u2014 A Lexicon of Original Concepts",
            "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, and temporal methodology.",
            "isPartOf": {"@id": "https://www.mycal.net/#website"},
            "about": {"@id": "https://www.mycal.net/terms/#termset"},
            "author": {"@id": "https://blog.mycal.net/about/#mycal"},
            "publisher": {"@id": "https://blog.mycal.net/#publisher"},
            "dateCreated": "2026-02-22T00:00:00-08:00",
            "dateModified": "2026-02-22T00:00:00-08:00",
            "inLanguage": "en-US",
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        },
    ]

    # DefinedTermSet
    graph.append({
        "@type": "DefinedTermSet",
        "@id": "https://www.mycal.net/terms/#termset",
        "name": "Mycal Terms",
        "description": "Original terms and conceptual frameworks coined by Mike Johnson (Mycal), spanning cronofuturist philosophy, AI infrastructure, the Substrate War, evaluation methodology, and temporal methodology.",
        "url": "https://www.mycal.net/terms/",
        "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
        "publisher": {"@id": "https://blog.mycal.net/#publisher"},
        "inLanguage": "en-US",
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "hasDefinedTerm": [{"@id": f"https://www.mycal.net/terms/#{t['slug']}"} for t in terms],
    })

    # Individual DefinedTerms
    no_defined_in = {
        "https://blog.mycal.net/",
        "https://nobgp.com/",
        "https://anchorid.net/",
        "https://music.mycal.net/",
    }
    for t in terms:
        dt = {
            "@type": "DefinedTerm",
            "@id": f"https://www.mycal.net/terms/#{t['slug']}",
            "name": t["name"],
            "termCode": t["slug"],
            "description": t["description"],
            "inDefinedTermSet": {"@id": "https://www.mycal.net/terms/#termset"},
            "url": f"https://www.mycal.net/terms/#{t['slug']}",
            "creator": {"@id": "https://blog.mycal.net/about/#mycal"},
            "dateCreated": t["date"],
        }
        # Infer isDefinedIn from first link
        first_url = t["links"][0][0]
        if first_url not in no_defined_in:
            if "archive.mycal.net" in first_url:
                dt["isDefinedIn"] = {"@type": "DiscussionForumPosting", "@id": first_url}
            elif "tag/" in first_url:
                dt["isDefinedIn"] = {"@type": "CreativeWorkSeries", "@id": first_url}
            else:
                dt["isDefinedIn"] = {"@type": "Article", "@id": f"{first_url}#article"}
        if t["sameAs"]:
            dt["sameAs"] = t["sameAs"]
        graph.append(dt)

    # BreadcrumbList
    graph.append({
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.mycal.net/"},
            {"@type": "ListItem", "position": 2, "name": "Mycal Terms", "item": "https://www.mycal.net/terms/"},
        ],
    })

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)


def build_html_entries(terms):
    """Build the HTML term entry blocks."""
    entries = []
    for t in terms:
        links_html = "\n".join([
            f'          <a href="{url}" class="term-link" data-umami-event="term-{t["slug"]}-{i}">{label}</a>'
            for i, (url, label) in enumerate(t["links"])
        ])
        entries.append(f'''      <div class="term-entry" id="{t["slug"]}">
        <div class="term-name">{t["name"]}</div>
        <div class="term-meta"><span>First used: {t["date"]}</span></div>
        <p class="term-definition">{t["description"]}</p>
        <div class="term-links">
{links_html}
        </div>
      </div>''')
    return "\n\n".join(entries)


def build_page(terms, jsonld, html_entries):
    """Assemble the full HTML page."""
    count = len(terms)
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

<!-- Identity Graph + DefinedTermSet — www.mycal.net/terms/ -->
<script type="application/ld+json">
{jsonld}
</script>

</head>
<body>
  <div class="container">
    <header>
      <a href="/" class="back-link">\u2190 mycal.net</a>
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
        <input type="text" id="term-search" placeholder="Search terms\u2026" autocomplete="off" spellcheck="false">
        <button class="search-clear" id="search-clear" aria-label="Clear search">\u00d7</button>
        <span class="search-hint" id="search-hint">/</span>
        <div class="search-count" id="search-count" aria-live="polite"></div>
      </div>
    </header>

    <main id="terms-list">

{html_entries}

      <div class="no-results" id="no-results">No terms match your search.</div>
    </main>

    <footer>
      <p>\u00a9 2025 <a href="/">Mike Johnson (Mycal)</a>. Licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>.</p>
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

      // Debounced URL update
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

      // Debounced Umami search tracking (3+ chars, 500ms idle)
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

    // Keyboard shortcut: / to focus search
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

    // Support linking with ?q=term
    const params = new URLSearchParams(location.search);
    const qParam = params.get('q');
    if (qParam) {{
      input.value = qParam;
      doSearch(false);
    }}

    // Handle back/forward with ?q= changes
    window.addEventListener('popstate', () => {{
      const p = new URLSearchParams(location.search);
      input.value = p.get('q') || '';
      doSearch(false);
    }});

    // Hash navigation: scroll and pulse on direct link
    function handleHash() {{
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


def main():
    terms = load_terms()
    if not terms:
        print("No term files found in data/", file=sys.stderr)
        sys.exit(1)

    jsonld = build_jsonld(terms)
    html_entries = build_html_entries(terms)
    page = build_page(terms, jsonld, html_entries)

    with open(OUTPUT_FILE, "w") as f:
        f.write(page)

    print(f"Generated {len(terms)} terms \u2192 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

