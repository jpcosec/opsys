REFORMULACION
Propósito: inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, sin confundir tablas/funciones internas con interfaz. Resultado: `auditoria/scion.md` en deskops, con campos internos fuera de la API pública, capacidades que exigen API real y mapeo a WS32/WS33. Repo dueño: deskops; lee también `../scion`. Límites: solo código/documentación; no endpoints vivos, credenciales, agentes, mensajes ni cambios de configuración; puede leer configuración sin secretos y no mostrar tokens; no produce G_SCION.

AMBIGUEDADES
ninguna

DRY-RUN
Un ejecutor futuro leería brief/alcance/decisiones/cobertura, el nodo WS05, su `task_file` y la documentación/SDK exportado de `deskops` y `../scion`. Crearía/actualizaría únicamente `auditoria/scion.md`, con inventario separado, límites público/interno, permisos y capabilities marcadas para WS32/WS33. Consumiría WS01 como prerrequisito; no consumiría G_SCION ni lo emitiría. Si falta documentación/exportación pública, o no puede separar público/interno o permisos, se detendría y registraría el hueco con repo productor, sin contactar endpoints ni inventar sustituto. Validaría que el inventario no use tablas internas como interfaz y que el archivo no contenga tokens.

FUTURO
WS44 realizará el probe read-only y producirá la evidencia de G_SCION cuando un humano designe operador/acceso y se registre en `autorizaciones/scion.md`. WS32.1/WS32.2 usarán el inventario para intento/dispatch y manifiesto; WS33 para mensajes/resultados/decisiones.
