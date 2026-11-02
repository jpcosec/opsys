REFORMULACION
Propósito: construir en graph_ui la captura con destino elegido —candidato de drawer o protoátomo— definida por WS25.2, sin crear tarea. Resultado: captura persistente tras recargar, con origen (ruta o mensaje), colisiones controladas y «permisos del contrato aplicados». Repo: graph_ui, limitado a `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no crea API ni modelo; depende de la capacidad probada por WS46 y de la admisión WS48; G_HUMAN_READ solo habilita uso; no autoriza mutaciones reales ni actas.

AMBIGUEDADES
1. «origen ... con representación fijada por el contrato WS12». WS12 dice: «Es una propuesta: ningún test comprueba que se conserve». Obliga a decidir si la representación es contractual o propuesta, e inventar el criterio de persistencia.
2. «endpoints autorizados por el contrato WS12». WS12 no autoriza endpoints: declara HO-01 y que la captura «no está habilitada». Obliga a elegir rutas e inventar su contrato de error.
3. «Permisos del contrato aplicados». WS12 fija la whitelist y deja al adaptador «fijar el store, el path y el modelo»; no enumera permisos para captura. Obliga a inventar la lista aplicable.
4. «G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas ... pueden avanzar». No aclara si el nodo puede cerrarse antes de G_HUMAN_READ o si este bloquea la entrega; obliga a inventar la condición de cierre.

DRY-RUN
Ejecutor futuro: leería WS25.2, WS12 (3, 4.2, 7, 10), pruebas de WS46 y API de WS48. Cambios previstos: módulo de captura y tests en graph_ui; sin tocar deskops/sldb. Dependencias: WS46 debe probar origen, colisión y no-tarea para cada destino; WS48, la admisión; WS12 fija representación y endpoints. Validación: persistencia tras recarga, origen ruta y mensaje visibles, colisión sin sobrescritura, ninguna tarea en Board ni `list tasks`. Estado esperado: bloqueado; sin WS46/WS48 y sin endpoint autorizado no hay ejecución válida. Errores: dependencia ausente, endpoint no autorizado, colisión o falta de admisión.

FUTURO
WS46 produce y prueba la capacidad; WS48 produce la admisión; P01 registra el acta; el humano concede G_HUMAN_READ y autoriza la promoción. Nada de eso lo decide este nodo.
