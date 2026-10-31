## REFORMULACION
- **Propósito:** WS13 es un nodo agregado que integra el lector del workspace sobre el ticket draft de `graph_ui`: documento/fuente solo lectura, contexto, enlaces, Code local, explorador de documentos modelados/no modelados, dos documentos lado a lado, pestañas/historia y foco por documento/nodo.
- **Resultado:** agregado no ejecutable; se satisface cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación. Sus dependientes siguen dependiendo de WS13.
- **Repo:** `graph_ui`, con el contrato de navegación e identidad de WS11.
- **Límites:** sin índices nuevos, sin otro workspace independiente, sin mutaciones; reutiliza `shell/registry.js`; `G_UI_READ` pendiente; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

Las dependencias y el gate pendiente están nombrados con actor/productor (WS11, WS07) y la regla de falta de contrato está cubierta por `alcance.md`. Los detalles de archivos, TaskDoc y pills se delegan a la promoción.

## DRY-RUN
- **Lecturas:** nodo WS13, bloque de gates y aristas vecinas como contratos; guía, brief, alcance, decisiones, cobertura y reconciliación.
- **Cambios previstos:** ninguno; no se ejecuta ni se modifica el plan.
- **Dependencias:** WS11 (contrato y acta `G_UI_READ`), WS13.1–WS13.3, gate `G_UI_READ` con resolver WS11; WS07 designa al responsable de `graph_ui`; matriz WS06 y contrato WS09 llegan de forma transitiva.
- **Validaciones futuras:** cierre del agregado al cumplir los hijos; evidencia de `G_UI_READ` con responsable identificado; no despacho de UI hasta el gate; el TaskDoc de promoción fijará archivos, escenarios y textos.

## FUTURO
- WS11 produce el contrato de navegación e identidad y el acta de aceptación del delta lector; WS13.1–WS13.3 implementan; WS07 designa responsables; el humano resuelve P01/P07/P08; WS16 valida sobre el corpus; la promoción la autoriza otro nodo o una persona.
