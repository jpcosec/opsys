"""TestCoverageDoc: qué test ejercita qué símbolo — el set mínimo de tests a correr."""

from pydantic import Field

from sldb import StructuredNLDoc


class TestCoverageDoc(StructuredNLDoc):
    __semantics__ = {"type": ["code", "test_coverage"], "workspace": ["desk", "code"]}
    __containment__ = {}
    __references__ = ["covers_symbol"]
    __template__ = """---
# test-coverage-xxx
id: ⸢rev•id⸥
test_qualname: ⸢rev•test_qualname⸥
# Ref a PythonSymbolDoc cubierto por el test
covers_symbol: ⸢rev•covers_symbol⸥
# module | symbol
granularity: ⸢rev•granularity⸥
# import_decl | pytest_trace | manual
source: ⸢rev•source⸥
# e.g., type:test-coverage
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥
""".strip()

    id: str = Field(description="Stable test coverage identifier.")
    title: str = Field(description="Short test coverage title.")
    test_qualname: str = Field(description="Qualified name of the test.")
    covers_symbol: str = Field(description="Ref to the PythonSymbolDoc this test covers.")
    granularity: str = Field(description="Coverage granularity: module or symbol.")
    source: str = Field(description="How coverage was derived: import_decl, pytest_trace, or manual.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )