REFORMULACION

WS33 es un agregado de implementación en deskops: vincula mensajes y resultados de Scion a intentos, con deduplicación y procedencia, y registra la decisión humana (aprobar/pedir corrección) asociada al intento y su tarea. No produce artefacto propio; su resultado es la suma verificada de WS33.1 y WS33.2. Límites: backend documental, independiente del editor UI; no toca tablas Scion; no hace dispatch/reply; completed no equivale a aprobado. Depende de WS32, WS11 y sus hijos; requiere G_SCION y G_WRITE_CONTRACT. Promoción no autorizada.

AMBIGUEDADES

1. «depends_on: - WS32 - WS11 - WS33.1 - WS33.2» frente a «Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación». WS11 no lo declaran los hijos y el alcance es backend documental, no navegación. Obliga a decidir si WS11 condiciona el cierre del agregado, si debe añadirse a los hijos o si la arista sobra.

DRY-RUN

WS33 no se ejecuta: es agregado. Un ejecutor futuro lo trataría como cierre de hijos.

- WS33.1: leería el contrato público de Scion (Hub/proyecto/conversación/mensaje/intento), crearía adaptador en `runtime/`, modelos/reportes y `tests/`; aplicaría dedup y registraría huecos. Consume WS32 y G_SCION/G_WRITE_CONTRACT. Validaría importación repetida sin duplicados, sin atribuir la conversación completa a un intento y con no vinculados como huecos. Transfiere referencias de intento resueltas y procedencia.
- WS33.2: usaría la operación de WS12 y la identidad de WS32 para escribir actor, intento, tarea y resultado aprobar/pedir corrección (con texto). Validaría que completed no se registre como aprobado.
- Conjunto: ambos flujos sobre contrato real; decisión enlazada al mismo intento/tarea, sin duplicados ni atribuciones indebidas. Si falta G_SCION o la operación WS12, se detiene y registra hueco con dueño, sin sustituto.

FUTURO

WS44 produce G_SCION; WS12, el contrato por delta; WS32, la identidad de intento; el receptor P01 registra actas. WS34/WS35 consumen estos registros. La promoción y el TaskDoc fijan archivos, pruebas y textos; este nodo no autoriza dispatch ni escritura Scion.
