## REFORMULACION
Propósito: auditar el estado actual de graph_ui (Board, tareas, git y código) para mapear cada nodo de este plan que toque graph_ui a una base reutilizada, delta, ticket existente o ausencia explícita, y detectar sesiones y solapamientos sin alterar tareas ajenas. Resultado: `auditoria/ui.md` en deskops, con inventario de tareas externas (path, estado, SHA256, alcance), solapamientos, reconciliación del SPEC externo y tabla de mapeo por nodo graph_ui (ID, clasificación, path/símbolo, commit observado). Repo dueño: deskops; lee graph_ui y el SPEC externo. Límites: no ejecutar producto, no modificar Board/tareas/sesiones, no ampliar aceptación; un commit solo prueba la base citada. Depende de WS01.

## AMBIGUEDADES
1. «Sesión = trabajo en curso observable en Board, git status o paneles herdr.» No define qué es un panel herdr ni cómo acceder; obligaría a inventar el canal de observación o a omitir una fuente exigida para detectar solapamientos.
2. «reconciliar también el SPEC externo (...) con path y hash» frente a «Hash = SHA256 del archivo de tarea»: el hash solo está definido para tareas; para el SPEC obligaría a inventar si es SHA256 del archivo, del commit u otra base.
3. «Cada tarea externa con path, estado observado, hash y alcance» no acota si comprende todas las tareas del Board de graph_ui o solo las relacionadas con nodos del plan; obligaría a inventar el universo inventariable.

## DRY-RUN
Lecturas: `dag.yaml`, `brief.md`, `decisiones.md` y `alcance.md`; Board y archivos de tarea de graph_ui en HEAD 134a665; git status/log y símbolos citados; commits a1b2b22/f16fcd1; SPEC externo. Cambios previstos: crear/actualizar solo `auditoria/ui.md` con inventario, solapamientos, reconciliación del SPEC y tabla por nodo graph_ui, incluyendo ausencias explícitas. Dependencia: consume WS01. Sin gate propio; validación futura por coordinador (hashes, cobertura de nodos, solapamientos, SPEC) y consumo por WS06. Errores: registrar hueco si falta archivo, hash o commit, sin sustituirlo. No se tocan tareas externas.

## FUTURO
El solicitante puede aportar un «encargo» al ejecutar; si no hay, se registra que no hubo. WS06 consume `auditoria/ui.md` para su matriz; la promoción de WS04 sigue no autorizada y requiere preflight de tarea.
