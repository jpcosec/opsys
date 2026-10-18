"""Golden files pin the machine-readable outputs other tools depend on.

The fixture desk is copied into a throwaway git repository. The real CLI then
builds the graph snapshot, writes the self-reflection report, and makes one
closeout commit per route (run-linked and manual). Volatile values (root paths,
timestamps, commit hashes) are normalized before comparison.

Run ``pytest tests/test_output_goldens.py --update-golden`` to rewrite the
committed goldens after an intentional output change.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
FIXTURE_DESK = TESTS_DIR / "fixtures" / "golden_desk"
GOLDEN_DIR = TESTS_DIR / "fixtures" / "golden"

GRAPH_SNAPSHOT = Path(".sldb/runtime/graphs/deskops.kg.json")
GRAPH_NETWORKX = Path(".sldb/runtime/graphs/deskops.nx.json")
SELF_REFLECTION = Path(".sldb/runtime/self_reflection_findings.json")

RUN_DIR = "runs/subagents/golden-run"
RUN_ID = "run-golden-001"
SESSION_SHA256 = "1" * 64

POSITIONAL_ARGUMENT_RE = re.compile(r"^    (?P<name>\S+)(?:\s{2,}|$)")
ISO_TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b"
)
COMMIT_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TRAILER_RE = re.compile(r"^(?P<key>[A-Z][A-Za-z0-9-]+): (?P<value>.+)$")


def _env(home: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env["COLUMNS"] = "80"
    if home is not None:
        env["HOME"] = str(home)
        env["XDG_CACHE_HOME"] = str(home / ".cache")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) + (os.pathsep + existing if existing else "")
    return env


def _cli(
    cwd: Path, *argv: str, home: Path | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=cwd,
        env=_env(home),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def _git(cwd: Path, *argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _normalize_text(text: str, root: Path) -> str:
    text = text.replace(str(root), "<root>")
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return text


def _normalize_json(value: Any, root: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: "<sha>" if key == "commit" else _normalize_json(item, root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_normalize_json(item, root) for item in value]
    if isinstance(value, str):
        return _normalize_text(value, root)
    return value


def _json_document(value: Any, root: Path) -> str:
    return json.dumps(_normalize_json(value, root), indent=2, sort_keys=True) + "\n"


def _check_golden(relative_path: str, actual: str, request: pytest.FixtureRequest) -> None:
    path = GOLDEN_DIR / relative_path
    update = request.config.getoption("--update-golden")
    if not actual.endswith("\n"):
        actual += "\n"
    if update:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    assert path.exists(), f"missing golden {path}; run pytest --update-golden"
    expected = path.read_text(encoding="utf-8")
    if relative_path.startswith("help/"):
        # argparse wraps the usage block differently across Python versions
        # (3.12 vs 3.13); its words, not its line breaks, are the contract.
        actual, expected = _unwrap_usage(actual), _unwrap_usage(expected)
    assert actual == expected, f"golden mismatch: {relative_path}"


_SHORT_OPTION_METAVAR_RE = re.compile(r"(?m)^(\s+-\w) (\S+), (--[\w-]+) \2$")


def _unwrap_usage(text: str) -> str:
    """Collapse the leading `usage:` block into one line and use 3.13 option spelling.

    3.12 lists a short option with its metavar (`-m MESSAGE, --message MESSAGE`);
    3.13 lists it once (`-m, --message MESSAGE`).
    """
    text = _SHORT_OPTION_METAVAR_RE.sub(r"\1, \3 \2", text)
    if not text.startswith("usage:"):
        return text
    usage, sep, rest = text.partition("\n\n")
    return " ".join(usage.split()) + sep + rest


def _make_fixture_repo(destination: Path) -> Path:
    root = destination / "repo"
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    return root


def _write_run_evidence(root: Path) -> Path:
    run_dir = root / RUN_DIR
    run_dir.mkdir(parents=True)
    for name in ("board.txt", "task.txt", "git-status.txt", "result-summary.md"):
        (run_dir / name).write_text(f"{name} evidence\n", encoding="utf-8")
    (run_dir / "run.yaml").write_text(
        "\n".join(
            [
                f"run_id: {RUN_ID}",
                f"session_sha256: {SESSION_SHA256}",
                "touched:",
                f"- {RUN_DIR}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return run_dir


def _trailers(root: Path) -> dict[str, str]:
    message = _git(root, "log", "-1", "--format=%B")
    trailers: dict[str, str] = {}
    for line in message.splitlines():
        match = TRAILER_RE.match(line)
        if match:
            trailers[match.group("key")] = match.group("value")
    return trailers


@pytest.fixture(scope="module")
def golden_outputs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = _make_fixture_repo(tmp_path_factory.mktemp("golden-output"))

    _cli(root, "graph", "build", "--root", str(root))
    _cli(root, "graph", "reflect", "--root", str(root))

    snapshot = json.loads((root / GRAPH_SNAPSHOT).read_text(encoding="utf-8"))
    networkx = json.loads((root / GRAPH_NETWORKX).read_text(encoding="utf-8"))
    self_reflection = json.loads((root / SELF_REFLECTION).read_text(encoding="utf-8"))

    _write_run_evidence(root)
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-alpha",
        "--run-dir",
        RUN_DIR,
    )
    run_trailers = _trailers(root)

    note = root / "notes" / "golden-note.txt"
    note.parent.mkdir(parents=True)
    note.write_text("manual closeout note\n", encoding="utf-8")
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-beta",
        "--no-run",
        "--reason",
        "golden manual closeout",
        "--paths",
        "notes/golden-note.txt",
    )
    no_run_trailers = _trailers(root)

    return {
        "root": root,
        "graph_snapshot": snapshot,
        "graph_networkx": networkx,
        "self_reflection": self_reflection,
        "closeout_trailers": [
            {"route": "run-dir", "trailers": run_trailers},
            {"route": "no-run", "trailers": no_run_trailers},
        ],
    }


def test_graph_snapshot_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_snapshot"], golden_outputs["root"])
    _check_golden("graph_snapshot.kg.json", actual, request)


def test_graph_networkx_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_networkx"], golden_outputs["root"])
    _check_golden("graph_snapshot.nx.json", actual, request)


def test_self_reflection_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["self_reflection"], golden_outputs["root"])
    _check_golden("self_reflection_findings.json", actual, request)


def test_run_index_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    root = golden_outputs["root"]
    index_path = root / "runs" / "subagents" / "index.jsonl"
    entries = [
        _normalize_json(json.loads(line), root)
        for line in index_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    actual = "".join(json.dumps(entry, sort_keys=True) + "\n" for entry in entries)
    _check_golden("run_index.jsonl", actual, request)


def test_closeout_trailers_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["closeout_trailers"], golden_outputs["root"])
    _check_golden("closeout_trailers.json", actual, request)


def _positional_names(help_text: str) -> list[str]:
    names: list[str] = []
    in_positionals = False
    for line in help_text.splitlines():
        if line.strip() == "positional arguments:":
            in_positionals = True
            continue
        if not in_positionals:
            continue
        if line and not line.startswith(" "):
            break
        match = POSITIONAL_ARGUMENT_RE.match(line)
        if match:
            names.append(match.group("name"))
    return names


def _help(prefix: list[str]) -> str:
    result = _cli(REPO_ROOT, *prefix, "--help")
    assert result.stdout.startswith("usage: deskops"), result.stdout
    return result.stdout


def _collect_help() -> dict[str, str]:
    outputs: dict[str, str] = {}
    pending: list[list[str]] = [[]]
    while pending:
        prefix = pending.pop(0)
        name = "_".join(["deskops", *prefix])
        text = _help(prefix)
        outputs[f"help/{name}.txt"] = text
        for candidate in _positional_names(text):
            if candidate in {"-h", "--help"}:
                continue
            child = [*prefix, candidate]
            result = _cli(REPO_ROOT, *child, "--help")
            if result.stdout.startswith("usage: deskops"):
                pending.append(child)
    return outputs


def test_help_goldens(request: pytest.FixtureRequest) -> None:
    outputs = _collect_help()
    update = request.config.getoption("--update-golden")
    if update:
        help_dir = GOLDEN_DIR / "help"
        for stale in help_dir.glob("*.txt"):
            if f"help/{stale.name}" not in outputs:
                stale.unlink()
    for relative_path, actual in sorted(outputs.items()):
        _check_golden(relative_path, actual, request)


# --- command output goldens -------------------------------------------------

STAMP_RE = re.compile(r"\b\d{8}-\d{6}\b")
FORMATS_TEXT_JSON = ("text", "json")
FORMATS_TEXT_JSON_YAML = ("text", "json", "yaml")

OUTPUT_FIXTURE_DOCS = (
    (
        "ritual",
        (
            ["--title", "Golden ritual"],
            ["--purpose", "Golden purpose"],
            ["--trigger", "Golden trigger"],
            ["--completion", "Golden completion"],
        ),
    ),
    (
        "board",
        (
            ["--title", "Golden board"],
            ["--scope", "golden scope"],
            ["--purpose", "Golden purpose"],
        ),
    ),
    (
        "materialization",
        (
            ["--title", "Golden materialization"],
            ["--target-kind", "document"],
            ["--target-identity", "atom-golden-one"],
            ["--intent", "Golden intent"],
        ),
    ),
    (
        "repository",
        (
            ["--name", "Golden repository"],
            ["--description", "Golden description"],
        ),
    ),
    (
        "inbox-note",
        (
            ["--kind", "unclear"],
            ["--created-at", "2026-01-01T00:00:00"],
            ["--status", "open"],
            ["--title", "Golden inbox note"],
            ["--body", "Golden body"],
        ),
    ),
    (
        "faq-doc",
        (
            ["--title", "Golden FAQ"],
            ["--body", "What is golden?\n\nGolden output."],
        ),
    ),
    (
        "step",
        (
            ["--title", "Golden step"],
            ["--action", "Golden action"],
            ["--outcome", "Golden outcome"],
        ),
    ),
)

SHOW_SUBJECTS = (
    ("task", "task-golden-alpha"),
    ("pill", "pill-golden-rule"),
    ("ritual", "ritual-golden-ritual"),
    ("board", "board-golden-board"),
    ("atom", "atom-golden-one"),
    ("materialization", "materialization-golden-materialization"),
    ("repository", "repo-golden-repository"),
    ("inbox-note", "inbox-note-golden-inbox-note"),
    ("faq-doc", "faq-golden-faq"),
    ("step", "step-golden-step"),
)

LIST_SUBJECTS = (
    "tasks",
    "pills",
    "rituals",
    "boards",
    "atoms",
    "materializations",
    "repositories",
    "inbox-notes",
    "faq-docs",
    "steps",
)

FAKE_HERDR = """#!/usr/bin/env python3
import json
import sys

