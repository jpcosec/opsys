## REFORMULACION
- **Propósito**: agrupar la publicación básica sobre recorridos ya demostrados.
- **Resultado**: manual versionado y entradas del desk real publicados, con instrucciones trazables a actas/versiones, entradas `desk/README.md` y mapa authored probados, y procedencia átomo→documento verificada.
- **Repo**: `deskops`.
- **Límites**: PK06 es agregado no ejecutable; no autoriza tareas ni añade aristas; no implementa ni sustituye la aceptación de sus hijos; Scion, modelos y Changes no demostrados siguen propuestos y no bloquean el manual básico. La revisión de comprensión no equivale a producto entregado.

## AMBIGUEDADES
ninguna.

## DRY-RUN
PK06 no se ejecuta: termina cuando terminan sus hijos. Por aristas, WS43 precede a WS31.

WS43, tras WS17 y WS30 y con sus gates pendientes, consume las plantillas/índices WS17 y el acta WS30; publica en `deskops` `desk/README.md`, mapa/índices authored y átomos enlazados, más su acta de publicación. Contrasta paths/hashes WS17 con lo validado por WS30, enlaza todos los repos de `deskops list repositories` y muestra entradas ausentes sin fabricarlas. Entrega a WS31 el mapa publicado, acta/commit y átomos.

WS31, tras WS10, WS30 y WS43, consume el índice de WS10, el acta WS30 y el acta/versión WS43; publica `docs/workspace-user-manual.md`, assets y átomos de Pxx/contratos. Cada instrucción debe citar acta/versión y límites; links y atom→doc deben resolver; Scion queda propuesto, y modelos/Changes también si faltan G_HUMAN_MODEL/WS29.

Validación conjunta: WS43 debe corresponder al conjunto WS17 validado por WS30; WS31 debe citar la publicación WS43 y no prometer lo no demostrado. Si falta acta, versión, link o contrato, se detiene y se registra el hueco con repo dueño, sin sustituirlo.

## FUTURO
WS17, WS30 y WS10 producen entradas, acta e índice; el participante P08 recorre WS43; G_HUMAN_MANUAL y recibos por delta quedan para humanos/productores; WS38 añade Scion tras demostrarlo.
