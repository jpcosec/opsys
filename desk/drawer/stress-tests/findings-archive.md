# Stress-test findings archive

All 28 finding files from the six UX rounds, concatenated on 2026-09-24.
The fixes that came out of them are tracked in
`desk/drawer/issues/issue-stress-test-fix-backlog.md`.


---

## Round 01 — Graph knowledge inconsistencies

**Source:** ST-03, ST-04

### Node IDs vs CLI expectations

- `graph neighbors atom-deskops` → `Error: graph node not found`
- `graph neighbors atom:atom-deskops` → funciona. Pero el usuario no sabe del prefijo `atom:`.
- El error no sugiere formatos válidos ni lista prefijos disponibles.

### Cero edges en nodos atom

- 253 nodos en total, 68 edges.
- Metadata es correcta (`node_count: 253`, `edge_count: 68`).
- Sin embargo, **todos los nodos `atom:*` tienen 0 edges**.
- Los 68 edges están en nodos con prefijos: `diagram:`, `doc:`, `source_file:`, `config_file:`, `issue:`, `spec:`, `test_file:`.
- Las conexiones semánticas entre átomos (declaradas en el contenido markdown) no se materializan como edges.

### graph missing

- Funciona correctamente: encontró una referencia dangling, muestra provenance con archivo:línea.
- El output es legible y accionable.

### graph build

- Es idempotente: rebuild produce exactamente los mismos 253 nodos y 68 edges.
- No hay indicación de progreso durante el build (silencioso hasta el final).


---

## Round 01 — Inbox capture friction

**Source:** ST-02

### Slugification pierde información

- `deskops inbox "¿Cómo va?"` → filename `...-como-va`
- `deskops inbox "ñandú > 100º"` → filename `...-and-100`
- `deskops inbox "test con ñ, ¿, símbolos: -> <html> </html>"` → filename `...-test-con-caracteres-s-mbolos-html-html`
- Caracteres UTF-8 se pierden en la conversión a slug. El filename no es representativo del contenido.

### Input largo = filename inservible

- 5000 caracteres de largo producen filename con 68 `a`s consecutivas y un sufijo `-unclear`.
- No hay forma de referenciar esa nota después sin buscar por contenido.

### Sin detección de duplicados

- Mismo mensaje dos veces → dos archivos independientes con distinto timestamp.
- No hay advertencia de duplicado.

### Default kind silencioso

- `deskops inbox "mensaje"` (sin `--kind`) crea nota con `kind: unclear`.
- El usuario no sabe que `--kind suggestion` o `--kind question` existen a menos que lea `--help`.

### --show no visible en --list

- `deskops inbox --list` muestra notas pero no sugiere que `--show <id>` existe para ver detalle.
- El usuario tiene que saber del flag por `--help`.


---

## Round 01 — Nomenclature & command gaps

**Source:** ST-01, ST-02, ST-05, ST-07, ST-14

### Commands que no existen (pero las atoms los describen)

| Concepto en atoms | Realidad CLI | Brecha |
|---|---|---|
| drift check | no existe | No hay comando `drift` ni top-level ni subcommand |
| materialize | no existe | No hay comando |
| status / health | no existe | No hay comando |
| closeout | no existe | No hay comando |
| validate | no existe | No hay comando |
| graph reflect | no existe | `graph` solo tiene `build`, `neighbors`, `missing` |
| atoms list | no existe | `list atoms` sí, pero `atoms list` no |
| atoms show | no existe | `show atom` sí, pero `atoms show` no |
| atoms new / validate / split / merge / deprecate | no existen | `atoms` solo tiene `add-namespace` |
| repo list | no existe | `repo` solo tiene `register` |

### Inconsistencias plural/singular

- `list` usa plural: `list tasks`, `list atoms`, `list pills`
- `show` usa singular: `show task`, `show atom`, `show pill`
- `add` usa singular: `add task`, `add atom`
- `advance` usa singular: `advance task`

Esto es consistente internamente pero puede confundir: `list tasks` funciona, `tasks list` no.

### Comandos medio implementados

- `advance task <id>` no acepta `--to` — el flag no existe. No se puede especificar el estado destino.
- `repo register` falla con error de modelo no registrado en store — el setup tiene un paso manual no resuelto.

### Átomos no cubiertos

- `list atoms` solo muestra 4 átomos (raíz de `desk/atoms/`). Los 60 átomos en `knowledge-model/` y `workflow-model/` no aparecen.
- `show atom <id>` solo encuentra los 4 de raíz.


---

## Round 02 — Artifact inventory and show/add quality

**Source:** ST-11

### Qué tiene datos vs qué está vacío

| Artifact | Items | Notas |
|---|---|---|
| pills | 11 | Datos completos con campos what/why/when/where/how/how_not |
| atoms | 4 | Solo los de raíz, no los 60 anidados |
| repositories | 1 | `repo-deskops` |
| inbox-notes | 2 | |
| steps | 1 | `step-document-the-cli` |
| tasks, routines, conditions, operators, checklists, hooks, edges, rituals, boards, faq-docs | 0 | Modelados en el parser pero sin archivos de datos |

### Pill show

Funciona para los 11. Output verboso pero completo con todos los campos del spec.

### Step show

Funciona. Renderiza campos `action` y `outcome`.

### Repository show

Funciona. Renderiza name/path/status/description.

### Add pill

Crea archivo en `desk/contexts/` (no `desk/pills/`). Imprime path. Slug se genera del `--title`.

### Add flags

Cada `add` subcomando tiene sus propios flags (`--what`, `--why` para pill; `--purpose`, `--trigger` para ritual; etc.). No hay base común (ni `--title` compartido). Todos soportan `--from-yaml` para batch loading.


---

## Round 02 — CLI integration readiness

