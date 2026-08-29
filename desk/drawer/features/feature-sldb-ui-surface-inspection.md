# Feature: SLDB UI Surface Inspection

## Kind

feature

## Status

open

## Problem

Currently, interacting with the different abstraction layers of `sldb` requires switching between the CLI, the filesystem, and mental models. There is no unified, domain-agnostic interface to inspect the raw physical and structural surfaces of a document simultaneously, which slows down debugging and authoring of structured documents. 

## Desired Outcome

Build a minimal, domain-agnostic UI (`sldb-viewer`) that allows a user to view and edit the fundamental work surfaces of the ecosystem in a single dashboard, with zero semantic coupling to specific workflows or specific diagramming logic.

The MVP must strictly expose the following 4 primary `sldb` surfaces for any given instance:

1. **Markdown**: The raw text layer (read/write editor).
2. **AST / Graph**: The parsed structural tree of the markdown (read-only JSON dump).
3. **StructuredDocModel**: The typed Pydantic fields extracted from the AST via templates (read-only JSON dump).
4. **Store**: The `.sldb/` database index (file tree and search).

## Technical Strategy

- **Agnosticism**: The UI must not parse Markdown or extract fields itself. It must act strictly as a client to the `sldb` backend API.
- **Decoupling Alignment**: By treating `AST / Graph` and `StructuredDocModel` as separate UI surfaces, the UI naturally aligns with SLDB's roadmap to decouple AST parsing from field instances (`feature-decoupled-ast-and-field-instances.md`).
- **No Over-engineering**: Do not inject advanced context mapping, dynamic tooltips, or complex rendering pipelines into this phase. Focus solely on dumping the raw data representations of the surfaces into simple UI panels.
