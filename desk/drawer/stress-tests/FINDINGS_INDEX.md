# Deskops UX Stress-Tests — Findings Index

## Por comando

### `inbox`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| H11 | HIGH | `--list --format json` crash: datetime not serializable | round-06-remaining |
| M2 | MEDIUM | slugification pierde UTF-8, filename muy largo es inidentificable | round-01-inbox |
| L1 | LOW | sin duplicate detection en inbox | round-01-inbox |
| U1 | INFO | `--desk-root` vs `--root` — flag naming inconsistente | round-05-edge |
| U2 | INFO | `inbox --list` vs `list inbox-notes` — dos commands, resultados distintos | round-05-workflows |

### `faq`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| M1 | MEDIUM | `--faq-path /nonexistent` → silent fallback al default, sin warning | round-05-repo |
| M2 | MEDIUM | JSON/YAML schema inconsistency (list wrapped, single not) | round-05-repo |
| H9 | HIGH | `deskops faq` (docs/faq.md) y `deskops add faq-doc` (desk/faq/) son dos sistemas separados que nunca interactúan | round-05-workflows |
| M15 | MEDIUM | YAML type coercion: `created_at: 2026-01-01` → `datetime.date`, crash | round-05-from-yaml |
| L9 | LOW | `faq` list output tiene `answer: null` — no se puede bulk-export | round-05-repo |

### `repo register`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C5 | CRITICAL | overwrites file antes de check store → disco inconsistente con índice | round-05-repo |
| C6 | CRITICAL | `init` no registra modelos → `repo register` falla post-init | round-05-repo |
| M3 | MEDIUM | no valida que path exista (`/nonexistent/path` aceptado) | round-05-repo |
| M4 | MEDIUM | slug collision: `"my repo"` y `"My Repo"` → mismo slug, segundo overwrites | round-05-repo |
| M5 | MEDIUM | empty name `""` → Pydantic traceback | round-05-repo |
| M19 | MEDIUM | `repo register deskops .` produce ID `deskops`; `add repository --name deskops-alt` produce ID `repo-deskops-alt` | round-05-workflows |

### `graph`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C8 | CRITICAL | KG JSON edges: 68 edges con `role=None target=None`; NX snapshot correcto | round-04-graph |
| H7 | HIGH | 253 nodos, 0 edges en atom nodes; 68 edges en non-atom nodes | round-04-graph |
| M7 | MEDIUM | `graph build` no actualiza `.nx.json` — queda stale | round-05-advance |
| M8 | MEDIUM | `graph neighbors --help` no documenta formato `type:id` (atom:, task:, issue:) | round-05-advance |
| M16 | MEDIUM | `--root` acepta cualquier path sin validación | round-04-graph, round-05-edge |
| L7 | LOW | `list atoms` solo ve 4 en desk/atoms/ root; ignora 60 en subdirectorios | round-01-graph |
| U3 | INFO | self-reflection module existe pero no está conectado al pipeline | round-04-graph |
| U4 | INFO | `find_missing_snapshot_targets` duplicado en checks.py y self_reflection.py | round-04-graph |
| U5 | INFO | Graph resilience: corrupted kg.json → rebuild OK | round-06-remaining |

### `add task`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C1 | CRITICAL | sldb DataExtractor misparses TaskDoc cuando checklist count != template → cross-wire de fields | round-05-advance |
| C7 | CRITICAL | `_normalize_task_payload` usa `list()` en vez de `_coerce_list()` → strings spliteados en caracteres | round-05-from-yaml |
| C9 | CRITICAL | `advance task` no funcional: sin `--to`, routine corrupto, msg duplicado | round-05-advance |
| H5 | HIGH | `--from-yaml` sin rollback: escribe files, falla post-facto, huérfanos | round-04-from-yaml |
| H6 | HIGH | `list()` bug: `pills: single-ref` → `['s','i','n','g','l','e','-','r','e','f']` | round-05-from-yaml |
| M9 | MEDIUM | `add task` sin args → Pydantic traceback, no usage | round-05-advance |
| M10 | MEDIUM | `''` (empty string payload) → crea `task-none` con título "None" | round-05-edge |
| M20 | MEDIUM | whitespace-only `--title "  "` aceptado, slug genérico | round-05-edge |
| L3 | LOW | `--dry-run` no existe | round-05-edge |
| L17 | LOW | Pydantic tracebacks al usuario | round-05-advance |

