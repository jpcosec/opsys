## REFORMULACION

- **Propósito:** verificar si WS13.1 está bien planteado como encargo de planificación.
- **Resultado:** lector de documento/fuente solo lectura con panel de contexto, enlaces y Code local, manteniendo foco por documento/nodo sobre el workspace integrado a1b2b22.
- **Repo dueño:** `graph_ui`; depende de WS11 y requiere G_UI_READ.
- **Límites:** no implementar la UI, no crear otro workspace, no exigir índices nuevos, no inventar mapeo texto→código, no ejecutar. Promoción no autorizada.

## AMBIGUEDADES

1. **“según acta WS11”** (scope). WS11 declara en su aceptación: “puede cerrar sin acta receptora” y su salida es “contratos/navegacion.md; enlaces a recibos externos G_UI_READ”. El ejecutor tendría que inventar qué es el “acta WS11”: ¿el contrato de navegación, un recibo G_UI_READ por delta o un artefacto distinto? La frase contradice la fuente suministrada.

2. **“Markdown sin modelo legible”** (acceptance), junto a “Documento/fuente solo lectura” (scope). No queda definido si “legible” exige Markdown renderizado, fuente cruda íntegra o ambas; el brief distingue “renderizado/fuente” como cosas diferentes. Obliga a inventar el resultado visible para Markdown no modelado.

## DRY-RUN

- **Lecturas previstas:** dag.yaml (WS11, WS13.1, gate G_UI_READ), guía, brief, alcance, decisiones, cobertura, reconciliación e instrucción.
- **Cambios previstos:** implementación o delta conciliado en `graph_ui/frontends/mindmap/views/workspace/` y `tests/`, reutilizando componentes existentes; sin ejecutar.
- **Dependencias:** WS11 y su contrato de navegación; WS09/WS08 de forma transitiva; G_UI_READ por delta; base a1b2b22.
- **Validaciones futuras:** aceptación de WS13.1, recibo G_UI_READ del delta, pruebas con store temporal o corpus WS40, y TaskDoc de promoción con archivos/evidencia.

## FUTURO

WS11 debe producir el contrato de navegación y WS09 sus borradores de vistas; P01/receptor de `graph_ui` debe emitir el recibo G_UI_READ de este delta. WS13.2/WS13.3 completan el agregado. La promoción exige TaskDoc y preflight; la aceptación humana no se sustituye por commits previos.
