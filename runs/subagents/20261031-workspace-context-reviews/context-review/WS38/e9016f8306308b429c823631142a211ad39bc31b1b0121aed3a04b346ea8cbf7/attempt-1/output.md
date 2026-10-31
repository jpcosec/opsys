## REFORMULACION

**Propósito:** publicar en el manual las operaciones de delegación y revisión trazable ya validadas en WS37.

**Resultado:** capítulo(s) de delegación en `docs/workspace-user-manual.md`, con pasos que remiten al acta de WS37, fallos documentados, nota de que G_EXEC es necesario para operar y átomos durables vinculados en `desk/atoms/`.

**Repo:** `deskops` (output_base `deskops:repository_root/`).

**Límites:** no ejecutar delegación ni sustituir el acta; no atomizar permisos de una sola sesión; buscar primero átomos de WS31 y crear solo si no existe regla equivalente; promoción no autorizada.

## AMBIGUEDADES

Ninguna. El nodo nombra repo, resultado, aceptación comprobable y límites. El acta y el gate G_HUMAN_DELEGATE tienen productor explícito (WS37) y ruta de evidencia; G_EXEC tiene productor externo y ruta declarada. La definición de acuerdo durable y la regla de búsqueda/creación de átomos están fijadas en la aceptación. Los detalles de archivos exactos, pills y pruebas quedan delegados a la promoción.

## DRY-RUN

**Lecturas previstas:** nodo WS38 y gates en `dag.yaml`; nodos vecinos WS37 y WS31; `context-review-guide.md`; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `borradores/manual.md`.

**Cambios previstos:** actualizar la sección de delegación en `docs/workspace-user-manual.md`; enlazar o crear átomos en `desk/atoms/` según reglas durables de WS37; posiblemente incorporar referencias en `docs/assets/workspace-user-manual/`.

**Dependencias:** acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; gate G_HUMAN_DELEGATE resuelto por WS37; manual y átomos de WS31; G_EXEC externo solo citado como requisito operativo.

**Validaciones futuras:** cada paso cita el acta de WS37 y operaciones reales; cada acuerdo durable tiene átomo vinculado y fuente; fallos del acta documentados; se indica G_EXEC; links resolubles y etiquetas coherentes con actas/commits.

## FUTURO

WS37 debe producir el acta y resolver G_HUMAN_DELEGATE. Un humano debe autorizar G_EXEC mediante `autorizaciones/scion.md`. La promoción fijará archivos, pills, átomos y pruebas exactas. WS38 no ejecuta la delegación ni crea permisos.
