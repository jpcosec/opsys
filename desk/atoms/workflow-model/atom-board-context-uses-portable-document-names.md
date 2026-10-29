---
id: atom-board-context-uses-portable-document-names
title: Board context uses portable document names
five_wh_one_plus: how
tags:
- system:deskops
- topic:boards
- topic:routing
---

# Board context uses portable document names

## Answer

Package Board pills and rituals use their existing unique tracked document names so SLDB linked consumers resolve context in the provider store. Pill names match local file stems; ritual names are explicit tracked identities such as ritual-phase, not the phase.md filename. Without a store, the local graph resolves the same names: a document is also reachable by its file stem, so pill-001-task-closure-commit reaches the pill whose frontmatter id is pill-001 (deskops/graph/extract_edges.py). Keep task paths for local operational routing. Validate linked containment with a real provider and consumer, including colliding consumer paths, and retain local graph containment, next/show pill selectors, and retirement matching.
