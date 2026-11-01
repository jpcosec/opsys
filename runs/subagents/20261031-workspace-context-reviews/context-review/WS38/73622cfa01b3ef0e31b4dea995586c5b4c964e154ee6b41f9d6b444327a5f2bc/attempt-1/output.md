## REFORMULACION
Propósito: publicar en el manual la operación de delegación y revisión trazable demostrada en WS37. Resultado: capítulo en `docs/workspace-user-manual.md` y átomos durables vinculados en `desk/atoms/`. Repo dueño: `deskops`. Límites: solo documentación; depende de WS37 y WS31; requiere `G_HUMAN_DELEGATE`; `G_EXEC` solo debe mencionarse como necesario para operar. Promoción no autorizada.

## AMBIGUEDADES
Ninguna. El acta de WS37 y `G_HUMAN_DELEGATE` están pendientes, pero tienen productor, resolver y ruta declarados. `G_EXEC` es un límite externo explícito, no una invención del ejecutor.

## DRY-RUN
Lecturas previstas: nodo WS38, guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, borrador de manual, bordes WS37/WS31 y gates.  
Cambios previstos: añadir el capítulo de delegación al manual; enlazar o crear átomos durables según la regla de WS38; documentar los fallos registrados en el acta de WS37.  
Dependencias: acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; manual y átomos de WS31; `G_HUMAN_DELEGATE`. `G_EXEC` se cita, no se satisface aquí.  
Validaciones futuras: cada paso remite al acta y a operaciones reales; cada acuerdo durable tiene átomo vinculado; fallos documentados; mención de `G_EXEC`; enlaces, etiquetas y relación átomo→documento verificables; Tester independiente antes del cierre. Sin ejecutar.

## FUTURO
WS37 produce el acta y resuelve `G_HUMAN_DELEGATE`. El solicitante o designee emite `G_EXEC` por canal externo. WS31 entrega manual y átomos base. La promoción y el TaskDoc fijarán archivos exactos, pills, átomos y evidencia, con preflight task-only; un humano autoriza la promoción y un Tester/validador comprueba la aceptación.
