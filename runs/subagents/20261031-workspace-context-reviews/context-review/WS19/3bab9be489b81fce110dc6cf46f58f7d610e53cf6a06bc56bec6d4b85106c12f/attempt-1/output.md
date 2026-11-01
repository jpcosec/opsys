## REFORMULACION
WS19 es un nodo agregado (`node_role: aggregate`, no ejecutable) del plan workspace-documental, repo dueño `graph_ui`. Encargo: integrar en el workspace a1b2b22 la edición de campos con conflicto visible y el alta/baja de relaciones permitidas, reutilizando editores/API, la precondición que fije WS12 y verifique WS45, sin editar campos protegidos ni crear semántica de relaciones en el componente. Resultado: salidas de WS19.1 y WS19.2; se cumple cuando ambos hijos cumplen su aceptación. Límites: no implementa por sí mismo; las mutaciones en UI solo se habilitan tras G_HUMAN_READ, aunque desarrollo y pruebas aisladas de API pueden avanzar. Depende de WS12 y de sus hijos.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Sin ejecutar: un ejecutor leería `dag.yaml` (WS19, hijos y gates), WS12, la evidencia de WS45, el acta de WS16 y la base graph_ui a1b2b22. No hay cambios propios de WS19. WS19.1 añadiría edición en `views/workspace/fields/` y tests: consume endpoints de WS12, aplica G_PAYLOAD_PRECONDITION y conserva el texto local ante rechazo/conflicto; transfiere a WS19.2 la misma precondición y disciplina de error visible. WS19.2 añadiría `views/workspace/relations/` y tests: alta/baja con API real, rechazo visible de relación no permitida o revisión obsoleta, sin definir semántica en el componente. El resultado conjunto se valida con la aceptación de ambos hijos —guardar/recargar, conflicto sin pérdida de texto y persistencia de relaciones—, no con un acto propio del agregado. Gates: G_HUMAN_READ antes de uso UI; G_UI_WRITE y G_WRITE_CONTRACT por delta de cada hijo; G_PAYLOAD_PRECONDITION pendiente. Si falta contrato o precondición: detener, registrar hueco y dejar la operación no disponible. WS21 y WS42 esperan a que ambos hijos terminen.

## FUTURO
WS12 fija representación y operaciones; WS45 produce G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 emite actas por delta; la promoción de cada hijo fija archivos, TaskDoc, pruebas y textos; un humano decide la aceptación y habilita las mutaciones en UI.
