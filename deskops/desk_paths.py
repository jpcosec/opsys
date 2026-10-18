"""One selector resolution rule for every desk artifact lookup.

Exact name or stem first, then a unique prefix; anything else is an error.
Callers provide the file pattern and whether the search recurses, so the rule
itself never depends on artifact-specific layout.
"""

from __future__ import annotations

from pathlib import Path


def _relative_candidates(desk_root: Path, paths: list[Path]) -> str:
    relative = []
    for path in paths:
        try:
            relative.append(str(path.relative_to(desk_root)))
        except ValueError:
            relative.append(str(path))
    return ", ".join(sorted(relative))


def resolve_selector(
    desk_root: Path,
    directories: list[Path],
    selector: str,
    pattern: str,
    what: str,
    recursive: bool,
) -> Path:
    """Resolve `selector` against `pattern` inside `directories`.

    Tier 1 accepts a file whose name or stem equals the selector. Tier 2
    accepts a unique file whose name or stem starts with it. Zero matches raise
    FileNotFoundError; more than one raise ValueError.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")

    candidates: list[Path] = []
    for directory in directories:
        if not directory.exists():
            continue
        matches = directory.rglob(pattern) if recursive else directory.glob(pattern)
        candidates.extend(sorted(matches))
    candidates = sorted(dict.fromkeys(candidates))

    exact = [path for path in candidates if selector in {path.name, path.stem}]
    if len(exact) == 1:
        return exact[0]
    if exact:
        raise ValueError(f"Ambiguous {what} selector '{selector}': {_relative_candidates(desk_root, exact)}")

    prefix = [path for path in candidates if path.name.startswith(selector) or path.stem.startswith(selector)]
    if not prefix:
        raise FileNotFoundError(f"No {what} file found for selector '{selector}'")
    if len(prefix) > 1:
        raise ValueError(f"Ambiguous {what} selector '{selector}': {_relative_candidates(desk_root, prefix)}")
    return prefix[0]
