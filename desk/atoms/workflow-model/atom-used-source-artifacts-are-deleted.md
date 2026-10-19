---
id: atom-used-source-artifacts-are-deleted
title: Used source artifacts are deleted
five_wh_one_plus: when
tags:
- system:deskops
- topic:drawer
- topic:inbox
- topic:cleanup
---

# Used source artifacts are deleted

## Answer

When inbox, drawer, or other source artifacts are consumed into active tasks, atoms, docs, specs, code, tests, or commits, the original source file should be deleted rather than marked with terminal statuses such as promoted or stable. `promote inbox-to-drawer-task` deletes the inbox note automatically; a drawer file recorded by `add task --from-drawer` is kept for manual cleanup and should be removed by hand.
