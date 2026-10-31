REFORMULACION
Propósito: encargo de planificación para que graph_ui tenga un generador versionado y reproducible del corpus Taller, usando el contrato WS11 y los CLI reales de deskops/sldb verificados en WS02/WS03, sin servidor fake. Resultado: comando de seed más fixtures/tests que crea o recrea un entorno aislado con dos repos temporales con desk (stores, documentos, Markdown no modelado, Code local, referencia rota), un tercer repo sin desk para UF10, enlaces authored entre desks para UF08, README/entrada mínima y manifiesto JSON con roots, stores, commits y documentos clave; admite plantillas WS17 opcionales. Repo dueño: graph_ui. Límites: no toca desk real; no produce índices ricos WS17 ni UI; WS17 solo aporta contenido authored; promoción no autorizada. Depende de WS11, WS08 y G_UI_READ.

AMBIGUEDADES
1. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a output_scope «tests/fixtures/workspace_documental/; script de seed; tests/» y aceptación «Un comando crea/recrea entorno aislado». Obliga a inventar si el comando por defecto escribe en .tmp fijo o en tmp_path, y si fixtures contiene fuentes o corpus generado; afecta al manifiesto y a la comprobación de aislamiento.
2. «Crear generador reproducible del corpus Taller» junto a «hace commits git reales en los repos temporales». No define si reproducible exige bytes/hashes/commits deterministas entre ejecuciones o solo poder recrear. Obliga a inventar fechas, autores y mensajes fijos, o a declarar no determinismo y su criterio de comparación.
3. «requires: - G_UI_READ», con WS40 incluido en scope_nodes de G_UI_READ, aunque WS40 no produce una lectura de UI. Obliga a decidir si el generador queda bloqueado por un recibo de lectura, qué delta/efecto aportaría y si basta el recibo del corpus; sin ello no se sabe si puede cerrar sin acta.

DRY-RUN
Lecturas previstas: dag.yaml (WS40, WS11, WS08), guía, alcance, decisiones y, al promover, TaskDoc. Cambios previstos: script de seed, fixtures y tests; creación de repos temporales, stores/documentos y commits reales; manifiesto JSON; README/entrada mínima. Dependencias: CLI deskops/sldb, contrato WS11, plantillas WS17 opcionales, G_UI_READ. Validaciones futuras: rerun aislado, manifiesto completo, no tocar desk real, consumo por WS16/30 y regeneración WS17. Nada ejecutado.

FUTURO
Promoción y TaskDoc fijan archivos, textos y pruebas; P01/receptor emite recibos por delta; WS16 valida con humano; WS30 usa el corpus; WS17 regenera con plantillas; WS41 lee el segundo desk; cambios de alcance vuelven a dag.yaml.
