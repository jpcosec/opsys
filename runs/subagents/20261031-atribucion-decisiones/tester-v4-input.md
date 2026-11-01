Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes. No corrijas nada.

Lee runs/subagents/20261031-atribucion-decisiones/comparison-ledger.md, ws07-cobertura-efectiva.md, root-focal-approval-20261101.md, tester-v4-facts.log (declaraciones del Supervisor, no verificación tuya) y final-attempts.json, todos en esa carpeta. Contrato de cada nodo: desk/drawer/plans/workspace-documental/dag.yaml. Fuente: decisiones.md y context-review-guide.md de esa carpeta del plan.

1. Registro. Elige 8 nodos de dag.yaml, incluidos WS07, WS12 y WS33.2. ¿context_review.evidence apunta al intento de final-attempts.json? ¿Esa carpeta tiene output.md, disposition.md y receipt.json con technical_failure false? ¿La ruta contiene el input_sha256?
2. Falsa aceptación. Elige tú 8 nodos con ambigüedades de: PK07, WS04, WS10, WS12, WS15.1, WS18, WS22, WS24, WS26.2, WS27.2, WS30, WS32.1, WS35, WS37, WS43, WS45. Lee output.md, disposition.md y el bloque del nodo en dag.yaml. ¿Alguna clasificada como detalle, no-ambigüedad o futuro asignado obligaría de verdad a inventar un resultado? Di cuáles elegiste. Comprueba por aristas lo que la disposición afirma sobre alcanzabilidad.
3. Rechazos. Lee attempt-1 y attempt-2 de PK02, PK07, WS16, WS19, WS33.2 y WS37. ¿Cada defecto era real? ¿Desapareció? ¿Algún defecto comparable sigue sin declararse? ¿Algún attempt-1 NO rechazado de la lista WS13, WS15, WS25, WS27, PK04 tiene una transferencia entre hermanos sin arista?
4. Aristas. Para WS13, WS15, WS19, WS25, WS27 y WS26 vigentes: compara cada transferencia afirmada con depends_on en dag.yaml.
5. Atribución. ¿El ledger, la cobertura o las disposiciones afirman algo que no pueda ser cierto o que exceda lo que dicen haber leído? En especial la tabla de conteos y que WS07 esté cubierta. Marca toda frase de ese tipo.
6. Límites. ¿Algo indica cambio de decisión, contrato o gate, activación de WS08-12, UI, Scion o push? Distingue lo visto de lo declarado.

Informe: tabla con objeto, evidencia real (archivo:línea leído), PASS o FAIL; hallazgos; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`. PASS significa que lo examinado es correcto, aunque queden observaciones menores.
