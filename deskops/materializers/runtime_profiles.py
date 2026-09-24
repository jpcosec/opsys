"""Translate a RoleDoc + its matching RuntimeProfileDoc into CLI args.

Deliberately pure: no filesystem writes, no subprocess calls, no Herdr. The
caller decides where to write a file-delivered system prompt and where the
session path points; this module only knows how to fold role settings
through a runtime's declared flag vocabulary.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.runtime.validation import extract_model_data

from deskops.models import RuntimeProfileDoc

JOIN_MODES = {"comma", "space", "repeat"}
SYSTEM_PROMPT_DELIVERIES = {"inline", "file"}


def runtime_profiles_dir(root: Path) -> Path:
    return root / "desk" / "runtimes"


def iter_runtime_profile_paths(root: Path) -> list[Path]:
    directory = runtime_profiles_dir(root)
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("*.md") if path.is_file())


def load_runtime_profile(path: Path) -> dict[str, Any]:
    return extract_model_data(RuntimeProfileDoc, path.read_text(encoding="utf-8"))


def load_runtime_profiles(root: Path) -> dict[str, dict[str, Any]]:
    """Map kind -> profile payload for every tracked RuntimeProfileDoc."""
    profiles: dict[str, dict[str, Any]] = {}
    for path in iter_runtime_profile_paths(root):
        data = load_runtime_profile(path)
        profiles[data["kind"]] = data
    return profiles


def _join_flag(flag: str, values: list[str], join: str) -> list[str]:
    if not values:
        return []
    if join == "repeat":
        return [item for value in values for item in (flag, value)]
    sep = "," if join == "comma" else " "
    return [flag, sep.join(values)]


def build_agent_spec_args(
    role_doc: dict[str, Any],
    profile: dict[str, Any],
    *,
    session_path: str | Path | None = None,
    system_prompt_path: str | Path | None = None,
) -> tuple[str, ...]:
    """Translate one RoleDoc + its matching RuntimeProfileDoc into CLI args.

    A flag is only emitted when the profile declares it AND the role has a
    meaningful (non-empty) value for that setting; an empty tools list or
    empty model must never surface as an explicit empty flag value.
    """
    args: list[str] = []

    model = role_doc.get("model")
    if profile.get("model_flag") and model:
        args += [profile["model_flag"], model]

    fallback_models = role_doc.get("fallback_models") or []
    if profile.get("fallback_models_flag") and fallback_models:
        args += _join_flag(profile["fallback_models_flag"], fallback_models, profile.get("fallback_models_join", "comma"))

    tools = role_doc.get("tools") or []
    if profile.get("tools_flag") and tools:
        args += _join_flag(profile["tools_flag"], tools, profile.get("tools_join", "comma"))

    body = role_doc.get("body")
    if profile.get("system_prompt_flag") and body:
        delivery = profile.get("system_prompt_delivery", "inline")
        if delivery == "file":
            if system_prompt_path:
                args += [profile["system_prompt_flag"], str(system_prompt_path)]
        else:
            args += [profile["system_prompt_flag"], body]

    if profile.get("session_flag") and session_path:
        args += [profile["session_flag"], str(session_path)]

    args += list(profile.get("extra_args") or [])
    return tuple(args)


def drift_check_runtime_bindings(root: Path) -> list[str]:
    """Cross-check every RoleDoc against the RuntimeProfileDoc for its kind.

    Two findings, both real capability-loss bugs rather than cosmetic drift:

    - a role's ``kind`` has no matching tracked RuntimeProfileDoc at all, so
      nothing in the fleet knows how to launch it;
    - a role declares ``tools`` or ``fallback_models`` that its runtime's
      profile has no flag for, and the profile does not list that field in
      ``unsupported_role_fields`` — meaning the setting would be silently
      dropped rather than deliberately acknowledged as unsupported.
    """
    from deskops.materializers.roles import iter_role_doc_paths, load_role_doc

    findings: list[str] = []
    profiles = load_runtime_profiles(root)
    for role_path in iter_role_doc_paths(root):
        role_doc = load_role_doc(role_path)
        role_name = role_doc.get("name") or role_path.stem
        kind = role_doc.get("kind")
        profile = profiles.get(kind)
        if profile is None:
            findings.append(f"missing runtime profile for kind '{kind}' (used by role '{role_name}')")
            continue

        unsupported = set(profile.get("unsupported_role_fields") or [])
        if role_doc.get("tools") and not profile.get("tools_flag") and "tools" not in unsupported:
            findings.append(
                f"silent capability loss: role '{role_name}' sets tools but runtime '{kind}' has no tools_flag "
                f"and does not list 'tools' in unsupported_role_fields"
            )
        if role_doc.get("fallback_models") and not profile.get("fallback_models_flag") and "fallback_models" not in unsupported:
            findings.append(
                f"silent capability loss: role '{role_name}' sets fallback_models but runtime '{kind}' has no "
                f"fallback_models_flag and does not list 'fallback_models' in unsupported_role_fields"
            )
    return findings
