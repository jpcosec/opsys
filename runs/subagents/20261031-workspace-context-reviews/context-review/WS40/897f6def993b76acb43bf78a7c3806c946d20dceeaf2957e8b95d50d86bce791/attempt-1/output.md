REFORMULACION

WS40 encarga a `graph_ui` un generador reproducible —script de seed versionado en `tests/fixtures/workspace_documental/` y `tests/`— que materialice el corpus Taller: dos repos temporales con desk, stores y documentos, más un tercer repo sin desk; incluye Markdown no modelado, Code local, referencia rota, Board, FAQ y documentos de conocimiento, README/instrucciones, enlaces authored entre desks y manifiesto JSON. Usa el contrato WS11 y los CLIs reales de deskops/sldb verificados en WS02/WS03, nunca servidor fake; acepta parámetro opcional con plantillas WS17. Límites: no toca desk real, no produce índices ricos WS17, no implementa UI ni acepta deltas; los commits son solo en repos temporales. Es productor único de corpus para WS16/30.

AMBIGUEDADES

1. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)»: obliga a inventar si el corpus que consume WS16 debe persistir en una ruta fija o solo existir en `tmp_path` efímero; el manifiesto no aclara qué ubicación es canónica para validación humana posterior.

2. «imprime un manifiesto JSON con roots, stores, commits y documentos clave»: no define criterio ni lista de «documentos clave»; el ejecutor debe inventar cuáles incluir, lo que afecta la comprobabilidad del manifiesto.

3. «entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal, su FAQ Markdown y documentos de conocimiento»: no indica cuál de los dos desks con desk recibe esa entrada ni si ambos; «su» es ambiguo y obliga a inventar el alcance de la entrada.

DRY-RUN

Lecturas: nodo WS40, contrato WS11, user-flows WS08, auditorías WS02/WS03, documentación de CLIs reales, ruta de plantillas WS17 si existe y recibo G_UI_READ de WS40.

Cambios previstos: crear script de seed y pruebas en `graph_ui`; generar tres repos temporales con `git init`/commits reales, stores, documentos, README, entrada mínima, enlaces y manifiesto JSON; probar recreación y aislamiento sin tocar desk real.

Dependencias y gates: WS11 y WS08 como prerrequisitos; G_UI_READ es `per_delta` y sigue pendiente: sin recibo no se declara aceptado. Plantillas WS17 son opcionales. Si falta contrato, CLI o permiso, detenerse y registrar el hueco con repo dueño.

Validación esperada: ejecutar el comando en `tmp_path`, verificar manifiesto, commits, referencia rota, enlaces entre desks, segundo desk y reproducibilidad; ejecutar tests. Errores esperados: plantillas ausentes, CLI no disponible o gate sin recibo.

FUTURO

WS16 ejecutará la validación humana usando el manifiesto; WS17 aportará plantillas y regenerará; WS30 usará el corpus para edición; WS41 leerá el segundo desk; P01/receptor emitirá G_UI_READ y un humano autorizará promoción/TaskDoc.
