## REFORMULACION
WS27 es un nodo **aggregate** de implementación cuyo propósito es agrupar la revisión de cambios y evidencia. Su resultado son las salidas de WS27.1 (diff Git read-only) y WS27.2 (evidencia declarada/encontrada/verificada). Repo dueño: `graph_ui`. No se ejecuta: termina cuando sus hijos cumplen su aceptación; sus dependientes siguen apuntando a WS27. Depende de WS13, WS12 y de sus hijos WS27.1/WS27.2, y requiere `G_UI_READ`. Límite: no revisar contratos de nodos vecinos ni ejecutar nada.

## AMBIGUEDADES
ninguna.

El alcance, la aceptación agregada, el repo y las dependencias están definidos; la guía aclara que un `aggregate` no se ejecuta y que un gate pendiente es intencional.

## DRY-RUN
- **Lecturas:** nodo WS27 en `dag.yaml`; guía, brief, alcance, decisiones, cobertura y gates aportados.
- **Cambios previstos:** ninguno; esta revisión no modifica archivos ni ejecuta comandos.
- **Dependencias:** WS12 y WS13 como prerrequisitos; WS27.1 y WS27.2 como hijos; `G_UI_READ` pendiente, resuelto por WS11.
- **Validaciones futuras:** comprobar que WS27.1 y WS27.2 cumplen su aceptación; verificar `G_UI_READ`; en promoción, revisar `task_file`, archivos, pills, átomos y evidencia, y el preflight task-only indicado.

## FUTURO
WS11 debe producir el acta de aceptación de lectura (`G_UI_READ`). WS12 debe cerrar el contrato de operaciones/escritura aplicable. WS27.1 y WS27.2 producen diff y evidencia; su promoción fijará TaskDoc, archivos y pruebas. Las decisiones humanas P01/P04/P07/P08/P09 y la designación de responsables corresponden a WS07 o al solicitante, no a este nodo.
