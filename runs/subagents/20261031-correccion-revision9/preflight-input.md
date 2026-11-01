FILE:desk/tasks/task-corregir-revisión-9-del-plan-workspace-tras-revisión-root.md
---
id: task-corregir-revisión-9-del-plan-workspace-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-correccion-revision9/review-source.md
- runs/subagents/20261031-ajuste-canonico-ws06/handoff.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-correccion-revision9/comparison-ledger.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-revision-9-del-plan-tras-revision-root.md
closeout_evidence:
- commit
- document
---

# Corregir revisión 9 del plan workspace tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aceptó cuatro decisiones pero no aprobó la revisión 9: un contrato incondicional, una interfaz sin productor, un dry-run faltante y una atribución de revisión que no ocurrió. Fuente: runs/subagents/20261031-correccion-revision9/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Corregir esos cuatro puntos con evidencia sincera y dejar el plan con build --check, validate --check y status en verde, sin implementar nada.

## Scope

_State what is in scope and what is out of scope._

Planificación en deskops. Archivos: desk/drawer/plans/workspace-documental/dag.yaml y sus proyecciones generadas, evidencia en runs/subagents/20261031-correccion-revision9/ y disposiciones nuevas o atestaciones en runs/subagents/20261031-workspace-context-reviews/context-review/. runs/subagents/20261031-correccion-revision9/review-source.md es contrato obligatorio.

Punto 1. En la aceptación de WS12, la cláusula que mantiene a WS21 bloqueado pasa a decir G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE. No cambia P04, ni añade gate ni actor.

Punto 2. WS12 asume en su aceptación producir, para el ramal E, la política y el umbral de timeout de dispatch y reply y su clasificación observable, como sección de contrato por delta. Sin elegir duración ahora, sin bloquear el cierre del contrato núcleo y sin permisos ni red nuevos. WS34.1 y WS34.2 declaran que solo avanzan con esa política aplicable y probada en el contrato de su delta. No se modifican los gates.

Punto 3. WS19.1 recibe un proceso barato nuevo que reformule y describa cambios futuros concretos de campos, consumo de precondición, bloqueo de campos protegidos, buffer y conflicto, y validación, sin ejecutar. El intento anterior se conserva sin crédito. No se inyecta su salida ni se rescata con experto. Si solo cambia la instrucción, se registran bytes y argv y no se usa el runner cuando devolvería answered.

Punto 4. Las disposiciones existentes se conservan: dicen revisado por el coordinador sin que esa revisión ocurriera nodo por nodo. Se escribe runs/subagents/20261031-correccion-revision9/comparison-ledger.md con supersesión fechada y, por cada nodo final: rol y actor real, sha de input, output y disposición, alcance de la comparación, resultado y fecha. El coordinador compara de verdad output y disposición finales de todos los nodos y asume la aceptación; el ledger dice exactamente qué leyó. Los defectos hallados se corrigen, no se waivan.

Además: result-summary.md de la consolidación afirma que WS42 no guarda payload por campos, y eso es falso; se corrige con nota fechada. WS42 sale de la justificación por tener guardas y contrato propios y WS19 transitivo, sin forzar un gate universal. promotion-notes.md se actualiza: no da por futuro lo que no tiene productor.

Roles: el Supervisor edita contratos, que la revisión root aceptó; corre revisiones, compara, firma el ledger, valida y cierra. Un agente puede preparar borradores, y el ledger lo dice. Un Tester independiente de solo lectura verifica los cuatro puntos y el cambio protector de G_SOURCE.

Fuera de alcance: código, validadores salvo fallo real con tarea específica, decisiones P01-P09, auditorías, reconciliacion.md salvo que un punto lo exija, WS07, WS08-12, UI, Scion, push.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Editar WS12, WS34.1 y WS34.2. 2. Regenerar y congelar. 3. Correr revisiones de los afectados según hashes. 4. Revisión nueva de WS19.1. 5. Comparar todos los nodos finales y corregir lo que aparezca. 6. Registrar context_review y ledger. 7. Tester. 8. Closeout y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- test -s runs/subagents/20261031-correccion-revision9/comparison-ledger.md
- git diff --name-only 5f05281c..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/decisiones.md desk/drawer/plans/workspace-documental/auditoria/ desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py desk/drawer/plans/workspace-documental/context_review.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-revision9/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

WS12 condiciona G_SOURCE a la variante editable; WS12 produce la política de timeout y WS34.1 y WS34.2 dependen de ella sin bloquear el núcleo; WS19.1 tiene dry-run real; cada nodo final tiene comparación verdadera en el ledger; build --check, validate --check y status en verde; y un Tester independiente da PASS.

FILE:runs/subagents/20261031-correccion-revision9/review-source.md
# Revisión root de la revisión 9, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31.

