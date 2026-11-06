---
id: materialization-closeout-gates-review-command
title: closeout gates review command
source_atoms:
- atom-review-attestations-state-only-what-was-actually-read
target_kind: code
target_identity: deskops/cli/commands/review.py
validation:
- pytest -q tests/test_review_command.py
tags:
- system:deskops
- topic:gates-por-tipo
---

# closeout gates review command

## Intent

deskops review preflight/node/dispose CLI, replacing the cold context_review.py scripts.
