## REFORMULACION
Encargo ejecutable de código en el repo **deskops**: cerrar el resto de CC35d migrando `domain_tree`, `atom_tags` y los chequeos de namespaces/padres de dominio a la API de tags de sldb (declaración, reglas, `tag_tree`, `tag_folder`). Resultado: `domain_tree.py` solo crea crossroads/protoatoms; se borran `require_domain_parents`, `_domain_errors` y `validate_atom_tag_namespaces`; `ATOM_TAG_PATTERN` prohíbe segmentos vacíos; los consumidores usan sldb con el mismo texto/exit; la declaración de tags se escribe vía `desk update --apply`; goldens, tests, `CHANGELOG` y `docs` actualizados. Límites: no escribir en sldb, no tocar `desk replace` ni vistas, nada manual en `desk/` o `.sldb/`, sin Python supliendo reglas, y validar en worktree con los 4 pasos en clon limpio.

## AMBIGUEDADES
1. “cuántos átomos de los 6 desks tienen ese patrón (copias en /dev/shm)”: no se indican rutas exactas de esas copias; obligaría a inventar ubicación y criterio de búsqueda.
2. “tag_models = [AtomDoc] y sus descendientes que deskops usa, más CrossroadDoc y ProtoAtomDoc si llevan tags del namespace”: “si llevan” exige inspección no especificada; obligaría a inventar la lista final de modelos.
3. “el informe cuenta…”: no se define qué informe, dónde se escribe ni su formato; obligaría a inventar el artefacto y su ubicación.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, `alcance.md`, `desk_declaration.yaml`, `tag-namespaces.yaml`, código y tests de las superficies listadas, goldens, informe de CC35d y copias de los 6 desks en `/dev/shm`. Cambios previstos: declarar tags con API sldb y `desk update --apply`; reducir `domain_tree.py`; borrar validadores; endurecer `ATOM_TAG_PATTERN`; sustituir llamadas en `doc_access`, `services/atoms`, CLI y doctor; actualizar tests, docs y changelog. Dependencias: GD27 ya en sldb main, worktree fijado por el coordinador, goldens/copias disponibles. Validaciones futuras: grep vacío, tests por archivo, goldens idénticos, `domain:a.b` sin crossroad con mismo fallo, `desk update --apply` idempotente, `doctor` sin hallazgos nuevos en 6 desks y 4 pasos en clon limpio. Sin ejecutar nada.

## FUTURO
El coordinador fija worktree, corre suite integrada y los 4 pasos; el supervisor decide revisiones en frío; el operador del desk dispone hallazgos; si falta capacidad en sldb, el coordinador abre nota y el equipo de sldb la resuelve.
