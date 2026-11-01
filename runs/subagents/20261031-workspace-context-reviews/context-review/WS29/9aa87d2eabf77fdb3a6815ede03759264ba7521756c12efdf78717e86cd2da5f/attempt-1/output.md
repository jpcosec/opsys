## REFORMULACION

**Propósito:** integrar en el lector una vista Changes que haga comprobable el impacto de una mutación del store. **Resultado:** delta sobre la tarea Changes actual que muestra documento afectado, relaciones entrantes/salientes a 1 hop mediante la API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando, con enlace al comando documentado; reparar no es automático. **Repo:** graph_ui; `frontends/mindmap/views/workspace/changes/`, rutas de integridad según contrato WS11 y `tests/`. **Límites:** sin CST/Merkle Kimun, sin duplicar la tarea Changes, sin bloquear lector/manual básico.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS29 y gates, aristas WS15/WS24 y referencia externa de Changes. Sin ejecutar comandos ni pruebas.

**Cambios previstos:** extender el ticket Changes existente; añadir la integración Changes en `views/workspace/changes/`; consumir las rutas de integridad que fije WS11; añadir pruebas en repo graph_ui. No reparar automáticamente.

**Dependencias:** WS15 (errores y degradación), WS24 (grafo/backlinks), WS11 como fuente de rutas de integridad, API de grafo de sldb, comandos de sldb y deskops, G_UI_READ.

**Validaciones futuras:** mutación real en store temporal; documento afectado visible; relaciones entrantes y salientes a 1 hop; hallazgos agrupados por comando y enlaces a su documentación; ausencia de CST/Kimun; no duplicación del ticket; preflight de promoción.

## FUTURO

- WS11 debe publicar las rutas de integridad y su forma.
- WS06 y el proceso de promoción deciden la integración en el ticket Changes existente; el TaskDoc fijará archivos, pruebas y textos.
- El receptor P01 emite el acta G_UI_READ por este delta.
- La aceptación real de WS29 se prueba sobre store temporal; el ticket externo observado no acredita aceptación.
- Reparaciones quedan como enlace/handoff al comando documentado, no como acción de la vista.
