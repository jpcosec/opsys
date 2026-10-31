## REFORMULACION
**Propósito:** integrar en `graph_ui` las operaciones de conocimiento ya contratadas (atoms split/merge y proto typing), con confirmación humana previa que muestre alcance y procedencia.
**Resultado:** vista/componente en `frontends/mindmap/views/workspace/knowledge/` que invoca contratos reales vía la whitelist de WS12, más tests; toda capability ausente se declara no disponible y no se simula.
**Repo:** `graph_ui` (owner_repo).
**Límites:** endpoints solo whitelist WS12; materializaciones se inspeccionan/validan, no se crean destinos arbitrarios; depende de WS19, WS24, WS12 y gates G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT, hoy pendientes por diseño.

## AMBIGUEDADES
1. «materializaciones se inspeccionan/validan, no se generan destinos arbitrarios» — el alcance incluye un comportamiento (inspección/validación de materializaciones) que la aceptación no recoge: no dice qué se valida, contra qué contrato ni cómo se comprueba. Obligaría a inventar resultado y criterio de aceptación, o a decidir si queda fuera.
2. «cada capability no soportada se declara no disponible y bloquea ese escenario» — «ese escenario» no está delimitado: puede ser la capability concreta, UF03 o el gate WS30. Obligaría a inventar el alcance del bloqueo y su efecto sobre la validación.

## DRY-RUN
**Lecturas (sin ejecutar):** guía, brief, alcance, decisiones, cobertura, nodo WS42 y bloques vecinos de `dag.yaml` como contratos.
**Cambios previstos:** implementación en `knowledge/` y `tests/` de `graph_ui`; llamadas a operaciones atoms split/merge y proto typing autorizadas; UI de confirmación con alcance/procedencia; estados de no disponible.
**Dependencias:** WS12 (whitelist, adapter y canal), WS19 (edición con conflicto), WS24 (grafo local/backlinks); gates G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.
**Validaciones futuras:** aceptación UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales; registro humano en WS30 bajo protocolo; escenarios no soportados bloquean, no simulan.

## FUTURO
WS12 produce whitelist, capability exacta y evidencias de G_UI_WRITE/G_WRITE_CONTRACT; WS16 resuelve G_HUMAN_READ; WS30 registra la aceptación humana y abre tarea en el nodo causante si falla el guion; el TaskDoc de promoción fija archivos, pills, textos de pantalla y escenarios; P04 (`source_mode`) y las demás Pxx quedan a decisión humana en WS07.
