from typing import Literal, Optional

from pydantic import Field

from sldb import StructuredNLDoc


class InboxNoteDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["desk", "inbox-note"],
        "workspace": ["desk", "inbox"],
    }
    __template__ = """---
# unclear | suggestion
kind: ⸢rev•kind⸥
# e.g., other_repo
sender_project: ⸢rev•sender_project⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# open | closed
status: ⸢rev•status⸥
---

# ⸢rev•title⸥

_Describe the incoming message with enough evidence to triage._

⸢rev,markdown•body⸥
"""

    kind: Literal["unclear", "suggestion"] = Field(
        description="Inbox note type indicating unresolved confusion or an improvement proposal."
    )
    sender_project: Optional[str] = Field(
        default=None,
        description="Project that sent the inbox message, resolved from the repo registry when possible."
    )
    created_at: str = Field(description="Timestamp for when the inbox note was created.")
    status: Literal["open", "closed"] = Field(
        description="Whether the inbox note is still open or already handled."
    )
    title: str = Field(description="Inbox note title shown as the H1 heading.")
    body: str = Field(description="Markdown body describing the question or suggestion in detail.")
