# ST-07: Drift check stress

**Basado en:** UC-07

## Script

```bash
# 1. Drift check completo
deskops drift check --root .

# 2. Drift check con salida a un directorio
deskops drift check --out <dir>
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `drift check` | ¿El reporte usa colores o iconos (✓/⚠/✗)? ¿O es texto plano sin señal visual? |
| Items green | ¿Son checks reales o falsos porque el test es demasiado superficial? |
| Items red | ¿El mensaje dice "el atomo X dice Y pero el codigo hace Z"? |

## Modos de fracaso

- `drift check` siempre da green porque las verificaciones son placeholder
- `drift check` siempre da red porque los checks son irreales
- No hay forma de distinguir "no hay drift" de "no hay check implementado para esto"
- `drift acknowledge` no persiste — el item reaparece siempre
- `drift show` requiere un ID que no aparece en el reporte principal
- El reporte es párafo largo sin estructura — imposible escanear rápidamente
- El check es tan lento que el usuario deja de usarlo
