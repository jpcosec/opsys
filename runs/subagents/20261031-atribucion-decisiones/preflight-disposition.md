# Comparación del coordinador — procedencia de decisiones, aceptada para despacho

Leí las ambigüedades de preflight y cold, y sus reformulaciones y dry-run. Reproducen parche único, conservación de decisiones, P07/P09, invalidación de 73 y roles.

- 73 = nodos ROOT, PK01-08 y tareas de dag.yaml, una entrada por nodo. v2 = `INSTRUCTION_VERSION` del helper. Helper = context_review.py. Comando: `context_review.py run --stale`.
- Commit se cita si la procedencia depende de una versión histórica del archivo.
- Búsqueda histórica: `git log -p` de decisiones.md y dag.yaml, y runs/subagents del plan: 20261031-finalizar-plan-workspace y 20261031-workspace-context-reviews.
- Forma: conservar la tabla y su columna de nodos y gates. Legible = una afirmación humana corta en la fila y la derivación técnica identificable junto a su fuente; si no cabe, sección nueva «Procedencia técnica» en el mismo archivo.
- Vocabulario de etiqueta: «Humana», «Técnica derivada» y «Técnica sin registro histórico localizado». Límite: en el archivo y en el mapa.
- Borradores del agente preparatorio no son vinculantes; acepta el coordinador.
- Independencia del Tester: proceso nuevo sin haber redactado.
