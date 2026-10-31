# Informe del Tester independiente — WS02 auditoría Deskops

Fecha de lectura: 2026-10-31. Solo lectura; sin bash ni escritura. Lo que proviene de `tester-facts.log` se marca «dato del Supervisor» y no cuenta como verificación propia.

## Comprobaciones obligatorias

| # | Objeto | Evidencia real leída | Resultado |
|---|---|---|---|
| 1a | No falta ningún comando de `command_registry()` | Enumerados en `deskops/cli/registry.py`: 20 base + 49 de `_operation_shared_commands` (add/edit/list/show/bind/next/advance con 9 sujetos de `ARTIFACT_SUBJECTS`, operations.py:87-97) + 44 restantes = 113. El entregable tiene 113 filas A1 (`deskops.md:30-142`). Lista y orden coinciden. | PASS |
| 1b | Los modelos del store figuran en B | `.sldb/store.yaml:1-65` declara 17 modelos; entregable con 17 filas B (`deskops.md:185-201`): Atom, Board, Crossroad, DeskFAQ, InboxNote, Materialization, Pill, ProtoAtom, Relation, RelationType, Repository, Ritual, Role, Run, RuntimeProfile, Step, Task. | PASS |
| 1c | A2 completo | `grep '^    def'` en operations.py da 24 métodos públicos sin guion bajo (excluidas 6 `@property`, operations.py:225,315,322,330,337,461); 24 filas A2. | PASS |
| 2 | Muestreo de 15 filas de A1 (efecto y efecto Git) | Ver tabla inferior. | PASS |
| 3a | Constructor escribe `.deskops.log` | `operations.py:201-223`: `_setup_logging` abre `self.root / ".deskops.log"` (`:215`) y se llama en `__init__` (`:212`); `.gitignore:5` lo ignora. | PASS |
| 3b | `validate_atoms` llama `ensure_workspace` y puede crear andamiaje | `services/atoms.py:154-155`; `ensure_workspace` en `operations.py:231-241` hace `scaffold_desk`, crea 5 carpetas y `ensure_default_namespaces`. | PASS |
| 3c | `retire` no hace commit | `services/retire.py:1-8` no importa `subprocess`; borrado vía `doc_io.DocTransaction` (`:103-107`). | PASS |
| 3d | `closeout commit` borra el archivo de la tarea | `services/closure.py:455-458` (`git rm -f`), `:465` (`unlink` si no estaba en HEAD); `:427` commit previo `Closeout-Mode: record` (`:625`). | PASS |
| 3e | 2 de 8 materializaciones no están en el índice local | `.sldb/store.yaml` declara 8; `.sldb/core/documents/MaterializationContractDoc/` contiene 6: faltan `materialization-board-portable-context` y `materialization-board-portable-references-regressions`. Además `desk/materializations/materialization-skill-drift-guard-tests.md` existe y no está declarada (9 archivos, 8 declarados). | PASS |
| 4 | 10 filas de `file-inventory.tsv` contra `.sldb/store.yaml` | Ver tabla inferior. | PASS |
| 4b | Hashes del anexo | «dato del Supervisor»: 192 filas, 0 distintos. No verificable sin bash; no cuenta como PASS propio. | NO VERIFICADO |
| 5 | Filas «comprobado» sin evidencia | Ninguna: todas las filas A1/A2/B/C/D traen columna evidencia no vacía. Hallazgos sobre `commands.log` abajo. | PASS con hallazgo |

## Muestreo A1 (15+ filas: 6 lectura, 9 mutación)

