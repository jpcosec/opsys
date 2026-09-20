"""The code world: what the task touches, when, and which tests to run.

F5. Three derived document families, never authored:

- `PythonSymbolDoc` (sldb's model): one per module/class/function, with the
  source span, hash, signature, docstring and imports.
- `TestCoverageDoc`: which test exercises which module, from the test's
  declared imports (module granularity, without running anything).
- `CommitDoc` / `ChangeDoc`: git history as documents, with each hunk resolved
  to the symbol whose span contains it.

`sldb selfdoc python-sync` cannot write the symbols here: it requires the AST
relation types (`contains`) declared with the snapshot's node types
(`python_module`/`python_symbol`), which collide with the document-graph
vocabulary in this store (gap-log, desk/pron-gap-log.md). The symbol inventory
comes from the same scan deskops reaches through the seam
(`deskops.world.scan_python_facts`); signature and docstring are read from the
source with the stdlib `ast` because the scan does not carry them.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
import re
import subprocess
from typing import Any

from deskops.world import DocId
from deskops.world import World

SYMBOL_MODEL = "PythonSymbolDoc"
COVERAGE_MODEL = "TestCoverageDoc"
COMMIT_MODEL = "CommitDoc"
CHANGE_MODEL = "ChangeDoc"

# Where the derived code documents are tracked inside the desk.
SYMBOL_DIR = Path("desk/code/symbols")
COVERAGE_DIR = Path("desk/code/coverage")
GIT_DIR = Path("desk/code/git")

NOT_DOCUMENTED = "Not documented."

HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


@dataclass(frozen=True)
class SymbolSyncReport:
    """What one `sync_symbols` run found and wrote."""

    files: int = 0
    symbols: int = 0
    written: list[str] = field(default_factory=list)
    unchanged: int = 0


def _carries(stored: dict[str, Any], derived: dict[str, Any]) -> bool:
    """Whether a stored payload already holds every derived value.

    The store's model adds fields of its own (`architecture_spec` defaults to
    "Not declared."), so the comparison is one way: every field this module
    derives must be there, with the same value.
    """
    return all(stored.get(key) == value for key, value in derived.items())


def _module_id(module: str) -> str:
    return f"python:{module}"


def _payload(
    *,
    symbol_id: str,
    module: str,
    path: str,
    qualname: str,
    kind: str,
    signature: str,
    docstring: str,
    imports: list[str],
    line_start: int,
    line_end: int,
    digest: str,
    purpose: str = NOT_DOCUMENTED,
    architecture: str = NOT_DOCUMENTED,
) -> dict[str, Any]:
    """One PythonSymbolDoc payload, with the derived fields sldb's model declares."""
    return {
        "id": symbol_id,
        "system": module.split(".")[0],
        "module": module,
        "qualname": qualname,
        "kind": kind,
        "source_path": path,
        "source_span": f"{line_start}-{line_end}",
        "source_sha256": digest,
        "signature": signature,
        "docstring": docstring or "",
        "imports": "\n".join(imports),
        "purpose": purpose,
        "architecture": architecture,
        "provenance": path,
        "tags": ["type:python-symbol"],
    }


def _qualname(module: str, name: str) -> str:
    return f"{module}:{name}"


def _signature(source: list[str], node: ast.AST) -> str:
    """The source text of the definition line, whitespace collapsed."""
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):  # pragma: no cover
        return ""
    text = " ".join(part.strip() for part in source[node.lineno - 1 : (node.body[0].lineno - 1) or node.lineno])
    return " ".join(text.split()).rstrip(":")


def _module_symbol(module: str, path: str, imports: list[str], digest: str, lines: int) -> dict[str, Any]:
    return _payload(
        symbol_id=_module_id(module),
        module=module,
        path=path,
        qualname=module,
        kind="module",
        signature=f"module {module}",
        docstring="",
        imports=imports,
        line_start=1,
        line_end=lines,
        digest=digest,
    )


def _walk_nodes(tree: ast.AST, prefix: str = "") -> list[tuple[ast.AST, str]]:
    """Every class/function of a tree, with the dotted path that nests it.

    A method is named by its class (`Greeter.greet`), so two classes with a
    method of the same name stay two symbols.
    """
    found: list[tuple[ast.AST, str]] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            path = f"{prefix}{node.name}"
            found.append((node, path))
            found.extend(_walk_nodes(node, f"{path}."))
    return found


def _repo_relative(source_root: Path, repo_root: str | Path | None, path: str) -> str:
    """A scanned file's path relative to the repository, which is what git reports."""
    if repo_root is None:
        return path
    try:
        prefix = source_root.relative_to(Path(repo_root).resolve())
    except ValueError:
        return path
    return path if str(prefix) == "." else f"{prefix}/{path}"


