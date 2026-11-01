# Comparación del coordinador — corrección de la revisión 9, aceptada para despacho

Preflight y cold en procesos Pi nuevos, sin herramientas y con stdin DEVNULL. Comparé ambas salidas completas con el encargo. Reproducen los cuatro puntos, límites y roles. Las ambigüedades listadas son de formato o quedan fijadas aquí.

- «Probada» en WS34.1 y WS34.2 = política presente en el contrato de su delta y verificada en G_WRITE_CONTRACT, que ya evalúa por delta. No se modifica el gate.
- Contrato núcleo = el que WS12 cierra para Entregas L y M; ramal E = Entrega E de alcance.md.
- Nodos finales = los 73 de `context_review.py status` más todo nodo nuevo; revisión final = la registrada en dag.yaml.
- Las atestaciones viven en `comparison-ledger.md`; los disposition.md nuevos van en el attempt que corresponda, según la ruta del runner.
- Corrección de WS42: en el result-summary de la consolidación, con nota fechada.
- Congelar = commit de fuentes antes del lote final.
- Independencia del Tester = proceso nuevo sin contexto, que no redactó ni comparó.
