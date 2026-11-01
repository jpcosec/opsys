# Mapa de atribución P01-P09

Archivo editado: `desk/drawer/plans/workspace-documental/decisiones.md` (único). Rutas relativas a `/home/jp/proyectos/SLDB_1/deskops`. `PIv2` = `runs/subagents/20261031-finalizar-plan-workspace/preflight-input-v2.md` (introducido en cc8d83da). `TF` = `.../finalizar-plan-workspace/taskdoc-frozen.md` (cc8d83da). `PI` = `.../finalizar-plan-workspace/preflight-input.md`. `Tabla inicial` = `decisiones.md` en commit 35543965 (primera versión del archivo; título «propuestas, pendientes de confirmación WS07», estado PENDING_OWNER; sin autor declarado más allá del commit). `OD` = `.../finalizar-plan-workspace/owner-decisions.json`. `dag` = `desk/drawer/plans/workspace-documental/dag.yaml` en el árbol actual (regla vigente, no prueba de autoría). Todas las fuentes se abrieron y se confirmó el texto.

Etiquetas: Humana / Técnica derivada / Técnica conservadora (P07, P09, ya en el archivo) / Técnica sin registro histórico localizado (no se necesitó: toda precisión tiene al menos un registro).

| Pxx | Fragmento | Tipo | Fuente exacta | Límite |
|---|---|---|---|---|
| P01 | Extender Mindmap; Operador Scion se designa después | Humana | OD ítem 0 respuesta «Sí, mantener esa base y Scion después» (pregunta: «extender el Mindmap existente»); ítem 2 pregunta «Scion se designa cuando abordemos ese ramal» | Ninguno |
| P01 | Solicitante responsable producto/aceptación de deltas graph_ui/sldb/spec2viz | Humana | OD ítem 2 pregunta + respuesta «Sí, yo» | Ninguno |
| P01 | Recepción técnica pendiente por delta (columna de nodos, sin mover) | Técnica derivada | PIv2 131-133 («Aceptación por delta = acta con actor receptor designado...»); vigente dag 164-167 (G_SLDB_WRITE) | Sin registro histórico de quién lo decidió; ningún ítem lo dice |
| P02 | SLDB/pron + Deskops; Kimun fuera de esta línea base (sin reescribir, per root) | Humana | OD ítem 0 pregunta «sin migrar a Kimun» + respuesta | «Kimun fuera» es vocabulario de `baseline_proposal` (dag), no literal del ítem; se mantiene como indicó root |
| P03 | Con otro coordinador escritor, UI read-only/handoff hasta contar con un canal de escritura coordinado | Humana | OD ítem 1 pregunta («la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado»), aceptada por la respuesta | Es premisa de la pregunta; la respuesta no la repite |
| P03 | Canal público con autoridad compartida CLI/agentes/UI, probado; lock solo UI no basta | Técnica derivada | PIv2 127-128 («Canal seguro = API con contrato y autoridad para coordinar escritores CLI/agentes/UI, no lock solo UI»); mismo texto en TF 73; antecedente en Tabla inicial línea 9 («canal autorizado real. No fingir lock compartido con CLI»); vigente dag 763-764 | Antecedente es propuesta sin aceptación; PIv2 es encargo técnico, no aprobación humana; no hay aceptación humana de «público» ni de «probado» |
| P04 | source_mode=editable; guardar Markdown tras probar API reversible, conflictos y campos protegidos | Humana | OD ítem 1 respuesta «Markdown editable tras probar API reversible, conflictos y campos protegidos» | Se quitó «solo»/«probados» del reformulado; el sentido es el mismo |
| P04 | Con revisión; recuperación | Técnica derivada | PIv2 124-126 («revisión esperada ... falla sin perder buffer si revisión cambia ... roundtrip/conflicto/recuperación»); vigente dag 44-49 (G_SOURCE), 1406-1408 (WS20) | Tabla inicial línea 10 no los contiene; primer registro hallado es PIv2 (cc8d83da); autor no declarado |
| P05 | Guardar no hace commit; cierre respeta el workflow Deskops | Humana | OD ítem 1 pregunta («guardar no hace commit; cierre y promoción respetan el workflow Deskops»), aceptada por la respuesta | Premisa de la pregunta, no repetida en la respuesta |
| P05 | Cierre por CLI/coordinador | Técnica derivada | Tabla inicial línea 11 («closeout commit fuera de HTTP, con handoff visible»); vigente dag 1980-1984 (WS28: «deskops closeout commit por CLI en modo manual, o al coordinador si está activo (P03)») | Propuesta inicial sin autor ni aceptación explícita |
| P05 | Refresco verificable | Técnica derivada | Tabla inicial línea 11 («refresco que verifica resultado»); vigente parcial dag 1980-1981 («Verificar con deskops closeout verify») | Solo respaldo derivado; no se halló «refresco verificable» en dag |
| P06 | Promoción y cierre respetan workflow Deskops; lectura/handoff hasta canal de escritura coordinado | Humana | OD ítem 1 pregunta (ambas cláusulas), aceptada por la respuesta | Premisa de la pregunta |
| P06 | Preparar; canal completo comprobado | Técnica derivada | Tabla inicial línea 12 («Solo ofrecer mutación cuando WS12 documente canal completo y efectos; de otro modo preparar/handoff manual»); gate vigente dag 122-131 (G_WRITE_CONTRACT: «canal público ... pruebas reales») | La frase «canal completo» no está en dag; el gate es respaldo derivado; propuesta inicial sin autor |
| P07 | Foco/historia/disposición locales | Técnica conservadora | Tabla inicial línea 13; PIv2 107-110 («estado local+lectura interdesk ... defaults técnicos documentados por Executor al terminar plan y revisables, sin requerir nueva firma humana»); TF 59; vigente dag 541-542 | PIv2 delega el default; ningún humano lo firmó; «disposición» solo en la fila actual y sin registro propio localizado como término (cubierto por «estado local») |
| P07 | Multidesk inicialmente read-only con rutas/aliases explícitos | Técnica conservadora | Registro histórico: Tabla inicial línea 13 («Multidesk inicialmente lectura y rutas/aliases explícitos, sin mutación cruzada»); encargo: PI 32-33 y TF 59 («P07 local/read-only multidesk ... decisiones técnicas conservadoras ... delegadas por el encargo»); vigente dag 693-695 (WS11), 1188-1196 (WS17) | Autor de la propuesta inicial no declarado (el commit es de github-actions[bot]); dag no prueba quién lo decidió |
| P08 | Taller temporal; solicitante participa; abrir/buscar ≤2 s, guardar ≤3 s, arranque ≤10 s (sin reescribir, per root) | Humana | OD ítem 2 pregunta (cifras) + respuesta «acepto Taller y esos objetivos iniciales» | «Actas humanas aún pendientes» es estado, no decisión |
| P09 | Entradas en desk/README.md + mapa authored en deskops | Técnica conservadora | Tabla inicial línea 14; PIv2 107-110 («ubicación de entradas en desk/README.md + mapa authored en deskops»); TF 59 («P09 rutas authored») | Delegado por el encargo; sin firma humana |
| P09 | Reutilizando registry; publicar WS43 tras validación; entradas reales | Técnica conservadora | Registro histórico: Tabla inicial línea 14 («reutilizando registry; publicar en deskops por WS43 después del ejemplo»); vigente dag 2804-2830 (WS43: «no publicar solo ejemplo como si fuera ecosistema real», «validados en Taller») y 1185-1196 (WS17: «Registry = desk/registry/repo-*.md ... WS43 lo reutiliza») | Autor de la propuesta inicial no declarado; PIv2 108-110 no contiene registry ni WS43 (confirmado); «tras validación» solo con respaldo vigente en WS43 |

