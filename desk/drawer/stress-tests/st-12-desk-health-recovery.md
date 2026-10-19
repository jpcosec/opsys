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
deskops doctor --root .

# 2. Auto-fix
deskops doctor --repair

# 3. Re-check después del fix
deskops doctor --root .
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `doctor` con archivo faltante | ¿Detecta que falta un atomo referenciado? |
| `doctor` con .sldb corrupto | ¿El error es "can't parse .sldb/core/something.yaml: line 1" o "something went wrong"? |
| `doctor` con desk sano | ¿El output es "✓ all good" o no imprime nada? |
| `--repair` | ¿Qué porcentaje de los issues se puede auto-fixear? ¿El resto da instrucciones? |

## Modos de fracaso

- `doctor` es otro nombre para `graph missing` — no cubre otras dimensiones
- `doctor` siempre dice "ok" aunque el desk esté roto (checks no implementados)
- `--repair` empeora las cosas (ej: regenerate snapshot vacío que sobreescribe el bueno)
- No hay `doctor --backup` antes del fix para poder revertir
- Las guías de reparación son párrafos de documentación en vez de comandos para copiar-pegar
- `doctor` es lento porque corre todos los checks secuencialmente
- El desk roto bloquea todos los comandos — no se puede ni pedir ayuda
