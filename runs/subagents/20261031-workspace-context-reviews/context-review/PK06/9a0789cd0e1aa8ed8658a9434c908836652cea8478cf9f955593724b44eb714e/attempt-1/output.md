## REFORMULACION

Propósito: revisar si PK06 está bien planteado como **encargo de planificación** (agrupación de revisión, no tarea ejecutable). Resultado: veredicto sobre claridad de propósito, resultado, repo, límites, dependencias y aceptación comprobable. Repo: deskops (nodo aggregate, sin `owner_repo` propio). Límites: no evalúa producto, no ejecuta nada, no revisa los bloques edge de WS31/WS43 como tareas, no trata Pxx como aprobadas.

## AMBIGUEDADES

1. **“hash de input y de contrato”** — cita: «cuyo hash de input y de contrato coinciden con los actuales». No se define qué constituye el “contrato” cuyo hash se compara (¿bloque edge del hijo?, ¿TaskDoc?, ¿parámetros?). El ejecutor de la comprobación tendría que inventar el objeto hasheado; sin embargo, el propio input indica que `context_review.py status` lo comprueba, por lo que la invención queda delegada a la herramienta. No obliga a inventar al revisor de PK06.

Ninguna otra: hijos enumerados (WS31, WS43), criterio de verdadero/falso y tratamiento de bloqueo externo con responsable están definidos; el aggregate no requiere repo ni aceptación de producto propia.

## DRY-RUN

- **Lecturas previstas:** `dag.yaml` (PK06, hijos WS31/WS43); disposition.md de cada hijo en su intento correspondiente; salida de `context_review.py status`.
- **Cambios previstos:** ninguno; PK06 no se ejecuta ni produce artefactos.
- **Dependencias:** revisiones vigentes de WS31 y WS43; herramienta de estado; hashes actuales de input/contrato.
- **Validaciones futuras:** ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; comprobar coincidencia de hashes, existencia de disposition.md y, si hay bloqueo, responsable y dependencia registrados.

## FUTURO

La sesión de coordinación ejecuta el comando de estado y registra bloqueos externos; los humanos resuelven Pxx y gates (G_PRODUCT, G_HUMAN_MANUAL, G_WRITE_CONTRACT); la promoción fija TaskDoc y archivos. Nada de eso corresponde a PK06.
