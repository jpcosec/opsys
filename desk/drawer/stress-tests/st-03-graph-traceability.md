# ST-03: Graph traceability stress

**Basado en:** UC-03

## Script

```bash
# 1. Build graph
deskops graph build

# 2. Navegar vecinos de un atomo clave
deskops graph neighbors atom-materialization-contracts-bind-source-output-validation

# 3. Navegar vecinos de algo que NO es atomo (spec, source file)
deskops graph neighbors specs/my-spec
deskops graph neighbors deskops/operations.py

# 4. Seguir cadena: vecinos de vecinos
deskops graph neighbors atom-specs-formalize-atoms-as-contracts

# 5. Nodo sin conexiones
deskops graph neighbors atom-orphaned-idea
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `graph neighbors` con ID válido | ¿Los roles de arista son legibles? ¿"related_to" o "implements" o "contradicts"? |
| Salida con muchos vecinos | ¿Se trunca? ¿Se agrupa por rol? ¿O es una lista plana sin orden? |
| Nodo sin conexiones | ¿El mensaje es "no connections" o simplemente no imprime nada? |
| IDs con caracteres especiales (guiones, puntos) | ¿El parsing de argumentos funciona? |
| Cadena de vecinos | ¿Puede el usuario seguir el grafo sin tener que recordar IDs? ¿Hay hint de label? |

## Modos de fracaso

- `neighbors` requiere el snapshot path exacto — el usuario no sabe dónde está
- Los roles de arista son técnicos ("EDGE_TYPE_47") en vez de semánticos
- El grafo muestra conexiones pero no se puede abrir el nodo destino desde la salida
- Seguir cadena es impracticable porque hay que copiar-pegar IDs manualmente
- `neighbors` es muy lento incluso después del build
- El label del nodo es el filename en vez del título semántico
