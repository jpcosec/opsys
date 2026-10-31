## REFORMULACION

**Propósito:** integrar en graph_ui las operaciones reales de conocimiento —atoms split/merge y proto typing— sobre los contratos disponibles, sin simular capacidades.

**Resultado:** vista de conocimiento en `frontends/mindmap/views/workspace/knowledge/`, invocando endpoints autorizados, con tests y declaración explícita de capabilities no soportadas.

**Repo dueño:** `graph_ui`.

**Límites:** materializaciones solo se inspeccionan/validan; no se generan destinos arbitrarios; ninguna capability ausente se simula; promoción `not_authorized`.

## AMBIGUEDADES

1. **«endpoints whitelist»** (output_scope). No queda claro si WS42 produce una whitelist propia o consume la que define WS12 («WS12 produce la whitelist final»). Obligaría a inventar el artefacto, su autoridad y su relación con el contrato de WS12.

2. **«con confirmación de alcance y procedencia»** (scope). No indica quién confirma —¿persona solicitante, WS12, WS30?— ni qué evidencia o criterio la hace válida. Obligaría a inventar actor y comprobación de aceptación.

## DRY-RUN

**Lecturas:** nodo WS42 en `dag.yaml`; aristas WS19, WS24, WS12; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; `cobertura.md` UF03; `decisiones.md` P03/P04; `alcance.md` entregas L/M; `brief.md`.

**Cambios previstos:** implementación en `knowledge/`; integración de llamadas a contratos reales; tests; lógica de declaración de no disponibilidad; sin generación de destinos.

**Dependencias:** WS19 (agregado, no ejecutable), WS24, WS12; gates pendientes resueltos por WS16/WS12; whitelist de WS12; `source_mode` según P04.

**Validaciones futuras:** WS30 (registro humano UF03); gates `G_UI_WRITE`/`G_WRITE_CONTRACT`/`G_HUMAN_READ`; preflight task-only y evidencia de promoción.

## FUTURO

- WS12 entrega whitelist final y resuelve `G_UI_WRITE`/`G_WRITE_CONTRACT`.
- WS16 produce `G_HUMAN_READ`.
- WS19 y WS24 entregan sus salidas.
- WS30 ejecuta la validación manual de UF03.
- El humano decide P03/P04 y autoriza cualquier promoción de WS42.
