## REFORMULACION

Propósito: encargo de planificación para integrar fuente y renderizado en el workspace según `source_mode`, reutilizando guardado autorizado. Resultado: alternancia fuente/render con mismo origen, revisión y buffer sucio; composición escribe solo en el documento dueño si WS12 lo soporta. Repo dueño: `graph_ui`, con salidas en `frontends/mindmap/views/workspace/; tests/`. Límites: no se ejecuta ni promociona; P04 fija `editable`, lo que añade WS20 y G_SOURCE; no se prepara con `pending`; no se inventa API ni se excede el `output_scope`.

## AMBIGUEDADES

1. «Alternar fuente/render con mismo origen, revisión y dirty buffer» / «Al alternar con cambios sin guardar se conserva el buffer». No se define si el render muestra el contenido persistido o el buffer sin guardar. Obligaría al ejecutor a inventar el comportamiento visible de la alternancia y qué contenido considera «mismo origen» cuando hay ediciones sucias.

## DRY-RUN

Lecturas previstas: guía, brief, alcance, decisiones, dag.yaml (WS21, parámetro `source_mode`, gates) y contratos vecinos WS19/WS20 solo como dependencias. Cambios previstos: componentes de alternancia fuente/render y pruebas en `frontends/mindmap/views/workspace/; tests/`, sin archivos concretos hasta TaskDoc. Dependencias: WS19 por agregado; variante editable añade WS20; WS12 llega transitivamente; gates G_UI_WRITE y G_WRITE_CONTRACT por delta, más G_SOURCE en editable; G_HUMAN_READ llega vía WS19. Validaciones futuras: pruebas de roundtrip/conflicto y campos protegidos, recibos per_delta, y validación manual WS30.

## FUTURO

WS12 debe producir el contrato técnico por operación, incluida composición si existe. WS20 debe producir G_SOURCE con API reversible y pruebas. El receptor P01 en `graph_ui` emite el acta de G_UI_WRITE al preparar/promover este delta. La promoción fijará archivos, escenarios y textos exactos en TaskDoc. WS30 decide el resultado manual; ninguna de estas piezas se ejecuta aquí.
