## REFORMULACION
**Propósito:** cerrar el contrato de navegación e identidad del workspace documental.  
**Resultado:** `contratos/navegacion.md` en deskops, con identidad/origen/foco/enlaces, lectura multidesk read-only, clasificación de huecos y mapa de deltas que requieren recibo.  
**Repo dueño:** deskops.  
**Límites:** nodo de planificación; no implementa, no escribe actas interrepo y no afirma recepciones. Puede cerrar sin acta receptora, sin Changes/Scion y sin ViewDoc; G_SPEC_VIEW solo se obtiene al preparar WS18.

## AMBIGUEDADES
1. «WS11 cierra con contrato básico revisado» — no indica quién revisa ni qué evidencia de revisión se exige. Obliga a inventar si basta autochequeo del Executor o si hace falta aceptación humana adicional, y cómo registrarla.
2. «cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes de code» — no define qué hacer si las auditorías no identifican productor. Obliga a inventar un dueño o a decidir por cuenta propia si el hueco queda sin productor, pese a la instrucción de no crear modelos hipotéticos.

## DRY-RUN
**Lecturas previstas:** brief, alcance, decisiones, cobertura, dag.yaml (WS11 y dependencias WS09/WS08), auditorías WS02–04 por dependencia transitiva.  
**Cambios previstos:** redactar `contratos/navegacion.md`; clasificar huecos; mapear deltas G_UI_READ con actor P01, IDs y efectos; enlazar actas externas solo si ya existen.  
**Dependencias:** WS09 aporta catálogo de vistas; WS08, user-flows; WS02–04, APIs/evidencia; G_PRODUCT está satisfecho.  
**Validaciones futuras:** comprobar citas path/símbolo/commit, ausencia de actores/API inventados, clasificación completa, ningún recibo declarado y revisión del contrato. G_UI_READ sigue pendiente por delta; G_SPEC_VIEW no bloquea WS11.

## FUTURO
El receptor P01 produce las actas G_UI_READ por delta en graph_ui; WS12 consume el contrato; WS13.x, WS17, WS40 y WS41 lo usan; WS18 obtiene G_SPEC_VIEW por separado. La promoción requiere TaskDoc y preflight, fuera de este nodo.
