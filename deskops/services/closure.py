"""One closure path for task bundles.

Every way of closing a task ends here: ``deskops closeout commit`` (run-linked
and manual routes), ``deskops closeout supersede``, ``deskops closeout retire``,
and the legacy ``close_auto`` hook. The service owns the whole closure, and
``verify_task_closeout`` with it: closeout gates for a board-routed task, Board
update, store untracking, bundle removal, exactly one closing commit carrying
the route's trailers, and the append-only index entry.

``advance`` no longer closes: it refuses at the closeout node and points here.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
from typing import TYPE_CHECKING

import yaml

from deskops import doc_access
from deskops.constants import SKILL_TREE_PREFIXES
from deskops.models import BoardDoc
from deskops.models import TaskDoc
from deskops import lifecycle
from deskops.models.task_types import canonical_task_type_name
from deskops.models.task_types import closeout_evidence_kinds
from deskops.models.task_types import declared_evidence_list
from deskops.services import closeout_gates as closeout_gates_module
from deskops.services.atoms import reference_points_to_atom

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations
    from deskops.services.closeout_gates import CloseoutGraph


#: Engine of the ``evidence`` receipts ``deskops closeout verify`` writes (CC33a).
EVIDENCE_ENGINE = "deskops-closeout"

#: The lifecycle node the closeout rules read the task at (the source of ``task_completes``).
CLOSEOUT_NODE = "ritual-closeout"


class ClosureCommitError(RuntimeError):
    """The closing commit could not be made; the desk was restored."""


@dataclass
class ClosureOutcome:
    """What one closure did, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CloseoutGateReport:
    ok: bool
    evidence: list[str]
    findings: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "evidence": list(self.evidence),
            "findings": [dict(item) for item in self.findings],
        }


