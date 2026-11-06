FILE:desk/tasks/task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb.md
---
id: task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
pills: []
files:
- deskops/workspace.py
- deskops/data/templates/
- deskops/data/desk_declaration.yaml
- deskops/doc_access.py
- deskops/lifecycle.py
- deskops/cli/commands/core.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/doctor.py
- deskops/bootstrap.py
- pyproject.toml
- tests/test_scaffold_golden.py
- tests/fixtures/golden/scaffold/
- tests/test_desk_sync.py
- tests/test_packaging.py
- tests/
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC36: Plantillas del desk (board, rituales, drawer, faq) como datos escritos por el scaffold de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC36 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 2 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PF1, árbol T3.6. Depende de: CC30, integrado en main (93cc1943). Gate requerido: G_GD26 (scaffold_store con semillas declaradas), satisfied en 1e7d6233. DP3: las plantillas de fábrica son semillas del paquete deskops pasadas en proceso a sldb.api.scaffold_store.

## Goal

_Describe the concrete result this task must produce._

Las plantillas del desk (config.json, Board, pills, rituales phase/execution/testing/closeout, drawer/README.md, atoms/tag-namespaces.yaml y el perfil runtime-pi-deepseek-flash) pasan a archivos de deskops/data/templates/ y a una declaración deskops/data/desk_declaration.yaml (folders y seeds if_missing) que deskops pasa a sldb.api.scaffold_store. desk update usa includes declarados en lugar de adivinar modelos por ruta. Se borran scaffold_desk, _write_if_missing, los *_template y guess_model_for_path. El resultado de init y de desk update es idéntico al golden capturado antes del cambio.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/workspace.py, deskops/data/templates/ (nuevo), deskops/data/desk_declaration.yaml (nuevo), deskops/doc_access.py (ensure_workspace), deskops/lifecycle.py (default_ritual_text), deskops/cli/commands/core.py, desk.py y doctor.py, deskops/bootstrap.py, pyproject.toml (solo package-data, c6), los tests y CHANGELOG.md. Fuera: subir la versión de sldb o el pin (c1); semillas managed de ciclo de vida, reglas y vistas (CC31/CC32/CC34); inspect_desk, migrate_desk y la clasificación absent/empty/legacy/current; escrituras en sldb; formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 2, CC36). SCOPE: Primer paso: golden del scaffold (deskops init en un directorio temporal: lista de rutas y sha256 de cada archivo, y desk update --apply sobre un desk viejo de prueba). Las plantillas que hoy son strings de workspace.py (config.json :236, Board :292 vía BoardDoc, contexts/pills.md :322, rituales phase/execution/testing/closeout :340-398, drawer/README.md :412, atoms/tag-namespaces.yaml :419) pasan a archivos en deskops/data/templates/ y una declaración deskops/data/desk_declaration.yaml (folders y seeds, modo if_missing; las de ciclo de vida, reglas y vistas que agreguen CC31/CC32/CC34 con modo managed) que deskops pasa a sldb.api.scaffold_store(declaration=..., apply) (GD26, DP3); las carpetas extra de ensure_workspace (operations.py:231-241) entran a folders. default_ritual_text (workspace.py:401, usado por lifecycle.py:271) lee la plantilla. desk update deja de adivinar modelos por ruta (cli/commands/desk.py:100 guess_model_for_path) y usa includes declarados {model, glob} (apply_includes de sldb). La FAQ: docs/faq.md sigue siendo la ruta por defecto y deskops/data/faq.md el respaldo; init no la escribe (como hoy). Se borran scaffold_desk, _write_if_missing y los *_template de workspace.py; inspect_desk/migrate_desk (clasificación absent/empty/legacy/current) se quedan como código del caso.

ACCEPTANCE: deskops init en un directorio temporal produce las mismas rutas y los mismos sha256 que el golden; desk update --apply sobre el desk viejo de prueba produce el mismo reporte (created/preserved) y el mismo árbol; una segunda corrida no cambia nada; grep de _write_if_missing, scaffold_desk, guess_model_for_path y "_template(" en deskops/ vacío; un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos; goldens de ayuda de init y desk idénticos; líneas de workspace.py antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/workspace.py, deskops/data/templates/, deskops/data/desk_declaration.yaml, deskops/operations.py (ensure_workspace), deskops/lifecycle.py (default_ritual_text), deskops/cli/commands/core.py, deskops/cli/commands/desk.py, deskops/bootstrap.py, tests/, CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06, coordinador del plan):
c1 (gate y pin): G_GD26 está satisfied en el dag (1e7d6233). pyproject.toml sigue pidiendo structuredLanguageDB>=0.1.13: es la versión actual de sldb, que no subió con GO/GD, y el venv la usa editable. El pin efectivo de este nodo es el main de sldb >= 96d7b823 (squash de GD26, closeout 713978e5). Este nodo NO sube la versión de sldb ni toca la dependencia en pyproject.toml; si hiciera falta, es otra decisión y se avisa al coordinador.
c2 (rutas vigentes tras CC30): las líneas del SCOPE son de antes de CC30. Hoy, en main: deskops/workspace.py (885 líneas) tiene scaffold_desk :170, _write_if_missing :262, _write_or_patch_config :269 y las plantillas _config_template :247, _board_template :303, _pills_template :333, _phase/_execution/_testing/_closeout_template :351-410, default_ritual_text :412, _drawer_template :423, _atom_tag_namespaces_template :430 y _runtime_pi_deepseek_flash_template :463. Esta última es de GC03 y no la nombra el SCOPE: entra igual, como semilla if_missing de desk/runtimes/runtime-pi-deepseek-flash.md. ensure_workspace vive en deskops/doc_access.py:146 (no en operations.py) y crea atoms, materializations, steps, registry y faq. scaffold_desk lo importan doc_access.py:51, cli/commands/core.py:8 y cli/commands/doctor.py:14. guess_model_for_path está en cli/commands/desk.py:104 (lo usa :473 y lo prueba tests/test_desk_sync.py:226-230). default_ritual_text lo usa lifecycle.py:285-295.
c3 (golden primero): el primer commit de la rama captura el golden con el código de main, antes de cambiar nada, en tests/fixtures/golden/scaffold/: (a) init.json con la lista ordenada de rutas y el sha256 de cada archivo que escribe «deskops init» en un directorio temporal con un nombre de desk fijo; (b) update.json con el reporte y el árbol (rutas y sha256) de «deskops desk update --apply» sobre un desk viejo de prueba. Para (b) se reusa un fixture existente de desk viejo (tests/fixtures/golden_desk o el que usan los tests de migrate_desk/desk_sync; el worker elige uno y lo nombra en el informe). Un test, tests/test_scaffold_golden.py, compara contra esos goldens. Pasa en el primer commit y sigue pasando sin cambios después.
c4 (plantillas con el nombre del desk): las plantillas usan el nombre del desk (project_identity en config.json; título y propósito del Board; textos de pills, rituales y drawer). Las semillas text/file de sldb son estáticas, así que deskops arma la StoreDeclaration en proceso: lee deskops/data/desk_declaration.yaml y los archivos de deskops/data/templates/, sustituye el nombre del desk y pasa las semillas ya rendidas a sldb.api.scaffold_store(declaration=..., apply=...) (DP3, «declaradas y pasadas en proceso»). El Board va como semilla document {model: BoardDoc, name, payload}, renderizada por el modelo como hoy. La sustitución es un str.format o un string.Template sobre un solo placeholder del nombre; no es un evaluador de reglas. config.json conserva su forma JSON exacta (golden).
c5 (qué se borra y qué queda): se borran scaffold_desk, _write_if_missing y todos los *_template de workspace.py, y guess_model_for_path (desk update pasa a includes declarados {model, glob} con sldb.api.apply_includes). Se quedan como código del caso inspect_desk, migrate_desk, classify_desk, ensure_target_directory y _write_or_patch_config, que parchea un config.json existente y es migración, no plantilla (si el worker ve que puede ser una semilla, lo anota y no lo cambia). default_ritual_text lee la plantilla del ritual del paquete con el nombre sustituido. tests/test_desk_sync.py:226-230 se adapta a los includes declarados.
c6 (empaquetado): [tool.setuptools.package-data] en pyproject.toml hoy es deskops = ["spec/**/*.yaml", "data/faq.md"]. Este nodo agrega "data/templates/**/*" y "data/desk_declaration.yaml". Es el único cambio permitido en pyproject.toml. tests/test_packaging.py comprueba que las plantillas viajan en el paquete.
c7 (desks reales): «un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos» se prueba sobre una copia del desk de deskops en un directorio temporal bajo /dev/shm, borrada al terminar. Nunca sobre un desk real.
c8 (goldens de ayuda): help de init y de desk idénticos (tests/test_output_goldens.py y tests/test_cli_help_examples.py, sin --update-golden).

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-06):
e1 (desk viejo de c3): es tests/fixtures/golden_desk. Se copia a un directorio temporal bajo /dev/shm y desk update --apply corre sobre la copia; el fixture no se modifica nunca.
e2 (carpetas): se edita deskops/doc_access.py:ensure_workspace (c2 manda sobre «operations.py:231-241» del SCOPE, que es de antes de CC30). Sus carpetas (atoms, materializations, steps, registry, faq bajo desk/) pasan a «folders» de la declaración, y ensure_workspace llama al scaffold declarado.
e3 (placeholder): las plantillas usan el texto literal {desk_name} y deskops lo sustituye con str.replace('{desk_name}', name), no con str.format: las plantillas JSON y YAML tienen llaves propias. No hay otro placeholder.
e4 (includes): van en deskops/data/desk_declaration.yaml, clave «include», con el esquema de sldb StoreDeclaration.include (sldb/src/sldb/api/stores/store_declaration.py:33): una entrada {model, glob} por cada caso que hoy resuelve guess_model_for_path (cli/commands/desk.py:104-...). deskops llama a sldb.api.apply_includes(store_path, root, declaration). Si un caso de guess_model_for_path no se expresa con {model, glob}, se anota como hipótesis y se usa {model, paths}; no se escribe lógica de adivinación nueva.
e5 (FAQ): no es semilla. deskops/data/faq.md se queda donde está, como respaldo, y init no escribe la FAQ, como hoy. «faq» en el título solo dice que su ruta no cambia.

## Validation

_List the checks required before this task can close._

- Golden del scaffold capturado en el primer commit con el código de main (c3): tests/fixtures/golden/scaffold/init.json y update.json, y tests/test_scaffold_golden.py verde antes y después
- grep -rn '_write_if_missing\|scaffold_desk\|guess_model_for_path\|_template(' deskops/ vacío
- segunda corrida de desk update --apply sin cambios (test)
- desk update en dry-run sobre una copia del desk de deskops bajo /dev/shm sin cambios nuevos (c7)
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_scaffold_golden, test_desk_sync, test_packaging, test_lifecycle_graph, test_doctor_*, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- wc -l deskops/workspace.py antes (885) y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

deskops init en un directorio temporal produce las mismas rutas y los mismos sha256 que el golden; desk update --apply sobre el desk viejo de prueba produce el mismo reporte (created/preserved) y el mismo árbol; una segunda corrida no cambia nada; grep de _write_if_missing, scaffold_desk, guess_model_for_path y "_template(" en deskops/ vacío; un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos; goldens de ayuda de init y desk idénticos; líneas de workspace.py antes y después; CHANGELOG.

FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

FILE:deskops/workspace.py
from __future__ import annotations

from dataclasses import dataclass
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Literal

import yaml

from deskops.constants import CURRENT_DESK_FORMAT

DeskClassification = Literal["absent", "empty", "legacy", "current"]

_MODELED_DESK_TOP_LEVEL_DIRS = {
    "tasks",
    "contexts",
    "rituals",
    "atoms",
    "roles",
    "registry",
    "steps",
    "faq",
}


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths)


@dataclass
class DeskInspection:
    classification: DeskClassification
    surface_docs: list[Path]
    missing_surfaces: list[str]
    malformed_surfaces: list[str]
    tracked_surface_docs: set[Path]
    invalid_surface_docs: list[str]
    store_check_message: str | None = None


@dataclass
class DeskMigrationResult:
    adopted: list[str]
    preserved: list[str]
    still_manual: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.adopted)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def classify_desk(root: Path) -> DeskClassification:
    return inspect_desk(root).classification


