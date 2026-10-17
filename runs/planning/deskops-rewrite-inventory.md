# deskops: inventario de malas prácticas y plan de reescritura

Fecha: 2026-10-16. Hecho con 4 revisiones de solo lectura (operations.py, capa CLI,
graph/specs/materializers, models/identity/borde con sldb) y verificación propia de
los hallazgos altos. Estado de verificación por hallazgo: **E** = reproducido con
ejecución, **L** = confirmado leyendo el código, **P** = reportado y plausible, sin
verificar a mano.

## Veredicto

Reescritura **por dentro, módulo a módulo, detrás de un contrato congelado**
(strangler), no big-bang. Razones:

- El contrato externo es grande y otros dependen de él: 24 stores en la máquina
  trackean `TaskDoc`. sldb hashea el contrato de cada modelo (campos con sus
  descripciones, `__template__`, `__semantics__`, bases, `__references__`,
  `__containment__`, `__compositions__`: `sldb/store/hashing.py:_contract_parts`).
  Una reescritura que toque un modelo deja desfasados a todos esos stores.
- Hay 335 tests al 2026-10-16 (306 al hacer el inventario; 120 vía subprocess de la CLI). Sirven como especificación si se
  congela el contrato antes.
- El interior sí está para reescribirlo: `operations.py` tiene 2.913 líneas en una
  sola clase con 15 dominios mezclados. Hay tres caminos de cierre de task, el grafo
  se extrae con regex en paralelo a lo que sldb ya indexa, los errores se tragan por
  todos lados y hay pocas mutaciones transaccionales.

Hay **bugs que hoy destruyen datos**. Se arreglan antes de reescribir (fase 0),
independiente de la decisión.

## Estado (actualizado 2026-10-16)

- **Cerrado**, commiteado y pusheado por el coordinador:
  - Issue 1, drawer → task: `from_drawer` es procedencia, no una referencia que deba resolver (494ba45).
  - Los comandos `graph` importan en Python 3.10/3.11 y no tapan el error real (62e7603); arregla el CI de Governance.
  - Issue 2, closeout sin corrida: el dueño eligió la opción A. Está en 819a8b8 como
    `deskops closeout commit --no-run --reason <texto>`, con los trailers `Closeout-Mode: manual` y
    `Closeout-Reason`, y una entrada en el índice con `run_dir: null` y `mode: manual`.
  - Las primitivas se retiraron: el ciclo de vida de las tasks vive en el grafo de sldb (afdec7f,
    mergeado en 56f49d5). Los estados son los rituales execution, testing y closeout; las
    transiciones son `RelationDoc` con condición `--where` en `desk/lifecycle/`; se borraron los
    modelos Condition, Checklist, Operator, Edge, Hook y Routine, las 17 primitivas por task y su
    runtime. `deskops desk update --apply` migra los desks existentes. Con esto desaparece D1, la
    task de D1+D2 queda reducida a D2 (`task-rw-f0-closeout-amends-only-its-own-commit`) y
    F3b (servicio de primitivas y código muerto) deja de existir. Requiere
    `structuredLanguageDB>=0.1.9`.
- **sldb 0.1.4** arregla `sldb fields update`, que dejaba el registro del documento con el hash
  viejo (era la caché de shards).
- **El plan está en el desk**: cada nodo del DAG es una task diferida en `desk/drawer/tasks/`
  (`task-rw-*`, más `task-doctor-crashes-on-deskless-roots`). Lo genera y lo prueba
  `runs/planning/rewrite-plan/`:
  - `gen.py` escribe las tasks y la sección del Board del drawer;
  - `check.py` hace los chequeos estáticos;
  - `rehearse.py` crea y cierra todas las tasks con la CLI real en una copia sandbox;
  - `preflight.sh` y `resolve.sh` hacen el preflight sin contexto con pi/deepseek-flash y la
    clasificación con acceso al repo.

  La evidencia está en `runs/subagents/20261016-rw-plan-preflight-r1/` y `-r2/`.
