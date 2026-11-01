## REFORMULACION

WS39 es un nodo de implementación en `graph_ui` cuyo propósito es integrar la inspección y edición de modelos ya existentes —Schema y edición de clases— en el lector del workspace, usando `draft/validate/promote` de sldb y sin reimplementar modelos. El resultado esperado es un punto de entrada desde el panel Context del lector WS13: al abrir un documento activo debe mostrar su Schema/clase de origen y abrir el editor ya inventariado por WS04. Incluye probar ese acceso además de la mutación UF09 en un store temporal real, comprobar efectos y errores del contrato WS12 y dejar acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`. Límites: no habilitar `promote` si falta API o autoridad; G_HUMAN_READ solo habilita mutaciones en UI, no desarrollo/pruebas aisladas de API; la ruta/selector exacto queda para TaskDoc.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro leería el contrato WS12 (`contratos/operaciones.md`), el lector/contexto de WS13 (`node/workspace-view.js`), el inventario WS04 del editor existente y la aceptación de WS39. Modificaría `shell/dialogs.js` y `views/models/`, añadiría pruebas en `tests/` y escribiría el acta en la ruta indicada. Consumiría WS12 como contrato de efectos/errores y recibo por delta, WS13 como lector requerido, y los gates G_HUMAN_READ —solo para uso de mutaciones en UI—, G_WRITE_CONTRACT y G_UI_WRITE por delta de WS39. Validaría con store temporal real: inspección y mutación UF09, efectos/errores declarados, acceso desde documento activo y acta humana. Si falta contrato, API o autoridad, se detendría, registraría el hueco con repo dueño y mantendría `promote` deshabilitado; no crearía sustituto. Produciría la evidencia de G_HUMAN_MODEL.

## FUTURO

El participante humano fijado por P08 firma el acta y determina el resultado de G_HUMAN_MODEL. WS12 aporta contrato y recibo técnico del delta. WS31 publica el capítulo 15 del manual solo después de que G_HUMAN_MODEL pase; WS39 no publica ese manual.
