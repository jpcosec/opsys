# Round 05 — OS/IO edge cases, special inputs, error resilience

**Source:** round-05-subagent-05

## Muy large title → OSError

`--title "$(python3 -c 'print("A" * 10000)')"` → `[Errno 36] File name too long`. Sin graceful truncation, crash.

## Empty string payload → artifact con título "None"

`deskops add task ''` → exit 0, crea `task-none.md`.

## Error messages a stdout

`deskops show task nonexistent 2>/dev/null` → el mensaje aparece (debería ir a stderr).

## Algunos flags inconsistentes

`inbox` usa `--desk-root`, `add task` usa `--root`. Distinto nombre para el mismo concepto.

## add task sin args → Pydantic traceback

`deskops add task` → `Unexpected: 2 validation errors for TaskDoc`. No muestra usage.

## Whitespace-only inputs

`--title "  "` → titulo literal de 3 espacios. Sin validación. Slug genérico `-item`.

## HTML/special chars sin sanitizar

`--title "Title with <html> & special chars"` → preservado verbatim en el archivo.

## Path traversal no validado

`--root /tmp/../../etc` → resuelve a `/etc`, error de permiso del OS. No hay path validation propia.

## Múltiples --root

`--root . --root /tmp` → último gana. Sin warning.

## --dry-run no existe en ningún comando

## HOME, TMPDIR no son necesarios

Corre limpio sin `$HOME`.

## List con --root no valido

`deskops list tasks --root /tmp/nonexistent` → exit 0, sin output. Sin error.
