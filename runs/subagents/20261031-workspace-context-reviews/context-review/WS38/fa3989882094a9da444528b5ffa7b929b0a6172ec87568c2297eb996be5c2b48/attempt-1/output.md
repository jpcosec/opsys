## REFORMULACION
WS38 es un nodo de documentación cuyo propósito es añadir al manual la operación de delegación y la revisión trazable tal como quedaron demostradas en WS37. El resultado esperado son capítulos en `docs/workspace-user-manual.md` y átomos vinculados en `desk/atoms/`; el repo dueño es `deskops`. Límites: solo puede documentar lo que recoja el acta de WS37 y operaciones reales; debe registrar los fallos de esa acta e indicar que `G_EXEC` es necesario para operar; no debe atomizar permisos de una sola sesión ni autorizar ejecución. Depende de WS37 y WS31, y requiere `G_HUMAN_DELEGATE`.

## AMBIGUEDADES
Ninguna. El nodo nombra la fuente (acta de WS37), el manual base (WS31), el repo y los criterios de aceptación. La búsqueda de átomos existentes por regla está acotada por la definición de acuerdo durable y por la convención atom→doc de WS31.

## DRY-RUN
Un ejecutor futuro leería el acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`, el manual publicado por WS31 y los átomos existentes en `deskops:desk/atoms/` para localizar reglas equivalentes. Después añadiría al manual los pasos de delegación, intervención, corrección, evidencia y decisión demostrados, citando cada uno al acta; documentaría los fallos registrados; señalaría que operar requiere `G_EXEC`; y enlazaría o actualizaría átomos para acuerdos durables, creando uno solo si no existe regla equivalente. Consumiría `G_HUMAN_DELEGATE` como gate resuelto por WS37; sin acta o sin gate, se detendría y registraría el hueco, sin crear sustituto. Validaría que los enlaces resuelven, que cada paso remite al acta, que los fallos aparecen, que los átomos están vinculados y que no se atomizaron permisos de sesión.

## FUTURO
WS37 produce el acta y resuelve `G_HUMAN_DELEGATE`; un humano la acepta. `G_EXEC` lo autoriza un actor externo. La promoción de WS38 fijará archivos, pills y evidencia en su TaskDoc; un tester independiente verificará los criterios antes del cierre.
