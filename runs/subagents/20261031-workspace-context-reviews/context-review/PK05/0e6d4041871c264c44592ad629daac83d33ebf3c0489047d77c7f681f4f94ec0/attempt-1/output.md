## REFORMULACION

**Propósito:** revisar PK05 como encargo de planificación de la Entrega M: agrupación de revisión de autoría y operación manual, no una tarea ejecutable.

**Resultado:** PK05 es verdadero cuando cada hijo directo —WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30, WS42— tiene `context_review` vigente, con hashes de input y contrato actuales y `disposition.md` guardada, o un bloqueo externo explícito con responsable registrado en esa disposición. PK05 no produce código ni entregables propios.

**Repo:** PK05 no declara `owner_repo`; su aceptación remite a la raíz de `deskops` y a `context_review.py`, coherente con una agrupación no ejecutable.

**Límites:** no ejecuta nada, no autoriza candidatas, no sustituye gates `G_*` ni decisiones Pxx, y no revisa los bloques edge de sus vecinos.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía de context review, brief, alcance, decisiones, cobertura y aceptación de PK05 y de sus hijos directos.

**Cambios previstos:** emitir una `disposition.md` para PK05 con veredicto y causa; no modificar `dag.yaml` ni promover nodos.

**Dependencias:** PK05 no tiene `depends_on`/`requires` propios; su verdad depende de las revisiones de sus hijos. Los hijos arrastran WS12, WS16, WS17, WS22, WS40, gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, `G_SOURCE`, `G_CLOSEOUT`, `G_SLDB_WRITE` y las decisiones P03–P06/P04.

**Validaciones futuras:** la sesión de coordinación ejecutará `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops` para comprobar hashes y disposiciones; si falta un hijo o hay ambigüedad propia, PK05 no será verdadero; si hay bloqueo externo, deberá constar responsable y dependencia.

## FUTURO

La sesión de coordinación ejecuta el status y registra bloqueos; el humano responsable resuelve `P04` (`source_mode`), `G_CLOSEOUT`, `G_SOURCE` y demás decisiones pendientes. Las revisiones de los hijos determinan PK05; este revisor solo deja constancia, sin ejecutar ni aprobar.
