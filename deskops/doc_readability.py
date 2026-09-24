"""Detect documents a model cannot read back from its own text.

A rendered document carries the model template's fixed text, and the extractor
locates each field's value relative to it. A document that was authored by hand,
or produced by an older template, has the sections but not the fixed text, so
every body field extracts as empty. Reading such a document looks fine, but any
write renders the empty payload back and erases the content.

These helpers make that condition detectable before a write destroys anything.
"""

from __future__ import annotations

import re
from typing import Any

HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$", re.MULTILINE)
MIN_CONTENT_CHARS = 20


def section_bodies(text: str) -> dict[str, str]:
    """Map each heading to the body between it and the next heading."""
    bodies: dict[str, str] = {}
    matches = list(HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        bodies[match.group(2).strip().lower()] = text[match.end() : end]
    return bodies


def _content_only(body: str) -> str:
    """Drop the template's own instructional lines, which are styled `_like this_`."""
    lines = [line for line in body.splitlines() if not (line.strip().startswith("_") and line.strip().endswith("_"))]
    return "\n".join(lines).strip()


def unread_section_fields(model: type[Any], existing_text: str, rendered_text: str) -> list[str]:
    """Fields whose content exists in `existing_text` but not in `rendered_text`.

    An empty result means rewriting the document keeps everything the reader can see.
    """
    existing = section_bodies(existing_text)
    rendered = section_bodies(rendered_text)
    missing: list[str] = []
    for field in getattr(model, "model_fields", {}):
        before = _content_only(existing.get(field.replace("_", " "), ""))
        after = _content_only(rendered.get(field.replace("_", " "), ""))
        if len(before) < MIN_CONTENT_CHARS:
            continue
        if len(after) < MIN_CONTENT_CHARS:
            missing.append(field)
    return missing


def is_unreadable_by_model(model: type[Any], text: str) -> list[str]:
    """Fields the model extracts as empty although the document states them."""
    from sldb.runtime.validation import extract_model_data

    try:
        payload = extract_model_data(model, text)
    except Exception:
        return []
    bodies = section_bodies(text)
    unreadable: list[str] = []
    for field in getattr(model, "model_fields", {}):
        content = _content_only(bodies.get(field.replace("_", " "), ""))
        if len(content) >= MIN_CONTENT_CHARS and not str(payload.get(field) or "").strip():
            unreadable.append(field)
    return unreadable