def inspect_desk(root: Path) -> DeskInspection:
    desk_dir = root / "desk"
    if not desk_dir.exists():
        return DeskInspection(
            classification="absent",
            surface_docs=[],
            missing_surfaces=["desk/"],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    surface_docs = _surface_docs(desk_dir)
    if not surface_docs:
        return DeskInspection(
            classification="empty",
            surface_docs=[],
            missing_surfaces=[],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    missing_surfaces: list[str] = []
    malformed_surfaces: list[str] = []

    config_path = desk_dir / "config.json"
    if not config_path.exists():
        missing_surfaces.append("desk/config.json")
        return DeskInspection(
            classification="legacy",
            surface_docs=surface_docs,
            missing_surfaces=missing_surfaces,
            malformed_surfaces=malformed_surfaces,
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    desk_format = _read_declared_desk_format(config_path)
    if desk_format != CURRENT_DESK_FORMAT:
        malformed_surfaces.append(
            f"desk/config.json (versions.desk_format={desk_format!r}; expected {CURRENT_DESK_FORMAT!r})"
        )

    tracked_surface_docs, invalid_surface_docs, store_check_message = _inspect_surface_store_health(root, surface_docs)
    malformed_surfaces.extend(invalid_surface_docs)
    if store_check_message:
        malformed_surfaces.append(store_check_message)

    classification: DeskClassification = "legacy" if malformed_surfaces else "current"
    return DeskInspection(
        classification=classification,
        surface_docs=surface_docs,
        missing_surfaces=missing_surfaces,
        malformed_surfaces=malformed_surfaces,
        tracked_surface_docs=tracked_surface_docs,
        invalid_surface_docs=invalid_surface_docs,
        store_check_message=store_check_message,
    )


def migrate_desk(root: Path) -> DeskMigrationResult:
    before = inspect_desk(root)
    adopted: list[str] = []
    preserved = [str(path.relative_to(root)) for path in before.surface_docs]
    still_manual: list[str] = []

    desk_dir = root / "desk"
    result = scaffold_desk(root)
    adopted.extend(str(path.relative_to(root)) for path in result.created_paths)

    config_status = _write_or_patch_config(root)
    if config_status == "created" and "desk/config.json" not in adopted:
        adopted.append("desk/config.json")
    elif config_status == "updated":
        adopted.append("desk/config.json (patched desk_format)")

    after = inspect_desk(root)
    tracked_after = after.tracked_surface_docs if after.classification in {"legacy", "current"} else set()
    for path in after.surface_docs:
        rel = str(path.relative_to(root))
        if path not in tracked_after:
            still_manual.append(f"{rel} (preserved; manual model conversion or sldb docs track required)")

    for invalid in after.invalid_surface_docs:
        still_manual.append(f"{invalid} (manual SLDB/model repair required)")

    if after.store_check_message:
        still_manual.append(f"{after.store_check_message} (manual SLDB health follow-up)")

    return DeskMigrationResult(
        adopted=_dedupe(adopted),
        preserved=_dedupe(preserved),
        still_manual=_dedupe(still_manual),
    )


def scaffold_desk(target_path: Path) -> DeskScaffoldResult:
    desk_dir = target_path / "desk"
    created_paths: list[Path] = []
    subdirs = [
        "tasks",
        "contexts",
        "rituals",
        "atoms",
        "roles",
        "inbox",
        "reviews",
        "drawer",
        "runtimes",
    ]

    desk_dir.mkdir(parents=True, exist_ok=True)
    for sub in subdirs:
        subdir = desk_dir / sub
        if not subdir.exists():
            subdir.mkdir(parents=True, exist_ok=True)
            created_paths.append(subdir)

    _write_if_missing(
        desk_dir / "config.json",
        _config_template(target_path.name),
        created_paths,
    )

    _write_if_missing(
        desk_dir / "tasks" / "Board.md",
        _board_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "contexts" / "pills.md",
        _pills_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "phase.md",
        _phase_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "execution.md",
        _execution_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "testing.md",
        _testing_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "closeout.md",
        _closeout_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "drawer" / "README.md",
        _drawer_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "atoms" / "tag-namespaces.yaml",
        _atom_tag_namespaces_template(),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md",
        _runtime_pi_deepseek_flash_template(),
        created_paths,
    )

    return DeskScaffoldResult(created_paths=created_paths)


def _config_template(name: str) -> str:
    data = {
        "project_identity": name,
        "versions": {
            "desk_format": CURRENT_DESK_FORMAT,
            "model_version": "1.0.0",
        },
        "sandbox": {
            "enabled": False,
            "sandbox_root": ".tmp/deskops-sandbox",
        },
    }
    return json.dumps(data, indent=2) + "\n"


def _write_if_missing(path: Path, content: str, created_paths: list[Path]) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")
    created_paths.append(path)


def _write_or_patch_config(root: Path) -> str | None:
    desk_dir = root / "desk"
    config_path = desk_dir / "config.json"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(_config_template(root.name), encoding="utf-8")
        return "created"

    data: dict[str, object]
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    data = dict(payload)
    versions = data.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    versions = dict(versions)
    changed = versions.get("desk_format") != CURRENT_DESK_FORMAT
    versions["desk_format"] = CURRENT_DESK_FORMAT
    data["versions"] = versions
    data.setdefault("project_identity", root.name)

    rendered = json.dumps(data, indent=2) + "\n"
    if config_path.read_text(encoding="utf-8") != rendered:
        config_path.write_text(rendered, encoding="utf-8")
        return "updated"
    return None


def _board_template(name: str) -> str:
    """The scaffolded board, rendered by the model so it stays readable.

    A hand-written board that lacks the model's fixed text extracts as empty for
    purpose and notes, so the first update through the model would blank them.
    """
    from deskops.models import BoardDoc
    from sldb.runtime.validation import render_model_markdown

    return render_model_markdown(
        BoardDoc,
        {
            "id": "board-001",
            "title": f"{name} Board",
            "scope": "desk",
            "purpose": f"Route the active execution set for {name}.",
            "tasks": [],
            "pills": ["desk/contexts/pills.md"],
            "rituals": [
                "desk/rituals/phase.md",
                "desk/rituals/execution.md",
                "desk/rituals/testing.md",
                "desk/rituals/closeout.md",
            ],
            "notes": "Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.",
            "tags": ["workspace:desk"],
        },
    ) + "\n"


def _pills_template(name: str) -> str:
    return f"""---
id: contexts-pills
tags:
- workspace:desk
---

# Pills

Pills are reusable context documents for the {name} desk routine.

## Notes

- Keep active task-to-pill binding in task docs.
- Add temporary context here only when it affects execution safety or scope.
"""


def _phase_template(name: str) -> str:
    return f"""---
id: ritual-phase
steps: []
tags:
- workspace:desk
---

# Phase ritual for dependency-layer execution

Run one horizontal layer of {name} tasks whose prerequisites are satisfied and whose
planned changes do not overlap, then close the layer with integration validation,
pill reconciliation, and next-phase preparation.

Each task in the phase still closes with its own validation and its own commit;
the phase adds the pass that only makes sense once those tasks are integrated.
"""


def _execution_template(name: str) -> str:
    return f"""---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for {name}.
"""


def _testing_template(name: str) -> str:
    return f"""---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when {name} changes shared behavior.
"""


def _closeout_template(name: str) -> str:
    return f"""---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a {name} task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.
"""


def default_ritual_text(ritual_id: str, name: str) -> str:
    """The ritual `deskops init` writes for one lifecycle state."""
    templates = {
        "ritual-phase": _phase_template,
        "ritual-execution": _execution_template,
        "ritual-testing": _testing_template,
        "ritual-closeout": _closeout_template,
    }
    return templates[ritual_id](name)


def _drawer_template(name: str) -> str:
    return f"""# Drawer

Deferred desk work for {name} lives here until it is promoted into active execution.
"""


def _atom_tag_namespaces_template() -> str:
    return """namespaces:
  domain:
    do_not_use_when: A more specific system, topic, layer, or pattern tag applies.
    examples:
    - domain:knowledge-management
    - domain:task-execution
    meaning: Problem domain or durable area of concern.
    use_when: The atom belongs to a reusable problem domain.
  layer:
    do_not_use_when: The tag names only a broad topic or system.
    examples:
    - layer:document-model
    - layer:runtime
    - layer:cli
    meaning: Architectural layer where the atom applies.
    use_when: The atom is scoped to a layer of the system.
  system:
    do_not_use_when: The tag is only a general topic.
    examples:
    - system:deskops
    meaning: System, project, or tool the atom belongs to.
    use_when: The atom is about a specific system.
  topic:
    do_not_use_when: The atom describes a reusable implementation shape.
    examples:
    - topic:atoms
    - topic:composition
    meaning: Subject area discussed by the atom.
    use_when: The atom is about a conceptual topic.
"""


def _runtime_pi_deepseek_flash_template() -> str:
    """The default ``deskops review`` engine profile, seeded idempotently by init/update."""
    from deskops.models import RuntimeProfileDoc
    from deskops.services.review import SYSTEM
    from sldb.runtime.validation import render_model_markdown

    payload = {
        "id": "runtime-pi-deepseek-flash",
        "title": "Pi deepseek-flash isolated reviewer",
        "status": "active",
        "kind": "pi",
        "binary": "pi",
        "model_flag": "--model",
        "fallback_models_flag": "",
        "fallback_models_join": "comma",
        "tools_flag": "",
        "tools_join": "comma",
        "system_prompt_flag": "--system-prompt",
        "system_prompt_delivery": "inline",
        "system_prompt": SYSTEM,
        "session_flag": "",
        "extra_args": [
            "--provider",
            "deepseek",
            "--model",
            "deepseek-flash",
            "--thinking",
            "low",
            "--offline",
            "--no-session",
            "--no-context-files",
            "--no-skills",
            "--no-extensions",
            "--no-prompt-templates",
            "--no-tools",
            "--print",
        ],
        "unsupported_role_fields": [],
        "notes": "Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.",
        "summary": "Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.",
        "tags": ["system:deskops"],
    }
    return render_model_markdown(RuntimeProfileDoc, payload) + "\n"


def desk_markdown_docs(desk_dir: Path) -> list[Path]:
    return sorted(path for path in desk_dir.rglob("*.md") if path.is_file())


def desk_doc_is_modeled_by_sldb(root: Path, doc_path: Path) -> bool:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return False

    parts = relative.parts
    if not parts:
        return False

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return False

    return top_level in _MODELED_DESK_TOP_LEVEL_DIRS


def desk_doc_unmodeled_reason(root: Path, doc_path: Path) -> str | None:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return None

    parts = relative.parts
    if not parts:
        return None

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return f"desk/{relative.name} is a top-level desk note intentionally not SLDB-modeled"
    if top_level not in _MODELED_DESK_TOP_LEVEL_DIRS:
        return f"desk/{top_level}/** is intentionally not SLDB-modeled"
    return None


def modeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if desk_doc_is_modeled_by_sldb(root, path)]


def unmodeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if not desk_doc_is_modeled_by_sldb(root, path)]


def _surface_docs(desk_dir: Path) -> list[Path]:
    docs: list[Path] = []
    board = desk_dir / "tasks" / "Board.md"
    if board.exists():
        docs.append(board)

    tasks_dir = desk_dir / "tasks"
    if tasks_dir.exists():
        docs.extend(sorted(path for path in tasks_dir.glob("*.md") if path.name != "Board.md"))

    contexts_dir = desk_dir / "contexts"
    if contexts_dir.exists():
        docs.extend(sorted(path for path in contexts_dir.glob("*.md")))
    return docs


def _read_declared_desk_format(config_path: Path) -> str | None:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    versions = payload.get("versions")
    if not isinstance(versions, dict):
        return None
    desk_format = versions.get("desk_format")
    return desk_format if isinstance(desk_format, str) else None


def _inspect_surface_store_health(root: Path, surface_docs: list[Path]) -> tuple[set[Path], list[str], str | None]:
    store_path = root / ".sldb"
    if not store_path.exists():
        return set(), [], None

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(store_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    tracked: set[Path] = set()
    invalid: list[str] = []
    tracked_surface_set = {path.resolve() for path in surface_docs}

    payload: dict[str, object] | None = None
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout)
        except json.JSONDecodeError:
            return tracked, invalid, "sldb stores check returned unreadable JSON"
        if isinstance(loaded, dict):
            payload = loaded

    if payload is not None:
        for model in payload.get("models", []):
            if not isinstance(model, dict):
                continue
            for doc in model.get("documents", []):
                if not isinstance(doc, dict):
                    continue
                doc_path = doc.get("path")
                if not isinstance(doc_path, str):
                    continue
                absolute = (root / doc_path).resolve()
                if absolute not in tracked_surface_set:
                    continue
                tracked.add(absolute)
                # An edited, re-contracted or moved document is an alert, not a malformed
                # surface: it does not make the desk legacy (see deskops.doctor_findings).
                note = doc.get("note")
                if note not in _NOT_MALFORMED_NOTES:
                    invalid.append(f"{doc_path} ({note})")

    # `stores check` exits 1 on a store that only moved; its JSON is the verdict, the exit
    # code only matters when there is no JSON to read.
    if result.returncode != 0 and payload is None:
        stderr = result.stderr.strip().splitlines()
        if stderr:
            return tracked, invalid, f"sldb stores check failed: {stderr[0]}"
        return tracked, invalid, "sldb stores check failed"

    return tracked, invalid, None


_NOT_MALFORMED_NOTES = frozenset({"ok", "benign_mutation", "data_mutation", "contract_mutation", "missing"})


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


# ---------------------------------------------------------------------------
# Desk-local task type registration and legacy task_type migration (GC01).
#
# A desk adds its own task types as `desk/models/*.py` subclasses (DC7); `desk update
# --apply` registers them with `sldb add_model` and `pythonpath` = the desk root. Legacy
# `task_type` strings are then re-tracked under the model their canonical type names
# (TaskDoc precisión 4).

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

#: The legacy ``task_type`` values that map onto a known type (the same map the migration
#: uses). Anything else is an unknown legacy value and migrates to ``task.code``.
LEGACY_TASK_TYPE_KEYS = frozenset({"code", "implementation", "test", "docs", "spec", "design", "external", ""})


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _frontmatter_task_type(path: Path) -> str:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return ""
    return str(parsed[0].get("task_type") or "").strip()


def discover_local_task_type_models(desk_dir: Path) -> list[tuple[str, str]]:
    """``(model_ref, class_name)`` for every ``TaskDoc`` subclass defined in ``desk/models/*.py``."""
    from deskops.models import TaskDoc

    models_dir = desk_dir / "models"
    if not models_dir.is_dir():
        return []
    desk_root = str(desk_dir.resolve())
    added = desk_root not in sys.path
    if added:
        sys.path.insert(0, desk_root)
    found: list[tuple[str, str]] = []
    try:
        for path in sorted(models_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            module_name = f"models.{path.stem}"
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            for name in dir(module):
                obj = getattr(module, name, None)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, TaskDoc)
                    and obj is not TaskDoc
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    found.append((f"{module_name}:{name}", name))
    finally:
        if added:
            sys.path.remove(desk_root)
    return found


def pending_local_task_type_models(root: Path) -> list[str]:
    """Desk-local task type models that are not registered yet, as readable labels."""
    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    try:
        from deskops.bootstrap import SLDBBootstrap

        registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    except Exception:
        registered = set()
    return [
        f"{module_ref} ({class_name})"
        for module_ref, class_name in discover_local_task_type_models(root / "desk")
        if class_name not in registered
    ]


def register_local_task_type_models(root: Path) -> list[str]:
    """Register unregistered desk-local task types; one change line per registration."""
    from deskops import doc_io
    from deskops.bootstrap import SLDBBootstrap

    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for module_ref, class_name in discover_local_task_type_models(root / "desk"):
        if class_name in registered:
            continue
        try:
            doc_io.register_model(root, module_ref, pythonpath=pythonpath)
        except Exception as exc:
            raise RuntimeError(f"could not register desk-local task type {class_name}: {exc}") from exc
        changes.append(f"registered {class_name} from {module_ref}")
    return changes


def _task_type_migration_plan(root: Path) -> list[dict]:
    """Per-task migration plan for ``desk/tasks``, including the canonical type and target model."""
    from deskops.models.task_types import LEGACY_TASK_TYPE_MAP
    from deskops.models.task_types import canonical_task_type_name
    from deskops.operations import DeskopsOperations

    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    operations = DeskopsOperations(root)
    registry = operations.registered_task_types()
    fallback = registry.get("task.code")
    plan: list[dict] = []
    for path in sorted(tasks_dir.glob("*.md")):
        if path.name == "Board.md" or path.name.startswith("board-"):
            continue
        raw = _frontmatter_task_type(path)
        canonical = raw if raw in registry else canonical_task_type_name(raw)
        target = registry.get(canonical) or fallback
        plan.append(
            {
                "path": path,
                "raw": raw,
                "canonical": canonical,
                "target_cls": target,
                "target_name": target.__name__ if target is not None else "TaskDoc",
                "unknown": bool(raw) and raw not in registry and raw not in LEGACY_TASK_TYPE_MAP,
            }
        )
    return plan


def pending_task_type_migration(root: Path) -> list[str]:
    """The change lines ``migrate_task_types`` would apply, so the dry run can list them."""
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    lines: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        lines.append(_task_type_migration_line(item, rel))
    return lines


def _task_type_migration_line(item: dict, rel: str) -> str:
    if item["unknown"]:
        return (
            f"unknown legacy task_type {item['raw']!r} in {rel}: migrated to {item['canonical']} "
            f"(tracked as {item['target_name']})"
        )
    return (
        f"migrated {rel}: task_type {item['raw']!r} -> {item['canonical']!r} "
        f"(tracked as {item['target_name']})"
    )


def _rewrite_task_type(path: Path, canonical: str) -> None:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return
    data, text = parsed
    data["task_type"] = canonical
    body = text[_FRONTMATTER_RE.match(text).end():]
    path.write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body,
        encoding="utf-8",
    )


