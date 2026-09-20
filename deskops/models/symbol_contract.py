"""SymbolContractDoc: el contrato de un símbolo, escrito ANTES de implementarlo."""

from pydantic import Field

from sldb import StructuredNLDoc


class SymbolContractDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "symbol_contract"], "workspace": ["desk", "planning"]}
    __containment__ = {}
    __references__ = ["qualname"]
    __template__ = """---
# symbol-contract-xxx
id: ⸢rev•id⸥
# A qué símbolo le pone contrato (ref a PythonSymbolDoc)
qualname: ⸢rev•qualname⸥
# module | class | function | method
kind: ⸢rev•kind⸥
# Firma esperada, antes de existir
signature: ⸢rev•signature⸥
# Dónde va a vivir el test
test_qualname: ⸢rev•test_qualname⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Docstring

_Write what the symbol does and why it exists. Mandatory._

⸢rev•docstring⸥

## Purpose

_Describe the authored purpose this symbol serves._

⸢rev•purpose⸥

## Architecture

_Describe how this symbol fits the surrounding architecture._

⸢rev•architecture⸥

## Invariants

_List what must keep being true._

- ⸢rev,list•invariants⸥

## Lint Rules

_List the rules that apply (complexity, length)._

- ⸢rev,list•lint_rules⸥

## Test Plan

_List the cases the test proves, before writing them._

- ⸢rev,list•test_plan⸥
""".strip()

    id: str = Field(description="Stable symbol contract identifier.")
    title: str = Field(description="Short symbol contract title.")
    qualname: str = Field(description="Which symbol this contract governs, as a PythonSymbolDoc ref.")
    kind: str = Field(description="Symbol kind: module, class, function, or method.")
    signature: str = Field(description="Expected signature, before it exists.")
    docstring: str = Field(description="What the symbol does and why it exists. Mandatory.")
    purpose: str = Field(description="Authored purpose this symbol serves.")
    architecture: str = Field(description="How this symbol fits the surrounding architecture.")
    invariants: list[str] = Field(
        default_factory=list,
        description="Things that must keep being true.",
    )
    lint_rules: list[str] = Field(
        default_factory=list,
        description="Rules that apply, such as complexity or length.",
    )
    test_plan: list[str] = Field(
        default_factory=list,
        description="Cases the test proves, before they are written.",
    )
    test_qualname: str = Field(description="Where the test will live.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )