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
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.layout import project_root
from sldb.store.ops import track_document
from sldb.store.resolver import find_local_store

from deskops.identity import infer_sender_project_identity
from deskops.identity import resolve_registered_desk


class InboxCLI:
    """Log messages arriving to a project inbox."""

    def run(self, args: Any) -> int:
        if args.list:
            return self._list_notes(args)
        if args.show:
            return self._show_note(args)
        if not args.message:
            print("Provide a message or use --list/--show.")
            return 1

        desk_root = self._desk_root(args)
        inbox_dir = desk_root / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)

        created_at = datetime.now()
        title = args.title.strip() if args.title else self._derive_title(args.message)
        slug = self._slug(title)
        path = inbox_dir / f"{created_at.strftime('%Y%m%d-%H%M%S')}-{args.kind}-{slug}.md"
        sender_project = self._sender_project(args)
        path.write_text(
            self._render_note(args.kind, title, args.message, sender_project, created_at),
            encoding="utf-8",
        )
        tracked_name = self._auto_track_note(args, path)
        print(f"Wrote {path}")
        if tracked_name:
            print(f"Tracked '{tracked_name}'")
        return 0

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
        exact = next(
            (
                path
                for path in notes
                if raw in {path.name, path.stem}
            ),
            None,
        )
        if exact is not None:
            return exact
        lowered = raw.lower()
        return next((path for path in notes if lowered in path.stem.lower()), None)

    def _note_summary(self, path: Path) -> dict[str, str]:
        frontmatter, title, _ = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "kind": frontmatter.get("kind", ""),
            "sender_project": frontmatter.get("sender_project", ""),
            "status": frontmatter.get("status", ""),
            "created_at": frontmatter.get("created_at", ""),
            "title": title,
        }

    def _note_detail(self, path: Path) -> dict[str, str]:
        frontmatter, title, body = self._parse_note(path)
        return {
            "id": path.stem,
            "path": str(path),
            "title": title,
            "body": body,
            **frontmatter,
        }

    def _parse_note(self, path: Path) -> tuple[dict[str, str], str, str]:
        text = path.read_text(encoding="utf-8")
        frontmatter: dict[str, str] = {}
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
                        f"{item['id']} | {item['kind']} | {item['sender_project']} | {item['status']} | {item['title']}"
                    )
            else:
                print(f"# {payload['title']}")
                print("")
                for meta in ("kind", "sender_project", "created_at", "status", "path"):
                    if meta in payload:
                        print(f"{meta}: {payload[meta]}")
                print("")
                print(payload.get("body", ""))
        return 0

    def _derive_title(self, message: str) -> str:
        first = message.strip().splitlines()[0] if message.strip() else "Inbox note"
        return first[:72]

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "note"

    def _render_note(
        self, kind: str, title: str, message: str, sender_project: str, created_at: datetime
    ) -> str:
        return "\n".join(
            [
                "---",
                f"kind: {kind}",
                f"sender_project: {sender_project}",
                f"created_at: {created_at.isoformat(timespec='seconds')}",
                "status: open",
                "---",
                "",
                f"# {title}",
                "",
                message.strip(),
                "",
            ]
        )

    def _sender_project(self, args: Any) -> str:
        sender_root = Path.cwd().resolve()
        context = self._store_context(args)
        if context is None:
            return sender_root.name
        sender_project = infer_sender_project_identity(sender_root, args.store)
        if sender_project is None:
            return sender_root.name
        return sender_project

    def _auto_track_note(self, args: Any, path: Path) -> str | None:
        context = self._store_context(args)
        if context is None:
            return None
        store_path, root = context
        try:
            # We first try to resolve InboxNoteDoc from opsys itself if possible,
            # or rely on the store's registered model name.
            model_type, entry, idx = registered_model(
                store_path, "InboxNoteDoc", args.pythonpath
            )
        except SLDBStoreError:
            return None

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

