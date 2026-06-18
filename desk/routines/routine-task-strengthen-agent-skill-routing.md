---
id: routine-task-strengthen-agent-skill-routing
status: active
entrypoint: checklist-task-strengthen-agent-skill-routing-execution-ready
decomposition:
- checklist-task-strengthen-agent-skill-routing-execution-ready
- operator-task-strengthen-agent-skill-routing-activate
- checklist-task-strengthen-agent-skill-routing-testing-ready
- operator-task-strengthen-agent-skill-routing-ready-for-testing
- checklist-task-strengthen-agent-skill-routing-closeout-ready
- operator-task-strengthen-agent-skill-routing-close
edges:
- edge-task-strengthen-agent-skill-routing-execution-to-activate
- edge-task-strengthen-agent-skill-routing-activate-to-testing
- edge-task-strengthen-agent-skill-routing-testing-to-ready
- edge-task-strengthen-agent-skill-routing-ready-to-closeout
- edge-task-strengthen-agent-skill-routing-closeout-to-close
- edge-task-strengthen-agent-skill-routing-close-to-complete
terminal_nodes:
- complete
tags:
- workspace:desk
- primitive:routine
---

# Routine for Strengthen agent skill routing

## Summary

_Summarize what this routine does and how its nodes fit together._

Actionable routine for Strengthen agent skill routing.
