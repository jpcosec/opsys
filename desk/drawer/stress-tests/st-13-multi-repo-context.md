# ST-13: Multi-repo context stress

**Basado en:** UC-13

## Script

```bash
# 1. Registrar repos
deskops repo register ~/projects/hum-ecosystem/tools/deskops
deskops repo register ~/projects/hum-ecosystem/tools/another-tool

# 2. Listar repos registrados
deskops repo list

# 3. Switch context
deskops repo switch tools/another-tool
deskops atoms list  # deberia mostrar atoms de another-tool

# 4. Switch back
deskops repo switch tools/deskops
deskops atoms list

# 5. Ver repo activo actual
deskops repo current

# 6. Unregister
deskops repo unregister tools/another-tool
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `repo register` con path absoluto vs relativo | ¿Normaliza? ¿O se guarda tal cual? |
| `repo list` | ¿Marca cuál es el activo? ¿Con un * o color? |
| `repo switch` a repo no registrado | ¿Error claro o KeyError? |
| `atoms list` después de switch | ¿Efectivamente cambió el contexto? ¿O el estado es global? |
| `repo current` | ¿El output es un path completo o un alias corto? |

## Modos de fracaso

- `repo register` requiere flags en vez de aceptar el path como positional
- El contexto activo es ambiguo — corre en el repo incorrecto sin avisar
- `repo list` muestra paths larguísimos que rompen el layout de la terminal
- Registrar el mismo repo dos veces da duplicado silencioso o error confuso
- `repo unregister` borra el repo pero no pregunta si el usuario está seguro
- Si el path del repo ya no existe, los comandos fallan con error interno en vez de "repo not found at path"
- No hay `repo switch --last` para volver al repo anterior rápido
