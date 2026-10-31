REFORMULACION
Propósito: encargar a graph_ui una vista de procedimiento que represente RitualDoc/StepDoc/lifecycle sobre referencias reales, con pasos y fuentes navegables y transiciones solo representadas. Resultado: render de solo lectura en `frontends/mindmap/views/workspace/procedure/` con pruebas. Repo dueño: graph_ui. Límites: no escribe estado de pasos; el estado solo procede de deskops; no convierte transiciones en acciones; depende de WS13/WS09 y G_UI_READ; integración delta o ticket existente, sin duplicado paralelo; promoción no autorizada.

AMBIGUEDADES
ninguna. Las frases «RitualDoc/StepDoc/lifecycle sobre referencias reales», «pasos y fuentes navegables» y «transiciones solo representadas, no accionables» quedan acotadas por el glosario, WS09 y la aceptación; archivos, textos y escenarios detallados corresponden al TaskDoc de promoción.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación y fragmentos de dag (WS23, WS13, WS09, G_UI_READ). Cambios previstos: añadir vista read-only de procedimiento y tests en graph_ui; no tocar estado ni acciones. Dependencias: WS13 aporta lector/workspace; WS09 catálogo de renderizaciones/contrato o «sin contrato»; G_UI_READ pendiente; WS40 o store temporal para pruebas. Validaciones futuras: abrir procedimiento y sus documentos/soporte; comprobar que leer no marca pasos; verificar que el estado mostrado solo viene de deskops y que las transiciones no son accionables; integrar en ticket graph_ui según matriz WS06/WS11.

FUTURO
WS11 resuelve G_UI_READ; WS09 fija contrato/renderer de la fila; WS40 produce corpus; el TaskDoc de promoción precisará archivos, textos y escenarios; WS30 validará el recorrido; un humano decide P01/P02/P07/P08/P09 y autoriza promoción. Nada de esto se ejecuta aquí.
