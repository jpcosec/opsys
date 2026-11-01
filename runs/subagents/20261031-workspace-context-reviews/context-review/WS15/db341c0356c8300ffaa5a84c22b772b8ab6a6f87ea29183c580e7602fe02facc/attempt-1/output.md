## REFORMULACION

WS15 es un **agregado no ejecutable** del plan: agrupa «errores de lectura y modo degradado» (WS15.1) y «orientación sin desk» (WS15.2). Su propósito es que los dependientes sigan apuntando a un único ID mientras la entrega real se reparte entre sus hijos. No produce artefacto propio: su `output_scope` son las salidas de WS15.1 y WS15.2, y su aceptación es la suma de ambas. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: no duplica implementación, reutiliza la base `a1b2b22/f16fcd1/134a665`, exige `G_UI_READ` por delta y su promoción está `not_authorized` hasta preflight específico.

## AMBIGUEDADES

Ninguna. El nodo no define resultado propio que ejecutar; remite explícitamente a sus hijos y el criterio de cierre del agregado está fijado. No reviso los bloques de WS15.1/WS15.2 por ser contratos de vecinos.

## DRY-RUN

Un ejecutor futuro del agregado no escribiría archivos: solo comprobaría el cierre de sus hijos.

- **WS15.1**: implementaría en `frontends/mindmap/views/workspace/errors/` y `tests/`, consumiendo la lectura Markdown de WS13 y el contrato de errores/red de WS11. Aporta al agregado: panel de error sin borrar historial, distinción backend caído/CDN y reintento que conserva pestañas/foco.
- **WS15.2**: implementaría en `frontends/mindmap/views/workspace/orientation/` y `tests/`, consumiendo WS11. Aporta: orientación sin mutar, ruta absoluta y comando `deskops init`, más refresco tras init externo.

Dependencias: WS13 como base y un recibo `G_UI_READ` por delta (evaluation `per_delta`). Si falta WS11, WS13 o el recibo, el ejecutor se detiene y registra el hueco con repo dueño, sin crear sustituto. Validación conjunta: ambas aceptaciones hijas satisfechas; no comparten directorio de salida, por lo que no hay solapamiento entre ellas. WS15 cierra cuando cierran ambas.

## FUTURO

El receptor P01 emite las actas por delta en `graph_ui`; WS16 ejecuta la validación humana (UF07/UF10) sobre el corpus WS40; WS06 reconcilia al promover. La autorización de promoción no la decide este nodo.
