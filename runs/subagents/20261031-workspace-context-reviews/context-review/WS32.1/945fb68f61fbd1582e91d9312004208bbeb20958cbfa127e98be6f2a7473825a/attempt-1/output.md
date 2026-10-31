REFORMULACION
Propósito: separar la identidad de intento de la de slug y separar dispatch intent/confirmed, refinando un ticket existente sin segundo pipeline. Resultado: cambios en deskops/runtime/scion.py, models/run.py, services/closure.py y tests/; dos intentos del mismo agente y un dispatch fallido con identidades distintas; schema mediante SLDB. Repo dueño: deskops (output_base deskops:repository_root/). Límites: solo delta o ticket existente tras WS06, nunca duplicado paralelo; promoción no autorizada; sujeto a G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «schema mediante SLDB»: no identifica qué schema, qué operación ni quién lo produce/verifica en sldb; output_scope solo enumera archivos de deskops. Obligaría a inventar el cambio de schema y su repo.
2. «dispatch intent y confirmed separados»: no define qué son intent y confirmed (¿estados, registros, payloads?) ni su relación con «intento»; obligaría a inventar el modelo y los campos.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06»: depends_on solo incluye WS05 y WS12; obligaría a inventar si WS06 es prerrequisito ejecutable y cuándo se satisface la condición.
4. «Refinar ticket existente»: no nombra el ticket, su repo ni su estado; obligaría a inventar cuál es y qué partes se reutilizan o sustituyen.

DRY-RUN
Lecturas: nodo WS32.1 y vecinos; brief, alcance, decisiones, cobertura, reconciliación; salidas de WS05 (auditoria/scion.md), WS12 (contratos/operaciones.md), gates y task_file. Cambios previstos: los archivos de output_scope, separando identidad intento/slug y dispatch intent/confirmed, con schema SLDB. Dependencias: WS05, WS12; gates citados; WS06 por integration_mode; ticket existente. Validaciones futuras: prueba de dos intentos y dispatch fallido con identidades distintas; schema SLDB; preflight task-only; no duplicar pipeline.

FUTURO
WS44 produce G_SCION mediante probe y operador designado en WS07. WS12 produce G_WRITE_CONTRACT y whitelist; acepta delta sldb solo con source_mode editable. WS06 propone correspondencias/ticket; WS07 designa actores y el humano resuelve P01/P02 y autoriza promoción. WS32 cierra cuando WS32.1 y WS32.2 cumplen.
