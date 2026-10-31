## REFORMULACION

**Propósito**: integrar en el workspace de `graph_ui` una búsqueda navegable que use la API real de búsqueda (`sldb find` o su ruta en `sldb serve`), sin parser propio, abriendo resultados con su identidad y ruta de origen.

**Resultado**: búsqueda con teclado que conserva consulta y foco al abrir y volver; tres estados diferenciados (sin resultados, error de backend declarado, búsqueda degradada con límite declarado); sin recargar el grafo completo por tecla.

**Repo dueño**: `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/`, `tests/`.

**Límites**: candidato `status: candidate`, `promotion: not_authorized`; depende de WS13 (agregado) y, de forma transitiva, del contrato WS11 (produce `G_UI_READ`, pendiente) y de `auditoria/infraestructura.md` de WS03. Sin ejecución en esta revisión.

## AMBIGUEDADES

1. «Sin resultados/error/degradación diferenciados» (`scope`). Choca con `acceptance`: «se ven como tres estados distintos». El ejecutor no puede saber si el límite prohíbe o exige diferenciarlos; obligaría a inventar cuál de las dos frases prevalece.

2. «no cargar todo grafo en cada tecla» (`acceptance`). No fija umbral ni forma de comprobarlo (debounce, latencia, número de peticiones). Obligaría a inventar el criterio de verificación y el mecanismo.

## DRY-RUN

- **Lecturas previstas**: nodo WS14 en `dag.yaml`, guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y, al promover, `desk/drawer/tasks/workspace-documental/task-ws14.md`.
- **Cambios previstos**: ninguno ahora. En ejecución hipotética, código de búsqueda en `frontends/mindmap/source/` y `views/workspace/`, más pruebas en `tests/`.
- **Dependencias**: WS13 (lector/historia/foco), contrato WS11, `auditoria/infraestructura.md` (WS03), gate `G_UI_READ` (`per_delta`, sin recibos: `accepted_scope_nodes: []`).
- **Validaciones futuras**: recorrido por teclado buscar→abrir→volver con consulta y foco; distinción visual de los tres estados; declaración de capacidad parcial; ausencia de carga completa del grafo por tecla; pruebas con store temporal real.

## FUTURO

- WS11 emite el contrato de navegación y el acta de recepción concreta que satisface `G_UI_READ` para WS14.
- WS03 entrega `auditoria/infraestructura.md` decidiendo canal CLI o `serve`.
- La promoción fija archivos, escenarios de prueba y textos de pantalla en el TaskDoc.
- WS16 ejecuta la validación humana; el responsable de producto acepta el delta en el repo receptor.
- Si falta el contrato o permiso: detenerse y registrar el hueco según `alcance.md`, sin sustituto.
