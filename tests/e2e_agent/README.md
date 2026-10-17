# Agent e2e suite

A cheap agent (pi + DeepSeek Flash) uses deskops in a throwaway repo, knowing only the docs a
scenario hands it. The suite answers two questions separately:

1. **Does what has to work, work?** The harness judges with shell checks after the agent ends
   (git log, `desk/tasks`, `sldb stores check`, ...), never with the agent's own word. Each
   scenario also carries a reference solution; `test_reference_solutions` runs it with no LLM in
   the normal suite, and `test_checks_need_the_work` makes sure the checks do not hold after
   setup alone.
2. **Are the docs good enough?** The agent ends with a JSON report: the steps it took, which doc
   section it followed for each, and every friction point, classified as in
   `docs/how-to-test-ux-cli.md`. The harness adds what it measures from pi's event stream:
   failed commands, `--help` probing, and reads of deskops/sldb source (the docs were not enough).

A scenario passes when the checks hold (**works**) and the agent completed it from the docs,
with no `blocker` friction, at most `max_major_friction` (default 0) `major` ones, no source
reads beyond `max_source_reads`, and within its time and cost budget (**docs ok**).

## Running

```bash
python -m tests.e2e_agent --reference            # reference solutions only, no LLM
python -m tests.e2e_agent                        # every scenario with the agent
python -m tests.e2e_agent first-task-to-closeout --keep   # one scenario, keep the sandbox
python -m tests.e2e_agent --model openrouter/'~z-ai/glm-flash-latest'
DESKOPS_AGENT_E2E=1 pytest tests/e2e_agent       # the same, as tests
```

Each agent run writes `runs/e2e/<timestamp>-<scenario>/`: `summary.md` (read this),
`result.json` (verdict, metrics, checks, the agent's report, every command) and
`events.jsonl` (pi's raw event stream, not versioned).

A run costs a few cents with `deepseek/deepseek-flash`; each scenario stops at its
`max_cost_usd` (default $0.25) or `timeout_s` (default 900).

## Isolation

The sandbox is a fresh git repo under `/tmp`, with its own `HOME`, so `deskops bootstrap` builds
its global store there and never touches the real `~/.sldb`. pi keeps its configuration through
`PI_CODING_AGENT_DIR`. The agent runs with `--no-skills --no-context-files --no-extensions`: it
sees only the scenario's docs, attached to the prompt.

## Writing a scenario

`scenarios/<id>.yaml`:

- `intent`: what the user wants, in the user's words. Name outcomes, never commands.
- `docs`: repo-relative files attached to the prompt (what a newcomer would be pointed to).
- `setup`: shell steps that build the starting state.
- `reference`: a known-good solution with the documented commands.
- `checks`: `{name, run}`; each holds when `run` exits 0 in the sandbox.
- optional `max_cost_usd`, `timeout_s`, `max_source_reads`, `max_major_friction`.
