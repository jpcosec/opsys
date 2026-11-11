## REFORMULACION

**Propósito:** permitir que `deskops closeout resolved-by` cierre una `task.code` cuyo código vive en otro repo, aceptando referencias calificadas `<repo>:<sha>` y `<repo>:<ruta de test>` verificadas contra un repo del registro del ecosistema.

**Resultado:** `--ref <repo>:<sha>` acredita el commit si es ancestro del HEAD de ese repo; `--test <repo>:<ruta>` acredita el test si existe allí bajo reglas de tests; los trailers guardan la referencia calificada tal cual y `Closeout-Mode` sigue siendo `resolved-by`.

**Repo:** deskops (SLDB_1), con cambios en `deskops/services/closeout_gates.py`, `deskops/services/closure.py`, `deskops/identity.py`, `deskops/cli/commands/closeout.py`, `tests/`, `docs/operator-manual.md` y `CHANGELOG.md`.

**Límites:** solo `resolved-by`; quedan fuera `closeout verify`, `closeout commit`, la sugerencia de `task.external` y `supersede`.

## AMBIGUEDADES

1. “con el mismo commit de cierre y los mismos trailers”: no define “mismo” respecto de qué; obligaría a inventar si se reutiliza un commit previo o se compara con el repo local.
2. “registrados en el registro del ecosistema” (c5): no indica API ni formato para registrar dos repos en tests; obligaría a inventar el mecanismo de alta.
3. “Una referencia sin prefijo, o con un prefijo que no es un repo registrado, se trata como hoy”: no aclara colisiones con `:` en rutas o ids; obligaría a inventar la regla de parseo.
4. “Los files de la tarea no amplían los tests de otro repo”: no define si la ruta calificada puede apuntar al repo local; obligaría a inventar esa restricción.
5. “la suite completa de a un archivo desde /dev/shm”: no especifica comando ni orden; obligaría a inventar la invocación.

## DRY-RUN

Nodo ejecutable `task.code`, no agregado. Lecturas: los cinco archivos de código, tests existentes de resolved-by/closeout, manual y CHANGELOG. Cambios previstos: parseo de referencias calificadas en compuertas, resolución por registro, ayuda CLI, tests con dos repos git en `tmp_path` y documentación. Dependencias: API del registro, git disponible, `tmp_path`. Validaciones futuras: tests nuevos y existentes, suite completa archivo por archivo desde `/dev/shm`, y los 4 pasos de CI en clon limpio.

## FUTURO

El worker ejecutará tests focalizados y la suite; el coordinador correrá los 4 pasos del CI. Un humano decidirá el cierre y mantendrá la opción a en el drawer. `closeout verify` y `closeout commit` seguirán exigiendo evidencia local.
