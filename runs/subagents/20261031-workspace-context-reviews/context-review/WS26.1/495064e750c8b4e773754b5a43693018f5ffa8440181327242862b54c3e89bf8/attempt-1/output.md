## REFORMULACION

**Propósito:** implementar autoría explícita desde un candidato del drawer: evidencia declarada, dependencias y binding de contexto/pills, usando solo operaciones autorizadas por el contrato WS12. **Resultado:** UF04 sobre un TaskDoc real, con candidato autorado, evidencia/dependencias/pills vinculadas y visibles tras recargar, sin editar `status` para avanzar. **Repo:** `graph_ui`. **Límites:** `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`; promoción no autorizada; gates pendientes por delta; sin crear endpoints ni contratos.

## AMBIGUEDADES

1. «Autoría explícita desde candidato» y «el candidato queda autorado» frente a brief: «un candidato no es tarea hasta autorarlo con `deskops add task`». Obliga a inventar si autorar crea una tarea activa/enrutada —lo que WS26.2 reserva al enrutamiento— o solo redacta el TaskDoc; también si exige promoción pese a `promotion: not_authorized`.
2. «Si una operación Git no tiene contrato o dueño, la acción queda en handoff explícito y se declara no disponible». No hay operación Git en `scope`, `depends_on` ni `output_scope`. Obliga a inventar qué operación Git forma parte de la autoría, o si la cláusula es inerte; interpretarla como commit contradice P05 («Guardar no hace commit»).

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, nodo WS26.1, vecinos WS12/WS22/WS26/WS26.2 y gates. **Cambios previstos:** archivos bajo `frontends/mindmap/views/workspace/authoring/` y `tests/`; invocaciones a endpoints que fije WS12. Sin commit, sin mutar `status`, sin promoción. **Dependencias:** contrato WS12 por operación; representación Board WS22; G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta. **Validaciones futuras:** UF04 sobre TaskDoc real; evidencia/dependencias/pills visibles tras recarga; ausencia de edición de `status`; handoff ante operación Git sin contrato; preflight de promoción cuando se autorice.

## FUTURO

WS12 produce el contrato técnico por operación y sus recibos; WS22 entrega la representación Board; WS16 produce el acta de G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta. Un humano decide la autorización de promoción y fija en el TaskDoc los archivos, escenarios y textos de pantalla. Nada de esto se ejecuta aquí.
