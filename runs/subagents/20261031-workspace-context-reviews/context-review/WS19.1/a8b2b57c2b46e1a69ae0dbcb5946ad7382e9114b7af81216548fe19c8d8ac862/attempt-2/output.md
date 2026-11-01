REFORMULACION
Encargo: implementar en graph_ui la edición de campos del workspace con conflicto visible. Resultado: guardar/recargar confirma el dato real y una escritura obsoleta no pierde el texto local. Repo: graph_ui (`frontends/mindmap/views/workspace/fields/`, `tests/`). Límites: solo desk en modo manual exclusivo; campos workflow-protected no editables; otros modos read-only; sin cambiar el contrato WS12.

AMBIGUEDADES
1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.» Ninguna fuente define qué es «modo manual exclusivo», quién lo declara ni cómo se comprueba. Obligaría a inventar un indicador o mecanismo de modo y su actor; sin ello el ejecutor no sabe cuándo habilitar la mutación ni qué significa «otros modos».

DRY-RUN
Lecturas: contrato WS12 (`contratos/operaciones.md`), ticket `editing`, vistas actuales del workspace y tests. Cambios: componentes de edición de campos en `frontends/mindmap/views/workspace/fields/` y pruebas; consumir endpoints de WS12 sin modificarlos. Dependencias/gates: WS12 debe fijar representación de precondición, whitelist y conflicto; exigen evidencia `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION` (WS45), `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta. Errores: contrato o evidencia ausente → detener y registrar hueco; campo protegido → rechazar; escritura obsoleta → conflicto visible conservando texto local y sin sobrescribir; fallo de guardado → no declarar éxito. Validación esperada: guardar y recargar muestra el dato persistido; repetir con escritura obsoleta produce rechazo visible y conserva el texto; pruebas focalizadas en verde.

FUTURO
WS12 fija representación y whitelist; WS45 produce `G_PAYLOAD_PRECONDITION`; WS16 produce `G_HUMAN_READ`; el receptor P01 emite `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta; la promoción fija TaskDoc. No son ambigüedades de este nodo.
