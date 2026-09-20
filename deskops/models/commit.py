"""CommitDoc: derivado de git — qué cambió y cuándo, visible desde la task."""

from pydantic import Field

from sldb import StructuredNLDoc


class CommitDoc(StructuredNLDoc):
    __semantics__ = {"type": ["code", "commit"], "workspace": ["desk", "code"]}
    __containment__ = {}
    __template__ = """---
# commit-<sha>
id: ⸢rev•id⸥
sha: ⸢rev•sha⸥
author: ⸢rev•author⸥
committed_at: ⸢rev•committed_at⸥
trailers: ⸢rev,dict•trailers⸥
# e.g., type:commit
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Message

⸢rev•message⸥
""".strip()

    id: str = Field(description="Stable commit identifier, conventionally 'commit-<sha>'.")
    title: str = Field(description="Short commit title.")
    sha: str = Field(description="Full commit sha.")
    author: str = Field(description="Commit author.")
    committed_at: str = Field(description="Commit timestamp (ISO 8601).")
    message: str = Field(description="Commit message body.")
    trailers: dict = Field(
        default_factory=dict,
        description="Git trailers such as co-authored-by or signed-off-by.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )