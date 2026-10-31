REFORMULACION
Propósito: integrar en graph_ui la inspección y edición de los modelos ya existentes, reutilizando Schema/editar clases y draft/validate/promote de sldb, sin reimplementar modelos.
Resultado: superficies navegables desde documento/contexto, mutación probada en store temporal real, acta humana en graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md, G_HUMAN_MODEL y habilitación del capítulo 15 del manual solo tras el gate.
Repo: graph_ui (output_scope y output_base).
Límites: no reimplementar modelos; no habilitar promote si falta API/autoridad; promoción no autorizada; extensión posterior al lector básico; sujeto a WS12/WS16 y a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «Hacer navegables Schema/editar clases ya disponibles desde documento/contexto». «Contexto» no está definido en el glosario ni se concreta si son dos entradas —documento y contexto— o una; obligaría a inventar el punto de entrada y qué superficie existente se reutiliza.

DRY-RUN
Lecturas: input completo, guía, brief, alcance, decisiones, cobertura, nodo WS39 y contratos vecinos WS12/WS16/gates.
Cambios previstos: ninguno; esta revisión no edita, promueve ni ejecuta.
Dependencias: contrato/whitelist de WS12 (G_UI_WRITE, G_WRITE_CONTRACT), G_HUMAN_READ de WS16, participante P08 y reglas de alcance para store temporal/corpus.
Validaciones futuras: prueba de inspección/mutación en store temporal; efectos y errores según WS12; acta humana con participante y resultado; G_HUMAN_MODEL antes de marcar disponible el capítulo 15; bloqueo de promote si falta API/autoridad.

FUTURO
WS12 produce whitelist, canal/efectos y gates G_UI_WRITE/G_WRITE_CONTRACT; WS16 produce G_HUMAN_READ; WS07/humano resuelve P01/P04/P08 y designa participantes; WS31 publica el manual; WS40 aporta corpus; el humano firma acta y G_HUMAN_MODEL; la promoción de task_file requiere autorización humana.