**Source:** ST-15

### Exit codes

| Escenario | Exit | Veredicto |
|---|---|---|
| `deskops about` | 0 | ✅ |
| `deskops nonexistent` | 2 | ✅ |
| `deskops show` (missing subcommand) | 2 | ✅ |
| `deskops` (sin args) | 2 | ✅ |
| `list atoms --root /nonexistent` | 0 | ⚠️ **root sin validación** |

El CLI es disciplinado con exit codes. Usa `argparse` consistentemente. **Pero** `--root` acepta cualquier path sin validar — esto es una trampa en CI.

### Output formats

- Solo `inbox --list` soporta `--format {text,json,yaml}`
- Ningún otro comando tiene `--format` o `--json`
- No hay `--ci` flag en ningún comando
- No hay `--version` flag
- No hay `--verbose` flag

### ANSI / colores

No hay códigos ANSI en ningún output. Texto plano. **Excelente para CI logs**, pero la experiencia en terminal es plana.

### Pipeline safety

- stderr/stdout están limpios y separados
- Piping funciona sin artefactos
- Redirección a archivo es limpia

### --root sin validación

`deskops list atoms --root /tmp` → exit 0, sin output, sin error. El usuario cree que funcionó pero no encontró nada. En CI esto es una falla silenciosa.

### Resumen

El CLI es **CI-safe** (texto plano, exit codes correctos, stderr/stdout separados) pero **no CI-friendly** (solo un comando soporta JSON, no hay `--version`, no hay `--ci`, `--root` no se valida).


---

## Round 02 — Edge cases and error quality

**Source:** ST-12

### --root validation

| Comando | Root inválido | Comportamiento |
|---|---|---|
| `list atoms --root /tmp` | Dir sin desk | Exit 0, sin output, sin error |
| `graph build --root /tmp` | Dir sin desk | Crea `.sldb/runtime/knowledge_graph.kg.json` adentro de `/tmp` — contamina el filesystem |
| `graph build --root /tmp/vacio` | Dir vacío | Crea estructura `.sldb` igual |
| `list atoms --root "/path with spaces"` | Path con espacios | Exit 0, sin output, sin error |

Ningún comando valida que `--root` apunte a un directorio con estructura de desk. `graph build` es especialmente peligroso porque **crea** estructura sldb donde sea.

### add task sin args

```
deskops add task
```
→ dump de Pydantic validation error (traceback crudo). El usuario ve un error interno de Python en vez de un mensaje amigable.

En cambio:
- `deskops add pill` → funciona, auto-genera `pill-none.md`
- `deskops add routine` → funciona, auto-genera `routine-none.md`

`add task` es el único que explota.

### add pill va a desk/contexts/ no desk/pills/

```
deskops add pill --title test-pill
→ desk/contexts/test-pill.md
```

El usuario esperaría `desk/pills/`. El `list pills` lee de `desk/contexts/` así que el comando y el listado son consistentes entre sí, pero el nombre del directorio contradice la intuición.

### Partial commands

Todos los comandos con subcomandos (`graph`, `atoms`, `repo`, `desk`) se comportan igual: exit 2 con `required argument` y lista de choices. Consistente.

### Vague show

Todos los `show <kind>` sin ID dan el mismo error argparse genérico: `error: the following arguments are required: <id>`. Funcional pero sin hint de qué IDs existen.


---

## Round 02 — Repo subsystem half-built

**Source:** ST-13

### Lo que existe

- `repo register <name> <path>` con flags `--id`, `--description`, `--tags`, `--store`, `--pythonpath`
- Modelo `RepositoryDoc` definido en `deskops/models.py` con campos: name, id, path, status, description, tags
- Output escribe archivo YAML en el store local

### Lo que NO existe (ni en parser ni en handler)

| Comando | Estado |
|---|---|
| `repo list` | No existe |
| `repo current` | No existe |
| `repo switch` | No existe |
| `repo unregister` | No existe |

### Modelo sin registrar en store

`repo register` falla con:
```
Error: RepositoryDoc model is not registered in the store.
Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>
```

El modelo existe como clase Python pero falta el bootstrap en sldb. El error es claro y da la solución, pero requiere un paso manual fuera de deskops.

### Error quality

Los errores de `argparse` son consistentes (exit 2 con `invalid choice` listando opciones válidas). El error de store es claro y accionable.


---

## Round 02 — Spec infrastructure hidden from CLI

**Source:** ST-06

### Hallazgo principal

`deskops.specs` es un motor de compilación completo (loader + compiler + mermaid renderer) que **no tiene superficie CLI directa**. No existe `deskops spec` ni ningún subcomando relacionado.

### Lo que existe pero no se ve desde la CLI

| Componente | Location | Función |
|---|---|---|
| SpecRegistry | `deskops/specs/loader.py` | Carga specs YAML de `spec/`, expone fields, primitives, artifacts |
| compile_artifact_spec | `deskops/specs/compiler.py:80` | Compila input + field specs → payload validado |
| compile_task_bundle_spec | `deskops/specs/compiler.py:25` | Compila input + task spec + primitives → task bundle |
| render_artifact_structure_mermaid | `deskops/specs/mermaid.py:6` | Diagrama Mermaid de relaciones de campos |
| render_task_routine_mermaid | `deskops/specs/mermaid.py:27` | Diagrama Mermaid del flujo de rutina |

### Lo que está en spec/ YAML

- `spec/artifacts/` (9 archivos): atom, board, faq, inbox_note, pill, repository, ritual, step, task
- `spec/fields/` (43 archivos): action, answer, author, body, category, goal, title, what, why, when, where, how, how_not...
- `spec/primitives/` (10 archivos): task_activate, task_close, task_closeout_ready, task_testing_ready...

