REFORMULACION
- **Propósito**: planificar un delta de la vista Changes que haga comprobable el impacto de una mutación real sobre el store, sin convertirlo en un árbol CST/Kimun.
- **Resultado**: extensión en `graph_ui` que muestre documento afectado, relaciones entrantes/salientes a 1 hop según la API de grafo de `sldb`, y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check` agrupados por comando; enlaces al comando documentado correspondiente, sin reparación automática; pruebas sobre store temporal real.
- **Repo**: `graph_ui` (`output_base: graph_ui:repository_root/`), salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según contrato WS11 y `tests/`.
- **Límites**: delta sobre la tarea Changes actual, sin duplicado paralelo; no CST ni árbol Kimun supuesto; no bloquea lector/manual básico; `G_UI_READ` pendiente.

AMBIGUEDADES
1. «muestra documento afectado, relaciones alcanzadas (...) y errores. (...) errores = hallazgos de esos tres comandos, agrupados por comando». No se especifica si deben mostrarse **todos** los hallazgos o solo los asociados al documento afectado. El ejecutor tendría que inventar el criterio de filtrado y el alcance de la lista de errores.

DRY-RUN
- **Lecturas**: nodo WS29, aristas WS15/WS24, gate `G_UI_READ`, brief, alcance, decisiones, cobertura UF07, reconciliación y guía.
- **Cambios previstos**: extender la vista Changes existente; integrar relaciones a 1 hop vía API de grafo; presentar hallazgos agrupados por comando; enlaces a documentación de reparación; tests con store temporal.
- **Dependencias**: WS15 (errores de lectura), WS24 (grafo/backlinks/vecindad), WS11 como productor de `G_UI_READ` y del contrato de rutas de integridad, auditoría de WS03 vía WS24, y comandos verificados según P02.
- **Validaciones futuras**: prueba de aceptación sobre store temporal real, cierre de `G_UI_READ`, prueba propia de WS29 en UF07 y promoción mediante TaskDoc. Sin ejecutar nada.

FUTURO
- WS11 producirá la aceptación `G_UI_READ`, la tarea receptora y el contrato de rutas de integridad.
- WS03/auditoría definirá la API de grafo de `sldb`; WS12 registrará acuerdos de mutación si corresponden.
- El humano resolverá P01/P02/P04/P07/P09 y WS07 identificará actores; el TaskDoc de promoción fijará archivos, escenarios y textos dentro de la aceptación.
