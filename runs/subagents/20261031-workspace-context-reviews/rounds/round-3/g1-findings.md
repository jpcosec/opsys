### PK02 [1]
1. «sin ambigüedad de encargo o bloqueo explícito con responsable» frente a «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa, y entonces esta aceptación no es verdadera; un bloqueo externo con responsable sí la admite». Un hijo bloqueado por ambigüedad propia cumple literalmente «bloqueo explícito con responsable» —la definición exige responsable y dependencia—, pero la frase siguiente lo excluye. Para decidir hay que inventar un discriminador de causa en `disposition.md` o una precedencia no escrita.

### PK04 [3]
1. Cita: «`context_review` del hijo en dag.yaml cuyo hash de input y de contrato coinciden con los actuales». No se define qué campo constituye el «contrato» del hijo ni de dónde se obtiene su hash actual. Obligaría a inventar la fuente y el algoritmo; el script `status` puede resolverlo, pero el encargo no lo declara como definición.
2. Cita: «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa... un bloqueo externo con responsable sí la admite». Ambos casos pueden acabar en `status=blocked` con «responsable y dependencia»; no hay campo ni criterio que distinga la causa. El revisor tendría que inventar cómo clasificar el bloqueo.
3. Cita: «con responsable y dependencia en esa disposition.md». No se define qué identifica a un «responsable» (nombre, rol, designación WS07) ni el formato mínimo. Obligaría a inventar el criterio de aceptación del bloqueo.

### PK05 [3]
1. «hash de input y de contrato coinciden con los actuales»: el input no define qué artefacto es el «contrato» ni cómo se calcula su hash. Obligaría a inventar el objeto y el algoritmo que la sesión coordinadora debe comparar.
2. «disposition.md guardada en su intento»: un hijo puede tener varios intentos; no se indica cuál cuenta (¿el último, cualquiera?). Obligaría a inventar la regla de vigencia entre intentos.
3. «read_only excluye WS20 de la entrega» (decisiones.md) frente a «cada hijo directo tiene revisión vigente»: con P04 en read_only, WS20 sigue listado como hijo, pero se excluye de la entrega. Obligaría a decidir si su revisión sigue siendo exigible para que PK05 sea verdadera.

### PK06 [2]
1. «un bloqueo externo con responsable sí la admite»: no se define qué hace «externo» a un bloqueo frente a la ambigüedad propia del hijo. Obligaría a inventar el criterio de clasificación (¿dependencia ajena, causa técnica, actor externo?) para decidir si PK06 admite el bloqueo.
   Cita: «un bloqueo externo con responsable sí la admite».
2. «cuyo hash de input y de contrato coinciden con los actuales»: no se identifica qué artefacto es el «contrato» del hijo ni quién fija su hash actual; el input remite a `dag.yaml` y a la guía, pero no a un contrato separado por hijo. Obligaría a inventar la fuente de hash.
   Cita: «cuyo hash de input y de contrato coinciden con los actuales».

### WS01 [3]
1. «Un review barato sin historial reformula el producto solo con brief.md». No define qué debe contener esa reformulación ni qué umbral la hace aceptable; obligaría a inventar criterios de suficiencia (propósito, superficies, recorridos, límites) para decidir si pasa.  
2. «Cada acuerdo de la sección «Encargo y acuerdos explícitos» cita al solicitante». La sección mezcla citas textuales y prosa de autorización; no aclara si «acuerdo» incluye solo blockquotes o también afirmaciones como «Esto autoriza corregir el plan…». Obligaría a inventar la clasificación y la forma de cita.  
3. «cada propuesta del registro Pxx remite a decisiones.md». No precisa si basta un enlace general o hay que enumerar cada Pxx en `brief.md`; obligaría a inventar cobertura y formato de remisión.

### WS02 [3]
1. «Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas» y «inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs»: no delimita si «archivo» incluye código fuente, planes, TaskDocs o solo datos runtime, ni la profundidad del inventario. Obliga a inventar el universo inventariable.

2. «Cada fila incluye ubicación (archivo o símbolo de código) y operación expuesta»: para un archivo Markdown o un dato no define qué cuenta como operación expuesta —lectura, comando que lo muta o método de API—. Obliga a inventar el vínculo archivo→operación.

3. «firmas públicas, efectos Git y cierre»: «efectos Git» no especifica qué efectos ni qué comandos entran; con aceptación de estado comprobado, obliga a decidir el alcance de esa comprobación sin ejecutar.

