## REFORMULACION

**Propósito:** que `deskops closeout verify` emita, por cada kind de evidencia verificado, un ReviewDoc `evidence` y quede como orquestador, sin cambiar aún el gate de cierre.

**Resultado:** ReviewDoc con `fact`, `value`, `verdict` accepted/rejected, `reason` y `subject` pinneado al contrato; deduplicación por `input_sha256` + `anchor_state`; envelope idéntico a hoy.

**Repo:** deskops.

**Límites:** solo productores en `closeout_gates.py`, `verify_task_closeout` y sus productores en `closure.py`, `models/review.py`, `cli/commands/closeout.py`, tests y CHANGELOG. Fuera: RuleDocs de cierre, borrado de `_add_closeout_facts`/`__closeout_evidence__` (CC33b), grafo (CC33c) y `close_*`. No se commitea `desk/` ni `.sldb/`.

## AMBIGUEDADES

1. «los kinds que exige el tipo de la tarea más su closeout_evidence»: no se define dónde ni cómo se declara `closeout_evidence`; obliga a inventar campo y lectura.
2. «value es lo que pasó, ordenado»: no fija criterio de orden; obliga a inventar (p. ej. lexicográfico).
3. «sha256 de «fact\nvalue\n» seguido, por cada ruta de archivo de value, del sha256 de sus bytes»: no fija codificación, separadores ni formato hex; obliga a inventar el byte-string exacto.
4. «para atom/materialization, los ids o rutas enlazados»: la disyuntiva «o» no decide cuál; obliga a inventar.
5. «anchor_state intact»: `anchor_state` «no es un campo del modelo» y no se nombra API de consulta; obliga a inventar cómo lo lee el escritor.
6. «subject doc:<Modelo>:<task>»: no aclara qué es `<Modelo>` ni el formato exacto del pin `@sha256`; obliga a inventar.
7. «reason es el texto que hoy da el gate cuando falta ese kind»: no cita los textos; si no existen literales, obliga a inventarlos.
8. «productores de hechos de git y archivos» frente a «external: reference_points_to_url»: una URL no es git ni archivo; tensión de alcance.

## DRY-RUN

**Lecturas:** `closure.py:578,773,880,925`; `closeout_gates.py` (293 líneas); `models/review.py:33`; `services/review.py` (`_write_review`); `services/atoms.py:71`; tests `test_closeout*.py`, `test_review_doc.py`; goldens.

**Cambios previstos:** añadir `evidence` a `ReviewKind` y `fact`/`value` opcionales con validador; separar productores de hechos; escribir recibos vía `doc_access` pinneados con dedupe; tests nuevos y CHANGELOG.

**Dependencias:** CC32, CC38 y CC35a ya en main; `depends_on` vacío.

**Validaciones futuras:** `pytest -q` de a un archivo con `TMPDIR=/dev/shm`; goldens de ayuda/salida sin `--update-golden`; `wc -l` antes/después; `deskops doctor` y `view board`.

## FUTURO

CC33b aplicará las reglas de activación y borrará `_add_closeout_facts`/`__closeout_evidence__`; CC33c abordará el grafo; CC35b cambiará la resolución de documentos; el supervisor correrá la suite completa y decidirá sobre goldens; el overlord habilitará la cuota; el coordinador fijará el worktree.
