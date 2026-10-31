## REFORMULACION
**Propósito:** integrar en la UI de conocimiento las operaciones existentes de atoms split/merge y proto typing, con confirmación humana que muestre alcance y procedencia. **Resultado:** escenarios UF03 (dividir/reunir/tipar) con persistencia, referencias y conflictos reales; inspección/validación de materializaciones existentes sin crear destinos; capabilities ausentes declaradas no disponibles, sin simulación. **Repo dueño:** `graph_ui`. **Límites:** `frontends/mindmap/views/workspace/knowledge/`, endpoints solo de la whitelist de WS12, `tests/`; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; aceptación cubierta por WS30.

## AMBIGUEDADES
1. **«las materializaciones existentes se inspeccionan y validan contra el modelo SLDB vigente»** — no se nombra artefacto, versión, repo ni nodo que produzca ese modelo. Obligaría a inventar cuál es la fuente autoritativa y cómo determinar su vigencia.
2. **«se inspeccionan y validan»** — no define resultado observable ni criterio de validación (¿mostrar, informar, bloquear?) ni qué ocurre si la validación falla. Obligaría a inventar la aceptación concreta de esa parte.
3. **«que ve el alcance y la procedencia antes de ejecutar»** — no fija qué información mínima debe verse ni cómo se comprueba en la aceptación, que no menciona esta confirmación. Obligaría a inventar contenido y verificación.

## DRY-RUN
**Lecturas previstas:** nodo WS42 y gates; whitelist/capabilities de WS12; deltas de WS19 y salidas de WS24; fuente del modelo SLDB (a confirmar); guion UF03/WS08 y `validacion-humana.md` para WS30. **Cambios previstos:** UI de invocación de split/merge/typing con confirmación; inspección/validación de materializaciones; declaración de no disponibilidad por capability; tests en `knowledge/` y `tests/`. **Dependencias:** WS12 debe entregar capability exacta; WS19 aporta edición/conflicto; WS24 aporta vista y navegación; gates pendientes. **Validaciones futuras:** pruebas con store temporal/corpus WS40, persistencia/referencias/conflictos, ausencia de simulación y registro manual WS30.

## FUTURO
WS12 produce y acepta la whitelist/capabilities y el delta de escritura; WS07 designa responsables y resuelve Pxx; WS16 produce `G_HUMAN_READ`; WS30 ejecuta la validación humana; un humano decide umbrales y corpus. Nada de eso se resuelve en este nodo.
