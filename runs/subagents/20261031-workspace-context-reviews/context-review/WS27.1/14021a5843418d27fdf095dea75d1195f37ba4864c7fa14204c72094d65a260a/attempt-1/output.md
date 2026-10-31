## REFORMULACION
- **Propósito:** añadir al workspace una vista read-only de diff e historial Git junto a la TaskDoc, usando `TaskDoc.references` y `TaskDoc.files`.
- **Resultado:** diff real e historial acotados a repo/tarea; una sección por repo alcanzado, con root declarado; sin commits, diff working tree→HEAD; ruta sin repo resoluble queda no disponible.
- **Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- **Límites:** no escribir ni revertir; no mostrar integridad del store (WS29); la asociación a intento llega en WS35; `G_UI_READ` es por delta y sigue pendiente; no se ejecuta nada.

## AMBIGUEDADES
1. **Referencias presentes pero no resolubles, o historial filtrado vacío.** Cita: «Historial baseline = commits de TaskDoc.references resolubles y ordenados por fecha de commit, limitados a TaskDoc.files» y «sin commits se declara que no hay historial referenciado». No se define qué mostrar si hay referencias pero ninguna resuelve, o si los commits resueltos no tocan `TaskDoc.files`: ¿se declara “sin historial referenciado”, se muestra sección vacía o se señala referencia inválida? El ejecutor tendría que inventar el estado visible y parte de la aceptación.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; en promoción, modelo TaskDoc, contrato WS11 y whitelist WS12. Sin ejecutar comandos.
- **Cambios previstos:** componentes de diff/historial read-only y pruebas en `graph_uir`; ningún cambio en deskops ni escritura Git.
- **Dependencias:** WS13 (lector/historia/foco) y WS12 (contrato de operaciones/lectura); WS11 transitiva para registry/aliases; `G_UI_READ` por delta.
- **Validaciones futuras:** casos con/sin commits, varios repos, rutas no resolubles, diff real acotado, ausencia de escritura/revert, no mostrar hallazgos WS29 y acta de recepción.

## FUTURO
- **WS35** añadirá la asociación a intento.
- **WS29** aportará integridad del store, fuera de esta vista.
- **WS11** publicará el contrato de rutas/aliases usado aquí.
- **Receptor humano P01** emitirá el acta `G_UI_READ` del delta y decidirá la promoción, hoy `not_authorized`.
