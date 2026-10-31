### WS19 [1]
1. **`kind: implementation` frente a `node_role: aggregate` y “Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.”** El nodo declara naturaleza de implementación y estimación M, pero su aceptación lo declara no ejecutable. Esto obliga al ejecutor a inventar si WS19 produce artefactos propios (código, tests, evidencia) o solo coordina a sus hijos; una lectura literal de `kind` podría exceder el alcance agregado.

### WS25.2 [2]
1. «destino elegido explícitamente por la persona usuaria» no se refleja en «una captura persiste tras recargar con origen...». Falta criterio para comprobar la elección explícita o rechazar un destino por defecto; obligaría a inventar cómo se evidencia y si un default cumple.
2. «cada destino se prueba por separado» no se concreta en la aceptación, que habla de «una captura». Obligaría a inventar si drawer y protoátomo deben pasar ambos persistencia/origen tras recarga o si basta uno, y qué resultado distinto se espera.

### WS26.2 [2]
1. «sin archivos solapados según los `files` declarados en cada TaskDoc» y «archivos solapados» en acceptance. No se define contra qué conjunto se compara el solapamiento: otras tareas de la capa lista, tareas en ejecución, todo el Board o tareas futuras. Obliga a inventar el criterio de exclusión y, por tanto, el resultado de «capa lista».
2. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real». No queda claro si WS26.2 debe implementar una acción/UI de promoción o solo enrutar y declarar handoff; «estado real» no se define. Obliga a inventar alcance y aceptación observable.

### WS29 [1]
1. «muestra documento afectado, relaciones alcanzadas (...) y errores. (...) errores = hallazgos de esos tres comandos, agrupados por comando». No se especifica si deben mostrarse **todos** los hallazgos o solo los asociados al documento afectado. El ejecutor tendría que inventar el criterio de filtrado y el alcance de la lista de errores.

### WS30 [1]
1. Cita: «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». `WS08` no figura en `depends_on` de WS30 y `validacion-humana.md` no fija el guion de teclado; esto obligaría a inventar esos escenarios o a suponer una dependencia no declarada.

### WS39 [1]
1. **Alcance de la mutación según `source_mode`.** Cita: «UF09 inspección y mutación en store temporal real de prueba» y «usar draft/validate/promote de sldb». El contrato vecino WS12 indica: «aceptar delta en sldb solo si source_mode=editable». Si `source_mode=read_only`, no queda claro si WS39 puede cerrar solo con inspección o si la aceptación exige mutación y el nodo queda bloqueado. Obligaría a inventar el criterio de cierre en modo lectura.

### WS43 [2]
1. «Registrar conocimiento durable en átomos antes de docs» / «los acuerdos durables aplicados al mapa quedan en átomos enlazados desde él». No se define qué acuerdos son «durables» ni el criterio de «aplicados al mapa». WS31 sí fija una regla (Pxx aceptadas y contratos), pero WS43 no remite a ella. Obligaría a inventar el conjunto de átomos y si incluye contratos o solo decisiones aceptadas.
2. «Aplicar entradas/índices authored validados en Taller al deskops real» / «el mapa publicado corresponde a las entradas/índices validados en Taller». WS17 entrega plantillas de ejemplo y WS30 las valida, pero no se define qué parte es plantilla reutilizable y qué debe reescribirse con los repos reales. Obligaría a inventar el mapeo ejemplo→ecosistema real.
