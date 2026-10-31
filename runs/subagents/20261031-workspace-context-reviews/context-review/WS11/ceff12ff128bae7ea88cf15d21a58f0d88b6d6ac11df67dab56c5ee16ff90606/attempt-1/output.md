## REFORMULACION
Encargo de planificación para WS11: cerrar en `deskops` el contrato `contratos/navegacion.md` sobre identidad/ruta/modelo de documentos y nodos, resolución repo/store, foco, enlaces/historia y lectura multidesk. Debe clasificar huecos como instancia, vínculo, consulta, API o renderer, y abrir dependencias acotadas si falta API. Límites: no implementar UI, no migrar a Kimun, no modificar repos receptores; requiere G_PRODUCT y depende de WS08/WS09. La aceptación exige actas de graph_ui y spec2viz; sin recepción, el contrato queda pendiente.

## AMBIGUEDADES
1. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk.» No se indica quién autoriza aliases/roots multidesk, dónde se declaran ni qué formato tienen. Obligaría a inventar la fuente de autorización y su responsable, afectando a WS41.
2. «Clasificar huecos sin modelos hipotéticos.» No hay criterio para decidir qué modelo es hipotético, pese a que el glosario admite modelo opcional y nodos no Markdown. Obligaría a inventar el límite entre hueco real y modelo supuesto.
3. «El acta de G_UI_READ enumera sus scope_nodes […] el acta de G_SPEC_VIEW enumera los suyos», pero `output_scope` solo nombra `contratos/navegacion.md`. Obligaría a inventar ubicación y formato de ambas actas o a decidir si van dentro del contrato.

## DRY-RUN
Lecturas previstas: brief, alcance, decisiones, cobertura, nodo WS11 y gates. Cambios previstos: redactar `contratos/navegacion.md`; clasificar cada hueco; registrar dependencias acotadas por API faltante; preparar evidencia de aceptación para G_UI_READ y G_SPEC_VIEW. Dependencias: salidas de WS08/WS09; designaciones humanas de WS07 vía G_PRODUCT; aceptación de responsables graph_ui/spec2viz. Validaciones futuras: revisar que cada hueco tenga clasificación y dueño; comprobar que las actas enumeran los `scope_nodes`; no publicar como cerrado sin recepción; verificar ausencia de migración Kimun implícita.

## FUTURO
WS07 debe registrar decisiones humanas y designar responsables por repo. Los responsables de graph_ui y spec2viz aceptan o rechazan los deltas; sin aceptación, WS11 no cierra. WS12, WS40, WS41 y los nodos de lectura consumirán el contrato. La resolución de P01/P07 y demás propuestas corresponde al solicitante humano, no a este nodo.
