# ST-14: Atom lifecycle split/merge/deprecate stress

**Basado en:** UC-14

## Script

```bash
# 1. Split atomo
deskops atoms split atom-big-idea --at new-atom-a --at new-atom-b

# 2. Ver resultado
deskops atoms list
deskops graph neighbors new-atom-a

# 3. Merge atomos
deskops atoms merge atom-alpha atom-beta --into atom-gamma

# 4. Deprecar
deskops atoms deprecate atom-old-idea --reason "superseded by atom-new-idea"

# 5. Listar incluyendo deprecados
deskops atoms list --include-deprecated

# 6. Validar grafo post-operacion
deskops graph build
deskops graph missing
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `atoms split` | ¿El contenido original se distribuye o se pierde? ¿Las referencias se migran? |
| `atoms merge` | ¿Los tags se combinan? ¿Si hay conflictos de tags, cómo se resuelven? |
| `atoms deprecate` | ¿El atomo desaparece del `list` normal o aparece con marca? |
| `graph missing` post-op | ¿Las referencias internas se actualizaron o hay broken links? |
| Dry-run | ¿Existe `--dry-run` para preview? ¿O es irreversible? |

## Modos de fracaso

- `split` sin `--at` (nombres destino) pide input interactivo o falla sin mensaje útil
- merge pierde metadata (tags, referencias) silenciosamente
- deprecate borra el archivo en vez de marcarlo — no hay vuelta atrás
- `graph missing` después de split/merge encuentra broken links que la operación debería haber prevenido
- No hay forma de ver el historial del atomo (qué contenía antes del split)
- git history: split/merge aparece como delete+create en vez de rename
- No hay rollback — si split sale mal, toca reconstruir manualmente
