REFORMULACION
Propósito: planificar el workspace documental de Deskops sobre Mindmap/SLDB/Deskops, con lector temprano, autoría/operación manual, manual publicado, extensiones y Scion posterior. Resultado: paquete DAG coherente, con decisiones humanas registradas y contratos por delta, sin implementar. Repo dueño: deskops. Límites: solo planificación; no autoriza tareas, UI, APIs, permisos Scion ni modifica otras sesiones. ROOT es agregado sin ejecución propia.

AMBIGUEDADES
ninguna.

DRY-RUN
ROOT no se ejecuta: termina cuando terminan sus hijos. Hipotéticamente:
1. PK01 audita base con WS01–WS06 y entrega evidencia y matriz de deltas a PK02.
2. PK02 consume esa matriz y las decisiones registradas; WS07–WS12 producen UFs, vistas, convención manual, identidad/navegación y whitelist por delta.
3. PK03 consume WS11/WS08 y WS40; WS13–WS15, WS40, WS41 y WS16 entregan lector, búsqueda, errores, Taller y acta humana temprana.
4. PK04 consume WS11/WS40/WS13/WS09; WS17, WS22, WS23 y WS24 entregan índices, Board, procedimientos y conocimiento; WS18 queda opcional tras su gate.
5. PK05 consume WS12, WS13/WS17 e hijos de autoría; WS19/WS20/WS45/WS21 habilitan fuente editable con guardas, WS25–WS28 intake/trabajo/cierre, WS42 conocimiento y WS30 acta humana.
6. PK06 consume WS30 y WS17; WS43 publica entradas reales y WS31 integra manual versionado.
7. PK07 ejecuta WS29/WS39 como ramas propias. PK08, tras WS05 y G_SCION real, usa WS44 y WS32–WS38 para delegación/intervención.

Integración: actas WS16/30 y publicación WS43/31 validan apertura, edición, evidencia y manual; se comprueban identidad/origen, APIs públicas, guardas/canales y ausencia de dependencias opcionales sobre núcleo. Si falta contrato/API/dato/permiso, se detiene y registra el hueco; no se crea sustituto. Gates pendientes no se satisfacen en el dry-run.

FUTURO
Deciden humanos: actas WS16/30/37 y publicación WS43/31. Otros nodos producen contratos/APIs, G_SOURCE, G_PAYLOAD_PRECONDITION, G_EXEC/G_SCION y recepción técnica por delta. No son ambigüedades de ROOT.
