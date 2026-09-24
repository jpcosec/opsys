from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Any

import yaml
from sldb.runtime.validation import extract_model_data

from deskops.models import RoleDoc


DEFAULT_PI_AGENT_DIR = Path.home() / ".pi" / "agent" / "agents"


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
    role_name = str(role_doc.get("name") or "").strip()
    if not role_name:
        raise ValueError("Role doc is missing a name")
    directory = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    return directory / f"{role_name}.md"


def _is_meaningful(value: Any) -> bool:
    """True unless ``value`` is absent, None, an empty string, or an empty list.

    Booleans are always meaningful (``False`` is a real, intentional value,
    not an absence — it must never be filtered out just because it is falsy).
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if value in ("", []):
        return False
    return True


def render_pi_agent_markdown(role_doc: dict[str, Any]) -> str:
    frontmatter = OrderedDict()
    frontmatter["name"] = role_doc.get("name")
    frontmatter["description"] = role_doc.get("description")
    for key in ("tools", "model", "fallback_models", "system_prompt_mode", "inherit_project_context", "inherit_skills", "default_context"):
        value = role_doc.get(key)
        if key in role_doc and _is_meaningful(value):
            # pi agent yaml expects camelCase
            camel_key = "".join(word.capitalize() if i > 0 else word for i, word in enumerate(key.split("_")))
            frontmatter[camel_key] = value

    frontmatter_text = yaml.safe_dump(dict(frontmatter), sort_keys=False, allow_unicode=True).strip()
    body = str(role_doc.get("body") or "").strip()
    return f"---\n{frontmatter_text}\n---\n\n{body}\n"


def materialize_role_docs(root: Path, out_dir: Path | None = None) -> list[tuple[Path, Path]]:
    written: list[tuple[Path, Path]] = []
    target_dir = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    for role_path in iter_role_doc_paths(root):
        role_doc = load_role_doc(role_path)
        if role_doc.get("kind") != "pi":
            continue
        output_path = output_path_for_role(root, role_doc, target_dir)
        output_path.write_text(render_pi_agent_markdown(role_doc), encoding="utf-8")
        written.append((role_path, output_path))
    return written


def drift_check_role_docs(root: Path, out_dir: Path | None = None) -> list[str]:
    # Only "pi" roles have a materialized pi-agent file to compare against.
    # Cross-kind capability-loss checks (a role's tools/fallback_models
    # silently unsupported by its RuntimeProfileDoc) belong to a separate
    # check once RuntimeProfileDoc exists; see
    # desk/drawer/features/feature-herdr-supervised-execution-runtime.md.
    findings: list[str] = []
    target_dir = out_dir if out_dir is not None else DEFAULT_PI_AGENT_DIR
    for role_path in iter_role_doc_paths(root):
        role_doc = load_role_doc(role_path)
        if role_doc.get("kind") != "pi":
            continue
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
