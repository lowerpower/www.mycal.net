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

## Current Term Count: 60

## Adding a Term

1. Create `your-term-slug.json` in `data/` (see `data/README.md` for format)
2. Run `python3 generate_terms.py`
3. Verify the output in `index.html`
4. Commit both the new JSON file and the regenerated HTML

The generator handles everything: HTML entries, JSON-LD graph, term count in the intro text, and alphabetical ordering.

## Generator Script

`generate_terms.py` reads all `data/*.json` files, sorts them alphabetically by slug (filename minus `.json`), and produces `index.html` with:

- **HTML entries**: Term cards with name, date, description, and source links
- **JSON-LD `@graph`**: Identity graph (Person, Organization, WebSite), WebPage, BreadcrumbList, DefinedTermSet, and one DefinedTerm per term file
- **Client-side search**: Full search UI with live filtering (see below)
- **Umami analytics**: `data-umami-event` attributes on all term links

### JSON-LD Details

The `build_jsonld()` function generates a `@graph` containing:

- **Static entities**: Person (Mike Johnson), Organization (Mycal Labs), WebSite (mycal.net), WebPage, BreadcrumbList
- **Dynamic entities**: DefinedTermSet + one DefinedTerm per data file, with smart `isDefinedIn` inference from the first link URL

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
- Alphabetical ordering throughout — no grouping or categorization
