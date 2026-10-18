"""One renderer for text, json and yaml command output.

Handlers return their data; for text mode they also pass a formatter that
produces exactly the human-readable stdout the command printed before the
renderer existed. JSON and YAML are produced here so every command shares the
same serialization rules.

Error envelopes are the machine-readable counterpart of a failed command. An
``--format json`` failure prints ``{"ok": false, "error": {...}}`` to stdout and
exits with the code the error carries.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any
from typing import Callable
from typing import TextIO

import yaml


TextFormatter = Callable[[Any], str]


def normalize(payload: Any) -> Any:
    """Convert dataclasses, paths, mappings, and sequences to JSON-safe data."""

    if hasattr(payload, "__dataclass_fields__"):
        return normalize(asdict(payload))
    if isinstance(payload, Path):
        return str(payload)
    if isinstance(payload, dict):
        return {str(key): normalize(value) for key, value in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [normalize(value) for value in payload]
    return payload


def serialize(data: Any, fmt: str) -> str | None:
    """Return the machine-readable text for ``fmt`` (None for text mode)."""

    if fmt == "json":
        return json.dumps(normalize(data), indent=2, default=str)
    if fmt == "yaml":
        # ``print`` adds a newline; safe_dump already ends with one, exactly as
        # the per-command yaml printers did before the renderer.
        return yaml.safe_dump(normalize(data), sort_keys=False, allow_unicode=True)
    return None


def render(
    data: Any,
    fmt: str = "text",
    text: TextFormatter | None = None,
    *,
    stream: TextIO | None = None,
) -> int:
    """Print ``data`` in ``fmt`` and return success."""

    target = stream if stream is not None else sys.stdout
    serialized = serialize(data, fmt)
    if serialized is not None:
        print(serialized, file=target)
        return 0
    if text is None:
        raise ValueError(f"No text formatter supplied for {type(data).__name__}")
    output = text(data)
    if output:
        print(output, file=target)
    return 0


def error_envelope(code: int, type_name: str, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "code": code,
            "type": type_name,
            "message": message,
        },
    }


def render_error(
    message: str,
    fmt: str = "text",
    *,
    code: int = 1,
    type_name: str = "DomainError",
    text: str | None = None,
    stream: TextIO | None = None,
) -> int:
    """Print a failure in the requested format and return its exit code."""

    target = stream if stream is not None else sys.stdout
    if fmt == "json":
        print(json.dumps(error_envelope(code, type_name, message), indent=2), file=target)
    else:
        print(text if text is not None else message, file=target)
    return code


def render_deprecation(replacement: tuple[str, ...]) -> None:
    """Announce a deprecated alias on stderr without touching stdout."""

    print(f"Deprecated: use `deskops {' '.join(replacement)}`", file=sys.stderr)


def requested_format(argv: list[str]) -> str:
    """Return the last ``--format`` value in argv, or ``text``.

    The dispatcher needs this before parsing so failures raised after argparse
    (domain errors, validation errors) can still use the error envelope.
    """

    fmt = "text"
    for index, token in enumerate(argv):
        if token == "--format" and index + 1 < len(argv):
            fmt = argv[index + 1]
        elif token.startswith("--format="):
            fmt = token.split("=", 1)[1]
    return fmt
