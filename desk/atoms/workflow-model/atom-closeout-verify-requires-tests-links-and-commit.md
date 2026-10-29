---
sldb:
  by: agent
  at: '2026-10-21T06:36:12Z'
  authority: generated
  via: save_document_payload
id: atom-closeout-verify-requires-tests-links-and-commit
title: Closeout verify requires tests links and commit
five_wh_one_plus: how
tags:
- system:deskops
- topic:closeout
- topic:workflow
- topic:materialization
---

# Closeout verify requires tests links and commit

## Answer

Before the tool-made closing commit, `deskops closeout verify` requires resolvable test evidence and a commit reference resolving to HEAD or an ancestor. When the current desk contains atom documents (including nested atom-*.md files), it also requires changed-file atom or materialization coverage, or a routed follow-up when a file lacks a live link. Missing knowledge coverage is optional only when the desk has no atom documents; a missing, empty, or README-only atoms directory qualifies. Invalid changed-file paths still fail. Changed generated artifacts with a live sibling source must still declare `source_atoms` or `provenance`; path-pair drift comparison stays out of scope for this gate.
