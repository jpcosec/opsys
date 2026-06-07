# Round 02 — Repo subsystem half-built

**Source:** ST-13

## Lo que existe

- `repo register <name> <path>` con flags `--id`, `--description`, `--tags`, `--store`, `--pythonpath`
- Modelo `RepositoryDoc` definido en `deskops/models.py` con campos: name, id, path, status, description, tags
- Output escribe archivo YAML en el store local

## Lo que NO existe (ni en parser ni en handler)

| Comando | Estado |
|---|---|
| `repo list` | No existe |
| `repo current` | No existe |
| `repo switch` | No existe |
| `repo unregister` | No existe |

## Modelo sin registrar en store

`repo register` falla con:
```
Error: RepositoryDoc model is not registered in the store.
Register it first with: python -m sldb models add deskops.models:RepositoryDoc --store <path>
```

El modelo existe como clase Python pero falta el bootstrap en sldb. El error es claro y da la solución, pero requiere un paso manual fuera de deskops.

## Error quality

Los errores de `argparse` son consistentes (exit 2 con `invalid choice` listando opciones válidas). El error de store es claro y accionable.
