REFORMULACION
Propósito: fijar como encargo de implementación el vínculo de mensajes y resultados con un intento existente, con deduplicación y procedencia. Resultado: importación repetible que no duplica mensajes ni resultados, no atribuye conversaciones completas y deja como hueco los mensajes sin intento resoluble. Repo: deskops (runtime/adaptador, modelos/reportes, tests). Límites: backend documental sin editor UI; solo ids de intento existentes; no tocar tablas Scion; depende de WS32 y del gate G_SCION con contrato público real.

AMBIGUEDADES
1. «Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, con la misma regla de deduplicación y procedencia.» La clave declarada es «Hub + proyecto + conversación + id de mensaje», campos que un resultado puede no tener. Aunque se nombra WS05/WS44 para comprobar el identificador, no se define cómo se compone la clave de resultados ni su ámbito de unicidad. Obligaría a inventar la tupla de deduplicación de resultados y si dos resultados con el mismo id de fuente en conversaciones distintas son el mismo.
2. «un mensaje con varios intentos o sin intento resoluble no se vincula»: no se fija cómo decidir que hay «varios intentos» ni el criterio de «resoluble». Obligaría a inventar la regla de resolución/desambiguación y si esos mensajes también quedan como hueco.

DRY-RUN
Lecturas: nodo WS33.1, aristas WS32/WS33/WS33.2 y gate G_SCION; guía, brief, alcance, decisiones, cobertura y reconciliación; task_file solo referenciado. Cambios previstos: adaptador runtime, modelos/reportes y tests en deskops; sin UI ni tablas Scion. Dependencias: WS32 (agregado; WS32.1/2, WS05, WS12), G_SCION resuelto por WS44; WS05/WS44 para el identificador de resultados. Validaciones futuras: probe G_SCION; importación duplicada sin duplicados; mensajes multi/sin intento como hueco; resultados idempotentes; no atribución de conversación. No se ejecuta nada.

FUTURO
WS44/WS07 producen evidencia G_SCION y designan operador; WS05 inventaría la fuente; WS32 fija identidad/manifiesto; la matriz WS06 llega transitivamente por WS11/WS12. La promoción fijará TaskDoc, archivos, pills y evidencia, con preflight y autorización humana; las propuestas P01–P09 no se resuelven aquí.