Verificado por root: build/validate/status PASS; 73 inputs reconstruidos byte a byte, contratos/hashes/ordered_sources/outputs/recibos/DEVNULL/flags, 73 PID únicos y versión 0.67.3. Ningún cambio en los tres validadores, código, auditorías ni decisiones. Esto NO basta para aceptar comprensión si una disposición waivera un dry-run faltante.

Cuatro decisiones del handoff ACEPTADAS: (1) WS21 consume precondición payload porque ambas variantes editan campos; (2) la autorización local Deskops no inventa receptor ni firma nueva; (3) criterios origen/sin tarea activa/colisiones para falta de conducta workflow son adecuados; (4) correcciones de brief/contrato por Supervisor están autorizadas por TaskDoc punto 5. No hace falta otro Executor para repetir esa redacción solo por rol. WS42 sí modifica payload, pero tiene guardas/contrato específico y WS19 transitivo: no justificar exclusión diciendo que no escribe payload, ni forzar gate universal por reflejo. WS45 tarea propia y WS39 enganche son detalles válidos para promoción, no bloqueantes actuales.

NO APROBADO todavía:

1) WS12 acceptance (dag≈768-771) conserva 'manteniendo consumidor WS21 bloqueado por G_SOURCE y G_PAYLOAD_PRECONDITION' sin condicionar. WS21/variante read_only excluyen G_SOURCE. Sustituir cláusula por 'G_PAYLOAD_PRECONDITION y, SOLO en variante editable, G_SOURCE'. No cambia P04 actual editable ni añade gate/actor.

2) Interfaz de timeout faltante. WS34.1 output identifica falta de umbral; disposition reconoce que WS12 no lo lista pero lo descarta como futuro. WS34.2 output/disposition afirma que WS12 produce umbral sin que exista ese compromiso. Un consumidor no crea la obligación de su productor. Comprometer explícitamente política/umbral dispatch/reply y clasificación observable en contrato producido por WS12 para ramal E (o reasignar productor de forma explícita y coherente). NO elegir duración ahora, NO bloquear contrato núcleo por Scion posterior, NO introducir permisos/red nuevos. Asegurar que consumidor solo puede avanzar con contrato aplicable probado; no declarar 'futuro asignado' si productor no lo asume. promotion-notes por sí solo no cierra interfaz.

3) WS19.1 review final NO cumple dry-run. output en c342b4d…/attempt-1 dice 'Cambios previstos: ninguno; solo revisión'; disposition: 'no describe el delta (observación menor)'. Es requisito central de ritual-context-review. Mantener intento histórico sin crédito actual y lanzar nuevo proceso barato fresco que reformule y DESCRIBA cambios futuros concretos de campos, consumo precondición, bloqueo de campos protegidos, buffer/conflicto y validación, SIN ejecutar. No rescatar con experto ni inyectar output previo. La pregunta/brief debe dejar claro que se pide ejecución hipotética del nodo y no acciones del reviewer. Si solo cambia instrucción por intento, registrar bytes/argv exactos y no usar el runner si devuelve automáticamente answered del mismo input como si fuera nueva revisión. Vecinos solo se invalidan si cambia contrato suministrado.

4) Provenancia de comparación: los disposition.md inspeccionados dicen 'Borrador ... y revisado por el coordinador', mientras handoff reconoce 'no cada disposición'. No atribuir revisión individual que no ocurrió. Completar comparación real de TODOS los outputs+disposiciones finales por nodo y dejar ledger firmado por rol/actor real/input/output/disposition/alcance/fecha, o corregir honestamente la atribución y quién hizo cada comparación. Para cerrar el checkpoint se solicita comparación final efectiva de todos los nodos, con coordinador asumiendo aceptación; no basta leer lista de ambigüedades. Delegar redacción/comparación preparatoria está permitido; cada afirmación de revisión debe ser verdadera. Preservar original y dejar supersesión/atestación posterior con fecha; no retrofechar ni borrar fallo anterior.

Root escaneó WS01/03/15/25.1/26/34 por 'cambios ninguno': no son el mismo defecto (WS01 verifica cobertura existente, WS03 produce auditoría, WS25.1 describe futuro, los otros son agregados). No repetirlos por esa palabra automáticamente; comparar resultado de verdad.

Antes del último lote, congelar TODAS las correcciones fuente, ejecutar revisiones baratas de todos afectados/nuevos según hashes, comparar y registrar evidencia final sincera. No limitar a 73 ni reenviar todos por defecto: afectados reales, y todos finales sí deben tener comparación. Regenerar y mantener validadores intactos salvo fallo real con tarea específica, status 0 stale, tester independiente sobre estos 4 puntos y cambio protector de G_SOURCE. Tester puede ser read-only. No código producto, no WS07/08-12 activos ni UI. Traer checkpoint correctivo y riesgos residuales. Registrar esta revisión como fuente y proceder dentro de este alcance.

