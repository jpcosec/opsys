REFORMULACION  
Propósito: integrar en `graph_ui` las operaciones reales de conocimiento (`atoms split/merge`, proto typing) con confirmación humana que muestre origen y efecto, e inspeccionar/validar materializaciones existentes sin crear destinos. Resultado: UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales; materializaciones inválidas visibles y no operables; capabilities no soportadas declaradas no disponibles. Repo dueño: `graph_ui`. Límites: salida en `frontends/mindmap/views/workspace/knowledge/`; endpoints solo whitelist de WS12; no simular; cubierto por WS30; promoción no autorizada.

AMBIGUEDADES  
1. «modelo SLDB registrado en el store de la tarea»: no se define cuál es ese modelo/registro, dónde reside ni quién o con qué criterio valida una materialización. Obligaría a inventar la fuente de verdad, la ubicación del registro y la regla de validación.  
2. «confirmación … que ve el origen y el efecto de la operación» / «tras confirmación que muestra el origen y el efecto»: no se concreta qué compone el “efecto” —destino, relaciones, resultado del split/merge/typing— ni su representación mínima verificable. Obligaría a inventar el contenido de la confirmación y su comprobación.

DRY-RUN  
Lecturas: guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS42 y bloques de WS19, WS24, WS12, WS30 y gates. Cambios previstos: ninguno; esta revisión no edita `dag.yaml` ni promueve el nodo. Dependencias: WS19, WS24, WS12; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras: WS12 cierra whitelist y contrato; WS30 ejecuta la aceptación manual de UF03; `G_UI_WRITE` exige acta humana; la promoción requiere TaskDoc y preflight.

FUTURO  
WS12 produce la whitelist final y clasifica APIs; WS24 aporta la vista de documento/materializaciones; WS30 valida UF03; el humano designado acepta `G_UI_WRITE` y resuelve las Pxx de WS07; el TaskDoc de promoción fija archivos, pruebas y textos. Nada de esto se ejecuta aquí.
