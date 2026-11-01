REFORMULACION
Propósito: integrar en el workspace de graph_ui (base a1b2b22) la edición de campos y relaciones permitidas, con conflicto visible, precondición de escritura y campos protegidos no editables. Resultado: nodo agregado cuyas salidas son las de WS19.1 y WS19.2; no ejecutable por sí mismo. Repo dueño: graph_ui. Depende del contrato WS12 y de sus hijos. Límites: reutilizar editores/API y before-image; no crear semántica de relaciones en el componente; gates por delta; promoción no autorizada; solapamiento con `editing` se resuelve en preparación, sin duplicar implementación.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS19, gates y contratos vecinos de `dag.yaml`; guía, brief, alcance, decisiones, reconciliación y cobertura. Cambios previstos: ninguno en este revisor; la ejecución futura de los hijos afectaría `frontends/mindmap/views/workspace/fields/`, `relations/` y `tests/`. Dependencias: contrato WS12; G_PAYLOAD_PRECONDITION producido por WS45; G_HUMAN_READ por WS16; G_UI_WRITE por aceptación P01 por delta; G_WRITE_CONTRACT; base a1b2b22/f16fcd1/134a665 y ticket `editing`. Validaciones futuras: guardar/recargar confirma dato real; escritura obsoleta no pierde texto local y muestra conflicto; alta/baja permitida persiste y la no permitida se rechaza; campos protegidos no editables; acta de lectura y recibos por delta.

FUTURO
No son ambigüedades: WS12 fijará representación de la precondición y whitelist; WS45 verificará la precondición de payload; WS16 producirá el acta de lectura; P01 emitirá la aceptación por delta en graph_ui; la promoción concreta decidirá archivos, escenarios y textos; WS06/reconciliación ya fijaron la base reutilizable y el ticket candidato `editing`. WS21 y WS42 dependen de este agregado.