### Cómo se usa indirectamente

- `deskops add <kind>` deriva los flags CLI de `spec/artifacts/*.yaml`
- `deskops list <kind>` y `show <kind>` usan los mismos artifact registries
- `deskops advance` usa el task spec para definir el patrón de rutina

### Nada de esto tiene comando directo

Un usuario que quiere "inspeccionar un spec", "compilar un spec", o "generar un diagrama de spec" no tiene por dónde. El motor está ahí, los YAML están ahí, pero no hay `deskops spec list/show/build/compile/diagram`.


---

## Round 03 — Add task y advance rotos

**Source:** ST-add-task

### add task

| Aspect | Resultado |
|---|---|
| `add task --title "X" --goal "Y"` | Crea el archivo, **pero exit code 1** |
| Auto-generación | Crea routine, checklists, conditions, edges, operators automáticamente |
| Error en stdout | Pydantic errors sobre `id` / `status` requeridos aparecen en stdout a pesar de que el archivo se creó bien |

**BUG (medium):** exit code 1 con errores de validación de Pydantic a pesar de crear el archivo exitosamente. `id` y `status` son auto-generados pero el sistema no los pasa al modelo antes de validar.

### advance task — CRITICAL

| Comando | Resultado |
|---|---|
| `advance task --help` | No tiene flag `--to` |
| `advance task <id>` | Dice "has no routine" |
| `advance task <id> --to in_progress` | `--to` no existe como flag |

**BUG (critical):** `advance task` no funciona. La causa raíz: el campo `routine` en el archivo de task es sobreescrito por el primer checklist item durante la creación/extracción. Cuando `_load_routine` busca `routine-task-*` no lo encuentra y retorna None.

Además, `advance task` no tiene `--to` — el help no documenta cómo se supone que funcione.

### add otros tipos

| Tipo | Comando | Exit | Archivo |
|---|---|---|---|
| ritual | `--title "X" --purpose "Y"` | 0 | `desk/rituals/ritual-X.md` |
| board | `--title "X" --scope "Y"` | 0 | `desk/tasks/board-X.md` (en tasks!) |
| condition | `--title "X"` | 0 | `desk/primitives/conditions/condition-X.md` |
| checklist | `--title "X"` | 0 | `desk/primitives/checklists/checklist-X.md` |
| hook | `--title "X"` | 0 | `desk/primitives/hooks/hook-X.md` |
| step | `--title "X"` | 0 | `desk/steps/step-X.md` |
| atom | `--title "X"` | 0 | `desk/atoms/atom-X.md` |
| faq-doc | `--title "X"` | 0 | `desk/faq/faq-X.md` |
| repository | `--name "X" --path "/tmp"` | 0 | `desk/registry/repo-X.md` |

### Inconsistencias de flags

- `condition` usa `--title`, NO `--name` (pero el help sugiere `name`)
- `repository` usa `--name`, no `--title`
- Todos los demás usan `--title`

### board va a desk/tasks/

`add board` escribe en `desk/tasks/` (compartido con tasks), no en `desk/boards/`. Hay colisión de namespace.

### list commands rotos por artifacts incompletos

- `list tasks` falla si existe `task-item.md` con campos vacíos
- `list rituals` falla si existe `ritual-item` con campos vacíos
- `list pills` falla si existe `pill-none.md` con campos vacíos

**BUG (medium):** artifacts pre-existentes incompletos rompen `list` con errores de validación Pydantic no manejados. El sistema debería skipearlos en vez de crashear.


---

## Round 03 — Error message inconsistencies

**Source:** ST-show-nonexistent, ST-pills-deep

### Dos estilos de "not found"

| Grupo | Mensaje | Calidad |
|---|---|---|
| task, routine | `No {type} found for {id}` | ✅ Limpio, user-facing |
| Los otros 13 tipos | `Unexpected: No artifact.{ext} file found for id '{id}' in {path}` | ⚠️ Leakea path interno, prefijo "Unexpected:" sugiere bug |

### show con IDs raros

| Input | Comportamiento | Severidad |
|---|---|---|
| `""` (vacio) | Muestra `atom-001` (el primero) | 🔴 Bug — string vacío tratado como "sin argumento" |
| `" "` (espacio) | Llega al filesystem sin trim | ❗ Debería validar |
| `"."` | Llega al filesystem | ❗ Debería validar formato |
| `"  with spaces  "` | Llega al filesystem sin trim | ❗ No hay sanitización |

### add sin flags — inconsistencia

| Comando | Resultado | Severidad |
|---|---|---|
| `add task` (sin flags) | Error de validación (Pydantic traceback) | ✅ Catchado (pero feo) |
| `add ritual` (sin flags) | Crea `ritual-none` | 🔴 Bug — artifact basura |
| `add board` (sin flags) | Crea `board-none` | 🔴 Bug |
| `add step` (sin flags) | Crea `step-none` | 🔴 Bug |
| `add pill --title ""` | Crea `pill-none` | 🔴 Bug — título vacío aceptado |

Algunos tipos validan campos requeridos, otros crean silenciosamente basura.

### show con partial match

Ningún comando soporta fuzzy/partial match:
- `show pill self-reflection` → not found
- `show step document` → not found
- `show pill ".*"` → not found (regex no soportado)

### --root edge cases

| `--root` | Comportamiento | Severidad |
|---|---|---|
| `./nonexistent` | Exit 0, sin output | 🔴 Bug — error silencioso |
| `setup.py` (file) | Exit 0 inconsistente | 🔴 Bug — exit code incorrecto |
| Antes del positional | `invalid choice: '/tmp'` | 🔴 Bug — flag no reconocido antes del subject |

### Pydantic tracebacks al usuario

