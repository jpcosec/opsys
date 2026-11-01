REFORMULACION
WS08 es un encargo de planificación en deskops: precisar `borradores/user-flows.md` para que UF01–UF10 queden mapeados a operaciones auditadas de WS02/03/04, con entrada, salida, operación, error esperado, nodo del DAG y gate humano, incluyendo manual, captura, revisión, cambios UF07/WS29, arranque, multidesk, schemas y modo degradado. El resultado es un `user-flows.md` revisado y trazable, sin prometer funciones fuera de alcance; una operación ausente se marca como hueco. Límites: no implementa, no habilita delegación/Scion; UF02 responder es local y el ack queda pendiente de WS12; UF08 es solo lectura y el envío interdesk queda fuera de baseline. Repo dueño: deskops; depende de WS07 y G_PRODUCT ya satisfecho.

AMBIGUEDADES
ninguna.

DRY-RUN
No es un agregado ni ejecuta software: su ejecución futura consiste en producir el documento. Leería guía, brief, alcance, decisiones, cobertura, validacion-humana, DAG de WS08/arista WS07 y el borrador existente; consultaría las auditorías por dependencia transitiva vía WS06/WS07. Cambios previstos: reescribir `borradores/user-flows.md` añadiendo por UF los campos exigidos, mapa de operaciones, errores, nodos/gates, huecos con dueño y notas de degradado; no tocar otros archivos. Dependencias/gates: G_PRODUCT satisfecho; WS07 y auditorías transitivas. Errores: si falta auditoría u operación, registrar el hueco y detenerse según reglas comunes; si no hay gate humano adicional, escribir “ninguno adicional”; no inventar API ni actores. Validación esperada: UF01–UF10 completas, campos presentes, listas de operación/nodo/gate completas, WS29 distinguido como prueba técnica y G_SCION/G_EXEC no habilitados.

FUTURO
WS09 usará el mapa UF para el catálogo de renderizaciones; WS11 y WS12 para navegación y contrato de ack; WS16/30/37/39 ejecutarán los gates humanos; WS40 aportará el corpus. El humano ya resolvió P08; no se reabre.
