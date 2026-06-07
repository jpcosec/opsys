# Round 05 — Advance task deep dive + graph missing

**Source:** round-05-subagent-02

## CRITICAL: sldb DataExtractor misparses TaskDoc markdown

El template de TaskDoc tiene secciones en orden con `⸢...⸥` anchors. Cuando el archivo real tiene una cantidad distinta de checklist items que el template, los map indices del AST markdown se desplazan, causando que el extractor **cross-wire los campos**:

- `routine` → recibe el valor de `current_node` (un checklist ID, no el routine ID)
- `current_node` → queda vacío porque lookup en posición incorrecta
- `files` → recibe checklist IDs

Esto rompe `advance task` completamente porque `_load_routine()` busca un ID de routine que es en realidad un ID de checklist, no encuentra nada, y devuelve "task has no routine".

## Duplicate error message en advance

`advance task` imprime "has no routine — cannot advance" DOS veces: una en `operations.py:268` y otra en `operations.py:148` (CLI handler).

## graph build no actualiza knowledge_graph.nx.json

`graph build` escribe `knowledge_graph.kg.json`, `semantic_dag.yaml`, `semantic_index.yaml` pero NO actualiza `knowledge_graph.nx.json`. Ese archivo queda stale desde el primer build.

## graph missing funcional

`deskops graph missing` reporta dangling references con source file + line number. Formato claro.

## graph neighbors sin documentación de prefijos

`graph neighbors atom:atom-deskops` funciona, pero `graph neighbors atom-deskops` falla con "graph node not found". `--help` no documenta el formato `type:id`.

## add task sin args → Pydantic cryptic error

`deskops add task` sin flags → `Unexpected: 2 validation errors for TaskDoc ... id Field required, status Field required`. Debería mostrar usage/help.

## Empty string payload crea task con título "None"

`deskops add task ''` → exit 0, crea `task-none.md` con título `# None`.