def migrate_task_types(root: Path) -> list[str]:
    """Rewrite legacy ``task_type`` values and re-track each task under its type's model.

    Idempotent: a second run changes nothing. ``closeout_evidence`` is preserved because the
    frontmatter rewrite only touches ``task_type``.
    """
    from deskops import doc_io
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        if needs_rewrite:
            _rewrite_task_type(path, item["canonical"])
        if store_dir.exists() and item["target_cls"] is not None:
            if tracked_model is not None:
                try:
                    doc_io.untrack(root, path)
                except Exception:
                    pass
            doc_io.track(root, path, item["target_cls"], name=path.stem, pythonpath=pythonpath, force=True)
        changes.append(_task_type_migration_line(item, rel))
    return changes

FILE:deskops/doc_access.py
"""Reading, writing and resolving the documents of one desk.

Every function takes the repository ``root`` (the directory that holds ``desk/``) and
works on the desk documents under it: parse a document into its model payload, write
one through a ``doc_io`` transaction, resolve a selector to a file, read a task with
its inherited context, or list the artifacts of one kind. ``DeskopsOperations`` is a
facade over these functions and the services; the services call them directly.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any

import yaml
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_io
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.desk_paths import resolve_selector
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import DeskFAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import ReviewDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.runtime import Task
from deskops.specs import compile_artifact_spec
from deskops.specs import compile_task_spec
from deskops.workspace import scaffold_desk


ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.materialization": MaterializationContractDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.review": ReviewDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": DeskFAQDoc,
    "artifact.step": StepDoc,
}

ARTIFACT_PATHS = {
    "artifact.task": "tasks",
    "artifact.pill": "contexts",
    "artifact.ritual": "rituals",
    "artifact.board": "tasks",
    "artifact.atom": "atoms",
    "artifact.materialization": "materializations",
    "artifact.repository": "registry",
    "artifact.review": "reviews",
    "artifact.inbox_note": "inbox",
    "artifact.faq": "faq",
    "artifact.step": "steps",
}

ARTIFACT_SUBJECTS = {
    "artifact.pill": {"subject": "pill", "list_subject": "pills"},
    "artifact.ritual": {"subject": "ritual", "list_subject": "rituals"},
    "artifact.board": {"subject": "board", "list_subject": "boards"},
    "artifact.atom": {"subject": "atom", "list_subject": "atoms"},
    "artifact.materialization": {"subject": "materialization", "list_subject": "materializations"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.review": {"subject": "review", "list_subject": "reviews", "create": False},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}

# Fields whose value is an effect of a workflow command, not a free edit. The
# value names who writes the field, so the refusal teaches the correct entry
# point instead of only saying no.
_TASK_OWNED_FIELDS = {
    "status": "deskops advance (transition effects) and deskops closeout commit",
    "current_node": "deskops advance",
    "history": "deskops advance and deskops closeout (append-only)",
    "task_type": "deskops add task --task-type (create a new task to change the type)",
    "closeout_evidence": "the task type, and deskops add task --evidence at creation",
}

# Artifacts whose documents are named by hand: their files are not `<id_pattern>.md`.
_FREE_NAMED_ARTIFACTS = {"artifact.inbox_note", "artifact.board", "artifact.ritual", "artifact.review"}

# Artifacts `create_artifact` tracks in the desk's store on creation.
_TRACKED_ON_CREATE = {"artifact.atom", "artifact.pill", "artifact.materialization"}

# (absolute path, model) -> (text, payload): ``read_doc`` parses a document once per text.
_DOC_PAYLOADS: dict[tuple[str, Any], tuple[str, dict[str, Any]]] = {}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


@dataclass(slots=True)
class DocumentRecord:
    kind: str
    doc_id: str
    path: Path


@dataclass(slots=True)
class RepoTaskRoute:
    repo_id: str
    repo_root: Path
    task_id: str
    task_path: Path
    board_path: Path
    title: str
    status: str


def desk_root(root: Path) -> Path:
    return root / "desk"


# ---------------------------------------------------------------- workspace
def ensure_workspace(root: Path) -> None:
    """The desk scaffold, the artifact directories and the default tag namespaces."""
    scaffold_desk(root)
    for relative in [
        Path("atoms"),
        Path("materializations"),
        Path("steps"),
        Path("registry"),
        Path("faq"),
    ]:
        (desk_root(root) / relative).mkdir(parents=True, exist_ok=True)
    ensure_default_namespaces(default_registry_path(root))


# ---------------------------------------------------------------- read / write
def read_doc(path: Path, model: type[Any]) -> dict[str, Any]:
    """The model payload of a document, parsed once per text of the file.

    The parse is kept for the whole process under (path, model) with the text it came
    from, and handed out as a copy: a reader that builds a new ``DeskopsOperations`` per
    request (the UI's server) does not re-parse unchanged documents, and a caller that
    edits the payload it got does not edit the kept one.
    """
    raw_text = path.read_text(encoding="utf-8")
    key = (os.path.abspath(path), model)
    hit = _DOC_PAYLOADS.get(key)
    if hit is not None and hit[0] == raw_text:
        return copy.deepcopy(hit[1])
    payload = extract_model_data(model, raw_text)
    if "id" not in payload:
        payload["id"] = path.stem
    _DOC_PAYLOADS[key] = (raw_text, copy.deepcopy(payload))
    return payload


def write_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    rendered = render_model_markdown(model, payload) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        # A short new value is not proof the model cannot read the file: only
        # refuse when the current text really extracts empty for that field.
        unreadable = set(is_unreadable_by_model(model, existing))
        lost = [field for field in unread_section_fields(model, existing, rendered) if field in unreadable]
        if lost:
            raise ValueError(
                f"Refusing to rewrite {path.name}: its model cannot read "
                f"{', '.join(lost)} from the current file, so writing this payload "
                "would erase that content. The document was not produced by the "
                "model's own renderer; rewrite it through sldb (or fix the model's "
                "template) before editing it here."
            )
        # Headings and frontmatter keys the template never declares are dropped by
        # extraction; refuse when the rewrite would erase one. A heading counts only
        # if re-rendering the file's own payload loses it, so replacing a field that
        # carries a heading (atoms split/merge) is not refused.
        kept = set((render_model_markdown(model, extract_model_data(model, existing)) + "\n").splitlines())
        erased = [line for line in find_structural_noise(model, existing, path.name).undeclared if line not in kept]
        erased += [f"frontmatter key '{key}'" for key in undeclared_frontmatter_keys(model, existing)]
        if erased:
            raise ValueError(
                f"Refusing to rewrite {path.name}: it has content its model "
                f"({model.__name__}) does not declare, and rewriting would erase it: "
                f"{'; '.join(erased)}. Move that content into a declared field "
                "(or remove it) before editing the document here."
            )
    with doc_io.DocTransaction(root) as transaction:
        transaction.write(path, model, payload)


def write_new_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    try:
        write_doc(root, path, model, payload)
    except Exception:
        remove_created_file(path)
        raise


def remove_created_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def track_created_document(root: Path, model: type[Any], path: Path, doc_id: str) -> None:
    doc_io.track(root, path, model, name=doc_id)


def track_created_artifact(root: Path, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
    if artifact_id not in _TRACKED_ON_CREATE:
        return
    track_created_document(root, model, path, doc_id)


# ---------------------------------------------------------------- values
def coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def merge_unique(*values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value_list in values:
        for value in value_list:
            item = str(value)
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return merged


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    YAML folds the line breaks of multi-line text and reads `**bold` as an alias,
    so a text field (`str` or `str | None`) takes the raw value as written. A JSON
    string literal (`"..."`) is still decoded, for callers that quote their text.
    """
    annotation = model.model_fields[field_name].annotation
    if annotation in (str, str | None):
        if raw_value.startswith('"'):
            try:
                decoded = json.loads(raw_value)
            except ValueError:
                return raw_value
            if isinstance(decoded, str):
                return decoded
        return raw_value
    return parse_data_value(raw_value)


# ---------------------------------------------------------------- paths and selectors
def artifact_path(root: Path, artifact_id: str, doc_id: str) -> Path:
    return desk_root(root) / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"


def artifact_glob_pattern(artifact_id: str) -> str:
    if artifact_id in _FREE_NAMED_ARTIFACTS:
        return "*.md"
    id_pattern = str(getattr(ARTIFACT_MODELS[artifact_id], "__artifact__", {})["id_pattern"])
    return id_pattern.replace("{slug}", "*") + ".md"


def atom_folder_axis(root: Path) -> str | None:
    """Return the configured folder axis namespace for atoms, or None (flat)."""
    axis = DeskConfig.load(desk_root(root)).atom_folder_axis
    if axis is None:
        return None
    axis = str(axis).strip()
    if not axis:
        return None
    namespaces = load_namespaces(default_registry_path(root))
    if axis not in namespaces:
        raise ValueError(
            f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
            "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
        )
    return axis


def atom_doc_path(root: Path, atom_id: str, tags: list[str]) -> Path:
    base = desk_root(root) / "atoms"
    axis = atom_folder_axis(root)
    if axis is not None:
        value = folder_axis_value(tags, axis)
        if value is not None:
            return base / axis_folder_relpath(value) / f"{atom_id}.md"
    return base / f"{atom_id}.md"


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_selector(desk_root(root), [directory], doc_id, f"{doc_id}*.md", "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            directories,
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        if artifact_id != "artifact.review":
            raise
    # A review's id is the authority; its file is named `<kind>-<n>.md` under
    # `desk/reviews/<task-id>/`, so resolve it by the id its frontmatter carries
    # (TaskDoc precisión 4: nothing parses the id back out of the path).
    matches = [
        path
        for directory in directories
        if directory.exists()
        for path in sorted(directory.rglob("*.md"))
        if frontmatter_id(path) == selector
    ]
    if not matches:
        raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous {artifact_id} selector '{selector}': {names}")
    return matches[0]


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            [directory],
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        tracked = _tracked_task_paths(root) if artifact_id == "artifact.task" else set()
        if not tracked:
            raise
    # Tasks written before the `task-*` naming are still tracked TaskDocs.
    return resolve_selector(
        desk_root(root),
        [directory],
        selector,
        "*.md",
        artifact_id,
        recursive=True,
        keep=lambda path: path.resolve() in tracked,
    )


def _tracked_task_paths(root: Path) -> set[Path]:
    # Tasks are tracked under their type model (TaskCodeDoc, …) and, for pre-type
    # documents, under TaskDoc. Legacy file names resolve only through the tracked paths.
    from deskops.services.tasks import registered_task_types

    model_names = {"TaskDoc"}
    model_names.update(getattr(cls, "__name__") for cls in registered_task_types(root).values())
    tracked: set[Path] = set()
    for model_name in model_names:
        records = root / ".sldb" / "core" / "documents" / model_name
        if not records.is_dir():
            continue
        for record in records.glob("*.yaml"):
            try:
                path = (yaml.safe_load(record.read_text(encoding="utf-8")) or {}).get("path")
            except (OSError, yaml.YAMLError):
                continue
            if path:
                tracked.add((root / path).resolve())
    return tracked


def frontmatter_id(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        payload = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(payload, dict) or payload.get("id") is None:
        return None
    return str(payload["id"])


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    try:
        return resolve_artifact_selector(root, "artifact.ritual", directory, selector)
    except FileNotFoundError:
        pass
    # Ritual files are named by hand; accept the frontmatter id as well.
    matches = (
        [path for path in sorted(directory.glob("*.md")) if frontmatter_id(path) == selector]
        if directory.exists()
        else []
    )
    if not matches:
        raise FileNotFoundError(f"No artifact.ritual file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous artifact.ritual selector '{selector}': {names}")
    return matches[0]


def editable_artifact(root: Path, subject: str, selector: str) -> tuple[type[Any], Path, str]:
    """The model, file and kind of the document `deskops edit <subject> <selector>` names."""
    if subject == "task":
        try:
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "tasks", selector)
        except FileNotFoundError:
            # Drawer candidates are tasks too; an active task with the same
            # selector wins because it resolved before this fallback.
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "drawer" / "tasks", selector)
        return TaskDoc, path, "task"
    artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
    if subject not in artifact_subjects:
        raise ValueError(f"Unsupported edit subject: {subject}")
    artifact_id = artifact_subjects[subject]
    model = ARTIFACT_MODELS[artifact_id]
    if artifact_id == "artifact.ritual":
        return model, resolve_ritual_selector(root, selector), subject
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    path = resolve_artifact_selector_multi(root, artifact_id, directories, selector)
    return model, path, subject


# ---------------------------------------------------------------- tasks
def resolve_task_payload(root: Path, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
    """The normalized payload of a task with its inherited context (``effective_*``)."""
    if task_id in stack:
        chain = " -> ".join([*stack, task_id])
        raise ValueError(f"Task inheritance cycle detected: {chain}")
    path = resolve_glob(root, desk_root(root) / "tasks", task_id)
    payload = compile_task_spec(read_doc(path, TaskDoc), entry_node="").task_payload
    inherited_ids = coerce_list(payload.get("inherits_from") or [])
    inherited_payloads = [resolve_task_payload(root, parent_id, (*stack, task_id)) for parent_id in inherited_ids]

    payload["effective_references"] = merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
        payload.get("references", []),
    )
    payload["effective_pills"] = merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
        payload.get("pills", []),
    )
    payload["effective_tags"] = merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
        payload.get("atoms", []),
    )

    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = merge_unique(
            *[parent.get("effective_validation", parent.get("validation", [])) for parent in inherited_payloads],
            payload.get("validation", []),
        )
        parent_done_when = next(
            (
                str(parent.get("effective_done_when") or parent.get("done_when") or "")
                for parent in inherited_payloads
                if str(parent.get("effective_done_when") or parent.get("done_when") or "")
            ),
            "",
        )
        payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
    else:
        payload["effective_validation"] = coerce_list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    return payload


