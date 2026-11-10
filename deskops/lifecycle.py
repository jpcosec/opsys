"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

The activation gate of each factory task type is a ``RuleDoc`` (sldb GO06/GO08), also a
managed seed (``deskops/data/rules/``, written to ``desk/lifecycle/rule-activation-<type>.md``):
``on_transition`` over ``ritual-execution``, with subject ``model <= <TypeDoc>`` so a desk's
subtype inherits it without code, requiring the review receipts the type asks for
(``any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")``) and
the task's dependencies closed (``all(depends_on: status = "closed")``). sldb evaluates those
rules when ``edges_holding`` receives the task as ``document``; an ``error`` finding blocks
every edge and ``edges_blocked`` returns them with the findings ``deskops advance``, ``next``
and ``show`` print.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"
RULE_MODEL = "RuleDoc"
RULE_MODEL_REF = "sldb.models.rule_doc:RuleDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False
    #: The findings of the task's ``on_transition`` rules (sldb GO08), as ``finding_dict`` gives
    #: them: every finding on a blocked edge, only alerts on a holding one, none without a document.
    findings: tuple[dict[str, Any], ...] = ()

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it, ``transition_findings`` the store's rule graph (sldb loads the
    whole index for it, ~3 s on a small desk) and the closure service the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None
    rule_graph: Any = None
    has_rules: bool | None = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def finding_dict(finding: Any) -> dict[str, Any]:
    """An sldb ``Finding`` as the plain mapping ``show --format json`` prints."""
    return {"level": finding.level, "code": finding.code, "subject": finding.subject, "what": finding.what}


def finding_line(finding: dict[str, Any]) -> str:
    """One finding as sldb prints it: ``<level>: [<code>] <node>: <message> | <clause> (seen: ...)``."""
    return f"{finding['level']}: [{finding['code']}] {finding['subject']}: {finding['what']}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
        findings=tuple(finding_dict(f) for f in (getattr(edge, "findings", None) or ())),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any]) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them."""
    return [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any], document: str | None = None) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload. With ``document`` (the task's ``Model:name``
    in the store) the task's ``on_transition`` rules run too: an error finding holds every edge back."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transitions_blocked(root: Path, node: str, payload: dict[str, Any], document: str) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` but that an error
    finding of the task's ``on_transition`` rules blocks (``sldb.api.edges_blocked``), each
    carrying every finding."""
    from sldb.api import edges_blocked

    return _lifecycle_edges(node, edges_blocked(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transition_findings(root: Path, document: str, payload: dict[str, Any], *, snapshot: ReadSnapshot | None = None) -> list[dict[str, Any]]:
    """The findings of the task's ``on_transition`` rules read as ``payload`` (``sldb.api.transition_findings``).

    With a ``snapshot``, the store's rule graph is loaded once and shared by every task read of
    the pass (what ``sldb.api.transition_findings`` does on each call); a store without
    ``RuleDoc`` has no findings and loads nothing."""
    if snapshot is None:
        from sldb.api import transition_findings as sldb_transition_findings

        return [finding_dict(f) for f in sldb_transition_findings(_store(root), document, payload)]
    from sldb.api.rules.rule_graph import rule_graph
    from sldb.api.rules.rule_subjects import resolve_subject
    from sldb.api.rules.rules_on_transition import has_rules
    from sldb.api.rules.rules_on_transition import payload_findings

    if snapshot.has_rules is None:
        snapshot.has_rules = has_rules(_store(root))
    if not snapshot.has_rules:
        return []
    if snapshot.rule_graph is None:
        snapshot.rule_graph = rule_graph(_store(root))
    graph = snapshot.rule_graph
    return [finding_dict(f) for f in payload_findings(graph, "on_transition", resolve_subject(graph, document), payload)]


def task_document(root: Path, task_path: Path) -> str | None:
    """The ``Model:name`` the desk's store tracks ``task_path`` under (the subject of its rules);
    None for an untracked task or a desk without a store, where no rule runs."""
    from sldb.api.stores.doc_status import doc_status

    if not (_store(root) / "core").exists():
        return None
    try:
        status = doc_status(_store(root), task_path.resolve().relative_to(root.resolve()).as_posix())
    except Exception:
        return None
    if not status.model or not status.name:
        return None
    return f"{status.model}:{status.name}"


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None, document: str | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).

    With ``document`` (``task_document``) the task's ``on_transition`` rules run: when an error
    finding holds the edges back, the message lists each finding (rule, clause, node and value
    seen) instead of the edges' conditions.
    """
    from sldb.api import apply_effects

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
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload, document)
    if not holding:
        payload["current_node"] = node
        blocked = transitions_blocked(root, node, payload, document) if document else []
        findings = [f for t in blocked for f in t.findings if f["level"] == "error"]
        if findings:
            lines = "; ".join(finding_line(f) for f in findings)
            return TransitionResult(node, status, False, True, f"Gate {node} is blocked by its rules: {lines}")
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    target = COMPLETE if transition.terminal else transition.target
    # The model validates the whole new state (TaskDoc's lifecycle coherence): the edge's
    # ``sets``, the history it appends to and the node it leads to are applied together.
    history = [str(item) for item in payload.get("history") or []]
    sets = {**transition.sets, "history": [*history, transition.relation_type], "current_node": target}
    payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def ensure_rule_model(root: Path) -> bool:
    """Register sldb's ``RuleDoc`` in the desk's store when it lacks it (``sldb.api.add_model``);
    True when it was registered now. Tracking an activation rule needs the model, and each
    ``model <= <TypeDoc>`` of a rule's subject needs the type registered, which the deskops
    models always are."""
    from sldb.api import add_model
    from sldb.api import is_model_registered

    if is_model_registered(_store(root), RULE_MODEL):
        return False
    add_model(_store(root), RULE_MODEL_REF, pythonpath=package_pythonpath())
    return True


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds (the graph and the activation rules) and
    restores one the desk changed (``workspace.seed_desk``), registers sldb's relation models
    and ``RuleDoc`` when the store lacks them and tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import init_relations
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        init_relations(_store(root), pythonpath=package_pythonpath())
    ensure_rule_model(root)
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes


# Alias de compatibilidad hacia atrás
ensure_lifecycle_graph = write_lifecycle_graph

