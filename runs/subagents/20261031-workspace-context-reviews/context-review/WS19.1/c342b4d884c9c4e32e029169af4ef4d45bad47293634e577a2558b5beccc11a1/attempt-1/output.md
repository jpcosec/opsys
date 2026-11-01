REFORMULACION
Propósito: planificar la edición de campos en el workspace de graph_ui con precondición de escritura y conflicto visible, reutilizando editores y API. Resultado: delta en `frontends/mindmap/views/workspace/fields/` que consume endpoints del contrato WS12 sin cambiarlo, con tests; campos workflow-protected excluidos; mutación solo en desk/modo manual exclusivo. Repo dueño: graph_ui. Límites: depende de WS12; gates G_HUMAN_READ, G_PAYLOAD_PRECONDITION (WS45), G_UI_WRITE (P01) y G_WRITE_CONTRACT; no raw-source ni cambios de contrato; otros modos read-only hasta contrato.

AMBIGUEDADES
1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.» No se define qué es “modo manual exclusivo” ni cómo la UI lo detecta y aplica. P03 habla de otro coordinador escribiendo y WS12 de policy, pero no fija ese modo. Obligaría a inventar la definición y el mecanismo de restricción, y la aceptación no sería comprobable sin ello.

DRY-RUN
Lecturas: guía, nodo WS19.1, dag/gates, brief, alcance, decisiones, cobertura, reconciliación y referencia `editing`. Cambios previstos: ninguno; solo revisión. Dependencias: contrato WS12, gate WS45, acta P01 y G_HUMAN_READ. Validaciones futuras: guardar/recargar contra store real; escritura obsoleta rechazada sin perder texto local; campos protegidos no editables; restricción de modo; tests en graph_ui.

FUTURO
WS12 publica contrato de operaciones y precondición; WS45 verifica G_PAYLOAD_PRECONDITION; P01 emite acta G_UI_WRITE por delta; WS16 emite G_HUMAN_READ. La promoción fijará TaskDoc, archivos y escenarios. Nada de esto es ambigüedad.
