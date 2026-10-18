"""Locations of the deskops package and its packaged runtime data.

``package_pythonpath()`` is the directory that contains the ``deskops`` package.
It is the value sldb needs for model resolution and is valid both from an
editable checkout and from a regular (non-editable) install. ``data_path``
resolves files shipped as package data, which live next to this module in both
layouts.
"""

from __future__ import annotations

from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent


def package_pythonpath() -> str:
    """The directory containing the ``deskops`` package."""
    return str(PACKAGE_DIR.parent)


def data_path(*parts: str) -> Path:
    """A path inside the installed package, used for packaged runtime data."""
    return PACKAGE_DIR.joinpath(*parts)
