---
id: task-finalizar-plan-workspace-documental
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- a8601fe
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/drawer/plans/workspace-documental/README.md
- bd93985
- runs/subagents/20261031-finalizar-plan-workspace/tester-result-summary.md
- runs/subagents/20261031-finalizar-plan-workspace/council/summary.md
- desk/drawer/plans/workspace-documental/cierre.md
depends_on: []
pills:
- pill-001
- pill-005
- pill-007
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-finalizar-plan-workspace-documental.md
closeout_evidence:
- commit
- document
---

# Finalizar plan workspace reconciliado y revisado

## Rationale

_Explain why this task exists or the business driver behind it._

El solicitante pide terminar el plan y confirmó las decisiones de núcleo en owner-decisions.json, después del cierre de revisión barata a8601fe.

## Goal

_Describe the concrete result this task must produce._

Entregar un plan final coherente con decisiones humanas registradas, referencias externas actuales, deltas reales, ramales opcionales desacoplados y reviews baratos vigentes. No implementar producto.

## Scope

_State what is in scope and what is out of scope._

Solo desk/drawer/plans/workspace-documental/, desk/drawer/tasks/workspace-documental/ y evidencia runs/subagents/20261031-finalizar-plan-workspace/. Se permite usar runner existente context_review.py que escribe evidencia nueva en runs/subagents/20261031-workspace-context-reviews/context-review/; no sobrescribir intentos existentes. No modificar código de producto, rituales/skills/Board de repos hermanos ni cambios dirty ajenos. Supervisor administra TaskDoc/Board/cierre.

## Implementation Path

_Outline the expected implementation route or affected surface._

