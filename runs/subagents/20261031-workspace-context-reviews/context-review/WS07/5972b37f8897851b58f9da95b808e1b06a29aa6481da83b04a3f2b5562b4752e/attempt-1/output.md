REFORMULACION
Propósito: que el humano dueño del producto confirme o corrija P01–P09 y designe responsables, fijando `source_mode`. Resultado: `decisiones.md` con decisiones, alternativas, fecha y evidencia; designaciones de graph_ui/sldb/spec2viz y operador Scion en P01; `parameters.source_mode` editable/read_only y `baseline_proposal` en `dag.yaml`. Repo: deskops. Límites: no inventar aprobación; gates solo por registro explícito; no editar nodos; no configurar/ejecutar Scion ni conceder G_EXEC. Depende de WS06.

AMBIGUEDADES
1. «`baseline_proposal` de dag.yaml (propuesta de línea base, no aprobación del plan completo)» y output_scope «`baseline_proposal` ... en dag.yaml». No se define qué contiene ni qué debe registrarse o corregirse en esa salida. Obliga a inventar su estructura, contenido y criterio de aceptación.
2. «reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí». No dice dónde ni cómo se materializa esa reconsideración, ni qué la hace comprobable. Obliga a inventar el artefacto y su validación.

DRY-RUN
Lecturas: `decisiones.md`, `validacion-humana.md`, `dag.yaml` (`baseline_proposal`, `parameters`, `gates`) y `reconciliacion.md` de WS06. Cambios previstos: `decisiones.md` con P01–P09, designaciones, alternativas/fecha/evidencia; `parameters.source_mode` y `baseline_proposal`; sin tocar nodos. Dependencias: WS06, humano solicitante/designado, P04 y WS44. Validaciones futuras: G_PRODUCT/G_WRITE_POLICY, G_SCION de WS44 y consumo por WS08/09/10. No ejecutar.

FUTURO
El humano decide P01–P09 y `source_mode`; WS44 ejecuta el probe Scion; WS11/12 aceptan deltas por repo; WS08/09/10 consumen los gates; WS43 publica entradas reales. Nada de eso es ambigüedad de WS07.
