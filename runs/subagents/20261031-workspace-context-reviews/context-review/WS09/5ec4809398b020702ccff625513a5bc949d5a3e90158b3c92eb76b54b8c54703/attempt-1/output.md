## REFORMULACION
**Propósito:** precisar el catálogo inicial de renderizaciones de `vistas.md` como encargo de planificación. **Resultado:** cada fila con origen, contrato o «sin contrato», renderer, acción/dueño, error, estado y clasificación authored/derivado/preferencia local; además, ficha completa por fila. **Repo:** `deskops`. **Límites:** no implementar UI ni código; ViewDoc es solo grafo, no contrato universal de UI; no inventar disponibilidad, errores ni contratos. Depende de WS07, WS10 y WS08; `G_PRODUCT` ya está registrado.

## AMBIGUEDADES
1. «Cada fila tiene origen, contrato (o «sin contrato» si el soporte no lo tiene), renderer, acción/dueño, error y estado». Las tablas solo ofrecen «Operaciones / navegación» o «Acciones/dueño» de forma parcial, sin actor/repo dueño por acción. Obliga a inventar quién posee operaciones como enrutar, ack o editar.
2. «Cada fila tiene … renderer» frente a «Para propuesto/bloqueado indicar error esperado condicionado a contrato/implementación, o no definido con productor WS11/12 si falta». Solo el error admite «no definido»; el renderer no. Para filas propuestas/bloqueadas sin renderer existente, obliga a inventar uno o a declararlo sin contrato.
3. «Aplica a cada fila de las tablas de vistas.md y completa la ficha por fila». La ficha incluye «campos y relaciones usados» y «aceptación mediante user-flow», pero el input no define fuente ni productor por fila para esos campos. Obliga a inventar modelo de campos o aceptación de flujo.

## DRY-RUN
**Lecturas previstas:** guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vistas.md` y nodo WS09; auditorías citadas vía dependencias, sin ejecutar. **Cambios previstos:** editar únicamente `borradores/vistas.md` para completar filas y fichas; ningún archivo de código. **Dependencias:** WS10 para disponible/propuesto/bloqueado; WS08 para user-flows; WS07 para decisiones; WS04/auditoría UI para disponibilidad actual; WS11/12 como productores de contratos o errores faltantes. **Validaciones futuras:** comprobar que toda fila tenga los campos exigidos, que los estados usen WS10, que no haya errores actuales inventados, que ViewDoc no se trate como contrato universal y que la promoción fije archivos, pills y evidencia en TaskDoc.

## FUTURO
WS10 decide las definiciones de estado; WS08 aporta user-flows; WS04 aporta disponibilidad actual; WS11/12 producen contratos o errores no definidos. El humano responsable y la promoción autorizan TaskDoc/preflight. WS11 consume el catálogo; WS18 solo usa la selección mínima si existe.
