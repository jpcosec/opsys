from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import re
from typing import Any

import yaml
from sldb.cli.model_utils import registered_model, resolve_model_ref
from sldb.cli.store_context import get_store_context
from sldb.core.exceptions import SLDBStoreError, SLDBValidationError
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.layout import project_root
from sldb.store.ops import track_document
from sldb.store.resolver import find_local_store

from deskops.identity import infer_sender_project_identity
from deskops.identity import resolve_canonical_project_identity
from deskops.identity import resolve_registered_desk
from deskops.models import InboxNoteDoc


class InboxCLI:
    """Log messages arriving to a project inbox."""

    def run(self, args: Any) -> int:
        try:
            if args.list:
                return self._list_notes(args)
            if args.show:
                return self._show_note(args)
            if args.ack:
                return self._ack_note(args)
            if not args.message:
                print("Provide a message or use --list/--show/--ack.")
                return 1
            return self._deliver_note(args)
        except (SLDBStoreError, SLDBValidationError, ValueError) as exc:
            print(f"Error: {exc}")
            return 1

    def _deliver_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        inbox_dir = desk_root / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        created_at = datetime.now()
        title = args.title.strip() if args.title else self._derive_title(args.message)
        slug = self._slug(title)
        path = inbox_dir / f"{created_at.strftime('%Y%m%d-%H%M%S')}-{args.kind}-{slug}.md"
        sender_project = self._sender_project(args)
        payload = {
            "kind": args.kind,
            "sender_project": sender_project,
            "target_project": target_project,
            "created_at": created_at.isoformat(timespec="seconds"),
            "status": "open",
            "title": title,
            "body": args.message.strip(),
        }
        path.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
        tracked_name = self._verify_and_track_note(args, path)
        result = {
            "sender_project": sender_project,
            "target_project": target_project,
            "path": str(path),
            "tracked_name": tracked_name,
            "verified": True,
        }
        return self._print_delivery_result(result, args.format)

    def _list_notes(self, args: Any) -> int:
        notes = self._iter_notes(self._desk_root(args))[: args.limit]
        payload = [self._note_summary(path) for path in notes]
        return self._print(payload, args.format, key="notes")

    def _show_note(self, args: Any) -> int:
        note = self._resolve_note(self._desk_root(args), args.show)
        if note is None:
            print(f"Unknown inbox note: {args.show}")
            return 1
        payload = self._note_detail(note)
        return self._print(payload, args.format)

    def _ack_note(self, args: Any) -> int:
        target_project, desk_root = self._resolve_target(args)
        note = self._resolve_note(desk_root, args.ack)
        if note is None:
            print(f"Unknown inbox note: {args.ack}")
            return 1

        payload = extract_model_data(InboxNoteDoc, note.read_text(encoding="utf-8"))
        if payload.get("status") == "closed":
            raise ValueError(f"Inbox note '{note.stem}' is already acknowledged.")

        acknowledged_at = datetime.now().isoformat(timespec="seconds")
        payload["status"] = "closed"
        payload["target_project"] = payload.get("target_project") or target_project
        payload["acknowledged_by"] = target_project
        payload["acknowledged_at"] = acknowledged_at
        note.write_text(render_model_markdown(InboxNoteDoc, payload) + "\n", encoding="utf-8")
        tracked_name = self._verify_and_track_note(args, note)
        result = {
            "id": note.stem,
            "path": str(note),
            "status": "closed",
            "target_project": payload["target_project"],
            "acknowledged_by": target_project,
            "acknowledged_at": acknowledged_at,
            "tracked_name": tracked_name,
            "verified": True,
        }
        return self._print_ack_result(result, args.format)

    def _desk_root(self, args: Any) -> Path:
        if args.desk_root:
            return Path(args.desk_root).resolve()

        if args.repo:
            return self._resolve_repo_desk(args.repo, args.store, args.pythonpath)

        if args.store:
            return (project_root(Path(args.store).resolve()) / "desk").resolve()

        local_store = find_local_store()
        if local_store is not None:
            return (project_root(local_store) / "desk").resolve()

        return (Path.cwd() / "desk").resolve()

    def _resolve_target(self, args: Any) -> tuple[str, Path]:
        desk_root = self._desk_root(args)
        target_project = resolve_canonical_project_identity(desk_root.parent, args.store)
        return target_project, desk_root

    def _resolve_repo_desk(self, repo_name: str, store_arg: str | None, pythonpath: str | None) -> Path:
        _ = pythonpath
        return resolve_registered_desk(repo_name, store_arg)

    def _store_context_safe(self, store_arg: str | None) -> tuple[Path, Path]:
        if store_arg:
            return get_store_context(store_arg)
        local_store = find_local_store()
        if local_store is None:
            raise SLDBStoreError("No local store found. Use --store to anchor the repo lookup.")
        return local_store, project_root(local_store)

    def _iter_notes(self, desk_root: Path) -> list[Path]:
        inbox_dir = desk_root / "inbox"
        if not inbox_dir.exists():
            return []
        return sorted(inbox_dir.glob("*.md"), reverse=True)

    def _resolve_note(self, desk_root: Path, raw: str) -> Path | None:
        notes = self._iter_notes(desk_root)
        exact = next((path for path in notes if raw in {path.name, path.stem}), None)
        if exact is not None:
            return exact
        lowered = raw.lower()
        return next((path for path in notes if lowered in path.stem.lower()), None)

    def _note_summary(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, _ = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "kind": frontmatter.get("kind", ""),
            "sender_project": frontmatter.get("sender_project", ""),
            "target_project": frontmatter.get("target_project", ""),
            "status": frontmatter.get("status", ""),
            "created_at": frontmatter.get("created_at", ""),
            "acknowledged_by": frontmatter.get("acknowledged_by"),
            "acknowledged_at": frontmatter.get("acknowledged_at"),
            "title": title,
        }

    def _note_detail(self, path: Path) -> dict[str, str | None]:
        frontmatter, title, body = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "title": title,
            "body": body,
            **frontmatter,
        }

    def _parse_note(self, path: Path) -> tuple[dict[str, str | None], str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, str | None] = {}
        body = text
        if text.startswith("---\n"):
            _, rest = text.split("---\n", 1)
            fm_block, body = rest.split("\n---\n", 1)
            frontmatter = yaml.safe_load(fm_block) or {}
        lines = body.strip().splitlines()
        title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else path.stem
        content = "\n".join(lines[1:]).strip() if lines and lines[0].startswith("# ") else body.strip()
        return frontmatter, title, content

    def _print(self, payload: Any, fmt: str, key: str | None = None) -> int:
        if fmt == "json":
            print(json.dumps({key: payload} if key else payload, indent=2, default=str))
        elif fmt == "yaml":
            print(yaml.safe_dump({key: payload} if key else payload, sort_keys=False, allow_unicode=True))
        else:
            if key == "notes":
                if not payload:
                    print("No inbox notes.")
                    return 0
                for item in payload:
                    print(
                        f"{item['id']} | {item['kind']} | {item['sender_project']} -> {item['target_project']} | {item['status']} | {item['title']}"
                    )
            else:
                print(f"# {payload['title']}")
                print("")
                for meta in (
                    "kind",
                    "sender_project",
                    "target_project",
                    "created_at",
                    "status",
                    "acknowledged_by",
                    "acknowledged_at",
                    "path",
                ):
                    if meta in payload and payload[meta] not in {None, ""}:
                        print(f"{meta}: {payload[meta]}")
                print("")
                print(payload.get("body", ""))
        return 0

    def _print_delivery_result(self, payload: dict[str, Any], fmt: str) -> int:
        if fmt in {"json", "yaml"}:
            return self._print(payload, fmt)
        print(
            "Delivered inbox note "
            f"from {payload['sender_project']} to {payload['target_project']} at {payload['path']}"
        )
        print(f"Tracked '{payload['tracked_name']}'")
        return 0

    def _print_ack_result(self, payload: dict[str, Any], fmt: str) -> int:
        if fmt in {"json", "yaml"}:
            return self._print(payload, fmt)
        print(
            f"Acknowledged {payload['id']} as {payload['status']} "
            f"by {payload['acknowledged_by']} at {payload['acknowledged_at']}"
        )
        print(f"Path: {payload['path']}")
        print(f"Tracked '{payload['tracked_name']}'")
        return 0

    def _derive_title(self, message: str) -> str:
        first = message.strip().splitlines()[0] if message.strip() else "Inbox note"
        return first[:72]

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "note"

    def _sender_project(self, args: Any) -> str:
        if getattr(args, "sender", None):
            sender_desk = resolve_registered_desk(args.sender, args.store)
            return resolve_canonical_project_identity(sender_desk.parent, args.store)

        sender_root = Path.cwd().resolve()
        sender_project = infer_sender_project_identity(sender_root, args.store)
        if sender_project is None:
            raise SLDBStoreError(
                f"Unable to resolve sender identity for '{sender_root}'. Use --sender or register the repository canonically."
            )
        return sender_project

    def _verify_and_track_note(self, args: Any, path: Path) -> str:
        store_path, root = self._store_context_safe(args.store)
        model_type, entry, idx = registered_model(store_path, "InboxNoteDoc", args.pythonpath)

        rendered = path.read_text(encoding="utf-8")
        valid, details = validate_model_input_roundtrip(model_type, rendered)
        if not valid:
            raise SLDBValidationError("Inbox note failed validation", details)

        note_name = path.stem
        track_document(
            store_path,
            root,
            idx,
            model_type,
            entry,
            path,
            note_name,
            resolve_model_ref,
            args.pythonpath,
        )
        return note_name

    def _store_context(self, args: Any) -> tuple[Path, Path] | None:
        if args.store:
            return get_store_context(args.store)
        local_store = find_local_store()
        if local_store is None:
            return None
        return local_store, project_root(local_store)
