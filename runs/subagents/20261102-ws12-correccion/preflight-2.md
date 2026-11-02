## REFORMULACION

Encargo: en la tarea correctiva activa, aplicar siete ajustes (U03/WS48, WS26.1, separación candidato/promoción, HO-03, §6.3/§8, S01/S02/§9.4, WS47) con revisión de ambigüedad y canal Executor/Tester, sin abrir otro proyecto ni tocar producto. Verificados por Supervisor y Tester independiente, autoriza tres reviews baratas no ejecutoras (WS19.1, WS25.2, WS26.1); luego congelar/renovar solo nodos changed/pending con helper canónico; con vigencia y Testers, ejecutar checks documentales y 13 tests del helper y entregar checkpoint final. Excluye closeout, G_WRITE_CONTRACT, ejecución WS46/47/48, UI, SLDB, Scion y push; preserva cambios ajenos.

## AMBIGUEDADES

1. Cita: «un update seguro cuyo render no pierde contenido se aplica (incluido documento limpio); no promete editar todo documento con ruido ni un merge preservador». No define «pérdida de contenido» ni «ruido»; obligaría a inventar el criterio operativo de la guarda y el límite entre documento limpio y con ruido.

2. Cita: «F1 por configuración confiable externa suministrada por el responsable, cargada por WS48». No fija formato, ubicación ni mecanismo de carga; obligaría a inventar esquema y procedimiento, o a asumir uno existente sin base textual.

3. Cita: «requires G_PAYLOAD_PRECONDITION (su resolver WS45)». El antecedente de «su» es ambiguo: ¿WS45 resuelve la precondición o WS47? Obligaría a decidir el grafo de dependencias sin base textual.

## DRY-RUN

Hipotético: se localizan los siete puntos en contrato y aceptación; se corrigen textos y derivados; se recalculan hashes/diff; Supervisor coteja citas y Tester independiente verifica los siete sobre bytes finales. Si procede, se lanzan las tres reviews con contrato versionado, sin historial; se resuelven ambigüedades; se renuevan nodos changed/pending con helper; con vigencia y Testers se ejecutan checks y 13 tests; checkpoint final. Se detiene ante ambigüedad material nueva, compromiso humano o productor ausente.
