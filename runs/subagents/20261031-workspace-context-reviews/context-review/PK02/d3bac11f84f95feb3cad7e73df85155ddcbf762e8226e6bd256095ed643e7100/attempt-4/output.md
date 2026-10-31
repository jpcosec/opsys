## REFORMULACION
PK02 es un nodo agregado de revisión, no una tarea ejecutable. Su propósito es comprobar que cada hijo directo —WS07, WS08, WS09, WS10, WS11 y WS12— tiene una revisión de contexto vigente, sin ambigüedad de encargo o con bloqueo explícito que indique responsable y dependencia. El resultado esperado es determinar si la aceptación de PK02 es verdadera; no produce artefactos de producto. El repo dueño es `deskops`. Límites: solo se evalúa PK02 y el estado de sus hijos; no se revisan los bloques `edge` como contratos vecinos, no se ejecuta el script ni se modifica `dag.yaml`, disposiciones o decisiones.

## AMBIGUEDADES
ninguna.

La aceptación define la condición de verdad, la fuente (`context_review` del hijo en `dag.yaml`), la coincidencia exigida de hashes, la existencia de `disposition.md` y el comando de comprobación. El bloqueo explícito también queda definido con responsable y dependencia. No hay una frase que obligue al ejecutor de PK02 a inventar resultado, aceptación, repo, actor o límite.

## DRY-RUN
Lecturas previstas: `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, el nodo `PK02` y los estados de revisión de WS07–WS12 en `dag.yaml`. Cambios previstos: ninguno. Dependencias: los seis hijos directos y sus `disposition.md`; el script `context_review.py` como comprobador de estado. Validaciones futuras, sin ejecutar: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`; verificar hash de input y de contrato; verificar disposición guardada en el intento; tratar como no verdadera cualquier hijo `pending` o `blocked` sin responsable/dependencia registrados.

## FUTURO
Los nodos hijos producen sus revisiones y `disposition.md`. El coordinador registra bloqueos explícitos con responsable y dependencia. El humano de WS07 resuelve P01–P09 y designa responsables; esas decisiones no se presuponen aquí. La comprobación automatizada determina el estado de PK02.
