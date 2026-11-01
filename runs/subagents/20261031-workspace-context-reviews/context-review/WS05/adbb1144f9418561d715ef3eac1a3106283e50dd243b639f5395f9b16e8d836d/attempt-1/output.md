## REFORMULACION
**Propósito:** inventariar la identidad y la API pública de Scion leyendo código y documentación, sin acceso vivo. **Resultado:** `auditoria/scion.md` en el repo `deskops`. **Repo dueño:** deskops; fuentes: deskops y `../scion`. **Límites:** no usar tablas/funciones internas como interfaz; no contactar endpoints vivos, usar credenciales, crear agentes, enviar mensajes ni modificar configuración; puede leer configuración sin secretos y no muestra tokens. WS05 no produce `G_SCION`; solo el probe de WS44 lo evidencia. **Dependencia:** WS01. **Aceptación:** separar slug/agente/intento/dispatch/mensaje/conversación y permisos; señalar campos internos fuera de la API pública y capabilities que requieran API real; marcar las que requieran WS32/WS33.

## AMBIGUEDADES
ninguna

## DRY-RUN
Nodo de planificación ejecutable, no agregado. Un ejecutor futuro verificaría el recibo/hash de WS01, localizaría en deskops y `../scion` el runtime/templates/RunDoc y la API pública documentada o exportada, leería configuración sin copiar secretos y redactaría únicamente `auditoria/scion.md` con entidades, permisos y mapa de capabilities hacia WS32/WS33. Consumiría el brief/glosario de WS01. No consume ni produce gates; `G_SCION` sigue `unverified`. Si no hay API pública documentada/exportada, se detendría y registraría el hueco con repo dueño, sin inspeccionar tablas internas como sustituto; si encuentra tokens, los omitiría. Validación esperada: ausencia de tablas internas como interfaz, separación completa de identidades/permisos, campos internos señalados y capabilities marcadas. La promoción está no autorizada: el TaskDoc fijará archivos exactos.

## FUTURO
WS44 usará el inventario para definir el probe read-only y producir `G_SCION`; el solicitante/operador registrará el acceso. WS32.1/WS32.2 y WS33 consumirán identidad, dispatch, mensajes y decisiones. La promoción y el TaskDoc quedan a cargo de otro nodo o decisión humana.
