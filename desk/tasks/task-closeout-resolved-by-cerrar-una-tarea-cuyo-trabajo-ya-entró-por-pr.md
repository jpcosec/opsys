---
sldb:
  by: agent
  at: '2026-11-09T20:37:01Z'
  authority: generated
  via: save_document_payload
id: task-closeout-resolved-by-cerrar-una-tarea-cuyo-trabajo-ya-entró-por-pr
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_closeout_resolved_by.py
- pytest tests/test_closeout.py
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
- cdce4ca2d117adf0e6fa609eea77e6e9c145602c
- desk/atoms/atom-closeout-resolved-by-cierra-una-tarea-cuyo-trabajo-ya-entró-por-pr.md
depends_on: []
pills: []
files:
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- deskops/cli/registry.py
- tests/test_closeout_resolved_by.py
- tests/fixtures/golden/help/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# closeout resolved-by: cerrar una tarea cuyo trabajo ya entró por PR

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de deskops propuesto por AntonIA (nota de inbox desk/inbox/inbox-note-closeout-resolved-by-cerrar-una-tarea-cuyo-trabajo-ya-entró-por-pr.md, bce196e1), encargado por el coordinador de proyecto el 2026-11-09. Una tarea cuyo trabajo ya entró por PR antes del closeout no se puede cerrar con honestidad: closeout commit pide un átomo por archivo del commit, supersede es para un tema sin trabajo hecho y retire exige que la tarea ya esté resuelta.

## Goal

_Describe the concrete result this task must produce._

deskops closeout resolved-by --task <id> --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] --reason <texto> cierra una tarea cuyo trabajo ya está en la historia. Exige al menos un --ref que sea commit ancestro de HEAD y al menos un --test que el gate de tests acepte, pero no exige un átomo por archivo. Hace un solo commit de cierre con Closeout-Mode: resolved-by, como supersede.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/closure.py (solo un método nuevo close_resolved_by, junto a close_superseded, que reusa _close, _ref_resolves y los productores de hechos existentes de CloseoutGatesService), deskops/cli/commands/closeout.py (el despacho del subcomando), deskops/cli/registry.py (el comando closeout resolved-by), los goldens de ayuda de closeout (deskops_closeout.txt y el nuevo de resolved-by), tests/test_closeout_resolved_by.py (nuevo), docs/operator-manual.md (la sección de closeout) y CHANGELOG.md. Fuera: verify_task_closeout, closeout_gates.py, operations.py, services/tasks.py y las reglas de cierre, porque CC33 reescribe el closeout; también close_superseded, close_retired y close_with_run, que no cambian.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (origin/main 1cc19364): deskops/services/closure.py (1103 líneas).
- close_superseded (:121-200) es el modelo a seguir: valida reason y refs (_ref_resolves), lee la tarea, escribe status/history con doc_access.write_doc y llama a _close(task_id, route=..., trailers=[Task-Id, Closeout-Mode, Closeout-Reason, Closeout-Ref...], run_gates=False, index_entry={... "mode": ...}). Si falla, restaura el archivo.
- close_retired (:202) exige status en {resolved, closed, done, complete} (:246).
- CLI: deskops/cli/commands/closeout.py (129 líneas: _supersede :52 y despacho :27-37). registry.py :1567-1595 tiene closeout supersede con su epilog.
- Hechos: deskops/services/closeout_gates.py, CloseoutGatesService. reference_points_to_commit es un id hex en minúscula, ancestro de HEAD. reference_points_to_test(reference, files=...) acepta un .py existente bajo cualquier tests/ o declarado en files (tras el seguimiento closeout-tests-paths). reference_points_to_url acepta http(s).

