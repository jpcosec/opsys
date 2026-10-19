---
id: atom-primitives-encode-operational-rules
title: Operational rules are graph data
five_wh_one_plus: what
tags:
- system:deskops
- topic:lifecycle
- topic:workflow
---

# Operational rules are graph data

## Answer

Operational rules live as data in the desk's sldb graph, not inside CLI handlers or per-task documents: a gate is the --where condition of a RelationDoc, a transition is the RelationDoc itself, and the effect of a transition (the status it sets, whether it closes the task) is declared per relation type in deskops/spec/workflows/task_lifecycle.yaml. deskops code only computes the evidence facts the conditions test (closeout_evidence_verified) and fires the first transition whose condition holds, evaluated by sldb (sldb.api.where_matches).
