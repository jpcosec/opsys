---
id: feature-doc-materialization-pipeline
status: draft
created: 2026-06-14
tags:
- topic:documentation
- topic:materialization
- topic:atoms
- topic:spec
- topic:proposal
---

# Documentación Auto-generada desde Atoms + Specs

## Propósito

Generar documentación en lenguaje usuario (`docs/`) automáticamente a partir
de atoms de conocimiento + specs de sitio, siguiendo el patrón de progressive
disclosure de Crawl4AI.

El escritor escribe atoms. El sistema compone la documentación.

---

## Arquitectura

```
spec/docs/
  site.yaml                ← árbol de navegación global
  pages/
    quickstart.yaml        ← espec de cada página
    core-concepts.yaml
    ...

atoms/
  atom-desk.md
  atom-tasks.md
  atom-rituals.md
  ...

deskops/materializers/
  __init__.py
  atoms.py                 ← ya existe
  docs.py                  ← NUEVO: orquesta páginas desde atoms
  page_renderer.py         ← NUEVO: renderiza una página con template

docs/                      ← output generado (no editar a mano)
  README.md
  user-guide.md
  core-concepts/
    desk.md
    tasks.md
    ...
```

---

## 1. Site Spec (`spec/docs/site.yaml`)

Define la arquitectura de navegación completa.

```yaml
# spec/docs/site.yaml
site:
  title: deskops User Guide
  tagline: Workflow-domain layer for the hum-ecosystem

  navigation:
    - id: quickstart
      title: Quick Start
      path: quickstart.md
    - id: core-concepts
      title: Core Concepts
      path: core-concepts/index.md
      children:
        - id: concept-desk
          title: What is a Desk?
          path: core-concepts/desk.md
        - id: concept-tasks
          title: Tasks & Boards
          path: core-concepts/tasks.md
        - id: concept-pills
          title: Pills & Context
          path: core-concepts/pills.md
        - id: concept-rituals
          title: Rituals & Routines
          path: core-concepts/rituals.md
        - id: concept-atoms
          title: Atoms & Knowledge
          path: core-concepts/atoms.md
    - id: workflow-guides
      title: Workflow Guides
      path: workflow-guides/index.md
      children:
        - id: wf-execution
          title: How to Execute a Task
          path: workflow-guides/execution.md
        - id: wf-testing
          title: How to Test a Task
          path: workflow-guides/testing.md
        - id: wf-closeout
          title: How to Close a Task
          path: workflow-guides/closeout.md
    - id: reference
      title: CLI Reference
      path: reference/cli.md
```

## 2. Page Spec (`spec/docs/pages/*.yaml`)

Cada archivo define una página: su template, secciones, y cómo resolver
cada sección desde atoms.

### 2.1 Page Spec — Quick Start

```yaml
# spec/docs/pages/quickstart.yaml
page:
  id: quickstart
  template: tutorial            # ver sección 4
  title: Quick Start
  tagline: Your first desk task in 5 minutes
  what_youll_learn:
    - Create your first task
    - Advance it through its routine
    - Test and close it

  sections:
    - id: introduction
      title: What is deskops?
      type: atom_bullets
      bind:
        atom_tag: "system:deskops"
        five_wh: "what"             # usa el campo Answer del atom

    - id: first-task
      title: Your First Task
      type: code_tutorial
      bind:
        atom_tag: "topic:tasks AND topic:create"
        five_wh: "how"
      code_example: |
        deskops add task \
          --title "My first task" \
          --goal "Learn the workflow" \
          --scope "deskops only"
      annotations:
        - "`add task` creates a task bundle with routine, conditions, and checklists"
        - "The `--scope` flag defines what's inside/outside the task"
      callout:
        type: tip
        text: "Run `deskops add task --help` to see all available flags"

    - id: advance-task
      title: Advance the Task
      type: code_tutorial
      bind:
        atom_tag: "topic:routines AND topic:advance"
        five_wh: "how"
      code_example: |
        deskops advance task task-my-first-task
      annotations:
        - "Advance walks the task through its routine state machine"
        - "Each step checks conditions and moves to the next node"
      callout:
        type: important
        text: "Tasks start in draft. You must advance to reach active."

    - id: next-steps
      title: Next Steps
      type: next_steps
      links:
        - text: Core Concepts — What is a Desk?
          ref: core-concepts/desk.md
        - text: Workflow Guide — How to Execute a Task
          ref: workflow-guides/execution.md
```

