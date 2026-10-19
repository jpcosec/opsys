---
id: atom-desk-health-is-workspace-integrity-state
title: Desk health is workspace integrity state
five_wh_one_plus: what
tags:
- system:deskops
- topic:workspace-health
- topic:diagnosis
---

# Desk health is workspace integrity state

## Answer

Desk health is the integrity state of the desk/ workspace: whether it has the expected structure, tracked modeled documents, readable document content, and registered deskops models, and whether it classifies as absent, empty, legacy or current. deskops doctor measures it; store-level document validity is delegated to sldb stores check.

## Evidence

`deskops/cli/commands/doctor.py` checks:
- Missing or malformed `desk/` directory structure
- Untracked modeled documents in `desk/`
- Documents the model cannot read
- Invalid task/pill/atom/ritual documents (malformed YAML frontmatter)
- An unreadable local store index
- Unregistered deskops models

## Related Atoms

- `atom-stale-state-causes-agent-hallucination` — explains why health matters for agents
- `atom-desk-health-delegates-store-diagnostics-to-sldb` — defines the boundary

## Tags

- system:deskops
- topic:workspace-health
- topic:diagnosis
