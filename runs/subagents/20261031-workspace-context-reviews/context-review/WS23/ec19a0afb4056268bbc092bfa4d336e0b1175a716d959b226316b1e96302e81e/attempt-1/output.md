## REFORMULACION
**Propósito:** entregar en `graph_ui` un renderer que presente rituales y pasos como procedimiento navegable, sobre documentos y soporte reales.
**Resultado:** una vista de procedimiento que abre sus documentos y soporte, sin marcar pasos como realizados por el mero hecho de leerlos; incluye tests.
**Repo:** `graph_ui` (`frontends/mindmap/views/workspace/procedure/`; `tests/`).
**Límites:** depende de WS13 y WS09; exige `G_UI_READ`, aún pendiente (la produce WS11); no hay promoción autorizada; integración solo como delta o ticket existente tras WS06, nunca duplicado paralelo. No se ejecuta nada.

## AMBIGUEDADES
1. «RitualDoc/StepDoc/lifecycle» y «obligaciones, transiciones»: ninguno de estos términos está definido en el glosario ni se indica qué nodo produce su esquema. Obligaría a inventar modelo, estados, obligaciones y transiciones de paso.
2. «sobre referencias reales» y «Un procedimiento abre sus documentos y soporte»: no se nombra corpus, fixture ni resolución concreta, y WS23 no depende de WS40. Obligaría a inventar qué procedimiento real usar y qué cuenta como «soporte» abierto para poder verificar la aceptación.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: [WS13, WS09]`: no existe arista ni gate que garantice WS06. Obligaría a decidir si WS06 es prerrequisito real o solo una condición declarativa.
4. «no auto-marcar pasos como realizados por leerlos»: no se define quién o qué produce el estado «realizado» ni su contrato. Obligaría a inventar el mecanismo de marcado para poder probar la negación.

## DRY-RUN
**Lecturas:** guía de revisión, nodo WS23, bloques edge de WS13/WS09/WS30 y gates; brief, alcance, decisiones, cobertura y reconciliación.
**Cambios previstos:** archivos de renderer de procedimiento y tests bajo el `output_scope`; integración como delta en ticket existente.
**Dependencias:** WS13 (lector, foco, historia), WS09 (catálogo/contrato de renderizaciones), `G_UI_READ` vía WS11.
**Validaciones futuras:** aceptación del gate por el responsable de `graph_ui`; tests de WS23; inclusión en la validación humana WS30.

## FUTURO
WS09 debe publicar origen, contrato, renderer y acciones por vista. WS06 aporta la matriz de correspondencias. WS07 designa responsables; WS11 produce `G_UI_READ`. WS40 aporta corpus de ejemplo. WS30 realiza la validación humana. Las propuestas P01–P09 siguen pendientes de decisión humana y no se resuelven aquí.
