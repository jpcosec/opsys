FILE:desk/tasks/task-scion-autonomy-review-status.md
---
sldb:
  by: agent
  at: '2026-11-10T15:02:34Z'
  authority: generated
  via: save_document_payload
id: task-scion-autonomy-review-status
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- ea42ea58
- tests/test_review_command.py
- desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
depends_on: []
pills: []
files:
- deskops/services/review.py
- tests/test_review_command.py
- desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-review-status.md
---

# Scion autonomy: preserve current accepted review status

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Current accepted/rejected reviews are reported truthfully for the current exact input, preventing false technical failures and review loops.

## Scope

_State what is in scope and what is out of scope._

Only review status classification, its tests and atom-backed documentation; no lifecycle gates, model or CLI grammar changes. Independent runtime-readiness leaf of the autonomy repair phase.

## Implementation Path

_Outline the expected implementation route or affected surface._

Read task and routed workflow; fresh task-only and cold review. Current input identity is the existing SHA256 of exact input_data bytes via review.py _sha; keep its normalization and builders unchanged. In _state_for_key first collect all records for this key; no records means missing. Then filter records by input_sha256 equal to _sha(input_data); records exist but none match means stale, regardless of old verdict. Among matching records use existential priority: accepted > rejected > pending (state reviewed) > incomplete (state technical_failure). This matches existing lifecycle any-current-accepted semantics and does not change gates. Preserve every receipt and provenance. Add all regression scenarios to tests/test_review_command.py using its existing real isolated-desk CLI fixtures. Record atom-review-status-preserves-current-dispositions via CLI before changing docs/operator-manual.md. Hypothetical lookup of existing helpers in the named sources is implementation work, not an unresolved policy decision.

## Validation

_List the checks required before this task can close._

- pytest tests/test_review_command.py
- actual isolated review status after accepted disposition
- pytest at integration

## Done When

_Name the observable condition that makes the task complete._

Current accepted disposition survives status and older rejected/stale receipts do not mask it; input changes report stale; existing pending and technical failure contracts remain; tests and closeout evidence pass.

FILE:deskops/services/review.py
"""Cold context review service behind ``deskops review`` (GC03).

This replaces the two governed ``context_review.py`` scripts with a CLI command
(plan gates-por-tipo, D10). Every run writes the evidence the ritual asks for
under ``runs/subagents/<run>/context-review/<key>/<input sha256>/attempt-N/``
(``input.md``, ``manifest.json``, ``output.md``, ``stderr.log``, ``receipt.json``)
and one ``ReviewDoc`` receipt under ``desk/reviews/``.

Modes:
  node <plan-dir> [IDS...]   review drawer dag.yaml nodes (contract + neighbours + gates)
  preflight <task>           TaskDoc-only review before dispatch
  bundle <task>              cold bundle: TaskDoc + routed rituals + pills + atoms + files + validation
  status [task | plan-dir]   compare current inputs with recorded reviews; no model call
  dispose <review-id>        write the verdict on one pending receipt
  record <task> --kind K     reproduction/goldens/owner receipt from operator evidence; no model call

Caps (owner, D9): an unchanged input is not reviewed again; ``--max-attempts``
(default 2) refuses another *good* attempt on the same key unless ``--force`` with
``--reason``. Transport failures (non-zero exit, timeout, or output without the
``REFORMULACION`` section) do not count against the cap and are recorded as
``technical_ok: false`` with a ``verdict: incomplete`` / ``reason: technical``
receipt, kept separate from comprehension findings (ritual step 5).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from sldb.api.stores.doc_status import doc_status
from sldb.runtime.validation import extract_model_data

from deskops import doc_access
from deskops.config import DeskConfig
from deskops.errors import DomainError
from deskops.errors import UsageError
from deskops.models import ReviewDoc
from deskops.models import RuntimeProfileDoc
from deskops.models import TaskDoc
from deskops.models import BoardDoc


# The verified reviewer profile from desk/rituals/context-review.md step 3 (D4).
SYSTEM = (
    "Revisor barato aislado de un encargo de planificación. Trabajas solo con el input explícito: "
    "sin herramientas, historial ni otras fuentes. No ejecutas nada. Responde en español con estas "
    "secciones exactas: REFORMULACION (propósito, resultado, repo, límites), AMBIGUEDADES (numeradas, "
    'cada una con cita textual del input y qué obligaría a inventar; escribe "ninguna" si no hay), '
    "DRY-RUN (lecturas, cambios previstos, dependencias y validaciones futuras, sin ejecutar), "
    "FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). "
    "REFORMULACION describe el encargo del nodo, no esta revisión. DRY-RUN describe cómo lo ejecutaría "
    "un ejecutor futuro, hipotéticamente y sin ejecutar nada. Si el nodo es un agregado o paquete no "
    "ejecutable, dilo y además recorre cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente "
    "y cómo se valida el resultado conjunto. Máximo 350 palabras."
)
SELECTION = "deepseek-flash: perfil barato verificado en esta máquina por ritual-context-review (D4)"
MODEL = "deepseek/deepseek-flash"
DEFAULT_ENGINE = "runtime-pi-deepseek-flash"
TIMEOUT = 900
# Receipts ``deskops review record`` writes by hand (no model call); the others come from their command.
# Kinds an operator records by hand. ``preflight`` and ``bundle`` also come from their own
# model review; a hand-recorded one keeps ``engine: human`` so it never reads as a model review.
RECORD_KINDS = ("reproduction", "goldens", "owner", "preflight", "bundle")

# Recorded by hand, ``preflight`` and ``bundle`` name their operator (``--operator``) and say
# why no model reviewed them; they are for desks without a model (CI scenarios, the quickstart),
# not a substitute for ``deskops review preflight|bundle`` on a real desk.
HUMAN_REVIEW_KINDS = ("preflight", "bundle")
NO_MODEL_REASON = "no model available"

KEEP = (
    "id",
    "title",
    "kind",
    "owner_repo",
    "node_role",
    "parent_id",
    "children",
    "scope",
    "acceptance",
    "output_scope",
    "depends_on",
    "requires",
)
BASE = ["context-review-guide.md", "brief.md", "alcance.md", "decisiones.md"]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


class Bundle:
    """Accumulates the explicit input.md parts and their per-source hashes."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.sources: list[dict[str, Any]] = []
        self.omitted: list[dict[str, Any]] = []

    def add(self, path: str, text: str, projection: str = "whole_file") -> None:
        self.parts.append(f"FILE:{path}\n{text.rstrip()}\n")
        self.sources.append({"path": path, "sha256": _sha(text.encode()), "projection": projection})

    def omit(self, path: str, reason: str, size: int | None = None) -> None:
        record: dict[str, Any] = {"path": path, "reason": reason}
        if size is not None:
            record["size"] = size
        self.omitted.append(record)

    def close(self, instruction: str) -> bytes:
        self.parts.append(f"FILE:instruccion\n{instruction}\n")
        return "".join(part + "\n" for part in self.parts).encode()


