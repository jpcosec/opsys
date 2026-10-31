## REFORMULACION
- **Propósito:** implementar en `graph_ui` la lectura segura de un segundo desk, resolviendo aliases/roots autorizados por el contrato WS11 y usando APIs públicas de store, sin cambiar el global `SLDB_STORE` ni mutar datos.
- **Resultado:** segundo desk legible desde el workspace, con identidad/origen visibles, enlaces authored entre desks navegables, vuelta por historia y errores visibles ante alias no autorizado, path escapado o store ausente.
- **Repo dueño:** `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.
- **Límites:** solo lectura, sin mutaciones cruzadas ni federación por copia; no se aceptan roots/paths arbitrarios; promoción no autorizada.

## AMBIGUEDADES
1. «seguir enlaces authored del corpus entre desks». WS40 es el productor del corpus y de los dos stores, pero su alcance solo menciona Markdown no modelado, Code local, referencia rota y enlaces internos de la entrada mínima; no enumera enlaces authored entre desks. Esto obliga a inventar si WS41 debe crear esos enlaces en `tests/` —invadiendo el corpus— o si WS40 debe ampliarse, y cuál es el enlace exacto que prueba UF08.

## DRY-RUN
- **Lecturas:** nodo WS41, aristas WS13/WS11/WS40, gate `G_UI_READ`, brief, alcance, cobertura, decisiones y guía.
- **Cambios previstos:** resolución explícita de aliases/roots por request; lectura de segundo store vía APIs públicas; vistas en `views/workspace/`; pruebas en `tests/` para dos stores, historia, enlaces y errores de alias/path/store.
- **Dependencias:** WS13 aporta lector, historia y foco; WS11 define identidad, resolución repo/store y modo multidesk read-only; WS40 aporta manifiesto y corpus de dos stores; `G_UI_READ` sigue pendiente y lo resuelve WS11.
- **Validaciones futuras:** WS16 ejecuta UF08 con humano; se comprueba ausencia de mutación/copia y errores visibles. La promoción exige TaskDoc, archivos, pills/átomos y preflight, hoy no autorizados.

## FUTURO
- WS11 debe producir el contrato con aliases/roots autorizados y la aceptación que satisface `G_UI_READ`.
- WS40 debe aclarar o generar los enlaces authored entre desks que consume la aceptación.
- WS07 designa responsables y WS16 realiza la validación humana.
- La promoción y cualquier decisión Pxx pendiente corresponden a autorización humana, no a este nodo.
