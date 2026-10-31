# Executor comparison — WS29, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: integrar en graph_ui un delta sobre la tarea Changes que haga comprobable el impacto de una mutación del store. Resultado: vista que muestra documento afectado, relaciones entrantes/salientes a 1 hop vía API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando, con enlace a reparación documentada; sin reparación automática ni CST/Kimun. Repo: graph_ui; salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según WS11 y tests. Límites: solo lectura (G_UI_READ), pruebas en store temporal real, extensión independiente que no bloquea lector/manual; promoción no autorizada.

## Hallazgos/disposición contra intención

Descartados 1/2: output_scope incluye «rutas de integridad según contrato WS11» y scope API de grafo; WS11/03 deben producir canal/formato comprobado y clasificar faltantes. No autoriza parser inventado. Hallazgos se agrupan por comando como indica scope; atribución a documento solo si evidencia/API la soporta, resto hallazgo del store. Casos de prueba concretos son promoción sobre store real; si falta contrato, regla común bloquea, no cambia core.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
