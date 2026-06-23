---
id: routine-task-enrich-templates-with-instructional-text
status: active
entrypoint: checklist-task-enrich-templates-with-instructional-text-execution-ready
decomposition:
- checklist-task-enrich-templates-with-instructional-text-execution-ready
- checklist-task-enrich-templates-with-instructional-text-testing-ready
- checklist-task-enrich-templates-with-instructional-text-closeout-ready
edges:
- edge-task-enrich-templates-with-instructional-text-execution-to-testing
- edge-task-enrich-templates-with-instructional-text-testing-to-closeout
- edge-task-enrich-templates-with-instructional-text-closeout-to-complete
terminal_nodes:
- checklist-task-enrich-templates-with-instructional-text-closeout-ready
tags:
- system:deskops
- topic:templates
---

# Routine for Enriching Templates with Instructional Text

## Summary

This routine guides the process of adding instructional fixed text to all deskops model templates, ensuring proper execution, testing, and closeout.