def symbols_of(
    source_root: str | Path,
    package: str | None = None,
    repo_root: str | Path | None = None,
) -> dict[str, dict[str, Any]]:
    """Every symbol of a Python tree, keyed by its document id.

    Module ids follow the scan (`python:<module>`, dots and all); a class or
    function is `python:<module>:<dotted path inside the module>`. With
    `repo_root`, `source_path` is repository-relative, which is how git names
    the same file.
    """
    from deskops.world import scan_python_facts

    root = Path(source_root).resolve()
    facts = scan_python_facts(root, package)
    found: dict[str, dict[str, Any]] = {}
    for fact in facts:
        module = fact["module"]
        path = _repo_relative(root, repo_root, fact["path"])
        digest = fact["hash"]
        imports = sorted({str(binding["module"]) for binding in fact.get("imports", [])})
        text = (root / fact["path"]).read_text(encoding="utf-8")
        lines = text.splitlines()
        tree = ast.parse(text)
        found[_module_id(module)] = _module_symbol(module, path, imports, digest, len(lines))
        for node, dotted in _walk_nodes(tree):
            symbol_id = f"python:{module}:{dotted}"
            kind = "class" if isinstance(node, ast.ClassDef) else "function"
            found[symbol_id] = _payload(
                symbol_id=symbol_id,
                module=module,
                path=path,
                qualname=_qualname(module, dotted),
                kind=kind,
                signature=_signature(lines, node),
                docstring=ast.get_docstring(node) or "",
                imports=imports,
                line_start=node.lineno,
                line_end=node.end_lineno or node.lineno,
                digest=digest,
            )
    return found


def sync_symbols(
    root: str | Path,
    source_root: str | Path,
    package: str | None = None,
    *,
    world: World | None = None,
) -> SymbolSyncReport:
    """Track the symbols of `source_root` as documents, idempotent.

    A symbol whose payload did not change is left alone; a changed one is
    rewritten in place, which keeps the "what changed" question answerable
    without re-reading the whole tree every time.
    """
    from deskops.bootstrap import ensure_world

    world = world or ensure_world(root)
    found = symbols_of(source_root, package, repo_root=root)
    written: list[str] = []
    unchanged = 0
    for symbol_id, payload in found.items():
        name = symbol_id
        doc_id = DocId.of(SYMBOL_MODEL, name)
        existing = world.store.doc(doc_id)
        if existing is not None and _carries(dict(existing.payload), payload):
            unchanged += 1
            continue
        path = SYMBOL_DIR / f"{name.replace(':', '__')}.md"
        if existing is None:
            world.store.create(doc_id, payload, path)
        else:
            world.store.replace(doc_id, payload)
        written.append(name)
    return SymbolSyncReport(
        files=len({payload["source_path"] for payload in found.values()}),
        symbols=len(found),
        written=written,
        unchanged=unchanged,
    )


def _tests_of(root: Path, source_root: str, package: str | None) -> list[dict[str, Any]]:
    """The test modules of a tree, with the modules they import."""
    from deskops.world import scan_python_facts

    tree = Path(source_root)
    if not tree.exists():
        raise FileNotFoundError(f"No test tree at {tree}")
    facts = scan_python_facts(tree.resolve(), package)
    return [
        {
            "module": fact["module"],
            "path": fact["path"],
            "imports": sorted({str(binding["module"]) for binding in fact.get("imports", [])}),
            "symbols": [symbol["id"] for symbol in fact.get("symbols", [])],
        }
        for fact in facts
    ]


def derive_test_coverage(
    root: str | Path,
    source_root: str | Path = "tests",
    package: str | None = None,
    *,
    world: World | None = None,
) -> list[str]:
    """One TestCoverageDoc per (test module, module it imports), idempotent.

    Granularity is the module: `deskops.cli.main` covered by
    `tests.test_cli`. The symbol-level answer needs the call graph, which sldb
    documents it does not resolve (gap-log).
    """
    from deskops.bootstrap import ensure_world

    root_path = Path(root).resolve()
    world = world or ensure_world(root_path)
    tree = Path(source_root)
    if not tree.is_absolute():
        tree = root_path / tree
    written: list[str] = []
    for module in _tests_of(root_path, str(tree), package):
        for imported in module["imports"]:
            if imported.startswith("_"):
                continue
            name = f"coverage-{module['module']}--{imported}"
            payload = {
                "id": name,
                "title": f"{module['module']} covers {imported}",
                "test_qualname": module["module"],
                "covers_symbol": _module_id(imported),
                "granularity": "module",
                "source": "import_decl",
                "tags": ["type:test-coverage"],
            }
            doc_id = DocId.of(COVERAGE_MODEL, name)
            existing = world.store.doc(doc_id)
            if existing is not None and _carries(dict(existing.payload), payload):
                continue
            path = COVERAGE_DIR / f"{name}.md"
            if existing is None:
                world.store.create(doc_id, payload, path)
            else:
                world.store.replace(doc_id, payload)
            written.append(name)
    return written


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=root, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout


