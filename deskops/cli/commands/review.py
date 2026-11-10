"""``deskops review`` command handler: cold context reviews and their disposition."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.errors import DomainError
from deskops.errors import UsageError
from deskops.services.review import DEFAULT_ENGINE
from deskops.services.review import ReviewService


def _now_run() -> str:
    import datetime

    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")


def _format_run_report(data: dict[str, Any]) -> str:
    if data.get("state") == "unchanged":
        return f"{data['key']}: unchanged (already reviewed)"
    lines = [f"{data['key']}: {data['state']}"]
    if data.get("review_id"):
        lines.append(f"review: {data['review_id']}")
    lines.append(f"run_dir: {data.get('run_dir', '')}")
    lines.append(f"input_sha256: {data.get('input_sha256', '')}")
    return "\n".join(lines)


def _format_run_reports(data: list[dict[str, Any]]) -> str:
    if not data:
        return "No reviews run."
    return "\n\n".join(_format_run_report(item) for item in data)


def _format_status(data: list[dict[str, Any]]) -> str:
    if not data:
        return "No reviews recorded."
    return "\n".join(f"{item['key']:40} {item['state']:18} {item.get('input_sha256', '')[:12]}" for item in data)


def _format_dispose(data: dict[str, Any]) -> str:
    return (
        f"Disposed {data['review_id']} as {data['verdict']}\n"
        f"reason: {data['reason']}\n"
        f"disposed_at: {data['disposed_at']}\n"
        f"disposed_by: {data['disposed_by']}"
    )


def _format_record(data: dict[str, Any]) -> str:
    return (
        f"{data['key']}: {data['state']}\n"
        f"review: {data['review_id']}\n"
        f"evidence: {', '.join(data['evidence']) if data['evidence'] else '(none)'}\n"
        f"input_sha256: {data['input_sha256']}"
        + (f"\nengine: human; operator: {data['operator']}; {data['no_model_reason']}" if data.get("no_model_reason") else "")
    )


class ReviewCLI:
    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ReviewService(root)
        fmt = getattr(args, "format", "text")

        command = getattr(args, "review_command", None)

        if command == "preflight":
            return self._run_task(service, args, fmt, "preflight")
        if command == "bundle":
            return self._run_task(service, args, fmt, "bundle")
        if command == "node":
            return self._run_nodes(service, args, fmt)
        if command == "status":
            return self._status(service, args, fmt)
        if command == "dispose":
            return self._dispose(service, args, fmt)
        if command == "record":
            return self._record(service, args, fmt)
        return 1

    def _run_task(self, service: ReviewService, args: Any, fmt: str, mode: str) -> int:
        try:
            result = service.run_task(
                mode,
                args.task,
                run_name=getattr(args, "run", None) or _now_run(),
                engine=getattr(args, "engine", None) or DEFAULT_ENGINE,
                max_attempts=args.max_attempts,
                force=bool(getattr(args, "force", False)),
                reason=getattr(args, "reason", None) or "",
                timeout=args.timeout,
            )
        except (DomainError, UsageError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}", code=exc.exit_code)
        return render(result, fmt, _format_run_report)

    def _run_nodes(self, service: ReviewService, args: Any, fmt: str) -> int:
        try:
            results = service.run_nodes(
                args.plan_dir,
                list(args.ids or []),
                run_name=getattr(args, "run", None) or _now_run(),
                engine=getattr(args, "engine", None) or DEFAULT_ENGINE,
                max_attempts=args.max_attempts,
                force=bool(getattr(args, "force", False)),
                reason=getattr(args, "reason", None) or "",
                timeout=args.timeout,
            )
        except (DomainError, UsageError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}", code=exc.exit_code)
        return render(results, fmt, _format_run_reports)

    def _status(self, service: ReviewService, args: Any, fmt: str) -> int:
        try:
            results = service.status(getattr(args, "target", None))
        except (DomainError, UsageError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}", code=exc.exit_code)
        return render(results, fmt, _format_status)

    def _dispose(self, service: ReviewService, args: Any, fmt: str) -> int:
        try:
            result = service.dispose(args.review_id, args.verdict, args.reason)
        except (DomainError, UsageError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}", code=exc.exit_code)
        return render(result, fmt, _format_dispose)

    def _record(self, service: ReviewService, args: Any, fmt: str) -> int:
        try:
            result = service.record_receipt(
                args.task, args.kind, list(args.evidence or []), args.reason, getattr(args, "operator", None)
            )
        except (DomainError, UsageError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}", code=exc.exit_code)
        return render(result, fmt, _format_record)