if sys.argv[1:3] == ["workspace", "list"]:
    payload = {
        "result": {
            "workspaces": [
                {
                    "workspace_id": "w-1",
                    "label": "golden",
                    "number": 1,
                    "agent_status": "active",
                    "pane_count": 1,
                    "focused": True,
                }
            ]
        }
    }
elif sys.argv[1:3] == ["agent", "list"]:
    payload = {
        "result": {
            "agents": [
                {
                    "pane_id": "w-1:p-1",
                    "agent": "pi",
                    "name": "executor",
                    "agent_status": "idle",
                    "cwd": "/tmp/golden-work",
                    "workspace_id": "w-1",
                    "tab_id": "t-1",
                    "terminal_title_stripped": "deskops executor",
                    "state_change_seq": 7,
                    "focused": True,
                }
            ]
        }
    }
else:
    payload = {"result": {}}
print(json.dumps(payload))
"""


def _normalize_output(text: str, replacements: tuple[tuple[str, str], ...]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return STAMP_RE.sub("<stamp>", text)


def _prepare_output_repo(root: Path, home: Path) -> None:
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    for subject, arguments in OUTPUT_FIXTURE_DOCS:
        argv = ["add", subject, "--root", str(root)]
        for argument in arguments:
            argv.extend(argument)
        _cli(root, *argv, home=home)
    (root / "faq.md").write_text(
        "# Golden FAQ\n\n## What is golden?\n\nGolden output stays stable.\n\n"
        "## Why keep goldens?\n\nSibling tools parse the CLI.\n",
        encoding="utf-8",
    )


def _prepare_message_repos(base: Path, home: Path) -> tuple[Path, Path]:
    sender = base / "sender-repo"
    target = base / "target-repo"
    sender.mkdir()
    target.mkdir()
    _cli(sender, "init", str(sender), home=home)
    _cli(target, "init", str(target), home=home)
    return sender, target


def _reset_inbox(target: Path) -> None:
    for note in (target / "desk" / "inbox").glob("*.md"):
        note.unlink()


def _only_note(target: Path) -> Path:
    notes = sorted((target / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1, notes
    return notes[0]


@pytest.fixture(scope="module")
def output_golden_env(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    base = tmp_path_factory.mktemp("command-output-goldens")
    home = base / "home"
    home.mkdir()

    repo = base / "repo"
    _prepare_output_repo(repo, home)

    sender, target = _prepare_message_repos(base, home)

    herdr = base / "fake-herdr"
    herdr.write_text(FAKE_HERDR, encoding="utf-8")
    herdr.chmod(0o755)

    return {"base": base, "home": home, "repo": repo, "sender": sender, "target": target, "herdr": herdr}


def _collect_command_output_goldens(env: dict[str, Path]) -> dict[str, str]:
    home = env["home"]
    repo = env["repo"]
    sender = env["sender"]
    target = env["target"]
    repo_replacements = ((str(repo), "<root>"), (str(home), "<home>"))
    message_replacements = (
        (str(target), "<target>"),
        (str(sender), "<sender>"),
        (str(home), "<home>"),
    )
    outputs: dict[str, str] = {}

    def capture(
        name: str,
        fmt: str,
        argv: list[str],
        cwd: Path,
        replacements: tuple[tuple[str, str], ...],
    ) -> None:
        completed = _cli(cwd, *argv, "--format", fmt, home=home)
        outputs[f"{name}.{fmt}"] = _normalize_output(completed.stdout, replacements)

    for subject in LIST_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"list_{subject}",
                fmt,
                ["list", subject, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for subject, selector in SHOW_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"show_{subject}",
                fmt,
                ["show", subject, selector, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for name, argv in (
        ("atoms_list", ["atoms", "list", "--root", str(repo)]),
        ("atoms_show", ["atoms", "show", "atom-golden-one", "--root", str(repo)]),
        ("atoms_tree", ["atoms", "tree", "--root", str(repo)]),
    ):
        for fmt in FORMATS_TEXT_JSON:
            capture(name, fmt, argv, repo, repo_replacements)

    for fmt in FORMATS_TEXT_JSON_YAML:
        capture(
            "faq",
            fmt,
            ["faq", "--faq-path", str(repo / "faq.md")],
            repo,
            repo_replacements,
        )

    for fmt in FORMATS_TEXT_JSON_YAML:
        _reset_inbox(target)
        capture(
            "message_send",
            fmt,
            [
                "message",
                "send",
                f"Golden message for {fmt}.",
                "--title",
                f"Golden message {fmt}",
                "--kind",
                "suggestion",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )
        note = _only_note(target)
        capture(
            "message_list",
            fmt,
            ["message", "list", "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_read",
            fmt,
            ["message", "read", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_ack",
            fmt,
            ["message", "ack", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )

        _reset_inbox(target)
        capture(
            "inbox",
            fmt,
            [
                "inbox",
                f"Legacy golden message for {fmt}.",
                "--title",
                f"Legacy golden {fmt}",
                "--kind",
                "unclear",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )

    for fmt in FORMATS_TEXT_JSON:
        capture(
            "runtime_workers",
            fmt,
            [
                "runtime",
                "workers",
                "--root",
                str(repo),
                "--herdr",
                str(env["herdr"]),
            ],
            repo,
            repo_replacements,
        )

    return outputs


def test_command_output_goldens(
    output_golden_env: dict[str, Path], request: pytest.FixtureRequest
) -> None:
    outputs = _collect_command_output_goldens(output_golden_env)
    update = request.config.getoption("--update-golden")
    if update:
        output_dir = GOLDEN_DIR / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        for stale in output_dir.glob("*"):
            if f"output/{stale.name}" not in outputs:
                stale.unlink()
    for name, actual in sorted(outputs.items()):
        _check_golden(f"output/{name}", actual, request)