Executor independiente lee TaskDoc, pills 001/005/007 y ritual-context-review; fuentes explícitas: desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,alcance.md,decisiones.md,reconciliacion.md,cobertura.md,validacion-humana.md,context-review-guide.md,borradores/*.md,build_plan.py,validate_plan.py,context_review.py,render_diagram.py}; evidencia de decisiones en runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json; revisión previa a8601fe y runs/subagents/20261031-workspace-context-reviews/result-summary.md. Leer estado actual de git y Board de ../UIs/graph_ui, commits a1b2b22/f16fcd1/134a665 y código workspace_routes.py, views/workspace/node/, deskops_routes.py; deskops commits 59244c9/1fefa97 y tests/test_closeout_declared_evidence.py/evidencia de cierre. Refs borradas por closeout se reemplazan por código/documento durable actual y recibos git show verificables de tarea histórica, nunca recrear task activa desaparecida.
Registrar tres respuestas humanas exactas con actor/fecha/origen: host Mindmap+SLDB/pron+Deskops, Kimun fuera y Scion posterior; source_mode=editable solo tras guardas reales, guardar sin commit y cierre/promoción por workflow, UI read-only/handoff con coordinador escritor hasta canal seguro; humano solicitante acepta deltas graph_ui/sldb/spec2viz y participa en Taller, objetivos 2s lectura/búsqueda, 3s guardado, 10s arranque. P01/P02/P03/P04/P05/P06/P08 se actualizan de acuerdo al alcance literal confirmado, sin extenderlo a aceptación de implementación ni permisos Scion. P07 local/read-only multidesk y P09 rutas authored son decisiones técnicas conservadoras de este plan delegadas por el encargo, no atribuir firma humana no dada; sacar requisitos de firma artificiales. Modelo de producto aprobado no equivale a contrato técnico o API comprobada. Operador/permisos Scion se designan al abordar ramal y no bloquean L/M.
Reconciliar workspace base real con deltas WS13 y sus hijos, WS14/15/19/22–24/27–29/32; no dar nodos completos porque hay commit: distinguir reutilización comprobada de aceptación expandida pendiente. Workspace cerrado con código real no draft; editing y Changes siguen drafts con hashes actuales. G_CLOSEOUT: verificar evidencia focalizada de contrato y recibos; si todavía falta prueba de autoridad/identidad requerida, dejar condición concreta pendiente con productor/artefacto verificable y tarea documental de revalidación explícita si no hay productor, no referencia a task borrada. No exigir suite global verde para llamar claro a un plan; registrar riesgos reales de validación existente, sin arreglar producto ni fingir éxito.
Corregir contradicciones: Scion posterior no bloquea producto núcleo; navegación base no espera aceptación spec2viz opcional; aceptación receptora y whitelist se registran por delta concreto y efecto, sin obligar reader/manual a esperar Changes/modelos/Scion. Cada gate conserva productor, condición, evidencia y scope; si hay split añadir IDs acotados y revisar todos nuevos, actualizar cobertura/aristas. Fuente editable espera G_SOURCE real; no concederlo por decisión. Mutaciones requieren G_HUMAN_READ para habilitar uso en UI, no prohibir desarrollo/pruebas aisladas de API. Toda capacidad desconocida queda clasificada y con tarea/productor, no workaround. Conservar root/PK/WS01–44/19 hijos ya trazados; añadir nodos solo si falta entregable real, nunca para pulido editorial.
Preparar cierre.md dentro paquete con base acordada, qué existe/qué resta, secuencia por entregas y primera capa preparable, quién decide/ejecuta/acepta, manual/vistas/user-flows y evidencia, condiciones reales de inicio. Identificar paquete final terminado como planificación, execution_authorized=false y candidatas aún no TaskDoc. Decisiones humanas no sustituyen actas de uso/capability/recepción técnica. No afirmar que producto está disponible. Plan final debe poder leerse sin chat.
Regenerar desde dag.yaml. Modificar helpers .py locales solo si hace falta soportar estados finales/recibos/ramal y comprobarlos con semántica real; no debilitar validación para ocultar pendiente. context_review.py status detecta inputs afectados: corregir fuentes primero y congelar, luego lanzar solo afectados con Pi deepseek-flash low NUEVO proceso por nodo/intento, no-session/no-context-files/no-skills/no-extensions/no-prompt-templates/no-tools, stdin=DEVNULL; recibos exactos, no reviews anteriores en input, guardar reformulación/ambigüedades/dry-run sin ejecutar. Supervisor/Executor compara cada output contra intención, dispone hallazgos con cita real/razón, corrige y re-revisa. APTO no basta. Gates/decisiones suministrados cambiados invalidan afectados; no marcar vigente sin input actual. Evidencia extra append-only en run previo permitida, resumen/receipts nuevos en run de esta tarea. No pedir concilio experto para salvar comprensión; supervisor consulta concilio final separado y Tester independiente al acabar. Executor NO commitea, NO cierra ni cambia Board. Handoff incluye findings/disposiciones y limitaciones.
Precisiones v2 (parte del encargo, no historial de review):
Pregunta 0: Para la primera entrega, ¿confirmamos extender el Mindmap existente usando SLDB/pron y Deskops, sin migrar a Kimun, con lectura y operación manual primero y Scion como ramal posterior?
Respuesta humana exacta: Sí, mantener esa base y Scion después
Pregunta 1: ¿Qué alcance de edición dejamos en el plan? En ambos casos: guardar no hace commit; cierre y promoción respetan el workflow Deskops; con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado.
Respuesta humana exacta: Markdown editable tras probar API reversible, conflictos y campos protegidos
Pregunta 2: ¿Quedas tú como responsable de producto y aceptación de deltas en graph_ui, SLDB y spec2viz, y como participante de las pruebas de uso sobre el proyecto temporal Taller? Los objetivos iniciales serían abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s; Scion se designa cuando abordemos ese ramal.
Respuesta humana exacta: Sí, yo; acepto Taller y esos objetivos iniciales
Actor: humano solicitante de esta sesión, identificable por call_387acc8d34de4f35bc4bafab9263bd58 ítems 0–2 y fecha 2026-10-31; owner-decisions.json guarda origen/literal. Mapeo mínimo: respuesta0→P01(host),P02(stack), ramal E posterior; respuesta1→P03(concurrencia),P04(editable),P05(Git/cierre),P06(promoción por workflow); respuesta2→responsables P01 y P08(Taller/objetivos). P07 es estado local+lectura interdesk; P09 es ubicación de entradas en desk/README.md + mapa authored en deskops, ambos defaults técnicos documentados por Executor al terminar plan y revisables, sin requerir nueva firma humana. Suficiencia: cada decisión registra resultado concreto, tipo humano/técnico, actor y fuente, nodos/gates afectados; no inventa aprobación de APIs, código, actas de uso o Scion. Los 9 IDs ya existen en decisiones.md y se actualizan, no hay decisiones de producto nuevas delegadas.
Mapear deltas es el entregable de reconciliación de esta tarea: fuentes/commits exactos arriba; no se exige que reviewer lo haya auditado. Auditoría acotada read-only de esas superficies sí es trabajo del Executor; no auditoría completa de todos los repos. Primera capa preparable = nodos delivery cuyas dependencias están probadas y gates satisfechos; si solo WS01 cumple, mostrarlo sin llamar ready a su paquete. Candidatas existentes son fichas generadas en desk/drawer/tasks/workspace-documental/ desde tasks de dag.yaml; siguen status=candidate y execution_authorized=false en DAG. No escribir TaskDoc por WS en esta tarea.
G_SOURCE tiene productor WS20 en sldb: API pública guarda fuente con revisión esperada, extracción/validación/roundtrip, preserva campos protegidos y falla sin perder buffer si revisión cambia; evidencia son contrato API y pruebas reales de roundtrip/conflicto/recuperación. No se ejecuta WS20 ahora. Canal seguro = API con contrato y autoridad para coordinar escritores CLI/agentes/UI, no lock solo UI; hasta verificarse, UI read-only/handoff cuando otro coordinador escribe. Taller = corpus generado WS40 en graph_ui:.tmp/workspace-documental-ejemplo/, dos desks y repo sin desk para escenarios UF; validacion-humana.md define guion/mediciones. Aceptación por delta = acta con actor receptor designado, alcance concreto e IDs cubiertos, fecha y evidencia en repo dueño; no requiere aceptar otras extensiones para aceptar lector.
G_CLOSEOUT exige implementación/commit verificable y pruebas focalizadas del contrato de evidencia declarada y autoría de cierre, no mera desaparición de task. Inspeccionar tests/test_closeout_declared_evidence.py y tests/test_lifecycle_end_to_end.py existentes. Si se propone satisfied, nuevo tester corre pytest focalizado (puede ser pytest -q tests/test_closeout_declared_evidence.py tests/test_lifecycle_end_to_end.py -k 'closeout') y registra comandos/salida/exit/commit en run de esta tarea. Si evidencia aún falta, añadir WS45 (owner_repo=deskops, delivery, validación no implementación) para revalidar contrato con esos comandos, productor de G_CLOSEOUT; requiere cero permiso de UI y no bloquea lector. Scope archivo test/código solo lectura. La prueba debe comprobar autoría/relación task-commit real o dejar el escenario faltante bloqueado; no se declara satisfied por solo contar tests.
Matriz invalidación = exactamente la que implementa context_review.py: nuevo input/contract hash de nodo o fragmento suministrado invalida ese nodo; status calcula afectados, runner --stale lanza solo esos. Si se cambia guide/brief/alcance/decisiones/cobertura usados por todos, revisar todos. No mandar output/disposiciones previas al modelo. Cada nuevo hijo, agrupador o WS45 se añade a all_nodes y recibe review real; contratos arista suministrados cambian inputs según builder, la validación final exige cero stale. Rúbrica: comparación identifica propósito/resultado/repo/límites, secuencia y autoridad del dry-run, aceptación comprobable y ausencia de decisiones de encargo sin dueño. Hallazgo descartado requiere cita real o razón verificable de trabajo futuro asignado; no basta APTO.
Supervisor lanzará un nuevo Tester disponible por collaboration.spawn_agent fork_turns=none, con TaskDoc, owner answers, handoff y fuentes/rutas explícitas; no participó en Executor ni cambia plan. Evidencia nueva validation.log/result-summary.md; PASS/FAIL con muestras de todos reviews nuevos y limitaciones. Concilio final son los 3 panes expertos existentes de Herdr (Claude/DeepSeek/Gemini) consultados por supervisor tras congelar plan; no modifican archivos ni acreditan cheap review, solo dictamen separado con bloqueantes concretos. Supervisor cierra después. cierre.md es texto authored redactado por Executor, no generado; README/fichas/spec/diagramas/validation son proyecciones de helpers. Corregir incoherencia existente de build_plan.py: no imprimir “Revisión barata pendiente” cuando status=reviewed. No tocar ritual oficial ni código producto.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status: all reviews current
- Independiente: integridad/hashes/aislamiento/cobertura/dry-runs de todos los reviews nuevos; refs actualizadas y decisiones trazadas; ninguna autorización producto ni gate humano falso
- Validación focalizada de G_CLOSEOUT por tester si se propone satisfecho; no ejecutar suite global larga ya fallida salvo cambio o hallazgo que lo justifique. Para helpers .py usar checks semánticos y pytest focalizado apropiado; registrar baseline externo.

## Done When

_Name the observable condition that makes the task complete._

Plan final consistente, sin referencias obsoletas conocidas ni decisiones de núcleo sin dueño, ramales opcionales independientes, pendientes técnicos explícitos con productor/evidencia, reviews baratos vigentes y tester independiente; cierre oficial propio y fase documental. No producto ejecutado.
