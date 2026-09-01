# Ritual: Zero-context subagent stress test

ID: task-ritual-zero-context-subagent-stress-test
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260825-020103-suggestion-ritual-zero-context-subagent-stress-test.md`.

## Scope

Es vital estandarizar un 'Test de Estrés de Arquitectura de Cero Contexto' usando un subagente (context: fresh) para revisar la carpeta desk/ antes de empezar a programar. En nuestro proyecto de Agente Conversacional, este test detectó instantáneamente 9 vacíos graves (timeouts de state machine, esquemas de payload no definidos, colisiones de CRON vs User). Propongo agregarlo como un paso oficial en el ritual de 'design' o 'preparation'.

## Source

- `desk/inbox/20260825-020103-suggestion-ritual-zero-context-subagent-stress-test.md`

## Done When

- The message is resolved, answered, or promoted into active work.
