# SLDB templates

This guide is a human-facing materialization of these atoms:

- `desk/atoms/atom-sldb-template-markers-declare-where-each-field-lives.md`
- `desk/atoms/atom-sldb-extraction-reads-values-relative-to-the-template-s-own-text.md`
- `desk/atoms/atom-instructional-text-makes-a-template-self-sufficient.md`
- `desk/atoms/atom-templates-are-defined-as-model-strings.md`
- `desk/atoms/atom-do-not-use-instructional-text-as-model-documentation.md`

## What a template is

Each `StructuredNLDoc` model carries a `__template__`: a multiline string that
places every field in the Markdown document that represents it. The store
tracks the documents, not the templates.

## Markers

| Marker | Meaning |
| --- | --- |
| `⸢rev•field⸥` | Required scalar. Rendered from the value and read back from the same place. |
| `⸢optrev•field⸥` | Optional scalar. When the value is `None` the marker leaves **no trace at all** in the document, so extraction returns the field absent and the model applies its default. |
| `⸢rev,list•field⸥` | List, rendered as `- item` lines. |
| `⸢rev,dict•field⸥` | Mapping, rendered as a YAML block. |
| `⸢render•field⸥` | Composed projection. Written on render, never extracted. |

`optrev` is what makes optional fields safe: a document that does not mention
the field is still valid, and no marker text is left behind for a reader to
find.

## Fixed text is the anchor, not decoration

`TemplateExtractor` turns a template into recipes that pair each marker with the
text around it, and `DataExtractor` reads a document through those recipes. The
consequence matters more than it looks:

> A document that has a section but not the template's fixed text extracts as
> **empty** for that field. Reading it looks fine. Writing it back renders the
> empty payload and erases the content.

That is not hypothetical. The pills in this desk were authored by hand, without
the templates' fixed lines, so every one of them extracted as empty and
`deskops edit pill <id> status active` reported success while blanking the
document. `deskops` now refuses a rewrite that would drop content the file still
shows, and the doctor reports documents in that state.

## Instructional text

One line above each marker, italicised, saying what the field wants:

```markdown
## Goal

_Describe the concrete result this task must produce._

⸢rev•goal⸥
```

It makes a rendered document self-sufficient for whoever opens it, and it is the
same text extraction anchors on. Keep it to a single line, use the imperative,
and mention the closed vocabulary when the field has one (`# draft | active`).
Model contracts belong in `Field(description=...)`, not here.
