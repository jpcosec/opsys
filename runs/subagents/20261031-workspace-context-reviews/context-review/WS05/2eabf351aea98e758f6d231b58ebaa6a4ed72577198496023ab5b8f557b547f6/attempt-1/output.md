REFORMULACION  
WS05 es una auditoría de planificación en `deskops`: inventariar la identidad y la API pública de Scion, leyendo código/documentación de `deskops` y `../scion`, incluido `runtime/templates/RunDoc`. Debe separar slug, agente, intento, dispatch, mensaje, conversación y permisos (roles/scopes/operaciones) y dejar como resultado `auditoria/scion.md`. Límites: no usa endpoints vivos ni credenciales, no crea agentes, no envía mensajes, no modifica configuración y no muestra tokens. No produce `G_SCION`; solo WS44 puede aportar evidencia con probe real. Aceptación: no tratar tablas internas como interfaz, señalar campos internos fuera de la API pública y capacidades que exijan API real, y marcar qué capabilities requieren WS32 y WS33.

AMBIGUEDADES  
ninguna

DRY-RUN  
Un ejecutor futuro leería el brief/glosario de WS01, el código y documentación de `deskops` y `../scion`, `runtime/templates/RunDoc`, endpoints/SDK documentados o exportados y configuración sin secretos. Crearía únicamente `desk/drawer/plans/workspace-documental/auditoria/scion.md`, con secciones para identidades, permisos, API pública, campos internos excluidos, capabilities y su dependencia de WS32/WS33. Consumiría WS01 como contexto; no consumiría `G_SCION` ni ningún gate, y no ejecutaría probe ni red. Si falta la API pública, la documentación, el repo `../scion` o el artefacto RunDoc, se detendría, registraría el hueco con repo dueño y marcaría la capability como no disponible, sin sustituirla por tablas internas. Validaría después que cada concepto esté separado, que los permisos citen API pública, que los campos internos estén señalados, que las capabilities tengan destino WS32/WS33 y que no aparezcan tokens ni secretos.

FUTURO  
WS44 realizará el probe read-only y producirá `G_SCION`; un humano designará operador y registrará su acceso. WS32/WS32.1/WS32.2 usarán el inventario para identidad de intento, dispatch y manifiesto; WS33 para mensajes, resultados y decisiones. La promoción fijará archivos, pills y TaskDoc; no se autoriza implementación ni uso de Scion desde WS05.
