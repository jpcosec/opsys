## REFORMULACION
**Propósito:** verificar y mantener el registro trazable de las decisiones de núcleo ya acordadas (P01–P09), reutilizando `decisiones.md` y `owner-decisions.json`, sin reabrir preguntas ni inferir aprobaciones técnicas.
**Resultado:** registro con tipo humano/técnico, actor, fuente, fecha y nodos/gates por Pxx; `baseline_proposal` y `parameters.source_mode` de `dag.yaml` conservados salvo decisión nueva explícita y verificable.
**Repo:** `deskops`; salida en `desk/drawer/plans/workspace-documental/`.
**Límites:** no aprobar API/UI, contratos, actas de uso ni permisos Scion; P07/P09 son defaults técnicos delegados; `source_mode=editable` queda condicionado a G_SOURCE; no sustituye cobertura de UFs ni auditorías de WS06; promoción no autorizada.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas previstas:** `decisiones.md`, `owner-decisions.json` (respuestas 0–2), `dag.yaml` (`baseline_proposal`, `parameters.source_mode`, gates G_PRODUCT/G_WRITE_POLICY), `brief.md`, `alcance.md`, `cobertura.md` y `validacion-humana.md` solo como contraste de límites.
**Cambios previstos:** ninguno por defecto; si aparece una decisión nueva explícita con fuente verificable, actualizar el Pxx correspondiente en `decisiones.md`, `baseline_proposal` y/o `parameters.source_mode` según alcance. Sin decisión nueva, no editar.
**Dependencias:** WS06 como antecedente de auditorías/reconciliación; `owner-decisions.json` ya producido y localizable; G_PRODUCT y G_WRITE_POLICY registrados; G_SOURCE pendiente no bloquea el registro, solo la habilitación real de escritura.
**Validaciones futuras:** comprobar que cada P01–P09 tenga tipo, actor, fuente y nodos/gates; que no se repitan preguntas resueltas; que no se deduzca aceptación de API/UI ni permiso Scion; que `source_mode` conserve la condición G_SOURCE; que el string de `baseline_proposal` coincida con la base acordada; preflight de promoción y archivos exactos quedan para TaskDoc.

## FUTURO
WS08 consumirá G_PRODUCT para user-flows; WS20 producirá G_SOURCE; el solicitante decidirá cualquier cambio real de decisión y designará operador Scion al abordar el ramal E; la promoción y el TaskDoc fijarán archivos, pills y evidencia; WS06 aportará reconciliación sin que WS07 la sustituya.
