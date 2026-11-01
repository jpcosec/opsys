# Disposición WS22, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Board real como lista, tablero y dependencias abriendo el mismo TaskDoc, estados leídos de deskops (no de dag.yaml), sin drag-and-drop de status, repo graph_ui, depende de WS13 y WS09: coincide.

**Ambigüedades.**

1. «selección y links comunes con lector» frente a output_scope board/. Clase: `no es ambigüedad`. output_scope fija el límite (`views/workspace/board/; tests/`); «comunes» = reutilizar el comportamiento de WS13 desde board/, no modificar el lector.
2. «abriendo en el lector… sus pills/átomos referenciados». Clase: `no es ambigüedad`. el lector WS13 abre cualquier documento (modelado o no); abrir un pill/átomo es seguir un enlace a un documento, sin renderer nuevo (WS24 no es dependencia porque no se pide vista de conocimiento).
3. «dependencias declaradas en el TaskDoc» (campo fuente). Clase: `detalle de promoción`. el campo del modelo TaskDoc (depends_on/references/files) y la representación los fija el TaskDoc; la aceptación («presentar predicado satisfecho… no como test aprobado») es comprobable.
