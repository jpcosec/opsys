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


def transitions_from(root: Path, node: str, spec: LifecycleSpec | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology and conditions come from the graph; the effect of each transition comes from
    the spec. A relation type the spec does not know is not a lifecycle transition.
    """
    from sldb.api import edges_from

    spec = spec or load_lifecycle_spec()
    known = {t.relation_type for t in spec.transitions}
    found: list[Transition] = []
    for edge in edges_from(_store(root), ritual_export_id(node)):
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
        if _ensure_ritual_readable(path, ritual_id, relative):
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
