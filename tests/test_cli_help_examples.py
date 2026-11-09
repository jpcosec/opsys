"""Run the command lines printed by ``deskops --help`` and ``deskops add --help``.

The help epilogs are part of the CLI contract, and an example that fails as
printed is worse than none. This test extracts the indented ``deskops ...``
lines from the root "Typical flow", from the ``add`` examples and from every
generated ``add <kind>`` example, then runs them in order with subprocess in a
sandbox repository: an isolated ``HOME`` (the conftest fixture), a git repo
with one seed commit, and this checkout on ``PYTHONPATH``.

Prose lines that mention a command in backticks are not examples and are not
extracted; only lines indented under the ``Typical flow:`` / ``Examples:`` /
``Example:`` headings count.
"""

from __future__ import annotations

import contextlib
import io
import os
from pathlib import Path
import shlex
import subprocess
import sys

import pytest

from tests.activation_receipts import accept_receipts

from deskops.cli.main import main
from deskops.operations import ARTIFACT_SUBJECTS


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
ADD_KINDS = sorted(
    str(meta["subject"]) for meta in ARTIFACT_SUBJECTS.values() if meta.get("create") is not False
)


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    return env


def _run(root: Path, argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*CLI, *argv], cwd=root, env=_env(), capture_output=True, text=True
    )


def _help(*prefix: str) -> str:
    """The ``--help`` text, rendered in-process; ``main`` turns argparse's exit into 0."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        assert main([*prefix, "--help"]) == 0
    text = buffer.getvalue()
    assert text.startswith("usage: deskops"), text
    return text


def _example_lines(help_text: str, heading: str) -> list[str]:
    """Indented ``deskops ...`` lines under ``heading`` up to the next blank line."""
    lines = help_text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        pytest.fail(f"heading {heading!r} not found in help:\n{help_text}")
    examples: list[str] = []
    for line in lines[start:]:
        if not line.strip():
            break
        if line.startswith("  ") and line.strip().startswith("deskops "):
            examples.append(line.strip())
    assert examples, f"no example lines under {heading!r}:\n{help_text}"
    return examples


def _argv(example: str) -> list[str]:
    tokens = shlex.split(example)
    assert tokens[0] == "deskops", example
    return tokens[1:]


def _run_examples(root: Path, examples: list[str]) -> None:
    for example in examples:
        argv = _argv(example)
        if argv[:2] == ["advance", "task"]:
            # The printed flow does not show the review step; the task type's activation rule
            # (CC32) needs the receipts accepted and intact before `advance`, so the test
            # writes them the way the flow would after `deskops review` + `review dispose`.
            accept_receipts(root, argv[2])
        result = _run(root, argv)
        assert result.returncode == 0, (
            f"help example failed: {example}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def _git(root: Path, *argv: str) -> None:
    subprocess.run(
        ["git", *argv], cwd=root, env=_env(), check=True, capture_output=True, text=True
    )


def _fresh_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    return root


def test_root_help_typical_flow_runs(tmp_path: Path) -> None:
    examples = _example_lines(_help(), "Typical flow:")
    assert examples[0] == "deskops bootstrap"
    assert examples[1] == "deskops init ."
    assert any(example.startswith("deskops add task ") for example in examples)
    _run_examples(_fresh_repo(tmp_path), examples)


def test_add_help_examples_run(lifecycle_desk: Path) -> None:
    examples = _example_lines(_help("add"), "Examples:")
    assert any(example.startswith("deskops add task ") for example in examples)
    assert any(example.startswith("deskops add pill ") for example in examples)
    _run_examples(lifecycle_desk, examples)


@pytest.mark.parametrize("kind", ADD_KINDS)
def test_add_kind_help_example_runs(lifecycle_desk: Path, kind: str) -> None:
    help_text = _help("add", kind)
    if "Example:" not in help_text.splitlines():
        pytest.skip(f"deskops add {kind} --help prints no example")
    examples = _example_lines(help_text, "Example:")
    assert all(example.startswith(f"deskops add {kind} ") for example in examples)
    _run_examples(lifecycle_desk, examples)