DECISIONES (coordinador del plan, 2026-11-09; REVISABLES):
r1 (forma): deskops closeout resolved-by --root <r> --task <id> --reason "<texto>" --ref <ref> [--ref ...] --test <ref de test> [--test ...] [--paths ...] [--message ...]. --ref y --test son repetibles. --paths y --message con la misma semántica que en supersede.
r2 (evidencia): al menos un --ref tiene que pasar reference_points_to_commit, es decir, ser un commit ancestro de HEAD. Los demás --ref pueden ser commits ancestros o URLs http(s) (el PR), según reference_points_to_url. Cualquier --ref que no sea ninguna de las dos cosas se rechaza. Al menos un --test tiene que pasar reference_points_to_test con files = los files de la tarea. Cada rechazo es un error claro con exit 1, y no se escribe nada. No se exige átomo, materialization ni run.
r3 (estado): status «resolved» (el que close_retired acepta) e history + «resolved-by». Commit de cierre con los trailers Task-Id, Closeout-Mode: resolved-by, Closeout-Reason, un Closeout-Ref por ref y un Closeout-Test por test. index_entry con mode «resolved-by». run_gates=False, porque la evidencia es la de r2. La tarea sale del Board, como en supersede.
r4 (mínimo, por CC33): no se toca verify_task_closeout, ni closeout_gates.py, ni close_superseded, close_retired o close_with_run. El método nuevo llama a los productores de hechos tal como están. CC33 los convierte en recibos y, al hacerlo, decide si resolved-by escribe recibos evidence. Va como nota en el informe.
r5 (goldens de ayuda): cambia deskops_closeout.txt (lista el subcomando) y se agrega el golden del subcomando nuevo (deskops_closeout_resolved-by.txt o el nombre que use el arnés), generados con --update-golden solo para esos dos y revisados en el diff. Ningún otro golden cambia.
r6 (tests): tests/test_closeout_resolved_by.py nuevo, sobre un desk temporal con git. Cubre:
- cierre exitoso con commit ancestro y test existente: status resolved, history, trailers, Board y un solo commit;
- sin --ref commit: falla;
- --ref que no es commit ni URL: falla;
- sin --test o con un test inexistente: falla;
- URL de PR como --ref adicional: se acepta y queda en un trailer;
- sin --reason: falla;
- en cada falla, nada escrito (sha256 de desk/ y git status iguales).
Además, de a uno: tests/test_closeout.py (donde vive supersede), tests/test_command_registry.py, test_cli_help_examples y test_output_goldens; test_cli desde una copia en /dev/shm. El golden nuevo sigue el patrón de tests/fixtures/golden/help/deskops_closeout_supersede.txt.

PRECISIONES DEL PREFLIGHT (review-...-preflight-2, 2026-11-09; el intento 1 fue un timeout técnico del modelo):
b1 (nombre del golden): el arnés une el path del comando con «_» y conserva los guiones (deskops_promote_inbox-to-drawer-task.txt, deskops_add_faq-doc.txt). El nuevo es tests/fixtures/golden/help/deskops_closeout_resolved-by.txt.
b2 (--paths y --message): los de close_superseded (closure.py:121-200). --paths son las rutas extra que entran al commit de cierre; se pasan a _close con explicit_paths=True. --message reemplaza el asunto del commit; si falta, va self._default_subject(task_id). resolved-by los pasa igual a _close.
b3 (HEAD de qué repo): el del --root (CloseoutGatesService(root).reference_points_to_commit corre git en root), igual que supersede con _ref_resolves.
b4 (test_cli en /dev/shm): git -C ~/proyectos/SLDB_1/deskops-wt-rb worktree add --detach /dev/shm/deskops-rb HEAD; pytest ahí con PYTHONPATH=/dev/shm/deskops-rb; al terminar, git -C ~/proyectos/SLDB_1/deskops-wt-rb worktree remove --force /dev/shm/deskops-rb.

## Validation

_List the checks required before this task can close._

- tests/test_closeout_resolved_by.py nuevo (r6)
- Solo cambian deskops_closeout.txt y el golden nuevo del subcomando
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_closeout, test_command_registry, test_cli_help_examples, test_output_goldens; test_cli desde copia en /dev/shm
- verify_task_closeout y closeout_gates.py sin tocar (git diff)
- CHANGELOG y manual
- Resultado (coordinador de proyecto, squash cdce4ca2 sobre CC35b b2673b36): de a uno desde /dev/shm, closeout_resolved_by 19, closeout 49, command_registry 3 (con la línea ('review','record') que faltaba desde 293c4dc7), cli_help_examples 11, cli 101, output_goldens 7 (sin --update-golden).

## Done When

_Name the observable condition that makes the task complete._

deskops closeout resolved-by cierra una tarea con un commit ancestro y un test aceptado como evidencia, sin átomo por archivo, con un solo commit de cierre (Closeout-Mode: resolved-by) y status resolved. Las fallas no escriben nada. tests/test_closeout_resolved_by.py verde. Solo cambian el golden de ayuda de closeout y el nuevo del subcomando. test_cli, test_output_goldens y test_cli_help_examples verdes. Manual y CHANGELOG al día. verify_task_closeout y closeout_gates.py sin tocar.
