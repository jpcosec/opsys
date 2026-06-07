# Deskops — Prioritized Fix Roadmap

## Fase 0: Quick Wins (1-2 hrs c/u, sin dependencias)

| # | Fix | Esfuerzo | Impacto | Findings |
|---|-----|----------|---------|----------|
| 1 | `list --root /tmp/nonexistent` → error msg instead of silent exit 0. En `operations.py:225`, cambiar `return []` a validación temprana | 15 min | Medio | H15 |
| 2 | Duplicate error msg en `advance task`: remover el print de `operations.py:268`, dejar solo el de CLI handler | 5 min | Bajo | C9 (parte) |
| 3 | Whitespace-only inputs: `str(value).strip()` antes de slugify | 15 min | Bajo | M20 |
| 4 | `show <type> ""` → reject empty ID con error claro. Validar `doc_id` no vacío antes de glob | 15 min | Medio | H3 |
| 5 | `add task` sin args → mostrar usage en vez de Pydantic traceback | 30 min | Medio | M9 |
| 6 | `inbox --list --format json`: agregar `default=str` o `cls=CustomEncoder` para datetime | 15 min | Medio | C12 |
| 7 | Error messages a stderr en vez de stdout en show/list/advance | 30 min | Medio | H11 |
| 8 | `--faq-path /nonexistent` → warning visible en vez de silent fallback | 15 min | Bajo | M1 |

**Total Fase 0: ~2.5 horas**

---

## Fase 1: Data Integrity (4-8 hrs c/u, algunas dependencias)

| # | Fix | Esfuerzo | Dependencias | Impacto | Findings |
|---|-----|----------|-------------|---------|----------|
| 9 | `_resolve_glob` en operations.py:801 — cambiar `f"{id}*.md"` por exact match, y si no hay match exacto recién probar glob | 1 hr | — | Crítico | C2, C11 |
| 10 | `_normalize_task_payload` en operations.py: usar `_coerce_list()` para todos los list fields (references, depends_on, pills, files, validation, history, tags) | 30 min | — | Alto | C7, H6 |
| 11 | `compile_artifact_spec`: validar que `title` no sea None/vacío antes de escribir. `raw_payload.get("title") or ""` → `raw_payload["title"]` con KeyError manejado | 1 hr | — | Crítico | C4 |
| 12 | `repo register`: checkear duplicado en store ANTES de escribir archivo | 1 hr | — | Alto | C5 |
| 13 | `init`: agregar paso de registro de modelos en local store (llamar a `_register_deskops_models` con root path) | 2 hrs | — | Crítico | C6 |
| 14 | `--from-yaml`: ordenar operaciones para escribir archivos SOLO si toda la validación pasa. O implementar rollback con `try/finally` | 3 hrs | — | Alto | H5 |
| 15 | `--from-yaml` + inline flags: documentar precedencia. O hacer que CLI flags sobreescriban YAML (más intuitivo) | 30 min | — | Medio | H14 |
| 16 | `list inbox-notes`: arreglar glob pattern para matchear date-prefixed filenames o usar directory scan sin prefix filter | 30 min | — | Crítico | C3 |

**Total Fase 1: ~9.5 horas**

---

## Fase 2: Graph & Data Layer (4-12 hrs c/u)

| # | Fix | Esfuerzo | Dependencias | Impacto | Findings |
|---|-----|----------|-------------|---------|----------|
| 17 | KG JSON edge serialization: fixear `GraphSnapshot.serialize()` en snapshot.py para incluir `role`, `target`, `source_kind`, `confidence`, `provenance` correctamente | 3-6 hrs | — | Crítico | C8 |
| 18 | `graph build`: también rebuild `knowledge_graph.nx.json` | 1 hr | — | Medio | M7 |
| 19 | `graph neighbors --help`: documentar formato `type:id` | 15 min | — | Bajo | M8 |
| 20 | `--root` validation: agregar `Path(root).resolve().exists()` check global en CLI wrapper | 30 min | 21 | Medio | M16 |
| 21 | `list atoms`: recursive glob para incluir knowledge-model/ y workflow-model/ subdirectorios | 1 hr | — | Medio | L7 |
| 22 | `graph missing`: conectar `self_reflection.py` en pipeline de `graph build` | 2 hrs | — | Bajo | U3 |
| 23 | `list rituals` + `list boards`: arreglar filename pattern para incluir `closeout.md`, `Board.md` etc (usar internal ID: field si filename no matchea) | 1 hr | 9 | Medio | M12 |

**Total Fase 2: ~12.5 horas**

---

## Fase 3: Error Handling UX (2-4 hrs c/u)

