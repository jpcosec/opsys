FILE:desk/drawer/tasks/task-finalizar-plan-workspace-documental.md
# Finalizar plan workspace reconciliado y revisado

id: task-finalizar-plan-workspace-documental
title: Finalizar plan workspace reconciliado y revisado
why: El solicitante pide terminar el plan y confirmó las decisiones de núcleo en owner-decisions.json,
  después del cierre de revisión barata a8601fe.
goal: Entregar un plan final coherente con decisiones humanas registradas, referencias
  externas actuales, deltas reales, ramales opcionales desacoplados y reviews baratos
  vigentes. No implementar producto.
scope: Solo desk/drawer/plans/workspace-documental/, desk/drawer/tasks/workspace-documental/
  y evidencia runs/subagents/20261031-finalizar-plan-workspace/. Se permite usar runner
  existente context_review.py que escribe evidencia nueva en runs/subagents/20261031-workspace-context-reviews/context-review/;
  no sobrescribir intentos existentes. No modificar código de producto, rituales/skills/Board
  de repos hermanos ni cambios dirty ajenos. Supervisor administra TaskDoc/Board/cierre.
implementation_path: 'Executor independiente lee TaskDoc, pills 001/005/007 y ritual-context-review;
  fuentes explícitas: desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,alcance.md,decisiones.md,reconciliacion.md,cobertura.md,validacion-humana.md,context-review-guide.md,borradores/*.md,build_plan.py,validate_plan.py,context_review.py,render_diagram.py};
  evidencia de decisiones en runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json;
  revisión previa a8601fe y runs/subagents/20261031-workspace-context-reviews/result-summary.md.
  Leer estado actual de git y Board de ../UIs/graph_ui, commits a1b2b22/f16fcd1/134a665
  y código workspace_routes.py, views/workspace/node/, deskops_routes.py; deskops
  commits 59244c9/1fefa97 y tests/test_closeout_declared_evidence.py/evidencia de
  cierre. Refs borradas por closeout se reemplazan por código/documento durable actual
  y recibos git show verificables de tarea histórica, nunca recrear task activa desaparecida.

  Registrar tres respuestas humanas exactas con actor/fecha/origen: host Mindmap+SLDB/pron+Deskops,
  Kimun fuera y Scion posterior; source_mode=editable solo tras guardas reales, guardar
  sin commit y cierre/promoción por workflow, UI read-only/handoff con coordinador
  escritor hasta canal seguro; humano solicitante acepta deltas graph_ui/sldb/spec2viz
  y participa en Taller, objetivos 2s lectura/búsqueda, 3s guardado, 10s arranque.
  P01/P02/P03/P04/P05/P06/P08 se actualizan de acuerdo al alcance literal confirmado,
  sin extenderlo a aceptación de implementación ni permisos Scion. P07 local/read-only
  multidesk y P09 rutas authored son decisiones técnicas conservadoras de este plan
  delegadas por el encargo, no atribuir firma humana no dada; sacar requisitos de
  firma artificiales. Modelo de producto aprobado no equivale a contrato técnico o
  API comprobada. Operador/permisos Scion se designan al abordar ramal y no bloquean
  L/M.

  Reconciliar workspace base real con deltas WS13 y sus hijos, WS14/15/19/22–24/27–29/32;
  no dar nodos completos porque hay commit: distinguir reutilización comprobada de
  aceptación expandida pendiente. Workspace cerrado con código real no draft; editing
  y Changes siguen drafts con hashes actuales. G_CLOSEOUT: verificar evidencia focalizada
  de contrato y recibos; si todavía falta prueba de autoridad/identidad requerida,
  dejar condición concreta pendiente con productor/artefacto verificable y tarea documental
  de revalidación explícita si no hay productor, no referencia a task borrada. No
  exigir suite global verde para llamar claro a un plan; registrar riesgos reales
  de validación existente, sin arreglar producto ni fingir éxito.

  Corregir contradicciones: Scion posterior no bloquea producto núcleo; navegación
  base no espera aceptación spec2viz opcional; aceptación receptora y whitelist se
  registran por delta concreto y efecto, sin obligar reader/manual a esperar Changes/modelos/Scion.
  Cada gate conserva productor, condición, evidencia y scope; si hay split añadir
  IDs acotados y revisar todos nuevos, actualizar cobertura/aristas. Fuente editable
  espera G_SOURCE real; no concederlo por decisión. Mutaciones requieren G_HUMAN_READ
  para habilitar uso en UI, no prohibir desarrollo/pruebas aisladas de API. Toda capacidad
  desconocida queda clasificada y con tarea/productor, no workaround. Conservar root/PK/WS01–44/19
  hijos ya trazados; añadir nodos solo si falta entregable real, nunca para pulido
  editorial.

  Preparar cierre.md dentro paquete con base acordada, qué existe/qué resta, secuencia
  por entregas y primera capa preparable, quién decide/ejecuta/acepta, manual/vistas/user-flows
  y evidencia, condiciones reales de inicio. Identificar paquete final terminado como
  planificación, execution_authorized=false y candidatas aún no TaskDoc. Decisiones
  humanas no sustituyen actas de uso/capability/recepción técnica. No afirmar que
  producto está disponible. Plan final debe poder leerse sin chat.

  Regenerar desde dag.yaml. Modificar helpers .py locales solo si hace falta soportar
  estados finales/recibos/ramal y comprobarlos con semántica real; no debilitar validación
  para ocultar pendiente. context_review.py status detecta inputs afectados: corregir
  fuentes primero y congelar, luego lanzar solo afectados con Pi deepseek-flash low
  NUEVO proceso por nodo/intento, no-session/no-context-files/no-skills/no-extensions/no-prompt-templates/no-tools,
  stdin=DEVNULL; recibos exactos, no reviews anteriores en input, guardar reformulación/ambigüedades/dry-run
  sin ejecutar. Supervisor/Executor compara cada output contra intención, dispone
  hallazgos con cita real/razón, corrige y re-revisa. APTO no basta. Gates/decisiones
  suministrados cambiados invalidan afectados; no marcar vigente sin input actual.
  Evidencia extra append-only en run previo permitida, resumen/receipts nuevos en
  run de esta tarea. No pedir concilio experto para salvar comprensión; supervisor
  consulta concilio final separado y Tester independiente al acabar. Executor NO commitea,
  NO cierra ni cambia Board. Handoff incluye findings/disposiciones y limitaciones.'
validation:
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- 'python desk/drawer/plans/workspace-documental/context_review.py status: all reviews
  current'
- 'Independiente: integridad/hashes/aislamiento/cobertura/dry-runs de todos los reviews
  nuevos; refs actualizadas y decisiones trazadas; ninguna autorización producto ni
  gate humano falso'
- Validación focalizada de G_CLOSEOUT por tester si se propone satisfecho; no ejecutar
  suite global larga ya fallida salvo cambio o hallazgo que lo justifique. Para helpers
  .py usar checks semánticos y pytest focalizado apropiado; registrar baseline externo.
done_when: Plan final consistente, sin referencias obsoletas conocidas ni decisiones
  de núcleo sin dueño, ramales opcionales independientes, pendientes técnicos explícitos
  con productor/evidencia, reviews baratos vigentes y tester independiente; cierre
  oficial propio y fase documental. No producto ejecutado.
pills:
- pill-001
- pill-005
- pill-007
references:
- a8601fe
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/drawer/plans/workspace-documental/README.md
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
closeout_evidence:
- commit
- document
