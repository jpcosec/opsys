## REFORMULACION

**Propósito:** revisar si WS29, tal como está escrito, se entiende como encargo de planificación viable y comprobable.

**Resultado:** un delta sobre la tarea Changes actual de `graph_ui` que muestre impacto comprobable de una mutación en store temporal: documento afectado, relaciones a 1 hop y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, con enlace a reparación manual documentada.

**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad del contrato WS11 y `tests/`.

**Límites:** sin CST ni árbol Kimun supuesto; no repara automáticamente; no bloquea lector/manual básico. Depende de WS15 y WS24; `G_UI_READ` sigue pendiente de forma intencional.

## AMBIGUEDADES

1. **Canal de obtención de hallazgos no definido.** Cita: «stores check/doctor/drift y relaciones comprobadas; errores = hallazgos de esos tres comandos». Obligaría a inventar si la vista ejecuta los comandos, consume una API o solo lee resultados ya producidos; la aceptación solo exige enlazar al comando documentado para reparar.

2. **Atribución y filtro de errores al documento afectado.** Cita: «muestra documento afectado, relaciones alcanzadas [...] y errores» junto a «agrupados por comando». Obligaría a inventar si se muestran todos los hallazgos de los tres comandos o solo los atribuibles al documento y relaciones alcanzadas.

## DRY-RUN

- **Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS29 y contratos vecinos WS15/WS24/gates. Sin ejecutar comandos ni abrir repos.
- **Cambios previstos:** ninguno; esta revisión no edita `dag.yaml` ni TaskDoc.
- **Dependencias:** WS15 (errores/degradado), WS24 (grafo/backlinks), `G_UI_READ` resuelto por WS11, contratos WS11/WS12 transitivos, comandos sldb/deskops y decisiones P02/P03.
- **Validaciones futuras:** mutación en store temporal; relaciones entrantes/salientes a 1 hop vía API de grafo de sldb; hallazgos de los tres comandos; enlaces a documentación del repo dueño; ausencia de CST/Kimun; prueba propia WS29 y diagnóstico WS16.

## FUTURO

WS11 produce el acta `G_UI_READ` y las rutas de integridad; WS07 designa al responsable de `graph_ui`; las personas resuelven P01–P05; WS12 fija la política de escritura; el TaskDoc de promoción concreta archivos, escenarios y textos; WS16 valida diagnóstico; WS30 aplica aceptación; WS06 aporta la matriz de solapamiento.
