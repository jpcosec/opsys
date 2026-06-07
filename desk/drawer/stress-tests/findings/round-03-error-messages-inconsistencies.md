# Round 03 — Error message inconsistencies

**Source:** ST-show-nonexistent, ST-pills-deep

## Dos estilos de "not found"

| Grupo | Mensaje | Calidad |
|---|---|---|
| task, routine | `No {type} found for {id}` | ✅ Limpio, user-facing |
| Los otros 13 tipos | `Unexpected: No artifact.{ext} file found for id '{id}' in {path}` | ⚠️ Leakea path interno, prefijo "Unexpected:" sugiere bug |

## show con IDs raros

| Input | Comportamiento | Severidad |
|---|---|---|
| `""` (vacio) | Muestra `atom-001` (el primero) | 🔴 Bug — string vacío tratado como "sin argumento" |
| `" "` (espacio) | Llega al filesystem sin trim | ❗ Debería validar |
| `"."` | Llega al filesystem | ❗ Debería validar formato |
| `"  with spaces  "` | Llega al filesystem sin trim | ❗ No hay sanitización |

## add sin flags — inconsistencia

| Comando | Resultado | Severidad |
|---|---|---|
| `add task` (sin flags) | Error de validación (Pydantic traceback) | ✅ Catchado (pero feo) |
| `add ritual` (sin flags) | Crea `ritual-none` | 🔴 Bug — artifact basura |
| `add board` (sin flags) | Crea `board-none` | 🔴 Bug |
| `add step` (sin flags) | Crea `step-none` | 🔴 Bug |
| `add pill --title ""` | Crea `pill-none` | 🔴 Bug — título vacío aceptado |

Algunos tipos validan campos requeridos, otros crean silenciosamente basura.

## show con partial match

Ningún comando soporta fuzzy/partial match:
- `show pill self-reflection` → not found
- `show step document` → not found
- `show pill ".*"` → not found (regex no soportado)

## --root edge cases

| `--root` | Comportamiento | Severidad |
|---|---|---|
| `./nonexistent` | Exit 0, sin output | 🔴 Bug — error silencioso |
| `setup.py` (file) | Exit 0 inconsistente | 🔴 Bug — exit code incorrecto |
| Antes del positional | `invalid choice: '/tmp'` | 🔴 Bug — flag no reconocido antes del subject |

## Pydantic tracebacks al usuario

`add task` sin args muestra:
```
Unexpected: 2 validation errors for TaskDoc
id
  Field required [type=missing, input_value={'title': '...'}, input_type=dict]
```

Esto es un traceback interno de Python/Pydantic. Debería atraparse y mostrar "Missing required field: id".

## show ritual usa ID: field no filename

`show ritual` busca el `ID:` dentro del archivo, no el filename. `show ritual ritual-closeout` falla pero `show ritual closeout` funciona. Esto es **inconsistente** con `show pill` que usa filename.
