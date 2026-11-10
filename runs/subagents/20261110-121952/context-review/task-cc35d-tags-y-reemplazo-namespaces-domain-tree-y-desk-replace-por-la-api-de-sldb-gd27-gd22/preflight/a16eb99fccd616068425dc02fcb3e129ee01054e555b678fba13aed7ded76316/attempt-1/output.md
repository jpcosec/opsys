## REFORMULACION
Nodo ejecutable de código en el repo **deskops**: migrar las superficies de tags y reemplazo a la API de sldb según GD27/GD22. Propósito: que `tag-namespaces.yaml` se sincronice al store, que la validación de dominio use `tag_tree` de GD27, que `axis_folder_relpath` pase a `tag_folder` y que `services/replace.py` use `sldb replace_text`, borrando el código viejo. Resultado: `require_domain_parents` eliminado, sync idempotente de namespaces, reemplazo con la misma guarda de conteo, goldens de ayuda/salida idénticos, tests verdes, `CHANGELOG.md` y doctor sin hallazgos nuevos en 6 desks. Límites: no cambia el formato de `desk/` ni la gramática del CLI; fuera de alcance referencias entrantes (CC35c), closeout (CC33a/b) y grafo (CC33c); no se escribe a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.

## AMBIGUEDADES
1. «Parte de los chequeos que CC38 dejó inventariados para CC33… se anota cuáles»: no se listan los 9 chequeos ni el criterio de cobertura de GD27; obligaría a inventar el inventario y su correspondencia.
2. «Lo que queda de domain_tree.py es lo del caso (crear crossroads y protoátomos con sus plantillas)»: no enumera funciones retenidas; obligaría a inventar el límite exacto de borrado.
3. «si sldb.replace_text no lo cubre, el informe dice cómo»: no define informe, formato ni ubicación; obligaría a inventar un entregable.
4. «Toda capacidad entra con prueba, CHANGELOG.md y doc en docs/» frente a `OUTPUT_SCOPE` sin `docs/`: obligaría a decidir si se modifica documentación.
5. «desk update --apply lo sincroniza a tag_namespaces del store»: no define conflicto/merge si el store difiere; obligaría a inventar semántica salvo que GD27 la fije.

## DRY-RUN
Lecturas: `domain_tree.py`, `atom_tags.py`, `services/replace.py`, `cli/commands/desk.py`, `tag-namespaces.yaml`, tests y goldens citados, APIs de sldb y contrato GD27. Cambios previstos: sustituir validación/árbol de dominio, `axis_folder_relpath`→`tag_folder`, `replace_text`→API sldb conservando guarda, sync de namespaces, tests y CHANGELOG. Dependencias: CC35b cerrado y APIs de sldb main. Validaciones futuras: grep vacío, tests de a uno, idempotencia, goldens desde `/dev/shm`, doctor en 6 desks y workflow en clon limpio. Sin ejecutar.

## FUTURO
El coordinador corre workflow y doctor y fija worktree; el supervisor ejecuta la suite completa sobre lo integrado; CC33b recibe los chequeos no cubiertos y sldb recibe nota si `replace_text` no cubre documentos no modelados.
