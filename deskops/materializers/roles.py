from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import extract_model_data

from deskops.models import RoleDoc


DEFAULT_PI_AGENT_DIR = Path.home() / ".pi" / "agent" / "agents"


@dataclass(frozen=True)
class RoleAgentSpec:
    output_name: str
    frontmatter_items: tuple[tuple[str, Any], ...]


ROLE_AGENT_SPECS: dict[str, RoleAgentSpec] = {
    "deskops-supervisor": RoleAgentSpec(
        output_name="deskops-supervisor.md",
        frontmatter_items=(
            ("tools", ["read", "grep", "find", "ls", "bash"]),
            ("model", "anthropic/claude-opus-4-8"),
            ("fallbackModels", ["openai-codex/gpt-5.4"]),
            ("systemPromptMode", "replace"),
            ("inheritProjectContext", True),
            ("inheritSkills", True),
            ("defaultContext", "fresh"),
        ),
    ),
    "deskops-executor": RoleAgentSpec(
        output_name="deskops-executor.md",
        frontmatter_items=(
            ("systemPromptMode", "replace"),
            ("inheritProjectContext", True),
            ("inheritSkills", True),
            ("defaultContext", "fresh"),
            ("model", "openai-codex/gpt-5.4"),
            ("fallbackModels", ["google-gemini-cli/gemini-3.1-pro-preview"]),
        ),
    ),
    "deskops-tester": RoleAgentSpec(
        output_name="deskops-tester.md",
        frontmatter_items=(
            ("systemPromptMode", "replace"),
            ("inheritProjectContext", True),
            ("inheritSkills", True),
            ("defaultContext", "fresh"),
            ("model", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"),
            ("fallbackModels", ["openrouter/openai/gpt-oss-20b:free"]),
            ("tools", ["read", "grep", "find", "ls", "bash"]),
        ),
    ),
}


def role_docs_dir(root: Path) -> Path:
    return root / "desk" / "roles"


def iter_role_doc_paths(root: Path) -> list[Path]:
    directory = role_docs_dir(root)
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("*.md") if path.is_file())


def load_role_doc(path: Path) -> dict[str, Any]:
    return extract_model_data(RoleDoc, path.read_text(encoding="utf-8"))


def output_path_for_role(root: Path, role_doc: dict[str, Any], out_dir: Path | None = None) -> Path:
    spec = role_agent_spec(role_doc)
    directory = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    return directory / spec.output_name


def role_agent_spec(role_doc: dict[str, Any]) -> RoleAgentSpec:
    role_name = str(role_doc.get("name") or "").strip()
    try:
        return ROLE_AGENT_SPECS[role_name]
    except KeyError as exc:
        raise ValueError(f"Unsupported role doc name: {role_name}") from exc


def render_pi_agent_markdown(role_doc: dict[str, Any]) -> str:
    spec = role_agent_spec(role_doc)
    frontmatter = OrderedDict()
    frontmatter["name"] = role_doc["name"]
    frontmatter["description"] = role_doc["description"]
    for key, value in spec.frontmatter_items:
        frontmatter[key] = value
    frontmatter_text = yaml.safe_dump(dict(frontmatter), sort_keys=False, allow_unicode=True).strip()
    body = str(role_doc.get("body") or "").strip()
    return f"---\n{frontmatter_text}\n---\n\n{body}\n"


def materialize_role_docs(root: Path, out_dir: Path | None = None) -> list[tuple[Path, Path]]:
    written: list[tuple[Path, Path]] = []
    target_dir = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    for role_path in iter_role_doc_paths(root):
        role_doc = load_role_doc(role_path)
        output_path = output_path_for_role(root, role_doc, target_dir)
        output_path.write_text(render_pi_agent_markdown(role_doc), encoding="utf-8")
        written.append((role_path, output_path))
    return written


def drift_check_role_docs(root: Path, out_dir: Path | None = None) -> list[str]:
    findings: list[str] = []
    target_dir = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    for role_path in iter_role_doc_paths(root):
        role_doc = load_role_doc(role_path)
        output_path = output_path_for_role(root, role_doc, target_dir)
        expected = render_pi_agent_markdown(role_doc)
        if not output_path.exists():
            findings.append(
                f"missing: {output_path} (expected from {role_path.relative_to(root)})"
            )
            continue
        actual = output_path.read_text(encoding="utf-8")
        if actual != expected:
            findings.append(
                f"mismatch: {output_path} (rendered from {role_path.relative_to(root)})"
            )
    return findings
