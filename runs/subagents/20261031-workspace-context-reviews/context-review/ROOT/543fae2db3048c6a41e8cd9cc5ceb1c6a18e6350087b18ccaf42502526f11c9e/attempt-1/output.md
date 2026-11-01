**REFORMULACION**  
ROOT es un paquete agregado de planificación, no ejecutable, cuyo propósito es cubrir el workspace documental de Deskops sobre Mindmap/SLDB/Deskops: lector temprano, autoría/operación manual, manual publicado, extensiones independientes y Scion opcional. El resultado esperado es un conjunto integrado de auditorías, decisiones/contratos, lector validado, representaciones navegables, autoría segura con evidencia, publicación real y ramales separados con pruebas propias. Repo dueño: deskops. Límites: no implementa ni aprueba UI/APIs/Scion; extras no bloquean núcleo; revisiones de comprensión no equivalen a producto entregado.

**AMBIGUEDADES**  
ninguna.

**DRY-RUN**  
Hipotéticamente, ROOT termina cuando terminan sus hijos; no se ejecuta por sí mismo. PK01 recibe WS01 y produce auditorías WS02–04, inventario WS05 y matriz de deltas WS06; esa evidencia pasa a PK02. PK02 reutiliza decisiones con WS07 y produce UFs WS08, convención manual WS10, catálogo de vistas WS09 y contratos WS11/WS12; estos alimentan PK03–PK05. PK03 ejecuta lector WS13–15 con WS11/08, crea Taller WS40, añade multidesk WS41 y valida con acta WS16; entrega lector y mediciones a PK04–PK06. PK04 consume WS11/40 para índices WS17 y WS13/09 para Board WS22, procedimientos WS23 y conocimiento WS24; WS18 es opcional y no bloquea. PK05 sigue el orden declarado: WS12→WS19/20/45/21, WS25, WS27, WS26, WS42, WS28 y WS30; entrega autoría probada, evidencia y acta manual. PK06 usa WS17/30 en WS43 y WS10/30/43 en WS31; entrega entradas reales y manual versionado. PK07 prueba Changes/modelos por separado; PK08, tras WS05/WS44 y permisos, prueba Scion. Validación conjunta: actas WS16/30, publicación WS43/31, identidad/origen, guardas/canales y manual trazado, sin dependencias opcionales sobre núcleo.

**FUTURO**  
Producen otros nodos: WS16/30 actas, WS43/31 publicación, WS44 gate Scion, WS45 precondición. Deciden humanos: aceptación de deltas, acta WS37 y operador/acceso Scion; el TaskDoc de promoción fija archivos y pruebas.