def hydrate_task(payload: dict[str, Any]) -> Task:
    return Task(
        id=payload["id"],
        title=payload["title"],
        status=payload["status"],
        summary=payload["goal"],
        tags=list(payload.get("tags") or []),
        current_node=payload.get("current_node", ""),
        history=list(payload.get("history") or []),
        goal=payload.get("goal", ""),
        scope=payload.get("scope", ""),
        references=list(payload.get("references") or []),
        depends_on=list(payload.get("depends_on") or []),
        pills=list(payload.get("pills") or []),
        files=list(payload.get("files") or []),
        implementation_path=payload.get("implementation_path", ""),
        validation=list(payload.get("validation") or []),
        done_when=payload.get("done_when", ""),
        task_type=payload.get("task_type", ""),
        inherits_from=list(payload.get("inherits_from") or []),
        inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
        atoms=list(payload.get("atoms") or []),
        from_drawer=payload.get("from_drawer") or "",
        closeout_evidence=list(payload.get("closeout_evidence") or []),
        effective_references=list(payload.get("effective_references") or payload.get("references") or []),
        effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
        effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
        effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
        effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
        effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
    )


def load_task(root: Path, task_id: str) -> Task:
    return hydrate_task(resolve_task_payload(root, task_id))


# ---------------------------------------------------------------- artifacts
def list_artifacts(root: Path, artifact_id: str) -> list[dict[str, Any]]:
    model = ARTIFACT_MODELS[artifact_id]
    directory = desk_root(root) / ARTIFACT_PATHS[artifact_id]
    if not directory.exists():
        if not desk_root(root).exists():
            raise FileNotFoundError(f"Desk root not found at {desk_root(root)}. Run 'deskops init' to initialize.")
        return []
    pattern = artifact_glob_pattern(artifact_id)
    results = []
    for path in sorted(directory.rglob(pattern)):
        try:
            results.append(read_doc(path, model))
        except Exception as e:
            print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
    return results


def show_artifact(root: Path, artifact_id: str, doc_id: str) -> dict[str, Any]:
    if not doc_id:
        raise ValueError(f"No {artifact_id} ID provided")
    model = ARTIFACT_MODELS[artifact_id]
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    return read_doc(resolve_artifact_selector_multi(root, artifact_id, directories, doc_id), model)


def create_artifact(root: Path, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
    ensure_workspace(root)
    model = ARTIFACT_MODELS[artifact_id]
    compiled = compile_artifact_spec(artifact_id, raw_payload, model_fields=model.model_fields.keys())
    doc_id = compiled.artifact_payload["id"]
    if artifact_id == "artifact.atom":
        tags = list(compiled.artifact_payload.get("tags") or [])
        validate_atom_tag_namespaces(tags, default_registry_path(root))
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(desk_root(root) / "atoms", tags)
        path = atom_doc_path(root, doc_id, tags)
    else:
        path = artifact_path(root, artifact_id, doc_id)
    with doc_io.DocTransaction(root):
        write_new_doc(root, path, model, compiled.artifact_payload)
        track_created_artifact(root, artifact_id, model, path, doc_id)
    return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=doc_id, path=path)


def edit_artifact_field(root: Path, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
    ensure_workspace(root)
    model, path, kind = editable_artifact(root, subject, selector)
    field_name = field.replace("-", "_")
    if field_name not in model.model_fields:
        raise ValueError(f"Unknown field '{field_name}' for {subject}")
    if field_name == "id":
        raise ValueError("Cannot edit immutable field 'id'")
    if subject == "task" and field_name in _TASK_OWNED_FIELDS:
        raise ValueError(
            f"{field_name} is not editable with edit task; "
            f"it is written by {_TASK_OWNED_FIELDS[field_name]}."
        )
    if subject == "review" and field_name in {"verdict", "reason", "disposed_at", "disposed_by"}:
        raise ValueError(
            "verdict is written by deskops review dispose (GC03); a new review is a new document"
        )
    payload = read_doc(path, model)
    payload[field_name] = _parse_field_value(model, field_name, raw_value)
    write_doc(root, path, model, payload)
    return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)


# ---------------------------------------------------------------- registry
def registered_repositories(root: Path) -> list[dict[str, Any]]:
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    repositories = []
    for path in sorted(registry_dir.glob("repo-*.md")):
        try:
            repositories.append(read_doc(path, RepositoryDoc))
        except Exception as e:
            print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
            continue
    return repositories


def repository_root(root: Path, repository: dict[str, Any]) -> Path:
    repo_path = Path(str(repository["path"]))
    if repo_path.is_absolute():
        return repo_path.resolve()
    return (root / repo_path).resolve()


def _resolve_repo_board_task_path(repo_root: Path, task_ref: str) -> Path | None:
    tasks_root = (repo_root / "desk" / "tasks").resolve()
    task_path = Path(task_ref)
    if not task_path.is_absolute():
        task_path = repo_root / task_path
    task_path = task_path.resolve()
    try:
        task_path.relative_to(tasks_root)
    except ValueError:
        return None
    if not task_path.name.startswith("task-") or task_path.suffix != ".md":
        return None
    if not task_path.is_file():
        return None
    return task_path


def _task_route_summary(task_path: Path) -> dict[str, str]:
    text = task_path.read_text(encoding="utf-8")
    payload: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                frontmatter = None
            if isinstance(frontmatter, dict):
                payload = frontmatter
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), task_path.stem)
    legacy_status = next((line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Status:")), "unknown")
    task_id = str(payload.get("id") or task_path.stem)
    if not task_id.startswith("task-"):
        raise ValueError(f"Routed task id must start with 'task-': {task_id}")
    return {
        "id": task_id,
        "status": str(payload.get("status") or legacy_status),
        "title": title,
    }


def list_repo_task_routes(root: Path) -> list[RepoTaskRoute]:
    routes: list[RepoTaskRoute] = []
    for repository in registered_repositories(root):
        repo_root = repository_root(root, repository)
        board_path = repo_root / "desk" / "tasks" / "Board.md"
        if not board_path.exists():
            continue
        try:
            board_payload = read_doc(board_path, BoardDoc)
        except Exception:
            continue
        for task_ref in board_payload.get("tasks") or []:
            task_path = _resolve_repo_board_task_path(repo_root, str(task_ref))
            if task_path is None:
                continue
            try:
                summary = _task_route_summary(task_path)
            except (OSError, UnicodeDecodeError, ValueError):
                continue
            routes.append(
                RepoTaskRoute(
                    repo_id=str(repository["id"]),
                    repo_root=repo_root,
                    task_id=summary["id"],
                    task_path=task_path,
                    board_path=board_path,
                    title=summary["title"],
                    status=summary["status"],
                )
            )
    return routes

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task. deskops writes those documents
once per desk from ``deskops/spec/workflows/task_lifecycle.yaml`` and reads the transitions back
from the graph with ``sldb.api.edges.edges_from``; there are no per-task primitives.

What the graph does not carry is the effect of a transition: the status it sets and
whether it closes the task. Those come from the spec, keyed by relation type. Conditions
are evaluated by sldb itself (``sldb.api.where_matches``, sldb >= 0.1.6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import render_model_markdown

from deskops import doc_io
from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


@dataclass(frozen=True, slots=True)
class Transition:
    relation_type: str
    title: str
    description: str
    source: str
    target: str
    condition: str
    sets_status: str
    terminal: bool = False


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    entry_node: str
    transitions: tuple[Transition, ...]
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return list(dict.fromkeys(node for t in self.transitions for node in (t.source, t.target)))

    def effect(self, relation_type: str) -> Transition:
        for transition in self.transitions:
            if transition.relation_type == relation_type:
                return transition
        raise KeyError(f"Relation type '{relation_type}' is not part of the task lifecycle in {SPEC_PATH}")


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it and the closure service keeps the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    transitions = tuple(
        Transition(
            relation_type=str(item["relation_type"]),
            title=str(item.get("title") or item["relation_type"]),
            description=str(item.get("description") or ""),
            source=str(item["source"]),
            target=str(item["target"]),
            condition=str(item.get("condition") or ""),
            sets_status=str(item.get("sets_status") or ""),
            terminal=bool(item.get("terminal") or False),
        )
        for item in payload.get("transitions") or []
    )
    if not transitions:
        raise ValueError(f"Lifecycle spec declares no transitions: {path}")
    return LifecycleSpec(
        entry_node=str(payload.get("entry_node") or transitions[0].source),
        transitions=transitions,
        states=tuple(state for state in payload.get("states") or [] if isinstance(state, dict)),
    )


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def _pythonpath() -> str:
    return package_pythonpath()


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def transitions_from(
    root: Path, node: str, spec: LifecycleSpec | None = None, *, snapshot: ReadSnapshot | None = None
) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology and conditions come from the graph; the effect of each transition comes from
    the spec. A relation type the spec does not know is not a lifecycle transition.

    The lifecycle graph lives in the desk's own store (``ensure_lifecycle_graph`` writes it
    there), so only that store's edge index is read (sldb keeps it composed while its shards
    do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node, spec)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    spec = spec or load_lifecycle_spec()
    known = {t.relation_type for t in spec.transitions}
    found: list[Transition] = []
    for edge in edges_from(_store(root), ritual_export_id(node), include_linked=False):
        if edge.relation not in known or edge.metadata.get("origin") != "relation_doc":
            continue
        effect = spec.effect(edge.relation)
        target = edge.target.rsplit(":", 1)[-1]
        found.append(
            Transition(
                relation_type=edge.relation,
                title=effect.title,
                description=effect.description,
                source=node,
                target=target,
                condition=str(edge.metadata.get("condition") or ""),
                sets_status=effect.sets_status,
                terminal=effect.terminal,
            )
        )
    return sorted(found, key=lambda t: [x.relation_type for x in spec.transitions].index(t.relation_type))


def advance(root: Path, payload: dict[str, Any], spec: LifecycleSpec | None = None) -> TransitionResult:
    """Fire the first transition out of the task's current node whose condition holds.

    Mutates ``payload`` (``current_node``, ``status``, ``history``) and reports what
    happened; one call fires at most one transition.
    """
    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    transitions = transitions_from(root, node, spec)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    for transition in transitions:
        if not condition_holds(transition.condition, payload):
            continue
        if transition.sets_status:
            payload["status"] = transition.sets_status
        history = payload.setdefault("history", [])
        if isinstance(history, list):
            history.append(transition.relation_type)
        payload["current_node"] = COMPLETE if transition.terminal else transition.target
        verb = "Completed" if transition.terminal else "Advanced to"
        target = COMPLETE if transition.terminal else transition.target
        return TransitionResult(payload["current_node"], str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")
    payload["current_node"] = node
    gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
    return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")


# ---------------------------------------------------------------- writing the graph
def _doc_tracked(root: Path, model: str, name: str) -> bool:
    from sldb.api import doc_exists

    return doc_exists(_store(root), f"{model}/{name}")


def _track(root: Path, model: str, path: Path, name: str) -> None:
    doc_io.track(root, path, model, name=name, pythonpath=_pythonpath(), force=False)


def _ensure_ritual_readable(path: Path, ritual_id: str, relative: str) -> bool:
    """Re-render a ritual RitualDoc cannot read; raise if it still cannot round-trip.

    Returns whether the file was rewritten. A hand-authored or older-template ritual can
    extract as empty while its sections still hold text, so the extracted payload alone
    is not enough: the source must also be readable by the model.
    """
    from deskops.doc_readability import is_unreadable_by_model
    from deskops.models import RitualDoc
    from sldb.runtime.validation import extract_model_data

    text = path.read_text(encoding="utf-8")
    try:
        payload = extract_model_data(RitualDoc, text)
        rendered = render_model_markdown(RitualDoc, payload)
        round_trips = extract_model_data(RitualDoc, rendered) == payload
    except Exception as exc:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} cannot be read as {RITUAL_MODEL}: {exc}"
        ) from exc
    from sldb.api.documents.structural_noise import find_structural_noise

    undeclared = find_structural_noise(RitualDoc, text, relative).undeclared
    if undeclared:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} has sections {RITUAL_MODEL} does not declare: "
            + "; ".join(undeclared)
        )
    missing = is_unreadable_by_model(RitualDoc, text)
    if not missing and round_trips:
        return False

    path.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
    repaired = path.read_text(encoding="utf-8")
    try:
        still_missing = is_unreadable_by_model(RitualDoc, repaired)
        lost = [key for key in payload if extract_model_data(RitualDoc, repaired).get(key) != payload.get(key)]
    except Exception as exc:
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} cannot be read as {RITUAL_MODEL} after re-rendering: {exc}"
        ) from exc
    if still_missing or lost:
        fields = ", ".join(still_missing or lost)
        raise LifecycleGraphMissing(
            f"Lifecycle ritual '{ritual_id}' at {relative} still cannot round-trip through {RITUAL_MODEL} "
            f"after re-rendering; missing sections: {fields}"
        )
    return True


