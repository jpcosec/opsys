## REFORMULACION
Propósito: integrar en el lector existente la inspección y edición de modelos ya disponibles, sin reimplementarlos. Resultado: entrada desde documento/contexto que muestra Schema/clase origen y abre el editor inventariado, más mutación UF09 probada. Repo dueño: `graph_ui`. Límites: usar `draft/validate/promote` de sldb; no habilitar promover sin API/autoridad; `G_HUMAN_READ` solo habilita mutaciones en UI, no desarrollo/pruebas aisladas; ruta/selector exactos quedan para TaskDoc; acta humana en `runs/subagents/workspace-documental-acceptance/modelos/acta.md`.

## AMBIGUEDADES
1. «acceso desde documento activo muestra Schema/clase origen de ese documento y abre editor existente inventariado WS04». No define qué ocurre cuando el documento activo no tiene Schema/clase/modelo asociado: si la entrada se oculta, se deshabilita o muestra un aviso. El ejecutor tendría que inventar ese resultado visible y su criterio de aceptación.

## DRY-RUN
Lecturas: nodo WS39, guía, brief, alcance, decisiones, cobertura, contratos vecinos WS12/WS13 y gates. Cambios previstos: implementación en `graph_ui` (`shell/dialogs.js`, `views/models/`, `tests/`) y acta de aceptación en `runs/subagents/workspace-documental-acceptance/modelos/`. Dependencias: contrato WS12 por delta, lector WS13, inventario WS04 (transitivo), API sldb `draft/validate/promote`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras: UF09 sobre store temporal real; comprobar efectos/errores del contrato WS12; probar punto de entrada; acta humana con participante P08; `G_HUMAN_MODEL` antes de publicar el capítulo 15 en el manual WS31. Sin ejecución.

## FUTURO
WS12 debe producir el contrato técnico por delta y sus recibos; WS13, el lector requerido; WS04, el inventario del editor existente; WS16, `G_HUMAN_READ`; el receptor P01 en `graph_ui`, el acta `G_UI_WRITE` del delta; la persona designada por P08, el acta de `G_HUMAN_MODEL`; WS31 publica el capítulo tras pasar ese gate.