- **Hallazgos nuevos que dejó el plan:**
  - `from_drawer` dentro de un payload `--from-yaml` o JSON no se resuelve a ruta (task F0).
  - `deskops graph missing --root .` ya daba exit 1 en HEAD: 99 hallazgos de dos registros
    archivados del drawer (task F0, bloqueada por decisión).
  - El índice de aristas de sldb ignora los ids sin calificar (`_ids_in`,
    `../sldb/src/sldb/store/edge_index/declared_references.py:66-74`). deskops guarda ids sin
    calificar, así que hoy sldb no ve ninguna arista declarada de deskops (task F4 de petición a sldb).

## Números

- Producción: 14.159 líneas en 76 archivos. Tests: 9.814 líneas, 306 tests.
- `operations.py`: 2.913 líneas. `cli/parser.py`: 1.100. `graph/extract_coverage.py`: 907.
- ~190 líneas muertas solo en `operations.py` (`_default_*_payloads`, 1296-1487: 0 llamadas).
- `pyproject.toml` **no declara `sldb` ni `kgdb`** como dependencias (solo pydantic y PyYAML).

## Hallazgos que importan (ordenados por gravedad)

### Pérdida o corrupción de datos

| id | dónde | qué pasa | verif |
|---|---|---|---|
| D1 | `operations.py:1533` | **Resuelto en afdec7f** (ya no hay primitivas por task). El cierre borraba primitivas con el glob `*-{task_id}*.md`. Cerrar `task-foo` borra, des-trackea y commitea las 17 primitivas de `task-foo-bar`, que queda sin rutina ni checklists. | **E** |
| D2 | `operations.py:1547` | El amend se decide con `startswith("closeout: {task_id}")`. Si HEAD es `closeout: task-foo-bar`, cerrar `task-foo` hace `--amend` sobre el commit de la otra task. | L |
| D3 | `operations.py:1552` | El commit de cierre no lleva pathspec: arrastra cualquier cambio staged ajeno. `git add`/`rm --cached` van con `check=False`. | L |
| D4 | `operations.py:2162` | `_rewrite_inbound_atom_references` (solo la llama `merge_atom`) valida la coincidencia exacta por línea, pero después hace `replace` global: fusionar `atom-foo` corrompe `atom:atom-foo-bar`. `split_atom` no reescribe. | L |
| D5 | `operations.py:2612-2619` | `_resolve_glob` devuelve `matches[0]` del prefijo sin chequear ambigüedad: `advance task task-foo` puede avanzar `task-foo-bar`. `inherits_from` hereda del padre equivocado. | L |
| D6 | `operations.py:1567-1580` | Untrack después del commit: si falla, solo hay un warning, el archivo se borra igual y el store queda con entradas huérfanas. Usa `store=None` y `pythonpath="."` (relativo al cwd). | L |
| D7 | `operations.py:407`, `974-997`, `2758-2811` | El rollback de `create_task_bundle` no des-trackea. El de `merge_atom` no restaura los referidores reescritos. `_write_doc` hace untrack+track en dos pasos con `except Exception` → si falla, el doc queda des-trackeado y el caller ve éxito. | L |

### Diagnóstico roto o engañoso

| id | dónde | qué pasa | verif |
|---|---|---|---|
| X1 | `cli/commands/doctor.py:61,160` | `deskops doctor` sin `desk/` revienta con `Unexpected: cannot access local variable 'unreadable_docs'`. | **E** |
| X2 | `cli/main.py:380-392` | Toda excepción desconocida se convierte en `SystemExit("Unexpected: …")` sin traceback. Clasifica por `exc.__class__.__name__`. Es la razón de que X1 y el bug del CI de Governance se vieran como errores misteriosos. | L |
| X3 | `cli/commands/desk.py:149-171` | `desk update` ignora un `stores check` caído o un JSON roto (`pass`), imprime "Desk is up to date." y sale con 0. | P |
| X4 | `graph/extract_coverage.py:27`; `graph/extract_sources.py:15-26` | `graph build` mete en el grafo de deskops los atoms de `tools/repopackage/` (5 nodos hoy). Ninguno de los dos extractores excluye `tools` ni `.tmp`. | **E** |
| X5 | `graph/extract_edges.py:247`; `extract_docs.py:155` | Un YAML inválido en un fence de atom hace caer `graph build`/`graph missing`/la gate de closeout. En cambio, un frontmatter inválido borra en silencio todas las aristas del doc. | P |
| X6 | `operations.py:2242-2256` | La gate de "commit" acepta cualquier cosa que resuelva `git rev-parse` (`HEAD`, `main`) y la de "tests" acepta cualquier `.py` que exista: `references: ["HEAD","tests/x.py"]` pasa el closeout. | L |

