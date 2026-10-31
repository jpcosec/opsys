## REFORMULACION

- **Propósito**: revisar WS19.1 como encargo de planificación, no como implementación ni evaluación de producto.
- **Resultado**: nodo de edición de campos en `graph_ui`, con guardado/recarga verificable, conflicto visible y texto local conservado ante escritura obsoleta.
- **Repo**: `graph_ui`; alcance en `frontends/mindmap/views/workspace/fields/`, endpoints del contrato WS12 sin cambios y `tests/`.
- **Límites**: reutiliza editores/API y revisión esperada por hash CAS del documento; campos workflow-protected no editables; mutación solo en desk con modo manual exclusivo (P03); otros modos read-only. G_HUMAN_READ no bloquea desarrollo/pruebas aisladas de API.

## AMBIGUEDADES

ninguna

## DRY-RUN

- **Lecturas**: nodo WS19.1, guía, `brief.md`, `alcance.md`, `decisiones.md`, `reconciliacion.md` y gates. No revisé los bloques edge de vecinos.
- **Cambios previstos**: ninguno; esta revisión no modifica archivos ni ejecuta comandos.
- **Dependencias**: contrato/whitelist WS12; gates G_UI_WRITE y G_WRITE_CONTRACT por delta; G_HUMAN_READ producido por WS16 para habilitar uso de mutaciones UI; P03.
- **Validaciones futuras**: comprobar endpoint/campos autorizados por WS12; guardar y recargar dato persistido; simular escritura obsoleta y verificar rechazo, conflicto visible y texto local conservado; campos protegidos no editables; restricción de modo; pruebas en `tests/`.

## FUTURO

WS12 debe publicar contrato técnico y whitelist por operación/campo/canal/actor/revisión/efectos. WS16 produce el acta humana de lectura. La promoción fijará archivos, TaskDoc, textos de pantalla y casos concretos. Un humano decide aceptación de producto/delta. Si falta contrato, API, dato o permiso, el ejecutor se detiene y registra el hueco; no crea sustituto.