## Verificación literal de respuestas 0-2 tras la edición

Script `python3 -I` con `owner-decisions.json` y `decisiones.md` (bytes UTF-8): para cada `answers[i]` se busca `Ítem i. <pregunta>\n\n> <respuesta>\n`.

| Ítem | Bloque pregunta+respuesta idéntico | Apariciones |
|---|---|---|
| 0 | True | 1 |
| 1 | True | 1 |
| 2 | True | 1 |

`source_tool_call` `call_387acc8d34de4f35bc4bafab9263bd58`: 1 aparición. Filas `| P01 |` a `| P09 |`: una cada una. Última columna (nodos y gates) de las 9 filas sin cambio frente a HEAD (diff).

## Límites generales

- No existe registro de autor de la Tabla inicial (35543965) más allá del commit; no se atribuye a persona.
- PIv2, PI y TF son encargo técnico, no aprobación humana.
- No se tocó dag.yaml, helper, validadores ni gates; no se corrió `context_review.py run`; sin commits.

## Adenda 2026-10-31, revisión del Supervisor antes de congelar

Claude Opus 5.5, pane `w3Y:p1`, abrió cada rango de `dag.yaml` citado y corrigió tres celdas de `decisiones.md` directamente, sin Executor. Las filas anteriores de este mapa quedan como se escribieron; donde difieran, vale esto:

