REFORMULACION
Propósito: implementar en el workspace la edición de relaciones solo si el contrato las permite, mediante API real y before-image. Resultado: alta y baja persistentes, confirmadas tras recargar; relación no permitida o revisión obsoleta rechazada con error visible; código y pruebas en el ámbito declarado. Repo dueño: graph_ui. Límites: no crear semántica de relaciones en el componente; usar únicamente endpoints autorizados por WS12; someterse a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; promoción no autorizada; integración como delta o ticket existente, sin duplicado paralelo.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.2 y contratos vecinos WS12/WS16/WS19/gates. Cambios previstos: implementación en `frontends/mindmap/views/workspace/relations/` y `tests/`, sin ejecutar. Dependencias: contrato operativo de WS12 —whitelist, canal, efectos y endpoints—; validación humana de lectura de WS16; agregación en WS19; gates G_WRITE_CONTRACT, G_UI_WRITE y G_HUMAN_READ. Validaciones futuras: persistencia y recarga, rechazo visible de relación no permitida y de revisión obsoleta, uso de API/before-image, no invención de semántica; preflight y TaskDoc de promoción fijarán archivos, escenarios y textos.

FUTURO
WS12 produce el contrato y resuelve G_WRITE_CONTRACT/G_UI_WRITE; WS16 produce el acta de G_HUMAN_READ; un humano decide P04/source_mode y designa al responsable graph_ui; la promoción fijará archivos, pills y evidencia; WS19 cierra cuando cierren sus hijos. Nada de ello es ambigüedad de este nodo.
