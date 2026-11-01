## REFORMULACION
WS38 es un nodo de documentación en `deskops` cuyo propósito es publicar en `docs/workspace-user-manual.md` el capítulo de operación de delegación y revisión trazable tal como quedó demostrado en WS37, dejando átomos vinculados en `desk/atoms/`. El resultado es manual actualizado más acuerdos durables atomizados. Límites: usar solo el acta de WS37; no atomizar permisos de una sola sesión; no inventar autorizaciones Scion; indicar que G_EXEC es necesario para operar; no promocionar sin TaskDoc/preflight.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS38, WS37, WS31, gates), `brief.md`, `alcance.md`, `decisiones.md`, el manual base de WS31 y el acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; comprobaría que WS31 publicó el manual y que G_HUMAN_DELEGATE está resuelto.

Cambios previstos: añadir al manual el capítulo de delegación con pasos que enlacen el acta y operaciones reales; documentar los fallos registrados en el acta; incluir la nota de que G_EXEC es necesario para operar. En átomos: buscar los existentes de WS31 por regla durable, enlazar o actualizar el equivalente y crear solo si no existe; verificar la relación átomo→documento.

Dependencias consumidas: WS31 (manual base), WS37 (acta y gate G_HUMAN_DELEGATE); G_EXEC solo se menciona como requisito operativo. Validaciones futuras: enlaces resolubles al acta, cada paso con operación real, fallos cubiertos, átomos vinculados, etiquetas coherentes y ausencia de permisos de sesión atomizados. Ante acta, manual o gate ausentes: detenerse y registrar el hueco con repo dueño, sin crear sustituto.

## FUTURO
WS38 produce el capítulo verificado y los átomos vinculados; otra revisión humana o nodo posterior valida el manual publicado y sus enlaces.