@dataclass(frozen=True)
class GitSyncReport:
    """What one `sync_git` run wrote."""

    commits: list[str] = field(default_factory=list)
    changes: list[str] = field(default_factory=list)


def symbols_in_range(
    symbols: dict[str, dict[str, Any]], path: str, start: int, end: int
) -> list[str]:
    """Every symbol of `path` whose span overlaps `[start, end]`, innermost first."""
    found: list[tuple[int, str]] = []
    for symbol_id, payload in symbols.items():
        if payload["source_path"] != path:
            continue
        lo, _, hi = str(payload["source_span"]).partition("-")
        try:
            low, high = int(lo), int(hi or lo)
        except ValueError:  # pragma: no cover - malformed span
            continue
        if low <= end and start <= high:
            found.append((high - low, symbol_id))
    return [symbol_id for _, symbol_id in sorted(found)]


def symbol_at(symbols: dict[str, dict[str, Any]], path: str, line: int) -> str | None:
    """The innermost symbol of `path` whose source span contains `line`."""
    best: tuple[int, str] | None = None
    for symbol_id, payload in symbols.items():
        if payload["source_path"] != path:
            continue
        start, _, end = str(payload["source_span"]).partition("-")
        try:
            if int(start) <= line <= int(end or start):
                span = int(end or start) - int(start)
                if best is None or span < best[0]:
                    best = (span, symbol_id)
        except ValueError:  # pragma: no cover - malformed span
            continue
    return None if best is None else best[1]


def sync_git(
    root: str | Path,
    *,
    limit: int = 1,
    source_root: str | Path = "deskops",
    package: str | None = None,
    world: World | None = None,
) -> GitSyncReport:
    """Track the last `limit` commits as CommitDoc/ChangeDoc documents.

    Each change is one file of one commit, its line range resolved to the symbol
    of `source_root` that contains it.
    """
    from deskops.bootstrap import ensure_world

    root_path = Path(root).resolve()
    world = world or ensure_world(root_path)
    symbols = symbols_of(root_path / source_root, package, repo_root=root_path)
    report = GitSyncReport()
    log = _git(root_path, "log", f"-{limit}", "--format=%H%x1f%an%x1f%cI%x1f%B%x1e")
    for entry in [item for item in log.split("\x1e") if item.strip()]:
        sha, author, committed_at, message = entry.strip().split("\x1f", 3)
        commit_id = f"commit-{sha[:12]}"
        report.commits.append(commit_id)
        numstat = _git(root_path, "show", "--numstat", "--format=", sha)
        diff = _git(root_path, "show", "--unified=0", "--format=", sha)
        starts = _change_starts(diff)
        for line in numstat.splitlines():
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            added, removed, path = parts
            if path not in starts or _is_bookkeeping(path):
                continue
            start, end = starts[path]
            change_id = f"change-{sha[:12]}-{path.replace('/', '-')}"
            payload = {
                "id": change_id,
                "title": f"{path} @ {sha[:12]}",
                "path": path,
                "line_start": start,
                "line_end": end,
                "added": int(added or 0) if added.isdigit() else 0,
                "removed": int(removed or 0) if removed.isdigit() else 0,
                "symbol": symbol_at(symbols, path, start) or "",
                "tags": ["type:change"],
            }
            doc_id = DocId.of(CHANGE_MODEL, change_id)
            if world.store.doc(doc_id) is None:
                world.store.create(doc_id, payload, GIT_DIR / f"{change_id}.md")
            else:
                world.store.replace(doc_id, payload)
            report.changes.append(change_id)
            _link_change(world, commit_id, change_id)
        commit_doc = DocId.of(COMMIT_MODEL, commit_id)
        commit_payload = {
            "id": commit_id,
            "title": f"{commit_id}: {message.strip().splitlines()[0] if message.strip() else sha}",
            "sha": sha,
            "author": author,
            "committed_at": committed_at,
            "message": message.strip(),
            "trailers": _trailers(message),
            "tags": ["type:commit"],
        }
        if world.store.doc(commit_doc) is None:
            world.store.create(commit_doc, commit_payload, GIT_DIR / f"{commit_id}.md")
        else:
            world.store.replace(commit_doc, commit_payload)
    return report


