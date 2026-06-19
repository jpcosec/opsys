# Fix inbox sender project resolution against ambiguous local repository docs

## Kind

bug

## Status

open

## Problem

`deskops inbox` should infer `sender_project` from the source repository automatically, but the current resolution path can pick the wrong repository identity when multiple `RepositoryDoc` entries map to the same physical root.

In this repo, several local repository docs under `desk/registry/` point to `path: .`, so `_sender_project()` matches the current working directory against multiple candidates and returns the first one loaded from the store. In a live check from the `deskops` repo, a cross-repo inbox note written into `../sldb/desk` was created with `sender_project: myrepo` instead of `sender_project: deskops`.

## Evidence

- Source logic: `deskops/cli/commands/inbox.py`, `_sender_project()`
- The current algorithm scans tracked `RepositoryDoc` payloads and returns the first doc whose `path` contains the current working directory.
- Multiple docs in `desk/registry/` currently resolve to the same root (`path: .`), including `myrepo`, `my-repo`, `described-repo`, `deskops`, and others.
- Reproduced from `/home/jp/proyectos/hum-ecosystem/tools/deskops` while targeting `../sldb/desk` via `deskops inbox ... --desk-root ../sldb/desk`.

## Desired Outcome

Inbox sender inference should resolve to one canonical identity for the source repo, or fail clearly when identity is ambiguous, instead of silently picking the first matching repository doc.

## Questions

- Should sender inference require one canonical self-registration per repo?
- Should repository docs that point to the same root be allowed at all?
- If multiple matches exist, should inbox refuse to write until the ambiguity is resolved?
- Should sender inference prefer a dedicated self-identity doc over generic repository artifact docs?

## Related Atoms

- atom-code-changes-close-with-tests-and-commit
