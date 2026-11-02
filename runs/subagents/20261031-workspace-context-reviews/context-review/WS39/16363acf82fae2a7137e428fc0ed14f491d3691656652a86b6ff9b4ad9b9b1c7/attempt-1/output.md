REFORMULACION

WS39 encarga en `graph_ui` integrar la inspección y edición de modelos ya existentes: desde el panel Context del lector WS13, sobre el documento activo, mostrar su Schema/clase origen y abrir el editor inventariado WS04, reutilizando `draft/validate/promote` de sldb sin reimplementar modelos. Resultado: punto de entrada navegable y mutación UF09 probada en store temporal real, con acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/`. Límites: no habilitar promover sin API/autoridad; `G_HUMAN_READ` solo habilita uso de mutaciones en UI; desarrollo/pruebas aisladas pueden avanzar con contratos técnicos. Repo dueño: `graph_ui`. Promoción no autorizada; archivos exactos, ruta/selector, pills y TaskDoc se fijan al promover.

AMBIGUEDADES

Ninguna. No considero inventable la ruta/selector exacto («ruta/selector exacto se fija en TaskDoc») ni los textos/archivos de prueba, delegados a promoción. Las dependencias que aportan contrato, lector e inventario tienen productor nombrado.

DRY-RUN

Un ejecutor futuro leería WS12 (operaciones/errores), WS13 (`node/workspace-view.js` y Context), WS48 (admisión de escritura) y el inventario WS04; localizaría el editor existente y el punto de entrada desde documento activo. Cambiaría `shell/dialogs.js`, `views/models/` y `tests/` según TaskDoc: añadiría el acceso desde Context, conectaría inspección y mutación al editor existente mediante `draft/validate/promote`, y consultaría la admisión WS48 antes de escribir. Si falta API/autoridad para promover, registraría el hueco y dejaría la operación no disponible, sin sustituto. Validaría UF09 en store temporal real: inspección, mutación y errores/efectos del contrato WS12; después recogería acta humana con participante P08 y resultado, y solo entonces `G_HUMAN_MODEL` permitiría marcar disponible el capítulo 15 del manual WS31. `G_HUMAN_READ` no bloquearía pruebas aisladas; `G_UI_WRITE`/`G_WRITE_CONTRACT` sí condicionan el delta concreto.

FUTURO

WS12 produce el contrato; WS13 el lector/Context; WS48 la admisión; WS04 el inventario del editor; WS16/`G_HUMAN_READ` y el receptor P01/`G_UI_WRITE` aportan actas; P08 fija participante; WS31 publica manual. La promoción TaskDoc fija archivos, ruta/selector y pruebas.
