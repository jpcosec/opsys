# Two hand-written pills do not fit PillDoc

## Kind

issue

## Status

resolved

## What happened

`desk/contexts/pill-sldb-template-markers` and
`desk/contexts/pill-template-instructional-text` (both deleted) were free-form notes rather
than modelled pills: no frontmatter, the identifier in the body as `ID: ...`,
duplicated `## Goal` sections, and a section order PillDoc's template does not
use. Tracking them failed, so their knowledge was invisible to `sldb find`, the
graph and pill binding.

Investigating them surfaced the larger defect: **every** pill in the desk
extracted as empty, because extraction anchors on the fixed text a template
renders and none of these documents carry it. Any edit re-rendered those empty
values and blanked the document.

## Resolution

- The two notes were documentation about stable SLDB behaviour, not
  task-scoped guardrails, so they became atoms and a materialization:
  `desk/atoms/atom-sldb-template-markers-declare-where-each-field-lives.md`,
  `atom-sldb-extraction-reads-values-relative-to-the-template-s-own-text.md`,
  `atom-instructional-text-makes-a-template-self-sufficient.md`,
  `atom-templates-are-defined-as-model-strings.md`,
  `atom-do-not-use-instructional-text-as-model-documentation.md`, and
  `docs/sldb-templates.md`.
- The 34 documents in that state (29 pills, 4 conditions, 1 step) were rebuilt
  from their own text through their models, so they now read back.
- `deskops` refuses a rewrite that would drop content the document still shows,
  and the doctor reports the condition, so the next one cannot sit unnoticed.

## Tags

- workspace:desk
- artifact:issue
- topic:pills
- topic:store-health
