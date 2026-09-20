"""ChangeDoc: un hunk — la unión de git y AST; el rango de líneas se resuelve a símbolo."""

from pydantic import Field

from sldb import StructuredNLDoc


class ChangeDoc(StructuredNLDoc):
    __semantics__ = {"type": ["code", "change"], "workspace": ["desk", "code"]}
    __containment__ = {}
    __references__ = ["symbol"]
    __template__ = """---
# change-xxx
id: ⸢rev•id⸥
path: ⸢rev•path⸥
line_start: ⸢rev•line_start⸥
line_end: ⸢rev•line_end⸥
added: ⸢rev•added⸥
removed: ⸢rev•removed⸥
# Ref a PythonSymbolDoc, resuelto por source_span
symbol: ⸢rev•symbol⸥
# e.g., type:change
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥
""".strip()

    id: str = Field(description="Stable change identifier.")
    title: str = Field(description="Short change title.")
    path: str = Field(description="File path this change touches.")
    line_start: int = Field(description="First line of the hunk.")
    line_end: int = Field(description="Last line of the hunk.")
    added: int = Field(description="Number of lines added.")
    removed: int = Field(description="Number of lines removed.")
    symbol: str = Field(description="Ref to a PythonSymbolDoc, resolved by source_span.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )