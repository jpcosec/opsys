# CC35d worker report: entrega parcial (a4, desk replace por sldb)

Worker `cc35d-worker`, rama `wt/cc35d`, base `91cb77db`. Sin push.

**Decisión del coordinador (coord2, revisable):** CC35d se parte y ahora se entrega solo a4:
`desk replace` pasa por `sldb.replace_text`, con sus tests, goldens idénticos y CHANGELOG.
No se adopta `tag_folder` y no se escribe el test de b6, porque H3 lo decide sldb. B1, B2 y B3
quedan fuera: `domain_tree`, `require_domain_parents` y `tag_namespaces` no se tocan. El
coordinador abre H1, H2 y H3 en el drawer de sldb y registra el corte.

## Qué se entrega

Commits: `568d2140` (primer informe, de bloqueo), `3f28135b` (a4), `aa24986c` (arreglo de un
test nuevo) y el de este informe.

- `deskops/services/replace.py`: la escritura es `sldb.api.replace_text(store, <ruta relativa>,
  old, new, count=..., transaction=<tx del desk>, pythonpath=package_pythonpath())`, dentro de
  `doc_access.desk_transaction`.
  - **Se borra el camino viejo:** escribir los bytes, `transaction.record` y el
    untrack/track a mano a partir de `index_entry`.
  - **Queda en deskops lo suyo:** qué archivos alcanza el verbo (las rutas bajo `desk/`, los
    sujetos modelados que se derivan a `deskops edit` y el TaskDoc del drawer) y la guarda de
    conteo con su mensaje exacto, comprobada antes de llamar a sldb.
  - **Errores de sldb:** un `SLDBError` (un documento trackeado que deja de validar, o una regla
    `on_write`) pasa a `DomainError("Refusing to replace in <path>: <error de sldb> The file is
    unchanged.")`, con exit 1. La transacción se revierte.
  - **Desk sin store:** sldb no tiene store que abrir, así que se escribe el archivo directo,
    igual que hacía `desk_transaction` con `None`.
- `tests/test_desk_replace.py`: los 7 tests existentes quedan intactos y se agregan 3:
  - `test_replace_writes_through_sldb_replace_text`: un espía sobre `sldb.api.replace_text`
    confirma que la llamada pasa por sldb, con la transacción abierta;
  - `test_replace_refuses_a_tracked_document_the_new_text_breaks`: un RoleDoc trackeado cuyo
    reemplazo rompe el frontmatter se rechaza, el archivo queda byte a byte igual y
    `check_store` queda ok;
  - `test_replace_in_a_desk_without_a_store_writes_the_file`.
- `docs/operator-manual.md` (sección «Replace text in an unmodeled desk file»): la escritura es
  `replace_text` de sldb, y un archivo trackeado tiene que seguir validando.
- `CHANGELOG.md`: una entrada en «Changed».

### a4: el documento no modelado (`_modeled_subject`)

Una nota del drawer, el cuerpo de una issue o `tag-namespaces.yaml` siguen siendo reemplazables
como hoy. sldb los trata como «plain file under the project root» (`tx.write_file`). Lo cubren
los tests que ya existían: nota del drawer, issue y tarea legacy del drawer.

El cambio de comportamiento: un archivo trackeado, como un RoleDoc, ahora se valida bajo su
modelo y bajo las reglas `on_write`. Si el texto nuevo no hace round-trip, se rechaza. Antes se
escribía igual y se volvía a trackear.

## Aceptación (la de a4)

| Línea | Evidencia |
|---|---|
| desk replace por sldb.replace_text | `services/replace.py` llama a `sldb.api.replace_text`; lo prueba el test del espía |
| misma guarda de conteo | `test_replace_refuses_when_the_old_text_is_missing` y `test_replace_requires_an_exact_count` («found N occurrence(s)»), sin cambios y verdes |
| tests de los archivos tocados verdes | ver la tabla de tests |
| goldens de ayuda y salida idénticos | `test_output_goldens` desde `/dev/shm`, sin `--update-golden` (ver tabla) |
| doctor sin hallazgos nuevos | no se tocó doctor ni ningún documento del desk. Los 4 pasos y doctor en los 6 desks los corre el coordinador (a6) |
| CHANGELOG | entrada en «Changed» |

### Tests (de a uno, con guarda pgrep; logs en `~/proyectos/SLDB_1/coord2-ccconfig/cc35d/`)

| Archivo | Resultado |
|---|---|
| tests/test_desk_replace.py | 10 passed (110 s) |
| tests/test_command_registry.py | 3 passed |
| tests/test_operator_manual.py | 1 passed (148 s) |
| tests/test_output_goldens.py (/dev/shm) | 7 passed (320 s), sin --update-golden, sin diff en tests/fixtures |
| tests/test_cli.py (/dev/shm) | 101 passed (154 s) |

