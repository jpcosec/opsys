"""RoleDoc + RuntimeProfileDoc -> Scion agent template, against this repo's real desk."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from deskops.materializers.runtime_profiles import load_runtime_profiles
from deskops.models import RunDoc, TaskDoc
from deskops.runtime.scion import (
    TEMPLATE_FILES,
    find_role_doc,
    load_scion_context,
    materialize_scion_template,
    pick_harness_config,
    record_scion_run,
    scion_child_identity,
    scion_start_argv,
    scion_template_files,
    validate_scion_context,
)
from sldb.runtime.validation import extract_model_data, render_model_markdown
from sldb.store.graph.language.contract_hash import contract_hash
from sldb.store.hashing import hash_fields_with_map


@pytest.fixture(scope="module")
def executor() -> dict:
    _, role_doc = find_role_doc(ROOT, "role-deskops-executor")
    return role_doc


@pytest.fixture(scope="module")
def profiles() -> dict[str, dict]:
    return load_runtime_profiles(ROOT)


def test_harness_for_every_tracked_runtime_kind(profiles: dict[str, dict]) -> None:
    for kind in profiles:
        assert pick_harness_config(kind)
    with pytest.raises(ValueError, match="no Scion harness-config"):
        pick_harness_config("emacs")


def test_find_role_doc_accepts_id_and_name() -> None:
    by_id = find_role_doc(ROOT, "role-deskops-executor")[1]
    by_name = find_role_doc(ROOT, "deskops-executor")[1]
    assert by_id == by_name
    with pytest.raises(ValueError, match="no RoleDoc"):
        find_role_doc(ROOT, "role-nobody")


def test_claude_template_is_portable_and_loud_about_omissions(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["claude"], harness="claude", source="desk/roles/x.md")
    assert set(files) == set(TEMPLATE_FILES)

    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["schema_version"] == "1"
    assert agent["default_harness_config"] == "claude"
    assert agent["model"] == "medium"  # size alias, never the concrete RoleDoc model
    assert agent["auth_selectedType"] == "oauth-token"  # never left to whatever credential the Hub finds
    assert agent["agent_instructions"] == "agents.md"
    assert agent["system_prompt"] == "system-prompt.md"
    assert agent["max_turns"] and agent["max_duration"]
    assert "image" not in agent  # environment keys belong to the harness-config

    text = files["scion-agent.yaml"]
    assert "# Source: desk/roles/x.md" in text
    assert executor["model"] in text  # the concrete model is named in a comment
    assert "fallback_models" in text and "unsupported_role_fields" in text  # dropped, but said so
    assert files["system-prompt.md"].strip() == executor["body"].strip()
    assert "Write only there" in files["agents.md"]
    assert "deskops closeout" in files["agents.md"]


def test_pi_template_targets_the_pi_harness_config(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["pi"], harness="pi", model_alias="small", task_repo="sldb")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["default_harness_config"] == "pi"
    assert agent["model"] == "small"
    assert "auth_selectedType" not in agent
    assert "repository `sldb`" in files["agents.md"]


def test_supervisor_role_gets_coordinator_instructions(profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    agents = files["agents.md"]
    assert "coordinator of the `deskops` desk" in agents
    assert "One executor per repository at a time" in agents
    assert "Do not push" in agents and "Never decide for the owner" in agents
    # the executor text is not in it, and an explicit mode overrides the name
    assert "You are a deskops executor" not in agents
    forced = scion_template_files(supervisor, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in forced["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(supervisor, profiles["claude"], harness="claude", mode="boss")


def test_statuses_are_ones_sciontool_has_and_wake_the_coordinator(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")
    for text in (coordinator["agents.md"], worker["agents.md"]):
        statuses = set(re.findall(r"sciontool status (\w+)", text))
        assert statuses <= {"ask_user", "blocked", "task_completed"}, statuses
    assert "sciontool status task_completed" in worker["agents.md"]  # blocked would not wake the coordinator

    # A coordinator idles blocked on its children; the executor's limit would kill it.
    assert yaml.safe_load(coordinator["scion-agent.yaml"])["max_duration"] == "24h"
    assert yaml.safe_load(worker["scion-agent.yaml"])["max_duration"] == "2h"


def test_tools_fold_into_command_args_when_the_profile_has_a_flag(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "claude", "model": "", "tools": ["Read", "Bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["claude"], harness="claude")["scion-agent.yaml"])
    assert agent["command_args"] == ["--allowedTools", "Read", "--allowedTools", "Bash"]


def test_bad_alias_and_bad_harness_are_refused(executor: dict, profiles: dict[str, dict]) -> None:
    with pytest.raises(ValueError, match="model alias"):
        scion_template_files(executor, profiles["claude"], harness="claude", model_alias="huge")
    with pytest.raises(ValueError, match="unknown Scion harness-config"):
        scion_template_files(executor, profiles["claude"], harness="emacs")


def test_materialize_writes_the_three_files(tmp_path: Path) -> None:
    target = materialize_scion_template(ROOT, "deskops-executor", harness="claude", out_dir=tmp_path / "t")
    assert target == tmp_path / "t"
    assert sorted(p.name for p in target.iterdir()) == sorted(TEMPLATE_FILES)
    assert "Source: desk/roles/deskops-executor.md + desk/runtimes/runtime-claude.md" in (target / "scion-agent.yaml").read_text()


def test_cli_runtime_template(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude", "--out", str(tmp_path / "t")])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "Scion template:" in out and "scion start" in out
    assert (tmp_path / "t" / "scion-agent.yaml").exists()


def test_cli_task_root_puts_the_rundoc_next_to_the_task(tmp_path: Path, capsys) -> None:
    task_root = tmp_path / "other-repo"
    task_root.mkdir()
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-x", "--task-root", str(task_root),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    runs = list((task_root / "runs" / "subagents").glob("*-task-x/run.md"))
    assert len(runs) == 1, out

    # An agent that already made its own evidence dir: the RunDoc points there.
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-y", "--task-root", str(task_root),
        "--run-dir", "runs/subagents/20261029-000000-task-x",
    ])
    assert code == 0, capsys.readouterr().out
    doc = extract_model_data(RunDoc, (task_root / "runs/subagents/20261029-000000-task-x/run.md").read_text(encoding="utf-8"))
    assert doc["run_dir"] == "runs/subagents/20261029-000000-task-x" and doc["id"] == "run-agent-y"
    assert not list((ROOT / "runs" / "subagents").glob("*-task-x"))  # nothing written into the roles' repo
    assert extract_model_data(RunDoc, runs[0].read_text(encoding="utf-8"))["id"] == "run-agent-x"


def test_cli_task_without_agent_is_an_error(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--out", str(tmp_path / "t"), "--task", "task-x"])
    captured = capsys.readouterr()
    assert code != 0
    assert "--task and --agent go together" in captured.out + captured.err


def test_record_scion_run_writes_a_rundoc_that_roundtrips(tmp_path: Path) -> None:
    path = record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="sldb-close-serve",
        run_dir="runs/subagents/20261029-000000-task-close-serve",
    )
    assert path == tmp_path / "runs/subagents/20261029-000000-task-close-serve/run.md"
    data = extract_model_data(RunDoc, path.read_text(encoding="utf-8"))
    assert data["id"] == "run-sldb-close-serve"
    assert data["task_id"] == "task-close-serve"
    assert data["session_path"] == "scion://agent/sldb-close-serve"
    assert data["outcome"] == "in_progress" and data["ended_at"] == ""
    assert "intent, not proof of start" in data["summary"]
    assert data["tags"] == ["system:deskops", "runtime:scion"]


def test_record_scion_run_never_overwrites_a_previous_attempt(tmp_path: Path) -> None:
    run_dir = "runs/subagents/20261029-000000-task-close-serve"
    record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="deskops-e-abc123abc123",
        run_dir=run_dir,
    )
    original = (tmp_path / run_dir / "run.md").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="immutable"):
        record_scion_run(
            tmp_path,
            task_id="task-close-serve",
            role_id="role-deskops-executor",
            kind="claude",
            agent_slug="deskops-e-abc123abc123-a2",
            run_dir=run_dir,
        )
    assert (tmp_path / run_dir / "run.md").read_text(encoding="utf-8") == original


def _task_payload(**updates) -> dict:
    payload = {
        "id": "task-contract-identity",
        "title": "Identity test task",
        "status": "draft",
        "summary": "",
        "tags": ["workspace:desk", "artifact:task"],
        "current_node": "ritual-execution",
        "history": [],
        "references": ["tests/test_scion_runtime.py"],
        "depends_on": [],
        "pills": [],
        "files": ["deskops/runtime/scion.py"],
        "task_type": "task.code",
        "inherits_from": [],
        "inherit_acceptance_context": False,
        "atoms": [],
        "why": "Test why.",
        "goal": "Test goal.",
        "scope": "Test scope.",
        "implementation_path": "Test implementation.",
        "validation": ["pytest tests/test_scion_runtime.py"],
        "done_when": "The test passes.",
    }
    payload.update(updates)
    return payload


def _write_task(tmp_path: Path, name: str, **updates) -> Path:
    path = tmp_path / f"{name}.md"
    path.write_text(render_model_markdown(TaskDoc, _task_payload(**updates)) + "\n", encoding="utf-8")
    return path


def test_identity_uses_the_canonical_sldb_contract_digest(tmp_path: Path) -> None:
    path = _write_task(tmp_path, "task")
    markdown = path.read_text(encoding="utf-8")
    _, fields = hash_fields_with_map(TaskDoc, markdown)
    expected_contract = contract_hash(TaskDoc, fields)
    expected_name = "deskops-e-" + hashlib.sha256(
        f"task-contract-identity\0{expected_contract}\0executor".encode("utf-8")
    ).hexdigest()[:12]

    identity = scion_child_identity(path, "executor")
    assert identity["contract_sha256"] == expected_contract
    assert identity["name"] == expected_name
    assert identity["labels"] == {
        "deskops.task_id": "task-contract-identity",
        "deskops.contract_sha256": expected_contract[:63],
        "deskops.role": "executor",
        "deskops.attempt": "1",
    }
    assert scion_child_identity(path, "tester")["name"].startswith("deskops-t-")

    attempt_2 = scion_child_identity(path, "executor", attempt=2)
    assert attempt_2["name"] == expected_name + "-a2"
    assert attempt_2["labels"]["deskops.attempt"] == "2"
    for bad in (0, 3, True):
        with pytest.raises(ValueError, match="attempt must be 1 or 2"):
            scion_child_identity(path, "executor", attempt=bad)
    with pytest.raises(ValueError, match="role must be"):
        scion_child_identity(path, "coordinator")


def test_identity_ignores_status_history_and_references_but_moves_with_contract(tmp_path: Path) -> None:
    entry = scion_child_identity(_write_task(tmp_path, "entry"), "executor")
    active = scion_child_identity(
        _write_task(
            tmp_path,
            "active",
            status="active",
            current_node="ritual-testing",
            history=["task_activates"],
            references=["other.md"],
            summary="Different summary",
            tags=["workspace:desk", "artifact:task", "state:changed"],
        ),
        "executor",
    )
    finished = scion_child_identity(
        _write_task(
            tmp_path,
            "finished",
            status="closed",
            current_node="complete",
            history=["task_activates", "task_hands_to_closeout", "task_completes"],
            references=[],
        ),
        "executor",
    )
    assert entry["name"] == active["name"] == finished["name"]
    assert entry["contract_sha256"] == active["contract_sha256"] == finished["contract_sha256"]

    changed_goal = scion_child_identity(_write_task(tmp_path, "goal", goal="A changed goal."), "executor")
    changed_scope = scion_child_identity(_write_task(tmp_path, "scope", scope="A changed scope."), "executor")
    assert changed_goal["name"] != entry["name"]
    assert changed_scope["contract_sha256"] != entry["contract_sha256"]


def test_start_argv_carries_explicit_project_workspace_auth_and_labels(tmp_path: Path) -> None:
    identity = scion_child_identity(_write_task(tmp_path, "task"), "tester")
    argv = scion_start_argv(
        identity,
        prompt="Verify the contract.",
        project="sldb-1",
        workspace="/workspace",
        template="deskops-tester",
    )
    assert argv[:4] == ["scion", "start", identity["name"], "Verify the contract."]
    assert "--type" in argv and argv[argv.index("--type") + 1] == "deskops-tester"
    assert "--project" in argv and argv[argv.index("--project") + 1] == "sldb-1"
    assert "--workspace" in argv and argv[argv.index("--workspace") + 1] == "/workspace"
    assert "--harness-auth" in argv and argv[argv.index("--harness-auth") + 1] == "api-key"
    assert "--non-interactive" in argv
    labels = {argv[index + 1].split("=", 1)[0]: argv[index + 1].split("=", 1)[1] for index, item in enumerate(argv) if item == "--label"}
    assert labels == identity["labels"]


def _context(tmp_path: Path) -> tuple[dict, dict[str, Path]]:
    workspace = tmp_path / "workspace"
    desk_root = workspace / "repo"
    source_root = workspace / "source"
    sldb_root = workspace / "sldb" / "src"
    for path in (desk_root / "desk", source_root / "deskops", sldb_root / "sldb"):
        path.mkdir(parents=True)
    context = {
        "project": "sldb-1",
        "workspace_root": str(workspace),
        "desk_root": str(desk_root),
        "source_root": str(source_root),
        "sldb_root": str(sldb_root),
    }
    return context, {
        "workspace": workspace,
        "desk": desk_root,
        "source": source_root,
        "sldb": sldb_root,
    }


def test_context_emits_environment_volume_and_concrete_examples(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(
        supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude", mode="coordinator", context=context
    )
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["env"] == {
        "DESKOPS_DESK_ROOT": str(paths["desk"]),
        "DESKOPS_SOURCE_ROOT": str(paths["source"]),
        "DESKOPS_SLDB_SOURCE_ROOT": str(paths["sldb"]),
        "DESKOPS_WORKSPACE_ROOT": str(paths["workspace"]),
        "DESKOPS_SCION_PROJECT": "sldb-1",
        "PYTHONPATH": f"{paths['source']}:{paths['sldb']}",
    }
    assert agent["volumes"] == [{"source": str(paths["workspace"]), "target": str(paths["workspace"])}]
    agents = files["agents.md"]
    for fragment in (
        f"--root {paths['desk']}",
        f"--project sldb-1",
        f"--workspace {paths['workspace']}",
        "--type deskops-executor",
        "--type deskops-tester",
        "--harness-auth api-key",
        "--non-interactive",
        "--mode tester",
        "scion_child_identity(task_path, role, attempt)",
    ):
        assert fragment in agents


def test_omitted_context_keeps_the_template_without_env_or_volumes() -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, load_runtime_profiles(ROOT)["claude"], harness="claude")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert "env" not in agent and "volumes" not in agent
    assert "coordinator of the `<repo>` desk" in files["agents.md"]


def test_context_rejects_missing_unknown_relative_and_out_of_workspace_paths(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    assert validate_scion_context(context)["project"] == "sldb-1"

    with pytest.raises(ValueError, match="missing required key"):
        validate_scion_context({key: value for key, value in context.items() if key != "sldb_root"})
    with pytest.raises(ValueError, match="unknown key"):
        validate_scion_context({**context, "secret": "nope"})
    with pytest.raises(ValueError, match="absolute path"):
        validate_scion_context({**context, "desk_root": "repo"})
    with pytest.raises(ValueError, match="inside workspace_root"):
        validate_scion_context({**context, "desk_root": str(tmp_path / "outside")})
    with pytest.raises(ValueError, match="slug or UUID"):
        validate_scion_context({**context, "project": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing desk/"):
        validate_scion_context({**context, "desk_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="containing the deskops package"):
        validate_scion_context({**context, "source_root": str(paths["workspace"])})
    with pytest.raises(ValueError, match="sldb src directory"):
        validate_scion_context({**context, "sldb_root": str(paths["source"])})


def test_load_context_validates_json_and_cli_writes_nothing_on_failure(tmp_path: Path, capsys) -> None:
    context, _ = _context(tmp_path)
    valid = tmp_path / "context.json"
    valid.write_text(json.dumps(context), encoding="utf-8")
    assert load_scion_context(valid)["desk_root"] == validate_scion_context(context)["desk_root"]

    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps({key: value for key, value in context.items() if key != "project"}), encoding="utf-8")
    out_dir = tmp_path / "out"
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(invalid),
    ])
    captured = capsys.readouterr()
    assert code != 0
    assert "missing required key" in captured.out + captured.err
    assert not out_dir.exists()


def test_tester_mode_is_autodetected_and_explicit_mode_wins() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, tester = find_role_doc(ROOT, "role-deskops-tester")
    auto = scion_template_files(tester, profiles["claude"], harness="claude", task_repo="deskops")
    assert "independent tester" in auto["agents.md"]
    assert "## Tester scope" in auto["agents.md"]
    assert "## Completion" in auto["agents.md"]
    assert "You are a deskops executor" not in auto["agents.md"]
    assert "Do not run `deskops closeout`" in auto["agents.md"]

    _, executor = find_role_doc(ROOT, "role-deskops-executor")
    forced = scion_template_files(executor, profiles["claude"], harness="claude", mode="tester")
    assert "independent tester" in forced["agents.md"]
    explicit = scion_template_files(tester, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit["agents.md"]

    id_tester = {"id": "role-x-tester", "name": "custom reviewer", "description": "d", "kind": "claude", "body": "# t"}
    assert "independent tester" in scion_template_files(id_tester, profiles["claude"], harness="claude")["agents.md"]
    not_tester = {"id": "role-x", "name": "tester", "description": "d", "kind": "claude", "body": "# t"}
    assert "You are a deskops executor" in scion_template_files(not_tester, profiles["claude"], harness="claude")["agents.md"]

    id_coordinator = {"id": "role-x-coordinator", "name": "custom lead", "description": "d", "kind": "claude", "body": "# t"}
    coordinator = scion_template_files(id_coordinator, profiles["claude"], harness="claude")
    assert "coordinator of the" in coordinator["agents.md"]
    explicit_executor = scion_template_files(id_coordinator, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in explicit_executor["agents.md"]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def test_coordinator_reconciles_activity_own_lanes_and_reviews_before_dispatch() -> None:
    profiles = load_runtime_profiles(ROOT)
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    agents = _normalized(
        scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")["agents.md"]
    )
    assert "Never answer an executor's or tester's question" not in agents
    for fragment in (
        "activity=completed with phase=running means the child completed",
        "inspect activity=completed first and use phase only as fallback",
        "Reconcile your OWN completed or stopped lane",
        "must not skip your own task",
        "If its preflight or bundle receipt is missing",
        "routine coordinator work, not a human blocker",
        "do not blanket-surface every question",
        "closeout verify --task <id>",
        "--paths <scoped implementation, evidence and review paths>",
        "Never use `git add -A`",
        "Only an actual owner decision uses `ask_user`",
        "sciontool status task_completed",
        "Do not push.",
    ):
        assert fragment in agents, fragment
    assert "/tmp/scion" not in agents


def test_all_three_modes_receive_the_actual_context_roots(tmp_path: Path) -> None:
    context, paths = _context(tmp_path)
    profiles = load_runtime_profiles(ROOT)
    roles = {
        "role-deskops-executor": "executor",
        "role-deskops-tester": "tester",
        "role-deskops-supervisor": "coordinator",
    }
    for role_id, mode in roles.items():
        _, role = find_role_doc(ROOT, role_id)
        files = scion_template_files(role, profiles["claude"], harness="claude", context=context)
        agents = files["agents.md"]
        assert str(paths["desk"]) in agents, mode
        assert str(paths["source"]) in agents, mode
        assert f"cd {paths['desk']}" in agents, mode
        assert "/tmp/scion" not in agents, mode
        agent = yaml.safe_load(files["scion-agent.yaml"])
        assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"]), mode


def test_cli_tester_mode_and_context_file_are_available(tmp_path: Path, capsys) -> None:
    context, paths = _context(tmp_path)
    context_file = tmp_path / "context.json"
    context_file.write_text(json.dumps(context), encoding="utf-8")
    out_dir = tmp_path / "tester-template"
    code = main([
        "runtime", "template", "role-deskops-tester", "--root", str(ROOT),
        "--harness", "claude", "--out", str(out_dir), "--context-file", str(context_file),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "independent tester" in (out_dir / "agents.md").read_text(encoding="utf-8")
    agent = yaml.safe_load((out_dir / "scion-agent.yaml").read_text(encoding="utf-8"))
    assert agent["env"]["DESKOPS_DESK_ROOT"] == str(paths["desk"])


def test_executor_preserves_assigned_run_and_coordinator_commit_boundary(executor, profiles) -> None:
    agents = scion_template_files(executor, profiles["pi"], harness="pi", task_repo="example")["agents.md"]
    assert "Use the exact run_dir assigned by the coordinator" in agents
    assert "preserve its existing RunDoc intent" in agents
    assert "$(date" not in agents
    assert "graph.txt" in agents
    assert "Do not commit or close the task yourself" in agents


def test_omitted_context_keeps_legacy_tool_root_separate_from_task_repo(profiles) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["pi"], harness="pi", task_repo="example")
    assert "cd /workspace/example" in files["agents.md"]
    assert "--root /workspace/deskops" in files["agents.md"]
    assert "env:" not in files["scion-agent.yaml"]


@pytest.mark.parametrize("task_id", ["task-" + "a" * 58, "task-" + "b" * 59, "task-construcción"])
def test_native_labels_fit_scion_without_changing_canonical_identity(tmp_path, task_id) -> None:
    path = _write_task(tmp_path, "native-labels", id=task_id)
    identity = scion_child_identity(path, "executor")
    labels = identity["labels"]
    assert identity["task_id"] == task_id
    assert len(identity["contract_sha256"]) == 64
    assert labels["deskops.contract_sha256"] == identity["contract_sha256"][:63]
    assert len(labels) <= 16
    assert all(len(k) <= 63 and len(v) <= 63 for k, v in labels.items())
    assert all(all(0x20 <= ord(c) <= 0x7E for c in key + value) for key, value in labels.items())
    if len(task_id) <= 63 and task_id.isascii():
        assert labels["deskops.task_id"] == task_id
    else:
        assert labels["deskops.task_id"] == "t-" + hashlib.sha256(task_id.encode()).hexdigest()[:61]
    expected = hashlib.sha256(f"{task_id}\0{identity['contract_sha256']}\0executor".encode()).hexdigest()[:12]
    assert identity["name"] == "deskops-e-" + expected
