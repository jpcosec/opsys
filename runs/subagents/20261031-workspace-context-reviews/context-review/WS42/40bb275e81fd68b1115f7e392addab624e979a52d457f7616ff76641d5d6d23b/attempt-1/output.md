**REFORMULACION**
WS42 encarga, en `graph_ui`, integrar en la UI de conocimiento las operaciones existentes de atoms split/merge y proto typing, más la inspección/validación de materializaciones, invocando contratos reales y con confirmación humana que muestre origen y efecto. Resultado: operaciones ejecutables con persistencia, referencias y conflictos, y materializaciones validadas sin crear destinos; lo no soportado se declara no disponible. Repo dueño: `graph_ui`. Límites: endpoints solo de la whitelist WS12, sin renderer propio de validación, sin simular ni crear destinos arbitrarios.

**AMBIGUEDADES**
Ninguna.

**DRY-RUN**
WS42 es un nodo `delivery`, no un agregado. Un ejecutor leería el contrato WS12 (`contratos/operaciones.md`), inventarios WS02/WS03, salidas de WS19.1/WS19.2 y WS24, `MaterializationContractDoc` y el store temporal/manifiesto WS40. Comprobaría gates: acta G_HUMAN_READ de WS16 antes de habilitar mutaciones en UI —desarrollo y pruebas aisladas pueden avanzar—; WS42 en `accepted_scope_nodes` de G_WRITE_CONTRACT; y acta per_delta G_UI_WRITE de P01 para WS42. Cambios previstos: en `frontends/mindmap/views/workspace/knowledge/`, conectar split/merge/proto typing al adapter y al diálogo de confirmación; en `tests/`, probar persistencia, referencias, conflictos, validación/invalidez de materializaciones y ausencia de simulación. Errores: contrato, API o dato faltante → detenerse, registrar hueco y dueño, marcar capability no disponible; materialización inválida → mostrarla inválida y no ofrecerla. Validación esperada: aceptación de WS42 y, después, WS30.

**FUTURO**
WS12 publica la whitelist y el contrato por operación y registra huecos; WS45/G_PAYLOAD_PRECONDITION fija la precondición de escritura; WS16 produce el acta G_HUMAN_READ; P01 emite el acta G_UI_WRITE por delta; WS19 y WS24 entregan edición/conflicto y conocimiento/grafo integrados; WS40 aporta corpus/manifiesto; WS30 ejecuta la validación humana. No corresponde a WS42 decidir esos productos ni aprobar implementación/API.
