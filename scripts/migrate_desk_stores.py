#!/usr/bin/env python3
"""Migrate every discovered sldb store that tracks deskops models.

Discovery walks ``--home`` (default ``~``) for ``.sldb`` directories that track
``TaskDoc``, live inside a git work tree, and do not sit under a path segment the
migration deliberately skips.  ``--dry-run`` (the default) prints the stores and
the commands that ``--apply`` would run; ``--apply`` runs them and logs the
before/after ``sldb stores check`` result of each store.
"""

from __future__ import annotations

import argparse
import importlib
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) in sys.path:
    sys.path.remove(str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT))

import yaml  # noqa: E402
from sldb.store.hashing import hash_model_contract  # noqa: E402

EXCLUDED_SEGMENTS = frozenset({
    ".cache",
    ".claude",
    ".tmp",
    ".venv",
    "node_modules",
    "tools",
    "tmp",
})
# Repositories the owner forbids this migration to touch, relative to the discovery
# root and as absolute paths. A store anywhere below them is never discovered.
PROTECTED_RELATIVE_ROOTS = (Path("proyectos") / "kimun",)
PROTECTED_ABSOLUTE_ROOTS = (Path("/home/jp/proyectos/kimun"),)
COMMAND_TIMEOUT_SECONDS = 300
LOG_DIR = REPO_ROOT / "runs" / "planning"

Command = list[str]


@dataclass
class CommandResult:
    """One subprocess invocation and its outcome."""

    command: Command
    returncode: int | None
    stdout: str = ""
    stderr: str = ""
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and self.returncode == 0


@dataclass
class StoreResult:
    """The migration outcome for one store."""

    store: Path
    models: list[str]
    before: CommandResult
    steps: list[CommandResult]
    after: CommandResult | None
    ok: bool


def _walk_error(error: OSError) -> None:
    """Skip directories that raise PermissionError; surface anything else."""
    if not isinstance(error, PermissionError):
        raise error


def is_excluded(store: Path, root: Path) -> bool:
    """Whether a store path has an excluded segment relative to the discovery root."""
    try:
        relative = store.relative_to(root)
    except ValueError:
        relative = store
    return any(part in EXCLUDED_SEGMENTS for part in relative.parts)


def is_protected(path: Path, root: Path) -> bool:
    """Whether a path lies under a repository the migration must never touch."""
    resolved = path.resolve()
    if any(resolved == base or base in resolved.parents for base in PROTECTED_ABSOLUTE_ROOTS):
        return True
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return False
    return any(relative == base or base in relative.parents for base in PROTECTED_RELATIVE_ROOTS)


def _is_git_work_tree(repo: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def discover_stores(home: Path | str) -> list[Path]:
    """Find every TaskDoc-tracking store under ``home`` that belongs to a repo."""
    root = Path(home).expanduser().resolve()
    if not root.is_dir():
        return []

    stores: list[Path] = []
    for dirpath, dirnames, _filenames in os.walk(
        root, followlinks=False, onerror=_walk_error
    ):
        # Excluded segments are pruned by name; because only segments relative to
        # ``root`` are inspected, a discovery root that itself lives under /tmp is
        # still scanned.
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_SEGMENTS]

        current = Path(dirpath)
        if is_protected(current, root):
            dirnames[:] = []
            continue
        if current.name != ".sldb":
            continue

        # Never descend into a store, matched or not.
        dirnames[:] = []
        if not (current / "core" / "models" / "TaskDoc.yaml").is_file():
            continue
        if is_excluded(current, root) or is_protected(current, root):
            continue
        if _is_git_work_tree(current.parent):
            stores.append(current.resolve())

    return sorted(set(stores))


def _model_index_entry(entry: dict, store: Path) -> Path:
    """Resolve a store-index path, which is relative to the repository root."""
    path = entry.get("models_index")
    if path:
        return store.parent / path
    return store / "core" / "models" / f"{entry['name']}.yaml"


