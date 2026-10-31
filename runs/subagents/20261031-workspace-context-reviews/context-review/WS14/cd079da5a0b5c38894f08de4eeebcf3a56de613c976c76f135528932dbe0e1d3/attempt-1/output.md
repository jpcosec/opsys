## REFORMULACION

**Propósito:** integrar en el lector del workspace una búsqueda navegable sobre la API real de SLDB, sin parser propio ni duplicar el grafo.

**Resultado:** búsqueda por texto/campos/semántica según capacidad real; resultados que abren el documento con identidad y ruta de origen; estados distintos de sin resultados, error y degradación; consulta y foco conservados al volver; sin carga completa del grafo por tecla.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** no implementar búsqueda semántica inexistente, no crear parser alternativo, no prometer cobertura total si la API es parcial. Promoción aún no autorizada; gate `G_UI_READ` es por delta.

## AMBIGUEDADES

Ninguna.

Las referencias a `auditoria/infraestructura.md` de WS03 y al contrato WS11 tienen productor nombrado; el comportamiento ante contrato ausente lo resuelve `alcance.md`. La elección entre `sldb find` y su ruta en `sldb serve` queda determinada por esa auditoría. El mecanismo de debounce/umbral se delega explícitamente al TaskDoc. `G_UI_READ` pendiente es intencional y per_delta. No se detecta resultado indefinido, aceptación no comprobable, actor/repo ausente ni límite que permita exceder alcance.

## DRY-RUN

**Lecturas previstas:** nodo WS14 en `dag.yaml`; `context-review-guide.md`; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `reconciliacion.md`; en ejecución futura, auditoría WS03 y contrato WS11.

**Cambios previstos:** componente de búsqueda en workspace, presentación de resultados, tres estados diferenciados, manejo de teclado para buscar/abrir/volver, pruebas de peticiones y de interacción. Archivos exactos y textos de pantalla quedan para el TaskDoc de promoción.

**Dependencias:** WS13 para lector, apertura, historia y foco; WS11 como contrato de navegación/búsqueda; WS03 para decidir canal `find`/`serve`; `G_UI_READ` como recibo por delta.

**Validaciones futuras:** prueba de que teclear no dispara carga completa del grafo; recorrido con teclado conservando consulta y foco; verificación separada de sin resultados, error de backend y degradación parcial; revisión humana en WS16, no sustituible por agente.

## FUTURO

WS03 debe producir la auditoría que fije el canal real de búsqueda. WS11 debe entregar el contrato de navegación aplicable. El receptor humano de `graph_ui` debe emitir el acta `G_UI_READ` del delta concreto. El TaskDoc de promoción fijará archivos, pruebas y textos. WS16 validará el recorrido con una persona real. Nada de esto se ejecuta en esta revisión.
