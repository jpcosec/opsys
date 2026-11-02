# Aprobación de `operaciones.md`

Decisión root por delegación, 2026-11-02. No es aprobación humana. Texto: `runs/subagents/20261102-ws12-correccion/review-source-4.md`.

**Aprobado para uso de planificación:** `contratos/operaciones.md`, sha256 `754546d60c5ec47b369c8a8b3d47124615659481403939855bb1ff76b4ce9f39`, y el diseño de los nodos finales de `dag.yaml` revisión 10.

El encabezado de ese archivo dice «borrador» y se conserva como fotografía revisada. Para esos bytes, ese estado queda superado documentalmente por esta nota. Si el archivo cambia, esta nota no lo cubre.

**Precisiones de root.** El piso de WS47 es el mínimo observado en `_write_doc`, no exhaustividad: no puede rebajarse ni habilitar una pérdida conocida declarándola residuo. «No se inventa otro criterio» en §6.7 significa no inventarlo ahora en WS12; una ampliación futura la justifica el inventario y pasa la aceptación, sin merge nuevo ni promesa de editar todo ruido. WS26.1 es un único nodo: sus dos recorridos se entregan juntos aunque B no use WS47 ni WS48. La base `a1b2b22` existe en graph_ui y no es el `frontends/workspace/` excluido; su material y estado se recuperan al promover.

**No aprueba:** capacidades, implementación, actas humanas ni recepción. `G_WRITE_CONTRACT` sigue `pending` y `accepted_scope_nodes` vacío; `execution_authorized` sigue false. Ninguna fila queda aceptada por acta.

**Cobertura:** incremental por bytes, sin Tester único final, sin certificar las 65 filas y sin runtime. Detalle: `runs/subagents/20261102-ws12-correccion/freeze-final.md`.
