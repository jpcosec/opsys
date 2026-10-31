## REFORMULACION
WS24 es un nodo de implementación en `graph_ui` que debe integrar conocimiento y grafo local reutilizando el gráfico existente y una vista única de documento genérica registrada en `shell/registry.js`, con átomos/protoátomos/crossroads, materializaciones, pills, clasificación, vecindad de hasta 2 hops y backlinks derivados de la API de grafo de sldb. Resultado esperado: navegación ida/vuelta por fuentes y backlinks, soporte Markdown sin modelo visible con ruta de origen, clasificación y vecindad, preservando Code local del workspace `a1b2b22`. Límites: depende de WS13 y WS09; requiere G_UI_READ por delta; ViewDoc WS18 es opcional y no bloquea; no exige un renderer nuevo por clase; promoción no autorizada.

## AMBIGUEDADES
1. «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare». No se define quién produce ni dónde se leen los tags del documento; obligaría a inventar su fuente y contrato de lectura.
2. «un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista de documento genérica con su ruta de origen». El `scope` solo enumera átomos/protoátomos/crossroads/materializaciones/pills, clasificación y vecindad, mientras que explorar Markdown no modelado corresponde a WS13.2; obligaría a decidir si WS24 lo implementa o lo hereda, con riesgo de duplicar la dependencia.
3. «output_scope: frontends/mindmap/views/workspace/graph/; Context; tests/». «Context» no tiene ruta ni artefacto definido; obligaría a inventar dónde materializar esa salida.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS24 en `dag.yaml`; contratos vecinos solo como referencia. Cambios previstos: vista de grafo y vista genérica de documento, registro en `shell/registry.js`, contexto, pruebas. Dependencias: WS13 (incluye WS13.1–13.3), WS09, inventario WS02, auditoría WS03, contrato WS11 y recibo G_UI_READ propio del delta. Validaciones futuras: backlinks entrantes/salientes, fuente/ruta de Markdown sin modelo, tipo/tags, vecindad 2 hops, preservación de Code y ausencia de renderer obligatorio por clase; validación humana en WS30.

## FUTURO
WS11 emite el acta G_UI_READ por delta; WS09 entrega el catálogo; WS03 la auditoría de infraestructura; WS02 el inventario. WS18/G_SPEC_VIEW queda opcional. La promoción y el TaskDoc los decide otro nodo o un humano; WS30 aporta el registro manual.
