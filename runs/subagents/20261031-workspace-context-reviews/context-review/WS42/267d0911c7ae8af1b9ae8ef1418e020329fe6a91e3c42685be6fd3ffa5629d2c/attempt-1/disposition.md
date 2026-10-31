# Executor comparison — WS42, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION
- **Propósito:** integrar en `graph_ui` las operaciones reales de conocimiento —split/merge de átomos y tipado de protoátomos— con confirmación humana que muestre origen y efecto, e inspeccionar/validar materializaciones contra `MaterializationContractDoc` mediante API SLDB, sin generar destinos.
- **Resultado:** vista/espacio `knowledge/` que invoca contratos WS12, marca materializaciones inválidas como no operables y declara no disponibles las capabilities no soportadas, con tests.
- **Repo dueño:** `graph_ui`.
- **Límites:** endpoints solo de la whitelist WS12; sin renderer propio de materializaciones; no simular capacidades; mutaciones UI sujetas a `G_HUMAN_READ`; `G_UI_WRITE`/`G_WRITE_CONTRACT` se evalúan por delta.

## Hallazgos/disposición contra intención

1 pruebas usan store temporal real generado por CLI/modelos públicos (regla común), con materialización de entrada registrada válida/inválida según escenario TaskDoc; crear input de prueba no es generar/publicar destinos arbitrarios de materialización. No fake API ni destino de producto inventado. 2 versión/commit de artefactos/modelo/tools/store utilizados se registra por Executor en evidencia del run de la TaskDoc, como todo escenario verificable. 3 WS40 es alternativa, no dependencia obligatoria porque scope permite propio store temporal real; si se elige corpus futuro se espera su manifiesto, no se sustituye dato por mock. Dry-run/aceptación mantienen invalidas no operables y API SLDB real.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
