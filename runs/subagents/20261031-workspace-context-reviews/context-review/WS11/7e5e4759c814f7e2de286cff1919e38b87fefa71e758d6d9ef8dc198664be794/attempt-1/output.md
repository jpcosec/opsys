## REFORMULACION

**Propósito:** cerrar el contrato de navegación e identidad del workspace documental: identidad/ruta/modelo opcional del Markdown, nodos graph/code con origen, resolución explícita repo/store, foco, enlaces/historia y lectura multidesk read-only; clasificar huecos y mapear recepciones por delta.
**Resultado:** `contratos/navegacion.md` bajo `deskops:desk/drawer/plans/workspace-documental/`.
**Repo:** deskops.
**Límites:** no ejecutar implementación, no escribir/commitear actas interrepo, no aprobar APIs ni inventar modelos/actores. El contrato básico puede cerrar sin acta receptora; cada delta queda bloqueado hasta su recibo. Changes, Scion y ViewDoc opcional no bloquean.

## AMBIGUEDADES

1. **Enlaces a recibos vs cierre sin acta.** Cita: output_scope "enlaces a recibos externos G_UI_READ por delta, G_SPEC_VIEW opcional" frente a acceptance "puede cerrar sin acta receptora" y "Recibos son producidos por solicitante P01/repo receptor... no por Executor de WS11". Obliga a inventar si el entregable debe contener enlaces o placeholders a actas inexistentes, o si basta el mapa de deltas.

2. **Revisión del contrato básico.** Cita: "WS11 cierra con contrato básico revisado, clasificación de huecos y mapa de deltas...". No se nombra revisor, actor ni evidencia de revisión; G_PRODUCT ya está satisfecho por WS07 y G_UI_READ no cubre el cierre del contrato. Obliga a inventar si la revisión es autocontrol, par o humana, y qué la acredita.

## DRY-RUN

- **Lecturas previstas:** `borradores/vistas.md` (WS09), `borradores/user-flows.md` (WS08), auditorías WS02–04 (`auditoria/*.md`), `decisiones.md`, gates G_UI_READ/G_SPEC_VIEW y `dag.yaml`.
- **Cambios previstos:** redactar `contratos/navegacion.md`; clasificar huecos instancia/vínculo/consulta/API/renderer con productor dueño; mapa de deltas graph_ui con actor P01, IDs y efectos; enlaces solo a actas ya registradas.
- **Dependencias:** WS09 y WS08 cerrados; G_PRODUCT satisfecho; G_UI_READ pendiente por delta, no bloquea el cierre base; G_SPEC_VIEW separado para WS18.
- **Validaciones futuras:** cada identidad/origen/foco/enlace/multidesk debe citar API real con path/símbolo/commit; ningún recibo declarado como recibido; revisión del contrato y comprobación de que no se excede alcance.

## FUTURO

- P01/repo receptor produce actas G_UI_READ por delta al preparar cada implementación; G_SPEC_VIEW se obtiene al preparar WS18.
- WS12 consume este contrato para operaciones/escritura; WS13.x, WS40 y WS41 lo usan para lectura, corpus y multidesk.
- La promoción fijará archivos, TaskDoc y preflight; la aceptación de deltas y permisos Scion queda fuera de WS11.
