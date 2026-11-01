## Informe Tester WS10

| Objeto | Evidencia real (archivo:línea leído) | Resultado |
|---|---|---|
| Pérdidas de texto previo | `manual.md:1-39` conserva íntegro `manual-antes.md:1-39`; mismo título, estado, índice 1–17, convención y secciones editoriales | PASS |
| Índice y numeración 1–17 | `manual.md:5-23`; números y títulos intactos; WS39 cap. 15 sigue existiendo | PASS |
| 17 fichas con Propósito/Entradas/Salidas/Estado/Evidencia | `manual.md:61-178`; las 17 secciones tienen los cinco campos | PASS |
| Definiciones de aceptación | `manual.md:45-48`; `dag.yaml:663-667`; disponible/propuesto/bloqueado coinciden | PASS |
| Precedencia declarada aparte | `manual.md:50-52`; `preflight-disposition.md:7`; no mezclada con las definiciones | PASS |
| CLI reutilizado sin copiar | `manual.md:54`; remite a `docs/operator-manual.md`; no reproduce cuerpo | PASS |
| Cap. 1: cita y etiqueta | `manual.md:66`; `deskops.md:9,214-224`; `docs/operator-manual.md:137` | PASS |
| Cap. 2: cita y bloqueo | `manual.md:73`; `ui.md:61`; `decisiones.md:33`; `docs/operator-manual.md:109,57,48` | PASS |
| Cap. 3: cita y bloqueo | `manual.md:79-80`; `ui.md:54,56,57`; `decisiones.md:31` | PASS |
| Cap. 4: cita y bloqueo | `manual.md:87`; `infraestructura.md:82,104`; `ui.md:58,69` | PASS |
| Cap. 5: cita y bloqueo | `manual.md:94`; `infraestructura.md:33,54`; `ui.md:64-66` | PASS |
| Cap. 6: cita y bloqueo | `manual.md:101`; `ui.md:70-72`; `deskops.md:38`; `docs/operator-manual.md:303` | PASS |
| Cap. 7: cita y bloqueo | `manual.md:108`; `deskops.md:127,185,190`; `docs/operator-manual.md:500,644` | PASS |
| Cap. 12: propuesto con cita | `manual.md:142-143`; `dag.yaml:2110-2115`; `ui.md:82-84`; `docs/operator-manual.md:715` | PASS |
| Cap. 13: cita y bloqueo | `manual.md:150`; `ui.md:79`; `deskops.md:134`; `docs/operator-manual.md:407` | PASS |
| Cap. 14: bloqueo base + Changes avanzado propuesto | `manual.md:156-157`; `ui.md:60,80`; `deskops.md:125`; `infraestructura.md:82` | PASS |
| Cap. 15: propuesto con cita | `manual.md:163-164`; `ui.md:85,97`; `infraestructura.md:149-152` | PASS |
| Cap. 16: bloqueo y citas de inventario | `manual.md:171`; `deskops.md:24,181`; `docs/operator-manual.md:742`; no existe `contratos/` en `desk/drawer/plans/workspace-documental/` | PASS |
| Cap. 17: cita y bloqueo | `manual.md:178`; `ui.md:81,86`; `dag.yaml:2110-2112` | PASS |
| Ningún capítulo disponible | `manual.md:45`; estados `manual.md:65-177`; ninguna ficha usa “disponible” | PASS |
| Taller sin atribuir ruta/productor a P08 | `manual.md:55`; `decisiones.md:32`; `dag.yaml:660-661` | PASS |
| Sin pasos, capturas ni controles inventados | `manual.md:59`; menciones a “pasos/capturas” son convención o límite, no contenido inventado | PASS |
| Independencia de `user-flows.md` | `manual.md:175,178`; no cita ni depende de `borradores/user-flows.md` | PASS |
| Atribución del `result-summary` | `result-summary.md:3,13,49`; declara archivos, límites y validaciones no ejecutadas | PASS |
| Atribución del ledger | `comparison-ledger.md:5,7,11,15`; limita su comprobación a rango/IDs y deja el contenido al Tester | PASS |

### Hallazgos menores
- Cap. 12: el borrador previo decía “pendiente hasta WS37”, no literalmente “propuesto”; la etiqueta está respaldada por `dag.yaml:2114-2115` y `preflight-disposition.md:7`. Atribución algo imprecisa, no error material.
- Cap. 1 rotula como “hueco” la ausencia de glosario separado, aunque WS01/`brief.md` ya existe; no afecta la etiqueta `propuesto`.
- Cap. 17 menciona a WS08 como dueño del hueco de flujos, no su entregable; no cita `user-flows.md`.
- Los nuevos encabezados de caps. 12 y 17 abrevian la etiqueta del índice, pero el índice 1–17 y el estado conservan el texto relevante.

### No pude verificar
- No ejecuté `build_plan.py`, `validate_plan.py`, `context_review.py` ni closeout.
- No verifiqué commits, actas humanas, comportamiento real de UI ni pruebas de runtime.
- De `docs/operator-manual.md` comprobé encabezados y numeración de línea, no el cuerpo completo de cada sección.
- No pude comprobar por ejecución que el Executor solo escribiera dos archivos ni que no abriera `user-flows.md`; solo verifiqué que el entregable no lo cita.
- No verifiqué las 160 citas que el ledger declara en rango.

RESULTADO: PASS
