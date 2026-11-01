**Alcance de la revisión:** solo lectura. No ejecuté build, validate, status, tests ni closeout.

| Objeto | Evidencia real (archivo:línea leída) | Resultado |
|---|---|---|
| Pérdidas entre versión previa y actual | `runs/.../user-flows-antes.md:1-63`; `borradores/user-flows.md:9-236`. Textos UF01–UF10 y «Precisiones de revisión» conservados; solo se añaden convención y campos. | PASS |
| 10 UF con Entrada/Salida/Operación/Error/Nodo/Gate | `user-flows.md:9,15-17,26,31-32`; `:34,40-42,52,56-57`; `:59,65-67,80,84-85`; `:87,93-95,103,107-108`; `:110,116-118,128,132-133`; `:135,141-144,153,156-157`; `:159,165-167,176,180-181`; `:183,189-191,197,199-200`; `:202,206-208,214,216-217`; `:219,223-225,232,235-236` | PASS |
| Gates y nodos frente a cobertura y protocolo | `cobertura.md:5-14`; `validacion-humana.md:8-14`; `user-flows.md:31-32,56-57,84-85,107-108,132-133,156-157,180-181,199-200,216-217,235-236` | PASS |
| Gate humano distinto de WS29 | `user-flows.md:7,181`; `validacion-humana.md:13` | PASS |
| Citas: más de 20 líneas abiertas en 5 UF | `deskops.md:31,35,38,41,45,51,62,98,129,131,134,226,259-260`; `infraestructura.md:30,33,51-53,88,92,94,110,115-116,163`; `ui.md:54-57,60-61,63-65,67,69-72,79-80,85-87` | PASS |
| UF02: ack/responder local como pendiente, no disponible | `user-flows.md:48-49`; `deskops.md:38,41`; `ui.md:70-71`; `dag.yaml:758-759` | PASS |
| UF08 sin envío interdesk | `user-flows.md:188,195-196,200`; `deskops.md:38`; `decisiones.md:31` | PASS |
| UF06 condicionada a G_SCION/G_EXEC sin habilitarla | `user-flows.md:143,147,152,156-157`; `dag.yaml:63,71,2842-2862` | PASS |
| Taller como corpus futuro y G_PRODUCT no como aceptación | `user-flows.md:7,224,230`; `ui.md:86`; `dag.yaml:2672-2697`; `validacion-humana.md:6-7` | PASS |
| Independencia de `borradores/manual.md` | Sin coincidencias en `user-flows.md`; `result-summary.md:26` declara no haberlo leído | PASS |
| Atribución de `result-summary` y ledger | `result-summary.md:5,9,10,31`; `comparison-ledger.md:11,15` | PASS |

**Hallazgos menores**
- `user-flows.md:147` afirma que «bundle» no aparece en las auditorías; sí aparece `create_task_bundle` en `deskops.md:51,154`. El hueco de «preparar bundle de contexto» sigue sin operación auditada, pero la frase es imprecisa.
- `user-flows.md:171` cita `ui.md:60` para «modelo no importable»; esa línea documenta errores de catálogo/nodo/proyección y fallo CDN, no literalmente ese caso.
- `user-flows.md:89` incluye «vincular rituales»; `Operación` lista `list/show ritual` pero no una operación de vinculación ni lo marca como hueco.
- `result-summary.md:10` dice que nodos y gates salen de `cobertura.md` y `validacion-humana.md`; WS38, WS40 y WS43 también se apoyan en `dag.yaml` (`dag.yaml:2597-2608,2672-2697,2804-2830`).
- `user-flows.md:224` menciona «refresco tras resultado real» como objetivo del flujo; no hay operación auditada asociada, aunque no se presenta como implementada.

**No pude verificar**
- Runtime, UI real, build/validate/status, tests y closeout.
- El contenido del código de `sldb`, `graph_ui` y demás repos citados; solo contrasté las auditorías y sus líneas.
- Que `tester-facts.log` corresponda al HEAD real; son declaraciones del Supervisor.
- Que `user-flows-antes.md` sea exactamente la copia base usada; la comparación es por lectura.

RESULTADO: PASS
