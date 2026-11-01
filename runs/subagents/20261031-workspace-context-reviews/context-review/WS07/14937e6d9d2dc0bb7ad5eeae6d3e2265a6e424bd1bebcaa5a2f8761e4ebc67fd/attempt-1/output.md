REFORMULACION

WS07 es un nodo de planificación (`kind: planning`, `node_role: delivery`) del repo deskops, dependiente de WS06. Su propósito es mantener un registro trazable de decisiones ya acordadas, reutilizando `decisiones.md` y `owner-decisions.json`: respuestas humanas literales 0–2 y mapeo P01–P09 con tipo, actor, fecha, fuente y nodos/gates. Debe señalar P07/P09 como defaults técnicos delegados, no firmas humanas; mantener `source_mode=editable` condicionado a G_SOURCE; conservar `baseline_proposal` salvo nueva decisión explícita con fuente verificable; y no atribuir aceptación de API/UI ni permisos Scion. Resultado: registro verificado y cobertura documental reutilizada, con cambios solo ante decisión real. Límites: no repetir preguntas resueltas, no implementar contratos, no inferir aceptaciones, no tocar otros nodos; `promotion: not_authorized`. `output_scope`: `decisiones.md` y los campos indicados de `dag.yaml`.

AMBIGUEDADES

ninguna

DRY-RUN

No es un agregado ni un programa: es un nodo documental; su “ejecución” futura será verificación y, solo si procede, edición de registro. Un ejecutor, tras promoción, leería `owner-decisions.json`, `decisiones.md`, `dag.yaml` (parameters, `baseline_proposal`, gates G_PRODUCT/G_WRITE_POLICY y nodos citados) y, por dependencia, `reconciliacion.md` de WS06. Compararía cada Pxx: tipo humano/técnico, actor o “sin firma/no declarado”, fecha, fuente y nodos/gates; comprobaría que P07/P09 no se presentan como firmas; que `source_mode` sigue editable y condicionado a G_SOURCE; que `baseline_proposal` conserva el texto acordado; y que G_PRODUCT/G_WRITE_POLICY enlazan evidencia existente. Cambios previstos: ninguno si todo coincide; solo actualizaría una fila, `baseline_proposal` o `source_mode` ante una decisión nueva explícita con fuente verificable. No modificaría `owner-decisions.json` ni `reconciliacion.md`. Si falta el JSON o `reconciliacion.md`, se detiene y registra el hueco en deskops, sin sustituirlo. G_SOURCE sigue pendiente de WS20 y no se satisface aquí. Validación esperada: registro completo y sin inferencias; commit atómico en deskops tras promoción, con TaskDoc que fije archivos y evidencia. Errores: fuente no verificable, Pxx sin mapeo o contradicción con el DAG impiden cerrar.

FUTURO

WS08 consume G_PRODUCT para user-flows; WS09/WS10/WS11/WS12 y WS44 reutilizan decisiones; WS20 produce G_SOURCE. Un humano puede aportar una decisión nueva explícita o autorizar la promoción; el TaskDoc fijará archivos y evidencia. La designación del operador Scion queda para el ramal E. Cualquier cambio de baseline o `source_mode` requiere esa decisión.
