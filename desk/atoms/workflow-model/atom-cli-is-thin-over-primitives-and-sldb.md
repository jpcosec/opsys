---
id: atom-cli-is-thin-over-primitives-and-sldb
title: CLI is thin over SLDB and its graph
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:cli
- topic:primitives
---

# CLI is thin over SLDB and its graph

## Answer

The deskops CLI exposes workflow nouns and operations and delegates the rest: modeled document read, write and edit to SLDB, and lifecycle state rules to the SLDB graph (RelationDoc transitions whose --where conditions sldb evaluates). It must not become a second implementation of either layer.
