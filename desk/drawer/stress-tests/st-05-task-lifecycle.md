# ST-05: Task lifecycle stress

**Basado en:** UC-05

## Script

```bash
# 1. Ver tablero
deskops list

# 2. Ver detalle de una tarea
deskops show desk-042

# 3. Avanzar tarea por fases
deskops advance desk-042 --to in_progress

# 4. Saltarse una fase (intencional)
deskops advance desk-042 --to done
# ¿debería dejar? ¿tiene phase gates?

# 5. Avanzar tarea inexistente
deskops advance desk-999 --to in_progress

# 6. Estado después de todo
deskops list
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `list` | ¿Muestra fase actual? ¿Prioridad? ¿Asignado? ¿O solo ID y título? |
| `show` | ¿El detalle incluye historial de avances? ¿Quién movió la tarea y cuándo? |
| `advance` sin fase actual | ¿Asume una fase default o falla? |
| `advance --to done` saltándose review | ¿El phase gate lo bloquea con un mensaje claro? |
| Tarea inexistente | ¿El error identifica el problema o solo dice "not found"? |

## Modos de fracaso

- `list` muestra tareas en orden arbitrario — no se puede priorizar visualmente
- `advance` permite cualquier transición — los phase gates no existen o son inconsistentes
- `advance` a una fase en la que ya está la tarea — ¿falla, no-op, o lo permite?
- `list` después de avanzar no refleja el cambio (stale state)
- No hay `advance --undo` — si se avanza por error, no hay vuelta atrás
- El estado de la tarea vive en un archivo que se puede editar a mano, y entonces el CLI se desincroniza
