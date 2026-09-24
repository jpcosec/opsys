# Add knowledge drift check routine

## Kind

feature

## Status

open

## Problem

There is no routine that checks whether a change made atoms stale, made materializations stale, or made implementation violate known atoms/specs.

## Desired Outcome

Add a routine or checklist used during testing and closeout that asks which knowledge surface changed and what must be updated or routed.

## Questions

- Should this start as a ritual checklist or a CLI command?
- Which file changes should trigger atom/materialization review?
- Should drift checks block closeout or only create follow-up issues?

## Related Atoms

- atom-drift-checks-compare-atoms-materializations-implementation
- atom-closeout-validates-knowledge-surfaces
- atom-phase-gates-prevent-agent-skipping

---

## Merged item: `integrate-knowledge-surface-checks-into-closeout`

#### Kind

feature

#### Status

open

#### Problem

The closeout ritual checks tests, pills, board cleanup, store cleanup, and commit discipline, but it does not yet explicitly check atom references, materializations, diagram source rules, upstream gaps, source artifact deletion, or git tracking intent.

#### Desired Outcome

Update closeout once the atom reference and materialization conventions exist so every task closes with knowledge surfaces consistent or follow-up work captured.

#### Questions

- Which checks are mandatory gates versus advisory prompts?
- Should closeout require all new atoms to be referenced by at least one materialization or follow-up issue?
- How should untracked files be classified without trampling user work?

#### Related Atoms

- atom-closeout-validates-knowledge-surfaces
- atom-git-is-explanatory-surface-for-changes
- atom-used-source-artifacts-are-deleted

---

## Merged item: `define-self-reflection-loop`

#### Kind

feature

#### Status

open

#### Problem

The current workflow relies on agents noticing gaps and manually turning them into atoms or issues. There is no explicit loop that asks the system to inspect itself, compare artifacts against atoms, and route missing or unclear knowledge.

#### Desired Outcome

Define a repeatable self-reflection ritual or command that reviews recent work, git changes, test failures, user questions, docs, diagrams, atoms, and open issues, then writes new atoms or routed issues where appropriate.

#### Questions

- When should self-reflection run: after every task, on demand, before closeout, or periodically?
- What inputs should it inspect first?
- How does it avoid generating noisy atoms or duplicate issues?
- What validation proves self-reflection improved the knowledge base?

#### Related Atoms

- atom-self-reflection-is-a-feedback-loop
- atom-drift-checks-compare-atoms-materializations-implementation
- atom-promotion-needs-explicit-criteria
