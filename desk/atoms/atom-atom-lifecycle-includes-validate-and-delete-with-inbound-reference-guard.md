---
id: atom-atom-lifecycle-includes-validate-and-delete-with-inbound-reference-guard
title: Atom lifecycle includes validate and delete with inbound-reference guard
five_wh_one_plus: what
tags: []
---

# Atom lifecycle includes validate and delete with inbound-reference guard

## Answer

deskops atoms validate checks atom integrity, including domain-tree crossroad parents, and deskops atoms delete removes an atom only when no inbound atom references exist (override with --force). Split, merge, and create-from-source are implemented alongside validate and delete.
