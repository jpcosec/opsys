REFORMULACION
Propósito: revisar WS27 como encargo de planificación, no como implementación. Resultado: nodo agregado que integra diff Git (WS27.1) y evidencia (WS27.2) junto a la TaskDoc. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: es `aggregate`, no ejecutable; su aceptación es que todos sus hijos cumplan la suya; depende de WS13, WS12 y sus hijos; requiere `G_UI_READ`; promoción `not_authorized` y sujeta a TaskDoc/preflight.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas declaradas: nodo WS27, guía de revisión, brief, alcance, decisiones, cobertura y contratos vecinos aportados; sin herramientas ni ejecución.
Cambios previstos: ninguno propio de WS27; WS27.1 produce diff/historial read-only en `frontends/mindmap/views/workspace/diff/` y WS27.2 evidencia en `frontends/mindmap/views/workspace/evidence/`, ambas con tests.
Dependencias: WS13, WS12, WS27.1 y WS27.2; `G_UI_READ` como gate. WS13/WS12 ya son exigidas por los hijos.
Validaciones futuras: aceptación de WS27.1 (diff real, read-only, por repo/tarea, sin hallazgos de integridad de WS29) y de WS27.2 (declarada/encontrada/verificada distinguidas; evidencia ausente visible; apertura soportada solo si es Markdown del workspace); cierre agregado cuando ambos hijos cumplan.

FUTURO
WS11 produce/resuelve `G_UI_READ` con acta e identidad humana. WS12 produce el contrato de operaciones/lectura y requiere `G_WRITE_POLICY` aprobado por WS07. Los hijos implementan; WS28 y WS35 consumen WS27. La promoción fijará archivos, pruebas y textos exactos en TaskDoc. Las decisiones P01/P03/P04/P05 y la designación de responsables son humanas, no de este nodo.
