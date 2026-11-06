REFORMULACION

Encargo ejecutable (task.code) en el repo deskops: actualizar deliberadamente el snapshot de contratos de modelo para registrar el nuevo contrato de `RelationDoc` introducido por GO09 de sldb. Resultado: `tests/fixtures/model_contract_hashes.json` con el valor de `RelationDoc` = `a71cc045...`, sin tocar otras claves, y una línea en `CHANGELOG.md` (Unreleased/Changed) que cita GO09 y la migración `09b5075c`; `test_model_contract_snapshot.py` debe pasar (2 passed). Límites: solo esos dos archivos; fuera `.sldb/`, `desk/`, `scripts/migrate_desk_stores.py` y cualquier otro hash; los demás desks los repara el coordinador de proyecto.

AMBIGUEDADES

1. Recuento contradictorio de desks. Cita: «los otros 5 desks quedan para la tarea del coordinador de proyecto», frente a Scope, donde sldb «ya lo migró el coordinador de proyecto (96bcc5dd...)» y solo spec2viz, scion, pron y graph_ui siguen pendientes. Obligaría a inventar si son 4 o 5 y si sldb cuenta como pendiente.
2. Conflicto mismo-modelo/hash distinto. Cita: «Se toma de la salida "New hashes" del test y se comprueba que coincide con el contract_hash de .sldb/core/models/RelationDoc.yaml». Solo se ordena parar si falla «por un modelo distinto de RelationDoc»; no se define qué hacer si RelationDoc difiere de `a71cc045...`.
3. Rama y estado de origin. Cita: «la migración del store de deskops ya está hecha en main (09b5075c...)». No se indica que el ejecutor deba estar en main ni hacer fetch; obligaría a decidir si verificar la rama o el contenido de `origin/main`.
4. Estructura del CHANGELOG. Cita: «CHANGELOG, en Unreleased / Changed, una línea». Si faltan esas secciones, obligaría a inventar dónde insertarla.

DRY-RUN

Lecturas: TaskDoc; `tests/fixtures/model_contract_hashes.json`; `CHANGELOG.md`; `tests/test_model_contract_snapshot.py`; `.sldb/core/models/RelationDoc.yaml`; `git status` y `git merge-base HEAD origin/main`. Cambios previstos: sustituir solo el valor de `RelationDoc` por `a71cc045...`, preservando orden y claves; añadir una línea en Unreleased/Changed con el texto indicado. Dependencias: que `09b5075c` esté presente y el `contract_hash` del store coincida; que el test solo falle por RelationDoc. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_model_contract_snapshot.py` (2 passed); grep de RelationDoc igual a `a71cc045...` y al YAML; `git diff --stat` contra merge-base limitado a los dos archivos, una línea en el fixture. Sin ejecutar nada.

FUTURO

El coordinador de proyecto repara los otros desks (`desk update --apply` / `stores update`). Si el test falla por otro modelo, el ejecutor para y avisa al coordinador. La revisión, el merge y el cierre del nodo quedan a decisión humana; el closeout puede citar GO09.
