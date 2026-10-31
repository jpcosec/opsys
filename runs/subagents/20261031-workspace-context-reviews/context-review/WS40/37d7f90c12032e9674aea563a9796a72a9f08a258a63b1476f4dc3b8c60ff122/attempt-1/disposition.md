# Executor comparison — WS40, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: encargo de planificación para que graph_ui tenga un generador versionado y reproducible del corpus Taller, usando el contrato WS11 y los CLI reales de deskops/sldb verificados en WS02/WS03, sin servidor fake. Resultado: comando de seed más fixtures/tests que crea o recrea un entorno aislado con dos repos temporales con desk (stores, documentos, Markdown no modelado, Code local, referencia rota), un tercer repo sin desk para UF10, enlaces authored entre desks para UF08, README/entrada mínima y manifiesto JSON con roots, stores, commits y documentos clave; admite plantillas WS17 opcionales. Repo dueño: graph_ui. Límites: no toca desk real; no produce índices ricos WS17 ni UI; WS17 solo aporta contenido authored; promoción no autorizada. Depende de WS11, WS08 y G_UI_READ.

## Hallazgos/disposición contra intención

1 descartado con cita «.tmp/... (o tmp_path en pruebas)»: CLI usa ruta temporal del corpus, tmp_path es caso tests; fixtures son fuentes/generador versionados y salida temporal, no desk real. 2 reproducible = crear/recrear corpus/relaciones mediante CLI real; no pide hashes git idénticos, commits/tiempos concretos se registran manifiesto y pruebas. 3 gate scope_nodes contiene WS40 de modo explícito: receptor acepta delta corpus/fixtures en graph_ui al prepararlo, no acta humana de lectura; no confundir G_UI_READ con G_HUMAN_READ. Dry-run correcto sobre aislamiento/manifiesto sin autorización actual.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
