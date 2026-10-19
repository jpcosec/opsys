---
id: atom-task-bundles-are-tracked-in-the-store-at-creation-time
title: Task documents are tracked in the store at creation time
five_wh_one_plus: what
tags: []
---

# Task documents are tracked in the store at creation time

## Answer

deskops add task writes the TaskDoc and tracks it through doc_io.track_document_file (sldb.api) inside a DocTransaction at creation time; if a store exists but TaskDoc is not registered, tracking fails and the task is rolled back instead of leaving an untracked document.
