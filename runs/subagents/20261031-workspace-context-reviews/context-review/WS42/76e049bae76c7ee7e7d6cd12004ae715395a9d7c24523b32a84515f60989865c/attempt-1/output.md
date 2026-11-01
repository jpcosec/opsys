REFORMULACION
Encargo: integrar en graph_ui las operaciones de conocimiento existentes —split/merge de átomos y proto typing— y la inspección/validación de materializaciones, con confirmación humana que muestre origen y efecto. Resultado: acciones y vista en `frontends/mindmap/views/workspace/knowledge/` que invocan solo endpoints de la whitelist WS12, más `tests/`; las materializaciones se validan por API pública SLDB contra `MaterializationContractDoc`, sin renderer propio ni destinos nuevos. Repo: `graph_ui`. Límites: si falta contrato/API/operación, WS12 registra hueco y la UI no está disponible; gates `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; aceptación cubierta por WS30.

AMBIGUEDADES
ninguna

DRY-RUN
Un ejecutor futuro leería WS12 (whitelist/contrato), WS19 (conflicto/precondición), WS24 (vista genérica/grafo/backlinks), inventarios WS02/WS03, `MaterializationContractDoc` y TaskDoc/WS40. Cambiaría `frontends/mindmap/views/workspace/knowledge/`: acciones split/merge/proto typing, diálogo de confirmación con origen/efecto, inspector/validador de materializaciones, etiquetas de disponibilidad; `tests/` con store temporal real. Consumiría gates: `G_HUMAN_READ` antes de habilitar mutaciones UI; `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta WS42, con desarrollo/pruebas API aisladas antes. Errores: operación/API no whitelist o ausente -> no disponible y hueco registrado, sin sustituto; conflicto de escritura -> mostrarlo y no persistir; materialización inválida -> mostrarla inválida y no operable; fallo SLDB -> límite declarado. Validación: persistencia/referencias/conflicto, materializaciones contra el modelo registrado, sin crear destinos, escenarios UF03; WS30 recoge acta humana.

FUTURO
WS12 produce/verifica whitelist y contrato y registra huecos; WS16 produce `G_HUMAN_READ`; P01 receptor en graph_ui produce acta `G_UI_WRITE` por delta; el TaskDoc de promoción fija archivos, pills, átomos y preflight; WS40/Taller aporta corpus/manifiesto; WS30 y el humano deciden aceptación y bloqueo por fallo.
