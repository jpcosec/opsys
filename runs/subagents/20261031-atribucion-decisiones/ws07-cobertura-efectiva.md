# Cobertura efectiva de WS07 tras la corrección de procedencia

Fecha: 2026-11-01. Autor: Claude Opus 5.5, pane `w3Y:p1`. Sustituye al dictamen de `runs/subagents/20261031-ws07-decisiones/coverage-report.md` en el defecto D1 y en la observación O6, que quedan como historia.

| Aceptación WS07 | Estado | Evidencia |
|---|---|---|
| Registro de cada Pxx con tipo, actor, fuente y nodos/gates | Cubierto | `decisiones.md` 25-33 y tabla «Procedencia técnica» |
| Respuestas literales 0–2 | Cubierto | Iguales a `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`, comprobado por programa; líneas 1-22 iguales a `7b045a6f` |
| P07/P09 sin firma humana | Cubierto | Actor técnico registrado; no prueba la autoría inicial, que sigue sin localizar |
| Sin repetir preguntas ni inferir API, UI o Scion | Cubierto | Sin preguntas nuevas; `dag.yaml` solo cambia en evidencia |
| `baseline_proposal` y `source_mode` | Sin cambio | Comparación estructural de `dag.yaml` |

D1 queda corregido: lo humano conserva solo lo aceptado y cada precisión pasa a T-Pxx con fuente y límite.

Sigue abierto, sin bloquear: la autoría inicial de la tabla y de P07/P09 sigue sin localizar. No se inventa. La suite general no se reabrió: su estado sigue siendo el declarado en `ef636f4d`, no verde.
