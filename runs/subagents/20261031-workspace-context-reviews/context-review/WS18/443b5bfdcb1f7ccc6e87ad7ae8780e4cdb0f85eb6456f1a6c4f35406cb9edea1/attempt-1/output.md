REFORMULACION
Propósito: declarar proyecciones de grafo reutilizables en spec2viz, sin crear UI declarativa ficticia. Resultado: un ViewDoc con su NotationDoc para selecciones y notación ya soportadas, con tests, portable y documentado. Repo dueño: spec2viz; salida prevista en `sldb/views/` y `tests/`, con rutas confirmadas al promover. Límites: solo selecciones/notación soportadas; no modificar el repo desde este plan; promoción no autorizada; depende de WS09 y WS11 y exige G_SPEC_VIEW.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas previstas: catálogo de WS09, contrato/acta G_SPEC_VIEW de WS11, soporte real de spec2viz para ViewDoc/NotationDoc y el TaskDoc de promoción.
Cambios previstos: definir ViewDoc y NotationDoc en `sldb/views/` y pruebas en `tests/`.
Dependencias: WS09 y WS11 como prerrequisitos; G_SPEC_VIEW pendiente y resuelto por WS11; recepción y promoción por el dueño designado de spec2viz.
Validaciones futuras: renderizar el mismo ViewDoc sobre un store real, comprobar que coincide con la selección declarada, verificar ausencia de código específico del host y que el ViewDoc documenta qué selecciona. No se ejecuta nada.

FUTURO
WS11 debe producir el acta G_SPEC_VIEW y identificar al responsable de spec2viz; el dueño de spec2viz confirma rutas, recepción y promoción de tareas; el TaskDoc fija archivos, escenarios y evidencia. La decisión humana sobre P01/P04 y la autorización de promoción quedan fuera de este nodo.
