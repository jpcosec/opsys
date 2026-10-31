REFORMULACION (propósito, resultado, repo, límites)  
Encargo de planificación para WS33.1: definir la vinculación de mensajes y resultados a un intento, con referencias, procedencia y deduplicación. Resultado esperado: backend documental en `deskops`, con adaptador, modelos/reportes y tests. Límites: no editor UI, no modificar tablas Scion, solo vincular mensajes/resultados con referencia al intento; depende de WS32/WS11 y del gate G_SCION.

AMBIGUEDADES  
1. «Referencias Hub/proyecto/conversación/mensaje/intento y resultados» y «Clave de deduplicación: Hub + proyecto + id de mensaje». La clave solo cubre mensajes: no define identidad, procedencia ni deduplicación de «resultados». El ejecutor tendría que inventar el esquema de resultados y su idempotencia; la aceptación tampoco los menciona expresamente.  
2. «Solo se vinculan mensajes y resultados con referencia al intento.» No define qué es una referencia válida ni qué hacer si un mensaje referencia varios intentos, uno inexistente o solo una conversación. Obliga a inventar la regla de correspondencia y el tratamiento de conflictos; WS32 define identidad de intento, no referencia de mensaje.  
3. «una importación repetida no duplica»: no se define «importación» (unidad, origen, lote) ni el alcance de la repetición. Aunque la deduplicación por id de mensaje acota mensajes, el ejecutor debe inventar qué se importa y cómo se prueba la no duplicación de resultados.  
4. `depends_on: WS32, WS11`: WS11 entrega contrato de navegación e identidad documental, pero el scope de WS33.1 no menciona documentos ni navegación. El ejecutor tendría que inventar qué parte de WS11 consume o por qué bloquea este backend.

DRY-RUN  
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS33.1, aristas WS32/WS33/WS33.2 y gates. Cambios previstos: ninguno ahora; a futuro, solo `runtime/`, modelos/reportes y tests en `deskops`. Dependencias: WS32, WS11 y G_SCION (`WS44`/`WS07`). Validaciones futuras: contrato público real, importación repetida sin duplicados, no tocar tablas Scion y prueba de vinculación.

FUTURO  
WS44 con operador designado en WS07 produce G_SCION; WS32 fija identidad/manifiesto/cierre de intento; WS11 obtiene aceptación de su contrato; el TaskDoc de promoción fijará archivos, escenarios y evidencia. WS33.2 registra la decisión humana.
