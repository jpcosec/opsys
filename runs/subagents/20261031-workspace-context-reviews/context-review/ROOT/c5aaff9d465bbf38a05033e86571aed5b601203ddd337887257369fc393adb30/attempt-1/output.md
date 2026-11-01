## REFORMULACION
- **Propósito:** agrupar PK01–PK08 para llevar el workspace documental desde auditoría y contratos hasta lector, representaciones, autoría manual, publicación y ramales opcionales.
- **Resultado:** paquete planificado con identidad/origen documental compartidos, APIs y guardas verificables, manual trazado a versión y ausencia de dependencias opcionales sobre el núcleo.
- **Repo:** `deskops`.
- **Límites:** ROOT es agrupación sin ejecución propia; no autoriza tareas, no implementa UI, no hace commits/closeout y no convierte Scion en requisito del núcleo.

## AMBIGUEDADES
Ninguna. El encargo define hijos, orden, transferencias, repo y aceptación comprobable; la “completitud sustantiva” se concreta con las salidas e integración enumeradas.

## DRY-RUN
Hipotético, sin ejecutar:

1. **PK01** produce auditorías y matriz de deltas; alimenta a PK02 y entrega WS05 a PK08.
2. **PK02** consume PK01 y fija decisiones, UFs, vistas y contratos WS11/WS12; habilita navegación y operaciones.
3. **PK03** consume WS11/08 y entrega lector, búsqueda, errores, Taller WS40 y acta WS16.
4. **PK04** consume WS11/40 y WS13/09; produce índices, Board, procedimientos y conocimiento. WS18 es opcional.
5. **PK05** consume WS12 y salidas de PK04; produce contratos/API, intake, trabajo, evidencia, handoff y acta WS30.
6. **PK06** consume WS30/WS17; WS43 publica entradas reales y WS31 integra el manual versionado.
7. **PK07** corre tras sus insumos (WS29: WS15/24; WS39: WS12), sin bloquear el núcleo.
8. **PK08** espera WS05, acceso/permisos reales y manual básico; WS37 valida y WS38 publica el capítulo Scion.

**Integración:** ROOT solo comprueba terminación de hijos y artefactos: identidad/origen, APIs públicas, guardas/canales, manual trazado y ausencia de dependencias opcionales.

## FUTURO
Actas humanas WS16/WS30; publicación WS43/WS31; contratos WS11/12/20/45; acceso, operador y permisos Scion; aceptación WS37/38.
