### WS20 [4]
1. Cita: «Si la capacidad existe, esos tests bastan» frente a `requires: G_SLDB_WRITE`. Obligaría a inventar si la rama de solo verificación puede cerrar sin acta de alcance sldb o si el gate es previo a cualquier trabajo. La aceptación lo exime; el nodo lo exige.

2. Cita: «Si falta, se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE». Obligaría a inventar si WS20 ejecuta la implementación o solo registra/entrega esa tarea a otro ejecutor; cambia el resultado y los cambios previstos.

3. Cita: «recuperación tras fallo». Obligaría a inventar qué fallos cubre (conflicto, validación, caída, escritura parcial) y qué evidencia demuestra recuperación; sin elegirlo, la aceptación no es comprobable.

4. Cita: «conserva campos y secciones sin pérdida». Obligaría a inventar si exige roundtrip byte-idéntico o solo semántico (orden, comentarios, formato); determina qué pruebas demuestran reversibilidad.

### WS25.2 [2]
1. **Origen obligatorio frente a protoátomo libre.** Cita: «Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje)» y, en brief.md, «Protoátomo: átomo libre con título y contenido». Obliga a inventar si un protoátomo puede capturarse sin soporte de origen, qué origen mostrar en ese caso o si debe rechazarse; la aceptación exige «con origen» sin excepción.
2. **Elección del destino.** Cita: «destino elegido explícitamente por la persona usuaria» y «persiste tras recargar en el destino elegido». No define cómo se elige ni qué ocurre si no hay elección (¿bloquear guardado, destino por defecto, recordar último?). El ejecutor tendría que inventar el comportamiento, que afecta a la aceptación.

### WS26.2 [2]
1. **Criterio de solapamiento de archivos.** Cita: «sin archivos solapados según los `files` declarados en cada TaskDoc y el ritual de fase». No se define si «solapados» significa coincidencia exacta de ruta, misma carpeta, prefijo o glob. El ejecutor tendría que inventar el algoritmo de comparación, y con él qué tareas aparecen como no listas.
2. **Verificación de la promoción.** Cita: «el canal de promoción respeta commits previos y estado real». No se especifica qué commits previos, qué estado real ni cómo se comprueba en este nodo; la aceptación solo detalla el enrutado y la capa lista. El ejecutor tendría que inventar el comportamiento de promoción y su prueba, o declararlo fuera sin base explícita.

### WS27.1 [3]
1. «Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado.» No se indica dónde ni quién declara el repo, ni cómo derivarlo de las rutas. Obligaría a inventar el campo, formato y criterio de agrupación.
2. «commits listados en TaskDoc.references» no precisa cómo distinguir commits de otras referencias ni el formato esperado (hash, repo, tipo). Obligaría a inventar el criterio de selección y validación de referencias.
3. «Diff Git e historial read-only» y «sin commits, working tree contra HEAD limitado a esas rutas» no fijan el alcance del historial sin commits ni si incluye solo las rutas o todos los commits referenciados. Obligaría a inventar el rango y contenido del historial.

### WS27.2 [2]
1. **Estado de verificación no ejecutada.** Cita: «verificada = resultado de `deskops closeout verify`» y «verificación fallida se muestran como estados distintos». Obliga a inventar qué se muestra cuando la verificación no se ha ejecutado: ¿cuarto estado, asimilación a “fallida”, o ausencia de estado? También si el estado es por evidencia individual o por TaskDoc.

2. **Unidad de representación con evidencias mixtas.** Cita: «declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos, sin colapsarlos». No define si una TaskDoc con varias evidencias en estados distintos se representa por lista, por estado agregado o por contadores; obliga a inventar la unidad de estado y su agregación.

### WS28 [1]
1. «G_HUMAN_READ aplica porque es una acción de escritura del baseline.» El gate G_HUMAN_READ está definido como «Persona aprueba recorrido de lectura», con evidencia de acta de lectura producida por WS16. Aplicarlo a un handoff de cierre obligaría a inventar si el acta de lectura satisface una aprobación de escritura/cierre o si WS28 necesita otra aprobación humana distinta, y cómo conciliar ambas definiciones.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08» — WS08 no figura en `depends_on` ni se suministra su guion. Obligaría a inventar esos escenarios o a asumir un artefacto no disponible. Es una dependencia que falta.

2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó» — no se define canal, actor ni repo para abrir esa tarea, y `output_scope` solo cubre `runs/subagents/workspace-documental-acceptance/manual/`. Obligaría a inventar la operación de creación y su destino, o a exceder el alcance declarado.

### WS39 [1]
1. «Hacer navegables Schema/editar clases ya disponibles desde documento/contexto». «Contexto» no está definido en el glosario ni se concreta si son dos entradas —documento y contexto— o una; obligaría a inventar el punto de entrada y qué superficie existente se reutiliza.

### WS42 [2]
1. «modelo SLDB registrado en el store de la tarea»: no se define cuál es ese modelo/registro, dónde reside ni quién o con qué criterio valida una materialización. Obligaría a inventar la fuente de verdad, la ubicación del registro y la regla de validación.  
2. «confirmación … que ve el origen y el efecto de la operación» / «tras confirmación que muestra el origen y el efecto»: no se concreta qué compone el “efecto” —destino, relaciones, resultado del split/merge/typing— ni su representación mínima verificable. Obligaría a inventar el contenido de la confirmación y su comprobación.
