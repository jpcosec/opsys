# ST-09: Self-reflection stress

**Basado en:** UC-09

## Script

```bash
# 1. Build graph
deskops graph build

# 2. Self-reflection
deskops graph reflect

# 3. Reflection detallada
deskops graph reflect --verbose

# 4. Reflection por tipo de hallazgo
deskops graph reflect --kind orphans
deskops graph reflect --kind cycles
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `graph reflect` sin build previo | ¿Falla con "build the graph first" o corre sobre lo que haya? |
| Hallazgos | ¿Son concretos ("atomo X no tiene referencias") o vagos ("hay nodos desconectados")? |
| Orphans | ¿Diferencia entre "intencionalmente standalone" y "genuinamente huérfano"? |
| Ciclos | ¿Reporta el ciclo exacto (A→B→C→A) o solo "there's a cycle"? |
| `--verbose` | ¿Agrega información útil o solo ruido? |
| `--kind` | ¿Filtra bien? ¿Muestra kinds válidos si se pasa uno inválido? |

## Modos de fracaso

- `graph reflect` siempre encuentra lo mismo — el reportaje es ruido repetitivo
- `graph reflect` nunca encuentra nada útil — ¿para qué existe?
- Los hallazgos no tienen actionable next step — "hay un ciclo" ¿y ahora qué hago?
- No hay forma de silenciar hallazgos conocidos (acknowledge pattern)
- `--kind` acepta cualquier string sin validar y devuelve vacío — el usuario piensa que no hay hallazgos
- Los términos ("orphan", "cycle") no están definidos en ninguna parte — el usuario no sabe qué significan
