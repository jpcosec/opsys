Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes. No corrijas nada. Declara cobertura exacta: bloques tocados, no las 65 filas.

Separa LECTURA PROPIA de DATO DEL SUPERVISOR (runs/subagents/20261102-ws12-correccion/tester-d-facts.log).

Autoridad: runs/subagents/20261102-ws12-correccion/review-source-3.md. Diffs: runs/subagents/20261102-ws12-correccion/patch-3-contrato.diff y runs/subagents/20261102-ws12-correccion/patch-3-dag.diff. Contrato desk/drawer/plans/workspace-documental/contratos/operaciones.md, DAG desk/drawer/plans/workspace-documental/dag.yaml. DK/ = raíz deskops. Abre cada cita.

1. Dos recorridos en §4.4 y WS26.1: rastreado por S02; no rastreado por propuesta, handoff y refresco, sin HTTP ni «aplicado». ¿Queda W02 como escritura de la UI en alguna parte? ¿Prueba de stale prometida para CLI?
2. closeout_evidence: ¿excepción solo en drawer? ¿W03 permitido en algún lado? ¿id, status, current_node, history, from_drawer protegidos? Abre deskops/services/closeout_gates.py:54 normalize_declared_evidence.
3. Pills: lista entera, conservación, validación, sin bind, sin merge.
4. Selector: abre deskops/desk_paths.py:24-64, operations.py:_editable_artifact, _resolve_task_payload, _resolve_glob y cli/commands/operations.py:127-130. ¿Es cierto que show task solo busca en desk/tasks? ¿La comprobación es previa a mutar? Si no, ¿no hay comando? ¿Prueba de selector idéntico y prefijo?
5. G_PAYLOAD_PRECONDITION en WS26 con su razón; sin expected a handoff ni W01; WS47 en WS26.1. Sin ciclos.
6. WS47: qué detecta, qué no, qué queda deshabilitado; residuo no aprueba pérdida conocida.
7. Gemelas: §9.3, §4.2, §5.7, §10.2, HO-01, HO-02, §13.3, WS26.1, WS26.2: handoff de creación y promoción de WS26.2; ninguna frase «root debe decidir» o «ambigüedad abierta».

Informe: tabla con objeto, evidencia real archivo:línea, PASS o FAIL; lista final de FAIL con corrección implicada; cobertura. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
