# ST-12: Desk health and recovery stress

**Basado en:** UC-12

## Setup

```bash
# Romper el desk intencionalmente
rm desk/atoms/knowledge-model/atom-self-reflection-is-a-feedback-loop.md
echo "garbage" > .sldb/core/something.yaml
```

## Script

```bash
# 1. Health check
deskops status

# 2. Auto-fix
deskops status --fix

# 3. Re-check después del fix
deskops status

# 4. Repair manual guiado
deskops status --guide
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `status` con archivo faltante | ¿Detecta que falta un atomo referenciado? |
| `status` con .sldb corrupto | ¿El error es "can't parse .sldb/core/something.yaml: line 1" o "something went wrong"? |
| `status` con desk sano | ¿El output es "✓ all good" o no imprime nada? |
| `--fix` | ¿Qué porcentaje de los issues se puede auto-fixear? ¿El resto da instrucciones? |
| `--guide` | ¿Las instrucciones son accionables ("run: deskops atoms restore atom-X") o vagas? |

## Modos de fracaso

- `status` es otro nombre para `graph missing` — no cubre otras dimensiones
- `status` siempre dice "ok" aunque el desk esté roto (checks no implementados)
- `--fix` empeora las cosas (ej: regenerate snapshot vacío que sobreescribe el bueno)
- No hay `status --backup` antes del fix para poder revertir
- Las guías de reparación son párrafos de documentación en vez de comandos para copiar-pegar
- `status` es lento porque corre todos los checks secuencialmente
- El desk roto bloquea todos los comandos — no se puede ni pedir ayuda
