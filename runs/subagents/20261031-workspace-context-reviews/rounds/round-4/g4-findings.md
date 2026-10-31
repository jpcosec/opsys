### WS32.1 [4]
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc». «del RunDoc» admite leer “separados de” o “hechos del”. Obliga a inventar si viven fuera del RunDoc o como campos nuevos dentro.
2. «evidenciadas por ids de intento propios». No dice quién genera el id de intento ni con qué forma o garantía; `confirmed` remite a la identidad de la API, pero `intent` no. Obliga a inventar autoridad y generación del id (local/API/derivado).
3. «un dispatch fallido (rechazo o timeout de la API)». Un timeout no equivale a rechazo: la API pudo aceptar sin respuesta. Obliga a inventar si `confirmed` queda falso, desconocido o se reconcilia después.
4. «cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc». No define evidencia ni criterio observable de “no ad hoc”. Obliga a inventar cómo se demuestra en aceptación.

### WS32.2 [2]
1. «hash de sesión» aparece como campo mínimo y criterio de coincidencia en la aceptación, pero no se define en el input cómo obtenerlo, calcularlo ni compararlo. El ejecutor tendría que inventar su fuente y semántica de igualdad; si depende de Scion, debería indicarlo un contrato o el inventario de WS05.
2. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos» no fija qué ocurre si la repetición trae evidencia o hash distintos: conservar, rechazar o diagnosticar. El ejecutor tendría que inventar la política de conflicto.

### WS33.1 [2]
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «mismo Hub/proyecto y conversación». Obligaría a inventar si «conversación» forma parte de la identidad o es solo contexto; con ids de mensaje repetidos entre conversaciones, el ejecutor elegiría clave y podría deduplicar de más o de menos.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente […] con la misma regla de deduplicación». Obligaría a inventar la clave exacta de resultados: si «misma regla» conserva Hub+proyecto y sustituye id de mensaje por id de resultado, o añade intento; afecta deduplicación y procedencia.

### WS33.2 [2]
1. «asociada al intento y, por él, a su tarea»  
   Ningún contrato suministrado define explícitamente cómo se resuelve la tarea desde el intento; la aceptación solo exige «referencia al intento», no a la tarea. El ejecutor tendría que inventar el campo, relación o consulta intento→tarea, o decidir que basta el intento.

2. «depends_on: - WS32 - WS11 - WS33.1»  
   WS11 entrega un contrato de navegación e identidad documental, pero WS33.2 no indica qué artefacto de WS11 consume para registrar decisiones, intentos o tareas. Obliga a inventar el vínculo o a aceptar una dependencia que solo bloquea.

### WS35 [2]
1. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea»: no define qué hacer con mensajes o resultados sin intento/tarea vinculada. Obligaría a inventar si se ocultan, se agrupan aparte o se muestran como error.
2. «la evidencia abre en el lector (WS13)»: no define el comportamiento si la evidencia no es un documento legible por WS13 (por ejemplo, un diff o artefacto). Obligaría a inventar una representación o fallback no previsto.

### WS38 [1]
1. «output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados» — no se fija qué átomos crear ni con qué criterio quedan «vinculados»; la aceptación no menciona átomos. Obligaría al ejecutor a inventar la lista y el criterio de enlace, y a decidir si basta un átomo por capítulo o por acuerdo. Podría resolverse en la promoción si esta fija archivos, pero no se declara que los átomos sean detalle delegado.

### WS44 [2]
1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» y «capabilities… registrados»: no se define cómo se comprueba una capability de escritura (dispatch/mensaje) sin ejecutarla —¿endpoint de introspección, catálogo documentado o llamada real?—. Obligaría a inventar el método y podría chocar con el límite de no enviar mensajes.

2. «El operador indica el Hub desde la configuración existente»: no se indica ubicación, formato ni qué hacer si existen varios Hubs. Obligaría a inventar la fuente autoritativa del Hub.
