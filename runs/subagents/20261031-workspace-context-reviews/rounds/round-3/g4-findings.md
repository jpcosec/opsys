### WS32.2 [3]
1. «manifiesto, RunDoc e índice de cierre coinciden en id de intento, hash de sesión y evidencia». El «hash de sesión» no aparece entre los campos mínimos del manifiesto ni se define su origen. Obliga a inventar qué sesión se hashea, cómo se obtiene y cómo se compara.
2. «índice de cierre» aparece en aceptación, mientras el scope habla de «registros de closeout». Obliga a inventar si es un artefacto distinto, su formato, ubicación y dueño.
3. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos». No define qué ocurre si la repetición trae evidencia o commit de cierre distintos. Obliga a inventar si se rechaza, se conserva lo primero o se sobrescribe.

### WS33.1 [2]
1. «una importación repetida (mismo Hub/proyecto y conversación, con checkpoint)». No se define qué es el checkpoint ni quién lo emite. Obligaría a inventar cómo se simula o reanuda y qué evidencia demuestra la idempotencia; la aceptación deja de ser comprobable sin esa decisión.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente ... con la misma regla de deduplicación y procedencia». La clave explícita es «Hub + proyecto + id de mensaje»; para resultados no se fija una clave equivalente. Obligaría a inventar si la deduplicación usa Hub+proyecto+intento+id de fuente u otra combinación, y cómo resolver colisiones.

### WS33.2 [3]
1. «Registrar la decisión humana (aprobar o pedir corrección) con actor»: no se nombra el canal ni quién produce la decisión (endpoint de deskops, CLI, payload de Scion u otro). Obliga a inventar interfaz, autorización y validación; `G_SCION` cubre el contrato de Scion, no la captura de la decisión.
2. «con actor»: no se define de dónde sale ni cómo se verifica la identidad del actor. Obliga a inventar si es cadena libre, identidad autenticada o referencia externa, y qué aceptación tendría.
3. «asociada al intento y, por él, a su tarea»: no se explicita quién garantiza el vínculo intento→tarea ni qué ocurre si un intento no resuelve tarea. WS33.1 vincula mensajes/resultados, no esa asociación.

### WS34.1 [2]
1. «timeout/errores» y «vencido por timeout»: no fija umbral, política de timeout ni formato de error. WS34.2 sí dice «con el umbral del contrato WS12», pero WS34.1 no lo remite. Obligaría a inventar cuándo vence y cómo se reporta.
2. «identidad de intento»: no indica si la produce Scion, WS33 o el adaptador, ni su formato/unicidad. Aunque depende de WS33, el nodo solo remite expresamente la autoridad del coordinador a WS12 («Autoridad del coordinador según contrato WS12»). Obligaría a inventar fuente y semántica.

### WS35 [3]
1. Scope: «Lectura tarea-intento-conversación-resultados-decisión»; acceptance: «Cada mensaje y resultado se muestra bajo su intento; cada uno enlaza a su fuente; la evidencia abre en el lector.» La aceptación no cubre tarea, conversación ni decisión, aunque el scope las incluye. Obligaría a inventar si deben mostrarse, con qué jerarquía y cómo se comprueban.
2. «Cada mensaje y resultado se muestra bajo su intento» presupone que todo mensaje/resultado tiene intento; no define qué hacer con mensajes no ligados a un intento. Obligaría a inventar su agrupación, visibilidad u omisión.
3. «la evidencia abre en el lector» no identifica qué lector ni el contrato de apertura. Obligaría a inventar el destino y la integración.

### WS44 [3]
1. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33.» WS05 produce ese inventario, pero su contrato solo obliga a señalar «capacidades que requieren API real», no a mapearlas como requeridas por WS32/WS33. Si faltan, WS44 tendría que inventar qué capabilities probar y para qué nodo.
2. «El solicitante registra en WS07 qué acceso read-only tiene el operador.» WS07 exige designar identidad/fecha del operador y declara que «no concede permiso G_EXEC», pero no obliga a registrar el nivel de acceso read-only. WS44 tendría que inventar si el acceso está autorizado y con qué alcance.
3. «verifica capacidades/identidad necesarias para intento y mensajes» / «identidad/fecha/capabilities y actor registrados». No se define si «identidad» es la del operador, el Hub/tenant, el agente remitente o el principal de API; el ejecutor tendría que elegir cuál evidenciar.
