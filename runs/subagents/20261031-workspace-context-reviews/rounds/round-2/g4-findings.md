### WS32.1 [3]
1. «dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc»: no se define dónde se registra cada hecho ni qué evento exacto constituye «Scion aceptó». El ejecutor tendría que inventar el modelo de estados.
2. «cambios de RunDoc por el flujo de modelos SLDB»: el input no describe ese flujo ni su autoridad; obligaría a inventar el canal y el criterio de comprobación.
3. «un dispatch fallido conservan identidades distintas»: no se delimita qué fallos cubre (rechazo, timeout, error de transporte) ni cómo se evidencia la identidad distinta. Obligaría a inventar el criterio de aceptación.


### WS32.2 [3]
1. «sobre el intento correcto»: no se define cómo elegir ese intento entre varios del mismo agente o tras un dispatch fallido. Obliga a inventar la regla de selección y su efecto sobre el cierre.
2. «según el ticket de external_references.scion»: el ticket no se transcribe en el input y sería la única definición de manifiesto y registros de closeout. Obliga a inventar campos, formato y qué significa «materializa RunDoc».
3. «Manifiesto, RunDoc y cierre consistentes» frente a «Una finalización repetida... conserva identidad y evidencia sin crear registros nuevos»: la aceptación solo cubre idempotencia, no la consistencia entre los tres. Obliga a inventar cómo se comprueba esa consistencia.


### WS33.1 [4]
1. «Referencias Hub/proyecto/conversación/mensaje/intento y resultados» y «Clave de deduplicación: Hub + proyecto + id de mensaje». La clave solo cubre mensajes: no define identidad, procedencia ni deduplicación de «resultados». El ejecutor tendría que inventar el esquema de resultados y su idempotencia; la aceptación tampoco los menciona expresamente.  
2. «Solo se vinculan mensajes y resultados con referencia al intento.» No define qué es una referencia válida ni qué hacer si un mensaje referencia varios intentos, uno inexistente o solo una conversación. Obliga a inventar la regla de correspondencia y el tratamiento de conflictos; WS32 define identidad de intento, no referencia de mensaje.  
3. «una importación repetida no duplica»: no se define «importación» (unidad, origen, lote) ni el alcance de la repetición. Aunque la deduplicación por id de mensaje acota mensajes, el ejecutor debe inventar qué se importa y cómo se prueba la no duplicación de resultados.  
4. `depends_on: WS32, WS11`: WS11 entrega contrato de navegación e identidad documental, pero el scope de WS33.1 no menciona documentos ni navegación. El ejecutor tendría que inventar qué parte de WS11 consume o por qué bloquea este backend.


### WS33.2 [3]
1. «asociada a tarea/intento», frente a la aceptación «referencia al intento»: no queda claro si el vínculo obligatorio es la tarea, el intento o ambos. Obligaría a inventar el campo y su integridad referencial.
2. «(aprobar o pedir corrección)»: la aceptación no fija valores de resultado ni exige contenido para una corrección. Obligaría a inventar el vocabulario/estado y si el texto correctivo es obligatorio.
3. «validado y cerrado los lee de deskops»: no se nombra quién valida/cierra ni el dato exacto que consumen. Si este nodo debe exponerlo, obligaría a inventar un contrato de lectura o estados que su límite no posee.


### WS34.1 [1]
1. «output_scope: runtime/; cli/commands/runtime.py o API definida; tests/» no aclara si «API definida» es un canal público ya existente o una API que este nodo deba definir. WS12 establece que el adapter es un canal público existente y que, si falta, se registra hueco y dueño, no se diseña aquí. Obligaría a inventar el canal/contrato de dispatch y podría exceder el alcance.


### WS34.2 [1]
1. «con timeout/errores» frente a «agente real demuestra respuesta vinculada al intento correcto». La aceptación solo exige demostrar el caso exitoso; no fija comportamiento observable para timeout ni para errores. El ejecutor tendría que inventar el umbral de timeout, qué errores cubrir y cuándo considerarlos aceptados.

No encuentro otras: el repo está identificado, el resultado está acotado, las dependencias y gates están nombrados, y los contratos externos tienen productores designados.


### WS35 [1]
1. «Cada mensaje y resultado se muestra bajo su intento» junto con «mensajes de Scion por su API»: no se define qué es un «resultado» ni qué dependencia lo produce con contrato propio. WS33 se titula «Vincular mensajes, resultados y decisiones», pero el alcance de WS35 solo nombra mensajes de Scion, tarea, intento y decisión. El ejecutor tendría que inventar si «resultado» es un payload de mensaje Scion, una salida del intento o un registro de WS33, y cómo se enlaza «a su fuente».


### WS36 [2]
1. «revisión con actor/evidencia visible» — no define qué actor (humano, coordinador, agente), qué evidencia ni cómo se comprueba; la aceptación no la recoge. Obliga a inventar el sujeto y el criterio de visibilidad y prueba.
2. «registrar decisiones con WS33.2» — WS33.2 no se describe en el input ni figura en `depends_on`; solo aparece como referencia. Obliga a inventar su contrato o asumir una dependencia no declarada.


### WS37 [1]
1. «G_SCION/G_EXEC y protocolo» (acceptance). No identifica qué protocolo: `validacion-humana.md` es el único protocolo suministrado, pero el nodo no lo cita ni concreta qué pasos o evidencia de ese protocolo aplican a UF06. Obligaría a inventar el protocolo de aceptación o a elegir entre fuentes. Cita textual: «acceptance: G_SCION/G_EXEC y protocolo».

