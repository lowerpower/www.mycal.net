# Mycal Terms — Maintenance Guide

This directory contains the **Mycal Terms** lexicon page at `www.mycal.net/terms/`.

## Structure

Single file: `index.html` — contains all HTML, CSS, and JSON-LD inline.

The JSON-LD uses a single `@graph` array containing the identity graph (Person, Organization, WebSite), page metadata (WebPage), the term set (DefinedTermSet), each individual term (DefinedTerm), and navigation (BreadcrumbList). This matches the pattern used across all mycal.net domains.

Terms are listed **alphabetically** in both the HTML and the `hasDefinedTerm` array.

## Current Term Count: 55

## Generator Script

`generate_terms.py` in the repo root can regenerate `index.html` from its internal terms list. To add a term via the script, add a dict to the `TERMS` list (alphabetical position) and re-run. The script ensures perfect consistency between JSON-LD and HTML.

To add a term manually, update **three places** in `index.html`:

### 1. JSON-LD DefinedTerm (add to `@graph` array, alphabetical)

```json
{
  "@type": "DefinedTerm",
  "@id": "https://www.mycal.net/terms/#your-term-slug",
  "name": "Your Term Name",
  "termCode": "your-term-slug",
  "description": "Definition text. Keep identical to HTML version.",
  "inDefinedTermSet": { "@id": "https://www.mycal.net/terms/#termset" },
  "url": "https://www.mycal.net/terms/#your-term-slug",
  "creator": { "@id": "https://blog.mycal.net/about/#mycal" },
  "dateCreated": "YYYY",
  "isDefinedIn": { "@type": "Article", "@id": "https://blog.mycal.net/post-slug/#article" }
}
```

### 2. JSON-LD reference (add to `hasDefinedTerm` array, alphabetical)

```json
{ "@id": "https://www.mycal.net/terms/#your-term-slug" }
```

### 3. HTML entry (add in `<main>`, alphabetical position)

```html
<div class="term-entry" id="your-term-slug">
  <div class="term-name">Your Term Name</div>
  <div class="term-meta"><span>First used: YYYY</span></div>
  <p class="term-definition">Definition goes here. Must match JSON-LD description exactly.</p>
  <div class="term-links">
    <a href="https://blog.mycal.net/post-slug/" class="term-link" data-umami-event="term-slug-0">Post Title</a>
  </div>
</div>
```

## Naming Conventions

| Element | Pattern | Example |
|---|---|---|
| HTML `id` | lowercase, hyphenated slug | `substrate-war` |
| JSON-LD `@id` | `https://www.mycal.net/terms/#` + slug | `https://www.mycal.net/terms/#substrate-war` |
| JSON-LD `termCode` | same as slug | `substrate-war` |
| Umami event | `term-` + slug + `-` + index | `term-substrate-war-0` |

## Checklist for Adding a Term

- [ ] JSON-LD `DefinedTerm` object added to `@graph` array (alphabetical)
- [ ] JSON-LD `@id` reference added to `hasDefinedTerm` in `DefinedTermSet` (alphabetical)
- [ ] HTML `.term-entry` block added in `<main>` (alphabetical)
- [ ] `id` / `@id` / `termCode` / `url` all use the same slug
- [ ] `description` text is identical between HTML and JSON-LD
- [ ] `creator` references `https://blog.mycal.net/about/#mycal`
- [ ] `dateCreated` set to year (or specific date) of first known public usage
- [ ] `isDefinedIn` points to the originating blog post or work (if known)
- [ ] `dateModified` updated on the `WebPage` object in `@graph`
- [ ] At least one source link in `.term-links` pointing to originating work
- [ ] Umami `data-umami-event` attribute on each link
- [ ] Update term count in this README and in the page intro text

## Identity Graph

The `@graph` includes canonical identity objects. **Do not modify these** — they should stay in sync with blog.mycal.net:

- `Person` — `@id: https://blog.mycal.net/about/#mycal`
- `Organization` (Mycal Labs) — `@id: https://blog.mycal.net/#publisher`
- `WebSite` — `@id: https://www.mycal.net/#website`

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
- HTML `definition` and JSON-LD `description` must be identical
- Alphabetical ordering throughout — no grouping or categorization
- The intro paragraph includes the term count — update it when adding terms
