from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json
import sys
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS

from deskops import forms
from deskops.derived_conditions import UnknownTaskError


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

        if args.command == "edit" and args.subject == "task":
            # F4 T4.3: the task edit is a forms-layer move (read the document,
            # patch the modeled field, re-render), not a CRUD record.
            field = args.field.replace("-", "_")
            try:
                view = forms.edit_task_field(root, args.selector, field, args.value)
            except (forms.FormsError, UnknownTaskError, FileNotFoundError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Updated task {view.id} field {field}")
            print(f"Path: {view.path}")
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
            # F4 T4.2: the row a task shows is its derived status.
            tasks = forms.list_tasks(root)
            rows = [
                {
                    "id": task.id,
                    "status": task.status,
                    "title": str(task.payload.get("title") or task.id),
                    **forms.effective_payload(root, task.id),
                }
                for task in tasks
            ]
            repo_routes = operations.list_repo_task_routes() if getattr(args, "include_repos", False) else []
            if args.format == "json":
                payload = {"tasks": self._normalize(rows)}
                if getattr(args, "include_repos", False):
                    payload["repo_routes"] = self._normalize(repo_routes)
                self._print_json(payload)
                return 0
            for row in rows:
                print(f"{row['id']} | {row['status']} | {row['title']}")
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
        if args.command == "list" and args.subject == "atoms":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            if args.format == "json":
                self._print_json({"axis": axis, "atoms": self._normalize(payloads)})
                return 0
            for payload in payloads:
                label = payload.get("title") or payload.get("name") or payload["id"]
                if axis:
                    values = ",".join(payload.get("axis_values") or []) or "-"
                    print(f"{payload['id']} | {label} | {axis}:{values}")
                else:
                    print(f"{payload['id']} | {label}")
            return 0
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
            # F4 T4.2: same read as list, for one task, with its derived status.
            try:
                payload = forms.effective_payload(root, args.task_id)
            except (forms.FormsError, UnknownTaskError, FileNotFoundError):
                print(f"No task found for {args.task_id}")
                return 1
            if args.format == "json":
                self._print_json(self._normalize(payload))
                return 0
            print(f"Task: {payload['id']}")
            print(f"Title: {payload.get('title', '')}")
            print(f"Status: {payload['status']}")
            print(f"Task type: {payload.get('task_type', '')}")
            if payload.get("inherits_from"):
                print("Inherits from:")
                for item in payload["inherits_from"]:
                    print(f"- {item}")
            print(f"Routine: {payload.get('routine', '')}")
            if payload.get("effective_pills"):
                print("Effective pills:")
                for item in payload["effective_pills"]:
                    print(f"- {item}")
            if payload.get("effective_atoms"):
                print("Effective atoms:")
                for item in payload["effective_atoms"]:
                    print(f"- {item}")
            if payload.get("inherit_acceptance_context"):
                print("Effective validation:")
                for item in payload.get("effective_validation", []):
                    print(f"- {item}")
                print(f"Effective done when: {payload.get('effective_done_when', '')}")
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
            # F4 T4.4: the status is derived, so `advance` does not move a state
            # machine — it reports the derived status and the gate that the next
            # rung of the ladder still needs.
            try:
                view, gate = forms.advance_task(root, args.task_id)
            except (forms.FormsError, UnknownTaskError, FileNotFoundError) as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            print(f"Task: {view.id}")
            print(f"Status: {view.status}")
            if not gate.satisfied:
                print(f"Message: {gate.message}")
            return 0 if gate.satisfied else 1

        return 1

    def _print_next_action_report(self, report: dict[str, Any]) -> None:
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
