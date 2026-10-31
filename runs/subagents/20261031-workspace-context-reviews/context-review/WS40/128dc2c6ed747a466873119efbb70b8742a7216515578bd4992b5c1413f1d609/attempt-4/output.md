REFORMULACION
Propósito: definir un generador reproducible, versionado en graph_ui, que materialice un corpus aislado con dos repos temporales, sus stores y documentos (Markdown no modelado, Code local y referencia rota), usando contratos/CLI reales. Resultado: comando que crea/recrea el entorno, hace commits git reales, no toca desk real, imprime manifiesto JSON (roots, stores, commits, documentos clave) y produce README/instrucciones y entrada mínima ecosistema/proyecto; admite opcionalmente plantillas WS17. Repo dueño: graph_ui (tests/fixtures/workspace_documental/; script de seed; tests/). Límites: sin servidor fake ni desk real; WS17 solo aporta contenido authored; WS40 cierra sin plantillas; depende de WS11/WS08 y G_UI_READ.

AMBIGUEDADES
1. «Crear dos repos temporales bajo .tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «nunca toca desk real». Falta la base de `.tmp`: si cuelga de graph_ui, del cwd o de un desk. Obliga a inventar dónde se escribe y si eso contradice el límite.
2. «entrada mínima ecosistema/proyecto con enlaces al Board/FAQ/conocimiento». No se define si Board/FAQ/conocimiento son documentos Markdown, datos reales de Deskops (tareas/Board) o vistas. Obliga a inventar qué se enlaza y qué se crea en el corpus.
3. «usar contratos/CLI reales» no nombra el contrato ni los comandos concretos. Aunque WS11 es dependencia, el nodo no explicita que su contrato de navegación sea el aplicable ni qué CLI crea stores/commits; obliga a elegir interfaz.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS40 y aristas; cuando existan, contrato de WS11, flujos de WS08 y repo/CLI de graph_ui. Cambios previstos: generador/seed, fixtures y pruebas, README/entrada mínima y manifiesto; sin tocar desk real ni otros repos. Dependencias: WS11, WS08, G_UI_READ; plantillas WS17 opcionales. Validaciones futuras: recreación aislada, commits en repos temporales, desk real intacto, manifiesto JSON, README reproducible y regeneración con WS17; después WS16 (humano) y consumo por WS41/WS30.

FUTURO
WS11 produce el contrato y G_UI_READ; WS08 precisa flujos; WS17 aporta plantillas authored tras WS40; WS16 valida con humano; WS41 lee el segundo store; la promoción de WS40 exige TaskDoc/preflight y autorización humana. Las Pxx siguen pendientes.
