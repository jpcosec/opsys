"""PlanTargetDoc: una cosa que hay que tocar; el puente con el AST vía `symbol`."""

from pydantic import Field

from sldb import StructuredNLDoc


class PlanTargetDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "plan_target"], "workspace": ["desk", "planning"]}
    __containment__ = {"contract": ["SymbolContractDoc"]}
    __references__ = ["symbol"]
    __template__ = """---
# plan-target-xxx
id: ⸢rev•id⸥
# Archivo o superficie a tocar
surface: ⸢rev•surface⸥
# Ref a PythonSymbolDoc — enganche con el AST
symbol: ⸢rev•symbol⸥
# add | modify | delete | verify
change_kind: ⸢rev•change_kind⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Rationale

_Explain why this target must be touched._

⸢rev•rationale⸥

## Acceptance

_Describe what proves this target is done._

⸢rev•acceptance⸥
""".strip()

    id: str = Field(description="Stable plan target identifier.")
    title: str = Field(description="Short plan target title.")
    surface: str = Field(description="File or surface this target touches.")
    symbol: str = Field(description="Ref to a PythonSymbolDoc — the hook into the AST.")
    change_kind: str = Field(
        description="Kind of change: add, modify, delete, or verify."
    )
    rationale: str = Field(description="Why this target must be touched.")
    acceptance: str = Field(description="What proves this target is done.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )