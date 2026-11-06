"""The text of a model's rejection, as the validators raised it.

A document invariant lives in its model as a pydantic validator; sldb applies it on every
write. A service that needs to report the rejection prints the validator's own line, not
pydantic's multi-line dump.
"""
from __future__ import annotations

from typing import Any

from pydantic import ValidationError
from sldb.runtime.validation import extract_payload


def validation_messages(error: ValidationError, *, invalid: str | None = None) -> list[str]:
    """One line per error. A validator's own text is kept as it was raised; a pydantic error
    (a missing field, a wrong type) names its field, prefixed with ``invalid`` when given."""
    lines: list[str] = []
    for item in error.errors():
        message = str(item.get("msg", ""))
        if item.get("type") == "value_error":
            lines.append(message.removeprefix("Value error, "))
            continue
        location = ".".join(str(part) for part in item.get("loc", ()))
        line = f"{location}: {message}" if location else message
        lines.append(f"{invalid}: {line}" if invalid else line)
    return lines


class InvalidDocument(ValueError):
    """A model rejected a payload. ``str()`` is the validators' text, one error per line."""

    def __init__(self, error: ValidationError) -> None:
        self.error = error
        super().__init__("\n".join(validation_messages(error)))


def validated(model: type[Any], payload: dict[str, Any]) -> Any:
    """``model(**payload)``, with the rejection reported as ``InvalidDocument``."""
    try:
        return model(**payload)
    except ValidationError as error:
        raise InvalidDocument(error) from error


def model_errors(model: type[Any], payload: dict[str, Any], *, invalid: str | None = None) -> list[str]:
    """The lines a model rejects ``payload`` with, or ``[]`` when it accepts it."""
    try:
        model(**payload)
    except ValidationError as error:
        return validation_messages(error, invalid=invalid)
    return []


def check_document(model: type[Any], text: str, *, invalid: str | None = None) -> tuple[dict[str, Any], list[str]]:
    """The payload the model's template extracts from ``text`` and the lines the model rejects
    it with (``[]`` when it accepts it). The payload is raw, so a checker can still report what
    else is wrong with a document its model refuses."""
    payload = extract_payload(model.__template__, text)
    return payload, model_errors(model, payload, invalid=invalid)
