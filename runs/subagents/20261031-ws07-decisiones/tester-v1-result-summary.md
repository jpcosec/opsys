## Tabla de verificación

| Objeto | Evidencia real leída | Resultado |
|---|---|---|
| Réplica literal ítems 0-2 | `owner-decisions.json:7-19` vs `decisiones.md:9-19` | PASS visual. Comparación byte a byte: NO VERIFICADO (no se ejecutó script). |
| Afirmación «35 pares Pxx-nodo» | `coverage-report.md:19`; `decisiones.md:25-33`; `dag.yaml:307-2881` | FAIL. Hay 37 pares citados: P01 6, P02 3, P03 8, P04 4, P05 3, P06 3, P07 3, P08 4, P09 3. Las 64 tareas sí coinciden. |
| Existencia de nodos y gates citados | `dag.yaml:307-2881`; `dag.yaml:24,44,113,122,225,33` | PASS. WS13.3 existe (`dag.yaml:933`); todos los gates citados existen. |
| D1: frase de P03 ausente del ítem 1 | `owner-decisions.json:12-13`; `decisiones.md:27`; `taskdoc-frozen.md:73`; `preflight-input-v2.md:127-128` | PASS en lo literal. «Canal público», «autoridad compartida CLI/agentes/UI», «probado» y «lock solo UI no basta» no están en el ítem 1; sí en documentos de planificación. |
| D1 calificado como «DEFECTO REAL» | `taskdoc-payload.yaml:24`; `decisiones.md:27` | FAIL. P03 tiene actor, fuente y cita existente; no es dato falso, fila sin fuente, cita inexistente ni cambio de decisión. Es observación de fidelidad/procedencia, no defecto de la regla de edición. |
| P01/P04/P05/P06 «misma clase, menor gravedad» | `decisiones.md:25,28-30`; `owner-decisions.json:7-8,12-13` | PASS en la comparación: son del mismo tipo. FAIL en la consecuencia: si D1 es observación, estas también lo son; presentarlas como «menores» dentro de un defecto es inconsistente. |
| P07 «detalle: n/a» | `decisiones.md:31`; `preflight-input-v2.md:108-113` | FAIL. «Multidesk inicialmente read-only con rutas/aliases explícitos» no está en la fuente citada; `preflight-input-v2.md:108-113` solo dice «estado local+lectura interdesk». O6 lo da por respaldado sin serlo. |
| P09 «detalle: n/a» | `decisiones.md:33`; `preflight-input-v2.md:108-113`; `dag.yaml:2804-2807` | FAIL. «Entradas reales», «reutilizando registry» y «publicar WS43 tras validación» salen del DAG, no de la fuente citada «Executor por encargo TaskDoc v2». |
| P02 y P08 | `decisiones.md:26,32`; `owner-decisions.json:7-8,17-18`; `dag.yaml:10` | PASS con matiz. P02 «Kimun fuera de esta línea base» no es literal de la respuesta («sin migrar a Kimun»), pero sí del `baseline_proposal` (`dag.yaml:10`). P08 está respaldado por el ítem 2. |
| Párrafos posteriores fuera de la tabla | `decisiones.md:3,23,35` | PASS. No atribuyen al solicitante nada que no diga el ítem 2; la introducción está respaldada por `owner-decisions.json:17-18`. |
| O1 G_PRODUCT | `dag.yaml:24-32`; `coverage-report.md:41` | PASS como observación: `verified_evidence` desambigua P07/P09. FAIL aparte: `coverage-report.md:41` afirma «en ningún sitio», pero el título «por humano» y la lista de evidencia sí los presentan bajo ese gate; el propio O1 lo contradice. |
| O2 a O5 | `dag.yaml:113-121,51-53,65`; `decisiones.md:35` | PASS. O2 es texto irrelevante, no atribución falsa; O3, O4 y O5 están bien calificadas. |
| Límites | `coverage-report.md`; `taskdoc-payload.yaml:30-32` | PASS en no pedir decisión y no inferir API/UI/Scion. «No se editó nada»: NO VERIFICADO en lectura. |
| Dictamen | `coverage-report.md:74` | FAIL. Debe ser `CUBIERTO` con observaciones. |

## Hallazgos

- D1 no es un defecto real: la observación literal es cierta, pero la fila P03 no incurre en ninguna de las cuatro causas de edición (`taskdoc-payload.yaml:24`); la cita existe y el núcleo de la decisión sí está en el ítem 1.
- La frase añadida está en `preflight-input-v2.md:127-128` y `taskdoc-frozen.md:73`, que son documentos de planificación/encargo, no una respuesta humana. Llamarlo «encargo del solicitante» es impreciso.
- El informe afirma 35 pares Pxx-nodo; la tabla de `decisiones.md` contiene 37. Es una afirmación de cobertura falsa.
- El informe declara «n/a» el detalle de P07 y P09, pero ambas filas añaden contenido que su fuente citada no contiene; O6 lo da por respaldado sin serlo.
- Las observaciones O1-O5 están bien clasificadas; O1 no debe elevarse a defecto porque `verified_evidence` (`dag.yaml:32`) aclara que P07/P09 son defaults técnicos. G_WRITE_POLICY citando P07/P09 es texto irrelevante, no atribución humana.
- El dictamen correcto es `CUBIERTO` con observaciones, no `DEFECTO REAL`.

RESULTADO: FAIL
