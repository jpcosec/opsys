# Round 06 — Remaining surfaces: inbox JSON, tests, Python API, mixed flags

**Source:** round-06-subagent-03, round-06-subagent-01

## `inbox --list --format json` crashes

`deskops inbox --list --format json` → `Unexpected: Object of type datetime is not JSON serializable`. Los campos `created_at` son objetos `datetime.datetime` que el JSON encoder no serializa. `--format yaml` funciona correctamente.

## `--from-yaml` overrides inline CLI flags

`add pill --from-yaml /tmp/test.yml --title "CLI Title"` → el título en el archivo es el del YAML, no `"CLI Title"`. Precedencia: YAML > CLI flags. Esto puede sorprender al usuario.

## 59/59 tests pasan

14 test files en `tests/`. Todos pasan. 4 deprecation warnings por `datetime.utcnow()`.

## Python API no documentada

- `deskops/__init__.py` es solo un docstring — sin exports, sin `__version__`, sin `__all__`
- 23 submodules, todos importables
- `main()` catch-all handler: `except Exception: raise SystemExit("Unexpected: {exc}")` — masks programming errors
- `FaqDoc` no existe, es `FAQDoc` — naming trap
- 17 Pydantic v2 models, todos construibles y serializables

## Graph resilience

Corrupted `knowledge_graph.kg.json` → `graph build` regenera correctamente.

## `deskops about --help` funciona

Minimal help. Same output.

## atoms add-namespace --example requiere prefijo

Los examples deben tener prefijo `namespace:value`. `--example ex1` solo es rechazado (probablemente validación en tag-namespaces.yaml).

## 23 `-none.md` artifacts residuales

Scattered por desk/ — de pruebas de empty YAML. No limpiados.

## Mixed from-yaml + inline → YAML gana

Precedencia: `--from-yaml` sobreescribe flags inline.

## `inbox --show` para IDs inexistentes

`deskops inbox --show nonexistent` → `Unknown inbox note: nonexistent` (exit 1). Claro.

## sldb como sibling package

`/home/jp/proyectos/hum-ecosystem/tools/sldb/src/sldb/__init__.py`. Los tests añaden `../sldb/src` a sys.path.
