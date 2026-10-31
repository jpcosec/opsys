## REFORMULACION

**Propósito:** PK05 es una agrupación de revisión del bloque de autoría y operación manual; no es entregable ni se ejecuta. Agrupa WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30 y WS42.

**Resultado:** PK05 será verdadero cuando cada hijo directo tenga `context_review` vigente —hash de input y contrato coincidentes con los actuales y `disposition.md` guardada en su intento— o un bloqueo explícito registrado por el coordinador con responsable y dependencia. La comprobación indicada es `python desk/drawer/plans/workspace-documental/context_review.py status`.

**Repo:** no aplica. Es agrupación de revisión sin `owner_repo` por diseño; no produce código ni artefacto propio.

**Límites:** no ejecuta hijos, no implementa, no sustituye sus revisiones y no resuelve decisiones Pxx.

## AMBIGUEDADES

1. **Contradicción entre bloqueo aceptable y ambigüedad bloqueada.** El input dice: «sin ambigüedad de encargo o bloqueo explícito con responsable» y luego: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera.» No queda claro si un hijo bloqueado por ambigüedad no resuelta satisface PK05 por ser «bloqueo explícito» o la invalida por ser «ambigüedad sin resolver». Para decidirlo habría que inventar si «bloqueo explícito» cubre solo bloqueos por dependencia externa o también bloqueos por ambigüedad; el nodo no distingue ambos casos.

## DRY-RUN

- **Lecturas:** `dag.yaml` (PK05 y bloques de hijos), guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.
- **Cambios previstos:** ninguno de código; esta revisión solo produciría la `disposition.md` de PK05.
- **Dependencias:** revisiones vigentes de WS19, WS20, WS21, WS25, WS26, WS27, WS28, WS30 y WS42. WS30 depende además de WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28 y WS42; WS42 de WS19, WS24 y WS12. PK05 no declara `depends_on` directo.
- **Validaciones futuras:** ejecutar `context_review.py status`; confirmar hashes y `disposition.md` por hijo; verificar registro de bloqueos por el coordinador; contrastar que ningún hijo tenga ambigüedad sin resolver.

## FUTURO

Producen otros nodos: las revisiones e `disposition.md` de cada hijo; WS12, el contrato de operaciones; WS30, la validación humana; WS40, el corpus. Decide un humano: P04 `source_mode`, y las demás Pxx aplicables. El coordinador registra bloqueos con responsable y dependencia. No son ambigüedades de PK05.