def changed_models(store: Path) -> list[str]:
    """Deskops models registered in ``store`` whose contract hash no longer matches."""
    store = Path(store).resolve()
    index_path = store / "core" / "store_index.yaml"
    if not index_path.is_file():
        return []
    try:
        payload = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return []

    changed: list[str] = []
    for entry in payload.get("models") or []:
        name = entry.get("name")
        model_ref = entry.get("model_ref") or ""
        if not name or not model_ref.startswith("deskops.models:"):
            continue

        module_name, _, class_name = model_ref.partition(":")
        try:
            model_type = getattr(importlib.import_module(module_name), class_name)
            current_hash = hash_model_contract(model_type)
        except Exception:
            # A model that cannot be imported from this checkout is not ours to
            # re-hash; leave it to its owner store.
            continue

        model_index = _model_index_entry(entry, store)
        previous_hash = None
        if model_index.is_file():
            try:
                model_payload = (
                    yaml.safe_load(model_index.read_text(encoding="utf-8")) or {}
                )
                previous_hash = model_payload.get("contract_hash")
            except (OSError, yaml.YAMLError):
                previous_hash = None

        if previous_hash != current_hash:
            changed.append(str(name))

    return sorted(changed)


def plan_store(store: Path) -> tuple[list[str], list[Command]]:
    """The models to re-hash and the commands that migrate one store."""
    store = Path(store).resolve()
    target = store.parent
    models = changed_models(store)

    commands: list[Command] = [
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store)]
    ]
    for model in models:
        commands.append(
            [
                sys.executable,
                "-m",
                "sldb",
                "models",
                "update",
                model,
                "--store",
                str(store),
                "--pythonpath",
                str(REPO_ROOT),
            ]
        )
    commands.append(
        [
            sys.executable,
            "-m",
            "deskops",
            "desk",
            "update",
            "--root",
            str(target),
            "--apply",
        ]
    )
    commands.append(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(store)]
    )
    return models, commands


def format_command(command: Sequence[str]) -> str:
    """Render a command for the dry-run output and the log."""
    return shlex.join(command)


