from __future__ import annotations

from pathlib import Path

from sldb.runtime.validation import extract_model_data

from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations


REPO_ROOT = Path(__file__).resolve().parents[1]


def _taskdoc_paths() -> list[Path]:
    """Every TaskDoc under the live desk and the fixture desks, minus boards."""
    paths: set[Path] = set()
    for directory in (
        REPO_ROOT / "desk" / "tasks",
        REPO_ROOT / "desk" / "drawer" / "tasks",
        REPO_ROOT / "tests" / "fixtures",
    ):
        paths.update(directory.rglob("task-*.md"))
    return sorted(path for path in paths if path.is_file())


def test_read_doc_taskdoc_equals_extract_model_data() -> None:
    """TaskDoc reads go only through sldb's extractor.

    The regex overlay that used to win over `extract_model_data` is gone, so
    for every TaskDoc in the repository both reads must produce the same
    payload. A document sldb cannot parse is a failure here, never a skip.
    """
    operations = DeskopsOperations(REPO_ROOT)
    paths = _taskdoc_paths()
    assert paths, "no TaskDoc fixtures found"

    divergences: dict[str, str] = {}
    for path in paths:
        raw_text = path.read_text(encoding="utf-8")
        extracted = extract_model_data(TaskDoc, raw_text)
        read = operations._read_doc(path, TaskDoc)
        if read != extracted:
            fields = sorted(
                key for key in set(read) | set(extracted)
                if read.get(key) != extracted.get(key)
            )
            divergences[str(path.relative_to(REPO_ROOT))] = ", ".join(fields)

    assert not divergences, f"_read_doc no longer matches sldb extraction: {divergences}"
