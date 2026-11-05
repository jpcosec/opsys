---
id: atom-the-deskops-ui-reads-the-desk-only-through-deskops-view-and-writes-only-through-deskops-operations
title: The deskops UI reads the desk only through deskops view and writes only through
  deskops operations
five_wh_one_plus: how
tags:
- system:deskops
- topic:ui
- topic:read-surfaces
provenance: docs/deskops-ui.md
---

# The deskops UI reads the desk only through deskops view and writes only through deskops operations

## Answer

The UI composes its five screens (board, task, drawer, inbox, agents) from `deskops view`, a read-only service over the existing DeskopsOperations; it never reads desk/ files directly and never shows data without a real source (unresolved references go to errors, missing sources render as absent). Every write (advance, inbox ack, inbox promote) goes through a deskops operation behind a revision guard computed from the Board and the task file, so a stale screen cannot overwrite a change made since it was read. Actions without a deskops operation are shown disabled with the reason.
