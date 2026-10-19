# ST-05: Task lifecycle stress

**Basado en:** UC-05

## Script

```bash
# 1. Ver tareas
deskops list tasks

# 2. Ver detalle de una tarea
deskops show task <id>

# 3. Ver la siguiente accion
deskops next <id>

# 4. Avanzar tarea (transicion valida)
deskops advance task <id>

# 5. Verificar closeout
deskops closeout verify --task <id>

# 6. Cerrar con commit
deskops closeout commit --task <id> --no-run --reason "..."

# 7. Avanzar tarea inexistente
deskops advance task desk-999
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `list` | ¿Muestra fase actual? ¿Prioridad? ¿Asignado? ¿O solo ID y título? |
| `show` | ¿El detalle incluye historial de avances? ¿Quién movió la tarea y cuándo? |
| `advance` sin transición válida | ¿Asume una transición default o falla? |
| `advance` con transición inválida | ¿La validación de transición lo bloquea con un mensaje claro? |
| Tarea inexistente | ¿El error identifica el problema o solo dice "not found"? |

## Modos de fracaso

- `list` muestra tareas en orden arbitrario — no se puede priorizar visualmente
- `advance` permite cualquier transición — los phase gates no existen o son inconsistentes
- `advance` a una fase en la que ya está la tarea — ¿falla, no-op, o lo permite?
- `list` después de avanzar no refleja el cambio (stale state)
- No hay `advance --undo` — si se avanza por error, no hay vuelta atrás
- El estado de la tarea vive en un archivo que se puede editar a mano, y entonces el CLI se desincroniza
