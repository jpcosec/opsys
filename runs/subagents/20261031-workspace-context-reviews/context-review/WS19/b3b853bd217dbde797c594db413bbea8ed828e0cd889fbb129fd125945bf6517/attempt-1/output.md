## REFORMULACION

**Propósito:** WS19 es el agregado de implementación que integra en graph_ui la edición contextual de campos y de relaciones sobre el workspace ya integrado (a1b2b22), reutilizando editores y API existentes, la precondición de escritura que fija WS12 y verifica WS45, conflicto visible y campos workflow-protected no editables.

**Resultado:** las salidas de WS19.1 (`views/workspace/fields/`) y WS19.2 (`views/workspace/relations/`), con sus tests.

**Repo:** graph_ui. **Límites:** no ejecutable por sí mismo; no crea semántica de relaciones en el componente; no habilita campos protegidos; promoción no autorizada; solapa con el ticket `editing` sin duplicarlo.

## AMBIGUEDADES

ninguna.

## DRY-RUN

No hay ejecución de WS19: termina cuando terminan sus hijos. Un verificador futuro leería el contrato WS12, la evidencia de WS45, WS47/WS48 y el workspace a1b2b22.

- **WS19.1:** consume whitelist/precondición de WS12, guarda de contenido de WS47, admisión de escritura de WS48 y G_PAYLOAD_PRECONDITION. Cambia `fields/` y tests. Valida guardar/recargar, escritura obsoleta sin pérdida del texto local, rechazo visible de campos protegidos y no edición de contenido no declarado.
- **WS19.2:** consume los mismos productores; cambia `relations/` y tests. Valida alta/baja persistente tras recarga, rechazo visible de relación no permitida o revisión obsoleta, y que la baja de RelationDoc use el efecto público o se declare no habilitada.

No hay arista entre hermanos: ambos consumen WS12/WS47/WS48, pero no se transfieren nada entre sí. La validación conjunta es sobre el mismo documento en el workspace: editar un campo y agregar/quitar una relación, recargar, y comprobar que ambos efectos coexisten y cada conflicto queda atribuido a su operación, sin que un canal pise la evidencia del otro. Los recibos per_delta de G_UI_WRITE y G_WRITE_CONTRACT se consumen por hijo; no se inventa un acta propia del agregado.

## FUTURO

WS12 fija representación y whitelist; WS45 produce G_PAYLOAD_PRECONDITION; WS47/WS48 producen guarda y admisión; WS16 produce G_HUMAN_READ. El receptor P01 emite las actas por delta en graph_ui. La promoción decide extender el ticket `editing` o delta, archivos, pills y evidencia.
