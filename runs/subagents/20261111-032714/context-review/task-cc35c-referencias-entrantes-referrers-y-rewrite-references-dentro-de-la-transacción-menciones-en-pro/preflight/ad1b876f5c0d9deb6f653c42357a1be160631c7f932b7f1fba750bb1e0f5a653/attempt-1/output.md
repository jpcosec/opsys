REFORMULACION

Propósito: sustituir en deskops las búsquedas/reescrituras propias de referencias entrantes por `sldb.api.edges.referrers` y `rewrite_references` (GD22), dentro de la misma `desk_transaction`, para atoms delete/split/merge, retire, drawer remove y closeout; las menciones en prosa y bullets del drawer se resuelven con `MentionPattern` del grafo. Resultado: código viejo borrado, pruebas, docs y CHANGELOG, sin cambiar formato del desk ni gramática CLI. Repo: deskops (worktree robocop2; base origin/main b990c49e). Límites: `deskops/services/`, `deskops/atom_references.py`, `deskops/graph/desk_graph.py`, `tests/`, `docs/`, `CHANGELOG.md`; fuera tags (CC35d/DO7) y vistas (CC34). Ejecutable, no agregado.

AMBIGUEDADES

1. “drawer remove y closeout buscan y reescriben” vs “sigue sin tocarlas (no se suma comportamiento)” y “reporta... con un alert... sin reescribir”. ¿Reescribir o alertar? b3 aclara alertar, pero no fija formato/canal; inventaría mensaje, severidad y destino.
2. “Goldens de ayuda y salida idénticos” vs “Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`)”. ¿Aplica aquí? Inventaría aceptar diferencias o regenerar.
3. “el MentionPattern que falte se suma ahí” no da sintaxis ni ubicación; inventaría regex/orden si referrers no ve una forma.

DRY-RUN

Lecturas: TaskDoc; `atoms.py`, `retire.py`, `drawer.py`, `atom_references.py`, `desk_graph.py`; tests, `docs/operator-manual.md`, CHANGELOG; API sldb edges/transacción (CC35a), grafo (CC33c). Cambios: reemplazar `_find_inbound_atom_references`, `_rewrite_inbound_atom_references`, `_inbound_references` por `referrers`/`rewrite_references` en la misma transacción; verificar/añadir MentionPattern ATOM para `atom:atom-<slug>` y `atom-<slug>`; drawer/closeout reportan referrers colgando sin reescribir; borrar búsquedas propias; tests tmp_path de retire de pill (Board+2 tareas, fallo forzado), merge con ambas formas; docs/CHANGELOG; tabla `wc -l` antes/después. Dependencias: CC35a/CC33c en main; GD22; `ProjectGraph(root, desk_graph_config())` en proceso. Validaciones futuras: grep vacío; pytest por archivo; goldens idénticos; doctor 6 desks; `sldb stores build --check`; `ci-knowledge-check.sh`; suite completa por supervisor.

FUTURO

CC35a entrega transacción; CC33c grafo; CC35d/DO7 tags y CC34 vistas quedan fuera. El coordinador fija worktree, corre los 4 pasos en clon limpio, revisa preflight/cold-bundle y abre nota a sldb si b2 se cumple. El supervisor corre suite completa y decide cierre; el operador promueve con `deskops add task --from-drawer`.
