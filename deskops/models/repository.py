from typing import Optional

from pydantic import Field

from sldb import StructuredNLDoc


class RepositoryDoc(StructuredNLDoc):
    """Model for registering a repository/tool within the opsys ecosystem."""

    __semantics__ = {
        "type": ["desk", "repository"],
        "workspace": ["desk", "registry"],
    }
    __template__ = """---
# repo-xxx
id: ⸢rev•id⸥
# Relative path to repository
path: ⸢rev•path⸥
# active | maintenance | archived
status: ⸢rev•status⸥
# e.g., type:tool, layer:infra
tags: ⸢rev•tags⸥
---

# Repository: ⸢rev•name⸥

## Description

_Describe the repository purpose, scope, and role in the ecosystem._

⸢rev,markdown•description⸥
"""

    name: str = Field(description="Short human-readable name of the repository.")
    id: Optional[str] = Field(
        default=None,
        description="Stable unique identifier for the repository."
    )
    path: Optional[str] = Field(
        default=None,
        description="Relative path to the repository root from the ecosystem root."
    )
    status: str = Field(
        default="active",
        description="Current status of the repository (e.g., active, maintenance, archived).",
    )
    description: str = Field(description="Markdown description of the repository's purpose and scope.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags for categorization (e.g., type:tool, layer:infra).",
    )
