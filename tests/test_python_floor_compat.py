"""deskops declares requires-python >=3.10.

Python 3.12 (PEP 701) lets an f-string reuse its own quote inside a
replacement field; 3.10 and 3.11 reject that file with a SyntaxError at import
time. The suite runs on newer interpreters, so the check reads the tokens.
"""

from __future__ import annotations

from pathlib import Path
import sys
import token
import tokenize

import pytest


PACKAGE = Path(__file__).resolve().parents[1] / "deskops"


def _fstrings_reusing_their_quote(path: Path) -> list[int]:
    lines: list[int] = []
    stack: list[str] = []
    with path.open("rb") as handle:
        for tok in tokenize.tokenize(handle.readline):
            if tok.type == token.FSTRING_START:
                quote = tok.string.lstrip("rRbBfFuU")
                if stack and stack[-1][0] in quote:
                    lines.append(tok.start[0])
                stack.append(quote)
            elif tok.type == token.FSTRING_END:
                stack.pop()
            elif tok.type == token.STRING and stack:
                if stack[-1][0] in tok.string.lstrip("rRbBfFuU")[:3]:
                    lines.append(tok.start[0])
    return lines


@pytest.mark.skipif(sys.version_info < (3, 12), reason="older interpreters fail at import instead")
def test_no_fstring_reuses_its_own_quote() -> None:
    offenders = {
        str(path.relative_to(PACKAGE.parent)): found
        for path in sorted(PACKAGE.rglob("*.py"))
        if (found := _fstrings_reusing_their_quote(path))
    }
    assert offenders == {}