class ClosureService:
    """Build the closing commit and its run-index entry as one clean unit.

    ``runs/subagents/index.jsonl`` records ``task_id``, ``run_dir`` and the
    route fields, but not the closing commit hash: the index line is written
    after the commit exists and folded into that same commit with one
    ``git commit --amend --no-edit``, which changes the hash. ``commit`` is
    therefore always null in new entries. Readers resolve the closing commit
    with ``git log -1 --grep 'Task-Id: <task_id>'``, using the trailer every
    closing commit already carries. The amend is limited to the index path so
    the working tree is clean when the command returns.
    """

    REQUIRED_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]

    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self._gate_notes: list[str] = []

    # ---------------------------------------------------------------- routes
    def close_manual(
        self,
        task_id: str,
        *,
        reason: str,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["--no-run needs a non-empty --reason saying why the task closes without a subagent run."],
            )
        subject = message or self._default_subject(task_id)
        trailers = [f"Task-Id: {task_id}", "Closeout-Mode: manual", f"Closeout-Reason: {reason}"]
        return self._close(
            task_id,
            route="manual",
            subject=subject,
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=paths is not None,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "manual",
            },
            success_line=f"Closing commit {{commit}} made manually (no run): {reason}",
        )

    def close_superseded(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Close a task whose subject no longer exists, from any lifecycle node.

        No evidence gates run: tests, atoms and a run would all describe work
        that was never done. The reason and at least one resolvable ref (an
        ancestor commit or an existing path) are the evidence instead, and the
        closing commit says ``Closeout-Mode: superseded``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Supersede needs a non-empty --reason saying why the task's subject no longer exists."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Supersede needs at least one --ref naming an ancestor commit or an existing path."],
            )
        unresolved = [ref for ref in cleaned_refs if not self._ref_resolves(ref)]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need an ancestor commit or an existing path)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        original = task_path.read_bytes()
        payload = doc_access.read_doc(task_path, TaskDoc)
        payload["status"] = "superseded"
        payload["history"] = [*(payload.get("history") or []), "superseded"]
        try:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        except Exception as exc:  # noqa: BLE001 - a task that cannot record superseded is not closed
            task_path.write_bytes(original)
            return ClosureOutcome(1, [f"Could not record superseded status on {task_id}: {exc}"])

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: superseded",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        try:
            outcome = self._close(
                task_id,
                route="superseded",
                subject=message or self._default_subject(task_id),
                trailers=trailers,
                paths=list(paths or []),
                explicit_paths=True,
                run_gates=False,
                index_entry={
                    "task_id": task_id,
                    "run_id": None,
                    "run_dir": None,
                    "session_sha256": None,
                    "mode": "superseded",
                },
                success_line=f"Closing commit {{commit}} made in superseded mode: {reason}",
            )
        except Exception:
            task_path.write_bytes(original)
            raise
        if outcome.exit_code != 0:
            task_path.write_bytes(original)
        return outcome

    def close_resolved_by(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        tests: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Close a task whose work already entered the history, for example through a PR.

        The per-file atom gate does not run: the work is already committed. The
        evidence is a reason, at least one ``--ref`` that is HEAD or an ancestor
        commit (further refs may be ancestor commits or http(s) URLs, such as the
        PR) and at least one ``--test`` the tests gate accepts for the task's
        ``files``. Every ref and test must resolve; a refusal writes nothing.
        The task is marked ``resolved`` and the closing commit says
        ``Closeout-Mode: resolved-by``.
        """
        gates = self._ops.closeout_gates
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Resolved-by needs a non-empty --reason saying where the task's work entered the history."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        unresolved_refs = [
            ref
            for ref in cleaned_refs
            if not gates.reference_points_to_commit(ref) and not gates.reference_points_to_url(ref)
        ]
        if unresolved_refs:
            return ClosureOutcome(
                1,
                [
                    f"Unresolvable --ref: {', '.join(unresolved_refs)} "
                    "(need a commit that is HEAD or an ancestor, or an http(s) URL)."
                ],
            )
        if not any(gates.reference_points_to_commit(ref) for ref in cleaned_refs):
            return ClosureOutcome(
                1,
                ["Resolved-by needs at least one --ref naming a commit that is HEAD or an ancestor."],
            )

        cleaned_tests = [str(test).strip() for test in tests or [] if str(test).strip()]
        if not cleaned_tests:
            return ClosureOutcome(
                1,
                ["Resolved-by needs at least one --test naming a test file the tests gate accepts."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        original = task_path.read_bytes()
        payload = doc_access.read_doc(task_path, TaskDoc)
        task_files = list(payload.get("files") or [])
        unresolved_tests = [test for test in cleaned_tests if not gates.reference_points_to_test(test, files=task_files)]
        if unresolved_tests:
            return ClosureOutcome(
                1,
                [
                    f"Unresolvable --test: {', '.join(unresolved_tests)} "
                    "(need an existing .py file under a tests/ directory or declared in the task's files)."
                ],
            )

        payload["status"] = "resolved"
        payload["history"] = [*(payload.get("history") or []), "resolved-by"]
        try:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        except Exception as exc:  # noqa: BLE001 - a task that cannot record resolved is not closed
            task_path.write_bytes(original)
            return ClosureOutcome(1, [f"Could not record resolved status on {task_id}: {exc}"])

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: resolved-by",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
            *[f"Closeout-Test: {test}" for test in cleaned_tests],
        ]
        try:
            outcome = self._close(
                task_id,
                route="resolved-by",
                subject=message or self._default_subject(task_id),
                trailers=trailers,
                paths=list(paths or []),
                explicit_paths=True,
                run_gates=False,
                index_entry={
                    "task_id": task_id,
                    "run_id": None,
                    "run_dir": None,
                    "session_sha256": None,
                    "mode": "resolved-by",
                },
                success_line=f"Closing commit {{commit}} made in resolved-by mode: {reason}",
            )
        except Exception:
            task_path.write_bytes(original)
            raise
        if outcome.exit_code != 0:
            task_path.write_bytes(original)
        return outcome

    def close_retired(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Remove a task that was already resolved before the ritual lifecycle.

        The task keeps its status: it is not made ``superseded`` and no evidence
        gates run. A resolved-family status plus a reason and at least one ref
        that is HEAD or an ancestor commit are the evidence instead, and the
        closing commit says ``Closeout-Mode: legacy-resolved``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Retire needs a non-empty --reason saying why the task is already resolved."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Retire needs at least one --ref naming a commit that is HEAD or an ancestor."],
            )
        unresolved = [
            ref for ref in cleaned_refs if not self._ops.closeout_gates.reference_points_to_commit(ref)
        ]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need a commit that is HEAD or an ancestor)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        payload = doc_access.read_doc(task_path, TaskDoc)
        status = str(payload.get("status") or "").strip().lower()
        if status not in {"resolved", "closed", "done", "complete"}:
            return ClosureOutcome(
                1,
                [
                    f"Task {task_id} has status '{payload.get('status') or ''}'; only resolved, "
                    "closed, done or complete tasks can be retired."
                ],
            )

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: legacy-resolved",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        return self._close(
            task_id,
            route="legacy-resolved",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=True,
            run_gates=False,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "legacy-resolved",
            },
            success_line=f"Closing commit {{commit}} made in legacy-resolved mode: {reason}",
        )

    def _ref_resolves(self, reference: str) -> bool:
        if self._ops.closeout_gates.reference_points_to_commit(reference):
            return True
        path = Path(reference)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def close_with_run(
        self,
        task_id: str,
        *,
        run_dir: str | Path,
        paths: list[str] | None = None,
        run_id: str | None = None,
        session: str | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        root = self.root
        resolved_run_dir = Path(run_dir)
        if not resolved_run_dir.is_absolute():
            resolved_run_dir = (root / resolved_run_dir).resolve()

        if not self._is_under(resolved_run_dir, root / "runs" / "subagents"):
            return ClosureOutcome(1, [f"Run dir must live under runs/subagents/: {resolved_run_dir}"])
        if not resolved_run_dir.is_dir():
            return ClosureOutcome(1, [f"Run dir not found: {resolved_run_dir}"])

        missing = [name for name in self.REQUIRED_EVIDENCE if not (resolved_run_dir / name).exists()]
        if missing:
            return ClosureOutcome(
                1,
                [f"Missing required evidence in {resolved_run_dir}: {', '.join(missing)}"],
            )

        manifest_path = resolved_run_dir / "run.yaml"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

        run_id = run_id or manifest.get("run_id")
        session = session or manifest.get("session")
        session_sha256 = manifest.get("session_sha256")
        session_path = Path(str(session)) if session else None
        if session_path and session_path.is_file():
            session_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()

        rel_run_dir = resolved_run_dir.relative_to(root).as_posix()
        manifest.update(
            {
                "task_id": task_id,
                "run_dir": rel_run_dir,
                "run_id": run_id,
                "session": session,
                "session_sha256": session_sha256,
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")

        staged_paths = list(paths) if paths is not None else list(manifest.get("touched") or [])
        trailers = [f"Task-Id: {task_id}", f"Run-Dir: {rel_run_dir}"]
        if run_id:
            trailers.append(f"Run-Id: {run_id}")
        if session_sha256:
            trailers.append(f"Session-Sha256: {session_sha256}")

        return self._close(
            task_id,
            route="run",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=staged_paths,
            explicit_paths=True,
            extra_stage_paths=[rel_run_dir],
            index_entry={
                "task_id": task_id,
                "run_id": run_id,
                "run_dir": rel_run_dir,
                "session_sha256": session_sha256,
            },
            success_line=f"Closing commit {{commit}} linked to run {rel_run_dir}",
        )

    def close_auto(self, payload: dict[str, Any], task_path: Path) -> None:
        """Legacy hook: close a task from its payload, committing only its own files."""
        task_id = payload.get("id", "unknown-task")
        files = [str(item) for item in payload.get("files") or []]
        try:
            self._close(
                task_id,
                route="legacy",
                subject=self._default_subject(task_id, task_path),
                trailers=[f"Task-Id: {task_id}"],
                paths=files,
                explicit_paths=True,
                task_path=task_path,
                run_gates=False,
                index_entry={},
                success_line="",
            )
        except ClosureCommitError as exc:
            raise RuntimeError(
                f"Failed to commit task closure for {task_id}. The bundle was not deleted "
                f"and the desk was left unchanged. Git output: {exc}"
            ) from exc

    # ---------------------------------------------------------------- internals
    def _close(
        self,
        task_id: str,
        *,
        route: str,
        subject: str,
        trailers: list[str],
        paths: list[str],
        explicit_paths: bool,
        index_entry: dict[str, Any],
        success_line: str,
        task_path: Path | None = None,
        extra_stage_paths: list[str] | None = None,
        run_gates: bool = True,
    ) -> ClosureOutcome:
        self._gate_notes = []
        task_path = task_path or self._task_path(task_id)
        task_rel = self._relative(task_path)
        board_path = self.desk_root / "tasks" / "Board.md"
        board_before = board_path.read_text(encoding="utf-8") if board_path.exists() else None
        routed = self._board_routes(board_path, task_id, task_path) if board_before is not None else False

        if run_gates and task_path.exists() and routed:
            gate_outcome = self._gate_outcome(task_id)
            if gate_outcome is not None:
                return gate_outcome

        staged_before = self._git("diff", "--cached", "--name-only", check=False)
        if explicit_paths:
            for path in paths:
                self._git("add", "-A", "--", path, check=False)
            for path in extra_stage_paths or []:
                self._git("add", "-A", "--", path, check=False)
        elif not staged_before:
            if route == "manual":
                return ClosureOutcome(1, ["Nothing staged and no paths given. Pass --paths."])
            return ClosureOutcome(
                1,
                ["Nothing staged and no paths given. Pass --paths or record 'touched' in run.yaml."],
            )

        commit_paths: list[str] = []
        if explicit_paths:
            commit_paths.extend(paths)
            commit_paths.extend(extra_stage_paths or [])

        def add_commit_path(path: str) -> None:
            if path not in commit_paths:
                commit_paths.append(path)

        task_bytes = task_path.read_bytes() if task_path.exists() else None
        paths_to_remove: list[Path] = []

        try:
            if task_bytes is not None:
                # A task created and closed between two commits never reached HEAD.
                # Record its body first so the closing commit does not erase it.
                self._record_uncommitted_task(task_id, task_path, task_rel)

            with doc_access.desk_transaction(self.root):
                if routed and board_before is not None:
                    board_payload = doc_access.read_doc(board_path, BoardDoc)
                    references = [
                        str(item)
                        for item in board_payload.get("tasks") or []
                        if not self._board_reference_matches(str(item), task_id, task_rel)
                    ]
                    board_payload["tasks"] = references
                    doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)
                    self._git("add", "--", "desk/tasks/Board.md", check=False)
                    add_commit_path("desk/tasks/Board.md")

                if task_bytes is not None:
                    doc_access.untrack_doc(self.root, task_path)

                sldb_status = self._git("status", "--porcelain", "--", ".sldb", check=False)
                if sldb_status:
                    self._git("add", "-A", "--", ".sldb", check=False)
                    add_commit_path(".sldb")

                if task_bytes is not None:
                    # Committed means present in HEAD, not merely staged: a directory in
                    # --paths can stage a task created in this cycle, and HEAD never had it.
                    in_head = self._in_head(task_rel)
                    if not in_head:
                        self._git("rm", "--cached", "-q", "--ignore-unmatch", "--", task_rel, check=False)
                    if in_head:
                        removed = subprocess.run(
                            ["git", "rm", "-f", "--", task_rel],
                            cwd=self.root,
                            capture_output=True,
                            text=True,
                        )
                        if removed.returncode != 0:
                            raise ClosureCommitError(
                                removed.stderr.strip() or removed.stdout.strip() or f"git rm failed for {task_rel}"
                            )
                        add_commit_path(task_rel)
                    else:
                        paths_to_remove.append(task_path)

                message = subject + "\n\n" + "\n".join(trailers) + "\n"

                head_task_id = self._git(
                    "log", "-1", "--format=%(trailers:key=Task-Id,valueonly)", check=False
                )
                head_mode = self._git(
                    "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)", check=False
                )
                pathspec = list(dict.fromkeys(commit_paths)) if explicit_paths else None
                if pathspec:
                    # A path git knows neither in the index nor in HEAD (a directory whose
                    # only file was the never-committed task) would fail the whole commit.
                    pathspec = [path for path in pathspec if self._git_knows(path)]
                    if not pathspec:
                        raise ClosureCommitError("None of the --paths match a file git knows; nothing to commit.")
                if head_task_id == task_id and head_mode != "record":
                    argv = ["commit", "--amend", "--no-edit"]
                else:
                    argv = ["commit", "-m", message]
                if pathspec:
                    argv.extend(["--", *pathspec])

                result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
                if result.returncode != 0:
                    raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

            # The commit exists; only now remove an untracked bundle from disk.
            for path in paths_to_remove:
                if path.exists():
                    path.unlink()
        except Exception:
            self._restore_index(commit_paths, task_rel)
            if task_bytes is not None:
                task_path.parent.mkdir(parents=True, exist_ok=True)
                task_path.write_bytes(task_bytes)
            if board_before is not None:
                board_path.write_text(board_before, encoding="utf-8")
            raise

        commit = self._git("rev-parse", "HEAD")
        messages: list[str] = []
        if index_entry:
            index_path = self.root / "runs" / "subagents" / "index.jsonl"
            index_rel = index_path.relative_to(self.root).as_posix()
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_before = index_path.read_bytes() if index_path.exists() else None
            entry = {**index_entry, "commit": None}
            with index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            try:
                # A project that ignores the run index keeps it local: the entry is written,
                # but neither staged nor folded into the closing commit (the trailer is enough).
                if not self._git_ignores(index_rel):
                    self._git("add", "--", index_rel)
                    self._git("commit", "--amend", "--no-edit", "--", index_rel)
            except Exception:
                if index_before is None:
                    index_path.unlink(missing_ok=True)
                else:
                    index_path.write_bytes(index_before)
                self._git("restore", "--staged", "--", index_rel, check=False)
                raise
            commit = self._git("rev-parse", "HEAD")
            messages.append(f"Index: {index_path}")
        messages = [*self._gate_notes, *messages] if run_gates else messages
        if success_line:
            messages.insert(0, success_line.format(commit=commit[:12]))
        return ClosureOutcome(0, messages)

    def _gate_outcome(self, task_id: str) -> ClosureOutcome | None:
        """Evaluate the task type's closeout rule (``rule-closeout-<type>``, CC33b) on the
        evidence receipts ``deskops closeout verify`` wrote; this path writes none (b2).

        The rule runs as it does on the ``task_completes`` edge: ``on_transition`` with the task
        read at ``ritual-closeout``. An error finding blocks the commit and is printed with the
        rule, clause and values seen; verify runs read-only first so its declared/found line and
        alerts are always reported.
        """
        self._gate_notes = []
        blocked = f"Closeout gate blocked {task_id}; the closing commit was not made."
        try:
            report = self.verify_task_closeout(task_id)
        except Exception as exc:  # noqa: BLE001 - a gate that cannot run blocks closure
            return ClosureOutcome(1, [blocked, f"- {exc}"])
        notes = [f"Closeout gate: {report.get('summary', '')}"]
        for alert in report.get("alerts") or []:
            notes.append(f"ALERTA {alert.get('code', 'alert')}: {alert.get('message', '')}")
        self._gate_notes = notes
        try:
            findings = self.closeout_rule_findings(task_id)
        except Exception as exc:  # noqa: BLE001 - a rule that cannot run blocks closure
            return ClosureOutcome(1, [blocked, *notes, f"- {exc}"])
        errors = [finding for finding in findings if finding.get("level") == "error"]
        if not errors:
            return None
        return ClosureOutcome(
            1,
            [
                blocked,
                *notes,
                *(f"- {lifecycle.finding_line(finding)}" for finding in errors),
                f"Run 'deskops closeout verify --task {task_id}' to write the evidence receipts the rule asks for, then commit again.",
            ],
        )

    def closeout_rule_findings(self, task_id: str) -> list[dict[str, Any]]:
        """The findings of the task's ``on_transition`` rules read at ``ritual-closeout``: its
        type's closeout rule and any rule the desk adds there. A task the store does not track
        cannot be evaluated and raises."""
        task_path = self._task_path(task_id)
        document = lifecycle.task_document(self.root, task_path)
        if document is None:
            raise RuntimeError(
                f"{self._relative(task_path)} is not tracked in the desk's store, so its closeout rule cannot run; "
                "track it with 'deskops desk update --apply'."
            )
        payload = dict(doc_access.resolve_task_payload(self.root, task_path.stem))
        payload["current_node"] = CLOSEOUT_NODE
        return lifecycle.transition_findings(self.root, document, payload)

    # ---------------------------------------------------------------- closeout verify
    def verify_task_closeout(self, task_selector: str, *, write_receipts: bool = False) -> dict[str, Any]:
        """Run the closeout fact producers and return the gate envelope.

        With ``write_receipts`` (``deskops closeout verify``), it also writes one pinned
        ``ReviewDoc`` kind ``evidence`` per declared kind the producers verified (CC33a); the
        envelope is the same either way. Read-only callers (the board view, the closing gate)
        leave it off.
        """
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        reference_evidence = self._closeout_reference_evidence(payload)
        changed_files = doc_access.coerce_list(payload.get("files") or [])
        type_kinds, extras, implicit = self._declared_closeout_evidence(payload)

        findings: list[dict[str, str]] = []
        alerts: list[dict[str, str]] = []
        unknown = [kind for kind in extras if kind not in closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY]
        for kind in unknown:
            alerts.append(
                {
                    "code": "unknown_closeout_evidence",
                    "message": f"Declared closeout evidence '{kind}' is not in the vocabulary: "
                    + ", ".join(closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY)
                    + "; it is not verified and does not block closeout.",
                }
            )
        # The type's kinds verify can produce; `goldens` is a review receipt the closeout rule
        # reads directly (`deskops review record --kind goldens`), not a fact verify checks.
        type_facts = [kind for kind in type_kinds if kind in closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY]
        extra_facts = [kind for kind in extras if kind not in unknown]
        declared = closeout_gates_module.order_evidence_kinds([*type_facts, *extra_facts])
        python_changes = [path for path in changed_files if str(path).endswith(".py")]
        if python_changes and "tests" not in declared:
            alerts.append(
                {
                    "code": "python_changes_without_declared_tests",
                    "message": "The task changes Python files ("
                    + ", ".join(python_changes)
                    + ") but did not declare tests as closeout evidence; this does not block closeout.",
                }
            )

        gate_dict: dict[str, Any] = {}
        found: list[str] = []
        ok = True
        link_in_type = "atom" in type_facts or "materialization" in type_facts

        def add_gate(name: str, gate: CloseoutGateReport, found_label: str | None) -> None:
            """A gate of the type's evidence blocks; one the task adds only alerts (DA5, c5)."""
            nonlocal ok
            gate_dict[name] = gate.to_dict()
            if found_label:
                found.append(found_label)
            in_type = link_in_type if name == "atom_or_materialization_link" else name in type_facts
            if in_type:
                findings.extend(gate.findings)
                ok = ok and gate.ok
            elif not gate.ok:
                messages = "; ".join(str(f.get("message") or f.get("code") or "") for f in gate.findings)
                alerts.append(
                    {
                        "code": "added_closeout_evidence_not_verified",
                        "message": f"Closeout evidence '{name}' the task adds to its type was not verified ({messages}); "
                        "this does not block closeout.",
                    }
                )

        if "tests" in declared:
            tests = reference_evidence["tests"]
            add_gate(
                "tests",
                CloseoutGateReport(
                    ok=bool(tests),
                    evidence=tests,
                    findings=[] if tests else [{"code": "missing_tests_evidence", "message": "No resolvable test evidence reference found."}],
                ),
                "tests" if tests else None,
            )
        if "atom" in declared or "materialization" in declared:
            link_gate = self._closeout_link_gate(payload, changed_files, reference_evidence)
            real_links = [item for item in link_gate.evidence if not item.startswith("knowledge-coverage-exempt")]
            label = None
            if link_gate.ok and real_links:
                label = "atom|materialization"
            elif link_gate.ok:
                label = "atom|materialization (exento: sin atoms locales)"
            add_gate("atom_or_materialization_link", link_gate, label)
        if "commit" in declared:
            commits = reference_evidence["commit"]
            add_gate(
                "commit",
                CloseoutGateReport(
                    ok=bool(commits),
                    evidence=commits,
                    findings=[] if commits else [{"code": "missing_commit_evidence", "message": "No resolvable commit reference found."}],
                ),
                "commit" if commits else None,
            )
        if "document" in declared:
            documents = reference_evidence["document"]
            add_gate(
                "document",
                CloseoutGateReport(
                    ok=bool(documents),
                    evidence=documents,
                    findings=[] if documents else [{"code": "missing_document_evidence", "message": "No existing document (a .md/.rst/.txt/.adoc/.yaml file outside tests/ and desk/tasks/) found in references or files."}],
                ),
                "document" if documents else None,
            )
        if "external" in declared:
            urls = reference_evidence["external"]
            add_gate(
                "external",
                CloseoutGateReport(
                    ok=bool(urls),
                    evidence=urls,
                    findings=[] if urls else [{"code": "missing_external_evidence", "message": "No http(s) URL found in references."}],
                ),
                "external" if urls else None,
            )

        report = {
            "task_id": str(payload.get("id") or task_path.stem),
            "ok": ok,
            "declared": declared,
            "found": found,
            "summary": closeout_gates_module.gate_summary(declared, found),
            "implicit_code": implicit,
            "alerts": alerts,
            "gates": gate_dict,
            "findings": findings,
        }
        if write_receipts:
            self._write_evidence_receipts(task_path, report["task_id"], declared, gate_dict)
        return report

    # ---------------------------------------------------------------- evidence receipts
    def _write_evidence_receipts(
        self, task_path: Path, task_id: str, declared: list[str], gates: dict[str, Any]
    ) -> list[str]:
        """One ``ReviewDoc`` kind ``evidence`` per declared kind, pinned on the task's contract.

        A receipt is skipped when one of the same fact for the task already carries the same
        ``input_sha256`` and an intact anchor (c2). Written by ``create`` plus an unchanged
        ``update`` in the same transaction, the save that pins ``subject`` (c1). A root without
        a store has no anchors to pin and gets no receipts. Returns the review ids written.
        """
        if not doc_access.has_store(self.root):
            return []
        facts = self._evidence_facts(declared, gates)
        if not facts:
            return []
        review_dir = self.desk_root / "reviews" / task_id
        subject = f"doc:{self._task_model(task_path)}:{task_id}"
        actor = self._closeout_identity()
        now = datetime.now(timezone.utc).isoformat()
        not_intact: set[str] | None = None
        pending: list[tuple[str, Path, dict[str, Any]]] = []
        for fact, verdict, items, reason in facts:
            value = "\n".join(items)
            input_sha256 = self._evidence_input_sha256(fact, items)
            same_input = [
                review_id
                for review_id, payload in self._evidence_receipts(review_dir, fact)
                if payload.get("input_sha256") == input_sha256
            ]
            if same_input:
                if not_intact is None:
                    not_intact = self._not_intact_documents()
                if any(review_id not in not_intact for review_id in same_input):
                    continue
            n = len(list(review_dir.glob(f"evidence-{fact}-*.md"))) + 1 if review_dir.exists() else 1
            review_id = f"review-{task_id}-evidence-{fact}-{n}"
            pending.append(
                (
                    review_id,
                    review_dir / f"evidence-{fact}-{n}.md",
                    {
                        "id": review_id,
                        "title": f"Closeout evidence {fact} of {task_id}",
                        "kind": "evidence",
                        "fact": fact,
                        "value": value,
                        "subject": subject,
                        "subject_ref": "",
                        "engine": EVIDENCE_ENGINE,
                        "actor": actor,
                        "run_dir": "",
                        "input_sha256": input_sha256,
                        "output_sha256": "",
                        "verdict": verdict,
                        "reason": reason,
                        "created_at": now,
                        "disposed_at": now,
                        "disposed_by": actor,
                        "summary": f"closeout verify checked {fact}: " + (", ".join(items) if items else "(nothing found)"),
                        "disposition": f"Verdict {verdict}: {reason}",
                        "tags": ["workspace:desk"],
                    },
                )
            )
        if not pending:
            return []
        review_dir.mkdir(parents=True, exist_ok=True)
        with doc_access.desk_transaction(self.root) as tx:
            for review_id, path, payload in pending:
                tx.create("ReviewDoc", review_id, payload, doc_access.relative_path(self.root, path))
                # The unchanged second save pins `subject` with the task's contract hash (GO07).
                tx.update(review_id, payload)
        return [review_id for review_id, _, _ in pending]

    def _evidence_facts(
        self, declared: list[str], gates: dict[str, Any]
    ) -> list[tuple[str, str, list[str], str]]:
        """``(fact, verdict, value items, reason)`` per declared kind, from the gates verify ran.

        Accepted when the kind's producer found evidence, rejected with the gate's finding
        message otherwise (b1, r7). ``value`` items are sorted, paths POSIX relative to the
        root (r2). The link gate gives an ``atom`` receipt for atom links and a
        ``materialization`` receipt for materialization links (r4).
        """
        facts: list[tuple[str, str, list[str], str]] = []

        def add(fact: str, ok: bool, items: list[str], findings: list[dict[str, str]]) -> None:
            items = sorted(set(items))
            if ok and items:
                facts.append((fact, "accepted", items, f"verified: {fact} " + "\n".join(items)))
                return
            messages = [str(item.get("message") or item.get("code") or "") for item in findings]
            facts.append((fact, "rejected", items, "; ".join(m for m in messages if m) or f"no {fact} evidence found"))

        for fact in ("tests", "commit", "document", "external"):
            gate = gates.get(fact)
            if fact not in declared or gate is None:
                continue
            evidence = [str(item) for item in gate.get("evidence") or []]
            if fact == "commit":
                items = [sha for sha in (self._ops.closeout_gates.full_commit_sha(ref) for ref in evidence) if sha]
            elif fact == "external":
                items = [item.strip() for item in evidence]
            else:
                items = [self._normalized_reference(item) for item in evidence]
            add(fact, bool(gate.get("ok")), items, gate.get("findings") or [])

        link = gates.get("atom_or_materialization_link")
        if link is not None:
            atoms, materializations = self._link_documents([str(item) for item in link.get("evidence") or []])
            ok = bool(link.get("ok"))
            findings = link.get("findings") or []
            if ok:
                for fact, ids in (("atom", atoms), ("materialization", materializations)):
                    if ids and fact in declared:
                        add(fact, True, ids, findings)
                if not atoms and not materializations and ("atom" in declared or "materialization" in declared):
                    # Exempt or follow-up-only coverage names no linking document: the gate
                    # passed, so an accepted atom receipt records why (b3) and the rule's
                    # atom|materialization clause needs no special case.
                    reasons = [str(item) for item in link.get("evidence") or []] or ["no changed file needs a link"]
                    add("atom", True, ["exempt: " + "; ".join(reasons)], findings)
            else:
                rejected = [fact for fact, ids in (("atom", atoms), ("materialization", materializations)) if ids]
                rejected = [fact for fact in rejected if fact in declared] or [
                    next(fact for fact in ("atom", "materialization") if fact in declared)
                ]
                for fact in rejected:
                    add(fact, False, atoms if fact == "atom" else materializations, findings)
        order = list(closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY)
        return sorted(facts, key=lambda item: order.index(item[0]))

    def _link_documents(self, evidence: list[str]) -> tuple[list[str], list[str]]:
        """The ids of the atoms and materializations a link-gate evidence list names."""
        atoms: list[str] = []
        materializations: list[str] = []
        for item in evidence:
            if item.startswith("graph:") and "->atom:" in item:
                atoms.append(item.rsplit("->atom:", 1)[1])
            elif item.startswith("atom-doc:"):
                atoms.append(Path(item.removeprefix("atom-doc:")).stem)
            elif item.startswith("materialization:") and "->" in item:
                materializations.append(item.removeprefix("materialization:").split("->", 1)[0].removeprefix("materialization:"))
            elif reference_points_to_atom(self.root, item):
                candidate = item.split("::", 1)[0].strip()
                atoms.append(Path(candidate).stem if candidate.endswith(".md") else candidate.removeprefix("atom:"))
        return atoms, materializations

    def _normalized_reference(self, reference: str) -> str:
        """A reference with its path POSIX-relative to the root, keeping a ``::node`` suffix."""
        text = reference.strip()
        if text.startswith("pytest "):
            return text
        path_text, sep, node = text.partition("::")
        relative = self._normalize_repo_relative_path(path_text)
        return (relative + sep + node) if relative else text

    def _evidence_input_sha256(self, fact: str, items: list[str]) -> str:
        """sha256 of ``fact\nvalue\n`` and, per file of value in order, ``path\nsha256\n`` (r3)."""
        data = f"{fact}\n" + "\n".join(items) + "\n"
        if fact != "commit" and fact != "external":
            for item in items:
                path_text = item.split("::", 1)[0]
                path = self.root / path_text
                if fact in {"atom", "materialization"} or not path_text or not path.is_file():
                    continue
                data += f"{path_text}\n{hashlib.sha256(path.read_bytes()).hexdigest()}\n"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def _evidence_receipts(self, review_dir: Path, fact: str) -> list[tuple[str, dict[str, Any]]]:
        if not review_dir.is_dir():
            return []
        from deskops.models.review import ReviewDoc

        receipts: list[tuple[str, dict[str, Any]]] = []
        for path in sorted(review_dir.glob(f"evidence-{fact}-*.md")):
            try:
                payload = doc_access.read_doc(path, ReviewDoc)
            except Exception:  # noqa: BLE001 - an unreadable receipt is never a match
                continue
            if payload.get("kind") == "evidence" and payload.get("fact") == fact:
                receipts.append((str(payload.get("id") or path.stem), payload))
        return receipts

    def _not_intact_documents(self) -> set[str]:
        """Ids of the store documents with an anchor that is not intact (r5: check_doc_anchors)."""
        from sldb.api.anchors.check_doc_anchors import check_doc_anchors

        from deskops.paths import package_pythonpath

        findings = check_doc_anchors(doc_access.store_path(self.root), pythonpath=package_pythonpath())
        return {str(finding.subject).rsplit(":", 1)[-1] for finding in findings}

    def _task_model(self, task_path: Path) -> str:
        """The typed model the store tracks the task under (``TaskCodeDoc``, ...), as review does."""
        from sldb.api.stores.doc_status import doc_status

        try:
            status = doc_status(doc_access.store_path(self.root), self._relative(task_path))
        except Exception:  # noqa: BLE001 - an untracked task anchors on the base model
            return "TaskDoc"
        return (status.model or "TaskDoc") if status.exists else "TaskDoc"

    def _closeout_identity(self) -> str:
        from deskops.config import DeskConfig

        identity = (DeskConfig.load(self.desk_root).project_identity or "").strip()
        return identity if identity and identity != "unknown-project" else self.root.name

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The closeout graph context, shared by every task read inside a read snapshot."""
        snapshot = self._ops.snapshot
        if snapshot is None:
            return self._ops.closeout_gates.build_closeout_graph_context()
        if snapshot.graph_context is None:
            snapshot.graph_context = self._ops.closeout_gates.build_closeout_graph_context()
        return snapshot.graph_context

    def _declared_closeout_evidence(self, payload: dict[str, Any]) -> tuple[list[str], list[str], bool]:
        """``(type kinds, kinds the task adds, implicit)`` of the evidence the task closes with.

        The type's kinds come from ``deskops/data/rules/closeout-evidence.yaml`` through the
        task's registered model (a desk subtype reads its nearest factory ancestor's); the
        task's own ``closeout_evidence`` only adds kinds, never removes one (DA5). A task whose
        type resolves to no factory type is gated as code; ``implicit`` says it has no
        ``task_type`` (a task that predates types, which the ``rule-closeout-alert-implicit-code``
        rule names when it is written).
        """
        declared = declared_evidence_list(payload.get("closeout_evidence"))
        task_type = str(payload.get("task_type") or "").strip()
        registry = self._ops.registered_task_types()
        type_model = registry.get(task_type) or registry.get(canonical_task_type_name(task_type))
        kinds = closeout_evidence_kinds(type_model) if type_model is not None else None
        type_kinds = list(kinds if kinds is not None else closeout_gates_module.CODE_EVIDENCE)
        extras = [kind for kind in dict.fromkeys(declared) if kind not in type_kinds]
        return type_kinds, extras, not task_type

    def _closeout_reference_evidence(self, payload: dict[str, Any]) -> dict[str, list[str]]:
        return self._ops.closeout_gates.closeout_reference_evidence(
            payload,
            points_to_atom=lambda reference: reference_points_to_atom(self.root, reference),
            points_to_routed_follow_up=self._reference_points_to_routed_follow_up,
        )

    def _closeout_link_gate(
        self,
        payload: dict[str, Any],
        changed_files: list[str],
        reference_evidence: dict[str, list[str]],
    ) -> CloseoutGateReport:
        evidence = list(reference_evidence["atom"])
        findings: list[dict[str, str]] = []
        has_local_atoms = any(
            path.is_file()
            for path in (self.desk_root / "atoms").rglob(doc_access.artifact_glob_pattern("artifact.atom"))
        )
        if not has_local_atoms:
            evidence.append("knowledge-coverage-exempt: no local atom documents")
        graph_context = self.build_closeout_graph_context()

        for raw_path in changed_files:
            relative_path = self._normalize_repo_relative_path(raw_path)
            if relative_path is None:
                findings.append(
                    {
                        "code": "changed_file_missing",
                        "path": str(raw_path),
                        "message": "Changed file path does not resolve inside the repository.",
                    }
                )
                continue

            source_finding = self._generated_artifact_source_finding(relative_path)
            if source_finding is not None:
                findings.append(source_finding)

            file_evidence = self._changed_file_link_evidence(relative_path, graph_context)
            file_evidence.extend(self._skill_guard_test_evidence(relative_path, graph_context))
            if file_evidence:
                evidence.extend(file_evidence)
                continue

            if reference_evidence["follow_up"]:
                for follow_up in reference_evidence["follow_up"]:
                    evidence.append(f"follow-up:{follow_up} -> {relative_path}")
                continue

            if not has_local_atoms:
                continue

            findings.append(
                {
                    "code": "missing_changed_file_link",
                    "path": relative_path,
                    "message": "Changed file has no atom/materialization link and no routed follow-up reference.",
                }
            )

        if has_local_atoms and not changed_files and not reference_evidence["atom"]:
            findings.append(
                {
                    "code": "missing_atom_or_materialization_link",
                    "message": "No atom reference or changed-file materialization coverage found.",
                }
            )

        return CloseoutGateReport(ok=not findings, evidence=self._dedupe_preserve_order(evidence), findings=findings)

    def _reference_points_to_routed_follow_up(self, reference: str) -> bool:
        candidate = reference.strip()
        if not candidate:
            return False
        if candidate.startswith(("task:", "issue:")):
            return self._reference_points_to_existing_route(candidate)
        if candidate.endswith(".md"):
            path = Path(candidate.split("::", 1)[0])
            if not path.is_absolute():
                path = self.root / path
            return path.exists() and any(
                self._resolved_is_under(path, self.root / relative)
                for relative in ("desk/tasks", "desk/drawer/issues", "desk/drawer/tasks")
            )
        return False

    def _reference_points_to_existing_route(self, reference: str) -> bool:
        kind, _, identifier = reference.partition(":")
        if not identifier:
            return False
        if kind == "task":
            return any(path.stem == identifier for path in (self.desk_root / "tasks").glob("task-*.md"))
        if kind == "issue":
            return any(path.stem == identifier for path in (self.desk_root / "drawer" / "issues").rglob("issue-*.md"))
        return False

    def _changed_file_link_evidence(self, relative_path: str, graph_context: "CloseoutGraph") -> list[str]:
        evidence: list[str] = []
        path = self.root / relative_path
        if path.suffix == ".md" and self._resolved_is_under(path, self.desk_root / "atoms"):
            evidence.append(f"atom-doc:{relative_path}")
        node_id = graph_context.node_id(relative_path)
        if node_id is None:
            return evidence
        for edge in graph_context.edges_around(node_id):
            if edge.source_id == node_id and edge.target_id.startswith("atom:"):
                evidence.append(f"graph:{node_id}->{edge.target_id}")
            if edge.target_id == node_id and edge.source_id.startswith("materialization:"):
                if edge.source_id in graph_context.invalid_materializations:
                    continue
                evidence.append(f"materialization:{edge.source_id}->{relative_path}")
        return self._dedupe_preserve_order(evidence)

    def _skill_guard_test_evidence(self, relative_path: str, graph_context: "CloseoutGraph") -> list[str]:
        """Evidence for a changed skill file covered by an atom-linked guard test.

        Skill Markdown files are not graph nodes. A changed skill file is linked
        only when a test that reads its skill tree (and names ``SKILL.md``) is
        itself linked to an atom or to a valid materialization.
        """
        matching_prefix = next(
            (prefix for prefix in SKILL_TREE_PREFIXES if relative_path.startswith(prefix)),
            None,
        )
        if matching_prefix is None:
            return []

        tree_token = matching_prefix.rstrip("/")
        evidence: list[str] = []
        for test_path in self._atom_linked_test_paths(graph_context):
            if not test_path.startswith("tests/"):
                continue
            path = self.root / test_path
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if "SKILL.md" not in text:
                continue
            if tree_token not in text and relative_path not in text:
                continue
            evidence.append(f"guard-test:{test_path} -> {relative_path}")
        return self._dedupe_preserve_order(evidence)

    @staticmethod
    def _atom_linked_test_paths(graph_context: "CloseoutGraph") -> list[str]:
        test_node_ids: set[str] = set()
        for edge in graph_context.test_link_edges():
            if edge.source_id.startswith("test_file:") and edge.target_id.startswith("atom:"):
                test_node_ids.add(edge.source_id)
            if edge.target_id.startswith("test_file:") and edge.source_id.startswith("materialization:"):
                if edge.source_id in graph_context.invalid_materializations:
                    continue
                test_node_ids.add(edge.target_id)
        return sorted(node_id.removeprefix("test_file:") for node_id in test_node_ids)

    def _generated_artifact_source_finding(self, relative_path: str) -> dict[str, str] | None:
        path = self.root / relative_path
        sibling = self._find_generated_artifact_source_sibling(path)
        if sibling is None or not path.exists() or path.suffix not in {".md", ".json"}:
            return None
        if self._declares_materialization_sources(path):
            return None
        return {
            "code": "generated_artifact_missing_declared_sources",
            "path": relative_path,
            "message": f"Rendered artifact has sibling source {sibling.name} but does not declare source_atoms or provenance.",
        }

    @staticmethod
    def _find_generated_artifact_source_sibling(path: Path) -> Path | None:
        for suffix in (".mmd", ".yaml", ".yml"):
            sibling = path.with_suffix(suffix)
            if sibling != path and sibling.exists():
                return sibling
        return None

    @staticmethod
    def _declares_materialization_sources(path: Path) -> bool:
        if path.suffix not in {".md", ".yaml", ".yml", ".json"}:
            return False
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return False
        if path.suffix == ".json":
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                return False
            if not isinstance(loaded, dict):
                return False
            return bool(loaded.get("source_atoms") or loaded.get("provenance"))
        if not text.startswith("---\n"):
            return False
        try:
            _, rest = text.split("---\n", 1)
            block, _body = rest.split("\n---", 1)
        except ValueError:
            return False
        loaded = yaml.safe_load(block) or {}
        if not isinstance(loaded, dict):
            return False
        return bool(loaded.get("source_atoms") or loaded.get("provenance"))

    def _normalize_repo_relative_path(self, raw_path: str) -> str | None:
        candidate = Path(str(raw_path).split("::", 1)[0].strip())
        if not candidate:
            return None
        if not candidate.is_absolute():
            candidate = (self.root / candidate).resolve()
        else:
            candidate = candidate.resolve()
        try:
            return candidate.relative_to(self.root).as_posix()
        except ValueError:
            return None

    @staticmethod
    def _dedupe_preserve_order(values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    @staticmethod
    def _resolved_is_under(path: Path, parent: Path) -> bool:
        try:
            path.resolve().relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _task_path(self, task_id: str) -> Path:
        try:
            return doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return self.desk_root / "tasks" / f"{task_id}.md"

    def _default_subject(self, task_id: str, task_path: Path | None = None) -> str:
        """Name the task file, so ``git log`` says what closed, not just its id."""
        path = task_path or self._task_path(task_id)
        return f"closeout: {path.stem}"

    def _board_routes(self, board_path: Path, task_id: str, task_path: Path) -> bool:
        try:
            payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return False
        task_rel = self._relative(task_path)
        return any(
            self._board_reference_matches(str(item), task_id, task_rel)
            for item in payload.get("tasks") or []
        )

    @staticmethod
    def _board_reference_matches(reference: str, task_id: str, task_rel: str) -> bool:
        return reference in {
            task_rel,
            f"desk/tasks/{task_id}",
            f"desk/tasks/{task_id}.md",
        }

    def _restore_index(self, commit_paths: list[str], task_rel: str) -> None:
        for path in dict.fromkeys([*commit_paths, task_rel]):
            self._git("restore", "--staged", "--", path, check=False)

    def _relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    @staticmethod
    def _is_under(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _in_head(self, path: str) -> bool:
        """Whether `path` is already committed in HEAD."""
        return subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{path}"],
            cwd=self.root,
            capture_output=True,
        ).returncode == 0

    def _record_uncommitted_task(self, task_id: str, task_path: Path, task_rel: str) -> None:
        """Commit the body of a task HEAD never saw, before the closing commit removes it.

        The record commit carries ``Closeout-Mode: record`` so the closing commit does
        not fold itself into it through the same-Task-Id amend.
        """
        if self._in_head(task_rel):
            return
        message = f"desk: registra {task_path.stem}\n\nTask-Id: {task_id}\nCloseout-Mode: record\n"
        added = subprocess.run(
            ["git", "add", "--", task_rel], cwd=self.root, capture_output=True, text=True
        )
        if added.returncode != 0:
            raise ClosureCommitError(added.stderr.strip() or added.stdout.strip() or f"git add failed for {task_rel}")
        result = subprocess.run(
            ["git", "commit", "-m", message, "--", task_rel],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

    def _git_ignores(self, path: str) -> bool:
        """Whether `path` is excluded by the project's ignore rules (a tracked file never is)."""
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=self.root,
                                capture_output=True, text=True)
        return result.returncode == 0

    def _git_knows(self, path: str) -> bool:
        """Whether `path` matches anything in the index or in HEAD."""
        for argv in (["ls-files", "--", path], ["ls-tree", "-r", "--name-only", "HEAD", "--", path]):
            listed = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
            if listed.returncode == 0 and listed.stdout.strip():
                return True
        return False

    def _git(self, *argv: str, check: bool = True) -> str:
        result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise ClosureCommitError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result.stdout.strip()
