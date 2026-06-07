# ST-04: Graph missing check stress

**Basado en:** UC-04

## Setup

```bash
# Meter una referencia rota manualmente en un atomo
echo 'See also: [atom-this-does-not-exist](atom-this-does-not-exist.md)' >> desk/atoms/knowledge-model/atom-self-reflection-is-a-feedback-loop.md

# Meter una referencia a un archivo que existe pero no es atomo
echo 'Implementation: [operations.py](deskops/operations.py)' >> desk/atoms/knowledge-model/atom-self-reflection-is-a-feedback-loop.md
```

## Script

```bash
# 1. Build con referencias rotas
deskops graph build

# 2. Missing check
deskops graph missing

# 3. Fix y re-check
# (editar y sacar la referencia rota)
deskops graph build
deskops graph missing
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `graph missing` con rotas | ¿Encuentra todas? ¿La provenance (archivo:línea) es correcta? |
| Referencia a archivo real (no-atomo) | ¿La marca como missing correctamente (no es nodo del grafo)? ¿O se confunde? |
| Salida con muchas rotas | ¿Es scrolleable? ¿Agrupa por tipo de referencia? |
| Después de fixear | ¿El re-build es incremental o rebuild completo? |

## Modos de fracaso

- `graph missing` reporta falsos positivos (links que son válidos pero el parser no entiende)
- `graph missing` no reporta referencias rotas obvias
- La provenance apunta a la línea incorrecta o al archivo equivocado
- El reporte mezcla broken links con otros tipos de issues sin distinguirlos
- No hay distinción entre "referencia a algo que nunca existió" vs "referencia a algo que se borró"
- Arreglar y re-check requiere rebuild completo que es lento
