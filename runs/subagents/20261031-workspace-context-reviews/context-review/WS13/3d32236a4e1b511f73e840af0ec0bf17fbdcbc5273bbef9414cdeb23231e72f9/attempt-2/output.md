## REFORMULACION
WS13 es un **agregado no ejecutable** de graph_ui: integra el lector workspace sobre la base a1b2b22 con documento/fuente de solo lectura, contexto, enlaces, foco, tabs/historia, explorador de documentos modelados y no modelados, y dos documentos lado a lado. Su resultado no es código propio: se cumple cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación. Límites: no requiere índices nuevos, no crea otro workspace independiente y no duplica la implementación existente. Depende de WS11 y requiere G_UI_READ por delta.

## AMBIGUEDADES
1. «organización de contenido procede de documentos/consultas»: ningún hijo ni contrato define qué es una «consulta» ni qué fuente la produce; obligaría a inventar un mecanismo de organización no asignado.  
2. «Se reutiliza el registro de vistas existente en shell/registry.js»: no se concreta qué vistas ni cómo se reutilizan, y ningún hijo lo exige en su aceptación; obligaría a inventar el punto de integración.

## DRY-RUN
Un ejecutor futuro no ejecutaría WS13: leería `dag.yaml`, los ámbitos/aceptaciones de WS13.1–WS13.3, el contrato WS11 y los recibos G_UI_READ por delta. No haría cambios en el agregado ni promovería `task_file` (`promotion: not_authorized`). Orden: WS13.1 primero; WS13.2 y WS13.3 después, pues ambos dependen de WS13.1. WS13.1 transfiere lector, contexto, enlaces y foco; WS13.2 añade explorador y refresco de catálogo sobre ese lector; WS13.3 añade tabs, divisiones e historia conservando el foco por documento. Validación conjunta: abrir documento modelado y no modelado, refrescar altas, alternar tabs/divisiones y volver conservando foco/historia, sin workspace duplicado. Si falta WS11 o el recibo de un hijo, se detiene y registra el hueco; no crea sustituto. El cierre no se infiere de commits.

## FUTURO
WS11 produce el contrato de navegación; WS09 aporta el catálogo de representaciones; P01/receptor emite cada G_UI_READ. WS14, WS22, WS23, WS24, WS27 y WS41 consumen WS13. La promoción y el TaskDoc quedan para decisión humana.
