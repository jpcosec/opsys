"""A throwaway repo for one scenario, isolated from the machine.

`HOME` points inside the sandbox, so `deskops bootstrap` builds its global store there and never
touches the real `~/.sldb`; pi keeps its own config through `PI_CODING_AGENT_DIR`. Git identity
comes from the environment because the fake home has no `.gitconfig`.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Sandbox:
    root: Path   # the repo the agent works in
    home: Path   # its HOME

    def env(self) -> dict[str, str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith(("DESKOPS_TEST_ROOT", "VIRTUAL_ENV_PROMPT"))}
        env.update({
            "HOME": str(self.home),
            "XDG_CACHE_HOME": str(self.home / ".cache"),
            "PI_CODING_AGENT_DIR": os.environ.get("PI_CODING_AGENT_DIR", str(Path.home() / ".pi" / "agent")),
            "GIT_AUTHOR_NAME": "e2e agent", "GIT_AUTHOR_EMAIL": "e2e@example.invalid",
            "GIT_COMMITTER_NAME": "e2e agent", "GIT_COMMITTER_EMAIL": "e2e@example.invalid",
        })
        return env

    def sh(self, command: str, timeout: int = 300) -> subprocess.CompletedProcess[str]:
        """Run one shell command in the repo, the way the agent's bash tool would."""
        return subprocess.run(["bash", "-c", command], cwd=self.root, env=self.env(), capture_output=True, text=True, timeout=timeout)


def make_sandbox(base: Path | None = None) -> Sandbox:
    top = Path(tempfile.mkdtemp(prefix="deskops-e2e-", dir=base))
    root, home = top / "repo", top / "home"
    root.mkdir()
    home.mkdir()
    return Sandbox(root=root, home=home)


def run_steps(box: Sandbox, steps: list[str], what: str) -> None:
    """Run setup or reference commands; the first that fails raises with its output."""
    for step in steps:
        done = box.sh(step)
        if done.returncode != 0:
            raise RuntimeError(f"{what} step failed ({done.returncode}): {step}\n{done.stdout}\n{done.stderr}")


def run_checks(box: Sandbox, checks) -> list[dict]:
    results = []
    for check in checks:
        done = box.sh(check.run)
        results.append({"name": check.name, "run": check.run, "ok": done.returncode == 0, "output": (done.stdout + done.stderr)[-800:]})
    return results
