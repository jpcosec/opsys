## REFORMULACION

Propósito: entregar en `graph_ui` la vista de inbox del workspace para leer mensajes entrantes, registrar ack y, solo si el contrato lo permite, responder localmente. Resultado: UI bajo `frontends/mindmap/views/workspace/inbox/` que consume exclusivamente endpoints autorizados por WS12, con ack persistente y sin efectos colaterales de triage. Repo dueño: `graph_ui`; pruebas en `tests/`. Límites: sin envío interdesk; ack ≠ aprobación del trabajo; no crea tarea implícita ni cron; mutaciones en UI sujetas a G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT (desarrollo y pruebas aisladas pueden avanzar con contratos técnicos).

## AMBIGUEDADES

Ninguna. Los condicionales del nodo (respuesta local, endpoints) nombran productor (WS12 y sus contratos por delta) y alcance.md fija la conducta ante contrato ausente.

## DRY-RUN

Lecturas: `dag.yaml` (nodo y arista WS12), `contratos/operaciones.md` de WS12, código existente de `views/workspace`, fixtures de inbox. Verificar en el contrato si existen operaciones de lectura de mensajes, ack y respuesta local; si falta lectura/ack, detenerse y registrar hueco con repo dueño según reglas comunes; si falta respuesta, la UI la declara no disponible.

Cambios previstos: componentes de listado y detalle de mensaje, acción ack, control de respuesta condicionado al contrato; pruebas en `tests/` sobre store temporal real (corpus WS40 si ya existe) que recargan y comprueban persistencia del ack mostrando el mensaje origen, y que no aparece tarea ni cron.

Dependencias y gates: consumo del contrato WS12 para el delta WS25.1 (G_WRITE_CONTRACT con `accepted_scope_nodes` del efecto concreto); recibo per-delta de G_UI_WRITE emitido por P01 en `graph_ui`; G_HUMAN_READ solo se exige para habilitar el uso humano de mutaciones, no para desarrollo/pruebas aisladas. Errores esperados: permiso rechazado visible, fallo de backend en modo degradado declarando el límite, conflicto de escritura reportado sin ocultarlo.

## FUTURO

WS25 cierra como agregado cuando WS25.1 y WS25.2 cumplan su aceptación. P01 receptor emite el acta por delta en `graph_ui`; WS16 produce G_HUMAN_READ; WS40 aporta corpus; WS12 entrega el contrato y declara huecos de API con dueño.
