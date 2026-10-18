from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error


@dataclass
class FAQEntry:
    index: int
    question: str
    slug: str
    answer: str


class FAQCLI:
    """Browse FAQ entries from the FAQ markdown file."""

    def run(self, args: Any) -> int:
        faq_path = Path(args.faq_path)
        if not faq_path.exists():
            if args.faq_path != "docs/faq.md":
                import sys
                print(f"Warning: FAQ path {args.faq_path} not found. Falling back to default.", file=sys.stderr)
            repo_faq = Path(__file__).resolve().parents[3] / "docs" / "faq.md"
            if repo_faq.exists():
                faq_path = repo_faq

        if not faq_path.exists():
            return render_error(
                f"FAQ file not found: {args.faq_path}",
                args.format,
                type_name="DomainError",
            )

        entries = self._parse_entries(faq_path)
        if not args.question:
            return self._print_index(entries, args.format)

        entry = self._select_entry(entries, str(args.question))
        if entry is None:
            return render_error(
                f"Unknown FAQ question: {args.question}",
                args.format,
                type_name="DomainError",
            )
        return self._print_entry(entry, args.format)

    def _parse_entries(self, path: Path) -> list[FAQEntry]:
        text = path.read_text(encoding="utf-8")
        matches = list(re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE))
        entries: list[FAQEntry] = []
        for idx, match in enumerate(matches, start=1):
            start = match.end()
            end = matches[idx].start() if idx < len(matches) else len(text)
            entries.append(
                FAQEntry(
                    index=idx,
                    question=match.group(1).strip(),
                    slug=self._slug(match.group(1).strip()),
                    answer=text[start:end].strip(),
                )
            )
        return entries

    def _select_entry(self, entries: list[FAQEntry], raw: str) -> FAQEntry | None:
        if raw.isdigit():
            wanted = int(raw)
            return next((entry for entry in entries if entry.index == wanted), None)

        normalized = raw.strip().lower()
        exact = next(
            (
                entry
                for entry in entries
                if normalized == entry.slug.lower() or normalized == entry.question.lower()
            ),
            None,
        )
        if exact is not None:
            return exact

        return next(
            (
                entry
                for entry in entries
                if normalized in entry.slug.lower() or normalized in entry.question.lower()
            ),
            None,
        )

    def _print_index(self, entries: list[FAQEntry], fmt: str) -> int:
        payload = [asdict(entry) | {"answer": None} for entry in entries]
        return render(
            {"questions": payload},
            fmt,
            lambda _data: self._format_index(entries),
        )

    @staticmethod
    def _format_index(entries: list[FAQEntry]) -> str:
        lines = ["deskops FAQ questions:", ""]
        lines.extend(f"{entry.index}. {entry.question} [{entry.slug}]" for entry in entries)
        return "\n".join(lines)

    def _print_entry(self, entry: FAQEntry, fmt: str) -> int:
        payload = asdict(entry)
        return render(payload, fmt, lambda _data: f"{entry.index}. {entry.question}\n\n{entry.answer}")

    def _slug(self, text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        return slug or "question"
