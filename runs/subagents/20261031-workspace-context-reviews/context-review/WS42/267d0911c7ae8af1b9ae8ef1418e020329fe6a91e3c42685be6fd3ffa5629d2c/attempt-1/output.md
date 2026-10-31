REFORMULACION
- **Propósito:** integrar en `graph_ui` las operaciones reales de conocimiento —split/merge de átomos y tipado de protoátomos— con confirmación humana que muestre origen y efecto, e inspeccionar/validar materializaciones contra `MaterializationContractDoc` mediante API SLDB, sin generar destinos.
- **Resultado:** vista/espacio `knowledge/` que invoca contratos WS12, marca materializaciones inválidas como no operables y declara no disponibles las capabilities no soportadas, con tests.
- **Repo dueño:** `graph_ui`.
- **Límites:** endpoints solo de la whitelist WS12; sin renderer propio de materializaciones; no simular capacidades; mutaciones UI sujetas a `G_HUMAN_READ`; `G_UI_WRITE`/`G_WRITE_CONTRACT` se evalúan por delta.

AMBIGUEDADES
1. **Origen de las materializaciones a inspeccionar.** Cita: «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea» y «registrado en el store temporal real seleccionado por TaskDoc (o manifiesto Taller WS40)». No se define de dónde salen esas materializaciones existentes si el store de la tarea está vacío ni si crear fixtures cuenta como «no se generan destinos arbitrarios». El ejecutor tendría que inventar el origen de los datos o la política de fixtures.
2. **Registro de versión/commit.** Cita: «versión/commit registrados». No se especifica de qué artefacto (modelo, materialización, store) ni dónde, quién o con qué evidencia se registra. El ejecutor tendría que inventar el formato y ubicación del registro.
3. **Dependencia no declarada para el fallback.** Cita: «(o manifiesto Taller WS40)». WS40 no figura en `depends_on` ni en `requires`; si se usa como fuente alternativa, el ejecutor debe decidir si espera a WS40 o sustituye el dato, sin arista que lo respalde.

DRY-RUN
- **Lecturas previstas:** `dag.yaml#node:WS42`, guía, brief, alcance, decisiones, cobertura, gates y bloques de vecinos WS12/WS19/WS24/WS30.
- **Cambios previstos:** extender `frontends/mindmap/views/workspace/knowledge/`, tests y llamadas a endpoints de la whitelist WS12; sin backend nuevo ni renderer propio.
- **Dependencias:** WS12 (contrato/whitelist), WS19 (edición/conflicto), WS24 (vista/backlinks), WS30 (validación humana); gates per_delta `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.
- **Validaciones futuras:** pruebas aisladas de API, inspección/validación de materializaciones, escenarios UF03 en acta WS30 y etiquetas de disponibilidad. Nada ejecutado.

FUTURO
- TaskDoc de promoción fijará archivos, store, escenarios y textos; WS12 publicará whitelist y huecos; WS40 aportará corpus/manifiesto; WS16 emitirá `G_HUMAN_READ`; el receptor P01 emitirá `G_UI_WRITE` por delta; WS30 registrará la aceptación UF03.
