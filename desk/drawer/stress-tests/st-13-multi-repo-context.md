# ST-13: Multi-repo context stress

**Basado en:** UC-13

## Script

```bash
# 1. Registrar repos
deskops repo register ~/projects/hum-ecosystem/tools/deskops
deskops repo register ~/projects/hum-ecosystem/tools/another-tool

# 2. Ver repo activo actual
deskops repo whoami

# 3. Ver los repos registrados: ls desk/registry/

# 4. Remover repo
deskops repo remove <selector>
```

## Puntos de estrés

| Paso | Qué mirar |
|---|---|
| `repo register` con path absoluto vs relativo | ¿Normaliza? ¿O se guarda tal cual? |
| `repo whoami` | ¿Dice con claridad qué repo resuelve la raíz actual? |
| `repo remove` de un repo no registrado | ¿Error claro o KeyError? |
| `repo whoami` | ¿El output es un path completo o un alias corto? |

## Modos de fracaso

- `repo register` requiere flags en vez de aceptar el path como positional
- El contexto activo es ambiguo — corre en el repo incorrecto sin avisar
- `repo whoami` o `repo remove` muestran paths larguísimos que rompen el layout de la terminal
- Registrar el mismo repo dos veces da duplicado silencioso o error confuso
- `repo remove` borra el repo pero no pregunta si el usuario está seguro
- Si el path del repo ya no existe, los comandos fallan con error interno en vez de "repo not found at path"
- No hay `repo switch --last` para volver al repo anterior rápido