def _technical_ok(attempt_dir: Path) -> bool:
    receipt = attempt_dir / "receipt.json"
    if not receipt.exists():
        return False
    try:
        return bool(json.loads(receipt.read_text(encoding="utf-8")).get("technical_ok"))
    except Exception:
        return False


class ReviewService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    # ------------------------------------------------------------------ paths
    def _reviews_dir(self) -> Path:
        return self.desk_root / "reviews"

    def _evidence_root(self, run_name: str) -> Path:
        return self.root / "runs" / "subagents" / run_name / "context-review"

    def _key_attempts(self, key: str) -> list[Path]:
        base = self.root / "runs" / "subagents"
        if not base.exists():
            return []
        return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))

    def _identity(self) -> str:
        identity = (DeskConfig.load(self.desk_root).project_identity or "").strip()
        if identity and identity != "unknown-project":
            return identity
        return self.root.name

    # ------------------------------------------------------------------ engine
    def _load_engine(self, engine_id: str) -> dict[str, Any]:
        directory = self.desk_root / "runtimes"
        for path in sorted(directory.glob("*.md")) if directory.exists() else []:
            try:
                data = extract_model_data(RuntimeProfileDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("id") == engine_id or path.stem == engine_id:
                return data
        raise DomainError(
            f"RuntimeProfileDoc '{engine_id}' not found under {directory}; "
            f"seed it with `deskops init` / `deskops desk update --apply` or write it by hand."
        )

    def _argv(self, engine: dict[str, Any], input_path: Path) -> list[str]:
        argv = [str(engine.get("binary") or "pi")]
        argv += [str(item) for item in (engine.get("extra_args") or [])]
        if engine.get("system_prompt_flag") and engine.get("system_prompt"):
            argv += [str(engine["system_prompt_flag"]), str(engine["system_prompt"])]
        argv.append(f"@{input_path}")
        return argv

    # ------------------------------------------------------------------ tasks
    def _task_path(self, task_id: str) -> Path:
        tasks_dir = self.desk_root / "tasks"
        try:
            return doc_access.resolve_document(self.root, tasks_dir, task_id, "task", recursive=False)
        except FileNotFoundError:
            raise DomainError(f"Task '{task_id}' not found under {tasks_dir}") from None

    def _resolve_task(self, selector: str) -> tuple[Path, str]:
        """The task file a selector names and the task's full id (its frontmatter ``id``, else the
        file stem). Receipts are keyed and anchored on that id, never on the selector as typed:
        ``task-cc37`` would otherwise give ``doc:<Model>:task-cc37``, a subject no rule matches."""
        task_path = self._task_path(selector)
        task_id = str(self._task_payload(task_path).get("id") or "").strip() or task_path.stem
        return task_path, task_id

    def _task_model(self, task_path: Path) -> str:
        store = self.root / ".sldb"
        if not store.exists():
            return "TaskDoc"
        try:
            status = doc_status(store, task_path.relative_to(self.root).as_posix())
        except Exception:
            return "TaskDoc"
        return status.model or "TaskDoc" if status.exists else "TaskDoc"

    def _task_payload(self, task_path: Path) -> dict[str, Any]:
        return extract_model_data(TaskDoc, task_path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ bundle
    def _preflight_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))
        instruction = (
            f"Preflight solo-TaskDoc de la tarea {task_id}: reformula el encargo tal como lo leería "
            "un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y "
            "da el DRY-RUN sin ejecutar nada. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _resolve_pill(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        try:
            return doc_access.resolve_document(self.root, self.desk_root / "contexts", ref, "pill")
        except (FileNotFoundError, ValueError):
            return None

    def _resolve_atom(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        atom_id = ref.removeprefix("atom:")
        matches = [path for path in (self.desk_root / "atoms").rglob("*.md") if path.stem == atom_id]
        if len(matches) == 1:
            return matches[0]
        return None

    def _bundle_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        payload = self._task_payload(task_path)

        # 1. TaskDoc
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))

        # 2. Rituals routed by the Board (desk/tasks/Board.md), in order.
        board_path = self.desk_root / "tasks" / "Board.md"
        rituals: list[str] = []
        if board_path.is_file():
            try:
                board = extract_model_data(BoardDoc, board_path.read_text(encoding="utf-8"))
                rituals = [str(item) for item in (board.get("rituals") or [])]
            except Exception:
                rituals = []
        if rituals:
            for ritual_ref in rituals:
                ritual_path = Path(ritual_ref)
                if not ritual_path.is_absolute():
                    ritual_path = self.root / ritual_path
                if ritual_path.is_file():
                    bundle.add(ritual_path.relative_to(self.root).as_posix(), ritual_path.read_text(encoding="utf-8"))
                else:
                    bundle.omit(ritual_ref, "missing")
        else:
            bundle.omit("desk/tasks/Board.md rituals", "missing")

        # 3. Bound pills (TaskDoc.pills), in order.
        for pill_ref in _coerce_list(payload.get("pills")):
            pill_path = self._resolve_pill(pill_ref)
            if pill_path is not None:
                bundle.add(pill_path.relative_to(self.root).as_posix(), pill_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(pill_ref, "unresolved")

        # 4. Bound atoms (TaskDoc.atoms), in order.
        for atom_ref in _coerce_list(payload.get("atoms")):
            atom_path = self._resolve_atom(atom_ref)
            if atom_path is not None:
                bundle.add(atom_path.relative_to(self.root).as_posix(), atom_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(atom_ref, "unresolved")

        # 5. Files the TaskDoc names, under 60 KB, files only, present.
        for file_ref in _coerce_list(payload.get("files")):
            file_path = Path(file_ref)
            if not file_path.is_absolute():
                file_path = self.root / file_path
            if not file_path.exists():
                bundle.omit(file_ref, "missing")
                continue
            if file_path.is_dir():
                bundle.omit(file_ref, "directory")
                continue
            size = file_path.stat().st_size
            if size >= 60_000:
                bundle.omit(file_ref, "size>=60000", size=size)
                continue
            bundle.add(file_ref, file_path.read_text(encoding="utf-8", errors="replace"))

        # 6. The TaskDoc validation section as the instruction.
        validation = _coerce_list(payload.get("validation"))
        validation_text = "\n".join(f"- {item}" for item in validation) if validation else "(sin validación declarada)"
        instruction = (
            f"Cold-bundle de la tarea {task_id}: con el TaskDoc, los rituales enrutados por el Board, "
            "las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el "
            "encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. "
            "No ejecutes nada.\n\nSección de validación del TaskDoc:\n" + validation_text
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    # ------------------------------------------------------------------ node
    def _load_dag(self, plan_dir: Path) -> tuple[dict, dict]:
        dag_path = plan_dir / "dag.yaml"
        if not dag_path.is_file():
            raise DomainError(f"No dag.yaml in plan directory {plan_dir}")
        try:
            dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise DomainError(f"Could not parse {dag_path}: {exc}") from exc
        nodes: dict[str, dict] = {}
        for task in dag.get("tasks") or []:
            nodes[task["id"]] = task
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            nodes[package["id"]] = package
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            nodes[root["id"]] = root
        return dag, nodes

    def _plan_nodes(self, dag: dict) -> list[str]:
        order: list[str] = []
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            order.append(root["id"])
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            order.append(package["id"])
        for task in dag.get("tasks") or []:
            order.append(task["id"])
        return list(dict.fromkeys(order))

    @staticmethod
    def _contract(node: dict) -> dict:
        return {key: node[key] for key in KEEP if key in node}

    @staticmethod
    def _neighbours(dag: dict, nodes: dict, node: dict) -> tuple[list[dict], dict]:
        tasks = {task["id"]: task for task in dag.get("tasks") or []}
        packages = {package["id"] for package in (dag.get("hierarchy") or {}).get("packages") or []}
        node_id = node["id"]
        if node_id == "ROOT":
            ids = list(node.get("children") or [])
        elif node_id in packages:
            ids = list(node.get("children") or [])
            inside = set(ids)
            for child in ids[:]:
                ids += [x for x in (tasks.get(child) or {}).get("depends_on") or [] if x not in inside]
        else:
            ids = list(node.get("depends_on") or [])
            ids += [task["id"] for task in (dag.get("tasks") or []) if node_id in (task.get("depends_on") or [])]
            ids += [node.get("parent_id") or ""]
        ids = list(dict.fromkeys(item for item in ids if item and item != node_id))
        gates_ids = list(node.get("requires") or [])
        gates_ids += [
            gate for gate, value in (dag.get("gates") or {}).items()
            if isinstance(value, dict) and value.get("produced_by") == node_id
        ]
        gates_ids += [
            gate for gate in (dag.get("gates") or {}) if gate in str(ReviewService._contract(node))
        ]
        return [nodes[item] for item in ids if item in nodes], {
            gate: (dag.get("gates") or {})[gate] for gate in dict.fromkeys(gates_ids) if gate in (dag.get("gates") or {})
        }

    def _node_input(self, plan_dir: Path, dag: dict, nodes: dict, node: dict) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        for rel in BASE:
            source = plan_dir / rel
            if source.is_file():
                bundle.add(f"{plan_rel}/{rel}", source.read_text(encoding="utf-8"))
            else:
                bundle.omit(f"{plan_rel}/{rel}", "missing")

        node_id = node["id"]
        bundle.add(f"{plan_rel}/dag.yaml#node:{node_id}", yaml.safe_dump(self._contract(node), allow_unicode=True, sort_keys=False), "node_contract")
        neighbours, gates = self._neighbours(dag, nodes, node)
        for neighbour in neighbours:
            bundle.add(f"{plan_rel}/dag.yaml#edge:{neighbour['id']}", yaml.safe_dump(self._contract(neighbour), allow_unicode=True, sort_keys=False), "edge_contract")
        if gates:
            bundle.add(f"{plan_rel}/dag.yaml#gates", yaml.safe_dump(gates, allow_unicode=True, sort_keys=False), "gate_contracts")

        is_aggregate = node_id == "ROOT" or node_id.startswith("PK")
        instruction = (
            f"Revisa el nodo {node_id} siguiendo context-review-guide.md. "
            + (
                "Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de "
                "sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. "
                if is_aggregate
                else ""
            )
            + "Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _find_plan_dir(self, plan_id: str) -> Path | None:
        plans_root = self.desk_root / "drawer" / "plans"
        if not plans_root.exists():
            return None
        for dag_path in sorted(plans_root.rglob("dag.yaml")):
            try:
                dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(dag, dict) and dag.get("id") == plan_id:
                return dag_path.parent
        return None

    # ------------------------------------------------------------------ caps
    def _next_attempt_dir(
        self,
        run_name: str,
        key: str,
        input_sha256: str,
        max_attempts: int,
        force: bool,
    ) -> Path | None:
        attempts = self._key_attempts(key)
        prior = [attempt for attempt in attempts if attempt.parent.name == input_sha256]
        if prior and any(_technical_ok(attempt) for attempt in prior) and not force:
            return None  # unchanged input already reviewed
        good = sum(1 for attempt in attempts if _technical_ok(attempt))
        if not prior and good >= max_attempts and not force:
            raise DomainError(
                f"{key}: {good} intentos ya; tope --max-attempts {max_attempts} "
                "(usa --force con --reason si el input cambió de verdad)"
            )
        out = self._evidence_root(run_name) / key / input_sha256 / f"attempt-{len(prior) + 1}"
        out.mkdir(parents=True, exist_ok=True)
        return out

    # ------------------------------------------------------------------ run
    def _run_one(
        self,
        *,
        run_name: str,
        key: str,
        input_data: bytes,
        sources: list[dict],
        omitted: list[dict],
        engine_id: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
        kind: str,
        subject: str,
        subject_ref: str,
        node_id: str | None,
        plan_id: str | None = None,
    ) -> dict[str, Any]:
        input_sha256 = _sha(input_data)
        attempt_dir = self._next_attempt_dir(run_name, key, input_sha256, max_attempts, force)
        if attempt_dir is None:
            return {"key": key, "state": "unchanged", "input_sha256": input_sha256}

        (attempt_dir / "input.md").write_bytes(input_data)
        engine = self._load_engine(engine_id)
        argv = self._argv(engine, attempt_dir / "input.md")
        start = _now()
        try:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
            stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as exc:
            detail = ""
            if isinstance(getattr(exc, "stderr", None), bytes):
                detail = exc.stderr.decode(errors="replace")
            elif isinstance(getattr(exc, "stderr", None), str):
                detail = exc.stderr or ""
            stdout, stderr, returncode = "", f"timeout after {timeout}s\n{detail}", None
        end = _now()

        (attempt_dir / "output.md").write_text(stdout, encoding="utf-8")
        (attempt_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        technical_ok = returncode == 0 and "REFORMULACION" in stdout

        manifest: dict[str, Any] = {
            "key": key,
            "input_sha256": input_sha256,
            "argv": argv,
            "model": MODEL,
            "profile": engine_id,
            "selection_reason": SELECTION,
            "sources": sources,
            "omitted_sources": omitted,
            "started": start,
            "finished": end,
        }
        if force and reason:
            manifest["retry_reason"] = reason
        (attempt_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        receipt: dict[str, Any] = {
            "key": key,
            "technical_ok": technical_ok,
            "returncode": returncode,
            "input_sha256": input_sha256,
            "output_sha256": _sha(stdout.encode()),
            "start": start,
            "end": end,
        }
        (attempt_dir / "receipt.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        run_dir = attempt_dir.relative_to(self.root).as_posix()
        if technical_ok:
            verdict = "pending"
            review_reason = reason if force else ""
        else:
            verdict = "incomplete"
            review_reason = "technical"

        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref=subject_ref,
            engine=engine_id,
            run_dir=run_dir,
            input_sha256=input_sha256,
            output_sha256=receipt["output_sha256"],
            verdict=verdict,
            reason=review_reason,
            node_id=node_id,
            plan_id=plan_id,
        )

        return {
            "key": key,
            "state": "reviewed" if technical_ok else "technical_failure",
            "input_sha256": input_sha256,
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "run_dir": run_dir,
            "technical_ok": technical_ok,
        }

    def _next_review_number(self, review_dir: Path, kind: str, node: bool) -> int:
        if not review_dir.exists():
            return 1
        prefix = "node-" if node else f"{kind}-"
        matches = [path for path in review_dir.glob(f"{prefix}*.md") if path.stem.startswith(prefix)]
        return len(matches) + 1

    def _write_review(
        self,
        *,
        kind: str,
        subject: str,
        subject_ref: str,
        engine: str,
        run_dir: str,
        input_sha256: str,
        output_sha256: str,
        verdict: str,
        reason: str,
        node_id: str | None,
        plan_id: str | None = None,
        summary: str | None = None,
        actor: str | None = None,
        title: str | None = None,
    ) -> tuple[str, Path]:
        if node_id is not None:
            node_lower = node_id.lower()
            plan_id = plan_id or (subject_ref.split("/dag.yaml#node:", 1)[0].rsplit("/", 1)[-1] if "/" in subject_ref else "")
            review_dir = self._reviews_dir() / f"{plan_id}-{node_lower}"
            n = self._next_review_number(review_dir, kind, node=True)
            review_id = f"review-{plan_id}-{node_lower}-node-{n}"
            title = title or f"Node review of {node_id}"
        else:
            task_id = subject.rsplit(":", 1)[-1].split("@", 1)[0]
            review_dir = self._reviews_dir() / task_id
            n = self._next_review_number(review_dir, kind, node=False)
            review_id = f"review-{task_id}-{kind}-{n}"
            title = title or f"{kind.capitalize()} review of {task_id}"

        path = review_dir / (f"node-{n}.md" if node_id is not None else f"{kind}-{n}.md")
        payload: dict[str, Any] = {
            "id": review_id,
            "title": title,
            "kind": kind,
            "subject": subject,
            "subject_ref": subject_ref,
            "engine": engine,
            "actor": actor or self._identity(),
            "run_dir": run_dir,
            "input_sha256": input_sha256,
            "output_sha256": output_sha256,
            "verdict": verdict,
            "reason": reason,
            "created_at": _now(),
            "disposed_at": "",
            "disposed_by": "",
            "summary": summary if summary is not None else f"{kind} review; engine {engine}; evidence under {run_dir}.",
            "disposition": "",
            "tags": ["workspace:desk"],
        }
        doc_access.create_doc(self.root, path, ReviewDoc, payload, review_id)
        return review_id, path

    # ------------------------------------------------------------------ record
    def record_receipt(
        self, task_id: str, kind: str, evidence: list[str], reason: str, operator: str | None = None
    ) -> dict[str, Any]:
        """A receipt the desk operator records without a model call (reproduction, goldens, owner,
        and preflight or bundle from operator evidence, always with ``engine: human``).

        Every ``evidence`` path must be an existing file inside the root; otherwise nothing is
        written. ``input_sha256`` hashes ``<path>\\n<content>\\n`` of each file, paths POSIX-relative
        to the root, sorted, without repeats (b1); empty without evidence. The verdict stays
        ``pending`` until ``deskops review dispose`` (r4).
        """
        if kind not in RECORD_KINDS:
            raise UsageError(
                f"--kind {kind} is not recorded by hand; use one of {', '.join(RECORD_KINDS)} "
                "(node comes from its own review command)"
            )
        if not (reason and reason.strip()):
            raise UsageError("--reason is required")
        operator = (operator or "").strip()
        if kind in HUMAN_REVIEW_KINDS and not operator:
            raise UsageError(
                f"--kind {kind} recorded by hand requires --operator <name>: the receipt names the "
                f"human who reviewed instead of a model ({NO_MODEL_REASON})"
            )
        paths: list[str] = []
        for raw in evidence:
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = self.root / candidate
            resolved = candidate.resolve()
            if not resolved.is_relative_to(self.root) or not resolved.is_file():
                raise DomainError(f"evidence not found: {raw}")
            paths.append(resolved.relative_to(self.root).as_posix())
        paths = sorted(set(paths))
        if not paths and kind != "owner":
            raise UsageError(f"--kind {kind} requires at least one --evidence")

        task_path, task_id = self._resolve_task(task_id)
        subject = f"doc:{self._task_model(task_path)}:{task_id}"
        input_sha256 = ""
        if paths:
            data = b"".join(rel.encode() + b"\n" + (self.root / rel).read_bytes() + b"\n" for rel in paths)
            input_sha256 = _sha(data)
        actor = operator or self._identity()
        summary = f"{kind} receipt recorded by {actor}; evidence: {', '.join(paths) if paths else '(none)'}"
        title = None
        if kind in HUMAN_REVIEW_KINDS:
            summary = (
                f"{kind} receipt recorded by hand by operator {operator}, not by a model review "
                f"(engine human; {NO_MODEL_REASON}); evidence: {', '.join(paths)}"
            )
            title = f"{kind.capitalize()} receipt of {task_id} by operator {operator} ({NO_MODEL_REASON})"
        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref="",
            engine="human",
            run_dir="",
            input_sha256=input_sha256,
            output_sha256="",
            verdict="pending",
            reason=reason,
            node_id=None,
            summary=summary,
            actor=actor,
            title=title,
        )
        return {
            "key": f"{task_id}/{kind}",
            "state": "recorded",
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "evidence": paths,
            "input_sha256": input_sha256,
            "engine": "human",
            "operator": actor,
            "no_model_reason": NO_MODEL_REASON if kind in HUMAN_REVIEW_KINDS else "",
        }

    # ------------------------------------------------------------------ dispose
    def dispose(self, review_id: str, verdict: str, reason: str) -> dict[str, Any]:
        path = self._resolve_review_path(review_id)
        payload = doc_access.read_doc(path, ReviewDoc)
        if (payload.get("verdict") or "pending") != "pending":
            raise DomainError(f"Review '{review_id}' already has verdict '{payload.get('verdict')}'; only a pending review can be disposed.")
        payload["verdict"] = verdict
        payload["reason"] = reason
        payload["disposed_at"] = _now()
        payload["disposed_by"] = self._identity()
        payload["disposition"] = f"Verdict {verdict}: {reason}"
        doc_access.write_doc(self.root, path, ReviewDoc, payload)
        return {
            "review_id": review_id,
            "verdict": verdict,
            "reason": reason,
            "disposed_at": payload["disposed_at"],
            "disposed_by": payload["disposed_by"],
        }

    def _resolve_review_path(self, review_id: str) -> Path:
        reviews_dir = self._reviews_dir()
        matches: list[Path] = []
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                payload = extract_model_data(ReviewDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if payload.get("id") == review_id:
                matches.append(path)
        if not matches:
            raise DomainError(f"Review '{review_id}' not found under {reviews_dir}")
        if len(matches) > 1:
            names = ", ".join(str(path.relative_to(self.desk_root)) for path in matches)
            raise DomainError(f"Ambiguous review selector '{review_id}': {names}")
        return matches[0]

    # ------------------------------------------------------------------ status
    def _review_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        reviews_dir = self._reviews_dir()
        if not reviews_dir.exists():
            return records
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                records.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
            except Exception:
                continue
        return records

    def _state_for_key(self, key: str, input_data: bytes) -> dict[str, Any]:
        current_sha = _sha(input_data)
        records = [
            record
            for record in self._review_records()
            if self._record_key(record) == key
        ]
        if not records:
            state = "missing"
        else:
            current = [record for record in records if record.get("input_sha256") == current_sha]
            verdicts = {record.get("verdict") for record in current}
            if not current:
                state = "stale"
            elif "accepted" in verdicts:
                state = "accepted"
            elif "rejected" in verdicts:
                state = "rejected"
            elif "pending" in verdicts:
                state = "reviewed"
            else:
                state = "technical_failure"
        return {"key": key, "state": state, "input_sha256": current_sha}

    def _record_key(self, record: dict[str, Any]) -> str:
        subject = str(record.get("subject") or "")
        subject_ref = str(record.get("subject_ref") or "")
        kind = str(record.get("kind") or "")
        if subject:
            task_id = subject.split("@", 1)[0].rsplit(":", 1)[-1]
            return f"{task_id}/{kind}"
        if subject_ref:
            node_id = subject_ref.rsplit("#node:", 1)[-1]
            plan_path = subject_ref.split("#node:", 1)[0]
            plan_dir = Path(plan_path)
            if not plan_dir.is_absolute():
                plan_dir = self.root / plan_dir
            try:
                dag = yaml.safe_load((plan_dir / "dag.yaml").read_text(encoding="utf-8"))
                plan_id = dag["id"]
            except Exception:
                plan_id = plan_path.rsplit("/", 1)[-1]
            return f"{plan_id}/{node_id}"
        return f"unknown/{kind}"

    def status(self, target: str | None) -> list[dict[str, Any]]:
        if target:
            if self._is_plan_dir(target):
                return self._status_plan(target)
            return self._status_task(target)
        # No target: every key that has at least one ReviewDoc.
        keys: list[str] = []
        for record in self._review_records():
            key = self._record_key(record)
            if key not in keys and not key.startswith("unknown/"):
                keys.append(key)
        reports: list[dict[str, Any]] = []
        for key in keys:
            input_data = self._input_for_key(key)
            if input_data is None:
                reports.append({"key": key, "state": "missing", "input_sha256": ""})
            else:
                reports.append(self._state_for_key(key, input_data))
        return reports

    def _is_plan_dir(self, target: str) -> bool:
        plan_dir = Path(target)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        return (plan_dir / "dag.yaml").is_file()

    def _status_task(self, task_id: str) -> list[dict[str, Any]]:
        task_path, task_id = self._resolve_task(task_id)
        reports: list[dict[str, Any]] = []
        for mode, builder in (
            ("preflight", self._preflight_input),
            ("bundle", self._bundle_input),
        ):
            input_data, _, _ = builder(task_path, task_id)
            reports.append(self._state_for_key(f"{task_id}/{mode}", input_data))
        return reports

    def _status_plan(self, plan_dir_str: str) -> list[dict[str, Any]]:
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        reports: list[dict[str, Any]] = []
        for node_id in self._plan_nodes(dag):
            node = nodes[node_id]
            input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
            reports.append(self._state_for_key(f"{dag['id']}/{node_id}", input_data))
        return reports

    def _input_for_key(self, key: str) -> bytes | None:
        if "/preflight" in key or "/bundle" in key:
            task_id, _, mode = key.rpartition("/")
            if mode not in {"preflight", "bundle"}:
                return None
            try:
                task_path = self._task_path(task_id)
            except DomainError:
                return None
            builder = self._preflight_input if mode == "preflight" else self._bundle_input
            input_data, _, _ = builder(task_path, task_id)
            return input_data
        # node key <plan-id>/<NODE>
        parts = key.split("/", 1)
        if len(parts) != 2:
            return None
        plan_id, node_id = parts
        plan_dir = self._find_plan_dir(plan_id)
        if plan_dir is None:
            return None
        dag, nodes = self._load_dag(plan_dir)
        node = nodes.get(node_id)
        if node is None:
            return None
        input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
        return input_data

    # ------------------------------------------------------------------ public run
    def run_task(
        self,
        mode: str,
        task_id: str,
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> dict[str, Any]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        task_path, task_id = self._resolve_task(task_id)
        model = self._task_model(task_path)
        subject = f"doc:{model}:{task_id}"
        builder = self._preflight_input if mode == "preflight" else self._bundle_input
        input_data, sources, omitted = builder(task_path, task_id)
        return self._run_one(
            run_name=run_name,
            key=f"{task_id}/{mode}",
            input_data=input_data,
            sources=sources,
            omitted=omitted,
            engine_id=engine,
            max_attempts=max_attempts,
            force=force,
            reason=reason,
            timeout=timeout,
            kind=mode,
            subject=subject,
            subject_ref="",
            node_id=None,
        )

    def run_nodes(
        self,
        plan_dir_str: str,
        ids: list[str],
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> list[dict[str, Any]]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        selected = ids or self._plan_nodes(dag)
        reports: list[dict[str, Any]] = []
        for node_id in selected:
            if node_id not in nodes:
                raise DomainError(f"Unknown node '{node_id}' in {plan_dir / 'dag.yaml'}")
            node = nodes[node_id]
            input_data, sources, omitted = self._node_input(plan_dir, dag, nodes, node)
            reports.append(
                self._run_one(
                    run_name=run_name,
                    key=f"{dag['id']}/{node_id}",
                    input_data=input_data,
                    sources=sources,
                    omitted=omitted,
                    engine_id=engine,
                    max_attempts=max_attempts,
                    force=force,
                    reason=reason,
                    timeout=timeout,
                    kind="node",
                    subject="",
                    subject_ref=f"{plan_rel}/dag.yaml#node:{node_id}",
                    node_id=node_id,
                    plan_id=dag["id"],
                )
            )
        return reports

FILE:tests/test_review_command.py
"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
PLAN_SRC = ROOT / "desk" / "drawer" / "plans" / "gates-por-tipo"


FAKE_PI = """#!/usr/bin/env python3
import os
import sys
import time

log = os.environ.get("FAKE_PI_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(sys.argv[1:]) + "\\n")

mode = os.environ.get("FAKE_PI_MODE", "ok")
if mode == "fail":
    sys.exit(1)
if mode == "no-reformulacion":
    print("sin seccion")
    sys.exit(0)
if mode == "sleep":
    time.sleep(5)
    print("REFORMULACION\\nDRY-RUN: nada.")
    sys.exit(0)
print(
    "REFORMULACION\\n"
    "Propósito: revisar el encargo.\\n"
    "AMBIGUEDADES: ninguna.\\n"
    "DRY-RUN: leer, proponer, validar, sin ejecutar.\\n"
    "FUTURO: otro nodo o un humano."
)
sys.exit(0)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(ROOT), env.get("PYTHONPATH"))))
    return env


def _run(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*argv], cwd=root, env=env or _env(), capture_output=True, text=True)


def _deskops(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root), env=env)


@pytest.fixture
def fake_pi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(FAKE_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("FAKE_PI_MODE", "ok")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return bin_dir, log


def _pi_calls(log: Path) -> int:
    if not log.exists():
        return 0
    return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


def _add_task(root: Path, *, title: str = "X", task_type: str = "task.code") -> str:
    result = _deskops(
        root,
        "add",
        "task",
        "--title",
        title,
        "--goal",
        "review goal",
        "--scope",
        "review scope",
        "--validation",
        "pytest",
        "--task-type",
        task_type,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return f"task-{title.lower().replace(' ', '-')}"


def _attempt_dirs(root: Path, key: str) -> list[Path]:
    base = root / "runs" / "subagents"
    if not base.exists():
        return []
    return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))


def _review_docs(root: Path) -> list[dict]:
    reviews = root / "desk" / "reviews"
    if not reviews.exists():
        return []
    docs: list[dict] = []
    for path in sorted(reviews.rglob("*.md")):
        docs.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
    return docs


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_writes_attempt_evidence_and_receipt(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 1
    attempt = attempts[0]
    assert attempt.name == "attempt-1"
    for name in ("input.md", "manifest.json", "output.md", "stderr.log", "receipt.json"):
        assert (attempt / name).is_file(), name

    input_bytes = (attempt / "input.md").read_bytes()
    assert input_bytes.decode().startswith("FILE:desk/tasks/task-x.md\n")

    manifest = _json(attempt / "manifest.json")
    assert manifest["input_sha256"] == __import__("hashlib").sha256(input_bytes).hexdigest()
    assert manifest["sources"][0]["path"] == "desk/tasks/task-x.md"
    assert manifest["argv"][0] == "pi"
    assert manifest["argv"][-1].startswith("@")

    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is True
    assert receipt["returncode"] == 0
    assert receipt["input_sha256"] == manifest["input_sha256"]

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "pending"
    assert doc["subject"] == "doc:TaskCodeDoc:task-x"
    assert doc["run_dir"] == attempt.relative_to(root).as_posix()
    assert doc["input_sha256"] == manifest["input_sha256"]
    assert doc["output_sha256"] == receipt["output_sha256"]


def test_unchanged_second_run_is_reviewed_and_does_not_call_the_model(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    calls_after_first = _pi_calls(_log)
    assert calls_after_first == 1

    second = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout
    assert _pi_calls(_log) == calls_after_first
    assert len(_attempt_dirs(root, "task-x/preflight")) == 1

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "reviewed"


def test_edited_goal_is_stale_and_next_run_uses_a_new_sha(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    first_sha = _attempt_dirs(root, "task-x/preflight")[0].parent.name

    edit = _deskops(root, "edit", "task", "task-x", "goal", "goal changed")
    assert edit.returncode == 0, edit.stdout + edit.stderr

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "stale"

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    new_shas = {attempt.parent.name for attempt in attempts}
    assert first_sha in new_shas
    assert len(new_shas) == 2


def test_bundle_includes_rituals_pills_and_files_in_order(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    pill = _deskops(
        root,
        "add",
        "pill",
        "--title",
        "Guardrail",
        "--what",
        "keep layers clean",
        "--why",
        "safety",
        "--when",
        "always",
        "--where",
        "desk",
        "--how",
        "read first",
        "--how-not",
        "skip it",
    )
    assert pill.returncode == 0, pill.stdout + pill.stderr
    assert _deskops(root, "bind", "pill", "task-x", "pill-guardrail").returncode == 0

    doc = root / "docs" / "foo.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Foo\nsmall file\n", encoding="utf-8")
    edit = _deskops(root, "edit", "task", "task-x", "files", '["docs/foo.md"]')
    assert edit.returncode == 0, edit.stdout + edit.stderr

    assert _deskops(root, "review", "bundle", "task-x", "--run", "test-run").returncode == 0

    attempt = _attempt_dirs(root, "task-x/bundle")[0]
    input_text = (attempt / "input.md").read_text(encoding="utf-8")
    file_headers = [line for line in input_text.splitlines() if line.startswith("FILE:")]
    assert file_headers[0] == "FILE:desk/tasks/task-x.md"
    assert "FILE:desk/rituals/phase.md" in file_headers
    assert "FILE:desk/rituals/execution.md" in file_headers
    assert "FILE:desk/rituals/testing.md" in file_headers
    assert "FILE:desk/rituals/closeout.md" in file_headers
    assert "FILE:desk/contexts/pill-guardrail.md" in file_headers
    assert "FILE:docs/foo.md" in file_headers
    assert file_headers[-1] == "FILE:instruccion"

    # Order: task, rituals, pill, file, instruction.
    ordered = [
        "FILE:desk/tasks/task-x.md",
        "FILE:desk/rituals/phase.md",
        "FILE:desk/rituals/execution.md",
        "FILE:desk/rituals/testing.md",
        "FILE:desk/rituals/closeout.md",
        "FILE:desk/contexts/pill-guardrail.md",
        "FILE:docs/foo.md",
        "FILE:instruccion",
    ]
    assert file_headers == ordered


def test_node_writes_one_review_doc_per_node(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)

    result = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    node_ids = [doc["id"] for doc in node_docs]
    assert "review-deskops-gates-por-tipo-gc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-pc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-root-node-1" in node_ids
    for doc in node_docs:
        assert doc["subject"] == ""
        assert doc["subject_ref"].startswith("desk/drawer/plans/gates-por-tipo/dag.yaml#node:")
        assert doc["verdict"] == "pending"


def test_dispose_writes_the_verdict_and_a_second_dispose_fails(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0

    disposed = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "accepted",
        "--reason",
        "looks right",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "looks right"
    assert doc["disposed_at"]
    assert doc["disposed_by"]

    again = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "rejected",
        "--reason",
        "changed my mind",
    )
    assert again.returncode == 1
    assert "already has verdict" in again.stdout


def test_third_good_attempt_on_the_same_key_fails_without_force(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)
    brief = plan_dir / "brief.md"
    log = fake_pi[1]

    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change one\n", encoding="utf-8")
    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    assert _pi_calls(log) == 2

    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change two\n", encoding="utf-8")
    third = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r")
    assert third.returncode == 1
    assert "tope --max-attempts" in third.stdout
    assert _pi_calls(log) == 2


def test_transport_failure_leaves_technical_failure_and_incomplete(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "fail")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is False
    assert receipt["returncode"] == 1

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_output_without_reformulacion_is_a_transport_failure(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "no-reformulacion")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    assert _json(attempt / "receipt.json")["technical_ok"] is False
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_force_requires_reason(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--run", "test-run")
    assert result.returncode == 2
    assert "--force requires --reason" in result.stdout


def test_force_with_reason_retries_the_same_input(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    assert _pi_calls(log) == 1

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--reason", "again", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _pi_calls(log) == 2

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    manifest = _json(attempts[1] / "manifest.json")
    assert manifest["retry_reason"] == "again"
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-2"]
    assert len(docs) == 1
    assert docs[0]["reason"] == "again"


def test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently(
    tmp_path: Path,
) -> None:
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0

    profile = root / "desk" / "runtimes" / "runtime-pi-deepseek-flash.md"
    assert profile.is_file()
    first = profile.read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == first

    # An existing profile is never overwritten.
    profile.write_text("# my own profile\n", encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == "# my own profile\n"


@pytest.mark.parametrize(
    ("receipts", "expected"),
    [
        ([], "missing"),
        ([("old", "accepted"), ("old", "rejected"), ("old", "incomplete")], "stale"),
        ([("current", "incomplete")], "technical_failure"),
        ([("current", "incomplete"), ("current", "pending")], "reviewed"),
        ([("current", "pending"), ("current", "rejected")], "rejected"),
        ([("current", "accepted"), ("current", "rejected"), ("current", "pending"),
          ("current", "incomplete"), ("old", "rejected")], "accepted"),
        ([("old", "accepted"), ("current", "rejected")], "rejected"),
    ],
)
def test_status_classifies_only_current_receipts_without_mutating_evidence(
    lifecycle_desk: Path, receipts: list[tuple[str, str]], expected: str
) -> None:
    from deskops.cli.main import main
    from deskops.services.review import ReviewService, _sha

    root = lifecycle_desk
    assert main([
        "add", "task", "--title", "Status", "--goal", "review goal",
        "--scope", "review scope", "--validation", "pytest", "--task-type", "task.code",
        "--root", str(root),
    ]) == 0
    service = ReviewService(root)
    task_path, task_id = service._resolve_task("task-status")
    input_data, _, _ = service._preflight_input(task_path, task_id)
    for index, (identity, verdict) in enumerate(receipts):
        evidence = root / "runs" / "subagents" / f"receipt-{index}"
        evidence.mkdir(parents=True)
        (evidence / "input.md").write_bytes(input_data if identity == "current" else b"old input\n")
        (evidence / "manifest.json").write_text(json.dumps({"profile": "test", "attempt": index}))
        review_id, _ = service._write_review(
            kind="preflight", subject=f"doc:TaskCodeDoc:{task_id}", subject_ref="",
            engine="test", run_dir=evidence.relative_to(root).as_posix(),
            input_sha256=_sha(input_data) if identity == "current" else _sha(b"old input\n"),
            output_sha256=_sha(b"review output"),
            verdict="pending" if verdict in {"accepted", "rejected"} else verdict, reason="test evidence",
            node_id=None,
        )
        if verdict in {"accepted", "rejected"}:
            service.dispose(review_id, verdict, "test disposition")
    preserved = {
        path: path.read_bytes()
        for directory in (root / "desk" / "reviews", root / "runs")
        if directory.exists() for path in directory.rglob("*") if path.is_file()
    }
    reports = {item["key"]: item for item in service.status("task-status")}
    assert reports["task-status/preflight"] == {
        "key": "task-status/preflight", "state": expected, "input_sha256": _sha(input_data),
    }
    assert reports["task-status/bundle"]["state"] == "missing"
    assert all(path.read_bytes() == content for path, content in preserved.items())


@pytest.mark.parametrize("tracked", [False, True], ids=["plain", "pinned"])
def test_disposed_review_status_uses_task_identity(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], tracked: bool
) -> None:
    root = lifecycle_desk
    if not tracked:
        shutil.rmtree(root / ".sldb")
    _add_task(root, title="Identity")
    result = _deskops(root, "review", "preflight", "task-identity", "--run", "identity")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review_docs(root)[0]
    assert doc["subject"].startswith("doc:TaskCodeDoc:task-identity" if tracked else "doc:TaskDoc:task-identity")
    disposed = _deskops(root, "review", "dispose", doc["id"], "--verdict", "accepted", "--reason", "correct")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    subject = _review_docs(root)[0]["subject"]
    if tracked:
        # GO07 pins the actual stored subject on disposition, not a parser fixture.
        assert "@sha256:" in subject
    else:
        assert "@" not in subject
    for target in [("task-identity",), ()]:
        status = _deskops(root, "review", "status", *target, "--format", "json")
        assert status.returncode == 0, status.stdout + status.stderr
        report = next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")
        assert report["state"] == "accepted"
    edit = _deskops(root, "edit", "task", "task-identity", "goal", "changed input")
    assert edit.returncode == 0, edit.stdout + edit.stderr
    status = _deskops(root, "review", "status", "task-identity", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    assert next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")["state"] == "stale"

FILE:desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
---
sldb:
  by: agent
  at: '2026-11-10T14:36:44Z'
  authority: generated
  via: create_document
id: atom-review-status-preserves-current-dispositions
title: Review status preserves current dispositions
five_wh_one_plus: how
tags:
- system:deskops
- topic:reviews
---

# Review status preserves current dispositions

## Answer

Review status groups task receipts by task id and kind, whether their subject is plain or pinned with a SHA256 anchor. The current input identity is the SHA256 of the existing builder output bytes. No receipts means missing; receipts without a matching input hash mean stale regardless of their verdict. Matching receipts use existential priority accepted, rejected, pending (reviewed), then incomplete (technical_failure). Older or lower-priority receipts never mask a current accepted disposition. Status preserves all receipts, evidence bytes and run provenance; it does not change lifecycle gates.

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

`--repair` acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`deskops inbox` is a deprecated alias for the same storage. Its flag grammar
(`--list`, `--show`, `--ack`) still works:

```bash runnable
deskops inbox --list --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity (`--sender` is the deprecated `inbox` spelling).
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. It refuses while other desk or docs files still reference the
document unless `--force` is passed. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`, or
`complete`, as pre-lifecycle tasks are. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites inbound `atom:<source>` references to the target and keeps the
source as a redirect stub. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-executor-task-fix-thing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task; `--mode coordinator` writes it for an agent that owns a desk (the
default follows the role name). With `--task` and `--agent` it also records a
RunDoc under `runs/subagents/`; `--task-root` names the repository whose desk
owns the task (default `--root`) and `--run-dir` reuses an existing evidence
directory instead of a new `runs/subagents/<ts>-<task>`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

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

- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
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
Cold-bundle de la tarea task-scion-autonomy-review-status: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- pytest tests/test_review_command.py
- actual isolated review status after accepted disposition
- pytest at integration

