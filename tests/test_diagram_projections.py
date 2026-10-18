"""Guard rendered diagram projections against their Mermaid sources.

Only the SLDB components diagram is covered here. spec2viz migration is
deferred until a spec2viz source workflow exists in this repository; until
then the Markdown fenced block is the projection and the ``.mmd`` file is the
source.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = ROOT / "docs" / "diagrams" / "codebase"
COMPONENTS_MD = DIAGRAMS / "sldb-primitives-docs-cli-components.md"
COMPONENTS_MMD = DIAGRAMS / "sldb-primitives-docs-cli-components.mmd"

FENCED_MERMAID = re.compile(
    r"^```mermaid[ \t]*\n(.*?)^```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)


def _normalize(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def _first_fenced_mermaid_block(markdown: str) -> str:
    match = FENCED_MERMAID.search(markdown)
    assert match is not None, f"no fenced mermaid block in {COMPONENTS_MD}"
    return match.group(1)


def test_components_diagram_markdown_matches_mmd_source() -> None:
    source = _normalize(COMPONENTS_MMD.read_text(encoding="utf-8"))
    projection = _normalize(_first_fenced_mermaid_block(COMPONENTS_MD.read_text(encoding="utf-8")))
    assert projection == source, (
        f"{COMPONENTS_MD} fenced mermaid block drifted from {COMPONENTS_MMD}"
    )