### `add` (otros tipos)
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C4 | CRITICAL | empty YAML `{}` crea basura para 8 tipos: pill, ritual, board, atom, repository, inbox-note, faq-doc, step | round-05-from-yaml |
| H14 | HIGH | `--from-yaml` overrides inline flags silenciosamente (YAML gana) | round-06-remaining |
| M12 | MEDIUM | rituales `closeout.md`, `execution.md`, `testing.md` invisibles (filename != `ritual-*`) | round-05-list |
| M13 | MEDIUM | `show ritual` usa ID: field vs `show pill` usa filename stem | round-05-list |
| M16 | MEDIUM | whitespace-only `--title` aceptado sin validación | round-05-edge |
| M19 | MEDIUM | `add repository` produce IDs con `repo-` prefix; `repo register` no | round-05-workflows |
| L4 | LOW | `atoms` solo tiene `add-namespace` — no list/show/new/validate/split/merge | round-01-nomenclature |
| L5 | LOW | `repo` solo tiene `register` — no list/current/switch/unregister | round-02-repo |
| L6 | LOW | 6 conceptos sin CLI: drift, materialize, status, closeout, validate, graph reflect | round-01-nomenclature |
| U6 | INFO | `board` escribe a `desk/tasks/`, `pill` escribe a `desk/contexts/` — directorios no intuitivos | round-05-workflows |

### `advance task`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C1 | CRITICAL | sldb DataExtractor misparses: routine y current_node cross-wired | round-05-advance |
| C9 | CRITICAL | sin flag `--to`, routine field corrupto, "has no routine" impreso 2x | round-05-advance |
| M9 | MEDIUM | sin `--root`, task no encontrada (scope issue) | round-05-advance |
| U7 | INFO | Runtime primitives tienen `TransitionResult` — advance task no lo usa | round-06-hidden |

### `list`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C3 | CRITICAL | `list inbox-notes` muestra 2 de 13 (glob incompatible con date-prefix) | round-05-list |
| H1 | HIGH | `list tasks` / `list pills` crash total por 1 archivo inválido | round-05-list |
| H15 | HIGH | `list --root /tmp/nonexistent` → exit 0, sin output, sin error | round-06-primitives |
| M11 | MEDIUM | 3 formatos de output distintos según el tipo | round-05-list |
| M12 | MEDIUM | `list rituals` no encuentra `closeout.md` etc (filename no matchea `ritual-*`) | round-05-list |
| U2 | INFO | `list inbox-notes` vs `inbox --list`: dos comandos, resultados distintos | round-05-workflows |

### `show`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C2 | CRITICAL | `_resolve_glob` con `f"{id}*.md"` → suffix match gana, muestra artifact equivocado | round-05-list |
| C10 | CRITICAL | `show condition` con Subject vacío → Subject/Predicate swapped | round-06-primitives |
| C11 | CRITICAL | glob bug confirmado en ALL 15 tipos | round-06-primitives |
| H2 | HIGH | 13/15 show types leakean paths absolutos con prefix "Unexpected:" | round-05-list |
| H3 | HIGH | `show <type> ""` matchea TODO via `*.md` glob | round-05-list |
| H13 | HIGH | `show routine` edges no se muestran (carga EdgeDoc objects, filtra None) | round-06-primitives |
| M13 | MEDIUM | `show ritual` vs `show pill` — lógica de lookup inconsistente | round-05-list |
| U8 | INFO | `show board` mislabel: tags mostrados como "rituals:" | round-05-workflows |

### `desk install`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| M6 | MEDIUM | no crea directorio target — requiere `mkdir -p` manual | round-05-repo |
| M18 | MEDIUM | no crea `.sldb` — user necesita `init` aparte | round-05-repo |
| L12 | LOW | `desk install` + `init` = 2 pasos para algo que debería ser 1 | round-05-repo |

### `init`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| C6 | CRITICAL | `init` no registra modelos → `repo register` falla post-init | round-05-repo |
| H8 | HIGH | `bootstrap` (global) vs `init` (local) — naming confuso, scope overlap | round-05-repo |

### `atoms add-namespace`
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| L4 | LOW | único subcomando de `atoms`; falta list/show/new/validate/split/merge | round-01-nomenclature |
| U9 | INFO | --example requiere prefijo `namespace:value` — validación ok | round-06-remaining |

