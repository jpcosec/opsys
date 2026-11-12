---
sldb:
  by: agent
  at: '2026-11-12T03:38:02Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta-reproduction-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: reproduction
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: human
actor: coord2
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: c43f28e50c9e998381c509833eeb60c51eb6f4656cfd6f193bc36ccdbf59d793
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: pending
reason: 'Mediciones del h11-worker sobre su layout (deskops 4904ddfe, sldb con H11):
  deskops view board caliente 4,94 s con 1,59 s de sldb views run board en el mismo
  layout, es decir ~3,3 s de trabajo propio de deskops; el coordinador no las re-corrió
  porque la máquina estaba cargada (11-13), y el worker de la tarea mide su línea
  base propia con caché frío y caliente.'
# ISO 8601 timestamp
created_at: '2026-11-12T03:38:02.067775+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: ''
disposed_by: ''
# e.g. workspace:desk
tags:
- workspace:desk
---

# Reproduction review of task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta

## Summary

_Summarize what was reviewed and the evidence this receipt records._

reproduction receipt recorded by coord2; evidence: runs/subagents/20261112-repro-boardperf/repro.log

## Disposition

_Record the verdict rationale and who disposed of the review._
