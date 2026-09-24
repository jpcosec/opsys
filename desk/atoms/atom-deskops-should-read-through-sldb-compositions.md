---
id: atom-deskops-should-read-through-sldb-compositions
title: Deskops should read through sldb compositions
five_wh_one_plus: how
tags:
- system:deskops
- system:sldb
- topic:diagnosis
- topic:composition
---

# Deskops should read through sldb compositions

## Answer

Prefer a composition declared in the model over code that reads several documents and stitches them together. A composition is a projection sldb can render and query; ad-hoc stitching in deskops is a projection only that code can see, so it drifts from the model the moment either changes.
