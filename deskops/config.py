from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from deskops.constants import CURRENT_DESK_FORMAT


class SandboxPolicy(BaseModel):
    enabled: bool = False
    sandbox_root: str | None = None


class VersionExpectations(BaseModel):
    desk_format: str = CURRENT_DESK_FORMAT
    model_version: str = "1.0.0"


class DeskConfig(BaseModel):
    project_identity: str = Field(default="unknown-project", description="Canonical project desk identity")
    versions: VersionExpectations = Field(default_factory=VersionExpectations)
    sandbox: SandboxPolicy = Field(default_factory=SandboxPolicy)
    load_warnings: list[str] = Field(default_factory=list, exclude=True)

    @property
    def has_load_warnings(self) -> bool:
        return bool(self.load_warnings)

    @classmethod
    def load(cls, desk_root: Path) -> "DeskConfig":
        merged_data: dict[str, Any] = {}
        load_warnings: list[str] = []

        for config_path in (desk_root / "config.json", desk_root / "config.local.json"):
            file_data = _load_json_object(config_path, load_warnings)
            if file_data is None:
                continue
            merged_data = _deep_merge_dicts(merged_data, file_data)

        return cls(**merged_data, load_warnings=load_warnings)


def _load_json_object(path: Path, load_warnings: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        message = f"Failed to parse desk config {path}: {exc.msg}"
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    if not isinstance(data, dict):
        message = f"Desk config {path} must contain a JSON object at the top level."
        load_warnings.append(message)
        warnings.warn(message, stacklevel=2)
        return None

    return data


def _deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = dict(base)
    for key, override_value in override.items():
        base_value = merged.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = _deep_merge_dicts(base_value, override_value)
        else:
            merged[key] = override_value
    return merged
