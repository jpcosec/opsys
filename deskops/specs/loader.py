from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class SpecRegistry:
    root: Path
    fields: dict[str, dict[str, Any]]
    primitives: dict[str, dict[str, Any]]
    artifacts: dict[str, dict[str, Any]]

    @classmethod
    def load(cls, root: Path) -> "SpecRegistry":
        root = root.resolve()
        return cls(
            root=root,
            fields=_load_spec_dir(root / "fields"),
            primitives=_load_spec_dir(root / "primitives"),
            artifacts=_load_spec_dir(root / "artifacts"),
        )


def _load_spec_dir(directory: Path) -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for path in sorted(directory.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        specs[str(payload["id"])] = payload
    return specs
