# terms/data/ — Term Definition Files

Each JSON file in this directory defines one term in the [Mycal Terms](https://www.mycal.net/terms/) lexicon.

## File Naming

Filename **must** match the term's slug: `your-term-slug.json`

This slug is used everywhere:
- HTML `id` attribute
- JSON-LD `@id` fragment (`https://www.mycal.net/terms/#your-term-slug`)
- JSON-LD `termCode`
- Umami event prefix

## File Format

```json
{
  "name": "Your Term Name",
  "date": "YYYY",
  "description": "1-3 sentence definition. Descriptive prose, not dictionary-style.",
  "links": [
    {
      "url": "https://blog.mycal.net/originating-post/",
      "label": "Originating Post Title"
    }
  ]
}
```

### Required Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Display name of the term |
| `date` | string | Year or specific date of first known public usage |
| `description` | string | Definition text (1-3 sentences, descriptive prose) |
| `links` | array | At least one source link to originating work |

### Optional Fields

| Field | Type | Description |
|---|---|---|
| `sameAs` | array of strings | URLs where this term is also defined (e.g., `["https://anchorid.net/"]`) |

### Link Objects

Each link in the `links` array has:

| Field | Type | Description |
|---|---|---|
| `url` | string | Full URL to the originating work |
| `label` | string | Short display label for the pill link |

The **first link** is treated as the primary origin. The generator uses it to build the `isDefinedIn` JSON-LD property:
- Blog post URLs → `{"@type": "Article", "@id": "URL#article"}`
- Archive URLs → `{"@type": "DiscussionForumPosting", "@id": "URL"}`
- Tag/series URLs → `{"@type": "CreativeWorkSeries", "@id": "URL"}`
- Other URLs (nobgp.com, anchorid.net, blog root) → no `isDefinedIn` generated

## Example

**`singularity-grade-ai.json`**

```json
{
  "name": "Singularity-grade AI",
  "date": "November 2, 1994",
  "description": "AI systems that rewrite themselves, operate with source code in flux, and see further and faster than humans ever will. Distinct from constraint-based 'safe' AI. Term coined November 2, 1994 in the Future Culture mailing list.",
  "links": [
    {
      "url": "https://archive.mycal.net/usenet/raw/mailing-lists/futureCulture/fc-Wed-02-Nov-1994-01:42:33-PST.txt",
      "label": "1994 Future Culture post"
    },
    {
      "url": "https://blog.mycal.net/the-lords-of-zero/",
      "label": "The Lords of Zero"
    }
  ]
}
```

## Adding a New Term

1. Create `your-term-slug.json` in this directory
2. Run `python3 generate_terms.py` from the repo root
3. Verify the output `terms/index.html`
4. Commit both the JSON file and the regenerated HTML

## Notes

- The slug is derived from the filename (minus `.json`), not from any field in the file
- The generator sorts all terms alphabetically by slug
- The generator builds both HTML entries and the full `@graph` JSON-LD from these files
- Identity graph objects (Person, Organization, WebSite) are hardcoded in the generator, not in these files
- Term count in the page intro is calculated automatically
