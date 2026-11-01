# WS07: informe de cobertura de decisiones.md (P01-P09)

Fecha: 2026-10-31. Postura: intento de refutar. Solo lectura de `desk/drawer/plans/workspace-documental/{decisiones.md,dag.yaml}` y `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`. No se editó nada fuera de este informe y de result-summary.md.

## 1. Respuestas literales 0-2 (script, comparación byte a byte)

Script Python (`python3 -I`): para cada `answers[i]` de owner-decisions.json se busca en decisiones.md `Ítem i. <question>` y la línea `> <answer>` (comparación de bytes UTF-8).

| Ítem | Pregunta idéntica | Respuesta idéntica (bytes) | Apariciones |
|---|---|---|---|
| 0 | True | True | 1 |
| 1 | True | True | 1 |
| 2 | True | True | 1 |

`source_tool_call` del JSON = `call_387acc8d34de4f35bc4bafab9263bd58`, aparece 1 vez en decisiones.md. Fecha 2026-10-31 coincide con `date` del JSON. Resultado: las tres respuestas están reproducidas exactas.

## 2. Tabla P01-P09 (reclamo vs fuente)

Existencia de nodos/gates verificada con script contra `tasks` y `gates` de dag.yaml: los 37 pares Pxx-nodo existen (64 tareas en dag). Corrección: el informe decía 35, error de recuento. Método: script `python3 -I` que, por cada fila `| Pxx |` de decisiones.md, toma la última columna (nodos y gates), antes del primer `;`, extrae con regex `WS\d+(\.\d+)?(/\d+(\.\d+)?)*`, expande los sufijos separados por `/` a IDs `WSnn` y cuenta IDs únicos por fila: P01 6, P02 3, P03 8, P04 4, P05 3, P06 3, P07 3, P08 4, P09 3 = 37, y los gates G_PRODUCT, G_WRITE_POLICY, G_WRITE_CONTRACT, G_SOURCE, G_SLDB_WRITE y G_CLOSEOUT existen. Ningún nodo citado pierde relación con su decisión (revisados título y scope/acceptance de cada uno).

| Pxx | Tipo/actor en el registro | Ítem citado y texto literal (owner-decisions.json) | Reclamo respaldado | Detalle que la respuesta no dijo | Nodos/gates |
|---|---|---|---|---|---|
| P01 | Humana; solicitante; ítems 0 y 2 | 0: "Sí, mantener esa base y Scion después"; 2: "Sí, yo; acepto Taller y esos objetivos iniciales" | Extender Mindmap; responsable de producto y aceptación de deltas graph_ui/sldb/spec2viz; Scion se designa después | "recepción técnica pendiente por delta" (derivado de G_SLDB_WRITE pending; no dicho) | existen; WS04 y WS13 relacionados (inventario UI, lector); G_PRODUCT satisfied |
| P02 | Humana; solicitante; ítem 0 | 0: "Sí, mantener esa base y Scion después" | SLDB/pron + Deskops, sin migrar a Kimun (la pregunta lo dice; la respuesta lo acepta) | Matiz: la fila dice "Kimun fuera de esta línea base"; el ítem 0 dice "sin migrar a Kimun". "Kimun fuera" es literal de `baseline_proposal` (dag.yaml raíz: "Kimun fuera y Scion posterior"), no del ítem | existen; G_PRODUCT |
| P03 | Humana; solicitante; "pregunta y respuesta ítem 1" | 1: "Markdown editable tras probar API reversible, conflictos y campos protegidos" | Solo "con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado" (premisa de la pregunta 1, aceptada) | "canal público", "autoridad compartida CLI/agentes/UI", "probado", "lock solo UI no basta": ni la pregunta ni la respuesta del ítem 1 lo dicen. Origen real: documentos de planificación (`taskdoc-frozen.md`, `preflight-input-v2.md` líneas 127-128: "Canal seguro = API con contrato y autoridad para coordinar escritores CLI/agentes/UI, no lock solo UI"), no citado en la fila | existen; WS34/WS36 (Scion) relacionados por autoridad del coordinador; G_WRITE_POLICY satisfied, G_WRITE_CONTRACT pending |
| P04 | Humana; solicitante; ítem 1 | 1: "Markdown editable tras probar API reversible, conflictos y campos protegidos" | source_mode=editable; guardar tras API reversible, conflictos y campos protegidos | "con revisión" y "recuperación" (no están en la respuesta; sí en G_SOURCE/WS20 y en el encargo) | existen; G_SOURCE y G_SLDB_WRITE pending (correcto: no concede edición). dag.yaml cita P04 en la evidencia de G_WRITE_POLICY, pero la fila P04 no lista G_WRITE_POLICY (ver observación O3) |
| P05 | Humana; solicitante; "pregunta y respuesta ítem 1" | 1 (pregunta): "guardar no hace commit; cierre y promoción respetan el workflow Deskops" | "Guardar no hace commit" y cierre por workflow: premisa de la pregunta, aceptada | "CLI/coordinador" y "refresco verificable" no están en el ítem | existen; G_WRITE_POLICY satisfied; G_CLOSEOUT satisfied |
| P06 | Humana; solicitante; "pregunta y respuesta ítem 1" | 1 (pregunta): "cierre y promoción respetan el workflow Deskops; ... lectura/handoff hasta contar con un canal de escritura coordinado" | Promoción y cierre por workflow Deskops | "preparar" y "canal completo comprobado" (la pregunta dice "coordinado") | existen; G_WRITE_POLICY |
| P07 | Técnica conservadora; "Executor por encargo TaskDoc v2"; sin firma humana | n/a (no hay ítem) | Respaldado solo en parte: `preflight-input-v2.md` 108-113 dice "P07 es estado local+lectura interdesk ... defaults técnicos ... sin requerir nueva firma humana" | "multidesk inicialmente read-only con rutas/aliases explícitos" no está en la fuente citada (ver O6) | existen; G_PRODUCT |
| P08 | Humana; solicitante; ítem 2 | 2: "Sí, yo; acepto Taller y esos objetivos iniciales" | Taller temporal; solicitante participa; abrir/buscar ≤2 s, guardar ≤3 s, arranque ≤10 s (cifras en la pregunta 2, aceptadas) | "actas humanas aún pendientes" es un estado, no una decisión; consistente con WS16/WS30 candidate | existen; G_PRODUCT |
| P09 | Técnica conservadora; "Executor por encargo TaskDoc v2"; sin firma humana | n/a | Respaldado solo en parte: la fuente citada dice "ubicación de entradas en desk/README.md + mapa authored en deskops" | "entradas reales", "reutilizando registry" y "publicar WS43 tras validación" salen del DAG (WS43, dag.yaml ~2804-2822), no de la fuente citada (ver O6) | existen; G_PRODUCT |

