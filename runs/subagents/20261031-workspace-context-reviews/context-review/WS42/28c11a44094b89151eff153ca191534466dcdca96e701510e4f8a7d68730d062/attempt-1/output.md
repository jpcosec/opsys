## REFORMULACION
WS42 es un nodo de implementación en `graph_ui` que integra en el workspace las operaciones de conocimiento ya contratadas: split/merge de átomos y proto typing, con confirmación humana en UI mostrando origen y efecto antes de ejecutar. También inspecciona y valida materializaciones existentes contra `MaterializationContractDoc` mediante API pública SLDB, sin crear destinos. Límites: solo endpoints de la whitelist WS12, sin renderer propio de validación, con capacidades no soportadas declaradas no disponibles. Depende de WS19, WS24 y WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Aceptación comprobable por UF03 con persistencia, referencias y conflictos reales, y por WS30.

## AMBIGUEDADES
Ninguna. Las ausencias de API/contrato tienen productor nombrado (WS12/WS03) y regla de parada; los detalles de archivos, textos y store quedan para TaskDoc; los gates pendientes son intencionales y per-delta.

## DRY-RUN
Un ejecutor futuro leería `task-ws42.md`, el contrato WS12, las salidas de WS19/WS24, `deskops/models/materialization.py` y el código actual de `frontends/mindmap/views/workspace/`. Crearía el módulo `knowledge/`, la confirmación UI con origen/efecto, llamadas a split/merge/proto typing según whitelist, inspección de materializaciones y pruebas en `tests/`. Consumiría la API SLDB y el modelo registrado en el store temporal fijado por TaskDoc o manifiesto WS40. Antes de habilitar mutaciones UI comprobaría G_HUMAN_READ; para cada operación, G_WRITE_CONTRACT y el recibo per-delta G_UI_WRITE. Si falta contrato/API, se detendría, registraría hueco y declararía la capability no disponible, bloqueando solo su escenario UF03. Una materialización inválida se mostraría como inválida y no operable; conflictos reales se mostrarían. Validaría con tests sobre store temporal real/corpus WS40 y después mediante WS30.

## FUTURO
WS12 produce/verifica contratos y huecos; WS16 emite el acta de G_HUMAN_READ; el receptor P01 acepta el delta concreto de G_UI_WRITE; WS19/WS24 entregan edición y vista de conocimiento; WS30 ejecuta la validación humana y puede abrir incidencias en el nodo causante.
