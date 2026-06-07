# ST-08: Closeout ritual stress

**Basado en:** UC-08

## Script

```bash
# 1. Closeout completo
deskops closeout

# 2. Closeout con fase especifica
deskops closeout --phase graph-building

# 3. Closeout falla — ver que falta
deskops closeout --verbose

# 4. Corregir lo que falta y re-ejecutar
# (various fixes)
deskops closeout
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `closeout` | ¿El output dice PASS/FAIL claramente? ¿O hay que escudriñar? |
| Detalle de fallo | ¿Cada fallo dice qué cheque se ejecutó, qué esperaba, y qué encontró? |
| Fase específica | ¿Corre solo los checks relevantes a esa fase, o es un alias para correr todo? |
| Re-ejecución | ¿Los items que ya pasaron se cachean o se re-ejecutan siempre? |

## Modos de fracaso

- `closeout` siempre falla con "algo está mal" sin decir qué
- `closeout` siempre pasa aunque el desk esté roto (checks vacíos)
- No hay closeout parcial — si una fase falla no se puede continuar con las demás
- Los mismos checks que `graph missing` y `drift check` se re-ejecutan en closeout sin compartir resultados
- El closeout es una caja negra: no se puede ver qué checks va a correr sin ejecutarlo
- Bypassear el closeout es trivial (solo no ejecutarlo) — no hay integración con `advance --to done`
