# Round 04 — --from-yaml y side effects

**Source:** ST-from-yaml

## --from-yaml existe en todos los tipos

Los 13 tipos de artifact soportan `--from-yaml`. Cada uno acepta un path a un archivo YAML.

## CRITICAL: Side effects en failure

`deskops add task --from-yaml` con YAML parcial (solo `title` + `goal`) **crea todos los archivos en disco** a pesar de devolver exit code 1:

- `desk/tasks/task-yaml-test-task.md`
- `desk/routines/routine-task-yaml-test-task.md`
- 3 checklists, 3 conditions, 6 edges, 3 operators

La validación falla después de escribir. No hay rollback. Esto es un hazard de integridad de datos.

## No hay bulk operations

`--from-yaml` es el único mecanismo batch, y opera un artifact por llamada. No hay `--batch`, `--bulk`, `--csv`, `--import`, multi-entity YAML array.

## Output format flags

Ningún `show` o `list` tiene `--format`, `--json`, `--yaml`, `--output`. Todo el output es markdown hardcodeado para humanos. No hay salida machine-parseable.
