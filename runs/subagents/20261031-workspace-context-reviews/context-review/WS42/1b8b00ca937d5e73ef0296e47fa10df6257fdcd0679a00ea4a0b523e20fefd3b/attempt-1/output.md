**REFORMULACION**
Propósito: integrar en `graph_ui` las operaciones de conocimiento ya contratadas —atoms split/merge y proto typing— sobre la vista documental. Resultado: UI que muestra alcance y procedencia, pide confirmación humana antes de mutar y declara no disponible lo no soportado; las materializaciones existentes solo se inspeccionan y validan. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/knowledge/`, endpoints de la whitelist de WS12 y `tests/`. Límites: no crear destinos, no simular capabilities, no generar materializaciones; depende de WS19, WS24 y WS12, y de G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

**AMBIGUEDADES**
1. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea»: no se identifica qué modelo o versión es ni quién lo registra en el store. WS24 cita `MaterializationContractDoc` y `deskops/models/materialization.py`, pero no aclara si ese es “el registrado en el store de la tarea”. El ejecutor tendría que inventar la identidad del modelo y el criterio exacto de validación.
2. «confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar»: no se define qué datos componen “alcance” ni “procedencia”, ni cómo se registra que la confirmación mostró ambos. El ejecutor tendría que inventar campos y evidencia. Aunque el texto exacto de pantalla quede al TaskDoc, aquí falta el contenido semántico que la aceptación exige.

**DRY-RUN**
Lecturas previstas: `dag.yaml` de WS42 y contratos vecinos, guía, brief, alcance, decisiones, cobertura, `task-ws42.md` y whitelist de WS12; sin ejecutar. Cambios previstos: componentes en `knowledge/`, invocación de endpoints whitelisted, confirmación previa, estados “no disponible” y tests. Dependencias: WS19 para edición/conflicto, WS24 para vista/modelo, WS12 para capacidades y efectos, además de los gates indicados. Validaciones futuras: WS30 sobre UF03, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

**FUTURO**
WS12 produce la whitelist y efectos por operación; WS24 aporta la vista y el modelo de materialización; WS19 define edición y conflicto; WS30 ejecuta la validación humana. El solicitante o su designado resuelve Pxx, aprueba G_UI_WRITE y autoriza la promoción, que fijará archivos, pills y evidencia.
