REFORMULACION
Propósito: cerrar la parte (3) del agregado CC35 en el repo deskops (worktree en robocop2). Resultado: atoms delete/split/merge, retire, drawer remove y closeout usan `referrers` y `rewrite_references` de sldb dentro de la misma `desk_transaction`; las menciones en prosa quedan cubiertas por los `MentionPattern` de `deskops/graph/desk_graph.py`; se borran `_find_inbound_atom_references`, `_rewrite_inbound_atom_references` y `_inbound_references`, con tests, `docs/operator-manual.md` y CHANGELOG. Límites: fuera la API de tags (CC35d/DO7) y las vistas (CC34); no cambia formato del desk ni gramática del CLI; nada se ejecuta aquí.

AMBIGUEDADES
1. "Si una no la ve referrers, se suma el patrón que falte en desk_graph.py" (b1) frente a "si con el MentionPattern declarado ... no devuelve la mención ... es caso de sldb: hipótesis" (b2). Obliga a inventar cuándo se corrige en deskops y cuándo es nota a sldb.
2. "los bullets del drawer se declaran como MentionPattern" (Goal) frente a "Drawer tasks keep the extraction they had ... their lines are not scanned" (LINE_MENTIONS). Obliga a inventar qué bullets del drawer entran.
3. "deja un solo commit o una sola escritura atómica" (a5) frente a "El commit no es parte de retire" (b4). Obliga a elegir el criterio del test de retire.
4. "deskops doctor sin hallazgos nuevos en los 6 desks" frente a "en un worktree de deskops por nodo" (regla común 2). Obliga a inventar cómo se validan los otros cinco desks.
5. "líneas antes y después" (aceptación; b5 pide tabla, no umbral). Obliga a inventar si hay límite de líneas.

DRY-RUN
Lecturas: TaskDoc, dag.yaml CC35c, alcance.md, `desk_graph.py`, `atom_references.py`, `services/atoms.py`, `retire.py`, `drawer.py`, `closure.py`, tests y fixtures golden. Cambios previstos: sustituir los tres helpers por `referrers`/`rewrite_references` dentro de `desk_transaction`; comprobar/añadir MentionPattern para `atom:<id>` y `atom-<slug>`; tests (retire de pill con fallo forzado, merge con ambas formas, drawer remove reportando colgantes sin reescribir); docs/operator-manual.md; CHANGELOG; tabla `wc -l`. Dependencias: CC35a (transacción), CC33c (grafo), sldb GD22, store `.sldb`. Validaciones futuras: grep vacío, goldens idénticos, 4 pasos (`stores build`, pytest por archivo, `--check`, `ci-knowledge-check.sh`), doctor en 6 desks. Sin ejecutar.

FUTURO
Coordinador: fija worktree, corre 4 pasos y suite completa, dispone hallazgos de preflight/bundle y abre la nota a sldb si aplica b2. Humano: aprueba excepciones y la promoción del nodo.
