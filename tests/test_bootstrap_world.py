"""F3 T3.4: `deskops init` builds the whole world from the spec, in process."""

from __future__ import annotations

from pathlib import Path

from deskops import derived_conditions as dc
from deskops import derived_status as ds
from deskops.bootstrap import LEGACY_MODEL_REFS
from deskops.bootstrap import bootstrap_world
from deskops.bootstrap import read_world_spec
from deskops.bootstrap import world_model_refs
from deskops.relations import RELATION_TYPES
from deskops.world import DocId
from deskops.world import get_world


def test_world_model_refs_follow_the_spec_worlds_section() -> None:
    spec = read_world_spec()

    refs = world_model_refs(spec)

    assert "deskops.models:TaskDoc" in refs
    assert "deskops.models:PlanTargetDoc" in refs
    assert "sldb.models.knowledge_surface:PythonSymbolDoc" in refs
    assert len(refs) == len(set(refs))


def test_bootstrap_registers_the_world_models_and_relations(tmp_path: Path) -> None:
    report = bootstrap_world(tmp_path)

    world = get_world(tmp_path)
    names = set(world.store.model_names())

    assert "PythonSymbolDoc" in names
    assert {"TaskDoc", "PlanDoc", "PlanTargetDoc", "SymbolContractDoc"} <= names
    assert len(report["relation_types_added"]) == len(RELATION_TYPES)
    for spec in RELATION_TYPES:
        assert world.store.doc(DocId.of("RelationTypeDoc", f"reltype-{spec['name']}")) is not None


def test_bootstrap_is_idempotent_and_leaves_a_current_graph(tmp_path: Path) -> None:
    bootstrap_world(tmp_path)

    second = bootstrap_world(tmp_path)

    assert second["models_added"] == []
    assert second["relation_types_added"] == []
    assert second["refresh"] is False
    assert get_world(tmp_path).graph.stale == []


def test_bootstrap_reports_the_spec_derivations_without_writing_them(tmp_path: Path) -> None:
    report = bootstrap_world(tmp_path)

    assert tuple(report["derived_status"]["values"]) == ds.CODE_LADDER
    assert [entry["name"] for entry in report["derived_conditions"]] == list(dc.DERIVED_CONDITIONS)


def test_bootstrap_keeps_the_legacy_models_the_operations_layer_still_writes(tmp_path: Path) -> None:
    bootstrap_world(tmp_path)

    names = set(get_world(tmp_path).store.model_names())

    for ref in LEGACY_MODEL_REFS:
        assert ref.split(":", 1)[1] in names


def test_refresh_after_bootstrap_does_not_raise(tmp_path: Path) -> None:
    bootstrap_world(tmp_path)
    world = get_world(tmp_path)

    report = world.refresh()

    assert report is not None
