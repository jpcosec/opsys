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

---

## Merged item: `add-repo-self-identity-document`

#### Kind

feature

#### Status

open

#### Problem

A repo can contain many repository artifact docs for examples, tests, or alternate registrations, but there is no explicit desk-local document that says "this desk belongs to this repository identity." Without that, features such as inbox sender inference and local repo self-discovery have to guess from registry entries and path matching.

#### Desired Outcome

Introduce a dedicated self-identity document under the desk surface that declares the local repo's canonical identity for operational workflows.

That document should make it possible to answer, without heuristics:

- the repo's canonical ID
- the repo's human name
- the repo root or normalized path
- the owning desk root
- optional links to the canonical ecosystem registration

#### Questions

- Should this be a new model such as `DeskIdentityDoc` or `RepositorySelfDoc`?
- Should it live under `desk/registry/`, `desk/meta/`, or another explicit location?
- Should `deskops init` scaffold it, or should `deskops repo register` backfill it?
- Should it be required before cross-repo inbox and promotion commands can run?

#### Follow-Up Shape

- Define the self-identity model and path.
- Make inbox sender inference prefer this doc over general repository lookup.
- Validate that the self-identity doc agrees with the canonical SLDB registration when both exist.
- Add a repair path when they diverge.

#### Related Atoms

- atom-deskops
- atom-deskops-models-are-sldb-documents
