REFORMULACION
WS30 valida de punta a punta la autoría y revisión manual en graph_ui: UF02, UF03 en edición, UF04, UF05 y UF01 con entradas authored de WS17 materializadas en el ejemplo. El resultado es un acta humana bajo `runs/subagents/workspace-documental-acceptance/manual/`, con guion, rutas/hashes, entradas validadas y recorridos, que resuelve G_HUMAN_MANUAL. Límites: no implementa correcciones, no declara un flujo listo por tests, no publica el desk real (WS43), no sustituye la lectura completa de WS16 y no atribuye causalidad ni corrige otros repos.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en `depends_on`. Obliga a inventar si el guion de WS08 es prerrequisito ejecutable o si WS30 debe reconstruirlo.
2. «entradas authored WS17 materializadas por generador WS40» e «integra conocimiento y tarea en ejemplo». WS40 tampoco figura en `depends_on`; WS17 solo produce plantillas. Obliga a inventar qué corpus usar y si esperar a WS40 o materializar por cuenta propia.
3. «que supervisor receptor autorice diagnóstico antes de atribuir nodo». No se identifica ese actor ni el registro del incidente. Obliga a inventar quién autoriza y dónde se asienta.

DRY-RUN
Lecturas: TaskDoc WS30, protocolo de validación, guion WS08, corpus del ejemplo, y salidas de WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28 y WS42. Cambios previstos: solo crear/actualizar el acta y sus soportes bajo `graph_ui:runs/subagents/workspace-documental-acceptance/manual/`; ningún cambio de producto. Dependencias y gates: se consumen las salidas y gates transitivos de esas aristas; WS30 no añade `requires` propios y produce G_HUMAN_MANUAL. Si falta corpus, contrato o guion, se detiene y registra el hueco con repo dueño, sin sustituto. Un fallo de guion bloquea el gate y abre tarea en el nodo causal; si la causa no está aislada, se registra incidente sin atribuir nodo. Validación esperada: la persona completa el recorrido sin instrucciones verbales correctivas; el acta enumera rutas/hashes, entradas y resultados, se versiona en commit atómico y su blob es enlazable; solo entonces G_HUMAN_MANUAL puede resolverse.

FUTURO
WS31 y WS43 consumen el acta; WS43 contrasta las entradas WS17 validadas con la publicación real. La persona participante decide la aceptación; WS08 debe producir el guion y WS40 el corpus materializado.