### WS03 [3]
1. «conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar)». No define qué es un «conflicto» (detección, resolución, solapamiento de escrituras) ni qué «límite» (timeout, granularidad, máximo, alcance). El ejecutor tendría que inventar las dimensiones del informe.
2. «referencias, búsquedas y alcance real ViewDoc». «Referencias» puede ser integridad referencial de DB, enlaces documentales o referencias de código; «búsquedas», API full-text, índices o consultas. Sin precisión, el ejecutor inventa qué inventariar y con qué evidencia.
3. «distinguir API comprobada, ausencia y hueco». No fija qué cuenta como comprobación (lectura de código, prueba ejecutada, documentación) ni qué revisión se audita; obliga a inventar el estándar de prueba y el snapshot de referencia.

### WS04 [3]
1. «mapear nodos de este plan a deltas existentes (tarea o entrada del Board de graph_ui, o commit que ya lo implementa)» junto con «Hash = SHA256 del archivo de tarea». Obliga a inventar qué `path` y qué hash corresponden a una entrada de Board sin archivo de tarea o a un commit, porque la regla de hash solo cubre archivos de tarea.

2. «identificar sesiones y solapamientos sin cambiar sus tareas». La aceptación no incluye sesiones ni solapamientos y no define qué cuenta como solapamiento. Obliga a inventar el criterio, la evidencia exigible y si ese inventario forma parte del resultado o es solo contexto.

3. «mapear nodos de este plan a deltas existentes». No acota si son todos los nodos o solo los relacionados con UI/graph_ui; el título dice «UI» pero el alcance no lo limita. Obliga a inventar el subconjunto de nodos que debe mapearse y permite exceder el alcance de `auditoria/ui.md`.

### WS05 [2]
1. «separar slug/agente/intento/dispatch/mensaje/conversación y permisos» frente a una aceptación que solo exige «No usar tablas internas como interfaz; señalar los campos internos… y capacidades que requieren API real». Obligaría a inventar qué matriz o evidencia demuestra la separación completa y si el inventario de permisos forma parte de la aceptación.  
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)» frente a «API pública definida en el scope». Obligaría a inventar la precedencia cuando documentación y exports discrepan, o el criterio para decidir si un símbolo exportado pero auxiliar cuenta como API pública; sin ello, el límite «no funciones internas» no es plenamente operable.

### WS07 [2]
1. «El humano dueño del producto confirma o corrige P01–P09 de decisiones.md y `baseline_proposal` de dag.yaml» y «decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml». No se define qué es `baseline_proposal`, dónde está ni qué campos tiene. Obligaría a inventar su esquema, su contenido y si confirmarlo equivale a aprobar el plan completo o solo una parte.
2. «| P08 | Uso humano y alcance | Proyecto Taller temporal, participante humano y presupuestos propuestos en validacion-humana.md.» Ese archivo no se suministra ni figura como dependencia de WS07. Obligaría a inventar los presupuestos, el participante y qué se está aprobando exactamente en P08, o a dar por suficiente una referencia que el ejecutor no puede verificar.

### WS11 [3]
1. «graph/code admiten otros nodos con origen»: no se define qué tipos de nodo admite cada representación ni con qué criterio. Obligaría a inventar una taxonomía de nodos admisibles.
2. «obtener aceptación del delta lector en graph_ui»: el input no delimita qué cambios componen ese “delta lector”. Obligaría a inventar el alcance exacto que el responsable de `graph_ui` debe aceptar.
3. «El acta receptora enumera scope_nodes de G_UI_READ/G_SPEC_VIEW, incluidos corpus WS40 y multidesk WS41»: no queda claro si WS40/WS41 deben constar también en el acta de `spec2viz`; en `dag.yaml#gates` solo figuran bajo `G_UI_READ`. Obligaría a decidir a qué acta pertenecen.

### WS12 [1]
1. «Aceptar deltas de escritura por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable.» No define la unidad de aceptación: ¿un acta global o una por operación/campo? Tampoco aclara si «delta» abarca todas las operaciones de los `scope_nodes` de G_UI_WRITE o solo las incluidas en la whitelist final. G_UI_WRITE fija la evidencia mínima del acta, no su granularidad. Obligaría a inventar el criterio de cierre y qué actas son exigibles.
