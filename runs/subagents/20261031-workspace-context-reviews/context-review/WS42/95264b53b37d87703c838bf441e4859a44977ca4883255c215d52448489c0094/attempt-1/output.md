## REFORMULACION

**Propósito.** Integrar en `graph_ui` las operaciones de conocimiento ya existentes —split/merge de átomos y tipado de protoátomos— invocando contratos reales de Deskops/SLDB concretados por WS12, con confirmación en UI que muestra origen y efecto antes de ejecutar. Además, inspeccionar y validar materializaciones existentes contra `MaterializationContractDoc` mediante API pública SLDB, sin crear destinos.

**Resultado.** Módulo en `frontends/mindmap/views/workspace/knowledge/`, endpoints limitados a la whitelist WS12 y tests. Cada capability no soportada se declara no disponible; no se simula. Aceptación cubierta por WS30.

**Repo.** `graph_ui`.

**Límites.** Depende de WS19 (agregado), WS24 y WS12. Gates: G_HUMAN_READ habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas; G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta. Si WS12 no concreta una operación o validación, se registra hueco/productor y la UI no la ofrece.

## AMBIGUEDADES

Ninguna. El nodo nombra productores y fallback para contratos ausentes; la confirmación, textos y archivos exactos quedan delegados al TaskDoc de promoción; los gates pendientes son intencionales.

## DRY-RUN

**Lecturas previstas:** WS42 y TaskDoc; contrato WS12 por operación; WS24 (registro/vista de documento); hijos de WS19; inventarios WS02/WS03 y `MaterializationContractDoc`; manifiesto/corpus WS40 si el TaskDoc lo elige; tests existentes.

**Cambios previstos:** en `knowledge/`, invocación de `DeskopsOperations`/CLI/API SLDB vía el adapter WS12; diálogo de confirmación con origen y efecto; persistencia real de split/merge/typing; inspector de materializaciones que llama validación pública SLDB; tests con store temporal real y fixtures válida/inválida; sin renderer propio ni destinos arbitrarios.

**Dependencias consumidas:** whitelist WS12 por operación/campo/canal; registro y vista WS24; APIs SLDB. Si falta una operación, se registra hueco y se marca no disponible; no se sustituye.

**Gates:** G_HUMAN_READ solo condiciona habilitar uso en UI; G_UI_WRITE/G_WRITE_CONTRACT requieren recibo del delta concreto. Su ausencia bloquea la habilitación de ese delta, no las pruebas aisladas de API.

**Errores esperados:** conflicto real (409) visible; capability ausente declarada no disponible; materialización inválida mostrada como inválida y no operable.

**Validación futura:** pruebas unitarias/integración contra store temporal; ejecución humana UF03 en WS30; evidencia de versión/commit y resultados en el store/acta correspondiente.
