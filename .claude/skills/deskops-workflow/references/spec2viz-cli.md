# spec2viz CLI reference

Captured from `spec2viz --help` and per-subcommand `--help`. Run `spec2viz <command> --help` (or
`spec2viz <group> <command> --help`) to confirm current flags before relying on this file.

Taxonomy: `diagram` (semantic diagram specs: render, validate, schema, lint, generate) and
`catalog` (HTML bundles / hierarchical diagram stores: build, schema, serve). Legacy flat
commands (`spec2viz render`, `spec2viz validate`, `spec2viz schema`, `spec2viz lint`) remain as
aliases for the `diagram` subcommands — prefer the `diagram ...` / `catalog ...` form in new work.

## Diagram specs

- `spec2viz diagram validate <spec.yml> [<spec2.yml> ...]` — validate one or more diagram specs
  against their Pydantic models before rendering.
- `spec2viz diagram render <spec.yml> [<spec2.yml> ...] --out <dir> \
  [--renderer|--backend plantuml|mermaid|vega|d2|antonia-html|tree|graph|json]`
  Renders to `--out` (default `.`). Omit `--renderer` to use the spec type's default renderer.
  Diagram types: sequence, state, component, activity, deployment, matrix, ast.
- `spec2viz diagram schema [--type sequence|state|component|activity|deployment|matrix] [--out <file>]`
  Export JSON Schema for one diagram type or all of them (writes to stdout without `--out`).
- `spec2viz diagram generate` — generate a component spec from Python source AST (reverse
  direction: code -> spec, useful for bootstrapping a spec from an existing codebase).
- `spec2viz diagram lint <spec-or-mmd> [...]` — lint rendered Mermaid for browser-breaking syntax.

## Catalogs (aggregating many diagrams into one browsable HTML)

- `spec2viz catalog build --config <vistas.yml-or-diagram-store.yml> --out <out.html> \
  [--base-dir <dir>] [--atoms-dir <dir>]`
  Builds one HTML bundle from either a legacy `vistas.yml` registry or a hierarchical
  `diagram-store` config. `--base-dir` resolves relative template/vista paths (defaults to the
  config file's directory). `--atoms-dir` injects W5H1 atom Markdown files into the page as
  `window.ATOMS_DB` so the catalog can cross-link diagrams to atoms.
- `spec2viz catalog schema [--out <file>]` — JSON Schema for diagram-store / `project.yml` configs.
- `spec2viz catalog serve` — serve a built catalog locally with auto-save for viewer annotations
  (annotations persist to a JSON file next to the catalog build output).

A hierarchical diagram-store config can itself aggregate other stores and legacy `vistas.yml`
leaves, then expose one catalog filterable by category/type/project/tags. Minimal shape:

```yaml
diagram_store:
  kind: diagram-store
  template: template.html   # keep this; do not create a local template.html unless overriding on purpose
  title: <Catalog Title>
  brand_name: <Brand>
  brand_subtitle: <Subtitle>
  project_name: <project path>
  stores:
    - path: <path to a vistas.yml or nested diagram-store>
      project: <project path>
      tags: [domain:example]
```

When `template.html` is absent, spec2viz falls back to its built-in template; when present it
prints a warning that a local override is active — only create one deliberately.

## Renderer-specific styling

Component diagrams may carry `style.kinds.<kind>.plantuml.{background,border,font}` in the YAML
to control PlantUML colors per semantic `kind`, without polluting `kind` itself with rendering
concerns. Omitting `style.kinds` falls back to the built-in palette for `core`/`boundary`/
`database`. This currently applies to PlantUML component rendering only.

## Python API (when a script needs this instead of the CLI)

```python
from spec2viz import compile_ir, load, render, validate, render_to_file, json_schema, write_json_schema

diagram = load("path/to/spec.yml")
validate(diagram)
ir = compile_ir(diagram)
output = render(ir)

# or, write straight to disk:
path = render_to_file("path/to/spec.yml", out="out")
```

## Legacy aliases (still work, prefer the `diagram`/`catalog` form above)

- `spec2viz render <spec.yml> --out <dir> [--renderer ...]` == `spec2viz diagram render`
- `spec2viz validate <spec.yml>` == `spec2viz diagram validate`
- `spec2viz schema [--type ...] [--out ...]` == `spec2viz diagram schema` (also accepts
  `--type diagram-store` for catalog schema, unlike the `diagram schema` form)
- `spec2viz lint <spec-or-mmd>` == `spec2viz diagram lint`
- Historical rename: the project used to be `yaml-charts` / `yaml_charts`; that CLI and import
  path still resolve with a deprecation warning. Never introduce new `yaml_charts` usage.
