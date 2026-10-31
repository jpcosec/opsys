REFORMULACION
Propósito: revisar si WS27 se entiende como encargo de planificación agregado para integrar revisión de cambios y evidencia. Resultado: nodo `aggregate` en `graph_ui` que agrupa WS27.1 (diff Git) y WS27.2 (evidencia); no ejecutable, se cierra cuando ambos hijos cumplen su aceptación. Repo dueño: `graph_ui`. Límites: no implementa ni ejecuta; depende de WS13, WS12 y sus hijos; requiere `G_UI_READ` por delta; no autoriza promoción; no revisa los bloques edge vecinos.

AMBIGUEDADES
Ninguna. La aceptación agregada está definida: «se cumple cuando todos sus hijos cumplen su aceptación». El rol `aggregate` aclara que no se ejecuta. El gate `G_UI_READ` pendiente y la recepción por delta son estados intencionales, no huecos que obliguen a inventar al ejecutor de este nodo.

DRY-RUN
Lecturas: nodo WS27 en `dag.yaml` y guía; brief, alcance, decisiones y cobertura para límites. Cambios previstos: ninguno; solo veredicto de revisión. Dependencias: WS13 (lector/foco/historia), WS12 (contrato de operaciones), WS27.1 y WS27.2; `G_UI_READ` con `evaluation: per_delta` y `contract_source: WS11`. Validaciones futuras: al promover, comprobar la aceptación de cada hijo y el recibo del delta concreto; no exigir aceptación conjunta ni implementar en esta revisión.

FUTURO
WS27.1 y WS27.2 producen las implementaciones de diff y evidencia; WS13 y WS12 sus contratos; el receptor humano P01 emite actas `G_UI_READ` por delta en `graph_ui`; la promoción fijará archivos, pills y evidencia. WS28 y WS35 consumirán WS27.
