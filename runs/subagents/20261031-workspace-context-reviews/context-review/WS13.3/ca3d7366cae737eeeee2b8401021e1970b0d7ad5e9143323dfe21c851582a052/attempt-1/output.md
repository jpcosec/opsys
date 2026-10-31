## REFORMULACION

**Propósito:** entregar en `graph_ui` la disposición de lectura del workspace —pestañas, dos documentos lado a lado, foco por documento e historia de navegación— como delta o integración conciliada en el ticket workspace draft, respetando rutas y contrato de WS11.

**Resultado:** código y tests en `frontends/mindmap/views/workspace/layout/`, más las rutas de lectura que fije WS11.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura (mutaciones tras WS16); disposición local por sesión, sin persistir tras recarga; depende de WS11 y WS13.1; `G_UI_READ` pendiente; no crea documento compartido ni workspace paralelo; no se ejecuta nada.

## AMBIGUEDADES

1. **Eventos que forman la historia.** Cita: «Cambiar de pestaña o división cambia el documento activo sin alterar el foco guardado de cada documento; volver restaura documento, foco y origen» y «Volver sigue el orden inverso de navegación». No define si cambiar pestaña/división, abrir un documento o seguir un enlace empujan historia; obligaría a inventar qué acciones son navegables.

2. **Efecto de cerrar pestaña.** Cita: «Abrir, cambiar y cerrar pestañas». No indica qué documento queda activo al cerrar la pestaña activa ni si se descartan su foco y su entrada de historia; obligaría a inventar la regla de cierre.

3. **Entrada de apertura y dependencia.** Cita: «Abrir documentos en pestañas y divisiones» con `output_scope` limitado a `layout/`. No nombra desde dónde se abren (enlaces de WS13.1, explorador de WS13.2) ni si WS13.2 es prerrequisito; obligaría a inventar interfaz de apertura o dependencia ausente.

## DRY-RUN

**Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS13.3, contratos vecinos WS11/WS13/WS13.1 y gates.

**Cambios previstos:** ninguno de código; solo este informe.

**Dependencias:** contrato de navegación/foco/historia de WS11; lector de WS13.1; `G_UI_READ` pendiente; matriz WS06 transitiva; acta receptora de `graph_ui`.

**Validaciones futuras:** aceptación por WS16 con corpus WS40; tests en `graph_ui` con store temporal; cierre agregado de WS13 cuando sus hijos cumplan; el TaskDoc de promoción fijará archivos, escenarios y textos.

## FUTURO

WS07 designa responsable de `graph_ui`. WS11 produce contrato y acta `G_UI_READ`, y decide si se integra el ticket draft. WS13.2 puede aportar el explorador como entrada de apertura. WS16 valida lectura. La promoción humana fija TaskDoc, pills y archivos exactos. P07 sigue pendiente, aunque el nodo ya autodefine disposición local.