`test_domain_tree`, `test_atom_tags`, `test_atom_folder_axis` y `test_desk_sync` no se
corrieron: sus superficies no cambian en esta entrega. La primera corrida de
`test_operator_manual` dejó el log vacío con el timeout de 900 s; se repitió con 2400 s y pasó en 148 s, así que el log vacío de la primera corrida no se explica por un timeout; no se reprodujo.

## wc -l antes y después

| Archivo | Antes | Después |
|---|---|---|
| deskops/services/replace.py | 120 | 139 |
| deskops/domain_tree.py | 331 | 331 (sin tocar) |
| deskops/atom_tags.py | 150 | 150 (sin tocar) |
| deskops/cli/commands/desk.py | 441 | 441 (sin tocar) |
| tests/test_desk_replace.py | 175 | 238 |

`replace.py` crece 19 líneas porque se borran las 10 del camino viejo y entra
`_sldb_replace`, que importa y traduce el error, más el docstring. La guarda de deskops se queda
porque el golden del mensaje es de deskops.

## Qué queda y por qué

Todo esto va a un nodo hijo pendiente de sldb:

- **B1, el ancla de `domain`.** El `anchored_by` de GD27 solo cuenta un ancla si el campo vale
  `domain:a.b`, pero `CrossroadDoc.path` vale `a.b`. En la sonda, con
  `crossroad-knowledge-management` presente igual salieron 5 hallazgos, y `tag_tree` dio
  `roots: []`. Se resuelve con **H1**: aceptar el valor sin namespace en el campo ancla.
- **B2, la sincronización de `tag-namespaces.yaml`.** Declarar los 5 namespaces del registro de
  átomos genera 115 errores nuevos en namespaces de otros modelos (`workspace` 78, `pill-type`
  29, `artifact` 4, `runtime` 2, `source-atom` 1 y `type` 1), y `on_write` rechazaría tareas y
  pills. Se resuelve con **H2**: acotar la familia por modelo, o dejar sin error un namespace no
  declarado.
- **B3, el contrato.** `require_domain_parents` y `DomainTree.check/tree` se usan en
  `deskops/doc_access.py`, `deskops/services/atoms.py` y `deskops/cli/commands/atoms.py`. El
  nodo hijo tiene que tenerlos en `files`.
- **b6, `tag_folder`.** No se adoptó. Difiere de `axis_folder_relpath` en `a..b` y en `a.`: hoy
  dan `a/b` y `a`, y sldb da `ValueError`. `ATOM_TAG_PATTERN` admite esos valores. Ningún desk
  configura `atom_folder_axis`. Lo decide **H3** en sldb.
- **a5 / b1, los chequeos de CC38 para CC33.** #3 (namespace declarado) y #5 (padres de domain)
  **no quedan cubiertos** por GD27 hoy (B2 y B1). Siguen en deskops. #13, #14, #15, #18, #24 y
  #25 siguen para CC33b.

Evidencia de la sonda: `~/proyectos/SLDB_1/coord2-ccconfig/cc35d/cc35d-probe.py` y
`probe-gd27.log`.

## Hipótesis para sldb (las abre el coordinador; no se escribió en sldb)

- **H1:** `anchored_by` acepta un campo cuyo valor es el valor del tag sin namespace, por ejemplo
  `anchored_by: {model, field, value: bare}`.
- **H2:** `tag_namespaces` acotado por modelo (`models: [...]`), o `undeclared: ignore | error`.
- **H3:** `tag_folder` ignora los segmentos vacíos, o los modelos los prohíben.

## Desvíos

- El TaskDoc lista en `files` `deskops/domain_tree.py`, `deskops/atom_tags.py` y
  `deskops/cli/commands/desk.py`, y esta entrega no los toca. Según la regla «files = entrega»,
  el coordinador debería podarlos del TaskDoc con `deskops edit task` antes del cierre. El worker
  no escribe en `desk/`.
- Atajo relativo a `desk/` en `replace_text`, que viene de antes: la ruta ya se resolvió a
  absoluta antes del `if not path.is_absolute()`, así que `drawer/x.md` nunca se resuelve como
  `desk/drawer/x.md`. Se conserva igual, porque cambiarlo cambiaría la gramática. Un test nuevo
  lo había asumido y se corrigió en `aa24986c`.
- Sonda en una copia desechable de `/dev/shm` (`sldb edges rebuild` y `save_declaration`), ya
  borrada.
