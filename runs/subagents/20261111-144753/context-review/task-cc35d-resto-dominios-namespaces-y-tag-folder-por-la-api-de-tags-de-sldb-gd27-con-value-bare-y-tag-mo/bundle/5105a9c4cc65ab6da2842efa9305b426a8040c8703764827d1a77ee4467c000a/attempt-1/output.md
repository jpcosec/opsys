## REFORMULACION

**Propósito:** cerrar el resto de CC35d pasando `domain_tree.py`, `atom_tags.py` y los chequeos de namespaces y padres de dominio a la API de tags de sldb (GD27), borrando `require_domain_parents`, `_domain_errors` y `validate_atom_tag_namespaces`.

**Resultado:** declaración del store con `tag_models` y `domain` anclado por `CrossroadDoc.path` con `value: bare`; `ATOM_TAG_PATTERN` sin segmentos vacíos; `tag_folder` de sldb para el eje; goldens idénticos; grep vacío; `desk update --apply` idempotente; `doctor` sin hallazgos nuevos en los 6 desks.

**Repo:** deskops, worktree en robocop2.

**Límites:** fuera `desk replace` (ya entró) y vistas (CC34); no se escribe en sldb; lo que falte de sldb queda como hipótesis.

## AMBIGUEDADES

1. «el informe cuenta cuántos átomos de los 6 desks tienen ese patrón (copias en /dev/shm)»: no dice qué informe (¿el de CC35d en `wt/cc35d`?) ni las rutas de las copias; obligaría a inventar ubicación y formato.
2. «tag_models = [AtomDoc] y sus descendientes que deskops usa, más CrossroadDoc y ProtoAtomDoc si llevan tags del namespace»: «si llevan» exige decidir qué modelos llevan tags; obligaría a inventar la lista.
3. «si archivo y declaración difieren, gana el archivo» junto a «desk update --apply de forma idempotente»: no dice cómo se reconcilia sin romper idempotencia; obligaría a inventar la política.
4. «lo que falte se deja como hipótesis en el informe»: mismo informe indeterminado del punto 1.
5. «menos lo que ya entró (a4, desk replace por sldb.replace_text, 6d55bb40)»: el commit no se identifica por rama; obligaría a inventar su alcance.

## DRY-RUN

**Lecturas:** TaskDoc y drawer de origen; `runs/subagents/cc35d-worker-report.md`; los ocho archivos listados; `tests/`, `docs/`, `CHANGELOG.md`; declaración y API de tags de sldb (`load_declaration`/`save_declaration`, `tag_tree`, `tag_folder`, `rules check`).

**Cambios previstos:** declarar `tag_models` y `domain` con `value: bare` vía API; borrar las tres funciones y sus llamadas en `doc_access`, `services/atoms`, `cli/atoms`, `cli/doctor`; endurecer `ATOM_TAG_PATTERN`; sustituir el eje por `tag_folder`; tests, docs y CHANGELOG.

**Dependencias:** GD27 en sldb main; worktree fijado por el coordinador; antes de tocar el patrón, conteo de átomos con segmentos vacíos (parar si hay).

**Validaciones futuras:** grep vacío; `domain:a.b` sin crossroad con mismo exit y texto; goldens; `doctor` en 6 desks; idempotencia; 4 pasos en clon limpio.

Nodo ejecutable (no agregado).

## FUTURO

sldb entrega GD27; el coordinador abre la nota si falta API, fija worktree y corre los 4 pasos y la suite completa; el supervisor decide revisiones en frío; el worker para y avisa si hay átomos con segmentos vacíos.