### Python API
| # | Severidad | Hallazgo | Archivo |
|---|-----------|----------|---------|
| L8 | LOW | Spec engine (loader, compiler, mermaid) con cero CLI | round-02-spec |
| U10 | INFO | `deskops/__init__.py` solo docstring — sin `__version__`, sin `__all__` | round-06-remaining |
| U11 | INFO | 23 submodules, todos importables; 17 Pydantic models | round-06-remaining |
| U12 | INFO | `main()` catch-all: `except Exception: SystemExit("Unexpected: {exc}")` | round-06-remaining |
| U13 | INFO | `FaqDoc` no existe, es `FAQDoc` — naming trap | round-06-remaining |
| U14 | INFO | Mermaid renderer + materializers = código funcional, sin CLI | round-06-hidden |

## Por severidad

### CRITICAL (12)
C1 → advance task / sldb parser cross-wire
C2 → show glob bug: `f"{id}*.md"` devuelve artifact equivocado
C3 → list inbox-notes: 2 de 13
C4 → empty YAML `{}` crea 8 garbage artifacts
C5 → repo register: overwrite antes de check
C6 → init no registra modelos
C7 → `list()` en vez de `_coerce_list()`: strings → chars
C8 → KG JSON edges: role/target null
C9 → advance task no funcional
C10 → show condition: Subject/Predicate swapped
C11 → show glob bug confirmado en 15/15 tipos
C12 → inbox --list --format json: datetime crash

### HIGH (15)
H1 → list tasks/pills crash total por 1 archivo
H2 → 13/15 show types leakean paths absolutos
H3 → show "" matchea todo
H4 → show task/repository: artifact equivocado
H5 → --from-yaml sin rollback
H6 → list() bug: pills strings → chars
H7 → graph: 253 nodos, 0 edges atom
H8 → bootstrap vs init naming/scope
H9 → dos FAQ systems separados
H10 → list inbox-notes: 11 de 13 invisibles
H11 → error messages a stdout, no stderr
H12 → 10K chars crash: OSError filename too long
H13 → show routine edges no display
H14 → --from-yaml overrides inline flags
H15 → list --root nonexistent: exit 0 sin error

### MEDIUM (16)
M1–M20 (ver tabla por comando arriba)

### LOW (14)
L1–L17 (ver tabla por comando arriba)

## Por causa raíz

### Bug en sldb
C1, C10 — DataExtractor positional map indices frágiles

### Bug en operations.py
C2, C11 — `_resolve_glob` usa `f"{id}*.md"` (debería preferir match exacto)
C7, H6 — `_normalize_task_payload` usa `list()` en vez de `_coerce_list()`
H5 — `_append_task_to_board` falla después de writes
H15 — list primitives returns `[]` si dir no existe

### Bug en models.py / spec
C4 — `compile_artifact_spec` usa `.get("title")` → None → "None"
H9 — `FAQDoc` usa `docs/faq.md`, `add faq-doc` usa `desk/faq/`
H14 — YAML payload merge, flags sobrescriben pero YAML gana

### Bug en main.py (CLI layer)
H2, H3 — `except Exception: SystemExit("Unexpected: {exc}")` catch-all
H11 — error messages a stdout
M9 — `add task` sin args → Pydantic error, no usage

### Bug en graph/
C8 — KG JSON serialization pierde role/target
M7 — `knowledge_graph.nx.json` no rebuild
H7 — 0 edges en atom nodes

### Bug en repo register
C5 — file write antes de store check
M3 — no path validation
M4 — slug collision sin warning

### Bug en init/bootstrap
C6 — `init` no registra modelos
H8 — naming confuso, scope overlap

### Feature gaps
L4 — atoms solo add-namespace
L5 — repo solo register
L6 — 6 concepts sin CLI (drift, materialize, etc.)
L8 — spec engine sin CLI
L3 — no --dry-run
L2 — no --version
L1 — no --format json en list/show
U7 — Runtime primitives con TransitionResult, advance task no lo usa
U14 — Mermaid + materializers: código, no CLI

### UX inconsistency
M11 — 3 formatos de output en list
M12 — rituales/boards invisibles por filename mismatch
M13 — show ritual vs show pill: lookup inconsistente
M16 — --root sin validación
M20 — whitespace-only inputs aceptados
U6 — directorios no intuitivos (pills en contexts, boards en tasks)
U8 — show board mislabel: rituals: workspace:desk
