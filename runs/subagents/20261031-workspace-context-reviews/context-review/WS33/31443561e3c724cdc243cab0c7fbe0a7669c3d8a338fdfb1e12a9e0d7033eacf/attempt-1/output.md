## REFORMULACION
Propósito: comprobar que WS33, tal como está escrito, es un encargo de planificación entendible y no una tarea ejecutable. Resultado: un agregado (`node_role: aggregate`) que agrupa WS33.1 (vincular mensajes/resultados al intento) y WS33.2 (registrar decisión humana), sin ejecución propia; se cierra cuando ambos hijos cumplen su aceptación. Repo dueño: `deskops`. Límites: backend documental, independiente del editor UI; no toca tablas Scion; no hace dispatch/reply; `promotion: not_authorized`; depende de WS32, WS11 y sus hijos, con `G_SCION` pendiente (producido por WS44) como bloqueo intencional, no defecto.

## AMBIGUEDADES
1. Dependencia WS11 sin artefacto declarado. Cita: «depends_on: - WS32 - WS11» junto a «Referencias Hub/proyecto/conversación/mensaje/intento». Obliga a inventar qué salida de WS11 (contrato de navegación/identidad, orientado a graph_ui) consume este backend, o si la arista sobra.
2. Gate de escritura ausente. Cita: «Este nodo solo escribe la decisión por la operación que fije el contrato WS12» frente a «requires: - G_SCION». Obliga a decidir si registrar una decisión corresponde a un delta de escritura que exige `G_WRITE_CONTRACT` (presente en WS32/WS34) o si `G_SCION` basta, sin poder deducirlo del input.

## DRY-RUN
Lecturas previstas: `task-ws33.md` (task_file), contratos WS12 y WS11, resultados de WS32.1/32.2 y de los hijos, matriz de promoción WS06 y `reconciliacion.md`, estado del Board en deskops. Cambios previstos: ninguno de código; solo cierre del agregado cuando los hijos cierren, sin editar `dag.yaml` salvo corrección de las ambigüedades. Dependencias: WS32, WS11, WS33.1, WS33.2 y `G_SCION` sin verificar. Validaciones futuras: aceptación de cada hijo, evidencia del gate en `auditoria/scion-probe.md`, ausencia de ticket duplicado y revisión de solapamiento con `scion`.

## FUTURO
WS34/WS35 consumen este ID; WS44 produce `G_SCION`; P01 registra actas por delta; WS06/WS07 verifican promoción. Ninguna ejecución autorizada.
