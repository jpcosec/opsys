REFORMULACION
WS33 es un agregado no ejecutable de deskops: encargo de vincular referencias Hub/proyecto/conversación/mensaje/intento y registrar la decisión humana explícita, con deduplicación y procedencia, como backend documental independiente del editor UI. Su resultado son las salidas de WS33.1 y WS33.2; termina cuando ambos hijos cumplen su aceptación. Límites: no tocar tablas Scion, no dispatch/reply ni UI, y queda sujeto a G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
Ninguna.

DRY-RUN
No ejecutable: un ejecutor futuro no corre WS33, recorre sus hijos.
- WS33.1 lee el contrato público de Scion (G_SCION, vía WS44), la identidad de intento de WS32 y el contrato de navegación de WS11; produciría adaptador en runtime/, modelos/reportes y tests. Transfiere a WS33.2 y WS35 referencias mensaje/resultado por intento, con clave Hub+proyecto+conversación+mensaje y hueco de procedencia para lo no vinculable.
- WS33.2 consume WS33.1 y la operación que fije WS12; registra actor, intento, tarea y resultado aprobar/pedir corrección con su texto. Transfiere la decisión asociada al intento.
Validación conjunta: importación repetida no duplica ni atribuye una conversación completa; mensajes sin intento quedan como hueco; la decisión incluye actor, intento, tarea y resultado explícito; completed nunca equivale a aprobado. Si falta contrato o API, se detiene y registra el hueco con repo dueño, sin sustituto. G_SCION y G_WRITE_CONTRACT pueden estar pendientes; no bloquean revisar el encargo.

FUTURO
WS44 resuelve G_SCION; WS12 produce G_WRITE_CONTRACT por delta; WS34 consume WS33 para dispatch/reply y WS35 para mostrar trazabilidad; la recepción humana valida el conjunto.
