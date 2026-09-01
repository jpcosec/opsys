# Closeout de tasks no limpia primitives ni deja status coherente

ID: task-closeout-de-tasks-no-limpia-primitives-ni-deja-status-coherente
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260826-033933-suggestion-closeout-de-tasks-no-limpia-primitives-ni-deja-status-coherente.md`.

## Scope

En conversational-agent-arch encontramos ~436 primitives/routines huerfanos: 20 tasks quedaron en estado draft aunque su codigo estaba implementado y testeado (68 tests verdes) fuera del flujo deskops. Al cerrarlas via 'deskops advance task --to complete' aparecen DOS limitaciones. (1) El override marca el node como 'complete' pero la task sigue con Status: active y NO archiva ni limpia sus primitives asociados (~16 archivos por task quedan en disco). No existe un closeout que borre el andamiaje (conditions/operators/checklists/edges/routines) de una task cerrada; hubo que hacer 'git rm -r desk/primitives desk/routines' a mano y luego 'sldb stores update'. (2) Tras borrar los primitives y sincronizar el store, 'deskops doctor' sigue listando las 20 tasks como 'Untracked desk documents' pese a estar tracked en git y en .sldb (relacionado con la nota del 2026-08-11 de sldb sobre doctor mezclando superficies no modeladas con estado roto). Sugerencia: (a) un 'deskops closeout task <id>' que archive la task y elimine/mueva su andamiaje en un solo paso; (b) que 'advance --to complete' deje la task en Status coherente (completed/archived), no active.

## Source

- `desk/inbox/20260826-033933-suggestion-closeout-de-tasks-no-limpia-primitives-ni-deja-status-coherente.md`

## Done When

- The message is resolved, answered, or promoted into active work.
