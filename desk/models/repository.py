from pydantic import Field

from sldb import StructuredNLDoc


class RepositoryDoc(StructuredNLDoc):
    """Model for registering a repository/tool within the opsys ecosystem."""

    __semantics__ = {
        "type": ["desk", "repository"],
        "workspace": ["desk", "registry"],
    }
    __template__ = """# Repository: ⸢rev•name⸥

ID: ⸢rev•id⸥
Path: ⸢rev•path⸥
Status: ⸢rev•status⸥

## Description

⸢rev,markdown•description⸥

## Tags

- ⸢rev,list•tags⸥
"""

    name: str = Field(description="Short human-readable name of the repository.")
    id: str = Field(description="Stable unique identifier for the repository.")
    path: str = Field(description="Relative path to the repository root from the ecosystem root.")
    status: str = Field(
        default="active",
        description="Current status of the repository (e.g., active, maintenance, archived).",
    )
    description: str = Field(description="Markdown description of the repository's purpose and scope.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags for categorization (e.g., type:tool, layer:infra).",
    )
