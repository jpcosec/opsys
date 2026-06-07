# ST-01: Fresh start orientation stress

**Basado en:** UC-01

## Script

```bash
# 1. First contact
deskops about

# 2. FAQ browse
deskops faq
deskops faq --topic atoms
deskops faq --topic graph

# 3. Atom discovery
deskops atoms list
deskops atoms list --tag system:deskops
deskops atoms show atom-deskops

# 4. Graph orientation
deskops graph build
deskops graph neighbors atom-deskops
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `about` | ¿Da contexto útil o solo texto genérico? ¿Invita a seguir explorando o es un callejón sin salida? |
| `faq` | ¿Las preguntas coinciden con lo que un recién llegado se preguntaría? ¿O son preguntas internas del equipo? |
| `atoms list` | ¿La salida es scrolleable y agrupable? ¿O es un muro de texto sin jerarquía? |
| `atoms show` | ¿Respeta el ancho de la terminal? ¿Muestra metadatos útiles (tags, referencias) o solo el contenido crudo? |
| `graph build` primera vez | ¿Falla porque no hay `.sldb`? ¿El error dice qué hacer? ¿O explota con traceback? |
| `graph neighbors` | Si no hay vecinos, ¿dice "no hay conexiones" o solo no imprime nada? |

## Modos de fracaso

- El usuario tiene que leer código fuente para entender qué hace deskops
- `about` y `faq` describen un mundo distinto al que `atoms list` muestra
- `graph build` requiere setup manual que no está documentado en el error
- El usuario no sabe si "terminó" la orientación — no hay un estado claro de "ok, ya entendí"