def _archive_legacy_ritual(root: Path, path: Path, ritual_id: str) -> Path:
    """Move a ritual RitualDoc cannot carry to desk/drawer/rituals/ and write the default one.

    A hand-written ritual (no frontmatter id, its own sections, other field shapes) would
    lose text if it were re-rendered, so it is kept byte for byte where the desk does not
    model documents, and the lifecycle state gets the ritual `deskops init` writes.
    """
    from deskops.workspace import default_ritual_text

    archive_dir = root / "desk" / "drawer" / "rituals"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = archive_dir / f"legacy-{path.name}"
    counter = 2
    while archived.exists():
        archived = archive_dir / f"legacy-{path.stem}-{counter}.md"
        counter += 1
    path.rename(archived)
    path.write_text(default_ritual_text(ritual_id, root.name), encoding="utf-8")
    return archived


def ensure_lifecycle_graph(root: Path, spec: LifecycleSpec | None = None) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: registers sldb's relation models, tracks the lifecycle rituals by their
    ids, and writes plus tracks one RelationTypeDoc and one RelationDoc per transition
    under desk/lifecycle/. Existing documents are left as they are.
    """
    from sldb.models.relation_doc import RelationDoc
    from sldb.models.relation_type_doc import RelationTypeDoc

    root = root.resolve()
    spec = spec or load_lifecycle_spec()
    changes: list[str] = []
    doc_io.init_relations_in(root, pythonpath=_pythonpath())

    from sldb.api import doc_status

    pending_rituals: list[tuple[str, Path, str]] = []
    for ritual_id in spec.rituals:
        if _doc_tracked(root, RITUAL_MODEL, ritual_id):
            continue
        path = root / "desk" / "rituals" / f"{ritual_id.removeprefix('ritual-')}.md"
        if not path.exists():
            raise LifecycleGraphMissing(f"Lifecycle ritual '{ritual_id}' has no document at {path.relative_to(root)}")
        relative = path.relative_to(root).as_posix()
        try:
            rerendered = _ensure_ritual_readable(path, ritual_id, relative)
        except LifecycleGraphMissing as exc:
            archived = _archive_legacy_ritual(root, path, ritual_id)
            changes.append(
                f"archived {relative} to {archived.relative_to(root).as_posix()} "
                f"and wrote the default ritual in its place ({exc})"
            )
            rerendered = _ensure_ritual_readable(path, ritual_id, relative)
        if rerendered:
            changes.append(f"re-rendered {relative} to the current {RITUAL_MODEL} template")
        pending_rituals.append((ritual_id, path, relative))

    for ritual_id, path, relative in pending_rituals:
        current = doc_status(_store(root), relative)
        if current.exists and current.name != ritual_id:
            # `desk update` tracks surface documents by file stem; the graph names a
            # ritual by its id, so the ritual is re-tracked under that id.
            doc_io.untrack(root, root / relative, pythonpath=_pythonpath())
            changes.append(f"untracked {relative} (was {current.model}:{current.name})")
        _track(root, RITUAL_MODEL, path, ritual_id)
        changes.append(f"tracked {relative} as {ritual_export_id(ritual_id)}")

    lifecycle_dir = root / LIFECYCLE_DIR
    lifecycle_dir.mkdir(parents=True, exist_ok=True)
    for transition in spec.transitions:
        type_name = transition.relation_type
        type_path = lifecycle_dir / f"type-{type_name}.md"
        if not type_path.exists():
            type_path.write_text(
                render_model_markdown(
                    RelationTypeDoc,
                    {
                        "title": transition.title,
                        "name": type_name,
                        "direction": "directed",
                        "cardinality": "many_to_many",
                        "axis": "HOW",
                        "source_types": [RITUAL_MODEL],
                        "target_types": [RITUAL_MODEL],
                        "condition": "",
                        "description": transition.description,
                    },
                )
                + "\n",
                encoding="utf-8",
            )
            changes.append(f"wrote {type_path.relative_to(root)}")
        if not _doc_tracked(root, RELATION_TYPE_MODEL, f"type-{type_name}"):
            _track(root, RELATION_TYPE_MODEL, type_path, f"type-{type_name}")
            changes.append(f"tracked {type_path.relative_to(root)}")

        edge_name = f"{transition.source.removeprefix('ritual-')}-{type_name}"
        edge_path = lifecycle_dir / f"{edge_name}.md"
        if not edge_path.exists():
            edge_path.write_text(
                render_model_markdown(
                    RelationDoc,
                    {
                        "title": transition.title,
                        "source_id": ritual_export_id(transition.source),
                        "target_id": ritual_export_id(transition.target),
                        "relation_type": type_name,
                        "condition": transition.condition,
                        "notes": transition.description,
                    },
                )
                + "\n",
                encoding="utf-8",
            )
            changes.append(f"wrote {edge_path.relative_to(root)}")
        if not _doc_tracked(root, RELATION_MODEL, edge_name):
            _track(root, RELATION_MODEL, edge_path, edge_name)
            changes.append(f"tracked {edge_path.relative_to(root)}")
    return changes


def lifecycle_graph_present(root: Path, spec: LifecycleSpec | None = None) -> bool:
    spec = spec or load_lifecycle_spec()
    try:
        return all(transitions_from(root, node, spec) for node in {t.source for t in spec.transitions})
    except Exception:
        return False

FILE:deskops/cli/commands/core.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import scaffold_desk


class AboutCLI:
    def run(self, args: Any) -> int:
        # Resolved through the CLI module so a patched entrypoint stays visible.
        from deskops.cli import main as main_module

        return main_module.print_about()


class BootstrapCLI:
    def run(self, args: Any) -> int:
        return SLDBBootstrap().ensure_machine_ready()


class InitCLI:
    def run(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        bootstrap = SLDBBootstrap()
        ready = bootstrap.ensure_machine_ready()
        if ready != 0:
            return ready

        local_store = bootstrap.init_local_store(target_path)
        if local_store != 0:
            return local_store

        result = scaffold_desk(target_path)
        if result.wrote_anything:
            print(f"Scaffolded desk at {target_path / 'desk'}.")
            for path in result.created_paths:
                print(f"Wrote {path}")
        else:
            print(f"Desk already exists at {target_path / 'desk'}.")
        from deskops.lifecycle import ensure_lifecycle_graph

        for change in ensure_lifecycle_graph(target_path):
            print(f"Lifecycle graph: {change}")
        print("Initialization complete.")
        return 0

FILE:deskops/cli/commands/desk.py
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from deskops import doc_io
from deskops.workspace import ensure_target_directory
from deskops.workspace import inspect_desk
from deskops.workspace import migrate_desk
from deskops.workspace import migrate_task_types
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import pending_local_task_type_models
from deskops.workspace import pending_task_type_migration
from deskops.workspace import register_local_task_type_models
from deskops.workspace import scaffold_desk
from deskops.bootstrap import SLDBBootstrap, MODEL_REFS
from deskops.errors import DeskopsEnvironmentError
from deskops.paths import package_pythonpath
import deskops.models as models

#: The deskops FAQ model used to be registered with the same name sldb uses for its
#: own model. sldb federates models by name, so the old name must be migrated.
LEGACY_FAQ_MODEL = "FAQDoc"
LEGACY_FAQ_MODEL_REF = "deskops.models:FAQDoc"
FAQ_MODEL = "DeskFAQDoc"
FAQ_MODEL_REF = "deskops.models:DeskFAQDoc"


def legacy_faq_model_pending(entries: dict[str, Any]) -> bool:
    """Whether a store still registers the old deskops FAQ model name."""
    entry = entries.get(LEGACY_FAQ_MODEL)
    return entry is not None and getattr(entry, "model_ref", None) == LEGACY_FAQ_MODEL_REF


def moved_model_contracts(root: Path, entries: dict[str, Any]) -> list[str]:
    """Registered deskops models whose store contract no longer matches this checkout."""
    from sldb.store.hashing import hash_model_contract
    from sldb.store.io import load_models_index

    moved: list[str] = []
    for name, entry in sorted(entries.items()):
        model_ref = getattr(entry, "model_ref", "") or ""
        model_type = getattr(models, name, None)
        models_index = getattr(entry, "models_index", None)
        if not model_ref.startswith("deskops.models:") or model_type is None or not models_index:
            continue
        try:
            stored = load_models_index(root / models_index).contract_hash
        except Exception:
            continue
        if stored != hash_model_contract(model_type):
            moved.append(name)
    return moved


def migrate_legacy_faq_model(root: Path, *, pythonpath: str | None = None) -> list[str]:
    """Move an existing store from `FAQDoc` to `DeskFAQDoc`, keeping its documents.

    sldb exposes no model rename, so this registers the new name, retracks every
    document the old model owns, and removes the old entry with its document
    records. The Markdown files are never touched, so they stay byte-identical.
    """
    from sldb.store.io import load_documents_index
    from sldb.store.io import load_models_index

    store_dir = root / ".sldb"
    pythonpath = pythonpath or package_pythonpath()
    bootstrap = SLDBBootstrap()
    entries = bootstrap._registered_model_entries(store_dir)
    if not legacy_faq_model_pending(entries):
        return []

    changes: list[str] = []
    if FAQ_MODEL not in entries:
        doc_io.register_model(root, FAQ_MODEL_REF, pythonpath=pythonpath)
        changes.append(f"registered {FAQ_MODEL}")

    # The old class no longer exists, so its documents are read from the indexes
    # instead of resolving the model reference.
    legacy_entry = entries[LEGACY_FAQ_MODEL]
    legacy_index = load_models_index(root / legacy_entry.models_index)
    old_documents = load_documents_index(root / legacy_index.documents_index).documents
    tracked: set[str] = set()
    new_entry = bootstrap._registered_model_entries(store_dir).get(FAQ_MODEL)
    if new_entry is not None:
        new_index = load_models_index(root / new_entry.models_index)
        tracked = {document.name for document in load_documents_index(root / new_index.documents_index).documents}
    for document in old_documents:
        if document.name in tracked:
            continue
        doc_io.track(root, document.path, FAQ_MODEL, name=document.name, pythonpath=pythonpath)
        changes.append(f"tracked {document.name} as {FAQ_MODEL}")

    doc_io.remove_model_from(
        root, LEGACY_FAQ_MODEL, pythonpath=pythonpath, untrack_documents=True
    )
    changes.append(f"removed {LEGACY_FAQ_MODEL}")
    return changes


def guess_model_for_path(desk_dir: Path, path: Path) -> type | None:
    rel = path.relative_to(desk_dir)
    parts = rel.parts
    if len(parts) == 2 and parts[0] == "tasks":
        # Boards share tasks/ with the tasks (ARTIFACT_PATHS): the main Board.md and
        # any extra board written by `deskops add board` (stem `board-…`).
        if parts[1] == "Board.md" or path.stem.startswith("board-"):
            return models.BoardDoc
        return models.TaskDoc
    if len(parts) == 2 and parts[0] == "contexts":
        return models.PillDoc
    if len(parts) == 2 and parts[0] == "rituals":
        return models.RitualDoc
    if len(parts) == 2 and parts[0] == "atoms":
        if path.stem.startswith("proto-"):
            return models.ProtoAtomDoc
        return models.AtomDoc
    if len(parts) == 2 and parts[0] == "roles":
        return models.RoleDoc
    if len(parts) == 2 and parts[0] == "inbox":
        return models.InboxNoteDoc
    if len(parts) == 2 and parts[0] == "registry":
        return models.RepositoryDoc
    if len(parts) == 2 and parts[0] == "steps":
        return models.StepDoc
    if len(parts) == 2 and parts[0] == "faq":
        return models.DeskFAQDoc
    if len(parts) == 2 and parts[0] == "lifecycle":
        return None  # written and tracked by deskops.lifecycle.ensure_lifecycle_graph
    return None


def _is_task_file(desk_dir: Path, path: Path) -> bool:
    """Whether a modeled markdown path is a task document (migration owns its tracking)."""
    try:
        rel = path.resolve().relative_to((desk_dir / "tasks").resolve())
    except ValueError:
        return False
    return rel.parts and len(rel.parts) == 1 and rel.name.startswith("task-")


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        if args.desk_command == "replace":
            return self.replace(args)
        if args.desk_command == "update":
            return self.update(args)
        return 1

    def replace(self, args: Any) -> int:
        from deskops.services.replace import replace_text

        result = replace_text(
            Path(args.root),
            args.path,
            args.old,
            args.new,
            count=args.count,
        )
        print(f"Replaced {result.replacements} occurrence(s) in {result.path}")
        return 0

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = scaffold_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")

        if (target_path / ".sldb").exists():
            from deskops.lifecycle import ensure_lifecycle_graph

            for change in ensure_lifecycle_graph(target_path):
                print(f"Lifecycle graph: {change}")
        else:
            print("No .sldb store yet: run 'deskops init' to create it and the lifecycle graph that 'deskops advance' reads.")
        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        result = migrate_desk(target_path)
        print(f"Desk migration report for {target_path}:")

        print("Adopted:")
        if result.adopted:
            for item in result.adopted:
                print(f"- {item}")
        else:
            print("- none")

        print("Preserved:")
        if result.preserved:
            for item in result.preserved:
                print(f"- {item}")
        else:
            print("- none")

        print("Still manual:")
        if result.still_manual:
            for item in result.still_manual:
                print(f"- {item}")
        else:
            print("- none")

        return 0

    def update(self, args: Any) -> int:
        root = Path(args.root).resolve()
        apply = getattr(args, "apply", False)

        desk_dir = root / "desk"
        store_dir = root / ".sldb"

        from deskops.lifecycle_migration import inspect_legacy_lifecycle
        from deskops.lifecycle_migration import migrate_legacy_lifecycle

        legacy = inspect_legacy_lifecycle(root) if desk_dir.exists() else None
        legacy_pending = bool(legacy and (legacy.needs_migration or legacy.registered_legacy_models))
        if legacy_pending and apply:
            from deskops.lifecycle_migration import LegacyMigrationBlocked

            print("Migrating the task lifecycle to the desk's sldb graph...")
            if store_dir.exists() and "RitualDoc" not in SLDBBootstrap()._registered_model_entries(store_dir):
                # The lifecycle states are RitualDocs; a store that never registered the
                # model (an early desk) gets the deskops models before the graph is written.
                SLDBBootstrap().init_local_store(root)
                print("- registered the deskops models the lifecycle graph needs")
            try:
                for change in migrate_legacy_lifecycle(root):
                    print(f"- {change}")
            except LegacyMigrationBlocked as exc:
                print(f"Error: {exc}")
                return 1
            legacy_pending = False

        inspection = inspect_desk(root)

        missing_desk_files: list[str] = []
        if inspection.classification == "absent":
            missing_desk_files.append("desk/")
        elif desk_dir.exists():
            if not (desk_dir / "tasks" / "Board.md").exists():
                missing_desk_files.append("desk/tasks/Board.md")
            if not (desk_dir / "drawer").exists():
                missing_desk_files.append("desk/drawer/")
            if not (desk_dir / "reviews").exists():
                missing_desk_files.append("desk/reviews/")
            if not (desk_dir / "rituals" / "phase.md").exists():
                missing_desk_files.append("desk/rituals/phase.md")
            if not (desk_dir / "runtimes" / "runtime-pi-deepseek-flash.md").exists():
                missing_desk_files.append("desk/runtimes/runtime-pi-deepseek-flash.md")

        bootstrap = SLDBBootstrap()
        registered_entries: dict[str, Any] = {}
        if store_dir.exists():
            try:
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception:
                pass

        legacy_faq_pending = legacy_faq_model_pending(registered_entries)
        if legacy_faq_pending and apply:
            print(f"Migrating the deskops FAQ model from {LEGACY_FAQ_MODEL} to {FAQ_MODEL}...")
            try:
                for change in migrate_legacy_faq_model(root):
                    print(f"- {change}")
                registered_entries = bootstrap._registered_model_entries(store_dir)
            except Exception as exc:
                print(f"Error: {exc}")
                return 1
            legacy_faq_pending = False

        moved_contracts = (
            moved_model_contracts(root, registered_entries) if store_dir.exists() else []
        )
        if moved_contracts and apply:
            pythonpath = package_pythonpath()
            for model_name in moved_contracts:
                print(f"Updating the {model_name} contract...")
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "sldb",
                        "models",
                        "update",
                        model_name,
                        "--store",
                        str(store_dir),
                        "--pythonpath",
                        pythonpath,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode != 0:
                    detail = result.stderr.strip() or result.stdout.strip()
                    print(f"Error: could not update the {model_name} contract: {detail}")
                    return 1
                print(f"Updated {model_name} contract.")
            registered_entries = bootstrap._registered_model_entries(store_dir)
            moved_contracts = moved_model_contracts(root, registered_entries)

        unregistered_models: list[str] = []
        copied_models: list[str] = []
        # A non-editable install has no owner store to inherit from; its directly
        # registered models are the expected state, not copies to convert.
        owner_store = bootstrap._deskops_owner_store()
        if owner_store is not None and store_dir.exists() and store_dir.resolve() == owner_store.resolve():
            # The owner store registers the deskops models directly; that is what
            # the other stores link to, not a copy of it.
            owner_store = None
        for model_name, model_ref in MODEL_REFS.items():
            entry = registered_entries.get(model_name)
            if entry is None:
                unregistered_models.append(model_name)
            elif (
                owner_store is not None
                and not getattr(entry, "origin", None)
                and getattr(entry, "model_ref", None) == model_ref
            ):
                copied_models.append(model_name)

        invalid_docs: list[str] = []
        missing_docs: list[str] = []
        tracked_mds: set[Path] = set()
        missing_store = not store_dir.exists()
        if not missing_store:
            result = subprocess.run(
                [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store_dir), "--format", "json"],
                capture_output=True,
                text=True,
                check=False,
            )
            payload = None
            if result.stdout and result.stdout.strip():
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as exc:
                    raise DeskopsEnvironmentError(
                        f"Could not parse 'sldb stores check' output for {store_dir}: {exc}"
                    ) from exc
            if payload is None:
                if result.returncode != 0:
                    raise DeskopsEnvironmentError(
                        f"'sldb stores check' failed for {store_dir} with exit code {result.returncode}"
                    )
                raise DeskopsEnvironmentError(
                    f"'sldb stores check' produced no JSON output for {store_dir}"
                )
            for model in payload.get("models", []):
                for doc in model.get("documents", []):
                    doc_path = doc.get("path")
                    if not doc_path:
                        continue
                    tracked_path = (root / doc_path).resolve()
                    tracked_mds.add(tracked_path)

                    if doc.get("note") not in ("ok",):
                        invalid_docs.append(f"{doc_path} ({doc.get('note')})")
                        if doc.get("note") == "missing":
                            missing_docs.append(doc.get("name") or Path(doc_path).stem)

        untracked_docs: list[Path] = []
        if desk_dir.exists():
            ignored_modeled_names = {
                "Board.md",
                "pills.md",
                "execution.md",
                "testing.md",
                "closeout.md",
                "phase.md",
                "README.md",
                "tag-namespaces.yaml",
            }
            modeled_mds = {
                path.resolve()
                for path in modeled_desk_markdown_docs(root, desk_dir)
                if path.name not in ignored_modeled_names
                and not _is_task_file(desk_dir, path)
            }
            untracked_docs = [p for p in modeled_mds if p not in tracked_mds]

        pending_local_types = pending_local_task_type_models(root)
        pending_migration = pending_task_type_migration(root)

        if not legacy_pending and not legacy_faq_pending and not missing_store and not missing_desk_files and not unregistered_models and not copied_models and not untracked_docs and not invalid_docs and not moved_contracts and not pending_local_types and not pending_migration:
            print("Desk is up to date.")
            return 0

        print("Desk divergence report:")
        if missing_store:
            print("- Missing store: .sldb")
        if legacy_faq_pending:
            print(
                f"- Legacy FAQ model: {LEGACY_FAQ_MODEL} ({LEGACY_FAQ_MODEL_REF}) should be {FAQ_MODEL}."
            )
        if moved_contracts:
            print(f"- Moved model contracts: {', '.join(moved_contracts)}")
        if legacy_pending and legacy is not None:
            print(
                "- Legacy task lifecycle: "
                f"{len(legacy.primitive_docs)} routine/primitive documents to delete, "
                f"{len(legacy.tasks_to_rewrite)} tasks to rewrite, "
                f"lifecycle graph {'missing' if legacy.graph_missing else 'present'}, "
                f"retired models still registered: {', '.join(legacy.registered_legacy_models) or 'none'}"
            )
        if missing_desk_files:
            print(f"- Missing desk structure: {', '.join(missing_desk_files)}")
        if unregistered_models:
            print(f"- Unregistered models: {', '.join(unregistered_models)}")
        if copied_models:
            print(f"- Copied deskops models: {', '.join(copied_models)}")
        if untracked_docs:
            rel_untracked = [str(p.relative_to(root)) for p in untracked_docs]
            print(f"- Untracked desk documents: {', '.join(rel_untracked)}")
        if pending_local_types:
            print(f"- Unregistered desk-local task types: {', '.join(pending_local_types)}")
        if pending_migration:
            print(f"- Pending task type migration: {len(pending_migration)} task(s)")
        if invalid_docs:
            print(f"- Stale document hashes: {', '.join(invalid_docs)}")

        if not apply:
            print("\nRun with --apply to repair these issues.")
            return 1

        print("\nApplying repairs...")
        
        if missing_desk_files:
            scaffold_desk(root)
            print("Scaffolded missing desk structure.")

        if unregistered_models or copied_models:
            bootstrap.init_local_store(root)
            print("Registered missing models and converted copied deskops models.")

        try:
            for change in register_local_task_type_models(root):
                print(f"- {change}")
        except Exception as exc:
            print(f"Error: {exc}")
            return 1
        for change in migrate_task_types(root):
            print(f"- {change}")

        if untracked_docs:
            pythonpath = package_pythonpath()
            for p in untracked_docs:
                model = guess_model_for_path(desk_dir, p)
                if model:
                    try:
                        doc_io.track(
                            root,
                            p,
                            model,
                            name=p.stem,
                            pythonpath=pythonpath,
                        )
                        print(f"Tracked {p.relative_to(root)} as {model.__name__}.")
                    except Exception as e:
                        print(f"Failed to track {p.relative_to(root)}: {e}")
                else:
                    print(f"Could not guess model for {p.relative_to(root)}.")

        if missing_docs:
            # A tracked document whose file is gone must be untracked, not
            # re-indexed: the store would keep describing something that is not there.
            pythonpath = package_pythonpath()
            for name in missing_docs:
                try:
                    doc_io.untrack(root, name, pythonpath=pythonpath)
                    print(f"Untracked {name}: its file is gone.")
                except Exception as e:
                    print(f"Failed to untrack {name}: {e}")

        if invalid_docs:
            pythonpath = package_pythonpath()
            doc_io.update_store_indexes_in(root, pythonpath=pythonpath, wait=False)
            print("Updated store derived indexes.")

        if store_dir.exists():
            from deskops.lifecycle import ensure_lifecycle_graph
            from deskops.lifecycle import lifecycle_graph_present

            if not lifecycle_graph_present(root):
                for change in ensure_lifecycle_graph(root):
                    print(f"Lifecycle graph: {change}")

        return 0

FILE:deskops/cli/commands/doctor.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.doctor_findings import REGISTER, Findings, moved_documents, print_findings, read_store_check
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk


_IGNORED_MODELED_NAMES = {
    "Board.md",
    "pills.md",
    "execution.md",
    "testing.md",
    "closeout.md",
    "phase.md",
    "README.md",
    "tag-namespaces.yaml",
}


class DoctorCLI:
    """Report what breaks the desk (errors) apart from what only moved (alerts).

    Exit 1 only when an error is left; alerts alone exit 0 and are always printed. `--repair`
    acts on errors only: an alert is not damage, it is registered with `deskops desk update
    --apply`. See `deskops.doctor_findings`.
    """

    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        repair = getattr(args, "repair", False)
        inspection = inspect_desk(root)
        desk_dir = root / "desk"
        if inspection.classification == "absent" and not (desk_dir / "config.json").exists():
            print(f"No desk at {root}: this repository has no desk/ (run deskops init to create one).")
            return 0
        findings = Findings()
        self._check_structure(root, desk_dir, inspection, repair, findings)
        if desk_dir.exists():
            self._check_documents(root, desk_dir, repair, findings)
            self._check_models(root, repair, findings)
        return self._report(findings, repair)

    def _check_structure(self, root: Path, desk_dir: Path, inspection, repair: bool, findings: Findings) -> None:
        missing = [rel for rel, exists in (
            ("desk/tasks/Board.md", (desk_dir / "tasks" / "Board.md").exists()),
            ("desk/drawer/", (desk_dir / "drawer").exists()),
            ("desk/rituals/phase.md", (desk_dir / "rituals" / "phase.md").exists()),
        ) if desk_dir.exists() and not exists]
        if missing and repair:
            scaffold_desk(root)
            findings.fixed.append(f"Scaffolded missing desk/ structure: {', '.join(missing)}")
        elif missing:
            findings.errors.append(f"Missing desk structure: {', '.join(missing)}")
        if inspection.classification == "legacy":
            surfaces = [*inspection.missing_surfaces, *inspection.malformed_surfaces]
            findings.errors.append(
                "Legacy desk detected: "
                + (", ".join(surfaces) if surfaces else "board/task/pill surfaces need explicit migration")
                + ". Migrate with: deskops desk migrate --root <repo>."
            )

    def _check_documents(self, root: Path, desk_dir: Path, repair: bool, findings: Findings) -> None:
        payload = self._store_check(root, findings)
        if payload is None:
            return
        docs = read_store_check(root, payload)
        modeled = {p.resolve() for p in modeled_desk_markdown_docs(root, desk_dir) if p.name not in _IGNORED_MODELED_NAMES}
        untracked = sorted(p for p in modeled if p not in docs.tracked)
        moves, gone, untracked = moved_documents(root, docs.missing, untracked)
        findings.alerts += [f"Edited: {d}" for d in docs.changed]
        findings.alerts += [f"Moved: {m}" for m in moves]
        findings.alerts += [f"Not tracked yet: {p.relative_to(root)}" for p in untracked]
        findings.alerts += docs.store_alerts
        findings.errors += [f"Tracked document is gone: {p.relative_to(root)} (restore it, or untrack it with {REGISTER})" for p in gone]
        findings.errors += [f"Invalid desk document: {d}" for d in docs.unknown]
        findings.errors += docs.store_errors
        findings.errors += self._unreadable(root, docs.by_model)

    def _store_check(self, root: Path, findings: Findings) -> dict | None:
        result = subprocess.run(
            [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb"), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not result.stdout:
            if result.returncode != 0:
                first = result.stderr.strip().split("\n")[0]
                findings.errors.append(f"SLDB store check crashed (likely malformed documents): {first}")
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            findings.errors.append("Failed to parse SLDB store check output.")
            return None

    def _unreadable(self, root: Path, by_model: list[tuple[str | None, Path]]) -> list[str]:
        """Documents whose model cannot read their own content: an edit through the model erases it."""
        out = []
        for model_name, doc_path in by_model:
            model = _resolve_deskops_model(model_name)
            if model is None or not doc_path.exists():
                continue
            if fields := is_unreadable_by_model(model, doc_path.read_text(encoding="utf-8")):
                out.append(
                    f"Model cannot read its own document: {doc_path.relative_to(root)} ({model_name}: {', '.join(fields)}). "
                    "Any edit through the model renders these fields back empty; rebuild the text through sldb and retrack it."
                )
        return out

    def _check_models(self, root: Path, repair: bool, findings: Findings) -> None:
        store_dir = root / ".sldb"
        if not store_dir.exists():
            return
        try:
            registered = SLDBBootstrap()._registered_model_names(store_dir)
        except Exception:
            findings.errors.append("Could not read the local .sldb store index; unregistered-model check skipped.")
            return
        if not (unregistered := sorted(name for name in MODEL_REFS if name not in registered)):
            return
        if repair and self._register_models(root):
            findings.fixed.append(f"Registered missing models: {', '.join(unregistered)}")
        else:
            findings.errors.append(f"Unregistered models: {', '.join(unregistered)}. Register them with {REGISTER}.")

    def _register_models(self, root: Path) -> bool:
        try:
            return SLDBBootstrap().init_local_store(root) == 0
        except Exception:
            return False

    def _report(self, findings: Findings, repair: bool) -> int:
        if not findings.errors and not findings.alerts and not findings.fixed:
            print("Desk is healthy. No issues found.")
            return 0
        print_findings(findings, repair=repair)
        if not findings.errors:
            print(f"\nDesk is healthy{f', with {len(findings.alerts)} alert(s)' if findings.alerts else ''}.")
            return 0
        return 1


def _resolve_deskops_model(name: str | None) -> type | None:
    """The deskops model registered under `name`, or None when it is not ours."""
    if not name:
        return None
    import deskops.models as models

    candidate = getattr(models, name, None)
    return candidate if isinstance(candidate, type) else None

FILE:deskops/bootstrap.py
from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

from sldb import StructuredNLDoc

from deskops import doc_io
from deskops import models as deskops_models
from deskops.paths import package_pythonpath


DESKOPS_STORE_LINK = "deskops"

#: Base classes that are never registered as models in a store.
BASE_MODEL_NAMES = frozenset({"PrimitiveDoc", "OperationalArtifactDoc"})

#: Every deskops model is inherited from the owner store by name and model ref.
MODEL_REFS = {
    name: f"deskops.models:{name}"
    for name in deskops_models.__all__
    if name not in BASE_MODEL_NAMES
    and isinstance(getattr(deskops_models, name, None), type)
    and issubclass(getattr(deskops_models, name), StructuredNLDoc)
}


class SLDBBootstrap:
    def ensure_sldb_available(self, *, allow_install: bool = False) -> int:
        """Check that sldb is importable.

        Only ``deskops bootstrap`` and ``deskops init`` may install it; every other
        command fails with the install hint instead of running pip behind the user's back.
        """
        if self._sldb_importable():
            if shutil.which("sldb") is None:
                print("sldb is importable but no shell entrypoint was found; using python -m sldb.")
            return 0

        if not allow_install:
            print(
                "Error: sldb is not installed. Run 'deskops bootstrap' or 'deskops init' to install it."
            )
            return 1

        install_path = self._resolve_sldb_checkout()
        if install_path is None:
            print("Error: sldb is not installed and no sibling checkout was found.")
            print(
                "Set DESKOPS_SLDB_PATH or keep the sibling checkout at ../sldb before running deskops init."
            )
            return 1
        print(f"Installing sldb from {install_path}...")
        try:
            self._run([
                sys.executable,
                "-m",
                "pip",
                "install",
                "-e",
                str(install_path),
            ])
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1
        importlib.invalidate_caches()

        return 0

    def ensure_machine_ready(self) -> int:
        ready = self.ensure_sldb_available(allow_install=True)
        if ready != 0:
            return ready

        return self.ensure_global_store_and_models()

    def default_pythonpath(self) -> str:
        return package_pythonpath()

    def ensure_global_store_and_models(self) -> int:
        global_store = Path.home() / ".sldb"
        if not global_store.exists():
            print(f"Initializing global store at {global_store}...")
            try:
                self._init_store(Path.home())
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        result = self._register_models(global_store)
        if result != 0:
            return result

        print("Global deskops model registry is ready.")
        return 0

    def init_local_store(self, target_path: Path) -> int:
        local_store = target_path / ".sldb"
        if local_store.exists():
            print(f"Local store already exists at {local_store}.")
        else:
            print(f"Initializing local store at {local_store}...")
            try:
                self._init_store(target_path)
            except RuntimeError as exc:
                print(f"Error: {exc}")
                return 1

        return self._register_models(local_store)

    def _register_models(self, store_path: Path) -> int:
        """Link the deskops owner store and inherit the model set from it.

        A model registered here as a copy of the deskops class is converted in place by
        `inherit_model`, keeping its documents and signed contract. A regular (non-editable)
        install ships no owner store, so the models are registered directly from the
        installed package instead.
        """
        try:
            owner = self._deskops_owner_store()
            if owner is None:
                self._register_models_directly(store_path)
            else:
                link_state = self._ensure_owner_link(store_path, owner)
                if link_state is None:
                    # The name is already taken by another checkout. sldb cannot replace a
                    # link, so leave this store as it is instead of inheriting from it.
                    print(
                        f"Skipping model registration in {store_path}: '{DESKOPS_STORE_LINK}' is linked elsewhere."
                    )
                    return 0
                if link_state:
                    print(f"Linked {owner} as {DESKOPS_STORE_LINK} in {store_path}.")

                entries = self._registered_model_entries(store_path)
                for model_name, model_ref in MODEL_REFS.items():
                    entry = entries.get(model_name)
                    if entry is not None:
                        origin = getattr(entry, "origin", None)
                        if origin == DESKOPS_STORE_LINK:
                            continue
                        if origin or getattr(entry, "model_ref", None) != model_ref:
                            continue
                    print(f"Inheriting {model_name} in {store_path}...")
                    self._inherit_model(model_name, store_path)

            self._init_relations(store_path)
            self._update_store_indexes(store_path)
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1

        return 0

    def _register_models_directly(self, store_path: Path) -> None:
        """Register the deskops models as copies when no owner store is installed."""
        owner = Path(package_pythonpath()) / ".sldb"
        print(
            f"No deskops owner store at {owner}; registering the models directly from the installed package."
        )
        entries = self._registered_model_entries(store_path)
        for model_name, model_ref in MODEL_REFS.items():
            if model_name in entries:
                continue
            print(f"Registering {model_name} in {store_path}...")
            self._register_model(model_ref, store_path)

    def _register_model(self, model_ref: str, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.register_model(store_path.parent, model_ref, pythonpath=package_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "models",
                "add",
                model_ref,
                "--store",
                str(store_path),
                "--pythonpath",
                package_pythonpath(),
            ])

    def _deskops_owner_store(self) -> Path | None:
        owner = Path(package_pythonpath()) / ".sldb"
        return owner if owner.exists() else None

    def _ensure_owner_link(self, store_path: Path, owner: Path) -> bool | None:
        """Link `owner` as `deskops`, repairing a broken link to it.

        Returns True when the link was added or repaired, False when it already points at
        `owner`, and None when the name is linked to a healthy different store (or the
        installed sldb cannot replace a link).
        """
        if self._sldb_importable():
            from sldb.api import store_links

            try:
                existing = next(
                    (link for link in store_links(store_path) if link["name"] == DESKOPS_STORE_LINK),
                    None,
                )
                if existing is not None:
                    target = Path(existing["resolved"])
                    if target == owner.resolve():
                        return False
                    if existing["status"] != "ok" and self._link_store_supports_replace():
                        doc_io.link_store_alias(
                            store_path.parent, owner, DESKOPS_STORE_LINK, replace=True
                        )
                        print(
                            f"Replaced broken '{DESKOPS_STORE_LINK}' link to {target} with {owner}."
                        )
                        return True
                    print(
                        f"Warning: {store_path} already links '{DESKOPS_STORE_LINK}' to {target}, "
                        f"not to {owner}."
                    )
                    return None
                doc_io.link_store_alias(store_path.parent, owner, DESKOPS_STORE_LINK)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            existing = self._store_link_names(store_path)
            if DESKOPS_STORE_LINK in existing:
                return False
            self.run_sldb([
                "stores",
                "add",
                str(owner),
                "--name",
                DESKOPS_STORE_LINK,
                "--store",
                str(store_path),
            ])
        return True

    def _inherit_model(self, model_name: str, store_path: Path) -> None:
        ref = f"{DESKOPS_STORE_LINK}:{model_name}"
        if self._sldb_importable():
            try:
                doc_io.inherit_model_from(store_path.parent, ref, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "models",
                "inherit",
                ref,
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _init_relations(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_relations_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb([
                "edges",
                "init",
                "--store",
                str(store_path),
                "--pythonpath",
                self.default_pythonpath(),
            ])

    def _update_store_indexes(self, store_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.update_store_indexes_in(store_path.parent, pythonpath=self.default_pythonpath())
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "update", "--store", str(store_path)])

    def run_sldb(self, args: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        return self._run([sys.executable, "-m", "sldb", *args], capture_output=capture_output)

    def _init_store(self, target_path: Path) -> None:
        if self._sldb_importable():
            try:
                doc_io.init_store_at(target_path)
            except Exception as exc:
                raise RuntimeError(str(exc))
        else:
            self.run_sldb(["stores", "init", "--path", str(target_path)])

    def _registered_model_entries(self, store_path: Path) -> dict[str, Any]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {m.name: m for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"]: entry for entry in payload.get("models", [])}

    def _store_link_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index

            try:
                idx = load_store_index(store_path)
                return {link.name for link in idx.stores}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["stores", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("stores", [])}

    def _registered_model_names(self, store_path: Path) -> set[str]:
        if self._sldb_importable():
            from sldb.store.io import load_store_index
            try:
                idx = load_store_index(store_path)
                return {m.name for m in idx.models}
            except Exception as exc:
                raise RuntimeError(str(exc))

        result = self.run_sldb(
            ["models", "list", "--store", str(store_path), "--format", "json"],
            capture_output=True,
        )
        payload = json.loads(result.stdout or "{}")
        return {entry["name"] for entry in payload.get("models", [])}

    def _link_store_supports_replace(self) -> bool:
        """Whether the installed sldb's `link_store` can re-point an existing link."""
        from inspect import signature

        from sldb.api import link_store

        return "replace" in signature(link_store).parameters

    def _sldb_importable(self) -> bool:
        return importlib.util.find_spec("sldb") is not None

    def _resolve_sldb_checkout(self) -> Path | None:
        candidates: list[Path] = []
        env_path = (os.environ.get("DESKOPS_SLDB_PATH") or "").strip()
        if env_path:
            candidates.append(Path(env_path).expanduser())

        package_root = Path(package_pythonpath())
        repo_root = package_root.parent
        candidates.append(repo_root.parent / "sldb")
        candidates.append(Path.cwd().resolve().parent / "sldb")

        seen: set[Path] = set()
        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            if (resolved / "pyproject.toml").exists() and (resolved / "src" / "sldb").exists():
                return resolved
        return None

    def _run(self, command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            capture_output=capture_output,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "command failed").strip()
            raise RuntimeError(detail)
        return result

