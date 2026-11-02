# Aplicar disponibilidad de alias en el contrato WS11

Estado: candidato capturado directamente en drawer, 2026-11-01. Trabajo local de deskops. Autorizado por la revisión root: `runs/subagents/20261101-ws11-disponibilidad/review-source.md`.

## Problema

§3.2 valida que `root` y `store` existen, y §8.5 exige E-MD3 para store ausente: si la carga rechaza la entrada, E-MD3 no se alcanza.

## Alcance propuesto

El reemplazo exacto preaprobado por root, en una cadena. Sin otros cambios.
