# Mycal Terms — Maintenance Guide

This directory contains the **Mycal Terms** lexicon page at `www.mycal.net/terms/`.

## Structure

```
terms/
├── generate_terms.py    # Generator script
├── index.html           # Generated output (do not edit by hand)
├── README.md            # This file
└── data/
    ├── README.md        # Data format docs
    ├── cronofuturism.json
    ├── lords-of-zero.json
    └── ...              # One JSON file per term
```

`index.html` is fully generated — all HTML, CSS, JavaScript, and JSON-LD are produced by `generate_terms.py`. Do not edit it directly.

## Adding a Term

1. Create `your-term-slug.json` in `data/` (see `data/README.md` for format)
2. Run `python3 generate_terms.py`
3. Verify generated output:
   - `index.html`
   - `<slug>/index.html` (canonical term page)
   - `terms.json`
   - `terms.ndjson`
   - `sitemap-terms.xml`
4. Commit the new JSON file and regenerated outputs

The generator handles everything: HTML entries, JSON-LD graph, term count in the intro text, and alphabetical ordering.

## Generator Script

`generate_terms.py` reads all `data/*.json` files, sorts them case-insensitively by slug (filename minus `.json`), and produces:

- **Index page**: `index.html`
- **Term pages**: `<slug>/index.html` for each term
- **Alias redirects**: `<alias>/index.html` redirecting to canonical slugs
- **Machine exports**: `terms.json` and `terms.ndjson`
- **Terms sitemap**: `sitemap-terms.xml`
- **HTML entries**: Term cards with name, date, description, source links, and direct links to canonical term pages
- **Related term rendering**: Canonical term pages render `Related Terms` links when referenced slugs resolve
- **JSON-LD `@graph`**:
  - Index page: identity graph, WebPage, BreadcrumbList, DefinedTermSet, DefinedTerm nodes
  - Term page: identity graph + WebPage + DefinedTerm, including custom `related` term references when available
- **Client-side search**: Full search UI with live filtering (see below)
- **Umami analytics**: `data-umami-event` attributes on all term links

### JSON-LD Details

The generator emits:

- **Index page graph**: Person, Organization, WebSite, WebPage, BreadcrumbList, DefinedTermSet, plus one DefinedTerm per data file
- **Term page graph**: Person, Organization, WebSite, WebPage, DefinedTerm

The identity graph objects are hardcoded in the generator, not in the data files. They should stay in sync with blog.mycal.net:

- `Person` — `@id: https://blog.mycal.net/about/#mycal`
- `Organization` (Mycal Labs) — `@id: https://blog.mycal.net/#publisher`
- `WebSite` — `@id: https://www.mycal.net/#website`

## Search

The generated page includes full client-side search:

- Live filtering across term name, description, metadata, and link text
- Multi-word AND search (all words must match)
- Keyboard shortcuts: `/` to focus, `Escape` to clear
- URL state via `?q=` parameter with `history.replaceState`
- Results counter ("X of Y terms")
- Clear button and "no results" message
- Umami analytics tracking on searches (3+ chars, 500ms debounce)
- Hash navigation (`#slug`) for direct linking to individual terms
- Alias hash normalization (`#old-slug` rewrites to canonical slug)

## Naming Conventions

| Element | Pattern | Example |
|---|---|---|
| Data file | `slug.json` | `substrate-war.json` |
| HTML `id` | lowercase, hyphenated slug | `substrate-war` |
| JSON-LD `@id` | `https://www.mycal.net/terms/#` + slug | `https://www.mycal.net/terms/#substrate-war` |
| JSON-LD `termCode` | same as slug | `substrate-war` |
| Umami event | `term-` + slug + `-` + index | `term-substrate-war-0` |

## Metadata

- **License:** CC BY-SA 4.0
- **Canonical Person ID:** `https://blog.mycal.net/about/#mycal`
- **Canonical Person UUID:** `urn:uuid:4ff7ed97-b78f-4ae6-9011-5af714ee241c`
- **AnchorID:** `https://anchorid.net/resolve/4ff7ed97-b78f-4ae6-9011-5af714ee241c`
- **Publisher:** Mycal Labs (`https://blog.mycal.net/#publisher`)
- **Analytics:** Umami — `data-umami-event` on all links
- **DefinedTermSet @id:** `https://www.mycal.net/terms/#termset`

## Style Notes

- Definitions: 1-3 sentences, descriptive prose (not dictionary-style)
- "First used" dates: earliest known public usage (blog post, mailing list, patent filing)
- Source links: pill-style `.term-link` elements linking to originating work
- Case-insensitive alphabetical ordering throughout — no grouping or categorization
- `related` slugs are canonicalized through aliases for HTML, exports, and term-page JSON-LD; unresolved related slugs warn during generation