FILE:pyproject.toml
[project]
name = "deskops"
version = "0.2.0"
description = "Workflow-domain layer for the hum-ecosystem"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pydantic>=2.0",
    "PyYAML>=6.0",
    "structuredLanguageDB>=0.1.13",
]

[project.scripts]
deskops = "deskops.cli.main:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["deskops*"]

[tool.setuptools.package-data]
deskops = ["spec/**/*.yaml", "data/faq.md"]

[tool.pytest.ini_options]
pythonpath = ["."]
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]

FILE:tests/test_desk_sync.py
import json
import pytest
from pathlib import Path
from sldb.api.stores.init_store import init_store
from sldb.cli.commands.model import ModelCLI
from deskops.cli.main import CLI
from deskops.workspace import scaffold_desk
from sldb.api.documents.track_document_file import track_document_file
import yaml
from types import SimpleNamespace
from deskops.bootstrap import SLDBBootstrap

def test_desk_update_command(tmp_path: Path):
    # Setup desk
    cli = CLI()
    assert cli.run(["init", str(tmp_path)]) == 0

    desk_dir = tmp_path / "desk"
    store_dir = tmp_path / ".sldb"

    # Create untracked file
    untracked_path = desk_dir / "tasks" / "task-untracked.md"
    untracked_path.write_text("---\nid: task-untracked\nstatus: active\ntags: []\n---\n# Untracked\n\n## Rationale\n\n## Goal\n")

    # Create tracked file then modify it to make hash stale
    tracked_path = desk_dir / "tasks" / "task-stale.md"
    tracked_path.write_text("---\nid: task-stale\nstatus: active\ntags: []\n---\n# Stale\n\n## Rationale\n\n## Goal\n")
    track_document_file(
        store_dir, "TaskDoc", tracked_path, name="task-stale",
        pythonpath=str(Path(__file__).resolve().parents[1]), force=True
    )
    tracked_path.write_text("---\nid: task-stale\nstatus: active\ntags: []\n---\n# Stale modified\n\n## Rationale\n\n## Goal\n")

    # Unregister a model
    store_idx = store_dir / "core" / "store_index.yaml"
    if not store_idx.exists():
        # Maybe it's json? No, sldb uses yaml for store_index now. 
        # But if not, we can just use bootstrap logic.
        store_idx = store_dir / "index.json"
    if store_idx.exists():
        if store_idx.suffix == ".yaml":
            with open(store_idx) as f: data = yaml.safe_load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: yaml.safe_dump(data, f)
        else:
            with open(store_idx) as f: data = json.load(f)
            data["models"] = [m for m in data["models"] if m["name"] != "DeskFAQDoc"]
            with open(store_idx, "w") as f: json.dump(data, f)

    # Test update (dry run)
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 1

    # Test update apply
    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    # Ensure it's clean now
    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0