### 2.2 Page Spec — Core Concept

```yaml
# spec/docs/pages/core-concepts/tasks.yaml
page:
  id: concept-tasks
  template: concept
  title: Tasks & Boards
  tagline: How work is tracked and routed

  sections:
    - id: what-is-a-task
      title: What is a Task?
      type: atom_single
      bind:
        atom_id: atom-tasks
        fields: [answer, tags, see_also]

    - id: task-lifecycle
      title: Task Lifecycle
      type: diagram
      bind:
        atom_tag: "topic:tasks AND topic:lifecycle"
        five_wh: "how"
      mermaid: |
        graph LR
          Draft --> Active --> Testing --> Closed --> Complete

    - id: boards
      title: Boards
      type: atom_single
      bind:
        atom_id: atom-boards
        fields: [answer]

    - id: related
      title: Related
      type: atom_list
      bind:
        atom_tag: "topic:tasks"
        exclude: "atom_id:atom-tasks OR atom_id:atom-boards"
      max_items: 5
```

### 2.3 Page Spec — Workflow Guide (Ritual)

```yaml
# spec/docs/pages/workflow-guides/execution.yaml
page:
  id: wf-execution
  template: how-to
  title: How to Execute a Task
  tagline: The execution ritual, step by step

  sections:
    - id: overview
      title: What You'll Do
      type: atom_bullets
      bind:
        atom_id: atom-execution-ritual
        fields: [purpose, trigger, preconditions]

    - id: step-by-step
      title: Step by Step
      type: ritual_steps
      bind:
        atom_tag: "topic:execution-ritual AND topic:steps"
      ritual_ref: desk/rituals/execution.md

    - id: validation
      title: How to Validate
      type: checklist
      bind:
        atom_tag: "topic:execution-ritual AND topic:validation"

    - id: failure-modes
      title: What Can Go Wrong
      type: atom_bullets
      bind:
        atom_tag: "topic:execution-ritual AND topic:failure-modes"

    - id: next-steps
      title: Next Steps
      type: next_steps
      links:
        - text: How to Test a Task
          ref: workflow-guides/testing.md
```

## 3. Templates (`deskops/materializers/page_renderer.py`)

Cada template define cómo se renderiza una página completa.

### Templates identificados

| Template | Para qué | Secciones típicas |
|---|---|---|
| `tutorial` | Primeros pasos numerados | intro, code_tutorial × N, next_steps |
| `concept` | Explicación de un concepto | atom_single, diagram, atom_list, related |
| `how-to` | Guía paso a paso de un ritual | atom_bullets, ritual_steps, checklist, failure_modes |
| `reference` | Referencia técnica (CLI, API) | atom_list, code_block, table |
| `landing` | Página índice de una categoría | atom_list con summaries |

### Composición de secciones

Cada sección tiene un `type` que define cómo se renderiza:

| Section type | Renderiza |
|---|---|
| `atom_single` | Un atom específico (por id) con campos seleccionados |
| `atom_bullets` | Lista de atoms (por tag) como bullets, cada uno con Answer |
| `atom_list` | Lista de atoms con título + link |
| `code_tutorial` | Bloque de código + annotations inline + callout opcional |
| `diagram` | Mermaid block, resuelto desde atom o literal |
| `ritual_steps` | Pasos de un ritual renderizados como lista numerada |
| `checklist` | Items de validación renderizados como checklist |
| `next_steps` | Lista de links a páginas siguientes |
| `table` | Tabla renderizada desde fields de atoms |

