## REFORMULACION
Propósito: revisar WS27 como encargo de planificación. Resultado: nodo agregado no ejecutable que integra diff Git, historial read-only y evidencia junto al encargo, distinguiendo cambios de código de integridad del store. Repo dueño: `graph_ui`. Límites: depende de WS13, WS12, WS27.1 y WS27.2; requiere `G_UI_READ`; no autoriza promoción ni ejecución; su aceptación es la de sus hijos.

## AMBIGUEDADES
1. «diferenciar cambios de código de integridad del store» carece de criterio comprobable. Las aceptaciones hijas cubren diff real (WS27.1) y evidencia declarada/encontrada/verificada (WS27.2), pero ninguna define qué representa «integridad del store» ni cómo mostrarla. Obligaría al ejecutor a inventar fuente, indicador y validación.
2. «artefactos de evidencia junto al encargo» no define qué es «el encargo» ni su ubicación. WS27.2 remite a «rutas de lectura definidas por el contrato WS11», pero el input no incluye ese contrato; sin él, el ejecutor debe inventar el contenedor o ubicación. No basta con que WS11 sea productor futuro: el nodo no indica qué hacer si falta.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS27, nodos hijos, dependencias WS13/WS12 y gate `G_UI_READ`. Cambios previstos: ninguno; esta revisión no edita archivos ni promueve el nodo. Dependencias: WS13 y WS12 como prerrequisitos, WS27.1/WS27.2 como hijos; `G_UI_READ` pendiente es intencional. Validaciones futuras: comprobar aceptación de cada hijo, diff acotado a repo/tarea sin revert, evidencia ausente visible como ausente, y resolver la ambigüedad de integridad del store antes de promover.

## FUTURO
WS11 debe aceptar el delta de lectura y resolver `G_UI_READ`; WS12 cierra el contrato de operaciones; WS28 y WS35 consumen WS27. La promoción, archivos exactos, pills, átomos y preflight corresponden al nodo de promoción y decisión humana, no a esta revisión. Las propuestas Pxx siguen sin aprobación.
