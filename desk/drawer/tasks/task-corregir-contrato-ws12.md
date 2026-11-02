# Corregir contrato de operaciones de WS12 tras revisión root

Estado: candidato capturado directamente en drawer, 2026-11-02. Trabajo local de deskops. Autorizado por la revisión root: `runs/subagents/20261102-ws12-correccion/review-source.md`.

## Problema

Root no aprobó `contratos/operaciones.md`: ocho afirmaciones no se sostienen o sobreafirman, y cinco huecos necesitan decisión técnica y productor explícito.

## Alcance propuesto

Parche de `contratos/operaciones.md` y propuesta canónica mínima de productores, dependencias, aceptaciones y gates en `dag.yaml`. Intake SLDB solo para gaps comprobados. Se congela y se entrega a root antes de renovar revisiones.
