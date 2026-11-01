REFORMULACION
Propósito: implementar en graph_ui la apertura de documentos en pestañas y divisiones, con foco e historia y disposición local. Resultado: UI que abre, cambia y cierra pestañas, muestra dos documentos lado a lado, alterna el activo y vuelve conservando foco e historia; la disposición no es documento compartido ni se exige tras recargar. Repo: graph_ui (`frontends/mindmap/views/workspace/layout/`, rutas de lectura WS11, `tests/`). Límites: depende de WS11 y WS13.1; requiere G_UI_READ por delta; promoción no autorizada.

AMBIGUEDADES
1. «Cambiar de pestaña o división cambia el documento activo...; volver restaura documento, foco y origen» frente a «Volver sigue el orden inverso de navegación.» No se define si cambiar de pestaña/división apila historia ni si la pila es global o por división. Obligaría a inventar qué acciones son «navegación» y qué restaura «volver».
2. «Abrir, cambiar y cerrar pestañas» / «abrir dos documentos en divisiones» no nombra la superficie de selección de documentos; `depends_on` solo incluye WS11 y WS13.1, no WS13.2 (explorador). Obligaría a inventar un selector o a asumir que el catálogo base basta, ampliando o recortando el resultado.

DRY-RUN
Lecturas: nodo WS13.3, referencias WS11/WS13.1, brief, alcance, decisiones, cobertura, reconciliación y external_reference; sin ejecutar. Cambios previstos: estado local de pestañas/divisiones y su integración con rutas de lectura WS11 bajo `views/workspace/layout/`, más tests. Dependencias: contrato WS11, lectura/foco WS13.1, G_UI_READ por delta; la base a1b2b22/f16fcd1/134a665 es solo punto de partida, no aceptación. Validaciones futuras: prueba de abrir/cambiar/cerrar, dos divisiones, alternancia y vuelta con foco e historia; acta de recepción en graph_ui.

FUTURO
WS11 fija identidad, rutas, foco e historia; WS13.1 aporta lectura y foco; WS13.2, si se usa, aporta el explorador. El receptor P01 emite G_UI_READ por delta. La promoción fijará archivos, textos y casos de prueba. Nada autoriza ejecutar.
