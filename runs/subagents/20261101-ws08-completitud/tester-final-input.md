Eres un Tester independiente del estado final, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes. No corrijas nada.

Separa siempre tres fuentes: LECTURA PROPIA (abriste el archivo), DATO DEL SUPERVISOR (runs/subagents/20261101-ws08-completitud/tester-final-facts.log) y COMPROBACIÓN ROOT (runs/subagents/20261101-ws08-completitud/root-focal-approval.md). No presentes una como otra.

Lee en runs/subagents/20261101-ws08-completitud: comparison-ledger.md, final-attempts.json, root-focal-approval.md, review-source.md, completeness-matrix.md, result-summary.md. Contratos: desk/drawer/plans/workspace-documental/dag.yaml. Fuentes: desk/drawer/plans/workspace-documental/borradores/user-flows.md y desk/drawer/plans/workspace-documental/cobertura.md.

1. Integridad: de final-attempts.json, elige 10 nodos, incluidos WS07, WS08, WS10, WS12, WS23, WS29 y WS42. ¿context_review.evidence en dag.yaml apunta a ese intento? ¿Hay output.md, disposition.md y receipt.json con technical_failure false? ¿La ruta contiene input_sha256 del nodo? ¿manifest.json declara v2?
2. Rechazos: lee attempt-1 y attempt-2 de WS23, WS29 y WS42 (misma carpeta de hash). ¿Cada defecto era real contra el contrato? ¿Desapareció?
3. Falsa aceptación: elige 10 nodos con ambigüedades entre WS09, WS12, WS13, WS13.1, WS13.3, WS15.1, WS17, WS21, WS22, WS27.1, WS28, WS30, WS32.1, WS34.2, WS35, WS41, WS43, WS45. Lee output.md, disposition.md y el contrato completo. ¿Alguna clase oculta una contradicción real? ¿Algún FUTURO o dry-run aceptado contradice arista, gate, productor, actor u output_scope? Di cuáles elegiste.
4. Aristas: ¿los agregados WS13, WS15, WS19, WS25, WS26, WS27, WS32, WS33 y WS34 describen transferencias solo donde depends_on las sostiene?
5. Fuente: ¿user-flows.md y cobertura.md conservan los productores de la decisión root? ¿WS29 sigue sin ser gate ni prerrequisito? ¿WS22 fuera de Nodo en UF01?
6. Atribución: ¿el ledger o las disposiciones afirman algo que exceda lo que dicen haber leído? Revisa los conteos que puedas comprobar.
7. Límites: ¿algo indica activación de WS09, WS11, WS12, UI, Scion o push, o cambio de contrato o gate?

Informe: tabla con objeto, fuente (LECTURA PROPIA, SUPERVISOR o ROOT), evidencia archivo:línea, PASS o FAIL; hallazgos; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`. PASS admite observaciones menores.
