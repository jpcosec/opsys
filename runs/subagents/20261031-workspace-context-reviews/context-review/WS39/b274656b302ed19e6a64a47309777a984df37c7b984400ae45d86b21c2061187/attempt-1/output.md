## REFORMULACION

**Propósito:** integrar en graph_ui la inspección/edición de modelos ya existentes (Schema/editar clases) desde el panel Context del lector WS13, usando `draft/validate/promote` de sldb sin reimplementar modelos.

**Resultado:** punto de entrada desde documento activo que muestra Schema/clase origen y abre el editor inventariado WS04; prueba UF09 de inspección/mutación en store temporal real; acta en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`.

**Repo dueño:** graph_ui. Salidas: `shell/dialogs.js`, `views/models/`, `tests/` y el acta.

**Límites:** no reimplementar modelos; no habilitar promover sin API/autoridad; G_HUMAN_READ solo habilita mutaciones en UI; ruta/selector exacto y archivos quedan para TaskDoc; depende de WS12 y WS13.

## AMBIGUEDADES

1. «acceso desde documento activo muestra Schema/clase origen de ese documento»: no define qué debe mostrar el punto de entrada cuando el documento activo no tiene Schema/clase origen (estado vacío, ocultar acceso, error u otra conducta). Obligaría al ejecutor a inventar el resultado y el criterio observable para documentos no modelados.

## DRY-RUN

**Lecturas:** nodo WS39, guía, brief, alcance, decisiones y cobertura; contratos de vecinos WS12/WS13 como prerrequisitos; inventario WS04 y API sldb `draft/validate/promote`; panel Context de WS13 (`node/workspace-view.js`).

**Cambios previstos:** solo `shell/dialogs.js`, `views/models/`, `tests/` y acta; no tocar sldb ni modelos.

**Dependencias:** WS12 (contrato por delta, G_WRITE_CONTRACT), WS13 (lector/Context); gates G_HUMAN_READ (WS16), G_UI_WRITE (recepción P01 por delta) y G_WRITE_CONTRACT; G_HUMAN_MODEL lo produce WS39.

**Validaciones futuras:** UF09 en store temporal real; efectos/errores declarados por WS12; acta humana con participante P08; bloqueo de promote sin API/autoridad; G_HUMAN_MODEL antes del manual de WS31.

## FUTURO

WS04 debe entregar el inventario del editor; WS12, el contrato por operación; WS13, lector y Context; WS16, acta de G_HUMAN_READ; el receptor P01, acta de G_UI_WRITE por delta; WS31 publica el capítulo 15. El TaskDoc fija ruta/selector, archivos y escenarios.
