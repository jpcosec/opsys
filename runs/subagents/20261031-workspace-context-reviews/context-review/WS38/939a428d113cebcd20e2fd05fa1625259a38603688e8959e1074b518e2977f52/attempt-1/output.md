## REFORMULACION
**Propósito:** publicar en el manual de usuario la operación de delegación y la revisión trazable tal como quedaron demostradas en WS37.

**Resultado:** `docs/workspace-user-manual.md` actualizado con pasos que remiten al acta de WS37 y a operaciones reales; fallos registrados en esa acta documentados; nota de que G_EXEC es necesario para operar; acuerdos durables respaldados por átomos vinculados en `desk/atoms/`.

**Repo dueño:** deskops.

**Límites:** solo lo demostrado en WS37; no atomizar permisos de una sola sesión; reutilizar/actualizar átomos equivalentes de WS31 antes de crear otros; depende de WS37 y WS31; requiere G_HUMAN_DELEGATE; no autoriza promoción ni ejecución.

## AMBIGUEDADES
ninguna

## DRY-RUN
Nodo documental ejecutable, no agregado.

1. **Lecturas:** acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; manual base y átomos producidos por WS31; contratos/decisiones ya citados por WS31 si aplican. Verificar que G_HUMAN_DELEGATE tenga evidencia de WS37 y que existan los átomos de WS31.
2. **Cambios previstos:** editar `docs/workspace-user-manual.md` para incorporar delegación y revisión trazable; cada paso con referencia al acta y a la operación real; documentar los fallos del acta; indicar G_EXEC como requisito operativo. En `desk/atoms/`, buscar átomos de WS31 por regla durable; enlazar/actualizar el equivalente o crear uno solo si no existe; no crear átomos de permisos de sesión.
3. **Dependencias y gates:** consumir WS37 (acta y G_HUMAN_DELEGATE) y WS31 (manual y átomos). Si falta el acta, el gate o el manual base, detenerse y registrar el hueco con repo dueño, sin sustituto.
4. **Validación esperada:** enlaces resolubles; cada paso cita acta y operación; fallos documentados; nota G_EXEC presente; átomos vinculados con relación atom→doc; ningún átomo de permiso puntual; cambios limitados al `output_scope`.

## FUTURO
WS37 produce el acta y resuelve G_HUMAN_DELEGATE. WS31 produce el manual base y los átomos de partida. La promoción de WS38 y el commit/cierre por el canal Deskops autorizado quedan fuera de este nodo; G_EXEC sigue siendo una autorización externa para operar, no para publicar el capítulo.
