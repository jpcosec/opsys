---
id: routine-task-add-json-output-for-modeled-documents
status: active
entrypoint: checklist-task-add-json-output-for-modeled-documents-execution-ready
decomposition:
- checklist-task-add-json-output-for-modeled-documents-execution-ready
- operator-task-add-json-output-for-modeled-documents-activate
- checklist-task-add-json-output-for-modeled-documents-testing-ready
- operator-task-add-json-output-for-modeled-documents-ready-for-testing
- checklist-task-add-json-output-for-modeled-documents-closeout-ready
- operator-task-add-json-output-for-modeled-documents-close
edges:
- edge-task-add-json-output-for-modeled-documents-execution-to-activate
- edge-task-add-json-output-for-modeled-documents-activate-to-testing
- edge-task-add-json-output-for-modeled-documents-testing-to-ready
- edge-task-add-json-output-for-modeled-documents-ready-to-closeout
- edge-task-add-json-output-for-modeled-documents-closeout-to-close
- edge-task-add-json-output-for-modeled-documents-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Add JSON output for modeled documents

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Add JSON output for modeled documents.
