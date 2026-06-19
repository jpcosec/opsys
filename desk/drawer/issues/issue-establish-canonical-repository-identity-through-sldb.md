# Establish canonical repository identity through SLDB

## Kind

feature

## Status

open

## Problem

Cross-repo workflows currently depend on repository registration and local desk artifacts, but there is no strong canonical identity contract for "who am I?" at the current repo root. That makes sender inference, repo targeting, and ecosystem routing fragile.

The recent inbox check exposed the gap: the sender should have been auto-inferred from the current repo, but multiple local `RepositoryDoc` artifacts mapped to the same path and produced an ambiguous identity. The repo-targeted inbox path also failed for `sldb` because the target repository was not registered in a discoverable canonical registry.

## Desired Outcome

Define one canonical SLDB-backed repository identity path that answers both of these questions reliably:

1. What repository am I in right now?
2. How do I find another repository in the ecosystem?

That identity should be usable by inbox routing, cross-repo desk targeting, task listing across repos, and future workflow federation.

## Questions

- Should the canonical source of truth live only in a central/global SLDB store, or should each repo also keep a local self-registration document?
- Should `deskops init` or `deskops repo register` create or validate that canonical identity automatically?
- How should local `.sldb` identity relate to the global ecosystem registry?
- What uniqueness constraints should exist for repository IDs, roots, and aliases?
- How should tools behave when the current repo has no canonical identity yet?

## Follow-Up Shape

- Define a canonical identity contract for repository discovery.
- Add ambiguity checks for duplicate roots and duplicate IDs.
- Make inbox/repo routing consume that identity contract instead of first-match scanning.
- Add tests for sender inference, self-discovery, and cross-repo routing under duplicate-path conditions.

## Related Atoms

- atom-deskops-models-are-sldb-documents
- atom-deskops-reads-and-writes-through-sldb
