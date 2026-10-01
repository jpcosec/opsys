# Issue: ecosystem desk sweep — repaired, pushed, and still pending

## Kind

issue

## Status

open

## Evidence

A sweep across the 39 desks under `/home/jp/proyectos` raised the healthy count
from 6 to 30. Verified per desk with `deskops doctor` plus
`sldb stores check --store .sldb`.

Pushed and healthy:

- `tools/deskops` (`cff4f30`) — 6 atoms carried the AtomDoc instruction line
  *inside* their own answer; 3 rituals and 2 drawer tasks had the opposite gap.
  Also removed a store shard pointing at a file in another repo by absolute path.
- `humble/Cotizador` (`ed04084`) — 58 ontology atoms folded into the single
  field AtomDoc models, 37 tasks moved onto `atoms`/`files`/`Scope`, 663
  generated primitives anchored. 931 documents, store PASS.
- `tools/repopackage` (`a7d9587`) — 19 tasks renamed onto TaskDoc fields; 2
  pills folded 4 undeclared sections into How and moved `## Tags` to the field.
- `tools/graph_ui` (`12dece7`) — 6 tasks renamed; `## Status` dropped only where
  it already agreed with the field; `Validation` is `list[str]`, so its prose
  line became a bullet.
- `matrix-shrdlu-spec` (`f13c67d`) — store migrated from monolithic indexes to
  per-model shards; one pill's undeclared `## Summary` had shifted every field
  by one position.

Earlier in the same sweep: 15 legacy 2026-06-02 briefs became 75 atoms plus
preserved `desk/briefs/` prose; ~295 documents had placeholder text left inside
extracted content; ~236 had stale hashes because shards without `field_hashes`
never recompute `content_hash`.

## Problem

Most desks were not unhealthy by accident: they carried knowledge their models
could not read. Three recurring drifts explain nearly every finding.

**Missing instruction anchors.** A template puts an italic instruction line
between a heading and the field content, and the extractor anchors on it. A
document written as heading + prose extracts that field as empty, so an edit
through the model renders the section back blank and erases it.

**Local field vocabulary.** Desks invented section names for fields that already
exist: `Objective` for Goal, `What to Fix` for Scope, `Governing Atoms` for the
`atoms` list, `Pills` for `pills`, `Location` for `files`, `## Status` for the
`status` field. A missing *intermediate* template section is worse than a
renamed one: the extractor then slides every later field into the previous one,
silently.

**Undeclared headings.** SLDB refuses headings a template does not declare, at
every level — `###` is rejected just like `##`. Where there is no stable shape
to declare, the content must live inside a declared field; bold lead-in text is
what admits it.

## Pending

1. **No git remote** — `humble/humble-framework`, `hum-ecosystem`,
   `hum-ecosystem/core/code2specyaml`, `hum-ecosystem-worktrees/pm-surface`,
   `hum-ecosystem-worktrees/sldb-ui`. Work is committed locally where it was
   done, but there is nothing to push to. `humble-framework` still needs 16
   tasks with lowercase `## Done when` and 54 atoms with no frontmatter;
   `code2specyaml` still reports unreadable fields.
2. **Legacy desks awaiting the sldb layout fix** — `hum-core`, `hum-scrapper`,
   `gemini_test/tests/knowledge`. `migrate_store_layout` dies before migrating
   because `load_store_index` only reads `core/store_index.yaml` and raises
   `FileNotFoundError` on the legacy layout. Routed to the sldb inbox; the local
   sldb tree already carries a fix commit, so retry these after it lands.
3. **`pills.md` index files inside the modeled `contexts/` directory** — 7
   repos. They are indexes, not pills, so the directory model rejects them.
   They need to move out rather than be forced into PillDoc; not touched.
4. **Domain-mismatched stores, deliberately untouched** — `hum-core` (a
   `wiki_compiler` TaskDoc) and `pm-surface` (an `ecosystem_inventory` store).
   Same model names, different domains; repairing them from here would be
   guessing.
5. **`gemini_test`** — has a remote and 21 unpushed commits predating this
   sweep, and still reports unreadable fields. Left alone: that backlog is not
   this sweep's to publish, so its desk repair should be a task of its own.

## Notes

Repair rule used throughout: dry-run first, write only when the model reads the
content back, and diff against a pre-change backup so no atom id, path or rule
is lost. Prose was never rewritten, only moved. In repopackage an apparent
122-token loss turned out to be backticked paths that had moved into frontmatter
lists; re-checking without the backticks showed zero real loss.

The repair scripts and the pre-change task backups are kept outside the repos at
`~/.local/share/desk-audit/`.

Items 1 and 3 need a decision, not a repair: whether those repos get remotes,
and where `pills.md` indexes should live relative to the modeled `contexts/`
directory. Item 4 should stay untouched until the owning domain is identified.
