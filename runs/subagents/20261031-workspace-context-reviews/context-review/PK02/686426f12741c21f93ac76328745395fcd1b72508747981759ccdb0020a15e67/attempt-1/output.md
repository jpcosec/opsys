**REFORMULACION**

PK02 es un agregado de planificación, no ejecutable: su propósito es producir el paquete coherente de decisiones y contratos que habilita los deltas posteriores. El resultado sustantivo son artefactos en `deskops`: registro trazado de Pxx, user-flows UF01–UF10 con operaciones/errores/nodos/gates, convención e índice del manual, catálogo de vistas con origen/contrato/renderer/estado, contrato de navegación/identidad y contrato de operaciones/whitelist/escritura. Límites: no implementa UI/API, no ejecuta mutaciones, no crea actas interrepo, no autoriza tareas ni añade aristas; lo editable queda condicionado a `G_SOURCE` y los extras no bloquean el núcleo.

**AMBIGUEDADES**

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». No se define artefacto, responsable ni comprobación de esa integración; obligaría a inventar dónde se consolida el paquete y quién valida el resultado conjunto, más allá de revisar cada salida.

**DRY-RUN**

Hipotéticamente, un ejecutor leería `decisiones.md`, `owner-decisions.json`, auditorías WS02–04, brief, alcance, cobertura y `dag.yaml`. Orden por aristas: WS07 reutiliza/verifica decisiones y entrega registro a WS08, WS09, WS10, WS11 y WS12; WS08 produce UFs y las transfiere a WS09/WS11/WS12; WS10 fija la convención/estado del manual y alimenta WS09; WS09 cataloga vistas usando UFs y convención y entrega a WS11; WS11 cierra identidad/navegación y entrega a WS12; WS12 cierra operaciones/whitelist. Cambios previstos: `decisiones.md`, `borradores/user-flows.md`, `borradores/manual.md`, `borradores/vistas.md`, `contratos/navegacion.md`, `contratos/operaciones.md`. Dependencias/gates: `G_PRODUCT`, `G_WRITE_POLICY`; `G_SOURCE` pendiente para editable. Validación integrada esperada: matriz Pxx→nodos/gates, cada UF con operación/error/nodo/gate, cada vista con origen/contrato/renderer/estado, navegación y operaciones sin actores/API inventados, huecos con productor y recibos por delta solo enlazados. Si falta auditoría o decisión: detener y registrar hueco. No hay pruebas de producto.

**FUTURO**

P01/repos receptores producen actas por delta; WS20 produce `G_SOURCE`; WS45 `G_PAYLOAD_PRECONDITION`; WS40 el corpus; WS16/30/37/39 validaciones humanas. Nada de ello se ejecuta aquí.