Actor, tipo y fuente están presentes en las 9 filas. Fecha común 2026-10-31 declarada en el encabezado de la tabla. La fuente de P07/P09 es "Executor por encargo TaskDoc v2" sin ruta de archivo.

## 3. P07 y P09 sin firma humana

- decisiones.md: tipo "Técnica conservadora"; no hay actor humano ni ítem.
- dag.yaml: nodo WS07 scope dice "P07/P09 son defaults técnicos delegados, no firmas humanas" (línea ~541); `context-review-guide.md` línea 16 igual. Búsqueda de P07/P09 en dag.yaml: ninguna aparición los presenta como firma humana.
- Gates: G_PRODUCT.verified_evidence y G_WRITE_POLICY.verified_evidence dicen "P07/P09 defaults técnicos delegados". Ver observación O1 sobre G_PRODUCT.

Resultado: ningún documento revisado les atribuye una firma o actor humano (no hay atribución de firma). Matiz: el título de G_PRODUCT ("registradas por humano") más su lista de `evidence` (P01/P02/P04/P07/P08/P09) los agrupa bajo un gate de decisiones humanas; `verified_evidence` desambigua que son defaults técnicos (observación O1).

## 4. baseline_proposal y parameters.source_mode

- `baseline_proposal` (dag.yaml raíz): "Base acordada 2026-10-31: Mindmap existente + SLDB/pron + Deskops, lector y manual primero; Kimun fuera y Scion posterior. Aprobación de producto no acredita contratos ni habilita ejecución." Coincide con ítem 0 ("extender el Mindmap existente usando SLDB/pron y Deskops, sin migrar a Kimun, con lectura y operación manual primero y Scion como ramal posterior" / "Sí, mantener esa base y Scion después"). Sin añadidos de decisión.
- `parameters.source_mode`: value `editable`, allowed [pending, editable, read_only], decided_by "P04/WS07", evidence "habilitación real requiere G_SOURCE". Coincide con ítem 1 ("Markdown editable tras probar ...") y G_SOURCE sigue `pending`, por lo que no se concede edición real.
- `execution_authorized`: False.

## 5. Estado de gates

- G_PRODUCT: state `satisfied`, produced_by WS07, evidence "no aprobación técnica ni Scion". No infiere API/UI ni Scion.
- G_WRITE_POLICY: state `satisfied`, produced_by WS07, evidence "no aprobación técnica ni Scion". No infiere API/UI ni Scion.
- Contraste: G_SOURCE pending, G_WRITE_CONTRACT pending (accepted_scope_nodes vacío), G_SLDB_WRITE pending, G_EXEC pending, G_SCION `unverified`. Ninguno se da por concedido. decisiones.md dice "G_EXEC/G_SCION siguen pendientes" y que "Ninguna decisión autoriza dispatch, mensajes o acceso Scion": no contradice.
- Requisitos: G_WRITE_POLICY lo requiere solo WS12; G_PRODUCT lo requieren WS08, WS09, WS10, WS11, WS43, WS44.