### Estructura

| id | dónde | qué pasa | verif |
|---|---|---|---|
| S1 | `operations.py:1027-1066`; `operations.py:1499`; `cli/commands/closeout.py` | Tres caminos de cierre: `advance` con gates y commit; `advance --to complete` sin gates, sin commit y dejando la task en el Board; `closeout commit` con run-dir y sin gates ni Board. | L |
| S2 | `operations.py` (15 dominios en una clase) | Lifecycle, primitivas, Board, git, gates, atoms (CRUD, split, merge, retarget), drawer, registry, IO de sldb, parseo de args del CLI (`parse_*_input`, 1068-1183) y logging. | L |
| S3 | `operations.py:2904-2910`, `154-208` | `_read_doc(TaskDoc)` superpone un parser regex de secciones encima de `extract_model_data`, y si difieren gana el regex. | L |
| S4 | `graph/extract_edges.py` (todo); `extract_docs.py` | Reimplementa lo que el edge index de sldb ya construye desde `__references__`/`__containment__` (`sldb/store/edge_index/declared_references.py`). Usa 5 esquemas de ids de nodo que compiten entre sí: `drawer_task` se identifica por ruta y `task` por id, así que promover cambia el id del nodo. | L |
| S5 | `graph/snapshot.py`, `checks.py`, `self_reflection.py` | El lector del snapshot está implementado 3 veces, con claves distintas. | P |
| S6 | borde con sldb (~30 imports) | Usa internos privados: `sldb.cli.commands.model.ModelCLI().add(SimpleNamespace)`, `DocCLI().untrack(...)`, `sldb.store.ops.track_document` con 9 argumentos posicionales, `sldb.store.io.*`, `sldb.store.resolver.find_local_store`. Para casi todos ya hay equivalente público en `sldb.api.*`. Todos los imports resuelven hoy. | L |
| S7 | `identity.py`, `cli/main.py:186-209` | `find_local_store()` sube por los padres hasta `~/.sldb`/`~/desk`: un sandbox dentro del repo usa el registry del repo (me pasó reproduciendo el issue del drawer). La regla de sandbox root no distingue `--root .` explícito del default, y la whitelist de comandos deja fuera `atoms`, `closeout`, `doctor` y `desk`, que mutan el desk real. | E (registry) / L |
| S8 | `cli/commands/message.py:171-181` | `message` define `--root` con default `"."`, así que las ramas `--store` y `find_local_store` son inalcanzables. | L |
| S9 | `bootstrap.py:14-32` | `MODEL_REFS` registra 17 modelos y el store del repo tiene 21: un `deskops init` nuevo no registra HookDoc, MaterializationContractDoc, RunDoc ni RuntimeProfileDoc. `ensure_sldb_available` puede correr `pip install -e ../sldb` desde `list`/`show`/`add`. | P |
| S10 | `models/task.py` | `extra: allow`; el campo `frontmatter` con `exclude=True` lo repuebla `render_payload` con una lista de campos de cuerpo mantenida a mano. El serializer de `from_drawer` mantiene los docs byte-idénticos, pero **no evitó** el cambio del hash del contrato (el campo existe, así que se hashea). El comentario lo afirma mal. | L |
| S11 | `specs/compiler.py:44-62` | Hardcodea los 16 campos de TaskDoc y reimplementa el defaulting de Pydantic (`default_factory=dict` → `[]`). | P |
| S12 | código muerto | **En parte resuelto en afdec7f** (`_default_*_payloads` y `PRIMITIVE_DIRS` se fueron con las primitivas). Queda: `_setup_logging` duplicado (el primero se recursaría si se usara), `specs/mermaid.py` y `materializers/atoms.py` (solo los usan tests), `RunDoc` sin escritor, ledger `self_reflection_decisions.json` sin escritor. | L |
| S13 | `graph/extract_coverage.py` (907 líneas) | Scoring difuso con umbrales mágicos, con ramas inalcanzables bajo el corte de 0,70, y estampa `confidence="high"` a todo. **Ninguna gate depende de él** (solo el snapshot). | P |