def _link_change(world: World, commit_id: str, change_id: str) -> None:
    """Track the authored `contains_change` edge from a commit to one change."""
    relation = f"rel-{commit_id}-contains-{change_id}"
    doc_id = DocId.of("RelationDoc", relation)
    if world.store.doc(doc_id) is not None:
        return
    world.store.create(
        doc_id,
        {
            "title": f"{commit_id} contains {change_id}",
            "source_id": f"{COMMIT_MODEL}:{commit_id}",
            "target_id": f"{CHANGE_MODEL}:{change_id}",
            "relation_type": "contains_change",
            "tags": ["layer.topology"],
        },
        GIT_DIR / f"{relation}.md",
    )


def _is_bookkeeping(path: str) -> bool:
    """Whether a changed path is the world's own record rather than code.

    The store, the desk documents and the derived code documents are written by
    this harness: counting them would make every sync look like a code change.
    A change is a Python file outside the store.
    """
    return path.startswith(".sldb/") or not path.endswith(".py")


def _trailers(message: str) -> dict[str, str]:
    """The `Key: value` trailer lines of a commit message."""
    found: dict[str, str] = {}
    for line in message.splitlines():
        key, sep, value = line.partition(":")
        if sep and key and key[0].isupper() and " " not in key.strip():
            found[key.strip()] = value.strip()
    return found


def _change_starts(diff: str) -> dict[str, tuple[int, int]]:
    """The first changed range of every file in a unified diff."""
    found: dict[str, tuple[int, int]] = {}
    current: str | None = None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if line.startswith("@@") and current:
            match = HUNK_RE.match(line)
            if match:
                start = int(match.group(1))
                count = int(match.group(2) or 1)
                found.setdefault(current, (start, start + max(count - 1, 0)))
    return found


def task_code_report(root: str | Path, task_id: str) -> dict[str, Any]:
    """What a task touches in the code world: symbols, changes and tests.

    The F5 gate: given a task, name the symbols its contracts declare, the
    commits/changes that touched them, and the tests covering their modules.
    """
    from deskops.bootstrap import ensure_world
    from deskops.derived_conditions import task_slice

    root_path = Path(root).resolve()
    world = ensure_world(root_path)
    slice_ = task_slice(world, task_id)
    symbols = {
        str(contract.payload.get("qualname", "")): contract.ref for contract in slice_.contracts
    }
    changes: list[dict[str, Any]] = []
    commits: list[str] = []
    for doc in world.store.docs_of(CHANGE_MODEL):
        payload = dict(doc.payload)
        touched = [
            qualname
            for qualname in _symbols_touching(world, str(payload["path"]), payload)
            if qualname in symbols
        ]
        if not touched:
            continue
        changes.append({"change": doc.name, "path": payload["path"], "symbol": touched[0]})
        for commit in world.graph.sources(f"{CHANGE_MODEL}:{doc.name}", "contains_change"):
            name = commit.rsplit(":", 1)[-1]
            if name not in commits:
                commits.append(name)
    tests: list[str] = []
    for doc in world.store.docs_of(COVERAGE_MODEL):
        payload = dict(doc.payload)
        covered = _module_of(world, str(payload.get("covers_symbol", "")))
        if covered and any(qualname.startswith(covered) for qualname in symbols):
            tests.append(str(payload.get("test_qualname", "")))
    return {
        "task": slice_.task.ref,
        "contracts": list(symbols.values()),
        "symbols": list(symbols),
        "changes": changes,
        "commits": commits,
        "tests": sorted(set(tests)),
    }


def _symbols_touching(world: World, path: str, change: dict[str, Any]) -> list[str]:
    """The qualnames of every tracked symbol whose span overlaps a change.

    A hunk that rewrites a line inside a function touches that function even
    when the hunk starts on the `def` line of the module.
    """
    start = int(change.get("line_start") or 0)
    end = int(change.get("line_end") or start)
    touched: list[str] = []
    for doc in world.store.docs_of(SYMBOL_MODEL):
        payload = dict(doc.payload)
        if payload.get("source_path") != path:
            continue
        lo, _, hi = str(payload.get("source_span", "")).partition("-")
        try:
            low, high = int(lo), int(hi or lo)
        except ValueError:  # pragma: no cover - malformed span
            continue
        if low <= end and start <= high:
            qualname = str(payload.get("qualname", ""))
            if qualname and qualname not in touched:
                touched.append(qualname)
    return touched


def _qualname_for_symbol(world: World, symbol_id: str) -> str:
    """The qualname of a PythonSymbolDoc, by node id or document name."""
    if not symbol_id:
        return ""
    doc = world.store.doc(DocId.of(SYMBOL_MODEL, symbol_id))
    if doc is None:
        return ""
    return str(dict(doc.payload).get("qualname", ""))


def _module_of(world: World, symbol_id: str) -> str:
    """The module a coverage document points at."""
    doc = world.store.doc(DocId.of(SYMBOL_MODEL, symbol_id))
    if doc is None:
        return ""
    return str(dict(doc.payload).get("module", ""))