| # | Fix | Esfuerzo | Dependencias | Impacto | Findings |
|---|-----|----------|-------------|---------|----------|
| 24 | `main.py:224`: sacar `except Exception` catch-all. Manejar errores específicos (FileNotFoundError, KeyError, ValidationError) con mensajes user-friendly | 2 hrs | — | Alto | H2 |
| 25 | `list tasks` / `list pills`: skip archivos inválidos con warning en vez de crash total | 3 hrs | — | Alto | H1 |
| 26 | `show routine` edges: mostrar IDs de edges inline desde payload, no intentar cargar EdgeDoc objects | 1 hr | — | Medio | H13 |
| 27 | `show condition` Subject/Predicate: fix en sldb extract_model_data o workaround en operations.py | 3-6 hrs | — | Alto | C10 |
| 28 | Very long title: truncar slug a 200 chars ANTES de crear filename | 30 min | — | Medio | H12 |
| 29 | `add task` sin args: attahear handler para mostrar usage en vez de dejar que Pydantic valide payload vacío | 1 hr | — | Medio | M9 |
| 30 | `list` output formats: estandarizar a `id | status | title` para todos los tipos (o agregar `--format` flag) | 2 hrs | — | Bajo | M11 |

**Total Fase 3: ~14.5 horas**

---

## Fase 4: Feature Gaps (varía, 4-40 hrs)

| # | Fix | Esfuerzo | Dependencias | Impacto | Findings |
|---|-----|----------|-------------|---------|----------|
| 31 | `advance task --to <state>`: implementar transiciones stateful usando `deskops.runtime.primitives` (TransitionResult existe) | 8-16 hrs | 1 (sldb parser fix) | Crítico | C1, C9 |
| 32 | Fix sldb DataExtractor: no usar positional map indices; usar heading name matching | 4-8 hrs | — | Crítico | C1 |
| 33 | Consistent IDs: `repo register` y `add repository` deben producir IDs con el mismo formato | 1 hr | — | Medio | M19 |
| 34 | `--version` flag global | 30 min | — | Bajo | L2 |
| 35 | `--format json` en list/show commands | 4-8 hrs | — | Bajo | L1 |
| 36 | Unificar FAQ: `deskops faq` debería mostrar tanto docs/faq.md como desk/faq/ | 4 hrs | — | Medio | H9 |
| 37 | Directorios consistentes: pills → desk/pills/, boards → desk/boards/ | 2 hrs | — | Bajo | U6 |
| 38 | `add step --ritual <id>` para cross-link | 2 hrs | — | Bajo | Workflows |
| 39 | Spec engine CLI: `deskops spec validate/show/render-mermaid` | 8-16 hrs | — | Bajo | L8 |
| 40 | Materializers CLI: `deskops atoms materialize <id>` | 4-8 hrs | — | Bajo | L6 |
| 41 | `dry-run` flag global | 2 hrs | — | Bajo | L3 |

**Total Fase 4: ~45 horas**

---

## Orden recomendado para arrancar

```
Fase 0 (2.5h) → Fase 1 (9.5h) → Fase 3 items 24-25 (5h) → Fase 2 (12.5h) → Fase 3 resto (9.5h) → Fase 4 (45h)
```

### Por qué este orden:

1. **Fase 0**: bugs de 5-30 min que mejoran UX inmediatamente
2. **Fase 1**: bugs de integridad de datos (show/show artifact equivocado, strings spliteados, garbage artifacts, repo overwrite)
3. **Fase 3 items 24-25**: catch-all exception handler + list crash — los dos errores más visibles
4. **Fase 2**: graph edge serialization, nx.json stale, recursive atoms
5. **Fase 3 resto**: show condition swap, show routine edges, long title
6. **Fase 4**: advance task (depende de sldb fix), FAQ unify, spec CLI, materializers, version flag

### Si solo tenés 1 día (8h):

```
1. _resolve_glob exact match   (1h)    — C2, C11: show bug crítico
2. _coerce_list fix            (0.5h)  — C7: strings → chars
3. empty YAML validation       (1h)    — C4: garbage artifacts
4. init + model registration   (2h)    — C6: repo register post-init
5. main.py catch-all removal   (2h)    — H2: path leaks + unexpected
6. list skip bad files         (1.5h)  — H1: crash total
                               = 8h
```

### Si solo tenés 1 semana (40h):

```
Día 1: Fase 0 completa + _resolve_glob + _coerce_list (3h)
Día 2: Fase 1 completa (9.5h)
Día 3: Fase 3 items 24-25-26-27 (8h)
Día 4: Fase 2 items 17-18-20-21 (8h)
Día 5: Fase 3 resto + Fase 4 items 31-32 (advance task) (11.5h)
       = 40h
```
