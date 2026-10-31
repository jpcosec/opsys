## REFORMULACION
Propósito: integrar en `graph_ui` conocimiento y grafo local reutilizando el gráfico actual y una vista genérica única registrada en `shell/registry.js`. Resultado: navegación ida/vuelta entre fuentes y backlinks derivados, con soportes Markdown no modelados visibles y navegables con su ruta de origen. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/graph/`; Context; tests/). Límites: depende de WS13 y WS18; exige `G_UI_READ`; backlinks provienen de la API de grafo de sldb según `auditoria/infraestructura.md` de WS03; clasificación por tipo/tags; vecindad 1–2 hops; conserva Code local del ticket workspace; no exige un renderer nuevo por clase; promoción no autorizada.

## AMBIGUEDADES
1. «crossroads (CrossroadDoc del árbol de dominio)»: “CrossroadDoc” y “árbol de dominio” no se definen en brief/glosario ni en alcance. Obligaría a inventar qué entidad es, de dónde se obtiene y cómo se representa.
2. «materializaciones»: se enumera como clase a mostrar, pero no hay definición ni contrato de origen en las fuentes. Obligaría a inventar su identificación y procedencia.
3. «Clasificación = tipo y tags»: no se define de dónde salen los tags ni su autoridad. Obligaría a decidir si son campos del modelo, del documento o inventados.
4. «Vecindad = 1–2 hops»: el rango no fija si se muestran uno, dos o ambos, ni si es configurable. Obligaría a inventar el comportamiento y el criterio comprobable.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación y bloque WS24 con gates. Cambios previstos, sin ejecutar: vista genérica en `graph/`, Context y tests; registro en `shell/registry.js`; consumo de API de backlinks y proyección Code. Dependencias: WS13 agregado, WS18, `G_UI_READ` pendiente; WS03 aporta auditoría por vía transitiva; WS11 produce acta. Validaciones futuras: ida/vuelta fuentes/backlinks, Markdown no modelado visible con ruta, ausencia de renderer obligatorio por clase; después WS29/WS30/WS42.

## FUTURO
`G_UI_READ` lo resuelve WS11 con responsable humano designado. WS18 produce proyecciones. La promoción queda a TaskDoc/preflight y no autoriza ejecución. WS29, WS30 y WS42 consumen WS24; WS17/WS40 aportan corpus e índices. WS04 reconcilia Board.
