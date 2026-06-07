# ST-02: Inbox capture stress

**Basado en:** UC-02

## Script

```bash
# 1. Capture simple
deskops inbox add "we should auto-tag atoms by content"

# 2. Capture con urgencia (medio escribiendo)
deskops inbox add "el grafo no esta mostrando"

# 3. Ver lo capturado
deskops inbox list

# 4. Ver detalle
deskops inbox show 1

# 5. Categorizar a posteriori
deskops inbox tag 1 --add topic:graph

# 6. Promover a trabajo real
deskops inbox promote 1 --to drawer
# o
deskops inbox promote 1 --to task
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `inbox add` | ¿El mensaje se captura exactamente como se escribió? ¿O se transforma (capitaliza, wrappea, etc.)? |
| `inbox add` con typo | ¿Acepta texto imperfecto? ¿O exige estructura? |
| `inbox list` | ¿Muestra fecha/hora? ¿El orden es predecible (más reciente primero)? |
| `inbox show` | ¿El texto original se ve igual? ¿O se perdió algo en la captura? |
| `inbox promote` | ¿Qué pasa con la nota original después del promote? ¿Se marca o desaparece? |

## Modos de fracaso

- El inbox pide más datos de los que el usuario tiene ganas de dar en el momento
- `inbox add` con un string largo falla o trunca silenciosamente
- El inbox se convierte en un agujero negro — lo que entra no vuelve a salir
- No hay forma de priorizar o marcar urgencia
- `inbox list` muestra ítems sin contexto temporal ("esto lo anoté ayer o hace un mes?")
- Promover es destructivo — la nota original se pierde y no hay vuelta atrás