- T-P01: 164-167 está en G_UI_READ, no en G_SLDB_WRITE. Vigente: 161-167 (G_UI_READ) y 225-233 (G_SLDB_WRITE).
- T-P05: 1980-1984 y 1980-1981 caen en la lista de gates de WS28. Vigente: 1984-1987 (scope) y 1991-1994 (acceptance).
- «Refresco verificable»: era falso que no tuviera respaldo vigente. WS28 acceptance dice que `deskops show task` y el commit de closeout confirman el cierre y que se refresca el estado desde deskops. Lo que no aparece es esa frase literal.
- T-P07: se agrega 945-946 (WS13.3), respaldo directo de la disposición local.

Las demás citas a `dag.yaml` se abrieron y coinciden. «Canal completo» sigue sin frase vigente.

## Adenda 2 — 2026-10-31, tras Tester FAIL

Claude Opus 5.5, pane `w3Y:p1`, corrigió `decisiones.md` directamente. Donde difiera, vale esto:

- P01: la fila decía «Operador Scion se designa después»; el ítem 2 dice «Scion se designa cuando abordemos ese ramal». «Operador» pasa a T-P01, con fuente. Esto no lo marcó el Tester: lo vi al releer.
- P03: vuelve al texto de la pregunta, «con otro coordinador escribiendo, la UI queda en lectura/handoff». No cambia el sentido; quita paráfrasis.
- P04: era falso que se hubiera quitado «solo». Ahora la fila dice «Markdown editable tras probar…», como la respuesta. `source_mode=editable` se conserva como parámetro de baseline.
- P06: la corrección anterior perdió la condición «con otro coordinador escribiendo», y la fila Humana afirmaba más de lo aceptado. Recuperada. T-P06 conserva la precisión técnica.

El Tester también señaló como no literales P05 y lo que queda de P01. El criterio de root es «conserva solo lo aceptado», no copia literal; esas omisiones no agregan nada. El Tester las marcó porque mi brief pedía «literalmente», más estricto que el contrato.

## Adenda 3 — 2026-11-01, decisión root

Claude Opus 5.5, pane `w3Y:p1`, corrigió `decisiones.md` y `context-review-guide.md` directamente, por `root-decision-20261101.md`. Donde difiera, vale esto:

- P07 y P09: mi parche quitó «Executor por encargo TaskDoc v2» y este mapa no lo declaró. Fue una omisión mía contra la orden de mantener actores. No la detectaron ni la revisión del Supervisor ni los Tester v1 y v2. La levantó el revisor de WS07 en la tanda 2. Restituido como actor técnico registrado, que no prueba la autoría inicial, sin localizar.
- T-P03.1, nueva: WS12 produce la definición operativa de «modo manual exclusivo». Origen: revisión root 2026-11-01, no el ítem 1.
- Guía: núcleo humano frente a derivaciones técnicas, y dry-run por aristas reales.
