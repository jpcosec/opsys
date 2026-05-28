from __future__ import annotations

from pathlib import Path
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

        if args.command == "list" and args.subject == "tasks":
            for task in operations.list_tasks():
                print(f"{task.id} | {task.status} | {task.current_node}")
            return 0

        if args.command == "list" and args.subject == "routines":
            for routine in operations.list_routines():
                print(f"{routine.id} | {routine.status} | {routine.entrypoint}")
            return 0

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            for payload in operations.list_artifacts(artifact_id):
                label = payload.get("title") or payload.get("name") or payload["id"]
                print(f"{payload['id']} | {label}")
            return 0

        if args.command == "list" and args.subject in {"conditions", "operators", "checklists", "hooks", "edges"}:
            kind = args.subject[:-1]
            for payload in operations.list_primitives(kind):
                print(f"{payload['id']} | {payload['status']} | {payload['title']}")
            return 0

        if args.command == "show" and args.subject == "task":
            task, statuses = operations.show_task(args.task_id)
            if task is None:
                print(f"No task found for {args.task_id}")
                return 1
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
            payload = operations.show_artifact(artifact_id, args.doc_id)
            print(f"{args.subject.capitalize()}: {payload['id']}")
            label = payload.get("title") or payload.get("name") or payload["id"]
            print(f"Title: {label}")
            for key, value in payload.items():
                if key in {"id", "title", "routine", "current_node", "history", "field_refs", "tags"}:
                    continue
                if isinstance(value, list):
                    print(f"{key}: {', '.join(str(item) for item in value)}")
                else:
                    print(f"{key}: {value}")
            print("Field refs:")
            for ref in payload.get("field_refs", []):
                print(f"- {ref}")
            return 0

        if args.command == "show" and args.subject in {"condition", "operator", "checklist", "hook", "edge"}:
            payload = operations.show_primitive(args.subject, args.primitive_id)
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
                print(f"No task found for {args.task_id}")
                return 1
            if result is None:
                print(f"Task {task.id} has no routine — cannot advance")
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            return 0

        return 1
