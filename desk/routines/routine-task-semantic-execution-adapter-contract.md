---
id: routine-task-semantic-execution-adapter-contract
status: active
entrypoint: checklist-task-semantic-execution-adapter-contract-execution-ready
decomposition:
- checklist-task-semantic-execution-adapter-contract-execution-ready
- operator-task-semantic-execution-adapter-contract-activate
- checklist-task-semantic-execution-adapter-contract-testing-ready
- operator-task-semantic-execution-adapter-contract-ready-for-testing
- checklist-task-semantic-execution-adapter-contract-closeout-ready
- operator-task-semantic-execution-adapter-contract-close
edges:
- edge-task-semantic-execution-adapter-contract-execution-to-activate
- edge-task-semantic-execution-adapter-contract-activate-to-testing
- edge-task-semantic-execution-adapter-contract-testing-to-ready
- edge-task-semantic-execution-adapter-contract-ready-to-closeout
- edge-task-semantic-execution-adapter-contract-closeout-to-close
- edge-task-semantic-execution-adapter-contract-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Semantic execution adapter contract

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Semantic execution adapter contract.
