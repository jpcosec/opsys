Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes ni declares haber probado comportamiento. No corrijas nada. Eres uno de tres Testers sin solape.

Tu ronda anterior y sus FAIL están en runs/subagents/20261101-ws12-operaciones/renovacion-1/tester-b-result.md, sobre bytes anteriores. La tabla de disposición está al final de runs/subagents/20261101-ws12-operaciones/result-summary.md: compruébala, no la asumas. Vuelve a recorrer TODA tu parte.

Separa LECTURA PROPIA de DATO DEL SUPERVISOR (runs/subagents/20261101-ws12-operaciones/tester-facts.log).

Contrato: desk/drawer/plans/workspace-documental/contratos/operaciones.md. Prefijos: GU/ = ../UIs/graph_ui/frontends/mindmap/ (tests en ../UIs/graph_ui/tests/), SL/ = ../sldb/src/sldb/ (tests en ../sldb/tests/), DK/ = raíz deskops, PR/ = ../pron/. Estas rutas existen: ábrelas con esa ruta relativa. Rótulos del contrato: COMP = prueba citada, LEC = lectura estática, NOAC = no aceptado como canal, HUE = hueco.

Recorre TODAS las filas y afirmaciones de tu parte, no una muestra. Abre cada cita en su línea real. Un test citado debe existir con ese nombre y probar lo que dice la fila. Comprueba cada negación con grep y cada «COMP» contra el test. Busca efectos transitivos no declarados: una lectura o diagnóstico que escribe. Lectura estática no es prueba de runtime: FAIL si el contrato lo presenta como probado.

TU PARTE: secciones 5, 6, 7, 8 y 9.

Autoridad: desk/drawer/plans/workspace-documental/decisiones.md (P03, P05, T-P03, T-P03.1) y runs/subagents/20261031-atribucion-decisiones/root-decision-20261101.md, y la parte final de runs/subagents/20261101-ws11-disponibilidad/review-source.md.

Comprueba además: ¿la ausencia de señal declara exclusividad en alguna fila? ¿El lock de UI se presenta como coordinación? ¿Se confunden `expected`, token publicado y capacidad compartida? ¿Es cierto que ningún escritor consume `version`? ¿La comparación de captura es exacta opción por opción? ¿`message send` + `promote` queda sin aprobar? ¿El ack pasa a disponible por un comando parecido? ¿closeout queda fuera del servidor UI?

Informe: una fila por afirmación con evidencia real archivo:línea, PASS o FAIL; lista final de FAIL con la corrección que implicaría; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
