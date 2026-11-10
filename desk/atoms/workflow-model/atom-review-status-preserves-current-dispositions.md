---
sldb:
  by: agent
  at: '2026-11-10T14:36:44Z'
  authority: generated
  via: create_document
id: atom-review-status-preserves-current-dispositions
title: Review status preserves current dispositions
five_wh_one_plus: how
tags:
- system:deskops
- topic:reviews
---

# Review status preserves current dispositions

## Answer

Review status groups task receipts by task id and kind, whether their subject is plain or pinned with a SHA256 anchor. The current input identity is the SHA256 of the existing builder output bytes. No receipts means missing; receipts without a matching input hash mean stale regardless of their verdict. Matching receipts use existential priority accepted, rejected, pending (reviewed), then incomplete (technical_failure). Older or lower-priority receipts never mask a current accepted disposition. Status preserves all receipts, evidence bytes and run provenance; it does not change lifecycle gates.
