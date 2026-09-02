from pydantic import Field, model_validator

from sldb import StructuredNLDoc


class RoleDoc(StructuredNLDoc):
    model_config = {"extra": "allow"}
    __semantics__ = {
        "type": ["workflow", "role"],
        "workspace": ["desk", "roles"],
    }

    frontmatter: dict | None = Field(
        default=None,
        description="YAML frontmatter containing role prompt metadata.",
        exclude=True,
    )

    @model_validator(mode="before")
    @classmethod
    def _merge_frontmatter(cls, data: dict) -> dict:
        if isinstance(data, dict) and "frontmatter" in data and isinstance(data["frontmatter"], dict):
            fm = data.pop("frontmatter")
            for key, value in fm.items():
                if key not in data or data[key] is None:
                    data[key] = value
        return data

    def render_payload(self) -> dict:
        data = super().model_dump(mode="json")
        body_fields = {"body"}
        data["frontmatter"] = {key: value for key, value in data.items() if key not in body_fields}
        return data

    __template__ = """---
⸢rev,dict•frontmatter⸥
---

⸢rev•body⸥
""".strip()

    id: str = Field(description="Stable role prompt identifier, conventionally 'role-<slug>'.")
    name: str = Field(description="Installed pi-agent role name, such as 'deskops-supervisor'.")
    description: str = Field(description="Short description of when to use this role prompt.")
    body: str = Field(description="Full role prompt markdown body after the YAML frontmatter.")
