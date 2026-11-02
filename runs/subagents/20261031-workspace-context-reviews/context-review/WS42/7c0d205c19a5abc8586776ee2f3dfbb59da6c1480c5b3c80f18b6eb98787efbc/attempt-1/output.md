## REFORMULACION
WS42 es un encargo de implementación en `graph_ui` para integrar en la vista de conocimiento las operaciones existentes de átomos —split/merge y proto typing— y la inspección/validación de materializaciones, usando los contratos reales que concrete WS12 y la admisión de escritura de WS48. Resultado: UI que muestra origen y efecto, pide confirmación, persiste vía API whitelisteada, valida materializaciones contra `MaterializationContractDoc` y declara no disponible lo no soportado, con tests. Límites: no crear destinos, no renderer propio, no simular; gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT; aceptación humana por WS30; promoción no autorizada.

## AMBIGUEDADES
1. «versión/commit registrados»: no dice de qué —modelo, store o materialización— ni dónde se registran; obligaría a inventar el objeto y el soporte del registro verificable.
2. «depends_on: - WS19»: el scope no menciona qué consume WS42 de WS19; si no aporta contrato o API usada por split/merge/typing, es una dependencia sobrante y el ejecutor tendría que decidir si esperarla o ignorarla.

## DRY-RUN
Lecturas: contrato WS12 y whitelist, inventario WS02/APIs WS03, código de WS24, módulo de admisión WS48, modelo `MaterializationContractDoc`, corpus/manifiesto WS40 y salidas de WS19 si se consumen. Cambios previstos: módulo en `views/workspace/knowledge/`, llamadas a canales WS12 para split/merge/proto typing, diálogo de confirmación origen/efecto, validación de materializaciones por API SLDB, etiquetas de disponibilidad y tests. Dependencias y gates: comprobar WS12/WS19/WS24/WS48 y recibos G_WRITE_CONTRACT/G_UI_WRITE; G_HUMAN_READ solo para habilitar uso. Errores: si falta contrato/API, detenerse, registrar hueco y marcar no disponible; materialización inválida se muestra inválida. Validación esperada: tests con store temporal real, persistencia/referencias/conflictos, sin destinos nuevos ni simulación; después WS30.

## FUTURO
WS12 produce contrato/whitelist y recibo G_WRITE_CONTRACT; WS48 produce la admisión; WS19/WS24 entregan sus vistas; WS02/WS03 inventario y APIs; WS30 ejecuta la validación humana; P01 receptor emite acta G_UI_WRITE por delta; WS16 produce G_HUMAN_READ. La promoción queda a autorización humana.
