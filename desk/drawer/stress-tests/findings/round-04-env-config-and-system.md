# Round 04 — Env vars, config, system integration

**Source:** ST-env-vars

## Config files

No existen. `~/.config/deskops`, `~/.deskops`, `/etc/deskops` — todo vacío. Deskops es completamente stateless en disco fuera de `.sldb/`.

## Environment variables

No hay variables `DESKOPS_*` ni `SLDB_*` definidas ni honradas.

## Version info

- Package: `deskops` v0.1.0
- Entry point: `deskops.cli.main:main`
- SLDB: desarrollo install desde `tools/sldb` (sibling directory)

## System integration

- Corre desde cualquier directorio
- No requiere `$HOME`
- Piped input a `inbox` falla si no coincide el formato esperado
- SLDB no tiene `__version__`

## Observación

La dependencia de sldb es un editable install desde `../sldb`. Si ese path se mueve o no está presente, deskops no funciona. Esto no es un problema ahora pero es un coupling a considerar para distribución.
