## REFORMULACION

**Propósito:** integrar en el workspace de `graph_ui` (delta sobre `a1b2b22`) la edición de campos con revisión esperada/CAS y conflicto visible, más alta/baja de relaciones permitidas por contrato, reutilizando editores y API existentes.

**Resultado:** agregado no ejecutable; se completa cuando cumplen WS19.1 y WS19.2.

**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/`.

**Límites:** los workflow-protected fields no son editables por este canal; no se crea semántica de relaciones en el componente; con otro coordinador escritor rige lectura/handoff (P03); G_HUMAN_READ solo habilita uso de mutaciones en UI, no bloquea desarrollo ni pruebas aisladas de API; G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta concreto.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS19 y bloques de contrato de WS12, WS19.1, WS19.2, WS21, WS42 y gates. Nada ejecutado.

**Cambios previstos:** ninguno. Es revisión de encargo; WS19 sigue `candidate` y `promotion: not_authorized`.

**Dependencias:** WS12 aporta contrato/whitelist y G_WRITE_CONTRACT; WS19.1 y WS19.2 aportan las implementaciones; G_HUMAN_READ depende de WS16; G_UI_WRITE depende de recepción externa por delta del receptor P01. WS11 y WS02–WS10 llegan transitivamente.

**Validaciones futuras:** aceptación de ambos hijos; guardar/recargar y conflicto sin pérdida de texto local; alta/baja persistente y rechazo visible de relación no permitida o revisión obsoleta; pruebas en store temporal; recibos per-delta; acta humana de lectura; verificación del contrato WS12; preflight y TaskDoc de promoción.

## FUTURO

WS12 debe producir y verificar el contrato técnico por operación, incluida la whitelist de campos y relaciones. WS19.1 y WS19.2 ejecutan los deltas en `graph_ui`. WS16 produce el acta de G_HUMAN_READ. El receptor P01 en `graph_ui` emite el acta G_UI_WRITE por delta concreto. WS12 registra G_WRITE_CONTRACT en `accepted_scope_nodes`. La promoción, vía WS06 y TaskDoc, fija archivos exactos, pruebas y textos de pantalla. La decisión de promover y aceptar cada delta corresponde al humano responsable; este revisor no ejecuta ni autoriza.
