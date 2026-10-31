REFORMULACION
Propósito: vincular mensajes y resultados a un intento existente, con deduplicación y procedencia, en el backend documental. Resultado: adaptador en `runtime/`, modelos/reportes y tests dentro de `output_scope`. Repo dueño: `deskops`. Límites: no toca tablas Scion, no incluye editor UI, solo vincula elementos con id de intento existente y no autoriza promoción ni ejecución; depende de WS32 y G_SCION.

AMBIGUEDADES
1. «Clave de deduplicación: Hub + proyecto + id de mensaje» frente a «mismo Hub/proyecto y conversación». Obligaría a inventar si «conversación» forma parte de la identidad o es solo contexto; con ids de mensaje repetidos entre conversaciones, el ejecutor elegiría clave y podría deduplicar de más o de menos.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente […] con la misma regla de deduplicación». Obligaría a inventar la clave exacta de resultados: si «misma regla» conserva Hub+proyecto y sustituye id de mensaje por id de resultado, o añade intento; afecta deduplicación y procedencia.

DRY-RUN
Sin ejecutar. Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación y `dag.yaml#node:WS33.1`; no se evalúan los bloques edge vecinos. Cambios previstos: adaptador en `runtime/`, modelos/reportes y tests. Dependencias: WS32 para identidad de intento, G_SCION resuelto por WS44, WS05/WS44 para identificadores de fuente y contratos transitivos WS11/WS12. Validaciones futuras: importación repetida sin duplicar mensajes/resultados, no atribuir una conversación completa a un intento, registrar hueco cuando el intento no sea resoluble, y comprobar que no se tocan tablas Scion.

FUTURO
WS44 produce la prueba y evidencia de G_SCION; WS05 inventaría identificadores de fuente; WS32 fija identidad de intento; WS33.2 registra la decisión humana; WS07 designa operador Scion; la promoción fijará archivos, pruebas y textos en TaskDoc; la aceptación humana autoriza o rechaza.