`add task` sin args muestra:
```
Unexpected: 2 validation errors for TaskDoc
id
  Field required [type=missing, input_value={'title': '...'}, input_type=dict]
```

Esto es un traceback interno de Python/Pydantic. Debería atraparse y mostrar "Missing required field: id".

### show ritual usa ID: field no filename

`show ritual` busca el `ID:` dentro del archivo, no el filename. `show ritual ritual-closeout` falla pero `show ritual closeout` funciona. Esto es **inconsistente** con `show pill` que usa filename.


---

## Round 03 — FAQ quality and desk data inventory

**Source:** ST-faq

### FAQ

- 14 preguntas con respuestas sustantivas (ejemplos de código, tablas de flags, cross-references)
- **`faq --topic` no existe** — error `unrecognized arguments`
- `faq <valid-slug>` funciona, retorna Q&A completo
- `faq <invalid-slug>` error claro: `Unknown FAQ question: X`
- Gap: no hay FAQ entry sobre `deskops graph` o `deskops atoms`

### Desk directory file counts

| Directorio | Archivos | Notas |
|---|---|---|
| `desk/atoms/` | 5 + 60 anidados | Solo 4 visibles via CLI |
| `desk/contexts/` (pills) | 13 | 11 pills numbered + index + readme |
| `desk/inbox/` | 11 | Notas con timestamp |
| `deskops/models/` | 17 | Model docs |
| `desk/rituals/` | 3 | closeout, execution, testing |
| `desk/routines/` | 2 | Task routines |
| `desk/steps/` | 1 | step-document-the-cli |
| `desk/tasks/` | 3 | Board.md + tasks |
| `desk/registry/` | 1 | repo-deskops |
| `desk/primitives/` | 9 | checklists, conditions, edges, hooks, operators |
| `desk/faq/` | 0 | Vacío — FAQ compilado de otra fuente |
| `desk/fields/` | 0 | Vacío |
| `desk/boards/` | 0 | Vacío |

### Pill quality

Los 11 pills reales tienen todos los campos (what, why, when, where, how, how_not, tags). Calidad excelente.


---

## Round 03 — Init, bootstrap, scaffold

**Source:** ST-init

### init

- Scaffolding completo: `.sldb/core/`, `.sldb/runtime/`, `desk/tasks/`, `desk/contexts/`, `desk/rituals/`, `desk/atoms/`, `desk/drawer/`, `desk/inbox/`, etc.
- Templates personalizados con el basename del target directory
- **Idempotente**: segunda corrida detecta "already exists" sin errores
- `init --help` no tiene descripción — solo usage line
- `init` sin path opera sobre CWD silenciosamente — el usuario puede no darse cuenta

### bootstrap

- `bootstrap --help` solo usage line, sin descripción
- `bootstrap` dice "Global deskops model registry is ready" pero no muestra qué hizo
- La diferencia entre `bootstrap` e `init` no es clara desde la ayuda

### desk install

- Existe como subcomando, acepta path posicional
- No se probó a fondo (requiere otro repo)

### graph build en scaffold fresh

- Produce KG snapshot con 1 nodo (`config_file:tag-namespaces.yaml`) y 0 edges
- Correcto para un scaffold vacío

### list atoms en scaffold fresh

- **Silencioso**: no imprime nada (no hay átomos todavía). No dice "no atoms found".

### Error handling

- Path inexistente → exit 1, mensaje claro
- Path es archivo → exit 1, mensaje claro
- Sin path → exit 0, opera en CWD (sorprendente)


---

## Round 03 — Model layer and sldb state

**Source:** ST-models

### Model hierarchy

```
StructuredNLDoc (sldb)
├── AtomDoc, FAQDoc, InboxNoteDoc, RepositoryDoc, StepDoc
└── PrimitiveDoc (deskops.models.base)
    ├── ChecklistDoc, ConditionDoc, EdgeDoc, HookDoc, OperatorDoc, RoutineDoc
    └── OperationalArtifactDoc
        ├── BoardDoc, PillDoc, RitualDoc, TaskDoc
```

17 clases de modelo, 3 niveles de herencia, todos con Pydantic v2. **Estructuralmente sano.**

### sldb store state

