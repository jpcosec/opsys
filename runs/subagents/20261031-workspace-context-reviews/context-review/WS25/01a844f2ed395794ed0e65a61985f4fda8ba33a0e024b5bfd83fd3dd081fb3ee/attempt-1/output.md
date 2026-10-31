## REFORMULACION

Propósito: revisar si WS25, «Integrar captura y triage en UI», está bien formulado como encargo de planificación. Resultado esperado: veredicto sobre propósito, resultado, repo dueño y límites del nodo, no sobre el producto. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: WS25 es `node_role: aggregate`; no se ejecuta, «se cumple cuando todos sus hijos cumplen su aceptación». Alcance acotado a mensaje/ack y captura interna de drawer/protoátomo «mediante operaciones permitidas por contrato; no confundir ack con aprobación». No se revisan los bloques edge de vecinos ni se ejecuta nada.

## AMBIGUEDADES

Ninguna. Lo comprobado:

- Resultado definido: `output_scope: 'Agregado: salidas de WS25.1, WS25.2'`, con dos hijos (`Leer inbox y registrar ack o respuesta local`, `Capturar en drawer o protoátomo`) que cubren el alcance del agregado.
- Aceptación comprobable: agregado no ejecutable, resuelto por aceptación de cada hijo.
- Repo y actor presentes: `owner_repo: graph_ui`.
- Dependencias coherentes: WS12 (contrato de operaciones) y WS16 (validación humana de lectura); los hijos como cierre del agregado.
- Gates explícitos y pendientes: `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.
- Límite claro: ack no equivale a aprobación; respuesta solo si el contrato WS12 la define.

No se computan como ambigüedad las Pxx pendientes ni los detalles que fijará el TaskDoc de promoción.

## DRY-RUN

Lecturas: únicamente el input suministrado (guía, brief, alcance, decisiones, cobertura, fragmentos de `dag.yaml`). Sin herramientas ni historial.

Cambios previstos: ninguno; solo el veredicto de revisión.

Dependencias observadas: WS25.1, WS25.2, WS12, WS16; gates G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT, todos `pending`. `promotion: not_authorized`.

Validaciones futuras (no ejecutadas): aceptación de cada hijo; persistencia de ack y captura tras recargar con origen tipado; aplicación de permisos del contrato; verificación agregada en WS30 (UF02); comprobación de no solapamiento y task receptora para `G_UI_WRITE`.

## FUTURO

- WS12 produce la whitelist y el canal; sin ella, respuesta local y captura quedan «no disponible».
- WS16 produce `G_HUMAN_READ` con acta humana.
- El responsable designado en P01 acepta el delta de `graph_ui` (`G_UI_WRITE`).
- Un humano autoriza la promoción y el TaskDoc fija archivos, pruebas y textos.
- WS30 valida el recorrido manual completo; observaciones abren tarea en el nodo causante.
