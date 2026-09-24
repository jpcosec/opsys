---
# routine-xxx
id: routine-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle
# active | archived
status: active
# Initial node identifier
entrypoint: checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-execution-ready
# Ordered or grouped primitive identifiers
decomposition:
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-execution-ready
- operator-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-activate
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-testing-ready
- operator-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-ready-for-testing
- checklist-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-closeout-ready
- operator-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-close
# Edge identifiers composing the graph
edges:
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-execution-to-activate
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-activate-to-testing
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-testing-to-ready
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-ready-to-closeout
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-closeout-to-close
- edge-task-make-terminal-node-completion-commit-before-it-deletes-the-bundle-close-to-complete
# Terminal node identifiers
terminal_nodes:
- complete
# e.g., system:deskops
tags:
- workspace:desk
- primitive:routine
---

# Routine for Make terminal-node completion commit before it deletes the bundle

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Make terminal-node completion commit before it deletes the bundle.
