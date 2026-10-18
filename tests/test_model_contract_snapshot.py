from __future__ import annotations

import importlib
import json
from pathlib import Path

import yaml
from sldb.store.hashing import hash_model_contract

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).with_name("fixtures") / "model_contract_hashes.json"
FIXTURE_UPDATE = (
    "Update tests/fixtures/model_contract_hashes.json only as part of a deliberate "
    "contract change requiring a store migration (task-rw-f6-migrate-tracking-stores)."
)


def _model_refs() -> dict[str, str]:
    """MODEL_REFS united with the models registered in this repo's store index."""
    from deskops.bootstrap import MODEL_REFS

    refs = dict(MODEL_REFS)
    store_index = yaml.safe_load((ROOT / ".sldb" / "core" / "store_index.yaml").read_text())
    for entry in store_index.get("models") or []:
        refs.setdefault(entry["name"], entry["model_ref"])
    return refs


def _load_model(model_ref: str) -> type:
    module_name, class_name = model_ref.split(":", 1)
    return getattr(importlib.import_module(module_name), class_name)


def _contract_hashes() -> dict[str, str]:
    return {
        name: hash_model_contract(_load_model(model_ref))
        for name, model_ref in sorted(_model_refs().items())
    }


def _snapshot() -> dict[str, str]:
    return json.loads(FIXTURE.read_text())


def test_snapshot_covers_the_registered_model_set() -> None:
    snapshot = _snapshot()
    discovered = _contract_hashes()

    missing = sorted(set(discovered) - set(snapshot))
    extra = sorted(set(snapshot) - set(discovered))
    assert not missing and not extra, (
        f"Model contract snapshot is out of date. "
        f"Missing from snapshot: {missing or 'none'}. "
        f"Extra in snapshot: {extra or 'none'}. {FIXTURE_UPDATE}"
    )


def test_model_contract_hashes_match_the_snapshot() -> None:
    snapshot = _snapshot()
    discovered = _contract_hashes()

    changed = sorted(name for name in snapshot if name in discovered and snapshot[name] != discovered[name])
    assert not changed, (
        f"Model contract changed for: {', '.join(changed)}. "
        f"This requires a store migration (task-rw-f6-migrate-tracking-stores). {FIXTURE_UPDATE}\n"
        f"New hashes:\n{json.dumps(discovered, indent=2, sort_keys=True)}\n"
    )
