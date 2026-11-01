REFORMULACION
Propósito: vincular mensajes y resultados a un intento existente, conservando procedencia y deduplicando importaciones. Resultado: adaptador documental en `deskops` (`runtime/` según contrato), modelos/reportes y pruebas; mensajes/results repetidos no se duplican ni se atribuye una conversación completa a un intento; lo no resoluble queda como hueco de procedencia. Repo: deskops. Límites: backend documental, independiente de editor UI; no tocar tablas Scion; depende de WS32; requiere G_SCION y G_WRITE_CONTRACT; promoción no autorizada.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: nodo y gates en `dag.yaml`; salida de WS32 (identidad de intento/RunDoc); inventario WS05 y probe WS44 para G_SCION; contrato WS12 por delta; código y tests existentes de `runtime/`. Cambios previstos: adaptador en `runtime/` conforme al contrato, modelos/reportes de vínculo y procedencia, tests; sin tablas Scion. Dependencias: WS32 debe aportar el id de intento existente; WS12, campos, actor, errores y operación; WS44/G_SCION, contrato público real e identificadores de mensaje/resultado. Gates: si falta contrato o gate, detenerse y registrar hueco con dueño, sin sustituto. Validación esperada: importación repetida del mismo Hub/proyecto/conversación no duplica mensajes ni resultados; mensajes con varios intentos o sin intento resoluble no se vinculan y quedan como hueco; no se atribuye la conversación completa a un intento; resultados se deduplican por Hub/proyecto/intento/id de fuente. Errores: contrato ausente, id de intento no existente, fuente sin identificador o intento ambiguo.

FUTURO
WS32 produce identidad de intento y cierre; WS05 inventaría Scion y WS44 aporta probe/G_SCION; WS12 fija contrato, actor y efectos por delta; WS33.2 registra la decisión humana. El operador Scion se designa al abordar el ramal E.
