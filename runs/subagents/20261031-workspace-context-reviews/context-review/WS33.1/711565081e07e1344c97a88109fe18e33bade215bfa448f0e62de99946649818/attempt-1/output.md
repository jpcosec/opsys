## REFORMULACION
Revisar si WS33.1 se entiende como encargo de planificación: vincular mensajes/resultados a un intento con deduplicación y procedencia, en el repo `deskops`, sin ejecutar ni revisar los nodos vecinos. Límites: no validar el producto, no dar por aprobadas las Pxx y no tratar `G_SCION` como satisfecho.

## AMBIGUEDADES
1. «Referencias Hub/proyecto/conversación/mensaje/intento y resultados, con deduplicación y procedencia». No define la clave de deduplicación. Obliga a inventar qué combinación identifica un registro y qué constituye duplicado; la aceptación solo exige que «una importación repetida no duplica», sin fijar el criterio.
2. «una importación repetida no duplica ni atribuye una conversación completa a un intento». No define «conversación completa» ni «resultados». Obliga a inventar si se refiere a todos los mensajes, a un rango o a otro artefacto, y qué resultado cuenta como vinculable; sin ello la aceptación no es plenamente comprobable.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación y contratos de vecinos WS32/WS33/WS33.2/WS11 y gate `G_SCION`. Cambios previstos: ninguno; solo revisión. Dependencias declaradas: WS32 (identidad de intento), WS11 (contrato de navegación/identidad) y `G_SCION` (unverified; resolver WS44). Validaciones futuras: comprobar que WS32 produce identidad de intento, que WS11 aporta referencias/resolución y que el probe de WS44 existe; verificar que la deduplicación y la no atribución se puedan probar con un caso repetido.

## FUTURO
WS44 produce el probe de `G_SCION`; WS07 designa al operador Scion; WS32 y WS11 producen sus contratos; la promoción de WS33.1 queda a decisión de otro nodo o humano.
