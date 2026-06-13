---
name: use-sldb
description: Use when working with SLDB StructuredNLDoc models, reversible markers, Markdown rendering/extraction, model registration, or .sldb stores.
---

# Use SLDB

SLDB owns reusable structured Markdown document infrastructure.

Use SLDB when the task involves:

- `StructuredNLDoc` models.
- `__template__` rendering/extraction.
- Reversible markers such as `⸢rev•field⸥`, `⸢rev,list•items⸥`, or `⸢rev,dict•frontmatter⸥`.
- Frontmatter extraction/rendering.
- `.sldb` stores, model registration, document tracking, and query/export commands.

Core boundary:

- SLDB should not contain deskops workflow logic.
- SLDB should provide generic document modeling, validation, stores, and queries.
- Domain-specific models can live in downstream packages such as `deskops.models`.

Common commands:

```bash
python -m sldb --help
python -m sldb stores init --path .
python -m sldb models add deskops.models:AtomDoc --store .sldb --pythonpath .
python -m sldb docs track <path> --model AtomDoc --store .sldb --pythonpath .
python -m sldb validate deskops.models:AtomDoc <doc.md> --pythonpath .
python -m sldb extract deskops.models:AtomDoc <doc.md> <out.yaml> --pythonpath .
python -m sldb render deskops.models:AtomDoc <payload.yaml> <out.md> --pythonpath .
```

Template guidance:

- Put machine metadata in YAML frontmatter where possible.
- Keep human content in Markdown sections.
- Use reversible markers only once per canonical field.
- Keep render-only markers out of extracted payload requirements.

Validation:

```bash
pytest
```

When changing SLDB extraction/rendering, run the SLDB suite and downstream deskops tests if deskops uses the changed behavior.
