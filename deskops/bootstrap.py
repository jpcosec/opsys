"""Bootstrap the deskops world in process through pron.

Replaces the old subprocess flow (`python -m sldb`, `pip install -e`). The
`deskops init` / `deskops bootstrap` entrypoints now build the world directly
through the pron seam (deskops/world.py):

1. `deskops.world.ensure_store_root(root)` creates the `.sldb` store when it
   does not exist yet, then `deskops.world.get_world(root)` opens it as a
   pron World.
2. `World.ensure_ready()` initialises pron's relations and models (idempotent).
3. Every model declared under `worlds[]` in spec/world/deskops-world.yaml is
   registered on the local store (`deskops.models:XxxDoc`, with
   `sldb.models:PythonSymbolDoc` for the symbol model); registering one that
   is already there is a no-op.
4. The 23 relation types are declared as RelationTypeDoc documents
   (deskops.relations.register_relation_types).
5. The store is refreshed so the derived graph is current.

`derived_status` / `derived_conditions` stay spec-only declarations: the spec
declares no document model for them, so bootstrap reads them from the YAML and
reports them but writes nothing. Computing the predicates is F3 T3.3 + F4
(docs/implementation-plan.md).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from deskops.relations import register_relation_types
from deskops.world import ensure_store_root
from deskops.world import get_world

# The world declaration this bootstrap materialises.
WORLD_SPEC = Path(__file__).resolve().parents[1] / "spec" / "world" / "deskops-world.yaml"

# Models the spec delegates to another package instead of deskops.models.
# PythonSymbolDoc is shipped by sldb under its re-export module (the same ref the
# repo store already tracks, F1 T1.3); `sldb.models:PythonSymbolDoc` does not
# resolve, and pron's register_model hides the ImportError as a False (gap-log).
EXTERNAL_MODEL_REFS = {
    "PythonSymbolDoc": "sldb.models.knowledge_surface:PythonSymbolDoc",
}

# Models the spec no longer declares (F2 T2.6: absorbed into pron/RitualDoc) but
# `deskops.models` still ships and the pre-F4 operations layer still creates
# documents of. Registered for compatibility until F4 retires that layer;
# keeping them out would break baseline-green promote/doctor flows.
LEGACY_MODEL_REFS = [
    "deskops.models:ChecklistDoc",
    "deskops.models:ConditionDoc",
    "deskops.models:EdgeDoc",
    "deskops.models:FAQDoc",
    "deskops.models:OperatorDoc",
    "deskops.models:RoutineDoc",
]


def world_model_refs(spec: dict[str, Any]) -> list[str]:
    """The registerable model refs declared under spec §worlds, deduplicated."""
    names: list[str] = []
    for world in spec.get("worlds", []):
        for name in world.get("models", []):
            if name not in names:
                names.append(name)
    return [EXTERNAL_MODEL_REFS.get(name, f"deskops.models:{name}") for name in names]


def read_world_spec() -> dict[str, Any]:
    return yaml.safe_load(WORLD_SPEC.read_text(encoding="utf-8")) or {}


def bootstrap_world(root: str | Path = ".") -> dict[str, Any]:
    """Build the deskops world at `root` in process. Idempotent: a second run
    registers nothing and leaves the already-current graph alone.

    Returns a report: what `ensure_ready` did, the models/relation types added,
    the refresh result, and the spec's derived_status/derived_conditions
    declarations (spec-only; not computed or written yet).
    """
    world = get_world(ensure_store_root(root))
    ensured = world.ensure_ready()
    spec = read_world_spec()

    refs = world_model_refs(spec) + LEGACY_MODEL_REFS
    models_added = [ref for ref in refs if world.store.register_model(ref)]

    relations_added = register_relation_types(world)

    # The graph must be current after any addition. When nothing was added the
    # world is still fresh: sldb keeps the edge index current on its own
    # writes, so refresh_if_stale() is a no-op there.
    changed = bool(ensured or models_added or relations_added)
    refresh = world.refresh() if changed else world.refresh_if_stale()

    return {
        "root": str(Path(root).resolve()),
        "ensure_ready": ensured,
        "models_registered": len(refs),
        "models_added": models_added,
        "legacy_models": len(LEGACY_MODEL_REFS),
        "relation_types_added": relations_added,
        "refresh": refresh,
        # Spec-only declarations; computation is F3 T3.3 + F4.
        "derived_status": spec.get("derived_status"),
        "derived_conditions": spec.get("derived_conditions"),
    }


class SLDBBootstrap:
    """CLI-facing wrapper kept for deskops/cli/main.py around the in-process
    bootstrap. `ensure_machine_ready` / `init_local_store` both build the world
    through pron now; no subprocess is spawned."""

    def ensure_sldb_available(self) -> int:
        try:
            import pron  # noqa: F401
        except ImportError:
            print(
                "Error: pron is not importable. Set PYTHONPATH to the deskops "
                "repo root (a stale deskops 0.1.0 in site-packages hijacks "
                "subprocess runs)."
            )
            return 1
        return 0

    def ensure_machine_ready(self, root: str | Path = ".") -> int:
        try:
            bootstrap_world(root)
        except Exception as exc:  # noqa: BLE001 - CLI boundary
            print(f"Error: world bootstrap failed: {exc}")
            return 1
        return 0

    def ensure_global_store_and_models(self) -> int:
        """Superseded: one .sldb per repo, models registered by reference on
        the local store. Kept as a no-op for interface compatibility."""
        return 0

    def init_local_store(self, target_path: Path) -> int:
        return self.ensure_machine_ready(target_path)

    def default_pythonpath(self) -> str:
        return str(self._package_root())

    def _package_root(self) -> Path:
        return Path(__file__).resolve().parents[1]