- **core/store_index.yaml**: Solo `AtomDoc` registrado como modelo
- **models/AtomDoc.yaml**: Descriptor completo del modelo
- **documents/AtomDoc.yaml**: 15+ AtomDoc entries indexados
- **runtime/**: knowledge_graph.kg.json (216KB) + knowledge_graph.nx.json (351KB)
- **.config/**: Ausente (no es problema)
- **Solo AtomDoc está persistido** — ningún otro modelo tiene documentos en store todavía

### Spec-driven CLI generation

El parser en `deskops.cli.parser.build_parser()` genera dinámicamente los 15 subcomandos de `add`/`list`/`show` desde el spec registry. Cada `add` expone flags derivados de spec (`--title`, `--goal`, `--what`, `--why`, etc.). **El mecanismo funciona.**

### Runtime classes

9 clases runtime que reflejan el model layer: `Task`, `Routine`, `Condition`, `Checklist`, `Edge`, `Hook`, `Operator`, `TransitionResult`, `Primitive`. Mismo patrón de 3 niveles.

### Issues encontrados

1. `DeskopsOperations.__init__` frágil con tipos — espera `Path` pero `root.resolve()` falla si recibe `str`
2. `__fields__` usado en vez de `model_fields` — deprecated en Pydantic v2, rompe en v3
3. Solo `AtomDoc` persiste en store — los demás modelos existen como clases pero no están registrados


---

## Round 04 — Desk install y pythonpath

**Source:** ST-desk-install

### desk install

- Funciona: scafollea 8 dirs + 6 files en el target
- Idempotente: segunda corrida no falla
- Path inexistente → exit 1, mensaje claro
- Sin path → exit 2, argparse standard

### --pythonpath flag

- **Solo existe en `inbox` y `repo register`**
- `list`, `show`, `add`, `graph` **no tienen** el flag — `_apply_default_pythonpath` en main.py es dead code para esos comandos
- `deskops list atoms --pythonpath /tmp` → `unrecognized arguments`

Esto es un bug de wiring: el flag debería ser global o sacarse el dead code.

### Entry points

- `deskops` y `python -m deskops` son consistentes (mismo output, mismos exit codes)
- `deskops about` funciona desde cualquier directorio
- No requiere `$HOME` — corre limpio con `env -i`


---

## Round 04 — Env vars, config, system integration

**Source:** ST-env-vars

### Config files

No existen. `~/.config/deskops`, `~/.deskops`, `/etc/deskops` — todo vacío. Deskops es completamente stateless en disco fuera de `.sldb/`.

### Environment variables

No hay variables `DESKOPS_*` ni `SLDB_*` definidas ni honradas.

### Version info

- Package: `deskops` v0.1.0
- Entry point: `deskops.cli.main:main`
- SLDB: desarrollo install desde `tools/sldb` (sibling directory)

### System integration

- Corre desde cualquier directorio
- No requiere `$HOME`
- Piped input a `inbox` falla si no coincide el formato esperado
- SLDB no tiene `__version__`

### Observación

La dependencia de sldb es un editable install desde `../sldb`. Si ese path se mueve o no está presente, deskops no funciona. Esto no es un problema ahora pero es un coupling a considerar para distribución.


---

## Round 04 — --from-yaml y side effects

**Source:** ST-from-yaml

### --from-yaml existe en todos los tipos

Los 13 tipos de artifact soportan `--from-yaml`. Cada uno acepta un path a un archivo YAML.

### CRITICAL: Side effects en failure

`deskops add task --from-yaml` con YAML parcial (solo `title` + `goal`) **crea todos los archivos en disco** a pesar de devolver exit code 1:

- `desk/tasks/task-yaml-test-task.md`
- `desk/routines/routine-task-yaml-test-task.md`
- 3 checklists, 3 conditions, 6 edges, 3 operators

La validación falla después de escribir. No hay rollback. Esto es un hazard de integridad de datos.

### No hay bulk operations

`--from-yaml` es el único mecanismo batch, y opera un artifact por llamada. No hay `--batch`, `--bulk`, `--csv`, `--import`, multi-entity YAML array.

### Output format flags

Ningún `show` o `list` tiene `--format`, `--json`, `--yaml`, `--output`. Todo el output es markdown hardcodeado para humanos. No hay salida machine-parseable.


---

## Round 04 — Graph: edge serialization bug

**Source:** ST-graph-deep

### CRITICAL: KG JSON edges are empty

Los 68 edges en `kg.json` existen como entradas de diccionario pero **todos tienen `role: None` y `target: None`**. El grafo serializado en KG JSON no puede ser recorrido — `graph neighbors` no encuentra edges porque los edges existen pero están vacíos.

### NetworkX snapshot tiene los datos correctos

El archivo `knowledge_graph.nx.json` tiene 82 links con `role: "references"`, `source_kind`, `confidence`, y `provenance` completos. **Los datos existen upstream** pero la serialización a KG JSON los pierde.

### Node count drift

- kg.json: 257 nodos
- nx.json: 260 nodos
Probablemente el NX snapshot es de un build anterior.

### Self-reflection no está en el pipeline

`find_missing_snapshot_targets` en `self_reflection.py` nunca se llama durante `graph build`. El módulo de self-reflection existe pero no está conectado.

### Code duplication

`find_missing_snapshot_targets` aparece tanto en `checks.py` como en `self_reflection.py` con la misma firma.

### Graph build performance

0.455 segundos. Rápido para el tamaño actual (257 nodos).

### __init__.py delgado

`deskops/graph/__init__.py` solo exporta `DocGraphNode` y `extract_doc_nodes` de los ~10 símbolos públicos del subpackage.


---

## Round 04 — Spec YAML structure

**Source:** ST-fields-primitives

### Directory layout

| Directorio | Archivos |
|---|---|
| `spec/artifacts/` | 9 (atom, board, faq, inbox_note, pill, repository, ritual, step, task) |
| `spec/fields/` | 42 (title, goal, status, what, why, when, where, how, how_not, etc.) |
| `spec/primitives/` | 10 (6 operators, 3 checklists, 1 edge_set) |

### Schema uniforme

Todos los specs siguen `{id, title, type, version, data}`.

### Task artifact incompleto

Es el **único** artifact sin `doc.model`. Todos los demás declaran su modelo Pydantic (`TaskDoc`, `PillDoc`, etc.). Task no.

### 6 campos huérfanos

Definidos en `spec/fields/` pero no referenciados por ningún artifact:
- `category`, `distinct_from_pills`, `for_whom`, `materializes_into`, `related_atoms`, `stabilized_in`

Probablemente reservados para uso futuro.

### Sin validation rules

0 rules de validación en 61 archivos YAML. La única constraint es `value_type` (string, markdown, enum, list) y `required` (true/false). No hay `description`, `pattern`, `min`, `max`, ni ningún otro metadata.

### Template system

El syntax `⸢...⸥` está declarado en AGENTS.md pero no aparece en ningún spec YAML. Los primitives usan `{braces}` style (`{task_id}`).

### Task lifecycle state machine

```
execution → [checklist: execution_ready] → operator: activate
  → [checklist: testing_ready] → operator: mark_ready_for_testing
  → [checklist: closeout_ready] → operator: close → complete
```

6 operators, 3 checklists, 6 edges. Definido en `spec/primitives/`.


---

## Round 05 — Advance task deep dive + graph missing

**Source:** round-05-subagent-02

### CRITICAL: sldb DataExtractor misparses TaskDoc markdown

El template de TaskDoc tiene secciones en orden con `⸢...⸥` anchors. Cuando el archivo real tiene una cantidad distinta de checklist items que el template, los map indices del AST markdown se desplazan, causando que el extractor **cross-wire los campos**:

- `routine` → recibe el valor de `current_node` (un checklist ID, no el routine ID)
- `current_node` → queda vacío porque lookup en posición incorrecta
- `files` → recibe checklist IDs

Esto rompe `advance task` completamente porque `_load_routine()` busca un ID de routine que es en realidad un ID de checklist, no encuentra nada, y devuelve "task has no routine".

### Duplicate error message en advance

`advance task` imprime "has no routine — cannot advance" DOS veces: una en `operations.py:268` y otra en `operations.py:148` (CLI handler).

### graph build no actualiza knowledge_graph.nx.json

`graph build` escribe `knowledge_graph.kg.json`, `semantic_dag.yaml`, `semantic_index.yaml` pero NO actualiza `knowledge_graph.nx.json`. Ese archivo queda stale desde el primer build.

### graph missing funcional

`deskops graph missing` reporta dangling references con source file + line number. Formato claro.

### graph neighbors sin documentación de prefijos

`graph neighbors atom:atom-deskops` funciona, pero `graph neighbors atom-deskops` falla con "graph node not found". `--help` no documenta el formato `type:id`.

### add task sin args → Pydantic cryptic error

`deskops add task` sin flags → `Unexpected: 2 validation errors for TaskDoc ... id Field required, status Field required`. Debería mostrar usage/help.

### Empty string payload crea task con título "None"

`deskops add task ''` → exit 0, crea `task-none.md` con título `# None`.


---

## Round 05 — Cross-command workflows

**Source:** round-05-subagent-04

### Dos sistemas de FAQ separados

`deskops faq` lee de `docs/faq.md` (preguntas estáticas). `deskops add faq-doc` / `list faq-docs` / `show faq-doc` operan en `desk/faq/`. Ambos sistemas **nunca interactúan**:
- `deskops faq "deploy"` falla aunque exista un faq-doc con ese título
- `deskops faq` (sin args) lista 14 preguntas estáticas, no los faq-docs creados
- El usuario no tiene forma de descubrir faq-docs via `faq` command

### Dos comandos para registrar repos

`deskops repo register deskops .` → ID: `deskops` (sin `repo-` prefix)
`deskops add repository --name "deskops-alt"` → ID: `repo-deskops-alt`
Inconsistente. Además `repo register` no crea tags, `add repository` sí.

### list inbox-notes vs inbox --list

`list inbox-notes` muestra 2 notas. `inbox --list` muestra 13. Dos commands para la misma operación con resultados distintos y formatos distintos.

### Ritual y step no se pueden linkear

`add step` no tiene `--ritual` flag. `add ritual` no acepta step IDs. Steps quedan huérfanos.

### board y task no se linkean

Board se crea con tasks vacío. Task se crea pero no se asocia al board. No hay flag `--board` en `add task` ni `--task` en `add board`.

### `show board` mislabel

El output de `show board` muestra tags bajo la label `rituals:`:
```
rituals: workspace:desk, artifact:board
```
(son tags, no rituals)

### Filenames vs directorios esperados

- `desk/pills/` no existe → pills están en `desk/contexts/`
- `desk/boards/` no existe → boards están en `desk/tasks/`
- `desk/repositories/` no existe → repos están en `desk/registry/`

### Created artifacts no aparecen en graph edges

Después de crear tasks, rituals, boards, atoms, steps: `graph neighbors` muestra 0 edges para todos. 286 nodos, 0 edges.


---

## Round 05 — OS/IO edge cases, special inputs, error resilience

**Source:** round-05-subagent-05

### Muy large title → OSError

`--title "$(python3 -c 'print("A" * 10000)')"` → `[Errno 36] File name too long`. Sin graceful truncation, crash.

### Empty string payload → artifact con título "None"

`deskops add task ''` → exit 0, crea `task-none.md`.

### Error messages a stdout

`deskops show task nonexistent 2>/dev/null` → el mensaje aparece (debería ir a stderr).

### Algunos flags inconsistentes

`inbox` usa `--desk-root`, `add task` usa `--root`. Distinto nombre para el mismo concepto.

### add task sin args → Pydantic traceback

`deskops add task` → `Unexpected: 2 validation errors for TaskDoc`. No muestra usage.

### Whitespace-only inputs

`--title "  "` → titulo literal de 3 espacios. Sin validación. Slug genérico `-item`.

### HTML/special chars sin sanitizar

`--title "Title with <html> & special chars"` → preservado verbatim en el archivo.

### Path traversal no validado

`--root /tmp/../../etc` → resuelve a `/etc`, error de permiso del OS. No hay path validation propia.

### Múltiples --root

`--root . --root /tmp` → último gana. Sin warning.

### --dry-run no existe en ningún comando

### HOME, TMPDIR no son necesarios

Corre limpio sin `$HOME`.

### List con --root no valido

`deskops list tasks --root /tmp/nonexistent` → exit 0, sin output. Sin error.


---

## Round 05 — --from-yaml para todos los tipos

**Source:** round-05-subagent-06

### Comportamiento inconsistente: empty YAML `{}`

8 tipos (pill, ritual, board, atom, repository, inbox-note, faq-doc, step) → **exit 0, crean basura** con `id: *-none`, `title: "None"`.
7 tipos (task, condition, operator, checklist, hook, edge, routine) → **exit 1, KeyError** en `'title'`. Clean failure.

Causa raíz: los primeros usan `.get("title")` (devuelve `None` → `str(None)` → `"None"`), los segundos usan `payload['title']` (KeyError).

### BUG en `_normalize_task_payload`: list() vs _coerce_list()

`_normalize_task_payload` usa `list(payload.get("pills") or [])` que para un string como `pills: single-pill-ref` lo splitea en **caracteres**: `['s', 'i', 'n', 'g', 'l', 'e', ...]`.

Afecta: `references`, `depends_on`, `pills`, `files`, `validation`, `history`, `tags` en task.

`_coerce_list()` existe pero se usa solo en `compile_task_bundle_spec` (post-normalize).

### YAML type coercion bug

- `created_at: 2026-01-01` → YAML lo parsea como `datetime.date`, Pydantic espera `str` → crash
- `scope: no` → YAML boolean `False` → `False or ""` → `""` (inconsistente con `done_when: true` que da `"True"`)

### Custom `id` en YAML funciona para task

`id: task-my-custom-id` → exit 0, ID respetado.

### Extra fields silenciosamente ignorados

Todos los tipos. Sin warning, sin error. Pydantic models sin `model_config = {"extra": "forbid"}`.

### Errores siempre wrapped en "Unexpected:"

KeyError, FileNotFoundError, YAML parse error, Pydantic validation error — todos con prefijo `Unexpected:`.

### clean failure property

Para la mayoría de los casos de fallo, no se escriben archivos. Excepción: `create_task_bundle` puede escribir task + primitives y luego fallar en `_append_task_to_board`, dejando archivos huerfanos.


---

## Round 05 — Repo register edge cases

**Source:** round-05-subagent-01

### No path validation

`deskops repo register myrepo /nonexistent/path` → exit 0, registra un repo cuyo path no existe. Sin warning.

### No path scope validation

`deskops repo register myrepo-etc /etc` → exit 0. Acepta `/etc`, `/tmp`, cualquier path del sistema.

### Duplicate: file overwritten before store check

`deskops repo register myrepo .` repetido → exit 1, pero el archivo `.md` en `desk/registry/` ya fue sobrescrito. Inconsistencia: file on disk != store index.

### init + repo register gap

`deskops init /tmp/test && cd /tmp/test && deskops repo register local-test .` → `Error: RepositoryDoc model is not registered in the store.`

`init` no registra modelos en el local store. `bootstrap` sí, pero solo en global store (~/.sldb).

### Path sí existe como archivo

`deskops repo register test /tmp/test-file` (file, not dir) → exit 0, sin error. Path validation inexistente.

### Duplicate slug collision

`"my repo"` y `"My Repo"` slugifican a `my-repo`. El segundo overwrites silenciosamente.

### Empty name → Pydantic traceback

`deskops repo register "" /tmp` → `Unexpected: 1 validation error for RepositoryDoc ... Field required`

### --pythonpath aceptado pero no persistido

Flag aceptado, usado para runtime resolution pero no guardado en el archivo markdown.


---

## Round 05 — Show/list: 13/15 tipos leakean paths, glob bug

**Source:** round-05-subagent-03 + round-05-subagent-04

### CRITICAL: `_resolve_glob` returns WRONG artifact

`show <type>` usa `f"{doc_id}*.md"` glob. Si `task-board` existe y `task-board-task-2` también, el glob `task-board*.md` matchea AMBOS. El que se muestra es el primero alfabéticamente, que suele ser el **sufijo** (no el exacto).

Ejemplos:
- `show task task-board` → muestra `task-board-task-2` (es el que querés pero hay otros)
- `show repository repo-deskops` → muestra `repo-deskops-alt` (el equivocado)
- `show operator operator-task` → muestra `operator-task-aaaauniquetitle999-activate`

Esto es un **data safety bug**: podes pedir un artifact y que te muestren otro sin advertencia.

### CRITICAL: `list inbox-notes` muestra 2 de 13

`list inbox-notes` solo muestra 2 notas. `inbox --list` muestra las 13. Causa: `list inbox-notes` usa un glob pattern `inbox-note-{slug}*` que no matchea los date-prefixed filenames (`20260604-171903-unclear-bug-found.md`).

### CRITICAL: `show <type> ""` matchea todo

`show task ""` → `*.md` glob, matchea `Board.md`, crash con Pydantic error.
`show pill ""` → crash similar.
`show condition ""` → devuelve la primera condition alfabética (no es un error, pero es silencioso).

### CRITICAL: `list tasks` crash por un archivo inválido

`task-item.md` con `# ` (título vacío) → `list tasks` entero crashea con Pydantic traceback. Idem `list pills` con `pill-none.md`.

### 13/15 show types leakean paths absolutos

`show`, `show routine` están bien ("No task found").
Los otros 13 tipos muestran:
```
Unexpected: No artifact.pill file found for id 'nonexistent' in /home/jp/.../desk/contexts
```

### 3 formatos de output distintos en list

- `list tasks`: `id | status | current_node`
- `list conditions/operators/checklists/hooks/edges`: `id | status | title`
- `list pills/rituals/boards/atoms/repositories/inbox-notes/faq-docs/steps`: `id | title` (sin status)

Sin `--format` flag en ningún list/show.

### Rituales invisibles: closeout.md, execution.md, testing.md

Existen en `desk/rituals/` pero tienen filenames que no empiezan con `ritual-`. `list rituals` los ignora. `show ritual ritual-closeout` falla. `show ritual closeout` funciona (filename stem match, no ID).

### Board.md invisible

`board-001` en `Board.md` (capital B). `list boards` lo ignora porque busca `board-*.md`.

### show: filename stem vs internal ID inconsistency

- `show ritual` busca por internal `ID:` field
- `show pill` busca por filename stem
- Combinación: `show ritual closeout` funciona pero `show ritual ritual-closeout` falla

### Error messages van a stdout, no stderr

`deskops show task nonexistent 2>/dev/null` → mensaje aparece. Debería ir a stderr.


---

## Round 06 — Primitive types comprehensive + show/list bugs

**Source:** round-06-subagent-01, round-06-subagent-02, round-06-subagent-03

### CRITICAL: `show condition` swaps Subject and Predicate when Subject is empty

Cuando Subject está vacío, `extract_model_data` (sldb parser) absorbe el contenido de Predicate en Subject. El file markdown tiene:

```
### Subject

(empty)

### Predicate

truthy
```

Pero `show condition` muestra `Subject: truthy, Predicate: `. Es un parser bug en sldb.

### CRITICAL: `show` glob bug confirmado en TODOS los primitives

`show checklist checklist-test-checklist` → muestra `checklist-test-checklist-stress` (el archivo equivocado). Misma causa: `f"{id}*.md"` glob, `-stress` ordena antes que `.md`.

### `show routine` edges no se muestran

El archivo markdown tiene `edge-1`, `edge-2` en `## Edges`. Pero `show routine` intenta cargar cada edge ID como un EdgeDoc completo. Como `edge-1` no existe como primitive standalone, `_load_edge` devuelve None, el list comprehension lo filtra, y la CLI muestra lista vacía.

### `list --root /tmp/nonexistent` silenciosamente exitoso

`list conditions --root /tmp/nonexistent` → exit 0, sin output. Operations.py:225-226 devuelve `[]` si el directorio no existe, sin error.

### Todos los primitives se crean correctamente

condition, operator, checklist, hook, edge, routine → todos exit 0, campos correctos.

### `list` para primitives consistente

Todos usan formato `id | status | title`. Exit 0.


---

## Round 06 — Remaining surfaces: inbox JSON, tests, Python API, mixed flags

**Source:** round-06-subagent-03, round-06-subagent-01

### `inbox --list --format json` crashes

`deskops inbox --list --format json` → `Unexpected: Object of type datetime is not JSON serializable`. Los campos `created_at` son objetos `datetime.datetime` que el JSON encoder no serializa. `--format yaml` funciona correctamente.

### `--from-yaml` overrides inline CLI flags

`add pill --from-yaml /tmp/test.yml --title "CLI Title"` → el título en el archivo es el del YAML, no `"CLI Title"`. Precedencia: YAML > CLI flags. Esto puede sorprender al usuario.

### 59/59 tests pasan

14 test files en `tests/`. Todos pasan. 4 deprecation warnings por `datetime.utcnow()`.

### Python API no documentada

- `deskops/__init__.py` es solo un docstring — sin exports, sin `__version__`, sin `__all__`
- 23 submodules, todos importables
- `main()` catch-all handler: `except Exception: raise SystemExit("Unexpected: {exc}")` — masks programming errors
- `FaqDoc` no existe, es `FAQDoc` — naming trap
- 17 Pydantic v2 models, todos construibles y serializables

### Graph resilience

Corrupted `knowledge_graph.kg.json` → `graph build` regenera correctamente.

### `deskops about --help` funciona

Minimal help. Same output.

### atoms add-namespace --example requiere prefijo

Los examples deben tener prefijo `namespace:value`. `--example ex1` solo es rechazado (probablemente validación en tag-namespaces.yaml).

### 23 `-none.md` artifacts residuales

Scattered por desk/ — de pruebas de empty YAML. No limpiados.

### Mixed from-yaml + inline → YAML gana

Precedencia: `--from-yaml` sobreescribe flags inline.

### `inbox --show` para IDs inexistentes

`deskops inbox --show nonexistent` → `Unknown inbox note: nonexistent` (exit 1). Claro.

### sldb como sibling package

`/home/jp/proyectos/hum-ecosystem/tools/sldb/src/sldb/__init__.py`. Los tests añaden `../sldb/src` a sys.path.


---

## Round 06 — Hidden modules: spec engine y materializers

### Mermaid renderer: código vivo, sin CLI

`deskops.specs.mermaid.render_task_routine_mermaid(registry, artifact_id)` → renderiza un diagrama Mermaid de la rutina de un artifact spec. `render_artifact_structure_mermaid` hace lo mismo para la estructura del artifact.

Ambos son funcionales pero no tienen CLI. `deskops graph` podría tener `graph mermaid` o `graph diagram`.

### Materializers: código vivo, sin CLI

`build_architecture_doc_payload(atom, title)` → genera un documento compuesto a partir de un átomo.

`build_composed_doc_payload(atoms, title, body_intro)` → combina múltiples átomos.

Son las funciones que implementan el concepto "materialize" del que hablan los átomos. Sin CLI.

### SpecRegistry.load(root) requiere project root

`SpecRegistry.load()` necesita un `Path` al root del proyecto. La CLI ya tiene este contexto pero no expone el spec registry programáticamente.

### Runtime primitives: máquina de estados

`deskops.runtime.primitives` contiene clases `Task`, `Routine`, `Checklist`, `Condition`, `Operator`, `Edge`, `Hook`, `TransitionResult`. Es el motor de ejecución que `advance task` debería usar. `TransitionResult` indica que hay soporte para transiciones stateful que nunca se expone.

### `inbox --list --format yaml` funciona

Output YAML con estructura, paths absolutos, y `created_at: null` para notas sin timestamp. Funcional pero los paths absolutos en output machine-parseable no son portables.

### `inbox` file headers tienen `created_at`

Los archivos en `desk/inbox/` con filenames date-prefixed (`20260604-171903-*.md`) contienen `created_at: 2026-06-04T17:19:03` en los headers. Las notas creadas via `add inbox-note` no tienen timestamp auto-populado.
