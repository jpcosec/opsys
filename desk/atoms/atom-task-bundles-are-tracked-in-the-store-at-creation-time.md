---
id: atom-task-bundles-are-tracked-in-the-store-at-creation-time
title: Task documents are tracked in the store at creation time
five_wh_one_plus: what
tags: []
---

# Task documents are tracked in the store at creation time

## Answer

deskops add task and promote track every generated task document into the local .sldb store via sldb.store.ops.track_document at write time; if a store exists but the task model is not registered, creation fails instead of silently leaving an untracked doc.
