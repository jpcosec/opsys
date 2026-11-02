## REFORMULACION
WS33.1 encarga, en deskops, un backend documental que vincule mensajes y resultados de Scion a un intento existente, conservando procedencia y deduplicando por Hub+proyecto+conversación+mensaje y Hub+proyecto+intento+id de fuente. Resultado: adaptador, modelos/reportes y pruebas en `runtime/`, `modelos/reportes` y `tests/`. Límites: solo vínculos con id de intento existente; mensajes con varios intentos o sin intento resoluble quedan como hueco; no tocar tablas Scion; sin dispatch/reply; depende de WS32 y de G_SCION/G_WRITE_CONTRACT por delta.

## AMBIGUEDADES
1. «Solo se vinculan mensajes y resultados con referencia a un id de intento existente; un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco.» La regla de hueco se enuncia solo para mensajes; para resultados sin intento resoluble o con varios no se define si se descartan, se registran como hueco ni con qué clave. Obligaría a inventar el tratamiento y su aceptación.

## DRY-RUN
Lecturas: contrato WS12 por delta vía G_WRITE_CONTRACT; identidad de intento de WS32.1; inventario WS05 y probe WS44 para identificadores de fuente; candidato Scion; `runtime/scion.py` (`record_scion_run`), servicios de cierre y modelos existentes.

Cambios previstos: adaptador en `runtime/` que lea la fuente y escriba vínculos con las claves de deduplicación, procedencia y huecos; modelos/reportes; tests de importación repetida. Sin tocar tablas Scion.

Dependencias: WS32 debe entregar un id de intento estable; WS44 debe resolver G_SCION con endpoint/identidad; WS12 debe fijar operación, actor y efectos. Si falta cualquiera: detener, registrar hueco con dueño y no crear sustituto, según alcance.

Validación esperada: dos importaciones de la misma conversación no duplican mensajes ni resultados; un mensaje con varios o ningún intento no se atribuye y queda como hueco; ninguna conversación completa se asigna a un intento. Errores: contrato, gate o id ausente → operación no disponible.

## FUTURO
WS33.2 consumirá los vínculos para registrar la decisión humana; WS34/WS35 usarán intento y procedencia; WS44 resolverá G_SCION; WS12 emitirá el contrato; WS05 inventariará la API. Un humano designa el operador Scion. Nada de esto lo decide WS33.1.
