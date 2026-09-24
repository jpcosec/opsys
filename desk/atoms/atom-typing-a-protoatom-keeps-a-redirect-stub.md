---
id: atom-typing-a-protoatom-keeps-a-redirect-stub
title: Typing a protoatom keeps a redirect stub
five_wh_one_plus: how
tags:
- system:deskops
- topic:atoms
provenance: null
---

# Typing a protoatom keeps a redirect stub

## Answer

Typing creates a new document of the target sldb model carrying the protoatom title, tags, provenance and content (into a chosen field), then keeps the protoatom as a redirect stub whose typed_as names Model:id, so the old id keeps resolving as with atom split and merge. sldb has no class migration, so typing is an explicit deskops operation rather than an in-place change of model.
