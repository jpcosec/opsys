**REFORMULACION**

Propósito: revisar si WS19.1 se entiende como encargo de planificación para editar campos en el workspace con conflicto visible, reutilizando editores y API existentes.

Resultado esperado: edición de campos en `frontends/mindmap/views/workspace/fields/` consumiendo los endpoints que fije el contrato WS12, sin cambiarlo; guardado con precondición de escritura de payload (representación fijada por WS12 y verificada por WS45) y rechazo visible conservando el texto local; campos workflow-protected fuera de este canal.

Repo dueño: `graph_ui`, sobre la base integrada a1b2b22. Aceptación: guardar/recargar confirma dato real; escritura obsoleta no pierde texto local y el conflicto se muestra como tal; mutación limitada a desk en “modo manual exclusivo”, otros modos read-only.

Límites: delta sobre workspace existente, no duplicar implementación; no crear semántica de relaciones; G_HUMAN_READ solo habilita uso de mutaciones en UI, no bloquea desarrollo/pruebas aisladas de API.

**AMBIGUEDADES**

1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.» No hay definición de “modo manual exclusivo” ni de qué modos existen. Obligaría a inventar el criterio de detección (¿ausencia de otro coordinador?, ¿configuración?, ¿estado del desk?) y qué hacer en cada modo.

2. «workflow-protected fields no editables por este canal.» La aceptación no incluye comprobar esa restricción; solo exige guardar/recargar y conflicto. Obligaría a inventar el escenario de prueba o a decidir si el requisito queda sin verificación, pese a que WS12 define la whitelist.

**DRY-RUN**

Lecturas: guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, `dag.yaml` (nodo WS19.1, aristas WS12/WS19, gates) y referencia externa `editing`. Cambios previstos del nodo: implementación de edición de campos y pruebas en `graph_ui`, sin cambios de contrato. Dependencias: contrato WS12, G_PAYLOAD_PRECONDITION (WS45), G_HUMAN_READ (WS16), G_UI_WRITE y G_WRITE_CONTRACT por delta. Validaciones futuras: guardar/recargar, rechazo por escritura obsoleta, conservación de texto local, campos protegidos y modo read-only; acta del receptor P01.

**FUTURO**

WS12 fija representación de precondición, operaciones y whitelist; WS45 verifica la precondición; WS16 produce el acta de lectura; el receptor P01 emite el acta G_UI_WRITE del delta; la promoción fija archivos, pills y escenarios; WS06 decide extender el ticket `editing` o crear delta atómico.