| Fila | Efecto afirmado | Evidencia leída | Git | Resultado |
|---|---|---|---|---|
| `about` | Lectura | `core.py:10-16`; `about.py:25-27` | sin git | PASS |
| `faq` | Lectura de `docs/faq.md`, no DeskFAQDoc | `faq.py:24-52` | sin git | PASS |
| `status` | Alias deprecado, delega en DoctorCLI | `registry.py:524-531`; `main.py:119-120`; `doctor.py:37` | sin git | PASS |
| `message list` | Lectura | `message.py:145-148,289-293` | sin git | PASS |
| `list atoms` | Lectura | `operations.py:102-116`; `services/atoms.py:81-100` | sin git | PASS |
| `repo whoami` | Lectura | `repo.py:169-176` | sin git | PASS |
| `doctor` | scaffold + init_local_store con `--repair` | `doctor.py:52-60,88-94,120-139`; `subprocess` solo a `sldb stores check` | sin git | PASS |
| `message send` | Escribe inbox y trackea | `message.py:96-143` (escritura `:123`, tracking `:130`) | sin git | PASS |
| `message ack` | Reescribe + rollback | `message.py:161-198` (escritura `:181`, rollback `:186-188`) | sin git | PASS |
| `promote inbox-to-drawer-task` | Crea tarea, untrack y borra nota | `services/drawer.py:92-139` (`:133-134`) | sin git | PASS |
| `drawer remove` | Borra archivo y viñetas | `services/drawer.py:141-181` | sin git | PASS |
| `retire` | Borra + desruta, sin commit | `services/retire.py:56-109` | sin git | PASS |
| `add task` | Tarea + Board + track | `operations.py:23-47`; `services/tasks.py:80-94` | sin git | PASS |
| `add ritual` | Escribe, no trackea | `operations.py:50-58`; `operations.py:1343-1346` (solo atom/pill/materialization) | sin git | PASS |
| `edit task` | Reescribe campo, id inmutable | `operations.py:60-68,271-282` | sin git | PASS |
| `bind pill` | Agrega pill a la tarea | `operations.py:70-79,284-296` | sin git | PASS |
| `advance task` | `complete` no se persiste | `services/tasks.py:172-209` | sin git | PASS |
| `atoms validate` | Lectura, puede crear andamiaje | `atoms.py:40-58`; `services/atoms.py:154-155` | sin git | PASS |
| `closeout commit` | stage, commit/amend, rm, index | `closeout.py:75-129`; `closure.py:392-396,400-402,439,447,455-458,487-489,524-525` | commit/amend; sin tag/push (`grep` solo texto en `scion.py:251`) | PASS |
| `graph build` | Escribe snapshot/runtime | `graph.py:21-51` | sin git | PASS |

## Muestreo C (10 filas TSV vs store.yaml)

| Archivo (TSV) | Modelo en TSV | Regla en `.sldb/store.yaml` | Resultado |
|---|---|---|---|
| `desk/contexts/README.md` | no modelado | no casa glob `desk/contexts/pill-*.md` (:126) | PASS |
| `desk/contexts/pill-001-task-closure-commit.md` | PillDoc | glob `desk/contexts/pill-*.md` (:125-126) | PASS |
| `desk/drawer/README.md` | no modelado | sin include para drawer | PASS |
| `desk/drawer/plans/workspace-documental/alcance.md` | no modelado | sin include para drawer | PASS |
| `desk/drawer/tasks/Board.md` | no modelado | BoardDoc solo `desk/tasks/Board.md` (:177-178) | PASS |
| `desk/inbox/20261019-112931-...md` | InboxNoteDoc | glob `desk/inbox/*.md` (:123-124) | PASS |
| `desk/lifecycle/closeout-task_completes.md` | RelationDoc | path exacto (:127-131) | PASS |
| `desk/lifecycle/type-task_activates.md` | RelationTypeDoc | path exacto (:132-137) | PASS |
| `desk/registry/repo-deskops.md` | RepositoryDoc | glob `desk/registry/*.md` (:156-157) | PASS |
| `desk/rituals/phase.md` | RitualDoc | path exacto (:161) | PASS |
| `desk/roles/deskops-tester.md` | RoleDoc | glob `desk/roles/*.md` (:169-170) | PASS |
| `desk/tasks/task-ws03-...md` | TaskDoc | glob `desk/tasks/task-*.md` (:173-174) | PASS |
| `desk/drawer/.../build_plan.cpython-313.pyc` | no comprobado (no UTF-8) | fuera de todo include | PASS (coherente con disposición) |

## Hallazgos

- `commands.log` está reconstruido y contiene líneas agrupadas y comentarios entre paréntesis (`python -c ... (volcado de ...)`), lo que incumple literalmente «un comando por línea». No invalida el contenido: los 113 comandos, los 24 métodos y los 17 modelos se re-derivaron aquí de `registry.py`, `operations.py` y `.sldb/store.yaml`.
- La frase de B «salida guardada en commands.log» es inexacta: el log guarda la línea del comando, no la salida de `sldb models list`. La fila B sigue respaldada por `.sldb/store.yaml`, no por el log.
- Conteos que dependen de salida de comando no reproducible sin bash quedan como dato del Supervisor: `wc` del TSV (193 líneas = 192 filas) y `grep -c "path=("` (80). Los totales por categoría del entregable (14+119+31+7+6+3+2+4+6=192; modelados 71) sí cuadran con el TSV leído.
- No se pudo recontar de forma independiente `.sldb/core/documents` (239), `.sldb/runtime` (3560), las 169 carpetas de `runs/subagents` ni los hashes del anexo: NO VERIFICADO (requiere bash).

RESULTADO: PASS
