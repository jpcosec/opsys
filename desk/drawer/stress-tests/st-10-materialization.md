# ST-10: Materialization stress

**Basado en:** UC-10

## Script

```bash
# 1. Materializar todo
deskops materialize

# 2. Materializar un atomo especifico
deskops materialize atom-deskops

# 3. Materializar por tag
deskops materialize --tag system:deskops

# 4. Ver que se generó
ls docs/
deskops materialize list

# 5. Re-materializar después de cambios
# (editar atomo)
deskops materialize atom-deskops
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `materialize` | ¿El output incluye un resumen (X docs generados en Y path)? |
| Output path | ¿Es configurable? ¿Predecible? ¿Obvio? |
| Materialización individual | ¿Genera un archivo limpio o un fragmento que no se entiende solo? |
| Materialización por tag | ¿Agrupa los atomos en un solo doc o genera N archivos? |
| Re-materialización | ¿Sobrescribe limpiamente? ¿Git diff es limpio? |

## Modos de fracaso

- `materialize` genera docs que son indistinguibles de los atomos originales — no hay valor agregado
- `materialize list` no existe o no encuentra lo generado
- Los docs materializados no tienen fecha/metadata de cuándo se generaron
- Materialización de un solo atomo produce un doc que referencia IDs que no existen en ese doc
- Re-materializar sin cambios sigue regenerando (no hay cache)
- El output va a una carpeta que no está en `.gitignore` — contaminando el repo
- No hay preview — no se puede ver qué va a generar sin generarlo
