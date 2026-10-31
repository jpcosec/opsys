## REFORMULACION
**Propósito:** declarar proyecciones de grafo reutilizables —ViewDoc y NotationDoc— para selecciones y notación ya soportadas, sin crear páginas de UI declarativas ficticias.
**Resultado:** una vista portable que renderiza sobre un store real la selección declarada, coincide con ella y queda documentada por el ViewDoc; incluye tests.
**Repo dueño:** spec2viz. **Límites:** no modificar ese repo desde este plan; promover tareas receptoras mediante su dueño; gate G_SPEC_VIEW requerido; `promotion: not_authorized`; depende de WS09 y WS11.

## AMBIGUEDADES
1. **«ViewDoc/NotationDoc para selecciones y notación ya soportadas»** (dag.yaml#node:WS18, scope).
   Las fuentes suministradas definen «Proyección de grafo ViewDoc» en el glosario, pero no definen **NotationDoc**: ni su contrato, ni su formato, ni si es un entregable separado de ViewDoc. El ejecutor tendría que inventar qué artefacto declarar y con qué contenido, y la aceptación no permite comprobar ese objeto por separado.

## DRY-RUN
- **Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura y nodo WS18; aristas WS09/WS11/WS24 leídas solo como contratos de vecinos, sin revisarlas.
- **Cambios previstos:** ninguno ejecutado. Al promoverse: declarar ViewDoc/NotationDoc y tests bajo `sldb/views/` y `tests/`, con rutas confirmadas por el dueño de spec2viz.
- **Dependencias:** inventario de renderizaciones de WS09; contrato de navegación/identidad y acta G_SPEC_VIEW de WS11. WS24 consume estas proyecciones.
- **Validaciones futuras:** render sobre store real, coincidencia con la selección declarada, documentación de lo seleccionado en ViewDoc, evidencia del gate y promoción por el dueño receptor.

## FUTURO
- WS07 debe designar explícitamente al responsable de spec2viz y al operador Scion; P01 sigue pendiente.
- WS11 produce el contrato y la evidencia de G_SPEC_VIEW.
- El dueño de spec2viz promueve las tareas receptoras y confirma rutas/no solapamiento.
- WS24 integra la navegación de grafo local una vez disponibles las proyecciones.
