REFORMULACION
Propósito: ejecutar la parte (4) del agregado CC35 del plan deskops-como-config (dag rev 4), gate G_GD27 satisfied y CC35b cerrado; nodo ejecutable (`task.code`), no agregado. Resultado: pasar cuatro superficies a la API de sldb (GD27/GD22): sincronizar `tag-namespaces.yaml` al store desde `desk update --apply`; sustituir `require_domain_parents` y `DomainTree.check/tree` por la validación y `tag_tree`; `axis_folder_relpath` por `tag_folder`; `services/replace.py` por `sldb replace_text` con la misma guarda de conteo. Repo: deskops, worktree en robocop2. Límites: solo los archivos listados; fuera CC35c, CC33a/b y CC33c; sin cambiar formato del desk ni gramática/goldens; borrar el código viejo en el mismo paso.

AMBIGUEDADES
1. «Lo que queda de domain_tree.py es lo del caso (crear crossroads y protoátomos con sus plantillas)»: no delimita funciones; obligaría a inventar el corte.
2. «cuáles de los 9 chequeos» / «si GD27 los cubre»: el inventario no está en el input; obligaría a inventarlo.
3. «la sincroniza a tag_namespaces del store por la API de sldb»: a2 solo da `tag_namespaces(store)` de lectura; obligaría a inventar la escritura y el modelo.
4. «el informe dice cómo»: no define informe ni artefacto; obligaría a inventar un entregable.
5. «axis_folder_relpath pasa a tag_folder»: no fija equivalencia semántica; obligaría a inventar la conversión.
6. «falla como antes»: no fija mensaje ni exit; obligaría a decidir si el error se conserva.

DRY-RUN
Lecturas: TaskDoc, Board, rituales, pills, átomos, los cuatro archivos y CHANGELOG; tests y goldens. Cambios: `require_domain_parents`→validación/`tag_tree`; `tag_folder`; `sldb replace_text` en replace.py y desk.py; sincronización idempotente en `desk update`; tests y CHANGELOG; líneas antes/después. Dependencias: sldb GD27/GD22, CC35b cerrado, store y seis desks. Validaciones futuras: grep vacío; pytest de a uno (domain_tree, atom_tags, atom_folder_axis, desk_replace, desk_sync, cli, output_goldens desde /dev/shm sin `--update-golden`); goldens idénticos; doctor en seis desks; cuatro pasos en clon limpio; segunda corrida idempotente.

FUTURO
CC35c resuelve referencias entrantes; CC33b decide chequeos no cubiertos; el coordinador corre el workflow en clon limpio y fija worktree; el supervisor corre la suite completa; sldb integra rule_graph; CC33c migra graph.
