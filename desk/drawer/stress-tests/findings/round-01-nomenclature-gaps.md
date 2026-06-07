# Round 01 — Nomenclature & command gaps

**Source:** ST-01, ST-02, ST-05, ST-07, ST-14

## Commands que no existen (pero las atoms los describen)

| Concepto en atoms | Realidad CLI | Brecha |
|---|---|---|
| drift check | no existe | No hay comando `drift` ni top-level ni subcommand |
| materialize | no existe | No hay comando |
| status / health | no existe | No hay comando |
| closeout | no existe | No hay comando |
| validate | no existe | No hay comando |
| graph reflect | no existe | `graph` solo tiene `build`, `neighbors`, `missing` |
| atoms list | no existe | `list atoms` sí, pero `atoms list` no |
| atoms show | no existe | `show atom` sí, pero `atoms show` no |
| atoms new / validate / split / merge / deprecate | no existen | `atoms` solo tiene `add-namespace` |
| repo list | no existe | `repo` solo tiene `register` |

## Inconsistencias plural/singular

- `list` usa plural: `list tasks`, `list atoms`, `list pills`
- `show` usa singular: `show task`, `show atom`, `show pill`
- `add` usa singular: `add task`, `add atom`
- `advance` usa singular: `advance task`

Esto es consistente internamente pero puede confundir: `list tasks` funciona, `tasks list` no.

## Comandos medio implementados

- `advance task <id>` no acepta `--to` — el flag no existe. No se puede especificar el estado destino.
- `repo register` falla con error de modelo no registrado en store — el setup tiene un paso manual no resuelto.

## Átomos no cubiertos

- `list atoms` solo muestra 4 átomos (raíz de `desk/atoms/`). Los 60 átomos en `knowledge-model/` y `workflow-model/` no aparecen.
- `show atom <id>` solo encuentra los 4 de raíz.
