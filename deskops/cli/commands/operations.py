from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
import sys
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS


class OperationsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        operations = DeskopsOperations(root)

        if args.command == "add" and args.subject == "task":
            payload = operations.parse_task_input(args)
            bundle = operations.create_task_bundle(payload)
            print(f"Created task bundle {bundle.task_id}")
            print(f"Task: {bundle.task_path}")
            print(f"Routine: {bundle.routine_path}")
            return 0

        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "add" and args.subject in artifact_subjects:
            artifact_id = artifact_subjects[args.subject]
            payload = operations.parse_artifact_input(artifact_id, args)
            record = operations.create_artifact(artifact_id, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            if args.subject == "repository":
                print("Note: this is a local repository artifact. Use 'deskops repo register' for canonical ecosystem registration.")
            return 0

        if args.command == "add" and args.subject in {"condition", "operator", "checklist", "hook", "edge"}:
            payload = operations.parse_primitive_input(args.subject, args)
            record = operations.create_primitive(args.subject, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "add" and args.subject == "routine":
            payload = operations.parse_routine_input(args)
            record = operations.create_routine(payload)
            print(f"Created routine {record.doc_id}")
            print(f"Path: {record.path}")
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
            if args.format == "json":
                payload = {"tasks": self._normalize(tasks)}
                if getattr(args, "include_repos", False):
                    payload["repo_routes"] = self._normalize(repo_routes)
                self._print_json(payload)
                return 0
            for task in tasks:
                print(f"{task.id} | {task.status} | {task.current_node}")
            for route in repo_routes:
                print(f"{route.repo_id}:{route.task_id} | {route.status} | {route.title} | {route.task_path}")
            return 0

        if args.command == "list" and args.subject == "routines":
            routines = operations.list_routines()
            if args.format == "json":
                self._print_json({"routines": self._normalize(routines)})
                return 0
            for routine in routines:
                print(f"{routine.id} | {routine.status} | {routine.entrypoint}")
            return 0

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            payloads = operations.list_artifacts(artifact_id)
            if args.format == "json":
                self._print_json({args.subject: self._normalize(payloads)})
                return 0
            for payload in payloads:
                label = payload.get("title") or payload.get("name") or payload["id"]
                print(f"{payload['id']} | {label}")
            return 0

        if args.command == "list" and args.subject in {"conditions", "operators", "checklists", "hooks", "edges"}:
            kind = args.subject[:-1]
            payloads = operations.list_primitives(kind)
            if args.format == "json":
                self._print_json({args.subject: self._normalize(payloads)})
                return 0
            for payload in payloads:
                print(f"{payload['id']} | {payload['status']} | {payload['title']}")
            return 0

        if args.command == "show" and args.subject == "task":
            task, statuses = operations.show_task(args.task_id)
            if task is None:
                print(f"No task found for {args.task_id}")
                return 1
            if args.format == "json":
                payload = self._normalize(task)
                payload["checklist_statuses"] = self._normalize(statuses)
                self._print_json(payload)
                return 0
            print(f"Task: {task.id}")
            print(f"Title: {task.title}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Routine: {task.routine}")
            print("Checklist status:")
            for checklist_id, complete in statuses.items():
                print(f"- {checklist_id}: {'complete' if complete else 'pending'}")
            return 0

        if args.command == "show" and args.subject == "routine":
            routine = operations.show_routine(args.routine_id)
            if routine is None:
                print(f"No routine found for {args.routine_id}")
                return 1
            if args.format == "json":
                self._print_json(self._normalize(routine))
                return 0
            print(f"Routine: {routine.id}")
            print(f"Title: {routine.title}")
            print(f"Status: {routine.status}")
            print(f"Entrypoint: {routine.entrypoint}")
            print("Decomposition:")
            for node in routine.decomposition:
                print(f"- {node}")
            print("Edges:")
            for edge in routine.edges:
                print(f"- {edge.id}: {edge.source} -> {edge.target}")
            return 0

        show_artifacts = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "show" and args.subject in show_artifacts:
            artifact_id = show_artifacts[args.subject]
            try:
                payload = operations.show_artifact(artifact_id, args.doc_id)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            if args.format == "json":
                self._print_json(self._normalize(payload))
                return 0
            print(f"{args.subject.capitalize()}: {payload['id']}")
            label = payload.get("title") or payload.get("name") or payload["id"]
            print(f"Title: {label}")
            for key, value in payload.items():
                if key in {"id", "title", "routine", "current_node", "history", "tags"}:
                    continue
                if isinstance(value, list):
                    print(f"{key}: {', '.join(str(item) for item in value)}")
                else:
                    print(f"{key}: {value}")
            return 0

        if args.command == "show" and args.subject in {"condition", "operator", "checklist", "hook", "edge"}:
            payload = operations.show_primitive(args.subject, args.primitive_id)
            if args.format == "json":
                self._print_json(self._normalize(payload))
                return 0
            print(f"{args.subject.capitalize()}: {payload['id']}")
            print(f"Title: {payload['title']}")
            print(f"Status: {payload['status']}")
            if args.subject == "condition":
                print(f"Subject: {payload['subject']}")
                print(f"Predicate: {payload['predicate']}")
            elif args.subject == "operator":
                print(f"Action: {payload['action']}")
                print(f"Target: {payload['target']}")
            elif args.subject == "checklist":
                print(f"Mode: {payload['mode']}")
                print("Items:")
                for item in payload.get('items', []):
                    print(f"- {item}")
            elif args.subject == "hook":
                print(f"Event: {payload['event']}")
                print(f"Target: {payload['target']}")
            elif args.subject == "edge":
                print(f"Source: {payload['source']}")
                print(f"Target: {payload['target']}")
            return 0

        if args.command == "advance" and args.subject == "task":
            task, result = operations.advance_task(args.task_id)
            if task is None:
                print(f"No task found for {args.task_id}", file=sys.stderr)
                return 1
            if result is None:
                print(f"Task {task.id} has no routine — cannot advance", file=sys.stderr)
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Message: {result.message}")
            return 1 if result.blocked else 0

        return 1

    def _print_next_action_report(self, report: dict[str, Any]) -> None:
        print(f"Task: {report['task']['id']}")
        print(f"Title: {report['task']['title']}")
        print(f"Status: {report['task']['status']}")
        print(f"Current node: {report['task']['current_node']}")
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

    def _print_json(self, payload: Any) -> None:
        print(json.dumps(self._normalize(payload), indent=2))

    def _normalize(self, payload: Any) -> Any:
        if hasattr(payload, "__dataclass_fields__"):
            return self._normalize(asdict(payload))
        if isinstance(payload, Path):
            return str(payload)
        if isinstance(payload, dict):
            return {str(key): self._normalize(value) for key, value in payload.items()}
        if isinstance(payload, (list, tuple)):
            return [self._normalize(value) for value in payload]
        return payload
