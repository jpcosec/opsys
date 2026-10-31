## REFORMULACION

Propósito: revisar PK07 como encargo de planificación. Resultado: agrupación de revisión cuyos hijos WS29 y WS39 tengan revisión vigente, sin ambigüedad propia ni bloqueo externo con responsable. Repo: PK07 no declara `owner_repo` porque es agrupación, no entregable ejecutable; sus hijos declaran `graph_ui`. Límites: no evalúa producto, no ejecuta, no revisa los bloques edge vecinos ni autoriza implementación. Aceptación comprobable mediante `context_review.py status`, hashes vigentes y `disposition.md`.

## AMBIGUEDADES

ninguna

## DRY-RUN

Lecturas previstas: `dag.yaml` (PK07, WS29, WS39), guía de revisión, `brief.md`, `alcance.md`, `decisiones.md` y `cobertura.md`. Cambios previstos: ninguno; esta revisión no modifica nodos ni archivos. Dependencias: PK07 no tiene dependencias operativas; WS29 depende de WS15/WS24 y requiere `G_UI_READ`; WS39 depende de WS12 y requiere `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras, sin ejecutar: desde la raíz de deskops, `python desk/drawer/plans/workspace-documental/context_review.py status`; comprobar que el hash de input y contrato de cada hijo coincide con los actuales y que existe `disposition.md` en el intento correspondiente. Si hay bloqueo, verificar que sea externo, con responsable y dependencia registrados. Un hijo con ambigüedad propia sin resolver no satisface PK07.

## FUTURO

Las revisiones de WS29 y WS39 las producen sus respectivos nodos de context review. La sesión de coordinación que ejecute `context_review.py` registra cualquier bloqueo externo y su responsable. Para WS39, el participante humano fijado por P08 produce el acta de prueba; `G_HUMAN_MODEL` debe pasar antes de marcar la capacidad disponible en el manual, y WS31 publica el capítulo 15. La aceptación de implementación de WS29/WS39 no forma parte de PK07.
