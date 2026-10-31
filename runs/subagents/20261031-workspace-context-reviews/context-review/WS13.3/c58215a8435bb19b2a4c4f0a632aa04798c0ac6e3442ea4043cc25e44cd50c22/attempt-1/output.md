## REFORMULACION

- **Propósito**: planificar la apertura de documentos en pestañas y divisiones con foco e historia de navegación en el workspace.
- **Resultado**: delta de UI en `frontends/mindmap/views/workspace/layout/`, con rutas de lectura del contrato WS11 y pruebas.
- **Repo dueño**: `graph_ui`.
- **Límites**: disposición como estado local por sesión de navegador, sin persistencia exigida tras recargar; foco por documento; no duplicar el ticket workspace; depende de WS11 y WS13.1; gate `G_UI_READ` pendiente es intencional; no ejecución.

## AMBIGUEDADES

1. «Abrir, cambiar y cerrar pestañas» — no se define qué documento queda activo al cerrar la pestaña activa ni cómo se ajustan foco e historia. Obliga a inventar la semántica de cierre.
2. «Volver restaura documento, foco y origen. Volver sigue el orden inverso de navegación.» — no se especifica qué acciones crean entrada de historia (cambio de pestaña, apertura en división, seguir enlace) ni cómo tratar duplicados. Obliga a inventar el modelo de historia.
3. «Pestañas, dos documentos lado a lado» y «abrir dos documentos en divisiones» — no se fija si el máximo son dos divisiones o si pueden abrirse más. Obliga a inventar el límite de disposición.
4. «Disposición por sesión de navegador; no se exige persistir tras recargar.» — no aclara si el estado es en memoria o en almacenamiento de sesión, que sí sobrevive a recarga. Obliga a inventar la implementación del estado local.

## DRY-RUN

- **Lecturas**: nodo WS13.3, contratos vecinos WS11/WS13.1, guide, brief, alcance, decisiones, cobertura, reconciliación.
- **Cambios previstos**: ninguno; esta revisión no modifica archivos.
- **Dependencias**: contrato de navegación WS11, lectura en WS13.1 y acta `G_UI_READ` (pendiente).
- **Validaciones futuras**: contraste de aceptación con el contrato WS11; verificación del acta y no solapamiento antes de despachar; TaskDoc de promoción fijará archivos y casos de prueba.

## FUTURO

- WS11 produce `contratos/navegacion.md` y el acta `G_UI_READ`.
- WS07/solicitante designa al responsable de `graph_ui`; sin designación el gate sigue pendiente.
- La promoción autorizada genera TaskDoc y preflight.
- WS13 cierra cuando cierren sus hijos; sus dependientes esperan a WS13.
