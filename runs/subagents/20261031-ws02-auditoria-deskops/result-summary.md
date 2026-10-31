# Resultado — WS02 auditoria Deskops (Executor)

## Que se hizo
- Entregable: `desk/drawer/plans/workspace-documental/auditoria/deskops.md` (secciones A1, A2, B, C con C2-C4, D, resumen).
- Anexos: `file-inventory.tsv` (192 filas), `runs-inventory.tsv` (169 filas), `commands.log` (62 lineas).
- Los inventarios y las filas de A1/A2 se generaron con scripts de solo lectura en /tmp (no en el proyecto): `inv.py` (os.walk + hashlib + `.sldb/store.yaml` + `git status --short -uall`), `runs.py`, `gen.py` (itera `command_registry()` y `dir(DeskopsOperations)`; aborta si falta una fila). Ningun hash se escribio a mano.
- No se ejecuto ningun comando mutador, ni commit, ni `git add`, ni closeout. Solo `sldb models list --store .sldb`, `sldb ... --help`, `deskops --help` y lecturas.

## Conteos reales vs cubiertos
| seccion | real | filas |
|---|---|---|
| A1 comandos `command_registry()` | 113 | 113 |
| A2 metodos publicos `DeskopsOperations` (sin 6 `@property`) | 24 | 24 |
| B modelos de `sldb models list` | 17 | 17 |
| C archivos del universo (anexo) | 192 | 192 |
| C2 existencia (issues, faq, crossroads, fases) | 4 | 4 |
| C3 runs/subagents (carpetas, sin la de este run) | 169 | 169 en anexo, 1 fila resumen |
| C4 store .sldb | 3 subarboles | 3 |
| D cierre | 2 (verify, commit) | 2 |

SHA-256 de `file-inventory.tsv`: `fa0dffc8162e5315ad8571c7f5bf33696a317f710494e3a2d5d681408686fa46`; de `runs-inventory.tsv`: `dfe72fdd1d175dc1370b72966e249efc0d0fa85fd47ec3ef3f344ad0c4478b40`.

## Decisiones de formato (por mi cuenta)
- El anexo de archivos tiene 2 columnas extra (`git`, `texto`) ademas de `path, sha256, modelo`.
- Se excluyen del inventario `desk/drawer/plans/workspace-documental/auditoria/` (entregable y auditorias hermanas en escritura paralela) y el run actual.
- Los 3 `.pyc` del drawer se listan como «no comprobado (no UTF-8)» siguiendo la disposicion previa (contradice en parte «binario ajeno se excluye»; se prefirio listarlos).
- `.sldb/runtime` (3560 archivos, derivado, ignorado, mutable) solo se cuenta; `.sldb/core` (257) y `.sldb/store.yaml` se resumen en C4, no fila a fila.
- Los comandos agrupadores tienen fila propia (estan en el registro).
- `commands.log` esta reconstruido a mano: agrupa varios greps/sed en una linea y no es una captura automatica.

## Huecos (no comprobado)
- `sldb stores check` (lo usan `doctor` y `desk update`): no se leyo ni ejecuto; se ignora si escribe cache.
- Repos hermanos (`../sldb`, `../spec2viz`, ...) no leidos.
- Efectos de comandos mutadores: leidos en codigo, no probados en vivo (por regla).

## Que revisar
- Sorpresas listadas al final del entregable: `.deskops.log` escrito por el constructor; `validate_atoms` llama `ensure_workspace`; `retire` no hace commit; 2 de 8 materializaciones declaradas no estan en el indice local; `closeout commit` borra el archivo de la tarea (tambien de este WS02 cuando se cierre).
- Muestrear citas archivo:linea de A1 (en especial closure.py y desk.py).
- `git status --short` varia mientras otras sesiones escriben; el encabezado fija 11 lineas al generar, 12 al terminar.