def test_desk_update_untracks_a_document_whose_file_is_gone(tmp_path: Path) -> None:
    """A deleted file must be untracked, not re-indexed.

    `git rm` on a tracked document leaves the store describing something that is
    not there, and neither 'stores update' nor an index rebuild clears it.
    """
    from deskops.cli.main import main
    from sldb.store.diagnostics import diagnose_store
    from sldb.api.model_registry.model_reference import resolve_model_ref

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        ["add", "atom", "--root", str(tmp_path), "--title", "Gone soon",
         "--five-wh-one-plus", "what", "--answer", "Answered."]
    ) == 0

    atom = tmp_path / "desk" / "atoms" / "atom-gone-soon.md"
    assert atom.exists()
    atom.unlink()

    assert main(["desk", "update", "--root", str(tmp_path)]) != 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0

    diagnosis = diagnose_store(
        tmp_path / ".sldb", resolve_model_ref, project_root=tmp_path, pythonpath=str(tmp_path)
    )
    notes = [doc.note.value for model in diagnosis.models for doc in model.documents]
    assert "missing" not in notes


def test_desk_update_apply_on_a_fresh_repo_writes_the_lifecycle_graph(tmp_path: Path, capsys) -> None:
    """One --apply on a fresh repo must leave a desk that the next update calls up to date."""
    cli = CLI()

    assert cli.run(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    assert cli.run(["desk", "update", "--root", str(tmp_path)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out


def _make_faq_model_legacy(root: Path) -> None:
    """Rewrite the store as it looked when the deskops FAQ model was still `FAQDoc`."""
    store = root / ".sldb"
    index_path = store / "core" / "store_index.yaml"
    index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    entry = next(model for model in index["models"] if model["name"] == "DeskFAQDoc")
    entry["name"] = "FAQDoc"
    entry["model_ref"] = "deskops.models:FAQDoc"
    entry["models_index"] = ".sldb/core/models/FAQDoc.yaml"
    index_path.write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")

    models_dir = store / "core" / "models"
    (models_dir / "DeskFAQDoc.yaml").rename(models_dir / "FAQDoc.yaml")
    model_index_path = models_dir / "FAQDoc.yaml"
    model_index = yaml.safe_load(model_index_path.read_text(encoding="utf-8"))
    model_index["name"] = "FAQDoc"
    model_index["model_ref"] = "deskops.models:FAQDoc"
    model_index["documents_index"] = ".sldb/core/documents/FAQDoc.yaml"
    model_index["sections_index"] = ".sldb/runtime/sections/FAQDoc.yaml"
    model_index_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")

    documents_dir = store / "core" / "documents"
    (documents_dir / "DeskFAQDoc").rename(documents_dir / "FAQDoc")


def test_desk_update_apply_migrates_the_legacy_faq_model(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.api import describe_model

    assert main(["init", str(tmp_path)]) == 0
    assert main(
        [
            "add",
            "faq-doc",
            "--root",
            str(tmp_path),
            "--title",
            "Legacy FAQ",
            "--body",
            "Question?\n\nAnswer.",
        ]
    ) == 0
    faq_path = tmp_path / "desk" / "faq" / "faq-legacy-faq.md"
    original = faq_path.read_bytes()
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()
    _make_faq_model_legacy(tmp_path)

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Legacy FAQ model" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    names = {
        model["name"]
        for model in yaml.safe_load(
            (tmp_path / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8")
        )["models"]
    }
    assert "DeskFAQDoc" in names
    assert "FAQDoc" not in names

    documents = describe_model(
        tmp_path / ".sldb",
        "DeskFAQDoc",
        pythonpath=str(Path(__file__).resolve().parents[1]),
    ).documents
    assert [document.name for document in documents] == ["faq-legacy-faq"]
    assert faq_path.read_bytes() == original

    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_desk_update_does_not_call_the_owner_store_models_copies(tmp_path: Path, monkeypatch, capsys) -> None:
    from deskops.bootstrap import SLDBBootstrap
    from deskops.cli.main import main

    # Without an owner store, init registers the models directly, which is the
    # shape of the deskops owner store itself.
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    assert main(["init", str(tmp_path)]) == 0
    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    other = tmp_path.parent / f"{tmp_path.name}-owner" / ".sldb"
    other.mkdir(parents=True)
    capsys.readouterr()

    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: other)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" in capsys.readouterr().out, "another store's direct models are copies"

    owner = tmp_path / ".sldb"
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: owner)
    main(["desk", "update", "--root", str(tmp_path)])
    assert "Copied deskops models" not in capsys.readouterr().out
def test_desk_update_apply_resigns_a_moved_model_contract(tmp_path: Path, capsys) -> None:
    from deskops.cli.main import main
    from sldb.store.hashing import hash_model_contract
    from deskops.models import RitualDoc

    assert main(["init", str(tmp_path)]) == 0
    model_path = tmp_path / ".sldb" / "core" / "models" / "RitualDoc.yaml"
    model_index = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    model_index["contract_hash"] = "0" * 64
    model_path.write_text(yaml.safe_dump(model_index, sort_keys=False), encoding="utf-8")
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(tmp_path)]) == 1
    assert "Moved model contracts: RitualDoc" in capsys.readouterr().out

    assert main(["desk", "update", "--root", str(tmp_path), "--apply"]) == 0
    capsys.readouterr()

    resigned = yaml.safe_load(model_path.read_text(encoding="utf-8"))
    assert resigned["contract_hash"] == hash_model_contract(RitualDoc)
    assert main(["desk", "update", "--root", str(tmp_path)]) == 0


