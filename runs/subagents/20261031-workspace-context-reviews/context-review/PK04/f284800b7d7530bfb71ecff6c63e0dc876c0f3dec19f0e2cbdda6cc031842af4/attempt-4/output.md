## REFORMULACION
**Propósito:** revisar PK04 como encargo de planificación agregado, no como ejecución. **Resultado:** veredicto sobre si su aceptación es comprobable y sus límites están claros. **Repo:** PK04 agrupa hijos de `deskops` (WS17), `spec2viz` (WS18) y `graph_ui` (WS22–WS24). **Límites:** no ejecutar, no revisar los bloques edge de los hijos, no evaluar el producto ni resolver decisiones Pxx.

## AMBIGUEDADES
1. **Contradicción sobre el bloqueo.** La aceptación admite «revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable», pero luego afirma: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». No queda claro si un hijo `blocked` con responsable permite que PK04 sea verdadera o la invalida; el ejecutor tendría que inventar la regla.
2. **Actor del bloqueo no identificado.** «que el coordinador registra con responsable y dependencia en esa disposition.md»: ninguna fuente suministrada define quién es «el coordinador» ni cómo se le reconoce. Para verificar un bloqueo explícito habría que inventar el actor autorizado.

## DRY-RUN
**Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo PK04 y edges de WS17/18/22/23/24. **Cambios previstos:** ninguno en repos ni en `dag.yaml`; solo el registro/veredicto de revisión. **Dependencias:** revisiones vigentes y `disposition.md` de los cinco hijos; `context_review.py status`; hashes de input/contrato; coordinador para bloqueos. **Validaciones futuras:** ejecutar el comando de estado, comprobar coincidencia de hashes, existencia de `disposition.md`, ausencia de ambigüedad resuelta y coherencia de bloqueos.

## FUTURO
Las revisiones y disposiciones de WS17/18/22/23/24 las producen otros revisores; el coordinador registra bloqueos y el humano resuelve ambigüedades de los hijos. `context_review.py` calcula el estado; PK04 no decide por inferencia.
