# Add a desk update command to sync desk structure across projects

## Kind

feature

## Status

open

## Problem

`deskops desk install` scaffolds an initial desk surface, but there is no explicit follow-up command to reconcile existing repos with newer desk structure, starter docs, or workflow conventions. That leaves projects drifting after install and encourages manual copy-paste updates.

The gap is especially visible in multi-repo ecosystems: once rituals, pills, or required structural surfaces evolve, there is no first-class way to propagate safe desk updates across sibling repos.

## Desired Outcome

Provide a dedicated update/sync command that compares a target repo's current desk surface against the current scaffold or policy contract and applies safe, reviewable updates.

Possible command shapes:

- `deskops desk update <path>`
- `deskops desk sync <path>`
- `deskops init --update`

## Questions

- Should the command only add missing structural surfaces, or also update existing starter docs?
- How should it distinguish user-owned desk content from generated/scaffolded content?
- Should updates be patch-based, model-based, or spec-driven?
- Should it support dry-run, diff preview, and selective adoption?
- How should it interact with local customizations and project-specific pills/rituals?

## Follow-Up Shape

- Define the desk scaffold contract that can be compared over time.
- Mark which scaffold artifacts are upgradeable vs user-owned.
- Add a dry-run/report mode before mutation.
- Add tests for upgrading older desk installs without overwriting project content.

## Related Atoms

- atom-deskops
- atom-phase-gates-prevent-agent-skipping
