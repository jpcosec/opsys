from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from deskops.cli.parse_input import parse_artifact_input
from deskops.cli.parse_input import parse_task_input
from deskops.cli.render import normalize
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS


class OperationsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        operations = DeskopsOperations(root)

        if args.command == "add" and args.subject == "task":
            payload = parse_task_input(args)
            drawer_selector = getattr(args, "from_drawer", None)
            if not drawer_selector:
                raw_drawer = payload.get("from_drawer")
                drawer_selector = str(raw_drawer) if raw_drawer else None
            drawer_source = None
            if drawer_selector:
                try:
                    drawer_source = operations.resolve_drawer_source(drawer_selector)
                except (FileNotFoundError, ValueError) as exc:
                    print(f"Error: {exc}")
                    return 1
                payload = operations.attach_drawer_source(payload, drawer_source)
            bundle = operations.create_task_bundle(payload)
            print(f"Created task bundle {bundle.task_id}")
            print(f"Task: {bundle.task_path}")
            if drawer_source is not None:
                print(f"From drawer: {drawer_source} (kept; remove it by hand once the task supersedes it)")
            return 0

        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "add" and args.subject in artifact_subjects:
            artifact_id = artifact_subjects[args.subject]
            payload = parse_artifact_input(artifact_id, args)
            record = operations.create_artifact(artifact_id, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            if args.subject == "repository":
                print("Note: this is a local repository artifact. Use 'deskops repo register' for canonical ecosystem registration.")
            return 0

        if args.command == "edit":
            try:
                record = operations.edit_artifact_field(args.subject, args.selector, args.field, args.value)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Updated {record.kind} {record.doc_id} field {args.field.replace('-', '_')}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "bind" and args.subject == "pill":
            try:
                record, pill_id, changed = operations.bind_pill_to_task(args.task, args.pill)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Bound" if changed else "Already bound"
            print(f"{verb} pill {pill_id} to task {record.doc_id}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "next":
            try:
                if getattr(args, "diagram", False):
                    print(operations.render_next_action_diagram())
                    return 0
                report = operations.next_action_report(getattr(args, "task_id", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            self._print_next_action_report(report)
            return 0

        if args.command == "list" and args.subject == "tasks":
            tasks = operations.list_tasks()
            repo_routes = operations.list_repo_task_routes() if getattr(args, "include_repos", False) else []
            payload: dict[str, Any] = {"tasks": tasks}
            if getattr(args, "include_repos", False):
                payload["repo_routes"] = repo_routes
            return render(payload, args.format, lambda _data: self._format_task_list(tasks, repo_routes))

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject == "atoms":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads, axis=axis),
            )
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            payloads = operations.list_artifacts(artifact_id)
            return render(
                {args.subject: payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads),
            )

        if args.command == "show" and args.subject == "task":
            task, gates = operations.show_task(args.task_id)
            if task is None:
                return render_error(
                    f"No task found for {args.task_id}",
                    args.format,
                    type_name="DomainError",
                )
            payload = normalize(task)
            payload["lifecycle_gates"] = normalize(gates)
            return render(payload, args.format, lambda _data: self._format_task_detail(task, gates))

        show_artifacts = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "show" and args.subject in show_artifacts:
            artifact_id = show_artifacts[args.subject]
            try:
                payload = operations.show_artifact(artifact_id, args.doc_id)
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                payload,
                args.format,
                lambda _data: self._format_artifact_detail(args.subject, payload),
            )

        if args.command == "advance" and args.subject == "task":
            from deskops.lifecycle import LifecycleGraphMissing

            try:
                task, result = operations.advance_task(args.task_id, target_node=getattr(args, "to", None))
            except LifecycleGraphMissing as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            if task is None:
                print(f"No task found for {args.task_id}", file=sys.stderr)
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Message: {result.message}")
            return 1 if result.blocked else 0

        return 1

    def _print_next_action_report(self, report: dict[str, Any]) -> None:
        kind = report.get("kind")
        if kind == "no_board_task":
            print("Next:")
            print(f"No active task is routed by {report['board']}.")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        if kind == "multiple_board_tasks":
            print("Next:")
            print(f"Multiple active tasks are routed by {report['board']}; pass a task selector.")
            print("Routed tasks:")
            for task in report["tasks"]:
                print(f"- {task['id']} | {task['status']} | {task['title']}")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        print(f"Task: {report['task']['id']}")
        print(f"Title: {report['task']['title']}")
        print(f"Status: {report['task']['status']}")
        print(f"Current node: {report['task']['current_node']}")
        if report['task'].get('task_type'):
            print(f"Task type: {report['task']['task_type']}")
        if report['task'].get('inherits_from'):
            print("Inherits from:")
            for item in report['task']['inherits_from']:
                print(f"- {item}")
        print(f"Phase: {report['phase']}")
        if report.get("ritual"):
            print("Required ritual:")
            print(f"- {report['ritual']}")
        if report.get("pills"):
            print("Required pills:")
            for pill in report["pills"]:
                print(f"- {pill}")
        print("Next actions:")
        for index, action in enumerate(report["next_actions"], start=1):
            print(f"{index}. {action}")
        if report.get("advance_when"):
            print("Advance when:")
            for item in report["advance_when"]:
                print(f"- {item}")
        print("Sources:")
        for label, path in report["sources"].items():
            print(f"- {label}: {path}")

    @staticmethod
    def _format_task_list(tasks: Any, repo_routes: Any) -> str:
        lines = [f"{task.id} | {task.status} | {task.current_node}" for task in tasks]
        lines.extend(
            f"{route.repo_id}:{route.task_id} | {route.status} | {route.title} | {route.task_path}"
            for route in repo_routes
        )
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_list(payloads: list[dict[str, Any]], *, axis: str | None = None) -> str:
        lines: list[str] = []
        for payload in payloads:
            label = payload.get("title") or payload.get("name") or payload["id"]
            if axis:
                values = ",".join(payload.get("axis_values") or []) or "-"
                lines.append(f"{payload['id']} | {label} | {axis}:{values}")
            else:
                lines.append(f"{payload['id']} | {label}")
        return "\n".join(lines)

    @staticmethod
    def _format_task_detail(task: Any, gates: list[dict[str, Any]]) -> str:
        lines = [
            f"Task: {task.id}",
            f"Title: {task.title}",
            f"Status: {task.status}",
            f"Current node: {task.current_node}",
            f"Task type: {task.task_type}",
        ]
        if task.inherits_from:
            lines.append("Inherits from:")
            lines.extend(f"- {item}" for item in task.inherits_from)
        if task.from_drawer:
            lines.append(f"From drawer: {task.from_drawer}")
        if task.effective_pills:
            lines.append("Effective pills:")
            lines.extend(f"- {item}" for item in task.effective_pills)
        if task.effective_atoms:
            lines.append("Effective atoms:")
            lines.extend(f"- {item}" for item in task.effective_atoms)
        if task.inherit_acceptance_context:
            lines.append("Effective validation:")
            lines.extend(f"- {item}" for item in task.effective_validation)
            lines.append(f"Effective done when: {task.effective_done_when}")
        if gates:
            lines.append("Lifecycle gates:")
            for gate in gates:
                state = "open" if gate["holds"] else "closed"
                condition = gate["condition"] or "(none)"
                lines.append(
                    f"- {gate['relation_type']} -> {gate['target']}: {state} [{condition}]"
                )
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_detail(subject: str, payload: dict[str, Any]) -> str:
        lines = [f"{subject.capitalize()}: {payload['id']}"]
        label = payload.get("title") or payload.get("name") or payload["id"]
        lines.append(f"Title: {label}")
        for key, value in payload.items():
            if key in {"id", "title", "current_node", "history", "tags"}:
                continue
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(str(item) for item in value)}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)
