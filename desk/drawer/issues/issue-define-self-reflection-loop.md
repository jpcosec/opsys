# Define self reflection loop

## Kind

feature

## Status

open

## Problem

The current workflow relies on agents noticing gaps and manually turning them into atoms or issues. There is no explicit loop that asks the system to inspect itself, compare artifacts against atoms, and route missing or unclear knowledge.

## Desired Outcome

Define a repeatable self-reflection ritual or command that reviews recent work, git changes, test failures, user questions, docs, diagrams, atoms, and open issues, then writes new atoms or routed issues where appropriate.

## Questions

- When should self-reflection run: after every task, on demand, before closeout, or periodically?
- What inputs should it inspect first?
- How does it avoid generating noisy atoms or duplicate issues?
- What validation proves self-reflection improved the knowledge base?

## Related Atoms

- atom-self-reflection-is-a-feedback-loop
- atom-drift-checks-compare-atoms-materializations-implementation
- atom-promotion-needs-explicit-criteria
