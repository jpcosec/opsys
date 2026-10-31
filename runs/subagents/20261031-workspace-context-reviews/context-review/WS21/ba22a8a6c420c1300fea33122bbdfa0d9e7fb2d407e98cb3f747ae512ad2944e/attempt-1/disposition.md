# Executor comparison — WS21, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

Propósito: encargo de planificación para integrar fuente y renderizado en el workspace según `source_mode`, reutilizando guardado autorizado. Resultado: alternancia fuente/render con mismo origen, revisión y buffer sucio; composición escribe solo en el documento dueño si WS12 lo soporta. Repo dueño: `graph_ui`, con salidas en `frontends/mindmap/views/workspace/; tests/`. Límites: no se ejecuta ni promociona; P04 fija `editable`, lo que añade WS20 y G_SOURCE; no se prepara con `pending`; no se inventa API ni se excede el `output_scope`.

##

## Hallazgos/disposición contra intención

Preview de render de buffer vs persistido es interacción que contrato WS11/12, catálogo WS09 y TaskDoc fijan antes de implementar. Aceptación invariante es mismo origen/revisión y buffer conservado, sin descarte sin confirmación y sin prometer guardado no observado. No se delega permiso ni fuente extra; ambos soportes tienen productor y se detiene si contrato falta. Dry-run recupera variante editable/G_SOURCE y protección de datos.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
