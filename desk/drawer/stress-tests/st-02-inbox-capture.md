# ST-02: Inbox capture stress

**Basado en:** UC-02

## Script

```bash
# 1. Capture simple
deskops inbox "we should auto-tag atoms by content"

# 2. Capture con urgencia (medio escribiendo)
deskops inbox "el grafo no esta mostrando"

# 3. Ver lo capturado
deskops inbox --list

# 4. Ver detalle
deskops inbox --show <selector>

# 5. Promover a trabajo diferido
deskops promote inbox-to-drawer-task <selector>

# 6. Promover trabajo diferido a tarea activa
deskops promote drawer-task-to-active-task <selector>
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `inbox` | ¿El mensaje se captura exactamente como se escribió? ¿O se transforma (capitaliza, wrappea, etc.)? |
| `inbox` con typo | ¿Acepta texto imperfecto? ¿O exige estructura? |
| `inbox --list` | ¿Muestra fecha/hora? ¿El orden es predecible (más reciente primero)? |
| `inbox --show` | ¿El texto original se ve igual? ¿O se perdió algo en la captura? |
| `promote inbox-to-drawer-task` | ¿Qué pasa con la nota original después del promote? ¿Se marca o desaparece? |

## Modos de fracaso

- El inbox pide más datos de los que el usuario tiene ganas de dar en el momento
- `inbox` con un string largo falla o trunca silenciosamente
- El inbox se convierte en un agujero negro — lo que entra no vuelve a salir
- No hay forma de priorizar o marcar urgencia
- `inbox list` muestra ítems sin contexto temporal ("esto lo anoté ayer o hace un mes?")
- Promover es destructivo — la nota original se pierde y no hay vuelta atrás