## Contrato a preservar (congelar antes de reescribir)

1. **Modelos** (21 registrados): nombres de clase, ruta `deskops.models:<Clase>`,
   campos y **descripciones**, templates, `__semantics__`, `__references__`,
   `__containment__`, `__compositions__` (con `deskops.models:TaskDoc`/`StepDoc`
   hardcodeados como string), y la cadena de bases (`PrimitiveDoc` →
   `OperationalArtifactDoc`). Ni siquiera se puede corregir un typo en una
   descripción sin migrar stores.
2. **CLI**: los ~60 comandos/subcomandos con sus flags (tabla completa en el reporte
   de la capa CLI). Sin tests directos: `runtime *`, `closeout commit` vía `main`,
   `atoms type/list/show`, `add board/faq/ritual/step/operator/checklist/hook/edge`
   y `bind`.
3. **Archivos de salida**: `.sldb/runtime/graphs/deskops.kg.json` (schema
   `deskops_kgdb_graph_snapshot_v1`) y `.nx.json`,
   `.sldb/runtime/self_reflection_findings.json`, `runs/subagents/index.jsonl`, y
   los trailers `Task-Id`/`Run-Dir` de los commits de cierre.
4. **Layout del desk** y `desk_format "1.0.0"` (`constants.py`).

## Qué se borra o delega

- **A sldb**: las aristas declaradas por modelo (`extract_edges` frontmatter y
  `__references__`), la extracción de nodos de documentos, el split de
  frontmatter (3 copias a mano) y las búsquedas de jerarquía de `domain_tree`.
  **Falta en sldb**: un reporte de referencias declaradas que no resuelven
  (`resolve_edges` las descarta en silencio). Va al inbox de sldb, no se suple con
  un parser paralelo.
- **Muerto**: los ítems de S12.
- **Decisión tuya**: `extract_coverage.py` (907 líneas, ninguna gate depende de él).
- **Se queda en deskops**: la semántica del workflow (gates de closeout, lifecycle,
  Board), los nodos de archivos no documento (`source_file:`/`test_file:`), el
  reporte de faltantes, la materialización de roles y runtime profiles, y
  `atom_tags`.

## DAG

Estimaciones en días de trabajo de un agente, con tests. Las tareas de una misma fase
sin overlap de archivos van en paralelo; las que editan `operations.py` van en serie,
de la más corta a la más larga.

```
F0 hotfixes ──► F1 congelar contrato ──► F2 infraestructura ──► F3 servicios ──► F5 CLI
                                                   │                  │
                                                   └──► F4 grafo ◄────┘
                                                                     F6 contratos de modelo (al final)
```

**F0. Hotfixes de datos (antes de todo, ~2 d).** Arreglos chicos con un test que falla
antes y pasa después; no esperan la reescritura.
- F0a `operations.py` (en serie): D1+D2 (match exacto de ids de primitiva y de
  subject; 0,5 d) → D5 (ambigüedad en `_resolve_glob`; 0,3 d) → D4 (reemplazo
  tokenizado; 0,3 d) → D3 (commit con pathspec; 0,3 d).
- F0b en paralelo, sin overlap: X1 doctor (0,2 d), declarar `sldb`/`kgdb` en
  `pyproject.toml` (0,1 d), excluir `tools`/`.tmp`/`.venv` del coverage (X4, 0,2 d).

**F1. Congelar el contrato (~2 d, paralelo).**
- F1a: test de snapshot del contrato de cada modelo (hash con `_contract_parts`
  comparado con `.sldb/core/models/*.yaml`; falla si cambia). Protege los 24 stores.
  0,5 d.
- F1b: tests de CLI vía `main(argv)` para las superficies sin test (lista en
  "Contrato"). 1,5 d.
- F1c: golden files del snapshot del grafo y de `index.jsonl`/trailers. 0,5 d.

**F2. Infraestructura nueva (~4 d).** Las tres extraen código de `operations.py`, así
que van en serie, de la más corta a la más larga:
- F2a `desk_paths.py`: resolución de selectores en un solo lugar, con error de
  ambigüedad (une los dos resolvers duplicados). 0,5 d.
