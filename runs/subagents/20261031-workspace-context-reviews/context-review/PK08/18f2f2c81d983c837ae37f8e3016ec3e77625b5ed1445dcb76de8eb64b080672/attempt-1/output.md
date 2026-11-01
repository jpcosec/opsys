## REFORMULACION
Propósito: agrupar, sin ejecución propia, la planificación del ramal Scion opcional para que delegación, registro e intervención tengan identidad, procedencia, permisos y evidencia verificables, sin duplicar el pipeline Scion. Resultado: paquete compuesto por inventario (WS05), probe de acceso (WS44→G_SCION), identidad/cierre (WS32), mensajes/decisiones (WS33), adaptador dispatch/reply (WS34, bajo G_EXEC), trazas UI (WS35), intervención humana (WS36), validación real (WS37) y publicación (WS38). Repo dueño: deskops; entregas UI en graph_ui. Límites: no ejecutar, no autorizar dispatch/Scion, no sustituir contratos faltantes, no convertir permisos de núcleo en dispatch.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Ejecución hipotética por hijos:
1. WS05 lee RunDoc/API pública y emite `auditoria/scion.md`; separa slug/agente/intento/dispatch/mensaje/conversación y capabilities requeridas por WS32/WS33.
2. Tras designación humana de operador/acceso y registro en `autorizaciones/scion.md`, WS44 hace probe read-only y emite `auditoria/scion-probe.md`; solo entonces G_SCION puede satisfacerse. Sin acceso, se detiene.
3. WS32 recibe WS05/WS12 y G_SCION; valida identidad, registro e idempotencia local sin red, y entrega base intento/manifiesto/RunDoc/cierre a WS33.
4. WS33 enlaza Hub/proyecto/conversación/mensaje/intento/decisión, con dedup y procedencia; entrega WS33.1/WS33.2 a WS34/WS35/WS36.
5. WS34 expone adaptador restringido dispatch/reply con confirmación, timeout/errores y autoridad; requiere G_EXEC.
6. WS35 lee WS33 y WS27; muestra tarea-intento-mensaje-resultado-decisión, enlaza fuentes y abre evidencia en el lector.
7. WS36 invoca solo WS34, registra decisiones vía WS33.2 y muestra actor/evidencia; prueba error visible si faltan API/permisos.
8. WS37 ejecuta UF06 real con actor humano, WS36/WS30 y protocolo; registra acta, sin mocks ni `completed`=aprobado.
9. WS38, tras WS37 y manual WS31, publica capítulo con enlaces al acta, átomos y aviso de G_EXEC.

Integración/validación: recorrido único intento→dispatch confirmado→mensaje deduplicado→decisión→traza→evidencia→cierre/handoff, comprobando idempotencia, separación intento/slug, no autoaprobación y bloqueo sin acceso.

## FUTURO
Producen otros/humanos: inventario WS05; designación de operador/acceso y probe WS44; G_SCION; autorización G_EXEC; acta WS37; manual WS31; G_HUMAN_DELEGATE; contratos WS11/WS12; evidencia WS27 y validación WS30. No son ambigüedades de PK08.
