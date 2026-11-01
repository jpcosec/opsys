REFORMULACION
Propósito: integrar en graph_ui la inspección y edición de modelos ya existentes desde el panel Context del lector WS13, reutilizando Schema/editor y `draft/validate/promote` de sldb, sin reimplementar modelos. Resultado: punto de entrada desde documento activo y mutación UF09 probada en store temporal, con acta humana en `runs/subagents/workspace-documental-acceptance/modelos/acta.md`. Repo dueño: graph_ui. Límites: `output_scope` acotado a `shell/dialogs.js`, `views/models/`, `tests/` y el acta; no promover sin API/autoridad; ruta/selector exacto queda para TaskDoc; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; G_HUMAN_READ no bloquea pruebas aisladas de API.

AMBIGUEDADES
Ninguna. El nodo nombra propósito, repo, dependencias, gates, aceptación y límites; las remisiones a WS12, WS13, WS04, P08 y TaskDoc tienen productor o regla de faltante.

DRY-RUN
Lecturas previstas: input, guía, brief, alcance, decisiones, cobertura, nodo WS39, bloques WS12/WS13 y gates. Cambios previstos: UI en graph_ui para acceso desde Context al editor existente, pruebas y acta de aceptación. Dependencias: contrato WS12, lector/contexto WS13, inventario WS04, participante P08, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Validaciones futuras: UF09 con inspección y mutación en store temporal real; efectos/errores declarados por WS12; acta humana; G_HUMAN_MODEL antes de marcar disponible el capítulo 15 del manual de WS31. Sin ejecución.

FUTURO
WS12 publicará contrato/whitelist; WS13 entregará lector y Context; WS04 aportará inventario del editor; WS16 resolverá G_HUMAN_READ; el receptor P01 aceptará G_UI_WRITE por delta; WS31 publicará el manual; la persona P08 ejecutará la prueba y dejará el acta.
