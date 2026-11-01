## REFORMULACION
PK04 es un macroencargo de planificación, no una tarea ejecutable: agrupa la navegación y las representaciones authored del desk sobre una identidad común. Su propósito es que Board, procedimiento, conocimiento e índices abran los mismos documentos/soportes desde distintas vistas, sin escribir estado desde renderers ni marcar pasos por lectura. El resultado sustantivo es el paquete integrado de salidas de WS17, WS22, WS23 y WS24, más WS18 solo si G_SPEC_VIEW se recibe; los índices deben seguir sus fuentes. Repo dueño: deskops para coordinación; implementación en graph_ui y, para WS18, spec2viz. Límites: no ejecuta, no autoriza tareas ni añade aristas; el gate de revisión no acredita completitud sustantiva. Termina cuando terminan sus hijos y se demuestra la integración indicada.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Hipotético, sin ejecutar. Con WS09/WS11/WS13/WS40 disponibles: WS17 escribe plantillas `ejemplo/nav/`; WS40 regenera el corpus y emite manifiesto. WS22 implementa Board; WS23 procedimiento; WS24 conocimiento/vecindad, todos en graph_ui y consumiendo WS13/WS09. WS18 queda separado: tras G_SPEC_VIEW, declara ViewDoc/NotationDoc y los prueba con graph_ui sobre store real.

Transferencias: WS17 aporta plantillas a WS40; WS40 aporta manifiesto/corpus a WS22/23/24; WS13 aporta lector/foco/historia; WS09 catálogo; WS11 identidad/resolución. Validación integrada: regenerar corpus, abrir el mismo TaskDoc desde lista, tablero y dependencias; abrir documentos y soportes desde procedimiento y conocimiento; comprobar que renderers no escriben status, que leer no marca pasos y que los índices resuelven fuentes. Si G_SPEC_VIEW existe, evaluar el ViewDoc concreto en graph_ui. Dependencias: G_UI_READ para hijos de graph_ui; G_SPEC_VIEW solo para WS18.

## FUTURO
Producen otro nodo: WS17, WS18, WS22, WS23, WS24 y los contratos WS09/WS11/WS13/WS40. Deciden humano/receptor: G_SPEC_VIEW, G_UI_READ, G_PRODUCT y la aceptación de deltas por repo. PK04 solo integra y verifica salidas; no las ejecuta.
