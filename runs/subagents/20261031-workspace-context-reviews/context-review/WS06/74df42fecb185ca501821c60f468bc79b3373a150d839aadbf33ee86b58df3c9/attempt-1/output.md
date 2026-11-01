REFORMULACION

WS06 es una entrega documental de planificación —no un agregado— en deskops: traducir las auditorías WS02–WS04 a una matriz única en `reconciliacion.md`, agrupada por repo dueño (graph_ui, sldb, spec2viz, deskops), clasificando cada delta o capacidad como ya cubierto, extender ticket existente o nuevo delta, con path/símbolo, commit observado, ticket/delta destino, responsable P01 y límites de evidencia. Debe añadir la atomización propuesta y cubrir los 64 nodos. Límites: no ejecuta WS05, no notifica, despacha ni modifica el Board de graph_ui, no crea gates ni recepción ficticia; «no designado en P01» para deskops es un dato, no un bloqueo.

AMBIGUEDADES

ninguna.

DRY-RUN

Un ejecutor futuro leería brief, alcance, decisiones, cobertura, `dag.yaml`, las tres auditorías y el Board, tickets y commits citados en graph_ui. Volcaría en `reconciliacion.md` una fila por capacidad o delta único —no por nodo— con las columnas anteriores; agruparía por repo dueño; remitiría los agregados por sus hijos; preservaría la fila Scion y su descomposición WS32/33 sin ejecutar WS05; añadiría la atomización y la tabla de cobertura de los 64 nodos. No tocaría otros archivos ni el Board. Dependencias: consume WS02–WS04. Si un path, ticket o commit no fuera accesible, marcaría «no comprobado» con causa, sin sustituirlo ni inventar capacidad. Validaría que cada delta tenga una sola fila, cada nodo esté mapeado, cada fila indique ticket/delta destino y responsable P01 o «no designado», y que no haya firmas, gates ni recepción ficticia. Error esperable: solapamiento de tickets o código observado sin dueño; se registraría como límite, no se resolvería inventando.

FUTURO

WS07 reutiliza la matriz para el registro de decisiones; WS11 y WS12 la usan como fuente de contrato para navegación y operaciones; el receptor P01 produce el acta por delta en su repo y un humano decide la recepción. La promoción sigue no autorizada. WS05 puede inventariar Scion después sin alterar la clasificación conservada.
