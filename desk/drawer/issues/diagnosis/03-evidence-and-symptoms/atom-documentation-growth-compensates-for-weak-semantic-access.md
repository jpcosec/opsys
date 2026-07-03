---
id: atom-documentation-growth-compensates-for-weak-semantic-access
title: Documentation growth compensates for weak semantic access
five_wh_one_plus: why
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:documentation
type: atom
description: Symptom connecting document growth with architectural underuse of SLDB.
---

# Documentation growth compensates for weak semantic access

## Answer

When structured knowledge is not easy to recover through queries and compositions, projects tend to add more explanatory docs, diagrams, summaries, and operational prompts to compensate. Some of the current documentation pressure likely comes from this missing semantic access path rather than from an intrinsic need for more prose.

## Related Tasks

- `desk/tasks/task-write-end-to-end-deskops-operator-manual.md`
- `desk/tasks/task-add-drift-check-review-loop.md`
- `desk/tasks/task-design-operational-cli-grammar.md`

## Evidence

- `docs/diagrams/` — the repo already carries many explanatory workflow diagrams across multiple subtrees.
- `AGENTS.md`, `README.md`, `docs/faq.md`, `desk/rituals/*.md`, and `.agents/skills/*.md` — together show a large amount of compensating operational prose.
- `.skills/sldb/SKILL.md` and `README.md` — indicate the intended structured access path that could reduce the need for some compensating prose if used more directly.