def _environment() -> dict[str, str]:
    """Run every subprocess against this checkout, not an installed earlier copy."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) + (
        os.pathsep + existing if existing else ""
    )
    return env


def run_command(command: Sequence[str], env: dict[str, str]) -> CommandResult:
    """Run one command, turning a 300 s timeout into a recorded FAIL."""
    argv = list(command)
    try:
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            argv,
            None,
            _as_text(exc.stdout),
            _as_text(exc.stderr),
            f"timeout after {COMMAND_TIMEOUT_SECONDS}s",
        )
    except OSError as exc:
        return CommandResult(argv, None, error=str(exc))
    return CommandResult(argv, completed.returncode, completed.stdout, completed.stderr)


def _as_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    return value if isinstance(value, str) else value.decode(errors="replace")


def _verdict_line(result: CommandResult) -> str:
    for line in reversed(result.stdout.splitlines()):
        stripped = line.strip()
        if stripped.startswith(("PASS:", "FAIL:")):
            return stripped
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return lines[-1] if lines else ""


def _result_label(result: CommandResult) -> str:
    state = "PASS" if result.ok else "FAIL"
    detail = result.error or f"exit {result.returncode}"
    verdict = _verdict_line(result)
    return f"{state} ({detail})" + (f" — {verdict}" if verdict else "")


def _failure_output(result: CommandResult, max_lines: int = 20) -> list[str]:
    if result.ok:
        return []
    lines = ["```"]
    stderr = result.stderr.strip()
    if stderr:
        lines.extend(stderr.splitlines()[-max_lines:])
    stdout_lines = [line for line in result.stdout.splitlines() if line.strip()]
    if stdout_lines:
        lines.extend(stdout_lines[-max_lines:])
    lines.append("```")
    return lines


def log_path() -> Path:
    stamp = datetime.now().strftime("%Y%m%d")
    return LOG_DIR / f"store-migration-{stamp}.md"


def write_log(
    home: Path,
    plans: Sequence[tuple[Path, list[str], list[Command]]],
    *,
    mode: str,
    results: Sequence[StoreResult] | None = None,
) -> Path:
    """Write the dated migration log, starting with the discovered store list."""
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Store migration — {datetime.now():%Y-%m-%d}",
        "",
        f"Mode: {mode}",
        f"Root: {home}",
        f"Discovered stores: {len(plans)}",
        "",
        "## Discovered stores",
        "",
    ]
    for position, (store, _models, _commands) in enumerate(plans, 1):
        lines.append(f"{position}. `{store}`")
    lines.append("")

    if mode == "dry-run":
        lines.extend(["## Planned commands", ""])
        for store, models, commands in plans:
            lines.append(f"### `{store}`")
            if models:
                lines.append(f"Models to update: {', '.join(models)}")
            else:
                lines.append("Models to update: none")
            for command in commands:
                lines.append(f"- `{format_command(command)}`")
            lines.append("")
    else:
        lines.extend(["## Results", ""])
        for result in results or []:
            lines.append(f"### `{result.store}`")
            if result.models:
                lines.append(f"Models updated: {', '.join(result.models)}")
            else:
                lines.append("Models updated: none")
            lines.append(f"Before: {_result_label(result.before)}")
            for step in result.steps:
                lines.append(f"- `{format_command(step.command)}`")
                lines.append(f"  {_result_label(step)}")
                lines.extend(f"  {line}" for line in _failure_output(step))
            lines.append(
                "After: "
                + (_result_label(result.after) if result.after else "not run")
            )
            lines.append(f"Result: {'PASS' if result.ok else 'FAIL'}")
            lines.append("")

        passed = sum(1 for result in results or [] if result.ok)
        lines.append(
            f"Summary: {passed}/{len(results or [])} stores PASS"
        )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _apply_store(
    store: Path, models: list[str], commands: list[Command], env: dict[str, str]
) -> StoreResult:
    """Run one store's migration; a failed command stops this store, not the run."""
    before = run_command(commands[0], env)
    steps: list[CommandResult] = []
    ok = True

    for command in commands[1:-1]:
        result = run_command(command, env)
        steps.append(result)
        if not result.ok:
            ok = False
            break

    after: CommandResult | None = None
    if ok:
        after = run_command(commands[-1], env)
        steps.append(after)
        ok = after.ok

    return StoreResult(
        store=store,
        models=models,
        before=before,
        steps=steps,
        after=after,
        ok=ok,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Migrate every sldb store under --home that tracks deskops models. "
            "Dry-run is the default."
        )
    )
    parser.add_argument(
        "--home",
        default=None,
        help="Discovery root (default: the current user's home directory).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        dest="mode",
        action="store_const",
        const="dry-run",
        help="List stores and commands without running anything (default).",
    )
    mode.add_argument(
        "--apply",
        dest="mode",
        action="store_const",
        const="apply",
        help="Run the migration for every discovered store.",
    )
    parser.set_defaults(mode="dry-run")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    """CLI entry point."""
    args = _build_parser().parse_args(list(argv) if argv is not None else None)
    home = Path(args.home).expanduser() if args.home else Path.home()
    stores = discover_stores(home)

    print(f"Discovered {len(stores)} store(s) under {home}:")
    for position, store in enumerate(stores, 1):
        print(f"{position}. {store}")

    plans = [(store, *plan_store(store)) for store in stores]

    if args.mode == "dry-run":
        print()
        print("Commands:")
        for store, models, commands in plans:
            print(f"[{store}]")
            print(f"  models to update: {', '.join(models) if models else 'none'}")
            for command in commands:
                print(f"  {format_command(command)}")
        path = write_log(home, plans, mode="dry-run")
        print()
        print(f"Log: {path}")
        return 0 if stores else 1

    env = _environment()
    results: list[StoreResult] = []
    print()
    for store, models, commands in plans:
        print(f"[{store}]")
        result = _apply_store(store, models, commands, env)
        results.append(result)
        print(f"  before: {_result_label(result.before)}")
        for step in result.steps:
            print(f"  {_result_label(step)}")
        if result.after is None:
            print("  after: not run")
        print(f"  result: {'PASS' if result.ok else 'FAIL'}")

    path = write_log(home, plans, mode="apply", results=results)
    passed = sum(1 for result in results if result.ok)
    print()
    print(f"Summary: {passed}/{len(results)} stores PASS")
    print(f"Log: {path}")
    return 0 if stores and passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
