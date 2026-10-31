REFORMULACION
Propósito: WS33 es un agregado que agrupa la vinculación de mensajes/resultados a intentos (WS33.1) y el registro de decisión humana (WS33.2), con deduplicación y procedencia, como backend documental sin editor UI. Resultado: agregado no ejecutable de las salidas de sus hijos; se cumple cuando ambos cumplen su aceptación. Repo: deskops. Límites: no tocar tablas Scion, no UI, no ejecutar aquí; requiere G_SCION y depende de WS32/WS11; promoción no autorizada.

AMBIGUEDADES
1. Posible dependencia sobrante de WS11. Cita: `depends_on: - WS32 - WS11 - WS33.1 - WS33.2`. Los hijos solo declaran WS32 y el alcance trata vínculos Scion, deduplicación y decisión, no la navegación/identidad documental de WS11; obligaría a inventar por qué WS11 es prerrequisito del agregado o a decidir ignorarlo. Ninguna otra.

DRY-RUN
Lecturas: nodo WS33 y sus hijos en dag.yaml; task-ws33.md; aceptación/evidencia de WS33.1 y WS33.2; acta G_SCION de WS44; contratos WS32/WS12 citados. Cambios previstos: ninguno, por ser aggregate. Dependencias: WS33.1/2 completos, WS32 y WS11 resueltos, G_SCION verificado. Validaciones futuras: aceptación de ambos hijos, deduplicación/procedencia, decisión con actor y resultado aprobar/pedir corrección, ausencia de tablas Scion y que WS33 no se marque ejecutado por sí mismo.

FUTURO
WS44 produce la probe/acta G_SCION; WS07 designa al operador Scion; WS12 fija actor y operación de la decisión; WS33.1/2 aportan evidencia; WS34/35 consumen el resultado. La autorización de promoción/ejecución y la resolución de gates son decisiones humanas o de otros nodos, no ambigüedades.
