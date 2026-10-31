## REFORMULACION

**Propósito:** revisar PK08 como encargo de planificación: agrupación de revisión del ramal Scion, no ejecutable.
**Resultado:** dictamen sobre si su aceptación es comprensible y comprobable, sin evaluar producto ni hijos.
**Repo:** PK08 no declara `owner_repo`; por ser agrupación de revisión no ejecutable, no procede asignarle uno. Los hijos pertenecen a `deskops` y `graph_ui`, pero sus contratos no se revisan aquí.
**Límites:** no ejecutar `context_review.py`; no resolver Pxx, gates ni bloqueos; no revisar bloques `edge` de vecinos; no convertir la revisión en aprobación.

## AMBIGUEDADES

Ninguna. La aceptación identifica el universo de hijos, el criterio de revisión vigente, la fuente de verdad (`context_review.py status`), el tratamiento de ambigüedad propia y la excepción de bloqueo externo con responsable registrado.

## DRY-RUN

**Lecturas previstas:** guía, nodo PK08, IDs de hijos (`WS32`–`WS38`, `WS44`), metadatos `context_review` y `disposition.md` de cada hijo, más brief/alcance/decisiones/cobertura para contexto. No se leen como revisión los contratos `edge` de los hijos.

**Cambios previstos:** ninguno sobre archivos; solo emitir el dictamen de revisión.

**Dependencias:** script `context_review.py` disponible desde la raíz de `deskops`; hashes actuales de input y contrato de cada hijo; `disposition.md` guardada en el intento correspondiente.

**Validaciones futuras:** ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status`; comprobar los ocho hijos; admitir solo bloqueos externos con responsable y dependencia registrados; rechazar ambigüedad propia sin resolver.

## FUTURO

Los revisores de cada hijo producen sus disposiciones; la sesión de coordinación clasifica y registra bloqueos externos; WS07 designa operador Scion y acceso read-only; WS44 produce `G_SCION`; el humano resuelve Pxx. Nada de esto se decide en PK08.
