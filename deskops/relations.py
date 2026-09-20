"""The deskops relation graph, declared as RelationTypeDoc payloads.

One entry per relation type in spec/world/deskops-world.yaml §relation_types.
The workflow is a graph: nodes are documents, these are the edge types.
`mode` (assert vs read) from the spec is not a RelationTypeDoc field, so it is
carried only in the description where it matters (see `blocks`).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.world import DocId

RELATION_TYPES: list[dict[str, Any]] = [
    # Workflow
    {"name": "has_step", "from": "RitualDoc", "to": "StepDoc",
     "description": "A ritual is made of ordered steps."},
    {"name": "next_step", "from": "StepDoc", "to": "StepDoc",
     "description": "The step that follows this one within a ritual."},
    {"name": "binds", "from": "TaskBindingDoc", "to": "PillDoc",
     "description": "The pills a task binding makes available for execution."},
    {"name": "depends_on", "from": "TaskDoc", "to": "TaskDoc",
     "description": "A task that must complete before this one can start."},
    {"name": "blocks", "from": "TaskDoc", "to": "TaskDoc",
     "description": "Derived (mode read): a task that cannot advance until this one does."},
    # Conocimiento (cruzan de world, mismo store)
    {"name": "domain_parent", "from": "AtomDoc", "to": "CrossroadDoc",
     "description": "The crossroad every atom of a domain path hangs under."},
    {"name": "typed_as", "from": "ProtoAtomDoc", "to": "AtomDoc",
     "description": "The atom type a proto-atom was captured to become."},
    {"name": "references", "from": "TaskBindingDoc", "to": "AtomDoc",
     "description": "The durable atoms a task binding leans on."},
    {"name": "graduates_to", "from": "PillDoc", "to": "AtomDoc",
     "description": "A pill that stabilized into durable knowledge."},
    # Planificación → código
    {"name": "plans_change", "from": "PlanTargetDoc", "to": "PythonSymbolDoc",
     "description": "The symbol a plan target says must change."},
    {"name": "iterates", "from": "PlanIterationDoc", "to": "PlanDoc",
     "description": "The plan an iteration records a pass over."},
    {"name": "contracts", "from": "SymbolContractDoc", "to": "PythonSymbolDoc",
     "description": "The contract declared before the symbol exists; after implementing, sldb selfdoc python-check compares."},
    {"name": "verifies", "from": "SymbolContractDoc", "to": "TestCoverageDoc",
     "description": "The test declared in a contract, once written."},
    # AST (sobre PythonSymbolDoc de sldb)
    {"name": "imports", "from": "PythonSymbolDoc", "to": "PythonSymbolDoc",
     "description": "A symbol imports another (declared module import)."},
    {"name": "defines", "from": "PythonSymbolDoc", "to": "PythonSymbolDoc",
     "description": "A symbol is defined within another symbol's scope."},
    {"name": "covers", "from": "TestCoverageDoc", "to": "PythonSymbolDoc",
     "description": "The symbol a test exercises."},
    {"name": "documents", "from": "AtomDoc", "to": "PythonSymbolDoc",
     "description": "An atom that explains a symbol, joining permanent knowledge with the code."},
    # git
    {"name": "touches", "from": "ChangeDoc", "to": "PythonSymbolDoc",
     "description": "The symbol a change's line range resolves to."},
    {"name": "contains_change", "from": "CommitDoc", "to": "ChangeDoc",
     "description": "A change a commit contains."},
    {"name": "produced_commit", "from": "RunDoc", "to": "CommitDoc",
     "description": "The commit a run produced."},
    {"name": "evidences", "from": "RunDoc", "to": "TaskDoc",
     "description": "The task a run produced evidence for."},
    {"name": "executed_by", "from": "RunDoc", "to": "RoleDoc",
     "description": "The role that executed a run."},
    {"name": "runs_on", "from": "RoleDoc", "to": "RuntimeProfileDoc",
     "description": "The runtime profile a role executes on."},
]


def relation_payload(spec: dict[str, Any]) -> dict[str, Any]:
    """A RelationTypeDoc payload for one relation spec entry."""
    return {
        "title": spec["name"],
        "name": spec["name"],
        "direction": "directed",
        "cardinality": "many_to_many",
        "axis": "",
        "condition": "",
        "source_types": [spec["from"]],
        "target_types": [spec["to"]],
        "description": spec["description"],
    }


def relation_doc_name(spec: dict[str, Any]) -> str:
    """The name a relation type is tracked under."""
    return f"reltype-{spec['name']}"


def register_relation_types(world) -> list[str]:
    """Write each declared relation type as a RelationTypeDoc, idempotent.

    Returns the names of the relation types newly registered.
    """
    source_dir = Path("desk") / "relation_types"
    added: list[str] = []
    for spec in RELATION_TYPES:
        name = relation_doc_name(spec)
        if world.store.doc(DocId.of("RelationTypeDoc", name)) is not None:
            continue
        world.store.create(
            DocId.of("RelationTypeDoc", name),
            relation_payload(spec),
            source_dir / f"{spec['name']}.md",
        )
        added.append(spec["name"])
    return added