REFORMULACION
Propósito: revisar si WS13.1 se entiende como encargo de planificación para lectura de documento, contexto y enlaces. Resultado: dictamen de claridad, sin ejecutar ni aceptar producto. Repo dueño: `graph_ui`, sobre workspace `a1b2b22`; depende del contrato WS11 y del gate `G_UI_READ` per-delta. Límites: no revisar nodos vecinos, no implementar, no aprobar API/Scion ni sustituir evidencia por commits previos.

AMBIGUEDADES
1. Foco compartido con Code cuando no hay correspondencia declarada. Cita: «Compartir foco solo donde exista correspondencia real de origen definida WS11; no inventar mapeo texto→código.» frente a «seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten». Obligaría a inventar qué ocurre si WS11 no define correspondencia para un Markdown sin modelo: si Code no es seleccionable, si el foco queda local o se limpia, y si la aceptación se evalúa solo donde hay correspondencia o en todos los casos.

DRY-RUN
Lecturas: nodo WS13.1, guía, brief, alcance, decisiones, cobertura, reconciliación, aristas WS11/WS13/WS13.2/WS13.3 y gate `G_UI_READ`. Cambios previstos: ninguno; solo este dictamen. Dependencias: contrato WS11 (identidad/origen/foco/enlaces), catálogo WS09 transitivo, acta externa `G_UI_READ` por delta, base `a1b2b22` y matriz WS06 vía WS11/WS12. Validaciones futuras: fuente cruda íntegra, panel con identidad/relaciones/origen, seguimiento de enlaces, alternancia texto/graph/code y foco por documento sin duplicar instancia; no basta `f16fcd1`.

FUTURO
WS11 produce el contrato de navegación y el mapa de recepción; WS09 el catálogo de vistas; P01/receptor del repo produce el acta `G_UI_READ` del delta; WS06/WS12 determinan el ticket o delta conciliado; WS13.2/WS13.3 completan explorador y pestañas; WS16/Taller validan. El TaskDoc de promoción fijará archivos, pruebas y textos. Nada de eso se decide aquí.
