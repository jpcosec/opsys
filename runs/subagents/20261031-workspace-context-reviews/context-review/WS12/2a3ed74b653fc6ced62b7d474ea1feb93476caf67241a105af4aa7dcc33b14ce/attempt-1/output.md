REFORMULACION
Propósito: fijar, como encargo de planificación, el contrato de operaciones y la política de escritura del workspace documental a partir de los principios que apruebe WS07. Resultado: `contratos/operaciones.md` con whitelist de lectura/mutación por campo/modelo, capabilities (operación, canal, efectos), clasificación de APIs existentes/comprobadas o faltantes y evidencia para G_WRITE_CONTRACT, G_UI_WRITE y G_SLDB_WRITE. Repo dueño: deskops. Límites: no diseña adapters nuevos ni implementa WS20; registra huecos con repo dueño; closeout fuera del servidor UI; no asume lock UI; no promueve la tarea.

AMBIGUEDADES
1. «Aceptar el delta de escritura … por graph_ui antes de cerrar; aceptar delta en sldb…» No se define qué acto o tarea materializa esa aceptación ni qué ocurre si no llega o se rechaza. Obligaría a inventar el procedimiento de aceptación y su efecto sobre el cierre.
2. «operaciones de autoría/cierre quedan bloqueadas por G_CLOSEOUT»: «autoría» puede referir a autoría de tareas (WS26) o a edición de fuente (WS20/21). Obligaría a decidir qué operaciones bloquea G_CLOSEOUT frente a G_SOURCE.
3. «clasifica APIs como existentes/comprobadas o faltantes»: no fija criterio ni evidencia mínima de «comprobada». Obligaría a inventar el baremo de verificación.

DRY-RUN
Lecturas: brief, alcance, decisiones, cobertura, `dag.yaml`, contratos WS07/WS08/WS11, auditorías de operaciones y modelo TaskDoc. Cambios previstos: redactar `contratos/operaciones.md`, whitelist, tabla de capabilities para los nodos listados, clasificación de APIs y borradores de evidencia de gates; registrar huecos. Dependencias: WS11/WS08, G_WRITE_POLICY, aceptación de graph_ui/sldb, G_CLOSEOUT, G_SOURCE y `source_mode`. Validaciones futuras: revisión por responsables designados, G_WRITE_CONTRACT, coherencia con `scope_nodes`, ausencia de supuestos de lock y no disponibilidad de operaciones sin contrato.

FUTURO
WS07/P01 designará responsables de graph_ui, sldb y operador Scion, y resolverá P03–P06/`source_mode`. WS20 implementará o acreditará raw-source. Los nodos consumidores usarán el contrato; WS16/WS30/WS43 validarán y publicarán. La aprobación humana de gates y la aceptación de deltas no se produce aquí.
