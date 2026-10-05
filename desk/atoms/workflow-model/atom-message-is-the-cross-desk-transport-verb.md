---
id: atom-message-is-the-cross-desk-transport-verb
title: Message is the cross-desk transport verb
five_wh_one_plus: what
tags:
- system:deskops
- layer:cli
- topic:cross-repo
- topic:workflow
- topic:usability
---

# Message is the cross-desk transport verb

## Answer

Cross-desk coordination is exposed as `deskops message send|list|read|ack`, not as `deskops inbox`. The command names the transport action so an agent routes a message through the CLI instead of writing a file under the `desk/inbox/` storage directory. `deskops inbox` remains only as a deprecated alias, and the `desk/inbox/` directory keeps its role as the receiving mailbox.
