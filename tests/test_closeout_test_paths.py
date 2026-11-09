"""Which references count as test evidence for the closeout gate.

A reference is test evidence when, after dropping ``::node`` and the ``pytest <path>``
form, it names an existing ``.py`` file inside the root that sits under a directory
named ``tests`` or is declared in the evaluated TaskDoc's ``files``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops.services.closeout_gates import CloseoutGatesService


def _touch(root: Path, relative: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    return path


def _tests_evidence(root: Path, references: list[str], files: list[str] | None = None) -> list[str]:
    payload: dict = {"references": references}
    if files is not None:
        payload["files"] = files
    evidence = CloseoutGatesService(root).closeout_reference_evidence(
        payload,
        points_to_atom=lambda ref: False,
        points_to_routed_follow_up=lambda ref: False,
    )
    return evidence["tests"]


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for relative in (
        "tests/x.py",
        "runtime/foo/tests/test_x.py",
        "ops/tests/sub/test_y.py",
        "tools/check_paths.py",
        "tests/notes.txt",
        "tests/upper.PY",
        ".venv/lib/python3.12/site-packages/pkg/tests/test_x.py",
        "vendor/site-packages/pkg/tests/test_x.py",
        "web/node_modules/pkg/tests/test_x.py",
    ):
        _touch(root, relative)
    (root / "empty" / "tests").mkdir(parents=True)
    return root


# Acceptance -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "reference",
    ["tests/x.py", "runtime/foo/tests/test_x.py", "ops/tests/sub/test_y.py", "./ops/tests/sub/test_y.py"],
)
def test_py_under_any_tests_directory_is_evidence(repo: Path, reference: str) -> None:
    assert CloseoutGatesService(repo).reference_points_to_test(reference)
    assert _tests_evidence(repo, [reference]) == [reference]


def test_py_declared_in_files_is_evidence_outside_tests(repo: Path) -> None:
    assert _tests_evidence(repo, ["tools/check_paths.py"], files=["tools/check_paths.py"]) == ["tools/check_paths.py"]
    assert _tests_evidence(repo, ["tools/check_paths.py"], files=["./tools/check_paths.py"]) == ["tools/check_paths.py"]


def test_py_outside_tests_and_not_declared_is_not_evidence(repo: Path) -> None:
    assert _tests_evidence(repo, ["tools/check_paths.py"]) == []
    assert _tests_evidence(repo, ["tools/check_paths.py"], files=["tools/other.py"]) == []


def test_files_alone_is_not_evidence(repo: Path) -> None:
    assert _tests_evidence(repo, [], files=["tools/check_paths.py", "tests/x.py"]) == []


@pytest.mark.parametrize(
    "reference",
    [
        "runtime/foo/tests/test_x.py::test_ok",
        "tests/x.py::TestThing::test_ok",
        "pytest runtime/foo/tests/test_x.py",
        "pytest -q ops/tests/sub/test_y.py::test_ok",
        "pytest 'tests/x.py'",
    ],
)
def test_node_and_pytest_forms_are_evidence(repo: Path, reference: str) -> None:
    assert _tests_evidence(repo, [reference]) == [reference]


def test_node_and_pytest_forms_count_for_declared_files(repo: Path) -> None:
    references = ["tools/check_paths.py::test_ok", "pytest -q tools/check_paths.py"]
    assert _tests_evidence(repo, references, files=["tools/check_paths.py"]) == references


# Rejection --------------------------------------------------------------------------


def test_absolute_path_is_not_evidence(repo: Path) -> None:
    absolute = str(repo / "tests" / "x.py")
    assert _tests_evidence(repo, [absolute], files=[absolute]) == []


def test_dotdot_escaping_the_root_is_not_evidence(repo: Path, tmp_path: Path) -> None:
    _touch(tmp_path, "outside/tests/test_out.py")
    reference = "../outside/tests/test_out.py"
    assert _tests_evidence(repo, [reference], files=[reference]) == []


def test_symlink_out_of_the_root_is_not_evidence(repo: Path, tmp_path: Path) -> None:
    _touch(tmp_path, "outside/test_out.py")
    (repo / "tests" / "linked").symlink_to(tmp_path / "outside", target_is_directory=True)
    reference = "tests/linked/test_out.py"
    assert (repo / reference).is_file()
    assert _tests_evidence(repo, [reference], files=[reference]) == []


@pytest.mark.parametrize("reference", ["tests/nope.py", "runtime/foo/tests/test_missing.py"])
def test_missing_file_is_not_evidence(repo: Path, reference: str) -> None:
    assert _tests_evidence(repo, [reference], files=[reference]) == []


@pytest.mark.parametrize("reference", ["tests/upper.PY", "tests/notes.txt"])
def test_suffix_other_than_py_is_not_evidence(repo: Path, reference: str) -> None:
    assert _tests_evidence(repo, [reference], files=[reference]) == []


@pytest.mark.parametrize(
    "reference",
    [
        ".venv/lib/python3.12/site-packages/pkg/tests/test_x.py",
        "vendor/site-packages/pkg/tests/test_x.py",
        "web/node_modules/pkg/tests/test_x.py",
    ],
)
def test_third_party_code_is_not_evidence(repo: Path, reference: str) -> None:
    assert _tests_evidence(repo, [reference], files=[reference]) == []


@pytest.mark.parametrize(
    "reference",
    ["tests pass", "see tests/", "tests/", "pytest", "tests/nope.py", "empty/tests", "empty/tests/", "pytest tests/"],
)
def test_strings_that_only_look_like_evidence_are_not_evidence(repo: Path, reference: str) -> None:
    assert _tests_evidence(repo, [reference], files=[reference]) == []
