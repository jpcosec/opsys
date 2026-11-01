REFORMULACION
PK04 es un agregado de planificación, no ejecutable, del plan workspace-documental. Propósito: agrupar entregables que hacen navegables las entradas authored y las representaciones del desk sobre identidad común. Resultado sustantivo: paquete integrado donde índices authored, Board, procedimiento y conocimiento abren los mismos documentos/soportes; los índices se regeneran desde sus fuentes; los renderers no escriben estado ni marcan pasos por lectura. Repo dueño: deskops; hijos escriben en deskops (WS17), graph_ui (WS22–24) y spec2viz (WS18). Límites: no ejecuta, no autoriza tareas, no añade aristas; WS18 es extensión opcional tras G_SPEC_VIEW y no bloquea WS24; no se inventan índices, estados ni selecciones.

AMBIGUEDADES
Ninguna.

DRY-RUN
Hipotético: con WS11/WS40, WS09/WS13 y G_UI_READ disponibles, ejecutar en paralelo lógico WS17 (consume WS11/WS40; escribe plantillas `ejemplo/nav/`), WS22/23/24 (consumen WS13/WS09; escriben vistas Board, procedimiento y conocimiento en graph_ui). WS40 regenera el corpus temporal con plantillas WS17; WS17 no es productor del corpus. WS22 transfiere lista/tablero/dependencias; WS23 procedimiento inerte; WS24 grafo/vecindad; todos reutilizan lector/registry de WS13. WS18, solo si P01/receptor emite G_SPEC_VIEW, produce ViewDoc/NotationDoc en spec2viz y los evalúa con `evaluate_view` de graph_ui sobre store real; no bloquea WS24. Integración: sobre corpus WS40 regenerado, abrir el mismo TaskDoc desde Board (lista/tablero/dependencias), procedimiento y conocimiento; verificar identidad/enlaces, índices que resuelven ambos desks sin duplicar registry, y ausencia de escrituras/estado mutado. Si falta contrato/gate: detener y registrar hueco, sin sustituto. Validación futura: prueba integrada sobre WS40 y recibos por delta; no ejecutada.

FUTURO
P01/receptor emite G_SPEC_VIEW por delta; el dueño de spec2viz promueve/ejecuta WS18; receptores graph_ui emiten G_UI_READ; WS16/WS30 o aceptación humana validan lector/índices. PK04 no decide ni ejecuta.
