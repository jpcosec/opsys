## REFORMULACION

**Propósito:** encargo de planificación para que WS13.3 sea ejecutable sin inventar: abrir documentos en pestañas y divisiones con historia y foco.
**Resultado:** pestañas documentales, dos documentos lado a lado, alternancia de documento activo, foco por documento e historia de navegación; disposición como estado local de sesión, sin persistir tras recarga.
**Repo dueño:** `graph_ui` (`frontends/mindmap/views/workspace/layout/`, `tests/`).
**Límites:** depende del contrato WS11 y de G_UI_READ por delta; no es documento compartido; no exige índices nuevos; promoción `not_authorized`.

## AMBIGUEDADES

1. «Abrir, cambiar y cerrar pestañas» no define qué documento queda activo ni qué foco se muestra al cerrar la pestaña activa. Obligaría a inventar la regla de sucesión (pestaña vecina, anterior en historia u otra).
2. «Volver restaura documento, foco y origen» junto a «Volver sigue el orden inverso de navegación» no aclara si «volver» es el historial del navegador (`popstate`) o un control propio, ni qué ocurre si la entrada anterior apunta a una pestaña ya cerrada. Obligaría a inventar semántica de historia y su interacción con el cierre.
3. «dos documentos lado a lado» y «abrir dos documentos en divisiones» no fijan si dos es máximo o un mínimo; el título dice «divisiones» sin límite. Obligaría a inventar si se admiten más de dos divisiones simultáneas.

## DRY-RUN

- **Lecturas:** nodo WS13.3, guía, brief, alcance, decisiones, reconciliación, dag (vecinos WS11/WS13.1/WS13 y gate G_UI_READ).
- **Cambios previstos:** ninguno; solo revisión textual, sin ejecución.
- **Dependencias:** contrato de navegación e identidad de WS11; base de lectura WS13.1 (a1b2b22/f16fcd1 reutilizable); acta G_UI_READ por delta.
- **Validaciones futuras:** prueba de abrir/cambiar/cerrar pestañas, dos divisiones, alternancia con foco e historia conservados; verificación de no persistencia tras recarga; recibo del delta en repo receptor.

## FUTURO

El TaskDoc de promoción fijará archivos exactos, pruebas y textos. WS11 producirá el contrato de navegación. El solicitante P01 emitirá el acta G_UI_READ del delta concreto. La decisión de promover WS13.3 corresponde a un humano; este nodo no autoriza ejecución.
