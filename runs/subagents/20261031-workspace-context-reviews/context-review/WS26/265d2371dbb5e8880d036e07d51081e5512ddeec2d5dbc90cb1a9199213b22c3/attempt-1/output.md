## REFORMULACION
WS26 encarga planificar la integración de autoría y contexto de tareas en `graph_ui`: preparar candidatos con evidencia, dependencias y pills; enrutarlos explícitamente en Board y mostrar la capa lista por dependencias/no solapamiento, sin confundir ruta con ejecución. El resultado agregado son las salidas de WS26.1 y WS26.2. Límites: es agregado no ejecutable; no crea la tarea activa en WS26.1, no hace promoción parcial ni oculta efectos, no inventa API/canal y deja en handoff lo que el contrato no cubre; las mutaciones UI dependen de G_HUMAN_READ y los gates son por delta.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
WS26 no se ejecuta ni modifica archivos: termina cuando WS26.1 y WS26.2 cumplen su aceptación. Un ejecutor futuro esperaría WS12, WS22 y los gates aplicables. WS26.1 produciría el candidato preparado —título/contenido, dependencias, files, references, tags, pills y closeout_evidence validada— por recorrido rastreado con `expected`/409 o por handoff explícito a `deskops edit task` y refresco, sin escribir desde HTTP ni crear tarea activa. WS26.2 consumiría ese candidato y la autorización humana para la operación conjunta crear+enrutar, solo si WS12 admite la operación completa; si falta, mostraría pendiente/handoff. También representaría la capa lista separada de ejecución, usando `files` normalizados y ritual vigente; glob/no resolución quedaría no comprobado. Dependencias: contrato WS12 por operación, representación Board WS22, WS47/WS48 y G_PAYLOAD_PRECONDITION para escritura rastreada; G_HUMAN_READ antes de uso UI; G_WRITE_CONTRACT/G_UI_WRITE por delta; G_CLOSEOUT. Si falta contrato/API/permiso, se registraría hueco con repo dueño y la acción quedaría no disponible, sin sustituto. Validación conjunta: aceptación de ambos hijos y después WS30, que depende de WS26, con registro humano de autoría, evidencia, enrutamiento y capa lista.

## FUTURO
WS12 fija operaciones, precondición y canal; WS22 aporta Board; WS47/WS48 sus capacidades; WS45 verifica G_PAYLOAD_PRECONDITION; el receptor P01 emite actas por delta y G_HUMAN_READ; WS30 valida el recorrido humano completo.
