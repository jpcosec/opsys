---
id: atom-multi-surface-drift-is-a-core-workflow-failure-mode
title: Multi-surface drift is a core workflow failure mode
five_wh_one_plus: why
tags:
- system:deskops
- topic:diagnosis
- topic:drift
---

# Multi-surface drift is a core workflow failure mode

## Answer

The same fact is normally written in more than one place: a model template and a document, a board and a task, an atom and the doc that materializes it, a role and the agent file installed from it. Any of them can be edited alone, and then the workflow is describing something that is no longer true while every individual file looks fine. Drift is therefore not a housekeeping concern but a correctness one, which is why drift checks are review surfaces with their own line in the diagnosis rather than cleanup steps.
