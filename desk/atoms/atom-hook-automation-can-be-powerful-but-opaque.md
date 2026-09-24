---
id: atom-hook-automation-can-be-powerful-but-opaque
title: Hook automation can be powerful but opaque
five_wh_one_plus: how_not
tags:
- system:deskops
- topic:diagnosis
- topic:hooks
---

# Hook automation can be powerful but opaque

## Answer

Do not let a hook change workflow state without leaving a record a reader can find afterwards. Automation that acts between visible steps is hard to debug and hard to trust: when it misfires, the state it changed is already gone. A hook should be visible in the task's history, not only in the effect it had.
