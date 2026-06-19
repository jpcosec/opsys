# Add a repo self-identity document for desk workflows

## Kind

feature

## Status

open

## Problem

A repo can contain many repository artifact docs for examples, tests, or alternate registrations, but there is no explicit desk-local document that says "this desk belongs to this repository identity." Without that, features such as inbox sender inference and local repo self-discovery have to guess from registry entries and path matching.

## Desired Outcome

Introduce a dedicated self-identity document under the desk surface that declares the local repo's canonical identity for operational workflows.

That document should make it possible to answer, without heuristics:

- the repo's canonical ID
- the repo's human name
- the repo root or normalized path
- the owning desk root
- optional links to the canonical ecosystem registration

## Questions

- Should this be a new model such as `DeskIdentityDoc` or `RepositorySelfDoc`?
- Should it live under `desk/registry/`, `desk/meta/`, or another explicit location?
- Should `deskops init` scaffold it, or should `deskops repo register` backfill it?
- Should it be required before cross-repo inbox and promotion commands can run?

## Follow-Up Shape

- Define the self-identity model and path.
- Make inbox sender inference prefer this doc over general repository lookup.
- Validate that the self-identity doc agrees with the canonical SLDB registration when both exist.
- Add a repair path when they diverge.

## Related Atoms

- atom-deskops
- atom-deskops-models-are-sldb-documents
