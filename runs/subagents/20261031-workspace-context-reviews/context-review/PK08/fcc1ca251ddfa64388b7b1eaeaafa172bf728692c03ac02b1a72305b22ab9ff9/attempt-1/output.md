REFORMULACION
- **Propósito:** revisar PK08 como encargo de revisión del ramal Scion opcional, no como ejecución.
- **Resultado:** PK08 se considera verdadero cuando cada hijo directo —WS32, WS33, WS34, WS35, WS36, WS37, WS38 y WS44— tiene revisión vigente o bloqueo externo explícito con responsable.
- **Repo:** PK08 no declara `owner_repo` porque es agrupación de revisión no operativa; la comprobación se ejecuta desde la raíz de `deskops`.
- **Límites:** no evalúa producto, no ejecuta hijos, no autoriza permisos Scion y no sustituye las revisiones de los hijos.

AMBIGUEDADES
Ninguna. La aceptación define revisión vigente por coincidencia de hashes, `disposition.md` del intento y comprobación con `context_review.py status`; también define el bloqueo externo con responsable.

DRY-RUN
- **Lecturas previstas:** PK08, lista de hijos, estado de revisión de cada hijo, hashes de input/contrato y `disposition.md` del intento correspondiente.
- **Cambios previstos:** ninguno en PK08; no se crea ni modifica `disposition.md` en esta revisión.
- **Dependencias:** vigencia de las revisiones de WS32–WS38 y WS44; bloqueos externos registrados con actor o repo responsable.
- **Validaciones futuras:** ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde `deskops`; verificar coincidencia de hashes; confirmar disposición guardada o bloqueo explícito con responsable.

FUTURO
La sesión de coordinación registra las disposiciones o bloqueos de los hijos. El solicitante designa al operador Scion y registra el acceso read-only de WS44; WS44 produce el probe real, WS37 el acta de delegación y WS38 los capítulos del manual. G_SCION y G_EXEC siguen pendientes y no se infieren de PK08.
