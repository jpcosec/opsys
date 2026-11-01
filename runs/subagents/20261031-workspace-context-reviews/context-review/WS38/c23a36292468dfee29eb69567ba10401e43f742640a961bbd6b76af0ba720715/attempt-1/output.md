REFORMULACION
Propósito: publicar en el manual los capítulos verificados de delegación y revisión trazable, tal como quedaron demostrados en WS37. Resultado: `docs/workspace-user-manual.md` ampliado y átomos de `desk/atoms/` vinculados. Repo dueño: `deskops`. Límites: se apoya en el acta de WS37 y en el manual/átomos de WS31; debe documentar fallos registrados e indicar que `G_EXEC` es necesario para operar; no atomiza permisos de una sola sesión; la promoción sigue `not_authorized`.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: acta de WS37 y evidencia de `G_HUMAN_DELEGATE`; manual y átomos de WS31; `decisiones.md` y contratos citados para etiquetas. Cambios previstos: añadir al manual la operación de delegación y revisión trazable; remitir cada paso al acta y a operaciones reales; documentar los fallos del acta; señalar la necesidad de `G_EXEC`; buscar átomos existentes por regla, enlazar/actualizar el equivalente o crear uno solo si no existe, y verificar enlaces átomo→documento. Dependencias: WS37 debe aportar acta y resolver `G_HUMAN_DELEGATE`; WS31 aporta manual base y átomos. Validaciones futuras: que cada paso sea trazable al acta/operaciones, que los acuerdos durables tengan átomo vinculado, que los fallos aparezcan y que la nota sobre `G_EXEC` esté presente. Si falta el acta o el gate, detenerse y registrar el hueco sin crear sustituto. No se ejecuta nada.

FUTURO
WS37 produce el acta y el estado de `G_HUMAN_DELEGATE`; WS31 produce el manual y los átomos base; el humano resuelve `G_EXEC` y la aprobación de delegación. La promoción fijará archivos, pills y evidencia exactos dentro de la aceptación.
