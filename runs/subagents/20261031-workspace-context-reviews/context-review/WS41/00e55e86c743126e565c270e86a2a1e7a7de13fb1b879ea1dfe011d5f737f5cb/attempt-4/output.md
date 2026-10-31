## REFORMULACION

**Propósito:** implementar en `graph_ui` la lectura segura de un segundo desk, resolviendo solo aliases/roots autorizados por el contrato WS11 y usando APIs públicas de los stores.

**Resultado:** una vista que muestra identidad/origen del segundo store, permite seguir enlaces authored del corpus y volver por la historia, con errores visibles ante alias no autorizado, path escapado o store ausente; sin mutaciones cruzadas, sin cambiar el global `SLDB_STORE` y sin afirmar federación por copia.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** no se autorizan roots arbitrarios; no se crean sustitutos si falta contrato, API o corpus; la promoción sigue `not_authorized` y requiere preflight/TaskDoc.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS41 y bloques de contrato WS11, WS13, WS40, WS16 y gate `G_UI_READ`. Sin ejecución.

**Cambios previstos:** ninguno en esta revisión. Al promoverse, WS41 prevé cambios solo en su `output_scope` y pruebas, dentro de `graph_ui`.

**Dependencias:** WS11 debe aportar contrato de resolución repo/store, aliases/roots y el acta de `G_UI_READ`; WS13 aporta el lector de workspace; WS40 aporta el corpus con dos stores y manifiesto; `G_UI_READ` sigue pendiente y es intencional.

**Validaciones futuras:** preflight del TaskDoc con archivos, pills y evidencia; pruebas de identidad/origen, enlaces entre desks, retorno por historia y errores visibles; lectura sobre los dos stores de WS40; validación humana WS16; cierre del gate por WS11.

## FUTURO

- **WS11:** produce el contrato de navegación/identidad y la aceptación `G_UI_READ`; si no hay recepción, el contrato queda pendiente.
- **WS40:** produce el corpus reproducible, manifiesto y segundo desk.
- **WS16:** ejecuta la validación humana de lectura, incluida UF08.
- **Promoción:** fija archivos exactos, escenarios de prueba y textos de pantalla dentro de la aceptación.
- **Humano/WS07:** resuelve P01, P02 y P07 si afectan host, backend o contexto; esta revisión no los aprueba.
