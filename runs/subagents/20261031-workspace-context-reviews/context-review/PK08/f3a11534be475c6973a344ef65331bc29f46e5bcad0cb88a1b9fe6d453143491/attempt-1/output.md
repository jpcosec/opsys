REFORMULACION
Propósito: agrupar el ramal E opcional de delegación Scion con intentos, mensajes/decisiones, dispatch/reply autorizado, trazabilidad e intervención humana verificables, sin ejecución propia. Resultado: paquete cuyo valor sustantivo es la cadena inventario→probe→identidad de intento/cierre→vínculo mensajes/decisiones→adaptador→lectura/UI→validación real→capítulo de manual, con cada artefacto enlazado y sin duplicar el pipeline Scion. Repo: deskops (agrupación); hijos en deskops y graph_ui. Límites: no ejecuta, no autoriza tareas ni añade aristas; no hay dispatch sin G_SCION/G_EXEC; ningún permiso de núcleo se convierte en dispatch; operador, acceso y acta son humanos.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético, sin ejecutar: con WS05 y WS07 listos, el solicitante designa operador y registra acceso read-only en autorizaciones/scion.md; WS44 hace probe read-only y produce auditoria/scion-probe.md, satisfaciendo G_SCION. Sin API/acceso, WS44 queda bloqueada y WS32 no arranca. WS32.1/32.2 validan identidad/registro/idempotencia local sin red; WS32 entrega a WS33. WS33.1/33.2 vinculan referencias Hub/conversación/mensaje/intento y decisión humana con dedup/procedencia; entregan a WS34 y WS35. WS34.1/34.2 fijan adaptador dispatch/reply, confirmación, timeout/errores y autoridad, con G_EXEC; alimentan WS36. WS35 lee WS33/WS27 y muestra tarea-intento-conversación-resultado-decisión; alimenta WS36. WS36 invoca solo WS34 y registra decisiones en WS33.2; entrega a WS37. WS37 recorre UF06 real con actor humano y acta en runs/.../delegacion/, sin mocks; con WS31 listo, WS38 publica capítulo en docs/workspace-user-manual.md y átomos vinculados. Validación integrada: existencia y enlace de cada transferencia (probe, manifiesto/RunDoc, dedup, intent/confirmed, permisos, evidencia UI, acta) y aceptación de todos los hijos; no status/hashes ni revisión de comprensión.

FUTURO
Deciden humanos: designación de operador/acceso y su registro; autorización G_EXEC con alcance; acta WS37; aceptación G_HUMAN_DELEGATE. Producen otros nodos: WS05 inventario, WS07 registro, WS12 contrato, WS27 revisión, WS30 validación manual, WS31 manual básico.
