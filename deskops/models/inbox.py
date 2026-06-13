from typing import Literal

from pydantic import Field

from sldb import StructuredNLDoc


class InboxNoteDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["desk", "inbox-note"],
        "workspace": ["desk", "inbox"],
    }
    __template__ = """---
kind: ⸢rev•kind⸥
author: ⸢rev•author⸥
created_at: ⸢rev•created_at⸥
status: ⸢rev•status⸥
---

# ⸢rev•title⸥

_Describe the unclear point or suggestion with enough evidence to triage._

⸢rev,markdown•body⸥
"""

    kind: Literal["unclear", "suggestion"] = Field(
        description="Inbox note type indicating unresolved confusion or an improvement proposal."
    )
    author: str = Field(description="Source label for who or what created the inbox note.")
    created_at: str = Field(description="Timestamp for when the inbox note was created.")
    status: Literal["open", "closed"] = Field(
        description="Whether the inbox note is still open or already handled."
    )
    title: str = Field(description="Inbox note title shown as the H1 heading.")
    body: str = Field(description="Markdown body describing the question or suggestion in detail.")
