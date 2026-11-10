---
sldb:
  by: agent
  at: '2026-11-10T21:20:06Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall@sha256:d24a9809f6bf9d6dbb0a528e54f18d7623a096c9e980302dbed590dd4866a96f
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: coord2
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 20fb831cf468325727723ea31c7aed0c1ed58d8d89969c75cd360d14c0b199e4
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: rejected
reason: el TaskDoc cambió (b1-b7) tras registrarlo; se registra de nuevo sobre el
  contrato vigente con la misma evidencia
# ISO 8601 timestamp
created_at: '2026-11-10T21:19:22.877260+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-10T21:20:04.316586+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Reproduction review of task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by coord2; evidence: runs/subagents/20261110-repro-advance/repro.log

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict rejected: el TaskDoc cambió (b1-b7) tras registrarlo; se registra de nuevo sobre el contrato vigente con la misma evidencia