## 4. Materializer (`deskops/materializers/docs.py`)

### Algoritmo

```python
def materialize_docs(site_spec_path, atom_store, output_dir):
    # 1. Load site spec
    site = load_yaml(site_spec_path)

    # 2. Load all page specs
    pages = [load_page_spec(p) for p in site.navigation]

    # 3. For each page:
    for page_spec in pages:
        # 3a. Resolve atoms for each section
        for section in page_spec.sections:
            atoms = query_atoms(atom_store, section.bind)
            section.resolved_atoms = atoms

        # 3b. Select template
        renderer = get_template(page_spec.template)

        # 3c. Render page
        output = renderer.render(page_spec)

        # 3d. Write to docs/
        write_page(output_dir, page_spec.path, output)

    # 4. Generate index / sidebar
    generate_index(site, output_dir)
```

### Queries de atoms

El `bind` en cada sección soporta:

```yaml
bind:
  atom_id: atom-tasks              # atom específico
  atom_tag: "topic:tasks"          # por tag (soporta AND, OR, NOT)
  five_wh: "what"                  # filtro por tipo de pregunta
  fields: [answer, tags]           # qué campos incluir
  exclude: "atom_id:atom-tasks"    # excluir atoms específicos
  max_items: 5                     # límite
```

## 5. Comando CLI

```bash
# Generar docs completa
deskops materialize docs

# Sobre escribir docs/ existente
deskops materialize docs --force

# Solo páginas específicas
deskops materialize docs --pages quickstart,concept-tasks

# Modo watch (regenera en cada cambio de atom o spec)
deskops materialize docs --watch
```

## 6. Pipeline completo

```
[Escribo atom]             → atoms/atom-tasks.md
[Escribo spec de página]   → spec/docs/pages/concept-tasks.yaml
[Ejecuto materialize]      → deskops materialize docs
[Output]                   → docs/core-concepts/tasks.md ← generado
                              docs/_sidebar.md ← generado
                              docs/README.md ← generado
```

El resultado es que **la documentación se auto-genera** a partir de:

1. **Atoms** → el conocimiento puro (5WH1+)
2. **Site spec** → la arquitectura de navegación
3. **Page specs** → qué atoms van en cada sección y cómo se renderizan
4. **Templates** → cómo se ve cada tipo de página (crawl4ai-style)

El escritor solo toca atoms y specs. El materializador compone el docs site.

---

## 7. Lo que hay que construir

### 7.1 Specs nuevos

- [ ] `spec/docs/site.yaml` — arquitectura de navegación
- [ ] `spec/docs/pages/` — specs de página por concepto
- [ ] Registrar `DocSiteSpec` y `DocPageSpec` como modelos sldb

### 7.2 Materializers nuevos

- [ ] `deskops/materializers/docs.py` — orquestador principal
- [ ] `deskops/materializers/page_renderer.py` — templates + section renderers
- [ ] `deskops/materializers/site_index.py` — generación de sidebar + index

### 7.3 CLI

- [ ] `deskops materialize` — comando nuevo
- [ ] `deskops materialize docs` — subcomando
- [ ] Soporte `--watch`, `--pages`, `--force`

### 7.4 Queries

- [ ] Extender sistema de queries de atoms para soportar bind DSL
- [ ] Resolución por `atom_id`, `atom_tag`, `five_wh`, `fields`

---

## 8. Open Questions

- ¿Los templates deberían ser spec YAML o código Python? (Python da flexibilidad para render, YAML permite cambiar sin deploy)
- ¿El sidebar se genera del site spec o se escribe a mano?
- ¿Los docs generados se versionan en git o se reconstruyen siempre?
- ¿Cómo se maneja la internacionalización? (atoms en ES + EN → docs en ambos idiomas)
- ¿Los rituales actuales en `desk/rituals/` deberían tener una versión atomizada para que el materializador los consuma?
