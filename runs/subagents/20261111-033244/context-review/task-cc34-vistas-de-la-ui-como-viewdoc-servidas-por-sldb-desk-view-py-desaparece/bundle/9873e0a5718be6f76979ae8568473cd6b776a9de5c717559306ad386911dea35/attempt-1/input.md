FILE:desk/tasks/task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece.md
---
sldb:
  by: agent
  at: '2026-11-11T03:32:05Z'
  authority: generated
  via: save_document_payload
id: task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/desk_view.py
- deskops/data/views/
- deskops/data/desk_declaration.yaml
- deskops/cli/commands/view.py
- deskops/runtime/
- deskops/operations.py
- deskops/domain_tree.py
- tests/
- tests/fixtures/golden/output/
- docs/deskops-ui.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC34: Vistas de la UI como ViewDoc servidas por sldb; desk_view.py desaparece

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC34 del plan deskops-como-config. Depende de CC33 (CC33a, CC33b y CC33c cerrados) y CC36 (cerrado). Gates G_GD25 y G_GD21 satisfied. Toca también graph_ui (UIs/graph_ui).

## Goal

_Describe the concrete result this task must produce._

deskops view board|task|drawer|inbox sale de sldb.api.run_view sobre ViewDocs semilla del paquete, con el mismo JSON que hoy salvo revision; graph_ui lee esas vistas sin importar DeskView; desk_view.py y sus helpers se borran.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/desk_view.py, deskops/data/views/, deskops/data/desk_declaration.yaml, deskops/cli/commands/view.py, deskops/runtime/, deskops/operations.py, tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md; en graph_ui: frontends/desk/serve.py, frontends/mindmap/deskops_routes.py, tests/. Fuera: proveedores computed (DA1) y carpeta desk/views (DA4).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml, CC34). SCOPE: Primer paso: capturar goldens JSON de deskops view board|task|drawer|inbox sobre un desk de prueba fijo (no existen hoy en tests/fixtures/golden/output/). ViewDocs semilla (deskops/data/views/: board, task, drawer, inbox) que reproducen el contrato de docs/deskops-ui.md (CONTRACT_VERSION 1): board = sección de tareas del Board agrupadas por current_node en el orden de los RitualDoc del ciclo de vida, con transitions (holding/blocked de GO08/GO09), rules (findings de las reglas de CC32/CC33) y edges (pills, atoms); task = una tarea por {id} con sus campos y next; drawer = selector por path_glob desk/drawer/tasks/*.md; inbox = notas del inbox. Sin proveedores computed (DA1): los hechos de git del closeout llegan a la vista como recibos ReviewDoc kind evidence de CC33 que la ViewDoc lee por edges o rules; lo que no es documento ni recibo (agents de Herdr, runtime/, P4) lo agrega deskops view sobre el resultado de run_view en el CLI, y graph_ui lo pide a deskops en proceso como las acciones (DP4); ningún agregado reimplementa una regla. deskops view <x> = sldb.api.run_view + el render_text actual (se conserva en el CLI); revision del payload = ETag de GD25 (los valores cambian, la clave y su semántica de guarda optimista no). Se borran services/desk_view.py, task_revision/note_revision y los alias privados de la fachada que CC30 conservó para graph_ui. graph_ui (repo aparte, UIs/graph_ui): GET /api/view/<view> lee GET /views/<view> de sldb serve (proxy o cliente directo, con ETag) en lugar de importar DeskView; deskops_routes.py deja de usar ops._read_doc/_resolve_glob/show_task y lee la vista task; las acciones siguen por el CLI de deskops en proceso (DP4); su guarda de revisión usa el ETag. Las ViewDocs viven solo como semillas del paquete deskops, sin carpeta desk/views/ (DA4); sldb serve las encuentra por un store de deskops enlazado.

ACCEPTANCE: deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados en el primer paso salvo el valor de revision; ayuda de view idéntica; GET /views/board de sldb serve sobre el desk de prueba devuelve el mismo payload; graph_ui sirve la vista board leyendo de sldb serve (test en graph_ui) y POST /api/desk/advance con un ETag viejo da 409; tests/test_desk_view.py reescrito sobre run_view y verde; grep de "desk_view\|DeskView" en deskops/ y en UIs/graph_ui/frontends vacío; deskops view board en los 6 desks responde; tiempo frío/caliente de view board sobre el desk real de deskops registrado (meta caliente < 1 s, la verifica CC52); CHANGELOG; docs/deskops-ui.md.

OUTPUT_SCOPE: deskops/services/desk_view.py (borrado), deskops/data/views/, deskops/cli/commands/view.py, deskops/runtime/ (agents en el CLI), deskops/operations.py (alias privados), tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md, UIs/graph_ui/frontends/desk/serve.py, UIs/graph_ui/frontends/mindmap/deskops_routes.py, UIs/graph_ui/tests/

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

PRECISIONES DE PROMOCIÓN (2026-11-11, coordinador del plan; base origin/main b990c49e, con CC33 y CC36 cerrados; decisiones revisables):
a1 (lo que hay hoy): deskops/services/desk_view.py (543 líneas): DeskView, CONTRACT_VERSION = 1, task_revision (:40), note_revision (:48), RUN_INDEX y los agents de herdr. graph_ui lo importa en frontends/desk/serve.py (from deskops.services.desk_view import DeskView, DeskViewError). sldb expone sldb.api.run_view y list_views (GD25).
a2 (dos repos, orden de integración): el nodo toca deskops y graph_ui. Para no romper graph_ui en ningún punto, el orden es:
1. graph_ui deja de importar DeskView y lee la vista nueva (deskops view <x> --format json en proceso, o GET /views/<x> de sldb serve con ETag). Va en una rama wt/ de graph_ui creada desde su master después de que entre la integración wt/deskops-ui.
2. deskops borra desk_view.py.
Entregas: rama wt/cc34 en deskops y rama wt/cc34-ui en graph_ui. El coordinador integra primero graph_ui y después deskops, y el CI de cada repo corre contra el main del otro. Si con eso un paso intermedio queda rojo, el worker para y avisa con la propuesta.
a3 (goldens primero): antes de cambiar nada, deskops view board|task|drawer|inbox --format json se captura en tests/fixtures/golden/output/ sobre un desk de prueba fijo (tmp_path con contenido determinista, sin fechas ni hashes variables salvo revision). Ese commit va solo. La aceptación compara contra esos goldens salvo el valor de revision.
a4 (agents y lo que no es documento): lo que no es documento ni recibo (agents de herdr, runs/subagents/index.jsonl) lo suma el CLI de deskops view sobre el resultado de run_view (DA1, DP4). No hay proveedor computed en sldb. Ningún agregado reimplementa una regla.
a5 (ETag): revision del payload = ETag de GD25. La clave revision y su guarda optimista no cambian; el valor sí. POST /api/desk/advance de graph_ui con un ETag viejo da 409 (test en graph_ui).
a6 (DA4): las ViewDoc viven solo como semillas en deskops/data/views/, sin carpeta desk/views/. sldb serve las encuentra por el store de deskops enlazado. Si no las encuentra, hipótesis y nota a sldb.
a7 (files): deskops: deskops/services/desk_view.py (borrado), deskops/data/views/, deskops/data/desk_declaration.yaml (solo si hace falta declarar las ViewDoc), deskops/cli/commands/view.py, deskops/runtime/, deskops/operations.py, tests/, tests/fixtures/golden/output/, docs/deskops-ui.md, CHANGELOG.md. graph_ui: frontends/desk/serve.py, frontends/mindmap/deskops_routes.py, tests/.
a8 (4 pasos): los de deskops (sldb stores build --store .sldb; pytest, un proceso por archivo; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh .) y todos los pasos de .github/workflows/ci.yml de graph_ui, con sus e2e. Los corre el coordinador en clones limpios.

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-11, coordinador del plan; decisiones revisables):
b1 (transporte de graph_ui): un solo transporte, GET /views/<vista> de sldb serve, como cliente directo con If-None-Match/ETag. Si sldb serve no responde, graph_ui devuelve 502 con el mensaje del error. No se usa la vía en proceso por CLI para leer vistas. Las acciones siguen por el CLI de deskops en proceso (DP4).
b2 (enlace del store): el store de graph_ui ya enlaza a deskops (.sldb/store.yaml: links name deskops, path ../../deskops/.sldb). Las ViewDoc semilla de deskops/data/views/ se trackean en el store del propio repo deskops (su .sldb), declaradas con `sldb stores declare --write`, nunca a mano. Así sldb serve sobre cualquier store que enlace a deskops las encuentra. Para los tests de deskops, el desk de prueba se arma igual: un store de prueba que enlaza al store de deskops.
b3 (desk_declaration.yaml): no hace falta tocarlo si b2 alcanza. Queda en files solo como reserva: si el worker lo toca, justifica en el informe por qué b2 no alcanzó.
b4 (forma de la ViewDoc): el modelo es sldb.models.notation.view_doc (GD25). Cada parte del contrato de docs/deskops-ui.md se lee como lo da el modelo: relaciones (pills, atoms) por edges y hallazgos de reglas (CC32/CC33) por rules. La forma de cada ViewDoc sale del contrato y del modelo, no se inventa. Si el modelo no expresa una parte, hipótesis y nota a sldb.
b5 (agregados del CLI): deskops view sobre run_view suma, con las mismas claves y el mismo orden que hoy, lo que no es documento: agents de herdr y runs/subagents/index.jsonl. `deskops view agents` sigue existiendo como hoy (cli/commands/view.py:28) y queda fuera de la comparación con goldens de ViewDoc.
b6 (desk de prueba determinista): una fixture de tests arma el desk en tmp_path con ids, títulos y fechas fijas (created_at por flag o por frontmatter del fixture). Antes de comparar con los goldens, el test normaliza los valores de revision y de fechas a marcadores fijos ('<revision>', '<date>'). inbox entra en los goldens con esa normalización.
b7 (alias privados): se borran los tres de deskops/operations.py:259-272 (_read_doc, _resolve_glob, _registered_repositories) y _repository_root si solo lo usa graph_ui. deskops/domain_tree.py todavía llama a uno: se cambia esa llamada a doc_access directamente (único cambio en domain_tree.py, que se suma a files). graph_ui deja de usarlos (deskops_routes.py).

DISPOSICIÓN DE PREFLIGHT-2 Y BUNDLE-2 (2026-11-11, coordinador del plan; decisiones revisables; mandan sobre a2, b1-b7 y el SCOPE donde difieren):
c1 (orden de integración; reemplaza a2): graph_ui lee las ViewDoc de deskops, así que deskops va primero. wt/cc34 en deskops trae las semillas ViewDoc, deskops view sobre run_view y el borrado de desk_view.py. wt/cc34-ui en graph_ui se verifica contra wt/cc34. El coordinador integra deskops y en seguida graph_ui. Mientras tanto, el master de graph_ui puede quedar rojo unos minutos contra deskops main; se acepta y no hay shim de compatibilidad. wt/cc34-ui parte del master de graph_ui después de que entre la integración wt/deskops-ui.
c2 (transporte, cierra el choque con DP4): graph_ui LEE las vistas por GET /views/<vista> de sldb serve (b1). Las ACCIONES (advance, acknowledge, etc.) siguen por el CLI de deskops en proceso (DP4). La frase del SCOPE "lo pide a deskops en proceso como las acciones" vale solo para los agregados de b5: agents y runs los pide graph_ui al CLI de deskops en proceso (deskops view agents --format json), no a sldb serve.
c3 (golden de task): el id es el de una tarea fija del desk de prueba de b6, invocado como `deskops view task <id> --format json`. El fixture lo define.
c4 (normalización): se normalizan solo los valores de revision y de fechas, con los marcadores de b6. Todo lo demás se compara igual. "salvo revision" del contrato se lee como revision y fechas.
c5 (6 desks): "responde" quiere decir exit 0, JSON válido con las claves del contrato y sin error. Se registra por desk en el informe.
c6 (GET /views/board): devuelve el resultado de run_view, sin los agregados del CLI de b5. El test lo compara con `deskops view board --format json` quitando esos agregados.
c7 (desk_declaration.yaml): "hace falta" quiere decir que sldb serve sobre el store de prueba enlazado no encuentra las ViewDoc con b2 solo. Si las encuentra, el archivo no se toca.
c8 (tiempo): `time deskops view board --format json` sobre el desk real de deskops, en frío (primera corrida tras borrar .sldb_cache) y en caliente (segunda corrida). Los dos valores van al informe; la meta la verifica CC52.
c9 (alias y agents):
- Inventario de usos con `grep -rn "_read_doc\|_resolve_glob\|_registered_repositories\|_repository_root" deskops/ ~/proyectos/SLDB_1/UIs/graph_ui/frontends`; se borra cada alias sin usos tras el cambio.
- agents() y la lectura de runs pasan de desk_view.py a deskops/runtime/ (agents de herdr) o a cli/commands/view.py, sin cambiar su salida.
- Mapeo campo a campo del contrato (errors, counts, closeout, next, markdown, excerpt, command...): es parte del trabajo. El informe lleva una tabla campo -> fuente (ViewDoc por edges o rules, o agregado del CLI de b5); lo que no tenga fuente en el modelo, hipótesis y nota a sldb.
- revision/ETag: cubre lo que ETag de GD25 cubre para esa vista. Si un cambio del Board ya no invalida la revision de task como hoy (sha256 de Board más tarea), se deja escrito y el test de 409 de graph_ui lo prueba con el cambio que sí la invalida.

## Validation

_List the checks required before this task can close._

- deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados primero (a3), salvo revision
- GET /views/board de sldb serve sobre el desk de prueba da el mismo payload
- graph_ui sirve board leyendo la vista nueva y POST /api/desk/advance con ETag viejo da 409
- grep de desk_view y DeskView vacío en deskops/ y en graph_ui frontends
- deskops view board responde en los 6 desks; tiempo frío y caliente registrado
- 4 pasos de deskops y CI completo de graph_ui en clones limpios

## Done When

_Name the observable condition that makes the task complete._

deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados en el primer paso salvo el valor de revision; ayuda de view idéntica; GET /views/board de sldb serve sobre el desk de prueba devuelve el mismo payload; graph_ui sirve la vista board leyendo de sldb serve (test en graph_ui) y POST /api/desk/advance con un ETag viejo da 409; tests/test_desk_view.py reescrito sobre run_view y verde; grep de "desk_view\|DeskView" en deskops/ y en UIs/graph_ui/frontends vacío; deskops view board en los 6 desks responde; tiempo frío/caliente de view board sobre el desk real de deskops registrado (meta caliente < 1 s, la verifica CC52); CHANGELOG; docs/deskops-ui.md.

FILE:deskops/services/desk_view.py
"""Read-only views of one desk for the deskops UI.

Each view composes existing operations (``show_task``, ``verify_task_closeout``,
``next_action_report``, the drawer and inbox readers, the Herdr runtime and the
run index) into one JSON-ready dict. Nothing here writes: a reference that does
not resolve lands in the view's ``errors`` list with its cause, never as data.

The contract of every view is written in ``docs/deskops-ui.md``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shlex
from typing import Any, Callable

from deskops import doc_access
from deskops import lifecycle
from deskops.models import BoardDoc
from deskops.models import InboxNoteDoc
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations

CONTRACT_VERSION = 1
BOARD_REF = Path("desk") / "tasks" / "Board.md"
RUN_INDEX = Path("runs") / "subagents" / "index.jsonl"
DEFAULT_RUNS_LIMIT = 20
EXCERPT_LINES = 3
_TEMPLATE_HINT = re.compile(r"^_.*_$")
_NOTE_STAMP = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-")


class DeskViewError(RuntimeError):
    """The view cannot be produced at all (no desk, unknown task)."""


def task_revision(board_path: Path, task_path: Path) -> str:
    """The advance guard: sha256 of Board.md bytes, a NUL byte, and the task file bytes.

    Same formula as graph_ui's ``DeskRoutes.detail``.
    """
    return hashlib.sha256(board_path.read_bytes() + b"\0" + task_path.read_bytes()).hexdigest()


def note_revision(path: Path) -> str:
    """The guard for inbox actions: sha256 of the note file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DeskView:
    def __init__(
        self,
        root: Path,
        *,
        operations: DeskopsOperations | None = None,
        runs_limit: int = DEFAULT_RUNS_LIMIT,
        herdr: str = "herdr",
        workers_provider: Callable[[], list[dict[str, Any]]] | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.board_path = self.root / BOARD_REF
        if not self.board_path.is_file():
            raise DeskViewError(f"No desk board at {self.board_path}; run 'deskops init' first.")
        self.ops = operations or DeskopsOperations(self.root)
        self.runs_limit = runs_limit
        self.herdr = herdr
        self._workers_provider = workers_provider
        self._spec = lifecycle.load_lifecycle_spec()

    # ------------------------------------------------------------ helpers
    def _rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    @staticmethod
    def _error(errors: list[dict[str, str]], reference: str, cause: str, task: str | None = None) -> None:
        item = {"reference": reference, "cause": cause}
        if task:
            item["task"] = task
        if item not in errors:
            errors.append(item)

    def _lifecycle_nodes(self) -> list[dict[str, Any]]:
        nodes = []
        for state in self._spec.states:
            node = str(state.get("current_node") or "")
            if not node or node == lifecycle.COMPLETE:
                continue
            nodes.append(
                {
                    "node": node,
                    "phase": str(state.get("phase") or ""),
                    "purpose": str(state.get("purpose") or ""),
                }
            )
        known = {item["node"] for item in nodes}
        for node in self._spec.rituals:
            if node not in known:
                nodes.append({"node": node, "phase": "", "purpose": ""})
        return nodes

    def _board_payload(self) -> dict[str, Any]:
        return doc_access.read_doc(self.board_path, BoardDoc)

    def _board_task_paths(self, errors: list[dict[str, str]]) -> list[Path]:
        tasks_dir = (self.root / "desk" / "tasks").resolve()
        paths: list[Path] = []
        for ref in self._board_payload().get("tasks") or []:
            path = (self.root / str(ref)).resolve()
            if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md":
                self._error(errors, str(ref), "Board reference is outside desk/tasks/ or is not a task file.")
                continue
            if not path.is_file():
                self._error(errors, str(ref), "Board reference points to a missing task file.")
                continue
            if path in paths:
                self._error(errors, str(ref), "Task listed twice in the Board.")
                continue
            paths.append(path)
        return paths

    def _resolve_pill(self, pill_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.pill", pill_id)
        except Exception:
            return None

    def _resolve_atom(self, atom_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.atom", atom_id)
        except Exception:
            return None

    def _pills(
        self, refs: list[tuple[str, str]], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        pills = []
        for pill_id, source in refs:
            doc = self._resolve_pill(pill_id)
            if doc is None:
                self._error(
                    errors,
                    pill_id,
                    f"Pill referenced by the {source} does not resolve to a PillDoc.",
                    task if source == "task" else None,
                )
                continue
            item = {"id": pill_id, "title": str(doc.get("title") or ""), "source": source}
            if detail:
                item.update({key: str(doc.get(key) or "") for key in ("what", "when", "how_not")})
            pills.append(item)
        return pills

    def _atoms(
        self, ids: list[str], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        atoms = []
        for atom_id in ids:
            doc = self._resolve_atom(atom_id)
            if doc is None:
                self._error(errors, atom_id, "Atom referenced by the task does not resolve to an AtomDoc.", task)
                continue
            item = {"id": atom_id, "title": str(doc.get("title") or "")}
            if detail:
                item["question"] = str(doc.get("five_wh_one_plus") or "")
                item["answer"] = str(doc.get("answer") or "")
            atoms.append(item)
        return atoms

    @staticmethod
    def _atom_ids(payload: dict[str, Any]) -> list[str]:
        ids = [str(item) for item in payload.get("effective_atoms") or payload.get("atoms") or []]
        ids += [
            str(ref)
            for ref in payload.get("effective_references") or payload.get("references") or []
            if str(ref).startswith("atom-")
        ]
        return list(dict.fromkeys(ids))

    def _closeout(self, task_id: str, node: str, errors: list[dict[str, str]]) -> dict[str, Any] | None:
        try:
            report = self.ops.verify_task_closeout(task_id)
        except Exception as exc:
            self._error(errors, task_id, f"verify_task_closeout failed: {exc}")
            return None
        at_closeout = node == "ritual-closeout"
        evidence = []
        for name, gate in report.get("gates", {}).items():
            state = "holds" if gate.get("ok") else ("failing" if at_closeout else "pending")
            evidence.append(
                {
                    "gate": name,
                    "state": state,
                    "evidence": list(gate.get("evidence") or []),
                    "findings": list(gate.get("findings") or []),
                }
            )
        for finding in report.get("findings", []):
            if finding.get("code") == "unknown_closeout_evidence":
                evidence.append({"gate": "unknown", "state": "failing", "evidence": [], "findings": [finding]})
        return {
            "ok": bool(report.get("ok")),
            "declared": list(report.get("declared") or []),
            "found": list(report.get("found") or []),
            "summary": report.get("summary"),
            "implicit_code": bool(report.get("implicit_code")),
            "alerts": list(report.get("alerts") or []),
            "evidence": evidence,
        }

    def _card(
        self, path: Path, board_pills: list[str], errors: list[dict[str, str]], *, detail: bool = False
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        stem = path.stem
        payload = doc_access.resolve_task_payload(self.root, stem)
        task_id = str(payload.get("id") or stem)
        task, gates = self.ops.show_task(stem)
        node = str(payload.get("current_node") or "")
        if task is not None and not gates and node and node != lifecycle.COMPLETE:
            try:
                lifecycle.transitions_from(self.root, node, snapshot=self.ops.snapshot)
                cause = f"The desk lifecycle graph declares no transition leaving {node}."
            except Exception as exc:
                cause = f"Lifecycle gates unavailable: {exc}"
            self._error(errors, task_id, cause)
        pill_refs = [(str(p), "task") for p in payload.get("effective_pills") or payload.get("pills") or []]
        pill_refs += [(p, "board") for p in board_pills if p not in {ref for ref, _ in pill_refs}]
        card = {
            "id": task_id,
            "title": str(payload.get("title") or ""),
            "status": str(payload.get("status") or ""),
            "current_node": node,
            "task_type": str(payload.get("task_type") or ""),
            "path": self._rel(path),
            "gates": [dict(gate) for gate in gates],
            "gates_holding": sum(1 for gate in gates if gate.get("holds")),
            "gates_total": len(gates),
            "closeout": self._closeout(stem, node, errors),
            "pills": self._pills(pill_refs, errors, detail=detail, task=task_id),
            "atoms": self._atoms(self._atom_ids(payload), errors, detail=detail, task=task_id),
        }
        return card, payload

    # ------------------------------------------------------------ views
    def board(self) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._board_view()

    def _board_view(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        board = self._board_payload()
        board_pills = [str(p) for p in board.get("pills") or []]
        nodes = self._lifecycle_nodes()
        columns = {item["node"]: {**item, "in_lifecycle": True, "count": 0, "tasks": []} for item in nodes}
        for path in self._board_task_paths(errors):
            try:
                card, _ = self._card(path, board_pills, errors)
            except Exception as exc:
                self._error(errors, self._rel(path), f"Task does not load: {exc}")
                continue
            node = card["current_node"]
            if node not in columns:
                self._error(errors, card["id"], f"current_node '{node}' is not a node of the task lifecycle.")
                columns[node] = {"node": node, "phase": "", "purpose": "", "in_lifecycle": False, "count": 0, "tasks": []}
            columns[node]["tasks"].append(card)
            columns[node]["count"] += 1
        cards = [card for column in columns.values() for card in column["tasks"]]
        return {
            "view": "board",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "board": {
                "path": self._rel(self.board_path),
                "pills": self._pills([(p, "board") for p in board_pills], errors, detail=False),
            },
            "columns": list(columns.values()),
            "counts": {
                "tasks": len(cards),
                "by_node": {node: column["count"] for node, column in columns.items()},
                "gates_holding": sum(card["gates_holding"] for card in cards),
                "gates_total": sum(card["gates_total"] for card in cards),
            },
            "errors": errors,
        }

    def task(self, selector: str) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._task_view(selector)

    def _task_view(self, selector: str) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        try:
            path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.ops.desk_root / "tasks", selector)
        except (FileNotFoundError, ValueError) as exc:
            raise DeskViewError(f"Task '{selector}' does not resolve: {exc}") from exc
        board_paths = self._board_task_paths([])
        board_pills = [str(p) for p in self._board_payload().get("pills") or []]
        card, payload = self._card(path, board_pills, errors, detail=True)
        try:
            report = self.ops.next_action_report(path.stem)
            next_info = {
                "phase": report.get("phase", ""),
                "ritual": report.get("ritual", ""),
                "next_actions": list(report.get("next_actions") or []),
                "advance_when": list(report.get("advance_when") or []),
            }
        except Exception as exc:
            next_info = None
            self._error(errors, card["id"], f"next_action_report failed: {exc}")
        return {
            "view": "task",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "task": {
                **card,
                "on_board": path.resolve() in board_paths,
                "why": str(payload.get("why") or ""),
                "goal": str(payload.get("goal") or ""),
                "scope": str(payload.get("scope") or ""),
                "implementation_path": str(payload.get("implementation_path") or ""),
                "validation": [str(v) for v in payload.get("effective_validation") or payload.get("validation") or []],
                "done_when": str(payload.get("effective_done_when") or payload.get("done_when") or ""),
                "references": [str(r) for r in payload.get("effective_references") or payload.get("references") or []],
                "files": [str(f) for f in payload.get("files") or []],
                "depends_on": [str(d) for d in payload.get("depends_on") or []],
                "inherits_from": [str(i) for i in payload.get("inherits_from") or []],
                "from_drawer": str(payload.get("from_drawer") or ""),
                "history": [str(h) for h in payload.get("history") or []],
            },
            "next": next_info,
            "revision": task_revision(self.board_path, path),
            "errors": errors,
        }

    def drawer(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        drawer_dir = self.root / "desk" / "drawer" / "tasks"
        index_files = self.ops.drawer.DRAWER_INDEX_FILES
        entries = []
        files = sorted(p for p in drawer_dir.glob("*.md") if p.name not in index_files) if drawer_dir.is_dir() else []
        for path in files:
            rel = self._rel(path)
            try:
                text = self.ops.drawer._read_markdown(path)
            except Exception as exc:
                self._error(errors, rel, f"Drawer file does not parse: {exc}")
                continue
            try:
                doc = doc_access.read_doc(path, TaskDoc)
            except Exception as exc:
                doc = {}
                self._error(errors, rel, f"Drawer file is not a valid TaskDoc: {exc}")
            lines = [
                line.strip()
                for line in text["body"].splitlines()
                if line.strip() and not line.lstrip().startswith("#") and not _TEMPLATE_HINT.match(line.strip())
            ]
            entries.append(
                {
                    "id": str(doc.get("id") or path.stem),
                    "markdown": path.read_text(encoding="utf-8"),
                    "title": text["title"],
                    "status": str(doc["status"]) if doc.get("status") else None,
                    "excerpt": lines[:EXCERPT_LINES],
                    "path": rel,
                    "command": "deskops add task --root . --from-drawer "
                    + shlex.quote(rel)
                    + " --title "
                    + shlex.quote(text["title"]),
                }
            )
        return {
            "view": "drawer",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "tasks": entries,
            "count": len(entries),
            "errors": errors,
        }

    def inbox(self) -> dict[str, Any]:
        from deskops.cli.commands.message import MessageCLI

        errors: list[dict[str, str]] = []
        reader = MessageCLI()
        notes = []
        for path in reader._iter_notes(self.root / "desk"):
            rel = self._rel(path)
            try:
                detail = reader._note_detail(path)
            except Exception as exc:
                self._error(errors, rel, f"Inbox note does not parse: {exc}")
                continue
            try:
                body = str(doc_access.read_doc(path, InboxNoteDoc).get("body") or "")
            except Exception as exc:
                body = str(detail.get("body") or "")
                self._error(errors, rel, f"Inbox note is not a valid InboxNoteDoc; body shown raw: {exc}")
            match = _NOTE_STAMP.match(path.name)
            date = "{}-{}-{}T{}:{}:{}".format(*match.groups()) if match else None
            if date is None:
                self._error(errors, rel, "Inbox note filename carries no YYYYMMDD-HHMMSS stamp.")
            status = str(detail.get("status") or "")
            notes.append(
                {
                    "id": path.stem,
                    "path": rel,
                    "kind": str(detail.get("kind") or ""),
                    "title": str(detail.get("title") or ""),
                    "sender": str(detail.get("sender_project") or ""),
                    "target": str(detail.get("target_project") or ""),
                    "date": date,
                    "status": status,
                    "acknowledged": status == "closed",
                    "acknowledged_by": detail.get("acknowledged_by"),
                    "acknowledged_at": detail.get("acknowledged_at"),
                    "body": body,
                    "revision": note_revision(path),
                }
            )
        return {
            "view": "inbox",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "notes": notes,
            "count": len(notes),
            "open": sum(1 for note in notes if not note["acknowledged"]),
            "errors": errors,
        }

    def _list_workers(self) -> list[dict[str, Any]]:
        if self._workers_provider is not None:
            agents = self._workers_provider()
        else:
            from deskops.runtime.herdr import HerdrClient, HerdrProvider

            agents = HerdrProvider(HerdrClient(self.herdr)).list_agents()
        from deskops.cli.commands.runtime import RuntimeCLI

        return [RuntimeCLI._project_agent(agent) for agent in agents]

    def agents(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        workers: list[dict[str, Any]] | None
        workers_error = None
        try:
            workers = self._list_workers()
        except Exception as exc:
            workers = None
            workers_error = f"{type(exc).__name__}: {exc}"
            self._error(errors, "runtime workers", f"Herdr runtime unavailable: {workers_error}")
        board_ids = set()
        for path in self._board_task_paths([]):
            try:
                board_ids.add(str(doc_access.read_doc(path, TaskDoc).get("id") or path.stem))
            except Exception:
                continue
        runs: list[dict[str, Any]] = []
        index = self.root / RUN_INDEX
        total = 0
        if index.is_file():
            lines = index.read_text(encoding="utf-8").splitlines()
            parsed = []
            for number, line in enumerate(lines, start=1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if not isinstance(entry, dict):
                        raise ValueError("entry is not an object")
                except ValueError as exc:
                    self._error(errors, f"{RUN_INDEX.as_posix()}:{number}", f"Run index line does not parse: {exc}")
                    continue
                parsed.append(entry)
            total = len(parsed)
            for entry in reversed(parsed[-self.runs_limit :] if self.runs_limit > 0 else []):
                task_id = str(entry.get("task_id") or "")
                runs.append(
                    {
                        "task_id": task_id,
                        "run_id": entry.get("run_id"),
                        "run_dir": entry.get("run_dir"),
                        "commit": entry.get("commit"),
                        "mode": entry.get("mode"),
                        "on_board": task_id in board_ids,
                    }
                )
        return {
            "view": "agents",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "workers": workers,
            "workers_error": workers_error,
            "live_workers": None if workers is None else len(workers),
            "runs": runs,
            "runs_total": total,
            "runs_limit": self.runs_limit,
            "errors": errors,
        }


# ---------------------------------------------------------------- text rendering
def _errors_text(view: dict[str, Any]) -> list[str]:
    return [f"! {item['reference']}: {item['cause']}" for item in view.get("errors") or []]


def render_text(view: dict[str, Any]) -> str:
    kind = view.get("view")
    lines: list[str] = []
    if kind == "board":
        for column in view["columns"]:
            lines.append(f"{column['node']} ({column['count']})")
            for card in column["tasks"]:
                lines.append(f"  {card['id']} [{card['status']}] gates {card['gates_holding']}/{card['gates_total']} - {card['title']}")
    elif kind == "task":
        task = view["task"]
        lines += [f"{task['id']} [{task['status']}] {task['current_node']}", task["title"], f"revision {view['revision']}"]
        for gate in task["gates"]:
            lines.append(f"  gate {gate['relation_type']} -> {gate['target']}: {'holds' if gate['holds'] else 'pending'} ({gate['condition'] or 'no condition'})")
        for item in (task.get("closeout") or {}).get("evidence", []):
            lines.append(f"  evidence {item['gate']}: {item['state']}")
    elif kind == "drawer":
        for entry in view["tasks"]:
            lines.append(f"{entry['id']} [{entry['status'] or '-'}] {entry['title']}")
    elif kind == "inbox":
        for note in view["notes"]:
            lines.append(f"{note['id']} [{'ack' if note['acknowledged'] else 'open'}] {note['sender']} -> {note['target']}: {note['title']}")
    elif kind == "agents":
        if view["workers"] is None:
            lines.append(f"workers unavailable: {view['workers_error']}")
        else:
            lines.append(f"live workers: {view['live_workers']}")
            for worker in view["workers"]:
                lines.append(f"  {worker.get('pane')} | {worker.get('kind')} | {worker.get('status')} | {worker.get('cwd') or ''}")
        lines.append(f"runs (latest {len(view['runs'])} of {view['runs_total']}):")
        for run in view["runs"]:
            lines.append(f"  {run['task_id']} | {run['mode'] or '-'} | {run['run_dir'] or '-'}")
    return "\n".join([*lines, *_errors_text(view)])

FILE:deskops/data/desk_declaration.yaml
# The desk a fresh repository gets: what `deskops init`, `deskops desk install`, `deskops desk
# update --apply` and the first desk operation create when it is missing (CC36, DP3).
#
# This is an sldb StoreDeclaration (`sldb.api.StoreDeclaration`) restricted to `folders`,
# `seeds` and `include`; deskops reads it, renders every seed for the desk at hand and passes
# the result in process to `sldb.api.scaffold_store` (`deskops.workspace.seed_desk`):
#
# - `{desk_name}` in a `file:` template or in a `document:` payload is replaced with the
#   project directory's name (`str.replace`, no other placeholder exists);
# - `file:` sources are read from `deskops/data/` (`templates/` for the desk's own files,
#   `lifecycle/` for the lifecycle graph);
# - `document:` seeds are rendered through their deskops model, as the Board and the review
#   runtime profile always were; the runtime profile's `system_prompt` is not data here: it
#   is `deskops.services.review.SYSTEM`, injected while the declaration is built.
#
# A desk's own files are `if_missing` seeds: a desk that already has the file keeps its own.
# The task lifecycle graph (CC31, GO09) is `managed`: the three RelationTypeDoc and the three
# RelationDoc under `desk/lifecycle/` are deskops' documents, written from `lifecycle/` and
# rewritten whenever a desk's copy differs (`deskops desk update --apply` reports it). Each
# RelationDoc carries the transition's effects in `attributes`: `sets` (the fields written on
# the task when the edge is taken) and `terminal` (the task closes). The activation gate of
# each factory task type (CC32, GO06/GO08) is a `managed` RuleDoc too, written from `rules/`
# to `desk/lifecycle/rule-activation-<type>.md`: `on_transition` over `ritual-execution`, with
# subject `model <= <TypeDoc>` so a desk subtype inherits it, it requires the review receipts
# the type asks for (accepted and intact) and the task's dependencies closed; sldb evaluates
# it when `deskops advance` asks for the holding edges. The closeout gate of each factory type
# (CC33b) is the same kind of managed RuleDoc, written from `rules/` to
# `desk/lifecycle/rule-closeout-<type>.md`: `on_transition` over `ritual-closeout`, it requires
# the evidence receipts `deskops closeout verify` writes (kinds in `rules/closeout-evidence.yaml`),
# accepted and intact, and `deskops closeout commit` evaluates it; the two
# `rule-closeout-alert-*.md` are `on_write` alerts over the task's own fields. The `include` rules say
# which desk documents `deskops desk update --apply` tracks under which model
# (`sldb.api.stores.apply_declaration.apply_includes`): the lifecycle documents, the rules,
# the three lifecycle rituals by their ids (`RitualDoc:ritual-<x>`, what the graph's edges
# name), the seeded Board (`BoardDoc:Board`) and phase ritual (`RitualDoc:ritual-phase`), which
# the selectors resolve through the store (CC35b d1), and one glob per desk folder. The tasks
# are tracked by their own paths.
folders:
- desk/tasks
- desk/contexts
- desk/rituals
- desk/atoms
- desk/roles
- desk/inbox
- desk/reviews
- desk/drawer
- desk/runtimes
- desk/materializations
- desk/steps
- desk/registry
- desk/faq
seeds:
- path: desk/config.json
  mode: if_missing
  file: templates/config.json
- path: desk/tasks/Board.md
  mode: if_missing
  track: false
  document:
    model: BoardDoc
    name: board-001
    payload:
      id: board-001
      title: '{desk_name} Board'
      scope: desk
      purpose: Route the active execution set for {desk_name}.
      tasks: []
      pills:
      - desk/contexts/pills.md
      rituals:
      - desk/rituals/phase.md
      - desk/rituals/execution.md
      - desk/rituals/testing.md
      - desk/rituals/closeout.md
      notes: Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
      tags:
      - workspace:desk
- path: desk/contexts/pills.md
  mode: if_missing
  file: templates/contexts/pills.md
- path: desk/rituals/phase.md
  mode: if_missing
  file: templates/rituals/phase.md
- path: desk/rituals/execution.md
  mode: if_missing
  file: templates/rituals/execution.md
- path: desk/rituals/testing.md
  mode: if_missing
  file: templates/rituals/testing.md
- path: desk/rituals/closeout.md
  mode: if_missing
  file: templates/rituals/closeout.md
- path: desk/drawer/README.md
  mode: if_missing
  file: templates/drawer/README.md
- path: desk/atoms/tag-namespaces.yaml
  mode: if_missing
  file: templates/atoms/tag-namespaces.yaml
- path: desk/runtimes/runtime-pi-deepseek-flash.md
  mode: if_missing
  track: false
  document:
    model: RuntimeProfileDoc
    name: runtime-pi-deepseek-flash
    payload:
      id: runtime-pi-deepseek-flash
      title: Pi deepseek-flash isolated reviewer
      status: active
      kind: pi
      binary: pi
      model_flag: --model
      fallback_models_flag: ''
      fallback_models_join: comma
      tools_flag: ''
      tools_join: comma
      system_prompt_flag: --system-prompt
      system_prompt_delivery: inline
      session_flag: ''
      extra_args:
      - --provider
      - deepseek
      - --model
      - deepseek-flash
      - --thinking
      - low
      - --offline
      - --no-session
      - --no-context-files
      - --no-skills
      - --no-extensions
      - --no-prompt-templates
      - --no-tools
      - --print
      unsupported_role_fields: []
      notes: 'Verified cheap profile for ritual-context-review step 3 (D4): offline, no session/context/skills/extensions/prompt-templates/tools.'
      summary: Isolated cheap reviewer profile (pi deepseek-flash) used by `deskops review`.
      tags:
      - system:deskops
- path: desk/lifecycle/type-task_activates.md
  mode: managed
  file: lifecycle/type-task_activates.md
- path: desk/lifecycle/type-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/type-task_hands_to_closeout.md
- path: desk/lifecycle/type-task_completes.md
  mode: managed
  file: lifecycle/type-task_completes.md
- path: desk/lifecycle/execution-task_activates.md
  mode: managed
  file: lifecycle/execution-task_activates.md
- path: desk/lifecycle/testing-task_hands_to_closeout.md
  mode: managed
  file: lifecycle/testing-task_hands_to_closeout.md
- path: desk/lifecycle/closeout-task_completes.md
  mode: managed
  file: lifecycle/closeout-task_completes.md
- path: desk/lifecycle/rule-activation-task-code.md
  mode: managed
  file: rules/rule-activation-task-code.md
- path: desk/lifecycle/rule-activation-task-docs.md
  mode: managed
  file: rules/rule-activation-task-docs.md
- path: desk/lifecycle/rule-activation-task-debug.md
  mode: managed
  file: rules/rule-activation-task-debug.md
- path: desk/lifecycle/rule-activation-task-refactor.md
  mode: managed
  file: rules/rule-activation-task-refactor.md
- path: desk/lifecycle/rule-activation-task-decision.md
  mode: managed
  file: rules/rule-activation-task-decision.md
- path: desk/lifecycle/rule-activation-task-aggregate.md
  mode: managed
  file: rules/rule-activation-task-aggregate.md
- path: desk/lifecycle/rule-activation-task-external.md
  mode: managed
  file: rules/rule-activation-task-external.md
- path: desk/lifecycle/rule-closeout-task-code.md
  mode: managed
  file: rules/rule-closeout-task-code.md
- path: desk/lifecycle/rule-closeout-task-docs.md
  mode: managed
  file: rules/rule-closeout-task-docs.md
- path: desk/lifecycle/rule-closeout-task-debug.md
  mode: managed
  file: rules/rule-closeout-task-debug.md
- path: desk/lifecycle/rule-closeout-task-refactor.md
  mode: managed
  file: rules/rule-closeout-task-refactor.md
- path: desk/lifecycle/rule-closeout-task-decision.md
  mode: managed
  file: rules/rule-closeout-task-decision.md
- path: desk/lifecycle/rule-closeout-task-aggregate.md
  mode: managed
  file: rules/rule-closeout-task-aggregate.md
- path: desk/lifecycle/rule-closeout-task-external.md
  mode: managed
  file: rules/rule-closeout-task-external.md
- path: desk/lifecycle/rule-closeout-alert-implicit-code.md
  mode: managed
  file: rules/rule-closeout-alert-implicit-code.md
- path: desk/lifecycle/rule-closeout-alert-pill-graduation.md
  mode: managed
  file: rules/rule-closeout-alert-pill-graduation.md
include:
- model: RelationTypeDoc
  glob: desk/lifecycle/type-*.md
- model: RelationDoc
  paths:
  - desk/lifecycle/execution-task_activates.md
  - desk/lifecycle/testing-task_hands_to_closeout.md
  - desk/lifecycle/closeout-task_completes.md
- model: RuleDoc
  glob: desk/lifecycle/rule-activation-*.md
- model: RuleDoc
  glob: desk/lifecycle/rule-closeout-*.md
- model: BoardDoc
  paths:
  - desk/tasks/Board.md
- model: RitualDoc
  paths:
  - path: desk/rituals/phase.md
    name: ritual-phase
  - path: desk/rituals/execution.md
    name: ritual-execution
  - path: desk/rituals/testing.md
    name: ritual-testing
  - path: desk/rituals/closeout.md
    name: ritual-closeout
- model: BoardDoc
  glob: desk/tasks/board-*.md
- model: PillDoc
  glob: desk/contexts/pill-*.md
- model: RitualDoc
  glob: desk/rituals/ritual-*.md
- model: AtomDoc
  glob: desk/atoms/atom-*.md
- model: ProtoAtomDoc
  glob: desk/atoms/proto-*.md
- model: RoleDoc
  glob: desk/roles/*.md
- model: RepositoryDoc
  glob: desk/registry/*.md
- model: StepDoc
  glob: desk/steps/*.md
- model: DeskFAQDoc
  glob: desk/faq/*.md

FILE:deskops/cli/commands/view.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error


class ViewCLI:
    """Read-only views of a desk for the deskops UI (contract: docs/deskops-ui.md)."""

    def run(self, args: Any) -> int:
        from deskops.services.desk_view import DeskView, DeskViewError, render_text

        fmt = getattr(args, "format", "text")
        try:
            view = DeskView(Path(args.root).resolve(), runs_limit=getattr(args, "runs", 20), herdr=getattr(args, "herdr", "herdr"))
            command = args.view_command
            if command == "board":
                payload = view.board()
            elif command == "task":
                payload = view.task(args.task_id)
            elif command == "drawer":
                payload = view.drawer()
            elif command == "inbox":
                payload = view.inbox()
            elif command == "agents":
                payload = view.agents()
            else:
                return render_error(f"Unknown view: {command}", fmt, type_name="DomainError")
        except (DeskViewError, FileNotFoundError, ValueError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}")
        return render(payload, fmt, render_text)

FILE:deskops/operations.py
"""The facade of one desk: every operation the CLI and the UIs call, as one call each.

``DeskopsOperations`` builds the arguments and delegates to the service that owns the
operation (tasks, atoms, closure, drawer, closeout gates), to ``deskops.doc_access`` for
plain document reads and writes, or to ``deskops.lifecycle``. No logic lives here.
"""

from __future__ import annotations

from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.doc_access import ARTIFACT_SUBJECTS
from deskops.doc_access import DocumentRecord
from deskops.doc_access import RepoTaskRoute
from deskops.doc_access import slugify
from deskops.lifecycle import ReadSnapshot
from deskops.lifecycle import TransitionResult
from deskops.paths import data_path
from deskops.runtime import Task
from deskops.services.atoms import AtomCreateResult
from deskops.services.atoms import AtomMergeResult
from deskops.services.atoms import AtomSplitResult
from deskops.services.atoms import AtomValidationRecord
from deskops.services.closure import CloseoutGateReport
from deskops.services.tasks import TaskBundle

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closure import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService

__all__ = [
    "ARTIFACT_MODELS",
    "ARTIFACT_PATHS",
    "ARTIFACT_SUBJECTS",
    "AtomCreateResult",
    "AtomMergeResult",
    "AtomSplitResult",
    "AtomValidationRecord",
    "CloseoutGateReport",
    "DeskopsOperations",
    "DocumentRecord",
    "RepoTaskRoute",
    "TaskBundle",
    "slugify",
]


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = data_path("spec")
        self.snapshot: ReadSnapshot | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @contextmanager
    def read_snapshot(self) -> Iterator[None]:
        """Reuse task-independent graph reads for the duration of one read-only pass.

        Inside the block, the closeout graph context and the lifecycle transitions
        leaving each node are computed once and shared by every task read. The caller
        promises not to write the desk inside the block; nesting reuses the outer one.
        """
        if self.snapshot is not None:
            yield
            return
        self.snapshot = ReadSnapshot()
        try:
            yield
        finally:
            self.snapshot = None

    # ---------------------------------------------------------------- services
    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService

            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService

            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService

            self._tasks = TasksService(self.root, self)
        return self._tasks

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService

            self._atoms = AtomsService(self.root, self)
        return self._atoms

    # ---------------------------------------------------------------- documents
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        return doc_access.create_artifact(self.root, artifact_id, raw_payload)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        return doc_access.edit_artifact_field(self.root, subject, selector, field, raw_value)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        return doc_access.show_artifact(self.root, artifact_id, doc_id)

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        return doc_access.list_repo_task_routes(self.root)

    # ---------------------------------------------------------------- tasks
    def registered_task_types(self) -> dict[str, type[Any]]:
        return self.tasks.registered_task_types()

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        return self.tasks.bind_pill_to_task(task_selector, pill_selector)

    def list_tasks(self) -> list[Task]:
        return self.tasks.list_tasks()

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        return self.tasks.show_task(task_id)

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def render_next_action_diagram(self) -> str:
        return self.tasks.render_next_action_diagram()

    # ---------------------------------------------------------------- closeout
    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        return self.closure.verify_task_closeout(task_selector)

    # ---------------------------------------------------------------- drawer
    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

    # ---------------------------------------------------------------- atoms
    def atom_folder_axis(self) -> str | None:
        return self.atoms.atom_folder_axis()

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    # ---------------------------------------------------------------- private aliases
    # graph_ui (UIs/graph_ui/frontends/mindmap/deskops_routes.py, frontends/desk/serve.py)
    # and deskops/domain_tree.py still call these private names; CC34 replaces that
    # access and removes the aliases.
    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    # CC34: alias for graph_ui, removed by CC34
    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return doc_access.resolve_glob(self.root, directory, doc_id)

    # CC34: alias for graph_ui, removed by CC34
    def _registered_repositories(self) -> list[dict[str, Any]]:
        return doc_access.registered_repositories(self.root)

    def _repository_root(self, repository: dict[str, Any]) -> Path:
        return doc_access.repository_root(self.root, repository)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:deskops/domain_tree.py
"""Domain tree: crossroads order a knowledge base and protoatoms hang from them.

A ``domain:a.b.c`` tag places a document under the path ``a.b.c``. Every prefix
of that path (``a``, ``a.b``, ``a.b.c``) needs a CrossroadDoc with written
content: the system is forced to write the parent before it can describe the
children. Protoatoms are free atoms; typing one into another sldb model keeps it
as a redirect stub whose ``typed_as`` names the typed document.

What one document must satisfy on its own (the form of its id, its tags and its
domain paths, one ``domain:`` tag per protoatom, a crossroad id naming its path)
is a validator of its model in ``deskops.models``. What is checked here needs
other documents or the file tree: the written parents of a domain path, the file
name of a document, the tag namespace registry and the target of ``typed_as``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.bootstrap import MODEL_REFS
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.models.atom import DOMAIN_NAMESPACE as DOMAIN
from deskops.models.atom import AtomDoc
from deskops.models.atom import domain_paths
from deskops.models.crossroad import CROSSROAD_PREFIX
from deskops.models.crossroad import DOMAIN_PATH_PATTERN
from deskops.models.crossroad import CrossroadDoc
from deskops.models.crossroad import crossroad_id
from deskops.models.protoatom import PROTO_PREFIX
from deskops.models.protoatom import ProtoAtomDoc
from deskops.models.validation import check_document
from deskops.models.validation import validated

__all__ = ["DOMAIN", "PROTO_PREFIX", "CROSSROAD_PREFIX", "domain_paths", "crossroad_id", "DomainTree"]

_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)


def prefixes(path: str) -> list[str]:
    """``a.b.c`` -> ``['a', 'a.b', 'a.b.c']``."""
    parts = path.split(".")
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def read_crossroads(atoms_dir: Path) -> dict[str, dict[str, Any]]:
    """Written crossroads by path. An unreadable or invalid one does not count as written."""
    found: dict[str, dict[str, Any]] = {}
    for file in sorted(atoms_dir.rglob(f"{CROSSROAD_PREFIX}*.md")):
        try:
            payload = extract_model_data(CrossroadDoc, file.read_text(encoding="utf-8"))
            CrossroadDoc(**payload)
        except Exception:
            continue
        found[str(payload["path"])] = {**payload, "file": file}
    return found


def missing_parents(tags: list[str], crossroads: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for value in domain_paths(tags):
        for prefix in prefixes(value):
            if prefix not in crossroads and prefix not in missing:
                missing.append(prefix)
    return missing


def require_domain_parents(atoms_dir: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix.

    The form of each path is the model's invariant (``AtomDoc.tags``); this only asks
    the file tree whether the parents are written.
    """
    missing = missing_parents(tags, read_crossroads(atoms_dir))
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


@dataclass
class Created:
    doc_id: str
    path: Path


@dataclass
class Typed:
    protoatom_id: str
    protoatom_path: Path
    model: str
    doc_id: str
    path: Path


class DomainTree:
    """Crossroads, protoatoms and typing over one repository's desk/atoms."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.desk_root = doc_access.desk_root(self.root)
        self.atoms_dir = self.desk_root / "atoms"

    def create_crossroad(self, path: str, *, title: str, content: str) -> Created:
        doc_access.ensure_workspace(self.root)
        payload = validated(
            CrossroadDoc, {"id": crossroad_id(path), "path": path, "title": title, "content": content}
        ).model_dump(mode="json")
        parent = path.rpartition(".")[0]
        if parent:
            require_domain_parents(self.atoms_dir, [f"{DOMAIN}:{parent}"])
        if path in read_crossroads(self.atoms_dir):
            raise FileExistsError(f"A crossroad for '{path}' already exists.")
        return self._create(CrossroadDoc, payload, [f"{DOMAIN}:{path}"])

    def create_protoatom(self, doc_id: str, *, title: str, content: str = "", tags: list[str]) -> Created:
        doc_access.ensure_workspace(self.root)
        tags = list(tags)
        payload = validated(ProtoAtomDoc, {"id": doc_id, "title": title, "content": content, "tags": tags}).model_dump(
            mode="json"
        )
        validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        require_domain_parents(self.atoms_dir, tags)
        return self._create(ProtoAtomDoc, payload, tags)

    def type_protoatom(
        self,
        selector: str,
        *,
        model_name: str,
        doc_id: str | None = None,
        content_field: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Typed:
        """Create the typed document, then turn the protoatom into its redirect stub."""
        doc_access.ensure_workspace(self.root)
        proto_path = self._find_protoatom(selector)
        proto = doc_access.read_doc(proto_path, ProtoAtomDoc)
        if proto.get("typed_as"):
            raise ValueError(f"{proto['id']} was already typed as {proto['typed_as']}.")
        model = self._resolve_model(model_name)
        slug = str(proto["id"]).removeprefix(PROTO_PREFIX)
        target_id = doc_id or f"{model.__name__.removesuffix('Doc').lower()}-{slug}"
        payload = validated(model, self._typed_payload(model, target_id, proto, content_field, data or {})).model_dump(
            mode="json"
        )
        stub = validated(ProtoAtomDoc, {**proto, "typed_as": f"{model.__name__}:{target_id}",
                                        "content": _redirect_content(model.__name__, target_id)})
        # Rendered before any write, so a stub that cannot be written never leaves a typed orphan.
        stub_text = render_model_markdown(ProtoAtomDoc, stub.model_dump(mode="json")) + "\n"
        target_path = self._typed_path(model, target_id, list(proto.get("tags") or []))
        self._write_and_track(target_path, model, payload, target_id)
        proto_path.write_text(stub_text, encoding="utf-8")
        return Typed(str(proto["id"]), proto_path, model.__name__, target_id, target_path)

    def check(self) -> list[dict[str, Any]]:
        """Domain-tree errors per document under desk/atoms."""
        crossroads = read_crossroads(self.atoms_dir)
        records: list[dict[str, Any]] = []
        for path in sorted(self.atoms_dir.rglob("*.md")):
            if path.name.startswith(CROSSROAD_PREFIX):
                doc_id, errors = self._check_crossroad(path, crossroads)
            elif path.name.startswith(PROTO_PREFIX):
                doc_id, errors = self._check_protoatom(path, crossroads)
            else:
                doc_id, errors = path.stem, self._check_atom(path, crossroads)
            records.append({"id": doc_id, "path": str(path), "errors": errors})
        return records

    def tree(self) -> dict[str, Any]:
        """Crossroads nested by path, with the documents hanging from each one."""
        crossroads = read_crossroads(self.atoms_dir)
        nodes = {
            path: {"path": path, "id": item["id"], "title": item["title"], "children": [], "items": []}
            for path, item in crossroads.items()
        }
        roots: list[dict[str, Any]] = []
        for path in sorted(nodes):
            parent = path.rpartition(".")[0]
            (nodes[parent]["children"] if parent in nodes else roots).append(nodes[path])
        orphans: list[dict[str, Any]] = []
        unplaced: list[dict[str, Any]] = []
        for file in sorted(self.atoms_dir.rglob("*.md")):
            if file.name.startswith(CROSSROAD_PREFIX):
                continue
            model = ProtoAtomDoc if file.name.startswith(PROTO_PREFIX) else AtomDoc
            try:
                payload = doc_access.read_doc(file, model)
            except Exception:
                continue
            item = {"id": payload.get("id") or file.stem, "title": payload.get("title"),
                    "model": model.__name__, "typed_as": payload.get("typed_as")}
            places = domain_paths(list(payload.get("tags") or []))
            if not places:
                unplaced.append(item)
            for place in places:
                (nodes[place]["items"] if place in nodes else orphans).append({**item, "domain": place})
        return {"roots": roots, "orphans": orphans, "unplaced": unplaced}

    def _create(self, model: type[Any], payload: dict[str, Any], tags: list[str]) -> Created:
        doc_id = str(payload["id"])
        if any(self.atoms_dir.rglob(f"{doc_id}.md")):
            raise FileExistsError(f"Refusing to overwrite existing document {doc_id}.")
        path = doc_access.atom_doc_path(self.root, doc_id, tags)
        self._write_and_track(path, model, payload, doc_id)
        return Created(doc_id, path)

    def _write_and_track(self, path: Path, model: type[Any], payload: dict[str, Any], doc_id: str) -> None:
        doc_access.write_new_doc(self.root, path, model, payload)
        try:
            doc_access.track_created_document(self.root, model, path, doc_id)
        except Exception:
            doc_access.remove_created_file(path)
            raise

    def _find_protoatom(self, selector: str) -> Path:
        matches = [path for path in self.atoms_dir.rglob(f"{PROTO_PREFIX}*.md") if selector in {path.stem, path.name}]
        if not matches:
            raise FileNotFoundError(f"No protoatom '{selector}' under {self.atoms_dir}.")
        if len(matches) > 1:
            raise ValueError(f"Protoatom selector '{selector}' is ambiguous: {', '.join(map(str, matches))}")
        return matches[0]

    def _resolve_model(self, name: str) -> type[Any]:
        from sldb.cli.model_utils import resolve_model_ref
        from sldb.store.io import load_store_index
        from sldb.store.layout import store_exists

        store = self.root / ".sldb"
        if store_exists(store):
            entry = next((model for model in load_store_index(store).models if model.name == name), None)
            if entry is None:
                raise ValueError(f"Model '{name}' is not registered in {store}; register it before typing into it.")
            return resolve_model_ref(entry.model_ref, str(self.root))
        if name in MODEL_REFS:
            return resolve_model_ref(MODEL_REFS[name])
        raise ValueError(f"Unknown model '{name}': there is no local store and it is not a deskops model.")

    def _typed_payload(
        self, model: type[Any], target_id: str, proto: dict[str, Any], content_field: str | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        fields = model.model_fields
        carried = {"id": target_id, "title": proto.get("title"),
                   "tags": list(proto.get("tags") or []), "provenance": proto.get("provenance")}
        payload = {name: value for name, value in carried.items() if name in fields and value is not None}
        content = str(proto.get("content") or "")
        target = content_field or ("content" if "content" in fields else None)
        if target is not None:
            if target not in fields:
                raise ValueError(f"{model.__name__} has no field '{target}' to receive the protoatom content.")
            payload[target] = content
        elif content.strip():
            raise ValueError(
                f"{model.__name__} has no 'content' field: pass --content-field to choose where the protoatom "
                "content goes (for AtomDoc, answer)."
            )
        return {**payload, **data}

    def _typed_path(self, model: type[Any], doc_id: str, tags: list[str]) -> Path:
        if model.__name__ == AtomDoc.__name__:
            return doc_access.atom_doc_path(self.root, doc_id, tags)
        artifact = next((key for key, known in ARTIFACT_MODELS.items() if known.__name__ == model.__name__), None)
        folder = Path(ARTIFACT_PATHS[artifact]) if artifact else Path("typed") / model.__name__
        return self.desk_root / folder / f"{doc_id}.md"

    def _check_crossroad(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(CrossroadDoc, path.read_text(encoding="utf-8"), invalid="crossroad is invalid")
        except Exception as exc:
            return path.stem, [f"crossroad is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        if path.stem != doc_id:
            errors.append(f"filename must match crossroad id '{doc_id}'")
        parent = str(payload.get("path") or "").rpartition(".")[0]
        if parent:
            errors.extend(self._domain_errors([f"{DOMAIN}:{parent}"], crossroads))
        return doc_id, errors

    def _check_protoatom(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload, errors = check_document(ProtoAtomDoc, path.read_text(encoding="utf-8"), invalid="protoatom is invalid")
        except Exception as exc:
            return path.stem, [f"protoatom is invalid: {_first_line(exc)}"]
        doc_id = str(payload.get("id") or path.stem)
        tags = list(payload.get("tags") or []) if isinstance(payload.get("tags"), list) else []
        if path.stem != doc_id:
            errors.append(f"filename must match protoatom id '{doc_id}'")
        try:
            validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        except ValueError as exc:
            errors.append(str(exc))
        errors.extend(self._domain_errors(tags, crossroads))
        typed_as = str(payload.get("typed_as") or "")
        if typed_as and not any(self.desk_root.rglob(f"{typed_as.split(':', 1)[-1]}.md")):
            errors.append(f"typed_as target not found: {typed_as}")
        return doc_id, errors

    def _check_atom(self, path: Path, crossroads: dict[str, Any]) -> list[str]:
        try:
            tags = check_document(AtomDoc, path.read_text(encoding="utf-8"))[0].get("tags")
        except Exception:
            return []  # atoms validate already reports unreadable atoms
        return self._domain_errors(list(tags) if isinstance(tags, list) else [], crossroads)

    def _domain_errors(self, tags: list[str], crossroads: dict[str, Any]) -> list[str]:
        """The domain paths of ``tags`` without a written crossroad. A malformed path is the
        model's error (reported with the document), so it is left out here."""
        valid = [f"{DOMAIN}:{value}" for value in domain_paths(tags) if _DOMAIN_PATH.fullmatch(value)]
        return [f"no written crossroad for domain path '{path}'" for path in missing_parents(valid, crossroads)]


def _redirect_content(model_name: str, doc_id: str) -> str:
    return (
        f"Typed as {model_name} {doc_id}. This protoatom is kept as a redirect stub so its id keeps "
        "resolving; its content now lives in the typed document."
    )


def _first_line(exc: Exception) -> str:
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return " ".join(lines[:3]) if lines else exc.__class__.__name__

FILE:docs/deskops-ui.md
# deskops view: el contrato de datos de la UI de deskops

`deskops view {board,task <id>,drawer,inbox,agents} --root <repo> --format json|text`
produce las vistas que dibuja la UI de deskops (graph_ui, `frontends/desk/`). La clase
que las arma es `deskops.services.desk_view.DeskView`; graph_ui la importa en el mismo
proceso y sirve exactamente el mismo JSON.

Reglas comunes:

- **Solo lectura.** Ninguna vista escribe en `desk/`, `.sldb/` ni `runs/`.
- **Sin datos inventados.** Una referencia que no resuelve (pill, atom, tarea del Board,
  nota, línea del índice de corridas, runtime de Herdr) no aparece como dato: va a
  `errors` como `{"reference": "<id o ruta>", "cause": "<por qué>"}`; si la referencia la hace
  una tarea (una pill o un atom de la tarea), el error lleva además `"task": "<id de la tarea>"`
  para que la UI marque la tarjeta.
- `--format json` es el contrato estable; `--format text` es un resumen legible.
- Toda vista lleva `view` (nombre), `contract` (versión, hoy `1`), `root` (ruta absoluta
  del repo) y `errors`.
- Un error que impide la vista entera (no hay `desk/tasks/Board.md`, la tarea no resuelve)
  sale como el sobre de error de deskops (`{"ok": false, "error": {...}}`) con código 1.

## board

Una columna por nodo del ciclo de vida, en el orden de
`deskops/spec/workflows/task_lifecycle.yaml` (`ritual-execution`, `ritual-testing`,
`ritual-closeout`). Las tareas salen de `desk/tasks/Board.md` (el Board es la verdad).

```json
{
  "view": "board", "contract": 1, "root": "/abs/repo",
  "board": {"path": "desk/tasks/Board.md", "pills": [{"id": "pill-…", "title": "…", "source": "board"}]},
  "columns": [
    {"node": "ritual-execution", "phase": "execution", "purpose": "…", "in_lifecycle": true,
     "count": 1, "tasks": [CARD]}
  ],
  "counts": {"tasks": 1, "by_node": {"ritual-execution": 1, "ritual-testing": 0, "ritual-closeout": 0},
             "gates_holding": 1, "gates_total": 1},
  "errors": []
}
```

Una tarea cuyo `current_node` no es un nodo del ciclo de vida aparece en una columna
extra con `in_lifecycle: false` y además en `errors`.

`CARD`:

```json
{
  "id": "task-…", "title": "…", "status": "draft", "current_node": "ritual-execution",
  "task_type": "code", "path": "desk/tasks/task-….md",
  "gates": [{"relation_type": "task_activates", "target": "ritual-testing", "condition": "", "holds": true}],
  "gates_holding": 1, "gates_total": 1,
  "closeout": {
    "ok": false, "declared": ["tests", "commit"], "found": [], "summary": "…",
    "implicit_code": false, "alerts": [],
    "evidence": [{"gate": "tests", "state": "pending", "evidence": [], "findings": [{"code": "…", "message": "…"}]}]
  },
  "pills": [{"id": "pill-…", "title": "…", "source": "task|board"}],
  "atoms": [{"id": "atom-…", "title": "…"}]
}
```

- `gates` es exactamente lo que devuelve `DeskopsOperations.show_task` (transiciones que
  salen del nodo actual, con su condición sldb y si se cumple hoy).
- `closeout` resume `verify_task_closeout`: `declared`/`found` tal cual; `evidence` trae
  una entrada por compuerta (`tests`, `atom_or_materialization_link`, `commit`,
  `document`, `external`) con `state`:
  `holds` (la compuerta se cumple), `pending` (falta, y la tarea aún no está en
  `ritual-closeout`) o `failing` (falta y la tarea está en `ritual-closeout`, o el tipo
  declarado no existe en el vocabulario).
- `pills`: `effective_pills` de la tarea (`source: task`) más las pills del Board
  (`source: board`), resueltas a `PillDoc`, igual que las fusiona `deskops next`.
- `atoms`: `effective_atoms` más las referencias `atom-*`, resueltos a `AtomDoc`.

## task

```json
{
  "view": "task", "contract": 1, "root": "/abs/repo",
  "task": {
    CARD…,
    "on_board": true,
    "why": "…", "goal": "…", "scope": "…", "implementation_path": "…",
    "validation": ["…"], "done_when": "…", "references": ["…"], "files": ["…"],
    "depends_on": ["…"], "inherits_from": ["…"], "from_drawer": "", "history": ["task_activates"],
    "pills": [{"id": "…", "title": "…", "source": "task", "what": "…", "when": "…", "how_not": "…"}],
    "atoms": [{"id": "…", "title": "…", "question": "what", "answer": "…"}]
  },
  "next": {"phase": "execution", "ritual": "desk/rituals/execution.md", "next_actions": ["…"], "advance_when": ["…"]},
  "revision": "<sha256 hex>",
  "errors": []
}
```

- `validation`, `done_when` y `references` son los efectivos (con herencia).
- `next` viene de `next_action_report`; si falla, `next` es `null` y la causa va a `errors`.
- `revision` = `sha256(bytes de desk/tasks/Board.md + b"\0" + bytes del archivo de la tarea)`,
  la misma guarda que usa `POST /api/desk/advance` de graph_ui (`DeskRoutes.detail`).

## drawer

```json
{
  "view": "drawer", "contract": 1, "root": "/abs/repo", "count": 1,
  "tasks": [{
    "id": "task-…", "markdown": "<texto completo del archivo>", "title": "…", "status": "deferred",
    "excerpt": ["primeras líneas del cuerpo"], "path": "desk/drawer/tasks/task-….md",
    "command": "deskops add task --root . --from-drawer desk/drawer/tasks/task-….md --title '…'"
  }],
  "errors": []
}
```

- Archivos `desk/drawer/tasks/*.md` salvo `Board.md` y `README.md`.
- `markdown`: el archivo completo, para la vista en crudo (solo lectura).
- `excerpt`: hasta 3 líneas no vacías del cuerpo, sin encabezados ni las pistas en cursiva
  de la plantilla (`_Explain …_`).
- `status` es `null` si el archivo no es un `TaskDoc` válido (la causa va a `errors`).
- `command` es el inicio del comando para autorizar la tarea; el resto de campos
  (`--goal`, `--scope`, `--validation`, `--task-type`…) los decide quien la promueve.

## inbox

```json
{
  "view": "inbox", "contract": 1, "root": "/abs/repo", "count": 2, "open": 1,
  "notes": [{
    "id": "20261104-101500-suggestion-…", "path": "desk/inbox/….md", "kind": "suggestion",
    "title": "…", "sender": "sldb", "target": "deskops", "date": "2026-11-04T10:15:00",
    "status": "open", "acknowledged": false, "acknowledged_by": null, "acknowledged_at": null,
    "body": "…", "revision": "<sha256 de los bytes de la nota>"
  }],
  "errors": []
}
```

- Mismo orden y misma lectura del frontmatter que `deskops message list` (más nuevas
  primero); `acknowledged` es `status == "closed"`, que es lo que escribe `message ack`.
- `date` sale del sello `YYYYMMDD-HHMMSS` del nombre de archivo; sin sello, `null` y aviso.
- `body` es el campo `body` del `InboxNoteDoc`.
- `revision` = `sha256(bytes del archivo de la nota)`: la guarda de las acciones del inbox
  (Reconocer, Pasar al drawer) en la UI.

## agents

```json
{
  "view": "agents", "contract": 1, "root": "/abs/repo",
  "workers": [{"pane": "w1:p1", "kind": "claude", "name": null, "status": "idle", "cwd": "…",
               "title": "…", "workspace": "w1", "seq": 3, "focused": false}],
  "workers_error": null, "live_workers": 1,
  "runs": [{"task_id": "task-…", "run_id": null, "run_dir": null, "commit": null, "mode": "manual", "on_board": false}],
  "runs_total": 122, "runs_limit": 20,
  "errors": []
}
```

- `workers` es la forma pública de `deskops runtime workers` (Herdr, toda la máquina, no
  solo este desk). Si Herdr no responde: `workers: null`, `live_workers: null`,
  `workers_error` con la causa y una entrada en `errors`; nunca una lista vacía muda.
- `runs`: las últimas `--runs` (20 por omisión) líneas de `runs/subagents/index.jsonl`, la
  más nueva primero; `on_board` dice si la tarea sigue en el Board.

## Mapeo de la pantalla de Stitch a fuentes reales

Copiado de `desk/drawer/plans/deskops-ui/alcance.md` (plan deskops-ui, 2026-11-04).

| Elemento de Stitch | Fuente real | Campo de la vista | Si no hay fuente |
|---|---|---|---|
| Columnas por etapa | `current_node` de cada tarea del Board; orden del spec | `board.columns` | — |
| Checklist de gates de la tarjeta | `show_task` → gates, más evidencia de `verify_task_closeout` | `CARD.gates`, `CARD.closeout.evidence` | — |
| "n de m rituales" | conteo de los mismos gates | `CARD.gates_holding`/`gates_total` | — |
| Pills de la tarjeta | `effective_pills` + pills del Board → `PillDoc` | `CARD.pills` (+ `what/when/how_not` en task) | id en `errors` |
| Atoms | `atoms` y referencias `atom-*` → `AtomDoc` | `CARD.atoms` (+ `answer` en task) | id en `errors` |
| "Promover a Atom" | no hay operación | — | botón deshabilitado: "requiere operación de graduación (no existe)" |
| "Iniciar ejecución" | no hay dispatch | — | deshabilitado: "llega con runtime dispatch (fábrica E3)" |
| Avanzar | `POST /api/desk/advance` de graph_ui | `task.revision` | — |
| Diferir a drawer | no hay operación | — | deshabilitado con motivo |
| Drawer: lista y vista raw | `desk/drawer/tasks/*.md` | `drawer.tasks` | — |
| Drawer: "Promover a Desk" | `add task --from-drawer` | `drawer.tasks[].command` | se muestra el comando, no un botón |
| Inbox: lista, lectura, emisor → destino | `InboxNoteDoc` | `inbox.notes` | — |
| Inbox: Reconocer | `deskops message ack` | — (acción de UI05) | — |
| Inbox: Pasar a drawer | `promote inbox-to-drawer-task` | — (acción de UI05) | — |
| Agentes y corridas | `runtime workers`, `runs/subagents/index.jsonl` | `agents.workers`, `agents.runs` | causa en `workers_error` |
| Métricas de cabecera | conteos derivables | `board.counts`, `drawer.count`, `inbox.open`, `agents.live_workers` | ningún porcentaje inventado |
| Hilo del inbox, firmas, prioridad, TTL, autor, versión | no existe | — | no se dibuja |
| Gates por tipo, recibos, `anchor_state` | plan `gates-por-tipo`, sldb GO07 | — | no se dibuja hasta que existan |

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Closeout rules (CC33b): the closeout gate of each factory task type is a `RuleDoc` seed, `deskops/data/rules/rule-closeout-task-<type>.md`, written as a managed seed to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`, glob `rule-closeout-*.md`; a second `--apply` changes nothing). Each is `on_transition`, `severity: error`, `where current_node = "ritual-closeout"` (the source of `task_completes`), subject `model <= <TypeDoc>`, and asks for the evidence receipts of CC33a, accepted and intact: `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")` per kind, `atom|materialization` as an `or` of two. `task.refactor` adds the `goldens` review receipt (`deskops review record --kind goldens`) to the `task.code` rule its family gets; `task.aggregate` asks only for `commit` (no `children` field yet). The kinds per type are data, `deskops/data/rules/closeout-evidence.yaml`, which `deskops closeout verify` and `deskops add task` read (a desk subtype reads its nearest factory ancestor's entry); `tests/test_closeout_rules.py` checks the rules against it. Two `on_write` alert rules cover task fields: `rule-closeout-alert-implicit-code` and `rule-closeout-alert-pill-graduation`.
- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
- Scion autonomy contract (task-scion-autonomy-coordinator-contract): runtime templates add independent `--mode tester`, strict `--context-file` and separate task-data `--task-root`. Coordinators reconcile their own children and Scion activity before selecting work, prepare missing reviews, require independent passing tests, and verify scoped closeout before continuing through phases. Child identities use the full canonical SLDB contract; native label descriptors fit Scion ASCII/63-character limits. RunDocs record immutable launch intent, and the supervisor may mutate modeled workflow through CLIs while implementation stays with executors.
- `deskops review record --kind preflight|bundle --operator <name>` (main en verde, decisión B del coordinador de proyecto con las condiciones del overlord): a desk without a model (CI scenarios, the quickstart) records those receipts by hand. `--operator` is required for both kinds (without it nothing is written); the receipt keeps `engine: human`, names the operator as `actor` and says `no model available` in its title and summary. Real desk tasks still get them from `deskops review preflight|bundle`.
- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).
- `deskops closeout resolved-by --task <id> --reason "..." --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] [--paths ...] [--message ...]` closes a task whose work already entered the history (for example through a PR) before its closeout (`ClosureService.close_resolved_by`). It does not ask for an atom per changed file: at least one `--ref` must be a commit that is HEAD or an ancestor of the `--root` repository, the other refs may be ancestor commits or http(s) URLs, and at least one `--test` is required, each one accepted by the tests gate for the task's `files`. Any ref or test that does not resolve, or a blank reason, is refused with exit 1 and writes nothing. It makes one closing commit with `Task-Id`, `Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and one `Closeout-Test` per test, marks the task `resolved` with `resolved-by` in its history, takes it off the Board and records the index entry with `mode: resolved-by` (`tests/test_closeout_resolved_by.py`).

### Changed

- `deskops desk replace` writes through `sldb.api.replace_text` (CC35d a4, GD27) inside the desk transaction (`doc_access.desk_transaction`), instead of writing the bytes and untracking and re-tracking the document itself. deskops keeps which files the verb reaches (modeled subjects are still pointed at `deskops edit`) and the count guard with its message (`Refusing to replace in <path>: found N occurrence(s) of --old, expected M. The file is unchanged.`), checked before sldb is called. A plain file (a drawer note, an issue body, `tag-namespaces.yaml`) is rewritten as before. A store-tracked file (a role prompt) is now validated under its model and the store's `on_write` rules before it is rewritten and tracked again, and a replacement that breaks it is refused with `Refusing to replace in <path>: <sldb error> The file is unchanged.` (exit 1), the transaction rolled back. A desk without a store still writes the file directly. The rest of CC35d (tag namespaces, the domain tree, `tag_folder`) waits on sldb (H1-H3) (`tests/test_desk_replace.py`).
- `deskops closeout commit` writes no receipt and no longer gates on verify's result: it evaluates the task type's closeout rule on the receipts `deskops closeout verify` wrote (task read at `ritual-closeout`). A blocked commit prints `Closeout gate blocked <task>; the closing commit was not made.`, the declared/found line and alerts of a read-only verify, one `- error: [rules/rule-closeout-<type>] ...` line per finding and `Run 'deskops closeout verify --task <task>' ...`; a task the store does not track cannot be evaluated and is blocked with that reason. The `task_completes` edge condition is `status = "ready_for_testing"` (the `has(closeout_evidence_verified)` fact is gone), so `deskops show task`, `next` and `advance` show the rule's findings on that gate. Editing a contract field after verify leaves the receipts `changed` and blocks again.
- `deskops closeout verify`: the task's `closeout_evidence` only adds kinds to its type's (DA5): an added kind is verified and gets its receipt, and a failure is the alert `added_closeout_evidence_not_verified` instead of a blocking finding; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`. `goldens` is read by the rule from the review receipt, not produced by verify, and `children` is no longer declared, so `closeout_evidence_not_verifiable` is gone. When the atom|materialization gate passes without a linking document (exempt desk, follow-up only, skill guard test) verify writes an accepted `atom` receipt with `value: exempt: <why>` (b3). The `closeout_evidence_not_declared` alert moved to the `rule-closeout-alert-implicit-code` rule.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
- `deskops graph neighbors|missing|reflect` and `deskops drift check` read sldb's project graph of the desk (CC33c, GD21: `sldb.api.edges.project_graph.ProjectGraph` with the configuration of `deskops/graph/desk_graph.py`) instead of a snapshot deskops built and read back. Without `--graph`, `graph neighbors` and `graph reflect` no longer need a prior `graph build` and no longer read `.sldb/runtime/graphs/deskops.kg.json` or the legacy `.sldb/runtime/knowledge_graph.kg.json`; `drift check` reads the graph's edges and its dangling edge targets whether or not a snapshot was built. `--graph <path>` still reads that graph file (`deskops/graph/view.py`, `read_graph_file`). `deskops graph build` still writes the KGDB GraphSnapshot and its NetworkX sibling, unchanged, from the same graph (`deskops/graph/export.py`). `deskops/graph/snapshot.py` is gone (its runtime-path fallback and `read_graph_neighbors` with it), and the atom-reference check of `drift check` reads the frontmatter of the project graph's documents under `desk/` and `docs/` instead of an `rglob` (`grep rglob deskops/graph/` is empty). `graph neighbors` and `graph missing` were compared with the frozen v1 extractors over a copy of the real desk (619 nodes, 296 edges, the same `(source, target, role)` sets and the same missing findings), and `tests/graph_oracle_v1/` was then removed; `tests/closeout_graph_oracle.py` keeps only the lifecycle-transitions oracle.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. CC33c lo decidió (a4): el grafo de proyecto de sldb sigue sin nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json`, así que la excepción queda. Tests en `tests/test_graph_missing_existing_files.py`.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or `deferred`, what a drawer task holds, when `current_node` is empty); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or, when `current_node` is empty (a task outside the lifecycle), `deferred` (a drawer task) or `resolved`/`closed`/`done`/`complete` (a task resolved before the lifecycle, what `closeout retire` removes)); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- Selectors of tracked desk documents resolve through `sldb.api.select_documents` (CC35b, GD23). `doc_access.resolve_document` asks the store twice, in order: by name (`prefix`, where an exact name wins over the one prefix match) under the directory's pattern, then, only if that found nothing, by file name (`path_glob` of `<selector>*.md`), so a ritual tracked as `ritual-execution` in `desk/rituals/execution.md` resolves as `ritual-execution` and as `execution`; an ambiguous query stops there. `resolve_glob`, `resolve_artifact_selector[_multi]`, `resolve_ritual_selector`, `registered_repositories` and the task and pill lookups of `deskops review` use it; the messages are the same (`No <what> file found for selector '<s>'`, `Ambiguous <what> selector '<s>': <paths relative to desk/>`), the ambiguity candidates being the rows sldb names. Gone: `_tracked_task_paths` (which read `.sldb/core/documents/` directly) and the frontmatter-id fallbacks of reviews and rituals (`frontmatter_id`): a legacy task resolves by the `TaskDoc` model family, a review and a ritual by the name the store tracks them by. A file on a tracked surface that the store does not track no longer resolves. The drawer and `desk/issues`, which the store does not track, and a desk without a store keep the disk rule of `desk_paths.resolve_selector` (marked `CC35b-a3`); the `operations.py` aliases graph_ui calls are marked `CC34`. `resolve_artifact_selector_multi` tries its directories in order (an active pill before a drawer pill of the same selector) instead of one candidate set across them. The desk declaration's `include` now names the seeded Board (`desk/tasks/Board.md` as `BoardDoc:Board`) and phase ritual (`desk/rituals/phase.md` as `RitualDoc:ritual-phase`), so `deskops init` and `deskops desk update --apply` track them and a new desk's `deskops edit board Board` resolves (CC35b d1); the Board seed keeps `track: false`.
- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- `__activation_receipts__` and `task_type_activation_receipts` are gone from `deskops/models/task_types.py`: the receipts a type requires live only in its activation `RuleDoc` (CC32). `ReviewDoc`'s docstring says what sldb does with `subject` now that GO07 is in (pins it on save, computes `anchor_state` on read); the model is unchanged. The tests that activate a task write its receipts first with `tests/activation_receipts.py` (accepted and pinned through `sldb.api.transaction`).
- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.
- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).

### Fixed

- `deskops review status` preserves current accepted/rejected dispositions, selects matching exact-input receipts before applying verdict priority, and groups pinned task subjects by task id. Older receipts no longer mask a current acceptance or turn a changed input into a technical failure.

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

### Removed

- `__closeout_evidence__` on the task type classes, the `closeout_evidence_verified` and `pill_graduation_verified` facts, `TasksService.add_closeout_facts`, `ClosureService.has_verified_task_closeout_evidence` and `has_verified_task_pill_graduation`, `task_type_closeout_evidence` and `NOT_YET_VERIFIABLE_EVIDENCE` (CC33b).

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
Cold-bundle de la tarea task-cc34-vistas-de-la-ui-como-viewdoc-servidas-por-sldb-desk-view-py-desaparece: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- deskops view board|task|drawer|inbox --format json idénticos a los goldens capturados primero (a3), salvo revision
- GET /views/board de sldb serve sobre el desk de prueba da el mismo payload
- graph_ui sirve board leyendo la vista nueva y POST /api/desk/advance con ETag viejo da 409
- grep de desk_view y DeskView vacío en deskops/ y en graph_ui frontends
- deskops view board responde en los 6 desks; tiempo frío y caliente registrado
- 4 pasos de deskops y CI completo de graph_ui en clones limpios

