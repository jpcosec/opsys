REFORMULACION
WS33 es un nodo **agregado no ejecutable**: agrupa WS33.1 (vincular mensajes/resultados al intento con dedup y procedencia) y WS33.2 (registrar decisión humana explícita). Su propósito es que mensajes, resultados y decisiones queden referidos a un intento y, por él, a su tarea. El resultado es la suma de las salidas de sus hijos, no una entrega propia. Repo dueño: deskops. Límites: backend documental sin editor UI; no despacha ni responde (WS34), no muestra en workspace (WS35), no toca tablas Scion, no escribe estados de validación/cierre y no sustituye el contrato WS12 ni la prueba de G_SCION.

AMBIGUEDADES
Ninguna. La aceptación agregada delega explícitamente en sus hijos («se cumple cuando todos sus hijos cumplen su aceptación»), y el alcance propio solo enumera los efectos ya asignados a WS33.1/WS33.2. No hay resultado indefinido ni límite que obligue al ejecutor de WS33 a inventar, porque WS33 no se ejecuta.

DRY-RUN
No aplica ejecución directa. Hipotéticamente:
- WS33.1 lee el contrato público de Scion (WS05/WS44) y la identidad de intento de WS32; produce vínculos Hub+proyecto+conversación+mensaje y Hub+proyecto+intento+fuente, con dedup, y deja mensajes sin intento resoluble como hueco de procedencia. Transfiere a WS33.2 la referencia de intento y los huecos.
- WS33.2 consume esa referencia, más el actor y la operación que fije WS12; escribe la decisión (aprobar o pedir corrección, esta con texto) vinculada a intento y tarea, sin convertir `completed` en aprobado.
- Dependencias y gates: WS32, WS11, WS12; G_SCION vía WS44 y G_WRITE_CONTRACT por delta. Si falta contrato, API o permiso, se detiene y registra el hueco, sin sustituto.
- Validación conjunta: importación repetida sin duplicados ni atribución de conversación completa (WS33.1); decisión con actor, intento, tarea y resultado explícito (WS33.2). WS33 queda cumplido solo con ambas aceptaciones.

FUTURO
WS44 produce G_SCION; WS12, G_WRITE_CONTRACT; WS34 usa WS33 para dispatch/reply; WS35 muestra la trazabilidad; WS37 valida con agente real. La designación del operador Scion corresponde a un humano al abordar el ramal E.
