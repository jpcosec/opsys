REFORMULACION
Propósito: integrar en graph_ui la inspección/edición de modelos ya existentes desde el documento activo y el panel Context del lector WS13, reutilizando el editor inventariado WS04 y draft/validate/promote de sldb, sin reimplementar modelos. Resultado: UF09 (inspección y mutación) probado en store temporal real, con efectos/errores del contrato WS12 y acta humana en `runs/.../modelos/`. Repo dueño: graph_ui. Límites: no habilitar promover sin API/autoridad; G_HUMAN_READ solo habilita mutaciones UI, no desarrollo/pruebas aisladas; promoción no autorizada.

AMBIGUEDADES
1. «abre editor existente inventariado WS04»: WS04 no figura en `depends_on`/`requires` del nodo ni se concreta el artefacto de inventario que debe consumirse. Obligaría a inventar qué editor existente y qué inventario usar.
2. «no habilitar promover si API/autoridad falta»: no se define qué «autoridad» falta ni quién la emite (¿WS12, P03/P04, G_UI_WRITE?). Obligaría a inventar el criterio para habilitar promote.

DRY-RUN
Lecturas: `dag.yaml` (WS39; aristas WS12/WS13; gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT/G_HUMAN_MODEL), `task-ws39.md`, contrato WS12, lector WS13 e inventario WS04. Cambios previstos: `shell/dialogs.js`, `views/models/`, `tests/` y acta en `graph_ui:runs/.../modelos/`. Dependencias: WS12 y WS13; inventario WS04; gates citados. Validaciones futuras: UF09 en store temporal, efectos/errores WS12, acta humana P08 y paso de G_HUMAN_MODEL antes de disponibilidad en manual. Sin ejecución.

FUTURO
WS12 publica contrato/whitelist por delta; WS13 entrega lector/contexto; WS04 (o su inventario) fija el editor; WS16 resuelve G_HUMAN_READ; P01 receptor emite G_UI_WRITE por delta; WS31 publica el capítulo 15; la persona P08 valida y produce G_HUMAN_MODEL. El TaskDoc fija ruta/selector, archivos y escenarios.
