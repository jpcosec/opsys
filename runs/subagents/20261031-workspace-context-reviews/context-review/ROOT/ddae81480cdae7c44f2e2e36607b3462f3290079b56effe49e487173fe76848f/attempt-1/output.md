## REFORMULACION
**Propósito:** revisar ROOT como encargo de planificación agregado, no como ejecución. **Resultado sustantivo:** un paquete planificado que integra auditoría/base, contratos, lector, representaciones, autoría/operación manual, publicación de manual/entradas y ramales independientes (Changes/modelos y Scion), con evidencias y actas humanas previstas. **Repo dueño:** deskops. **Límites:** ROOT no ejecuta tareas, no autoriza implementación, API, uso ni Scion; solo agrupa hijos y describe transferencias. La completitud depende de salidas de PK01–PK08, no de un gate de comprensión.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Ejecución hipotética, sin ejecutar:
1. **PK01** audita Deskops, infraestructura, UI y Scion; produce matriz de capacidades/deltas y evidencia por repo. Alimenta PK02 y ramales.
2. **PK02** reutiliza decisiones registradas y evidencia PK01; produce UFs, vistas, contratos WS11/WS12 y convención manual. Alimenta PK03–PK05 y PK07/PK08.
3. **PK03** implementa lector/búsqueda/errores con WS13–WS16, WS40/WS41; entrega lector probado, Taller y acta WS16. Alimenta PK04–PK06.
4. **PK04** produce índices, Board, procedimientos y conocimiento con WS17/22/23/24; WS18 queda opcional. Valida apertura de mismos soportes sin escritura desde renderer.
5. **PK05** usa WS12 y entradas WS17 para autoría, intake, tareas, evidencia y handoff; entrega API/guardas probadas y acta WS30.
6. **PK06** publica WS43 con acta WS30 e índices WS17; WS31 integra WS10/30/43 en manual versionado.
7. **PK07** ejecuta WS29/WS39 en paralelo posterior, con pruebas propias.
8. **PK08** solo con acceso/operador y G_SCION: WS44 habilita, WS32–WS36 implementan, WS37/38 validan y publican.

**Integración futura:** comprobar identidad/origen compartidos, APIs públicas, guardas/canales, actas y mediciones P08, manual trazado y ausencia de dependencias opcionales sobre el núcleo.

## FUTURO
Producen otro nodo: actas WS16/30/37, G_SOURCE, G_SCION, contratos técnicos por delta, publicación WS43/31 y recibos en repos dueños. Decide el humano: aceptación de deltas y uso del Taller; no es ambigüedad de ROOT.
