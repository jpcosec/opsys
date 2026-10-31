REFORMULACION
Propósito: que una persona real recorra UF01–UF05 (lectura, captura, autoría, edición de conocimiento, revisión y cierre por handoff) sobre el ejemplo, según guion y protocolo. Resultado: acta humana versionada, decisión de G_HUMAN_MANUAL y tareas de corrección en los nodos causantes. Repo dueño: graph_ui; evidencia en runs/subagents/workspace-documental-acceptance/manual/. Límites: no sustituir el acta por tests ni declarar disponible un flujo por tests verdes; no revisar vecinos.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no figura en depends_on y su guion no se suministra: el ejecutor tendría que inventar escenarios y el criterio de navegación por teclado, o decidir bloquear. La regla de alcance sobre huecos no fija el orden en el DAG.
2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó». Si la causa recae en WS25/WS26 (aggregate no ejecutables, sin hijos en el input) o cruza varios nodos, el destinatario de la tarea es indeterminado; obliga a inventar dónde registrarla.

DRY-RUN
Lecturas: nodo WS30 y edges suministrados, brief, alcance, decisiones, cobertura, validacion-humana, user-flows y guía. Cambios previstos: redactar runs/.../manual/acta.md con guion, versiones/commits, corpus, comandos, timestamps, capturas, ayudas, fallos y decisión; commit atómico en graph_ui; actualizar G_HUMAN_MANUAL con evidence_ref; abrir tareas de corrección y enlazar el acta desde el plan. Dependencias: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42; corpus WS40 transitivo; guion WS08 no declarado; gates G_UI_WRITE/G_WRITE_CONTRACT/G_HUMAN_READ transitivos. Validaciones futuras: protocolo, conflicto en dos ventanas, diff real, handoff closeout verificado, presupuestos p95 y muestras 20/10/10.

FUTURO
Deciden o producen otros: P04 source_mode y P08 participante/umbrales (WS07/humano); guion de WS08; corpus WS40; plantillas WS17; publicación real WS43; manual WS31; aprobación humana del gate. Un fallo puede abrir cambio de nodos y exigir revalidación.
