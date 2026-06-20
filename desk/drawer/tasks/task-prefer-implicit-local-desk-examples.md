# Prefer implicit local-desk examples in docs

ID: task-prefer-implicit-local-desk-examples
Status: deferred
Priority: medium

## Goal

Update operator-facing guidance so commands run from the repo root prefer the implicit local-desk default instead of spelling `--root .` everywhere, while keeping explicit-root examples where cross-repo, sandbox, or unusual targeting matters.

## Scope

- adjust local-repo examples in README/docs/agent guidance
- keep explicit `--root` only where override behavior is the point
- preserve clarity for graph, cross-repo, and sandbox guidance where explicit targeting still helps

## Suggested Pills

- `desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md`
- `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md`
- `desk/contexts/pill-cli-gaps-become-tracked-work.md`

## Done When

- local-repo examples prefer implicit local-desk commands
- explicit `--root` remains only where it carries real meaning
- validation passes and the task closes with its own commit
