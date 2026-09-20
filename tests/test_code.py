"""F5: the code world — symbols, test coverage and git as documents."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import code
from deskops.bootstrap import ensure_world
from deskops.world import DocId


@pytest.fixture()
def tree(tmp_path: Path) -> Path:
    """A tiny Python project: one package, one module, one test."""
    (tmp_path / "src" / "demo").mkdir(parents=True)
    (tmp_path / "src" / "demo" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "src" / "demo" / "core.py").write_text(
        '"""Demo module."""\n\n\nclass Greeter:\n    """Greets."""\n\n'
        "    def greet(self, name: str) -> str:\n"
        '        """Say hello."""\n'
        '        return f"hello {name}"\n\n\n'
        "def standalone() -> int:\n"
        "    return 1\n",
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_core.py").write_text(
        "from demo import core\n\n\ndef test_greet():\n    assert core.Greeter().greet('x') == 'hello x'\n",
        encoding="utf-8",
    )
    return tmp_path


def test_symbols_of_reads_modules_classes_and_functions(tree: Path) -> None:
    symbols = code.symbols_of(tree / "src" / "demo", "demo", repo_root=tree)

    assert set(symbols) == {
        "python:demo",
        "python:demo.core",
        "python:demo.core:Greeter",
        "python:demo.core:Greeter.greet",
        "python:demo.core:standalone",
    }
    greeter = symbols["python:demo.core:Greeter"]
    assert greeter["kind"] == "class"
    assert greeter["docstring"] == "Greets."
    assert greeter["signature"].startswith("class Greeter")
    assert greeter["qualname"] == "demo.core:Greeter"


def test_symbols_of_carries_the_source_span_and_digest(tree: Path) -> None:
    symbols = code.symbols_of(tree / "src" / "demo", "demo", repo_root=tree)

    standalone = symbols["python:demo.core:standalone"]
    start, _, end = standalone["source_span"].partition("-")
    text = (tree / "src" / "demo" / "core.py").read_text(encoding="utf-8").splitlines()
    assert text[int(start) - 1].startswith("def standalone")
    assert int(end) >= int(start)
    assert len(standalone["source_sha256"]) == 64
    assert "demo" in standalone["imports"] or standalone["imports"] == ""


def test_sync_symbols_tracks_them_once(tree: Path) -> None:
    first = code.sync_symbols(tree, tree / "src" / "demo", "demo")
    world = ensure_world(tree)
    tracked = {doc.name for doc in world.store.docs_of("PythonSymbolDoc")}

    second = code.sync_symbols(tree, tree / "src" / "demo", "demo")

    assert first.symbols == 5
    assert set(first.written) == tracked
    assert second.written == []
    assert second.unchanged == 5


def test_sync_symbols_rewrites_a_changed_symbol(tree: Path) -> None:
    code.sync_symbols(tree, tree / "src" / "demo", "demo")
    target = tree / "src" / "demo" / "core.py"
    target.write_text(
        target.read_text(encoding="utf-8").replace("return 1", "return 2"), encoding="utf-8"
    )

    report = code.sync_symbols(tree, tree / "src" / "demo", "demo")

    world = ensure_world(tree)
    payload = dict(world.store.doc(DocId.of("PythonSymbolDoc", "python:demo.core:standalone")).payload)
    assert report.written
    assert payload["source_span"].startswith("12-13") or payload["source_span"]


def test_derive_test_coverage_names_the_module_a_test_imports(tree: Path) -> None:
    written = code.derive_test_coverage(tree, "tests")

    world = ensure_world(tree)
    docs = {doc.name: dict(doc.payload) for doc in world.store.docs_of("TestCoverageDoc")}

    assert written == ["coverage-test_core--demo"]
    assert docs["coverage-test_core--demo"]["test_qualname"] == "test_core"
    assert docs["coverage-test_core--demo"]["covers_symbol"] == "python:demo"
    assert docs["coverage-test_core--demo"]["granularity"] == "module"
    assert docs["coverage-test_core--demo"]["source"] == "import_decl"


def test_derive_test_coverage_is_idempotent(tree: Path) -> None:
    code.derive_test_coverage(tree, "tests")

    assert code.derive_test_coverage(tree, "tests") == []


def test_symbol_at_resolves_a_line_to_its_innermost_symbol(tree: Path) -> None:
    symbols = code.symbols_of(tree / "src" / "demo", "demo", repo_root=tree)
    lines = (tree / "src" / "demo" / "core.py").read_text(encoding="utf-8").splitlines()
    greet_line = next(i for i, line in enumerate(lines, 1) if line.strip().startswith("def greet"))

    assert code.symbol_at(symbols, "src/demo/core.py", greet_line) == "python:demo.core:Greeter.greet"
    assert code.symbol_at(symbols, "src/demo/core.py", 99) is None


def _git(root: Path, *argv: str) -> None:
    import subprocess

    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True)


def test_sync_git_tracks_a_commit_its_changes_and_the_edge_between_them(tree: Path) -> None:
    _git(tree, "init", "-q")
    _git(tree, "config", "user.email", "test@example.com")
    _git(tree, "config", "user.name", "Test")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "demo: first cut\n\nTask-Id: task-demo")
    code.sync_symbols(tree, tree / "src" / "demo", "demo")
    target = tree / "src" / "demo" / "core.py"
    target.write_text(target.read_text(encoding="utf-8").replace("return 1", "return 2"), encoding="utf-8")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "demo: change standalone")

    report = code.sync_git(tree, limit=1, source_root="src/demo", package="demo")

    world = ensure_world(tree)
    commits = {doc.name: dict(doc.payload) for doc in world.store.docs_of("CommitDoc")}
    changes = {doc.name: dict(doc.payload) for doc in world.store.docs_of("ChangeDoc")}
    commit_id = report.commits[0]
    assert commits[commit_id]["trailers"] == {}
    assert report.changes
    change = changes[report.changes[0]]
    assert change["path"] == "src/demo/core.py"
    assert change["added"] >= 1
    edges = world.graph.targets(f"CommitDoc:{commit_id}", "contains_change")
    assert any(edge.endswith(report.changes[0]) for edge in edges)


def test_task_code_report_names_symbols_changes_and_tests(tree: Path) -> None:
    from derived_support import bind_task_plan, contract_payload, create, make_world, target_payload
    from deskops import forms

    forms.create_task(tree, title="Code report", goal="g", scope="s")
    world = make_world(tree)
    code.sync_symbols(tree, tree / "src" / "demo", "demo", world=world)
    code.derive_test_coverage(tree, "tests", world=world)
    contract = contract_payload("contract-report", "demo.core:standalone")
    create(world, "SymbolContractDoc", "contract-report", contract, "desk/plans")
    bind_task_plan(
        world,
        "task-code-report",
        "plan-report",
        [target_payload("plan-target-report", contract="SymbolContractDoc:contract-report")],
    )
    _git(tree, "init", "-q")
    _git(tree, "config", "user.email", "test@example.com")
    _git(tree, "config", "user.name", "Test")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "demo: cut")
    code.sync_git(tree, limit=1, source_root="src/demo", package="demo", world=world)

    report = code.task_code_report(tree, "task-code-report")

    assert report["symbols"] == ["demo.core:standalone"]
    assert any(entry["symbol"] == "demo.core:standalone" for entry in report["changes"])
    assert report["commits"]
    assert report["tests"] == ["test_core"]
