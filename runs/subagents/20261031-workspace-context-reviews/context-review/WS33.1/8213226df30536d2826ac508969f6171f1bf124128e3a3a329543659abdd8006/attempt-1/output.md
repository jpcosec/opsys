REFORMULACION
Propósito: vincular mensajes y resultados a un intento existente, con deduplicación y procedencia. Resultado: backend documental en `deskops` (`runtime/`, modelos/reportes, `tests/`), sin editor UI. Límites: no tocar tablas Scion; no vincular mensajes sin intento resoluble o con varios intentos; no inventar contrato ni sustituirlo. Depende de WS32 y del gate G_SCION, aún no verificado.

AMBIGUEDADES
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente… con la misma regla de deduplicación y procedencia». La única clave explícita es «Hub + proyecto + conversación + id de mensaje», aplicable a mensajes, no a resultados. El ejecutor tendría que inventar la clave de deduplicación de resultados o asumir que el identificador de fuente sustituye al de mensaje.
2. «un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco». No se define qué artefacto, campos ni comprobación materializan ese «hueco»; la aceptación solo cubre deduplicación y no atribuir una conversación completa. El ejecutor tendría que inventar el modelo/reporte de hueco y su evidencia.

DRY-RUN
Lecturas previstas: `dag.yaml#node:WS33.1`, guía, brief, alcance, decisiones, cobertura y reconciliación; no se ejecuta nada. Cambios previstos: adaptador en `runtime/`, modelos/reportes y tests del repo `deskops`; sin tablas Scion. Dependencias: WS32, y por él WS05/WS12 según el DAG; G_SCION pendiente. Validaciones futuras: importación repetida sin duplicar mensajes/resultados; no atribuir conversación completa a un intento; mensajes con varios intentos o sin intento resoluble no se vinculan y dejan procedencia/hueco; contrato público real comprobado.

FUTURO
WS44, con operador Scion designado en WS07, resolutará G_SCION y documentará endpoint/identidad/capabilities. WS05/WS44 deben exponer el identificador de resultados y el contrato público. El TaskDoc de promoción fijará archivos, pills y evidencia. Las Pxx siguen pendientes de decisión humana; este nodo no las aprueba.
