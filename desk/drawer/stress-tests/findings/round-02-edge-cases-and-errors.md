# Round 02 — Edge cases and error quality

**Source:** ST-12

## --root validation

| Comando | Root inválido | Comportamiento |
|---|---|---|
| `list atoms --root /tmp` | Dir sin desk | Exit 0, sin output, sin error |
| `graph build --root /tmp` | Dir sin desk | Crea `.sldb/runtime/knowledge_graph.kg.json` adentro de `/tmp` — contamina el filesystem |
| `graph build --root /tmp/vacio` | Dir vacío | Crea estructura `.sldb` igual |
| `list atoms --root "/path with spaces"` | Path con espacios | Exit 0, sin output, sin error |

Ningún comando valida que `--root` apunte a un directorio con estructura de desk. `graph build` es especialmente peligroso porque **crea** estructura sldb donde sea.

## add task sin args

```
deskops add task
```
→ dump de Pydantic validation error (traceback crudo). El usuario ve un error interno de Python en vez de un mensaje amigable.

En cambio:
- `deskops add pill` → funciona, auto-genera `pill-none.md`
- `deskops add routine` → funciona, auto-genera `routine-none.md`

`add task` es el único que explota.

## add pill va a desk/contexts/ no desk/pills/

```
deskops add pill --title test-pill
→ desk/contexts/test-pill.md
```

El usuario esperaría `desk/pills/`. El `list pills` lee de `desk/contexts/` así que el comando y el listado son consistentes entre sí, pero el nombre del directorio contradice la intuición.

## Partial commands

Todos los comandos con subcomandos (`graph`, `atoms`, `repo`, `desk`) se comportan igual: exit 2 con `required argument` y lista de choices. Consistente.

## Vague show

Todos los `show <kind>` sin ID dan el mismo error argparse genérico: `error: the following arguments are required: <id>`. Funcional pero sin hint de qué IDs existen.
