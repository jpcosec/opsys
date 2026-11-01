## REFORMULACION

**Propósito:** entregar UI para leer mensajes del inbox y registrar ack o respuesta local usando solo operaciones autorizadas por el contrato WS12.

**Resultado:** vista en `frontends/mindmap/views/workspace/inbox/` con ack persistente tras recarga, respuesta condicionada al contrato y pruebas en `tests/`.

**Repo:** `graph_ui` (`output_base: graph_ui:repository_root/`), nodo de implementación hijo de WS25.

**Límites:** sin envío interdesk; ack no equivale a aprobación; no crea tarea implícita ni cron de triage; no define endpoints fuera de WS12; las mutaciones en UI quedan sujetas a gates pendientes.

## AMBIGUEDADES

Ninguna. La respuesta local condicionada nombra productor (WS12) y conducta si falta (declararla no disponible); el contrato ausente se rige por las Reglas comunes de ejecución. Los gates pendientes son intencionales y la aceptación es comprobable.

## DRY-RUN

**Lecturas previstas:** contrato WS12 y su whitelist por operación, `dag.yaml`, fixture/corpus de inbox y pruebas existentes de la vista. No se ejecuta nada.

**Cambios previstos:** crear archivos UI dentro de `output_scope` y pruebas; ningún cambio en deskops ni en otros nodos.

**Dependencias:** WS12 (contrato técnico por delta); gates `G_HUMAN_READ` (resuelve WS16), `G_UI_WRITE` (acta P01 por delta concreto) y `G_WRITE_CONTRACT` (WS12).

**Validaciones futuras:** ack visible tras recarga mostrando el mensaje origen; respuesta local solo si WS12 define la operación, o declaración explícita de no disponible; ausencia de tarea implícita y cron; permisos del contrato aplicados; pruebas aisladas de API pueden avanzar sin acta humana de lectura.

## FUTURO

WS12 debe publicar operación, canal, campos, actor, revisión, efectos y errores del ack y, si existe, de la respuesta local. El receptor P01 emite el acta del delta en `graph_ui`; WS16 produce el acta de lectura; la promoción fijará archivos, textos de pantalla, escenarios y evidencia dentro de esta aceptación. Nada de ello es ambigüedad del nodo.
