---
id: atom-automatic-routines-vs-llm-tasks
title: Deterministic checks are not LLM tasks
five_wh_one_plus: how
tags:
- system:deskops
- topic:automation
- topic:workflow
---

# Deterministic checks are not LLM tasks

## Answer

Actions that require semantic judgment belong to LLM/subagent tasks. Deterministic checks over known inputs, such as running touched-surface tests, closeout validation, or phase end-to-end checks, belong to tests, CI, or CLI gates. The routine and hook models were retired with the primitive layer.
