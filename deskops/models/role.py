from pydantic import Field
from sldb import StructuredNLDoc

class RoleDoc(StructuredNLDoc):
    model_config = {"extra": "forbid"}
    __semantics__ = {
        "type": ["workflow", "role"],
        "workspace": ["desk", "roles"],
    }

    __template__ = """---
id: ⸢rev•id⸥
name: ⸢rev•name⸥
description: ⸢rev•description⸥
kind: ⸢rev•kind⸥
model: ⸢rev•model⸥
fallback_models: ⸢rev•fallback_models⸥
tools: ⸢rev•tools⸥
system_prompt_mode: ⸢rev•system_prompt_mode⸥
inherit_project_context: ⸢rev•inherit_project_context⸥
inherit_skills: ⸢rev•inherit_skills⸥
default_context: ⸢rev•default_context⸥
---

⸢rev•body⸥
""".strip()

    id: str = Field(description="Stable role prompt identifier, conventionally 'role-<slug>'.")
    name: str = Field(description="Installed pi-agent role name, such as 'deskops-supervisor'.")
    description: str = Field(description="Short description of when to use this role prompt.")
    kind: str = Field(default="pi", description="Agent runtime kind (e.g. pi, claude, opencode).")
    model: str = Field(default="", description="Primary model ID.")
    fallback_models: list[str] = Field(default_factory=list, description="Fallback models.")
    tools: list[str] = Field(default_factory=list, description="Enabled tools.")
    system_prompt_mode: str = Field(default="replace", description="System prompt mode.")
    inherit_project_context: bool = Field(default=True, description="Inherit project context.")
    inherit_skills: bool = Field(default=True, description="Inherit project skills.")
    default_context: str = Field(default="fresh", description="Default context type (e.g. fork).")
    body: str = Field(description="Full role prompt markdown body after the YAML frontmatter.")