- F2b errores y exit codes: errores tipados, una tabla de exit codes (0, 1 dominio,
  2 uso, 3 entorno), fin de "Unexpected:" (con `--debug` para el traceback) y
  logging configurado en el entrypoint. 1 d.
- F2c `doc_io.py`: único módulo que habla con sldb, solo con `sldb.api.*`
  público, con una transacción que cubre archivo + store (resuelve D6, D7 y S6).
  2-2,5 d.

**F3. Servicios de dominio (~5,5 d).** Cada uno sale de `operations.py` sobre F2; en
serie por overlap; `operations.py` queda como fachada que re-exporta.
- F3a `drawer_routing.py` (0,5 d) → (F3b, servicio de primitivas, ya no aplica: afdec7f) →
  F3c `closeout_gates.py`, con gates reales para commit y tests
  (X6; 1 d) → F3d `tasks_service.py`, sacando el parser regex de S3 (1,5 d) →
  F3e `atoms_service.py` (1,5 d).
- F3f `closure.py`: **un solo camino de cierre** (S1). El issue 2 está resuelto (opción A,
  819a8b8). Queda bloqueada solo por qué hace `advance` una vez que el cierre esté unificado. 1 d.

**F4. Grafo (~3 d, paralelo a F3 después de F2c).** Las aristas declaradas vienen
del edge index de sldb; deskops solo agrega nodos de archivo y el reporte de
faltantes; un solo esquema de ids y un solo lector de snapshot. Requiere que sldb
exponga las referencias no resueltas (gap para el coordinador de sldb).

**F5. CLI sobre registro de comandos (~3 d, después de F3).** Un registro
declarativo de comandos, args compartidos definidos una vez, `--root` resuelto en
un solo lugar (S7, S8), un renderer text/json/yaml con un envelope de error, y alias
deprecados con aviso.

**F6. Cambios de contrato de modelo (~2 d + migración, al final, una task propia).**
Sacar `from_drawer` de `__references__`, quitar `extra: allow` y el hack del
frontmatter de TaskDoc, y arreglar `MODEL_REFS`. Incluye un script que corre
`sldb models update` / `deskops desk update --apply` en los 24 stores.

**Total aproximado: ~21 días de agente** (después de afdec7f), de los cuales F0 (2 d) da valor
inmediato por sí sola.

## Decisiones pendientes del dueño

Cada decisión bloquea las tasks indicadas entre paréntesis. El issue 2 ya está decidido (opción A).

1. Qué hace `advance` con el cierre unificado (`task-rw-f3-single-closure-path`):
   A) deja de cerrar y remite a `closeout commit` (recomendada); B) llama al servicio y acepta
   `--run-dir` o `--no-run --reason`; C) se elimina `--to complete` y `advance` sigue cerrando vía
   el servicio.
2. `extract_coverage.py` (`task-rw-f4-coverage-extractor-decision`): borrarlo, o dejarlo como
   reporte opcional `deskops graph coverage`.
3. Comandos duplicados (`task-rw-f5-deprecated-aliases`): para `inbox`, `status`, `atoms list` y
   `atoms show`, alias con aviso o eliminación.
4. JSON de éxito (`task-rw-f5-output-renderer`): A) mantener las formas actuales por comando;
   B) envolverlas en `{"ok": true, "data": ...}`. El envelope de error va en los dos casos.
5. F6 en este ciclo (`task-rw-f6-taskdoc-contract-cleanup`, `task-rw-f6-migrate-tracking-stores`):
   sí o se posterga.
6. Registros archivados en `graph missing` (`task-rw-f0-graph-missing-ignores-archived-records`):
   tratamiento A) saltarlos, B) editarlos, C) informativos con exit 0 (recomendada); marca
   `record: true` en el frontmatter (recomendada), título con "archived", o sección `## Status`.
7. Verbo para borrar entradas del drawer (`task-rw-f3-drawer-entry-removal-verb`): el nombre
   (p. ej. `deskops drawer remove`), y si rechaza, avisa o sigue cuando una task activa la tiene
   en `from_drawer`.
