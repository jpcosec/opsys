# Two hand-written pills do not fit PillDoc

## What

`desk/contexts/pill-sldb-template-markers.md` and
`desk/contexts/pill-template-instructional-text.md` are the only desk documents
left untracked after the store repair. They were written by hand as free-form
notes, not through `deskops add pill`:

- no YAML frontmatter; the identifier sits in the body as `ID: pill-...`
- duplicated sections (`## Goal` appears twice in both files)
- sections that PillDoc does not declare, in an order the template does not use

So extraction finds no `id` and tracking fails with a PillDoc validation error.

## Why it matters

Both carry real knowledge worth keeping: how SLDB template markers behave
(`rev`, `optrev`, `render`, fixed text around markers) and how instructional
text in templates should be written. That content is currently invisible to
`sldb find`, the graph, and any pill binding.

## Options

1. Rewrite both as proper PillDoc documents, moving the body into the declared
   sections and dropping the duplicates.
2. Decide they are documentation rather than pills, and move them under `docs/`
   as a materialization of the relevant atoms.

Option 2 looks closer to what they actually are: neither reads like a
task-scoped guardrail, and both describe stable SLDB behavior.

## Tags

- workspace:desk
- artifact:issue
- topic:pills
- topic:store-health
