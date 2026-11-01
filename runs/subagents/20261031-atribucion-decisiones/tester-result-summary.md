## Informe de Tester

| Objeto | Evidencia real leída | Resultado |
|---|---|---|
| Procedencia Humana P01, P03, P04, P05, P06 | `decisiones.md:7-17` (preguntas/respuestas literales) frente a `decisiones.md:25-30`; `attribution-map.md:9-21` | **FAIL** |
| P07 y P09 sin firma humana | `decisiones.md:31,33`: «sin firma humana»; `decisiones.md:48-49` | PASS |
| Citas DAG «Procedencia técnica» | `dag.yaml:161-167`, `225-233`, `763-764`, `44-49`, `1406-1408`, `1984-1987`, `1991-1994`, `122-131`, `541-542`, `693-695`, `945-946`, `1188-1196`, `2804-2830`, `1185-1196` | PASS |
| Citas PIv2/TF/PI | `preflight-input-v2.md:107-110,124-128,131-133`; `taskdoc-frozen.md:59`; `preflight-input.md:32-33` | PASS |
| Muestra de disposiciones: WS09, WS19.1, WS22, WS29, WS31, WS32.1, WS36, WS40, WS42 | `output.md` y `disposition.md` de cada intento vigente; bloques DAG de cada nodo (`dag.yaml:608-645`, `1305-1327`, `1488-1517`, `2010-2048`, `2096-2134`, `2181-2227`, `2533-2567`, `2678-2706`, `2745-2780`) | PASS con reservas |
| Rechazos WS12, WS13, WS42 | `WS12/.../attempt-1/output.md:7,17`; `WS13/.../attempt-1/output.md:10`; `WS42/.../attempt-1/output.md`; `attempt-2` vigentes; `comparison-ledger.md:33-35` | PASS |
| Atribución del ledger | `comparison-ledger.md:14,16,37,41`; `WS19.1/731a.../attempt-1/output.md:2` | **FAIL** |
| Límites de decisión/contrato/gate | `dag-diff.txt`: solo cambian `context_review.evidence` e `input_sha256`; `decisiones.md:25-33` conserva IDs y columna de nodos/gates | PASS |

## Hallazgos

- **P04 no queda literal.** `decisiones.md:28` mantiene «solo» y añade «source_mode=editable»; la respuesta citada en `decisiones.md:13` solo dice «Markdown editable tras probar API reversible, conflictos y campos protegidos». Además, `attribution-map.md:15` afirma «Se quitó “solo”», pero la palabra sigue en `decisiones.md:28`.
- **P01/P03 tienen paráfrasis.** `decisiones.md:25` usa «solicitante» y «se designa después»; `decisiones.md:27` usa «escritor» y «read-only», mientras la pregunta literal dice «escribiendo» y «lectura». No cambian la decisión, pero no son literales.
- **P05/P06 omiten o reordenan cláusulas** de `decisiones.md:11` (`decisiones.md:29-30`): no reproducen literalmente «cierre y promoción» ni la condición «con otro coordinador escribiendo».
- **El ledger afirma algo falso sobre WS19.1.** `comparison-ledger.md:41` dice que «modo manual exclusivo» no tenía antecedente en el intento previo y que «la frase está solo» en la tabla inicial y `dag.yaml:1327`; el output anterior de WS19.1 sí contiene la frase: `WS19.1/731a0da.../attempt-1/output.md:2`. Además, `comparison-ledger.md:16` declara haber abierto del intento anterior solo ambigüedad y disposición, no el output completo.
- **Muestra de disposiciones:** las clases se sostienen en WS09, WS19.1, WS22, WS29, WS31, WS32.1, WS36, WS40 y WS42. WS36 y WS42 son las más frágiles: dependen de que el TaskDoc resuelva el canal WS33.2 y el registro del modelo en el store; no las marcaría falsa aceptación con la evidencia actual, pero quedan como hueco de promoción.
- **Rechazos:** el defecto de WS12 attempt-1 es real (`WS12/.../attempt-1/output.md:17`: «WS34.1/34.2 fijan su timeout» contra `dag.yaml:782` «no WS34»). El de WS13 attempt-1 también (`WS13/.../attempt-1/output.md:10`: transferencia WS13.2→WS13.3 sin arista; `dag.yaml:937-939` no la declara). WS42 attempt-1 no trae FUTURO. Los tres desaparecen en attempt-2 sin defecto comparable; WS42 attempt-2 cita G_PAYLOAD_PRECONDITION, ya advertido en su disposición.
- **Citas:** todas las filas de «Procedencia técnica» que abrí dicen lo que la fila afirma. La tabla inicial del mapa conserva un error de línea para T-P01 (`attribution-map.md:11`: 164-167 como G_SLDB_WRITE), pero la adenda y `decisiones.md:43` lo corrigen.
- **Límites:** no vi cambio de decisión de fondo, contrato ni gate en lo que leí; `dag-diff.txt` solo muestra cambios de evidencia/input hash. Los checks `build`, `validate`, `status`, pytest y los hashes/commits de `tester-facts.log` no los verifiqué.

## No pude verificar

- No ejecuté ningún comando; no comprobé `build_plan.py`, `validate_plan.py`, `context_review.py status`, pytest ni las 73 revisiones.
- No abrí los 73 `output.md` completos, bundles, manifests, recibos, `reconciliation`, `promotion` ni TaskDocs generados.
- No verifiqué los commits `35543965`, `cc8d83da`, `f76c2586`, `47b9e38b` ni el contenido histórico de la tabla inicial.
- No existe `desk/tasks/task-separar*`; leí `desk/drawer/tasks/task-separar-atribucion-en-decisiones-p01-p06.md` y el bloque embebido en `preflight-input.md`.
- Las afirmaciones de `tester-facts.log` son datos del Supervisor, no verificación mía.

RESULTADO: FAIL
