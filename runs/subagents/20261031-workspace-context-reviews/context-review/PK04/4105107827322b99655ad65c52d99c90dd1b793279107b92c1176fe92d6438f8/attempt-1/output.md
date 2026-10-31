## REFORMULACION
**Propósito:** revisar si PK04, como nodo de planificación, está bien formulado: agrupación de revisión de navegación y representaciones.
**Resultado:** veredicto de revisión del encargo, no implementación ni ejecución.
**Repo:** PK04 no declara `owner_repo` propio; es agrupación de revisión. El script de comprobación vive en `deskops`.
**Límites:** no ejecutar nada; no revisar los bloques edge de sus hijos; no evaluar calidad de producto; no convertir PK04 en tarea operativa.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** nodo PK04 en `dag.yaml`; lista de hijos WS17, WS18, WS22, WS23, WS24; `context_review.py status` como comando futuro, sin ejecutarlo; `disposition.md` de los intentos correspondientes a los hashes vigentes.
**Cambios previstos:** ninguno. PK04 no se ejecuta ni produce artefactos; su aceptación solo se evalúa.
**Dependencias:** los cinco hijos directos; sus revisiones vigentes y, en su caso, bloqueos externos con responsable registrado. WS18 arrastra `G_SPEC_VIEW`; WS17 depende de WS40; WS22/23/24 dependen de WS13 y WS09. No se revisan sus contratos aquí.
**Validaciones futuras:** comprobar que cada hijo tiene `context_review` con hash de input y contrato coincidentes con los actuales y `disposition.md` guardada; verificar que los bloqueos son externos, con responsable y dependencia declarada; confirmar que no hay ambigüedad propia pendiente en ningún hijo.

## FUTURO
La sesión de coordinación ejecutará `context_review.py status` y registrará las disposiciones y bloqueos. Los hijos producirán sus propias revisiones; WS18 necesitará `G_SPEC_VIEW` y WS17 dependerá del corpus de WS40. Nada de eso corresponde decidirlo a PK04.
