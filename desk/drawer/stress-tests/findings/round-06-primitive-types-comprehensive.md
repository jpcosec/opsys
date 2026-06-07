# Round 06 — Primitive types comprehensive + show/list bugs

**Source:** round-06-subagent-01, round-06-subagent-02, round-06-subagent-03

## CRITICAL: `show condition` swaps Subject and Predicate when Subject is empty

Cuando Subject está vacío, `extract_model_data` (sldb parser) absorbe el contenido de Predicate en Subject. El file markdown tiene:

```
## Subject

(empty)

## Predicate

truthy
```

Pero `show condition` muestra `Subject: truthy, Predicate: `. Es un parser bug en sldb.

## CRITICAL: `show` glob bug confirmado en TODOS los primitives

`show checklist checklist-test-checklist` → muestra `checklist-test-checklist-stress` (el archivo equivocado). Misma causa: `f"{id}*.md"` glob, `-stress` ordena antes que `.md`.

## `show routine` edges no se muestran

El archivo markdown tiene `edge-1`, `edge-2` en `## Edges`. Pero `show routine` intenta cargar cada edge ID como un EdgeDoc completo. Como `edge-1` no existe como primitive standalone, `_load_edge` devuelve None, el list comprehension lo filtra, y la CLI muestra lista vacía.

## `list --root /tmp/nonexistent` silenciosamente exitoso

`list conditions --root /tmp/nonexistent` → exit 0, sin output. Operations.py:225-226 devuelve `[]` si el directorio no existe, sin error.

## Todos los primitives se crean correctamente

condition, operator, checklist, hook, edge, routine → todos exit 0, campos correctos.

## `list` para primitives consistente

Todos usan formato `id | status | title`. Exit 0.
