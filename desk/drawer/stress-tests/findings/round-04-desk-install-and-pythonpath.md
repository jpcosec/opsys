# Round 04 — Desk install y pythonpath

**Source:** ST-desk-install

## desk install

- Funciona: scafollea 8 dirs + 6 files en el target
- Idempotente: segunda corrida no falla
- Path inexistente → exit 1, mensaje claro
- Sin path → exit 2, argparse standard

## --pythonpath flag

- **Solo existe en `inbox` y `repo register`**
- `list`, `show`, `add`, `graph` **no tienen** el flag — `_apply_default_pythonpath` en main.py es dead code para esos comandos
- `deskops list atoms --pythonpath /tmp` → `unrecognized arguments`

Esto es un bug de wiring: el flag debería ser global o sacarse el dead code.

## Entry points

- `deskops` y `python -m deskops` son consistentes (mismo output, mismos exit codes)
- `deskops about` funciona desde cualquier directorio
- No requiere `$HOME` — corre limpio con `env -i`
