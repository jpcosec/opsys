REFORMULACION
Propósito: integrar en graph_ui la autoría explícita desde candidato (evidencia declarada, dependencias y contexto/pills), el enrutamiento en Board y la representación de capa lista, sin confundir Board route con ejecución. Resultado: salidas agregadas de WS26.1 y WS26.2, no un artefacto propio. Repo: graph_ui (`output_scope: 'Agregado: salidas de WS26.1, WS26.2'`). Límites: agregado no ejecutable; no promoción nueva si WS12 no la admite; no editar status para avanzar; no commits automáticos; G_HUMAN_READ solo habilita mutaciones UI y no bloquea desarrollo/pruebas API aisladas; si falta contrato u operación, detenerse y registrar hueco.

AMBIGUEDADES
Ninguna. La promoción («promoción solo cuando el contrato resuelve commits previos por canal autorizado») queda acotada por WS26.2: «No implementar promoción nueva... si falta, preparar handoff». «Capa lista» se concreta en WS26.2 con normalización, contención y glob. La aceptación agregada remite a sus hijos. Nada obliga a inventar al ejecutor de WS26 porque no se ejecuta.

DRY-RUN
No ejecutable: termina cuando WS26.1 y WS26.2 cumplen. WS26.1 leería contrato WS12, vistas WS22 y TaskDoc real; cambiaría `authoring/` y tests; consumiría G_CLOSEOUT (satisfecho), G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta; validaría UF04: candidato autorado con evidencia, dependencias y pills visibles tras recarga, sin tocar status; sin contrato Git, handoff. Transfiere a WS26.2 tarea y contexto autorados. WS26.2 leería WS12/WS22 y esa autoría; cambiaría `routing/` y tests; validaría `deskops show board`, distinción respecto de ejecución, capa lista separada, no promoción nueva y reglas de solapamiento; si falta operación, pendiente/handoff. Validación conjunta: aceptaciones de ambos hijos; después WS30 valida el recorrido manual completo. Errores: contrato u operación ausente → hueco con repo dueño, no sustituto.

FUTURO
G_HUMAN_READ lo produce WS16 mediante acta humana; G_UI_WRITE lo acepta P01 por delta concreto; G_WRITE_CONTRACT lo produce WS12; el TaskDoc de promoción fija archivos, pruebas y textos; WS30 decide la aceptación humana; la promoción de WS26 sigue no autorizada.
