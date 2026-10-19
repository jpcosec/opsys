---
id: atom-networkx-is-first-graph-runtime
title: NetworkX is first graph runtime
five_wh_one_plus: how
tags:
- system:deskops
- system:kgdb
- topic:knowledge-graph
- topic:implementation
---

# NetworkX is first graph runtime

## Answer

The sldb graph runtime (sldb.api.graph) uses NetworkX for traversal, neighborhood queries, path analysis and snapshot export; deskops builds its graph snapshot from that API before introducing heavier ontology or OWL reasoning.
