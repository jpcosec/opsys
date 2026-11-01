# Ledger de comparación, tanda 2 sobre fc5e64a8

Fecha: 2026-11-01. Rol: Supervisor. Actor: Claude Opus 5.5, pane `w3Y:p1`. Sustituye al ledger de `tanda-1/`, que queda como historia junto con `47b9e38b`. Revisores: `pi`, deepseek-flash, instrucción v2.

## Conteo

| Estado | Nodos |
|---|---|
| Comparadas | 47 de 73 |
| Aceptadas como comprensión, sin registrar | 44 |
| No aceptadas | 3: WS07, WS13, WS19 |
| Sin respuesta | 26: WS27.1 a WS45 |

Las 44 no son aprobación: dependen de que `fc5e64a8` siga vigente, y nada se registró en `dag.yaml`.

## Disponibilidad

Tras la reanudación, solo WS27.1 con `--new-attempt`: `402 Insufficient Balance`, request `2128c419-ed51-48dc-a494-d57ecf19e7c5`, `attempt-4`, `technical_failure: true`, salida vacía. No se lanzaron los otros 25 ni más sondas. Antes de esa prueba, la comprobación por hash dio 47 respondidas y 26 pendientes, sin avances concurrentes.

## Qué leí

`output.md` completo de las 47. Los contratos los leí completos en la tanda 1, en esta misma sesión; `git diff 47b9e38b fc5e64a8 -- dag.yaml` es vacío. Esta vez solo volví a ver id, rol, kind, repo, depends_on, requires y children. No leí los bundles.

## Hallazgo principal: actor de P07 y P09

La fila decía `Técnica conservadora; Executor por encargo TaskDoc v2`. Desde mi parche dice `Técnica conservadora; sin firma humana; fuente en T-P07/T-P09`. Se quitó el actor. Root ordenó mantener actores, WS07 exige actor por Pxx, `attribution-map.md` no declara el cambio y ni yo ni los dos Tester lo detectamos. Lo levantó el revisor de WS07. Es ambigüedad real, causada por la fuente, no por el contrato.

Corrección propuesta, no aplicada porque la fuente está congelada y en revisión de root: `Técnica conservadora; Executor por encargo TaskDoc v2; sin firma humana; fuente en T-P07`, igual en P09. Conserva el actor registrado y no afirma que fuera quien decidió. Cambia el input de los 73: las 47 respuestas pasarían a historia y habría una tanda 3 completa. Conviene decidirlo antes de gastar saldo en los 26.

## Rechazos

- WS13: «WS13.3 consume la identidad de WS13.1/13.2»; no hay arista 13.2→13.3.
- WS19: «WS19.1 transfiere a WS19.2»; los hijos no tienen arista.

Ambos necesitan intento nuevo, imposible hoy por saldo.

## Clases

25 ambigüedades en intentos vigentes, contadas por script: 1 real (WS07), 12 `detalle de promoción`, 8 `futuro asignado`, 4 `no es ambigüedad`.

WS19.1 volvió a levantar «modo manual exclusivo». Reproducido en dos tandas y no definido en brief, alcance, decisiones ni dag: lo clasifico `futuro asignado` a la policy coordinador de WS12, pero es la clasificación más discutible.

## Límites

Las clases son juicio del Supervisor. No hubo Tester sobre esta tanda: usa el mismo proveedor sin saldo. `validate_plan.py --check` falla con 73 `input changed`, y `context_review.py status` también: es lo esperable sin registrar, no verde. `build_plan.py --check` 0 y pruebas del helper 13 passed.
