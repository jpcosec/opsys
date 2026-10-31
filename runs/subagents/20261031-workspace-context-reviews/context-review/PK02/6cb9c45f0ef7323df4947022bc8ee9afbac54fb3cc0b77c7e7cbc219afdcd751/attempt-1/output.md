## REFORMULACION
Propósito: revisar PK02 como agrupación de revisión de decisiones/contratos, no como tarea ejecutable. Resultado: PK02 es verdadero cuando cada hijo directo (WS07–WS12) tiene `context_review` vigente —hash de input y contrato actuales y `disposition.md` en el intento correspondiente— o bloqueo externo explícito con responsable y dependencia registrados. Repo dueño: `deskops`. Límites: no es dependencia operativa; no reviso contratos de nodos vecinos; no ejecuto; no autorizo implementación, API, uso ni permisos Scion; no sustituyo actas ni recibos.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas previstas: PK02 y sus hijos en `dag.yaml`; guía, brief, alcance, decisiones y cobertura; `disposition.md` de cada intento; hashes actuales; salida de `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`. Cambios previstos: ninguno en el plan, repos o hijos. Dependencias: WS07–WS12, herramienta `context_review`, disposiciones por intento y hashes coincidentes. Validaciones futuras: comprobar el estado de cada hijo; aceptar revisión vigente o bloqueo externo con responsable/dependencia; que ningún `pending`/`blocked` por ambigüedad propia del hijo cuente; no ejecutar ahora.

## FUTURO
La sesión de coordinación ejecutará `status` y registrará bloqueos externos con responsable y dependencia en `disposition.md`. Las revisiones de WS07–WS12 producirán sus disposiciones; sus autores resolverán ambigüedades propias. La persona responsable de producto/recepción decide aceptaciones por delta, no PK02. Si falta revisión, PK02 no será verdadero.
