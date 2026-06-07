# ST-15: CI integration stress

**Basado en:** UC-15

## Script

```bash
# Simular lo que correria en CI

# 1. Build graph
deskops graph build --ci

# 2. Missing check (exit non-zero si hay missing)
deskops graph missing --ci

# 3. Drift check (exit non-zero si hay drift)
deskops drift check --ci

# 4. Closeout (exit non-zero si no pasa)
deskops closeout --ci-mode

# 5. Ver exit codes
echo $?
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `--ci` flag | ¿Cambia el output (menos verbose, más parseable)? ¿O es igual que local? |
| Exit codes | ¿Cada comando distingue "error real" (2) de "found issues" (1) de "success" (0)? |
| Output en CI | ¿Los mensajes son grep-friendly? ¿O tienen colores/formatos que no funcionan en logs CI? |
| Dependencias | ¿Deskops requiere cosas que no están en un entorno CI mínimo (git config, home dir)? |
| Tiempo | ¿El pipeline completo es suficientemente rápido para un PR check? |

## Modos de fracaso

- `--ci` no existe o es idéntico al modo local — output con colores ANSI crudos en logs
- Exit code siempre 0 aunque haya missing references
- Exit code siempre 1 porque un check no implementado falla siempre
- Deskops requiere una terminal interactiva o `$HOME/.config/deskops` que no existe en CI
- `graph build` tarda 5+ minutos — nadie espera, lo sacan del CI
- Los paths en la salida de CI son absolutos (del runner) e inservibles para el developer
- El developer no puede reproducir el error localmente porque `--ci` mode hace cosas distintas
- No hay CI-only checks — lo que pasa en CI debería poder pasar local
