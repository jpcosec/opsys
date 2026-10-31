## REFORMULACION
Propósito: encargo de planificación para que `graph_ui` implemente una vista read-only de diff Git e historial junto al encargo, acotada a repo y tarea, y distinga cambios de código de integridad del store. Resultado: vista en `frontends/mindmap/views/workspace/diff/`, con rutas de lectura según contrato WS11 y tests. Repo dueño: `graph_ui`. Límites: solo lectura; sin execute/revert genérico; promoción no autorizada y sin ejecución.

## AMBIGUEDADES
1. «Diff real acotado al repo y tarea»: no se fija el baseline del diff. Obliga a inventar qué se compara —working tree, HEAD, rango de commits— y cómo se selecciona. WS12 menciona política Git, pero el nodo no declara que ese contrato produzca el baseline.
2. «acotado al repo y tarea»: no se define qué identifica la “tarea” ni cómo se relaciona con repo/rutas. Obliga a inventar la fuente del identificador y el filtro. WS35 solo añade «asociación a intento», no la identidad de tarea.
3. «Diff Git e historial read-only» frente a «sin execute/revert genérico»: “genérico” deja abierta la posibilidad de execute/revert dirigidos, contradiciendo el límite read-only. Obliga a inventar si alguna mutación específica está permitida.
4. «diferenciar cambios de código de integridad del store»: no hay criterio, etiquetas ni evidencia esperada para esa clasificación. Obliga a inventar categorías y cómo demostrarlas; además, no aparece en la aceptación.

## DRY-RUN
Lecturas previstas: nodo y guía; contrato de rutas WS11; contrato de operaciones/política Git WS12; lector WS13; código y tarea existentes en `graph_ui`. Cambios previstos: componentes read-only de diff/historial bajo la ruta indicada, clasificación código/store y tests; ninguna mutación. Dependencias: WS12, WS13 y gate `G_UI_READ` pendiente. Validaciones futuras: diff real acotado, ausencia de execute/revert, tests, evidencia del gate y preflight task-only. Sin ejecutar nada.

## FUTURO
WS11 produce rutas de lectura y `G_UI_READ`; WS12 produce política Git/operaciones; WS35 añadirá asociación a intento; WS27.2 aportará evidencia; el agregado WS27 cerrará cuando cierren sus hijos. La promoción y cualquier aprobación humana quedan fuera de este nodo.
