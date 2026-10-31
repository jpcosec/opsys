REFORMULACION
Propósito: registrar una decisión humana —aprobar o pedir corrección— con actor y vínculo a tarea/intento. Resultado: un registro persistido en deskops que otros leen; no registra el `completed` del agente como aprobación. Repo: deskops. Límites: este nodo solo escribe la decisión; no implementa UI, no toca tablas Scion y no ejecuta cierre ni validación.

AMBIGUEDADES
1. «asociada a tarea/intento», frente a la aceptación «referencia al intento»: no queda claro si el vínculo obligatorio es la tarea, el intento o ambos. Obligaría a inventar el campo y su integridad referencial.
2. «(aprobar o pedir corrección)»: la aceptación no fija valores de resultado ni exige contenido para una corrección. Obligaría a inventar el vocabulario/estado y si el texto correctivo es obligatorio.
3. «validado y cerrado los lee de deskops»: no se nombra quién valida/cierra ni el dato exacto que consumen. Si este nodo debe exponerlo, obligaría a inventar un contrato de lectura o estados que su límite no posee.

DRY-RUN
Lecturas previstas: guía, nodo WS33.2, WS32, WS11, WS33.1, gates y `task_file`. Cambios previstos: adaptador en `runtime/`, modelos/reportes y tests dentro de `output_scope`; registro de decisión con actor y referencia. Sin tablas Scion ni UI. Dependencias: WS32, WS11, WS33.1 y G_SCION; este último lo produce WS44. Validaciones futuras: decisión registrada con actor y referencia, `completed` nunca aprobado, lectura por consumidores. No se ejecutó nada.

FUTURO
WS44 produce G_SCION; WS07 designa actores/operador Scion; WS33.1 vincula mensajes y resultados; validación/cierre consumen el registro; el TaskDoc de promoción fija archivos y pruebas; el humano resuelve las Pxx.
