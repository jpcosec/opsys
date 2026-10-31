## REFORMULACION

**Propósito:** revisar PK07 como encargo de planificación. PK07 es una agrupación de revisión —no una dependencia operativa ni un nodo ejecutable— de WS29 y WS39.

**Resultado:** PK07 es verdadero cuando cada hijo directo tiene revisión vigente: `context_review` con hashes de input y contrato coincidentes con los actuales y `disposition.md` guardada en el intento correspondiente; o bien un bloqueo explícito externo, registrado con responsable y dependencia.

**Repo:** PK07 no declara `owner_repo`. Sus hijos pertenecen a `graph_ui`; la comprobación se ejecuta desde la raíz de `deskops` con `python desk/drawer/plans/workspace-documental/context_review.py status`.

**Límites:** no ejecutar nada; no revisar los contratos de los vecinos (WS15, WS24, WS12, WS16); no aprobar propuestas Pxx; no implementar WS29/WS39. La extensión no bloquea lector ni manual básico.

## AMBIGUEDADES

ninguna.

La aceptación es mecánica y comprobable mediante el comando indicado. La distinción entre ambigüedad propia del hijo y bloqueo externo con responsable está explicitada. Los detalles de hash y `disposition.md` quedan delegados a `context_review.py`, no al ejecutor de PK07.

## DRY-RUN

**Lecturas:** nodo PK07 y bloques de WS29/WS39 en `dag.yaml`; guía de revisión; brief, alcance, decisiones y cobertura; en el futuro, salida de `context_review.py status`.

**Cambios previstos:** ninguno. Es revisión, no promoción ni edición.

**Dependencias:** WS29 depende de WS15, WS24 y `G_UI_READ`; WS39 de WS12, WS16 y requiere `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. PK07 depende de las revisiones vigentes de ambos hijos.

**Validaciones futuras:** ejecutar `context_review.py status` desde `deskops`; verificar coincidencia de hashes de input y contrato; comprobar `disposition.md` en el intento correcto; confirmar que un bloqueo es externo y tiene responsable.

## FUTURO

La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos externos con su responsable. Las revisiones de WS29/WS39 producen sus `disposition.md`; una ambigüedad propia sin resolver mantiene PK07 no verdadero. Las decisiones P01/P04/P08 y los contratos de WS12/WS16 son insumos de otros nodos y no se resuelven aquí.