def test_guess_model_treats_extra_boards_in_tasks_as_boards(tmp_path: Path) -> None:
    """`deskops add board` writes `board-<slug>.md` next to Board.md (ARTIFACT_PATHS puts boards in
    tasks/); tracking it as a TaskDoc fails validation (no `status`) and breaks `desk update --apply`."""
    from deskops import models
    from deskops.cli.commands.desk import guess_model_for_path

    desk = tmp_path / "desk"
    assert guess_model_for_path(desk, desk / "tasks" / "Board.md") is models.BoardDoc
    assert guess_model_for_path(desk, desk / "tasks" / "board-compromisos-26-10.md") is models.BoardDoc
    assert guess_model_for_path(desk, desk / "tasks" / "task-doc-7.md") is models.TaskDoc

FILE:tests/test_packaging.py
from __future__ import annotations

from pathlib import Path

from deskops import paths
from deskops.bootstrap import MODEL_REFS
from deskops.bootstrap import SLDBBootstrap


def test_package_pythonpath_is_the_directory_containing_deskops() -> None:
    package_parent = Path(paths.package_pythonpath())

    assert (package_parent / "deskops" / "paths.py").is_file()
    assert SLDBBootstrap().default_pythonpath() == paths.package_pythonpath()


def test_runtime_specs_and_faq_ship_inside_the_package() -> None:
    assert paths.data_path("spec", "workflows", "task_lifecycle.yaml").is_file()
    assert paths.data_path("data", "faq.md").is_file()
    # Artifact and field specs are the models now (``__artifact__`` and the fields).
    assert not paths.data_path("spec", "artifacts").exists()
    assert not paths.data_path("spec", "fields").exists()


def test_packaged_faq_matches_the_human_copy() -> None:
    repo_faq = Path(__file__).resolve().parents[1] / "docs" / "faq.md"

    assert paths.data_path("data", "faq.md").read_text(encoding="utf-8") == repo_faq.read_text(encoding="utf-8")


def test_register_models_falls_back_when_no_owner_store_is_installed(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    root = tmp_path / "repo"
    root.mkdir()

    assert SLDBBootstrap().init_local_store(root) == 0

    from sldb.store.io import load_store_index

    entries = {entry.name: entry for entry in load_store_index(root / ".sldb").models}
    for name, model_ref in MODEL_REFS.items():
        assert entries[name].origin is None
        assert entries[name].model_ref == model_ref
    assert "registering the models directly" in capsys.readouterr().out


def test_desk_update_is_clean_with_directly_registered_models(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(SLDBBootstrap, "_deskops_owner_store", lambda self: None)
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()

    assert main(["desk", "update", "--root", str(root)]) == 0
    assert "Desk is up to date." in capsys.readouterr().out

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.

### Changed

- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.

### Fixed

- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Golden del scaffold capturado en el primer commit con el código de main (c3): tests/fixtures/golden/scaffold/init.json y update.json, y tests/test_scaffold_golden.py verde antes y después
- grep -rn '_write_if_missing\|scaffold_desk\|guess_model_for_path\|_template(' deskops/ vacío
- segunda corrida de desk update --apply sin cambios (test)
- desk update en dry-run sobre una copia del desk de deskops bajo /dev/shm sin cambios nuevos (c7)
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_scaffold_golden, test_desk_sync, test_packaging, test_lifecycle_graph, test_doctor_*, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- wc -l deskops/workspace.py antes (885) y después
- CHANGELOG

