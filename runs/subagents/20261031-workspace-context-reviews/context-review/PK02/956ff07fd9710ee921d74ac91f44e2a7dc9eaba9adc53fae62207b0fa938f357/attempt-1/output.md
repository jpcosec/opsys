REFORMULACION
Propósito: actuar como checkpoint de revisión que agrupa WS07–WS12 para declarar si sus encargos están revisados. Resultado: PK02 es verdadero solo si cada hijo directo tiene `context_review` vigente —hashes de input y contrato coincidentes, `disposition.md` en el intento correspondiente— sin ambigüedad propia o con bloqueo externo documentado con responsable y dependencia. Repo: deskops (planificación). Límites: no es dependencia operativa ni se ejecuta; no revisa los contratos edge de sus hijos; no resuelve Pxx, gates ni produce entregables.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: `dag.yaml#node:PK02` y sus hijos; `context-review-guide.md`; brief, alcance, decisiones y cobertura; registros de los hijos solo como contratos. Cambios previstos: ninguno; un nodo `aggregate` no se ejecuta. Dependencias: las revisiones de WS07–WS12 y sus `disposition.md`; el comando `python desk/drawer/plans/workspace-documental/context_review.py status`; la coincidencia de hashes. Validaciones futuras: comprobar revisión vigente de cada hijo; admitir `blocked` externo solo con responsable y dependencia registrados; si falta el script o su contrato, detenerse y registrar el hueco conforme a alcance, sin inventar sustituto.

FUTURO
La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos externos con responsable; el humano confirma P01–P09 y los gates G_PRODUCT/G_WRITE_POLICY; los hijos producen sus salidas y revisiones. PK02 termina cuando terminan sus hijos, no por ejecución propia.
