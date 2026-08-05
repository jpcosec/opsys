from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any


def _value_at_path(payload: dict[str, Any], path: str) -> Any:
    value: Any = payload
    for part in path.split("."):
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None
    return value


def _set_value_at_path(payload: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    target = payload
    for part in parts[:-1]:
        current = target.get(part)
        if not isinstance(current, dict):
            current = {}
            target[part] = current
        target = current
    target[parts[-1]] = value


@dataclass(slots=True)
class Primitive:
    id: str
    title: str
    status: str
    summary: str
    tags: list[str]


@dataclass(slots=True)
class Condition(Primitive):
    subject: str
    predicate: str
    expected: str

    def evaluate(self, payload: dict[str, Any]) -> bool:
        value = _value_at_path(payload, self.subject)
        if self.predicate == "equals":
            return value == self.expected
        if self.predicate == "not_equals":
            return value != self.expected
        if self.predicate == "truthy":
            return bool(value)
        if self.predicate == "falsy":
            return not bool(value)
        if self.predicate == "not_empty":
            return bool(value)
        if self.predicate == "contains":
            if isinstance(value, (list, tuple, set)):
                return self.expected in value
            if isinstance(value, str):
                return self.expected in value
            return False
        raise ValueError(f"Unsupported predicate: {self.predicate}")


@dataclass(slots=True)
class Operator(Primitive):
    action: str
    target: str
    value: str

    def apply(self, payload: dict[str, Any]) -> None:
        if self.action == "set_field":
            _set_value_at_path(payload, self.target, self.value)
            return
        if self.action == "append_list":
            current = _value_at_path(payload, self.target)
            if not isinstance(current, list):
                current = []
                _set_value_at_path(payload, self.target, current)
            try:
                parsed = json.loads(self.value)
            except json.JSONDecodeError:
                parsed = self.value
            current.append(parsed)
            return
        raise ValueError(f"Unsupported action: {self.action}")


@dataclass(slots=True)
class Checklist(Primitive):
    items: list[str]
    condition_refs: list[str]
    mode: str

    def is_complete(
        self,
        payload: dict[str, Any],
        conditions: dict[str, Condition],
    ) -> bool:
        if not self.condition_refs:
            return True
        results = [conditions[ref].evaluate(payload) for ref in self.condition_refs]
        if self.mode == "any":
            return any(results)
        return all(results)


@dataclass(slots=True)
class Edge(Primitive):
    source: str
    target: str
    condition_ref: str

    def is_available(self, payload: dict[str, Any], conditions: dict[str, Condition]) -> bool:
        if not self.condition_ref:
            return True
        return conditions[self.condition_ref].evaluate(payload)


@dataclass(slots=True)
class Hook(Primitive):
    event: str
    target: str
    condition_ref: str

    def matches(
        self,
        event: str,
        payload: dict[str, Any],
        conditions: dict[str, Condition],
    ) -> bool:
        if self.event != event:
            return False
        if not self.condition_ref:
            return True
        return conditions[self.condition_ref].evaluate(payload)


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


@dataclass(slots=True)
class Routine(Primitive):
    entrypoint: str
    decomposition: list[str]
    edges: list[Edge]
    terminal_nodes: list[str]

    def advance(
        self,
        payload: dict[str, Any],
        *,
        conditions: dict[str, Condition],
        operators: dict[str, Operator],
        checklists: dict[str, Checklist],
    ) -> TransitionResult:
        self.validate_integrity(
            payload,
            conditions=conditions,
            operators=operators,
            checklists=checklists,
        )
        start = payload.get("current_node") or self.entrypoint
        current = start

        while True:
            if current in self.terminal_nodes or current == "complete":
                payload["current_node"] = "complete"
                return TransitionResult("complete", str(payload.get("status", "")), False, False, "Task already complete.")

            if current in checklists:
                if current != start:
                    payload["current_node"] = current
                    return TransitionResult(current, str(payload.get("status", "")), True, False, f"Advanced to checklist {current}.")
                checklist = checklists[current]
                if not checklist.is_complete(payload, conditions):
                    payload["current_node"] = current
                    return TransitionResult(current, str(payload.get("status", "")), False, True, f"Checklist {current} is not complete.")

            if current in operators:
                operators[current].apply(payload)
                history = payload.setdefault("history", [])
                if isinstance(history, list):
                    history.append(current)

            edge = self._next_edge(current, payload, conditions)
            if edge is None:
                if current in operators:
                    payload["current_node"] = "complete"
                    return TransitionResult(
                        "complete",
                        str(payload.get("status", "")),
                        True,
                        False,
                        f"Completed after operator {current}.",
                    )
                payload["current_node"] = current
                return TransitionResult(current, str(payload.get("status", "")), current != start, False, f"No further transition from {current}.")

            current = edge.target
            if current in self.terminal_nodes:
                payload["current_node"] = current
                return TransitionResult(current, str(payload.get("status", "")), True, False, f"Reached terminal node {current}.")

    def _next_edge(
        self,
        source: str,
        payload: dict[str, Any],
        conditions: dict[str, Condition],
    ) -> Edge | None:
        for edge in self.edges:
            if edge.source != source:
                continue
            if edge.is_available(payload, conditions):
                return edge
        return None

    def validate_integrity(
        self,
        payload: dict[str, Any],
        *,
        conditions: dict[str, Condition],
        operators: dict[str, Operator],
        checklists: dict[str, Checklist],
    ) -> None:
        known_nodes = set(checklists) | set(operators) | set(self.terminal_nodes) | {
            "complete"
        }
        if self.entrypoint not in known_nodes:
            raise ValueError(
                f"routine {self.id} entrypoint references unknown node {self.entrypoint}"
            )

        current_node = payload.get("current_node")
        if current_node and current_node not in known_nodes:
            raise ValueError(
                f"routine {self.id} current_node references unknown node {current_node}"
            )

        for node_id in self.decomposition:
            if node_id not in known_nodes:
                raise ValueError(
                    f"routine {self.id} decomposition references unknown node {node_id}"
                )

        for checklist in checklists.values():
            for condition_ref in checklist.condition_refs:
                if condition_ref not in conditions:
                    raise ValueError(
                        f"checklist {checklist.id} references unknown condition {condition_ref}"
                    )

        for edge in self.edges:
            if edge.source not in known_nodes:
                raise ValueError(f"edge {edge.id} starts from unknown node {edge.source}")
            if edge.target not in known_nodes:
                raise ValueError(f"edge {edge.id} targets unknown node {edge.target}")
            if edge.condition_ref and edge.condition_ref not in conditions:
                raise ValueError(
                    f"edge {edge.id} references unknown condition {edge.condition_ref}"
                )


@dataclass(slots=True)
class OperationalArtifact(Primitive):
    routine: str
    current_node: str
    history: list[str]


@dataclass(slots=True)
class Task(OperationalArtifact):
    goal: str
    scope: str
    references: list[str]
    depends_on: list[str]
    pills: list[str]
    files: list[str]
    checklists: list[str]
    implementation_path: str
    validation: list[str]
    done_when: str
    task_type: str = ""
    inherits_from: list[str] = field(default_factory=list)
    inherit_acceptance_context: bool = False
    atoms: list[str] = field(default_factory=list)
    effective_references: list[str] = field(default_factory=list)
    effective_pills: list[str] = field(default_factory=list)
    effective_tags: list[str] = field(default_factory=list)
    effective_atoms: list[str] = field(default_factory=list)
    effective_validation: list[str] = field(default_factory=list)
    effective_done_when: str = ""
