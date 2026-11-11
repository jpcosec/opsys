## REFORMULACION
Propósito: sustituir las búsquedas propias de referencias entrantes por `referrers`/`rewrite_references` de sldb dentro de la misma transacción, en `atoms delete/split/merge`, `retire`, `drawer remove` y `closeout`, y declarar las menciones en prosa (y bullets del drawer) como `MentionPattern` en la configuración de grafo. Resultado: grep de los tres helpers vacío; retirar una pill la quita del Board y de dos tareas atómicamente; `atoms merge` reescribe menciones; goldens de ayuda/salida idénticos. Repo: deskops, worktree por nodo en robocop2 sobre origin/main b990c49e. Límites: fuera API de tags (CC35d/DO7) y vistas (CC34); no cambia formato del desk ni gramática CLI; no se inventan vías ausentes (a4).

## AMBIGUEDADES
1. «atoms merge reescribe menciones atom:<id> en prosa» frente a «MentionPattern ATOM (atom-<slug>)»: ¿la mención en prosa es `atom:<id>` o `atom-<slug>`? Obligaría a inventar qué regex ampliar.
2. «OUTPUT_SCOPE: deskops/services/, ... tests/, CHANGELOG.md» omite `docs/`, pero `files` incluye «docs/»: ¿entra documentación en `docs/`?
3. «se localizan las vías que hoy quitan referencias entrantes... Si no tienen, se deja escrito en el informe; no se inventan»: no dice qué comportamiento final tienen `drawer remove`/`closeout` si no existe vía.
4. «un solo commit o una sola escritura atómica»: ¿cuál de las dos se exige y se prueba?
5. «(o el comando que retire pills hoy)»: no se nombra; si no existe, ¿qué comando se usa?
6. «líneas antes y después»: sin unidad ni lugar donde registrarlo.

## DRY-RUN
Lecturas: contrato CC35c y a1–a8 en `dag.yaml`, `services/atoms.py` (helpers y usos), `services/retire.py`, `graph/desk_graph.py`, `atom_references.py`, `sldb.api.edges`. Cambios previstos: reemplazar los tres helpers por `referrers`/`rewrite_references` con `transaction=` dentro de `desk_transaction`; añadir/corregir `MentionPattern` si no cubre el caso; tests en `tmp_path` (pill en Board y dos tareas; fallo forzado revierte todo); CHANGELOG y docs. Dependencias: CC35a, CC33c, API GD22 de sldb. Validaciones futuras: grep vacío, pytest por archivo, goldens help/output, `deskops doctor` en los 6 desks, 4 pasos en clon limpio.

## FUTURO
El coordinador fija worktree y corre los 4 pasos en clon limpio; el supervisor corre la suite completa contra main; un humano decide la promoción y, si sldb no admite un caso, valida la hipótesis y la nota a sldb; el informe de a4 lo dispone quien opera el desk.
