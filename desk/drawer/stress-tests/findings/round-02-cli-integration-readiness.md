# Round 02 — CLI integration readiness

**Source:** ST-15

## Exit codes

| Escenario | Exit | Veredicto |
|---|---|---|
| `deskops about` | 0 | ✅ |
| `deskops nonexistent` | 2 | ✅ |
| `deskops show` (missing subcommand) | 2 | ✅ |
| `deskops` (sin args) | 2 | ✅ |
| `list atoms --root /nonexistent` | 0 | ⚠️ **root sin validación** |

El CLI es disciplinado con exit codes. Usa `argparse` consistentemente. **Pero** `--root` acepta cualquier path sin validar — esto es una trampa en CI.

## Output formats

- Solo `inbox --list` soporta `--format {text,json,yaml}`
- Ningún otro comando tiene `--format` o `--json`
- No hay `--ci` flag en ningún comando
- No hay `--version` flag
- No hay `--verbose` flag

## ANSI / colores

No hay códigos ANSI en ningún output. Texto plano. **Excelente para CI logs**, pero la experiencia en terminal es plana.

## Pipeline safety

- stderr/stdout están limpios y separados
- Piping funciona sin artefactos
- Redirección a archivo es limpia

## --root sin validación

`deskops list atoms --root /tmp` → exit 0, sin output, sin error. El usuario cree que funcionó pero no encontró nada. En CI esto es una falla silenciosa.

## Resumen

El CLI es **CI-safe** (texto plano, exit codes correctos, stderr/stdout separados) pero **no CI-friendly** (solo un comando soporta JSON, no hay `--version`, no hay `--ci`, `--root` no se valida).
