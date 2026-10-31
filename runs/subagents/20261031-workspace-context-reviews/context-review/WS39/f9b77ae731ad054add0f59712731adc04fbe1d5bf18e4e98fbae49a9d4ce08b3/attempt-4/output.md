## REFORMULACION

- **Propósito:** planificar la integración navegable de Schema/edición de clases ya existentes desde documento/contexto, usando `draft/validate/promote` de sldb sin reimplementar modelos.
- **Resultado:** nodo `implementation` en `graph_ui` con aceptación UF09 (inspección y mutación en store temporal real), comprobación de efectos/errores del contrato WS12, acta humana y `G_HUMAN_MODEL`.
- **Repo dueño:** `graph_ui`, con `output_scope` en `shell/dialogs.js`, `views/models/`, `tests/` y `runs/subagents/workspace-documental-acceptance/modelos/`.
- **Límites:** no reimplementar modelos; no habilitar promover si falta API/autoridad; extensión posterior al lector básico; promoción no autorizada; depende de WS12/WS16 y de `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`.

## AMBIGUEDADES

1. «G_HUMAN_MODEL debe pasar antes de marcar disponible el capítulo 15 del manual.»  
   No se identifica qué manual, dónde vive ni por qué es el capítulo 15. Obliga a inventar la fuente del manual, su numeración y qué significa «marcar disponible».

2. «Guardar acta de prueba humana [...] con participante designado y resultado»  
   No se nombra quién designa al participante ni qué persona concreta valida. Obliga a inventar el actor y el procedimiento de designación; `P08` sigue pendiente y no lo resuelve.

## DRY-RUN

- **Lecturas:** input completo; nodo WS39 en `dag.yaml`; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, `G_HUMAN_MODEL`; guía; brief; alcance; decisiones; cobertura.
- **Cambios previstos:** ninguno; esta revisión no edita ni ejecuta.
- **Dependencias:** WS12 debe producir contrato/capabilities y aceptar delta en `graph_ui`; WS16 debe producir `G_HUMAN_READ`; sldb debe ofrecer `draft/validate/promote`; store temporal real; corpus WS40 para validación humana.
- **Validaciones futuras:** prueba UF09 de inspección/mutación; comprobar efectos y errores declarados en WS12; acta en `modelos/acta.md`; paso de `G_HUMAN_MODEL`; disponibilidad del capítulo 15 del manual.

## FUTURO

WS12 produce el contrato y registra huecos de API/autoridad. WS16 produce el gate humano de lectura y el recorrido previo. La promoción fijará archivos, pills, textos y escenarios dentro de la aceptación. El humano designado valida y decide; este revisor no aprueba el acta ni resuelve `Pxx`.
