---
id: checklist-task-enrich-templates-with-instructional-text-testing-ready
status: complete
condition_refs:
- condition-task-enrich-templates-with-instructional-text-has-validation
mode: all
tags:
- system:deskops
- topic:templates
---

# Checklist: Enrich Templates (Testing Ready)

## Summary

This checklist verifies that the task to enrich templates with instructional text has been implemented and is ready for testing.

## Items

- All specified `deskops/models/*.py` files have been updated with instructional text.
- `⸢rev•⸥` markers remain present and functional.
- The `tests/test_model_templates.py` roundtrip test passes.
- New documents rendered from the updated templates are understandable without external context.
- The instructional text does not interfere with SLDB parsing.
