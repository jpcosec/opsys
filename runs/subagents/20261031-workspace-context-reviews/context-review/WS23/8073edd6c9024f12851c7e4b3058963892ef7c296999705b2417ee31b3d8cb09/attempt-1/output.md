REFORMULACION
Propósito: implementar en graph_ui la vista de procedimiento que renderiza RitualDoc/StepDoc/lifecycle desde referencias reales, con pasos y fuentes navegables y transiciones solo representadas. Resultado: vista de solo lectura que abre documentos/soporte y muestra el estado de pasos proveniente de deskops, sin escribirlo ni auto-marcarlos. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/procedure/` y `tests/`. Límites: no acciones de transición, no escritura de estado; pruebas con corpus WS40 o store temporal; depende de WS13/WS09 y G_UI_READ por delta; promoción no autorizada.

AMBIGUEDADES
1. «El estado de un paso solo viene de deskops»: no identifica qué contrato o campo de deskops expresa ese estado ni cómo se corresponde con un StepDoc/RitualDoc. Obligaría a inventar el mapeo paso→estado y si los pasos authored tienen estado propio o son inertes.
2. «transiciones solo representadas, no accionables» frente a una aceptación que solo exige abrir documentos/soporte y no escribir estado: no fija criterio observable de “representada” ni de “no accionable”. Obligaría a inventar la comprobación de esas transiciones.

DRY-RUN
Lecturas: dag.yaml WS23 y vecinos, guía, brief, alcance, decisiones, cobertura y reconciliación; referencias de WS13/WS09.
Cambios previstos: componentes/rutas de procedimiento y tests en graph_ui; sin tocar deskops ni otros repos.
Dependencias: WS13 (lector/historia/foco) y WS09 (catálogo de renderizaciones); G_UI_READ pendiente y per_delta; WS40 o store temporal para pruebas.
Validaciones futuras: apertura de documentos/soporte, estado de paso no escrito, no auto-marcado; acta de recepción G_UI_READ por delta; WS30 validación humana posterior. Sin ejecución.

FUTURO
WS09 produce el catálogo; WS13 el lector; WS40 el corpus; WS11 el contrato de navegación; el solicitante emite el acta G_UI_READ del delta; WS06/promoción autoriza TaskDoc y archivos; WS30 valida UF y WS43 publica. Son productos o decisiones de otros nodos/humanos, no ambigüedades de WS23.