## 6. WS45 y G_PAYLOAD_PRECONDITION

Ninguno aparece en decisiones.md. Son derivados posteriores (WS45 produce G_PAYLOAD_PRECONDITION, pending, "no hay evidencia de que exista ni esté aceptado"), independientes de source_mode y G_SOURCE. No cambian ninguna decisión Pxx y su ausencia no vuelve falsa ninguna fila. Es una observación (O4), no un defecto.

## 7. Defectos

**D1. P03: detalle atribuido al ítem 1 que el ítem 1 no dice (fuente real no citada).** La fila P03 (tipo "Humana", fuente "pregunta y respuesta ítem 1") afirma "canal público con autoridad compartida CLI/agentes/UI probado; lock solo UI no basta". La pregunta del ítem 1 dice solo "la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado" y la respuesta es "Markdown editable tras probar API reversible, conflictos y campos protegidos". "Público", "autoridad compartida", "CLI/agentes/UI", "probado" y "lock solo UI no basta" proceden del documentos de planificación (`runs/subagents/20261031-finalizar-plan-workspace/taskdoc-frozen.md` y `preflight-input-v2.md` líneas 127-128), que no es un ítem 0-2 ni está citado. Así, una fila marcada humana con fuente ítem 1 contiene contenido cuya fuente citada no lo respalda. Misma clase, de menor gravedad: P04 ("con revisión", "recuperación"), P05 ("CLI/coordinador", "refresco verificable"), P06 ("preparar", "canal completo comprobado"), P01 ("recepción técnica pendiente por delta"). Ninguno contradice una decisión ni cambia un gate. P01, P04, P05 y P06 son el mismo tipo de atribución que P03, de menor alcance. No se corrige aquí.

### 7.1 Fundamento del dictamen y postura contraria

- Fundamento (autoría: decisión del Supervisor): la aceptación exige tipo humano/técnico por decisión, y P03 rotula "Humana" una precisión técnica que ninguna persona dijo, por lo que ese campo es falso para esa parte, aunque la decisión de fondo y la cita existan.
- Postura contraria del Tester independiente (sin suavizar): D1 no cae en ninguna de las cuatro causas de edición (dato falso, fila sin actor o fuente, cita inexistente, cambio real de decisión): P03 tiene actor, fuente y cita existente, y el núcleo está en el ítem 1; es una observación de fidelidad/procedencia y el dictamen debería ser CUBIERTO con observaciones. Añade que, si D1 es observación, P01/P04/P05/P06 también lo son.

## 8. Observaciones (no defectos)

- O1. G_PRODUCT tiene título "Decisiones de producto registradas por humano" y su `evidence` enumera P01/P02/P04/P07/P08/P09, incluyendo P07/P09 bajo ese título. `verified_evidence` aclara que P07/P09 son defaults técnicos, por lo que no hay atribución explícita de firma, pero la lectura aislada del título más la lista es ambigua.
- O2. G_WRITE_POLICY.verified_evidence cita "P07/P09 defaults técnicos" aunque ni P07 ni P09 están en sus filas ni en su `evidence` (P03/P04/P05/P06): texto copiado, irrelevante.
- O3. dag.yaml G_WRITE_POLICY.evidence incluye P04, pero la fila P04 de decisiones.md lista G_PRODUCT/G_SOURCE/G_SLDB_WRITE y no G_WRITE_POLICY. Referencia cruzada incompleta; no falsea la decisión.
- O4. WS45 y G_PAYLOAD_PRECONDITION no figuran en decisiones.md (ver sección 6). Sin efecto sobre filas.
- O5. decisiones.md dice "G_EXEC/G_SCION siguen pendientes"; G_SCION está en `unverified`, no `pending`. Matiz de vocabulario, no cambia el sentido (no concedido).
- O6. Procedencia de P07/P09: son filas técnicas, sin atribución humana, pero con fuente incompleta. La fuente citada ("Executor por encargo TaskDoc v2", sin ruta) respalda solo "estado local + lectura interdesk" y "entradas en desk/README.md + mapa authored en deskops" (`preflight-input-v2.md` 108-113). "Multidesk inicialmente read-only con rutas/aliases explícitos" (P07) y "entradas reales, reutilizando registry, publicar WS43 tras validación" (P09) no están ahí; salen del DAG. Corrige la afirmación previa de que el respaldo era completo.
- O7. Los 6 gates restantes y WS07 `covered_work` coinciden con lo registrado ("decisions_documented_pending_audit_reconciliation").

DICTAMEN: DEFECTO REAL
