## REFORMULACION
PK02 es una agrupación no ejecutable cuyo resultado sustantivo es el paquete de decisiones y contratos previos a los deltas: registro trazado P01–P09, UFs con operaciones/errores/nodos/gates, índice y convención del manual, catálogo de vistas con origen/soporte, contrato de navegación/identidad y whitelist de operaciones/escritura. Repo dueño: `deskops`. Límites: no implementa producto, no autoriza mutaciones, no crea actas de recepción por delta, no supone editable sin `G_SOURCE` ni permisos Scion; los huecos se registran con productor.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
PK02 no se ejecuta directamente: termina cuando terminan sus hijos. Un ejecutor futuro respetaría las aristas: WS07 parte de WS06 y reutiliza `decisiones.md`/`owner-decisions.json`, produciendo registro y ajustes de `dag.yaml`; WS10 consume WS02/WS07 y deja `borradores/manual.md`; WS08 consume WS07 y produce `borradores/user-flows.md`; WS09 consume WS07/WS10/WS08 y produce `borradores/vistas.md`; WS11 consume WS09/WS08 y produce `contratos/navegacion.md`; WS12 consume WS11/WS08 y produce `contratos/operaciones.md`.

Cambios previstos: solo documentos de planificación en `deskops`; ninguno en repos receptores. Dependencias/gates: WS08–WS11 requieren `G_PRODUCT`; WS12 requiere `G_WRITE_POLICY`. WS12 distingue precondición de payload y no habilita escritura; `G_SOURCE` sigue pendiente de WS20 y no bloquea el núcleo ni autoriza edición.

Errores: si falta contrato/API/dato, el hijo debe detenerse, registrar hueco con repo dueño y no crear sustituto; si un recibo por delta no existe, se enlaza como pendiente, no se inventa; si una operación no tiene evidencia, se marca no comprobada/hueco, no disponible.

Validación integrada esperada: revisar que cada Pxx tenga tipo/actor/fuente/nodos/gates; que cada UF tenga entrada/salida, operación, error, nodo y gate; que cada vista declare origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; que navegación y operaciones citen APIs reales o huecos con productor; y que ningún texto prometa editable, cierre, Scion o recepción no probados.

## FUTURO
La recepción técnica por delta corresponde al solicitante P01/repos receptores al preparar cada delta; WS20 produce `G_SOURCE`; WS45 verificará la precondición de payload. La habilitación de mutaciones/UI y permisos Scion queda fuera de este paquete.
