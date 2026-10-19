# ST-11: Atom scaffold and validate stress

**Basado en:** UC-11

## Script

```bash
# 1. Scaffold atomo nuevo
deskops add atom --title "Why we use pydantic over dataclasses" --five-wh-one-plus what --answer "..."

# 2. Validar atomo vacio (solo scaffold)
deskops atoms validate desk/atoms/workflow-model/atom-why-we-use-pydantic-over-dataclasses.md

# 3. Escribir contenido minimo, re-validar
deskops atoms validate desk/atoms/workflow-model/atom-why-we-use-pydantic-over-dataclasses.md

# 4. Romper el formato intencionalmente
# (sacar un campo requerido)
deskops atoms validate desk/atoms/workflow-model/atom-broken-format.md

# 5. Scaffold con nombre invalido
deskops add atom --title "" --five-wh-one-plus what --answer "..."
deskops add atom --title "a" --five-wh-one-plus what --answer "..."  # demasiado corto
deskops add atom --title "a"$'\n'"b" --five-wh-one-plus what --answer "..."  # multilinea
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `add atom` | ¿El path donde crea el archivo es predecible? ¿Lo imprime? |
| Template inicial | ¿Tiene todos los campos requeridos? ¿Incluye comentarios guía? |
| `validate` | ¿Cada error señala línea exacta? ¿El mensaje dice "falta campo X" o "error de parsing"? |
| Validación de tags | ¿Valida contra el namespace conocido? ¿O acepta cualquier tag? |
| Nombre inválido | ¿El error es claro ("title must be between 2 and 100 chars") o críptico? |

## Modos de fracaso

- `atoms new` pone el archivo en un lugar que no es donde el usuario espera
- El template tiene placeholders que no se reemplazan automáticamente
- `validate` es tan estricto que ningún atomo real pasa
- `validate` es tan laxo que un archivo vacío pasa
- El ID generado no sigue la naming convention del grupo donde se creó
- No hay `atoms new --dry-run` para ver dónde caería antes de crearlo
- Scaffold crea el archivo pero `graph build` no lo detecta (falta registro?)
