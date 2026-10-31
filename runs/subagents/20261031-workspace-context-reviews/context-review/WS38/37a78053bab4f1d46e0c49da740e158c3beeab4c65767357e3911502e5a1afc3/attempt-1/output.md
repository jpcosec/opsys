## REFORMULACION
Encargo de documentación: añadir a `docs/workspace-user-manual.md` la operación de delegación y la revisión trazable tal como quedaron en WS37, con pasos que remiten al acta, fallos documentados y átomos vinculados por acuerdo durable. Repo dueño: `deskops`. Límites: solo ese manual y `desk/atoms/ vinculados`; depende de WS37 y WS31; requiere `G_HUMAN_DELEGATE`; no ejecuta Scion ni crea permisos; `G_EXEC` solo se declara necesario para operar.

## AMBIGUEDADES
1. «cada acuerdo durable deja su átomo vinculado»: no define qué es un «acuerdo durable» ni si debe crear un átomo nuevo o enlazar uno existente de WS31, que ya atomiza Pxx/contratos. Obligaría a inventar el criterio de clasificación, la granularidad y la deduplicación entre WS31 y WS38.

## DRY-RUN
Lecturas previstas: `dag.yaml`, acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`, manual base de WS31, `decisiones.md`, `alcance.md` y átomos existentes. Cambios previstos: editar los capítulos de delegación/revisión en `docs/workspace-user-manual.md`; crear o enlazar átomos en `desk/atoms/`. Dependencias: WS31 y WS37; `G_HUMAN_DELEGATE`; `G_EXEC` externo pendiente, solo se documenta. Validaciones futuras: cada paso enlaza al acta; se citan operaciones reales; se documentan los fallos del acta; átomos vinculados; nota de `G_EXEC`; enlaces y etiquetas. Sin ejecutar.

## FUTURO
WS37 produce el acta y `G_HUMAN_DELEGATE`; WS31 produce el manual base; un humano o externo resuelve `G_EXEC`; la promoción de WS38 —no autorizada— fijará archivos, pills y evidencia; la aceptación humana decidirá sobre el resultado.
