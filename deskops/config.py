from typing import Any
from pathlib import Path
import json
from pydantic import BaseModel, Field

class SandboxPolicy(BaseModel):
    enabled: bool = False
    sandbox_root: str | None = None

class VersionExpectations(BaseModel):
    desk_format: str = "1.0.0"
    model_version: str = "1.0.0"

class DeskConfig(BaseModel):
    project_identity: str = Field(default="unknown-project", description="Canonical project desk identity")
    versions: VersionExpectations = Field(default_factory=VersionExpectations)
    sandbox: SandboxPolicy = Field(default_factory=SandboxPolicy)

    @classmethod
    def load(cls, desk_root: Path) -> "DeskConfig":
        config_path = desk_root / "config.json"
        local_config_path = desk_root / "config.local.json"

        data: dict[str, Any] = {}
        if config_path.exists():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        if local_config_path.exists():
            try:
                local_data = json.loads(local_config_path.read_text(encoding="utf-8"))
                # basic merge
                if "project_identity" in local_data:
                    data["project_identity"] = local_data["project_identity"]
                if "versions" in local_data:
                    data.setdefault("versions", {}).update(local_data["versions"])
                if "sandbox" in local_data:
                    data.setdefault("sandbox", {}).update(local_data["sandbox"])
            except Exception:
                pass

        return cls(**data)
