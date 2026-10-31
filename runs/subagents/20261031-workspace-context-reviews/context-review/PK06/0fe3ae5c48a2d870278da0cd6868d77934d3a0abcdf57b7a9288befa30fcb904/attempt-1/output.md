## REFORMULACION
**Propósito:** revisar PK06 como agrupación de revisión del plan, no como tarea ejecutable. **Resultado:** PK06 es verdadero cuando cada hijo directo —WS31 y WS43— tiene revisión vigente sin ambigüedad de su propio encargo o un bloqueo externo explícito con responsable. **Repo:** PK06 no declara `owner_repo` porque es agrupación; sus hijos pertenecen a `deskops`. **Límites:** no es dependencia operativa ni entregable; no se ejecuta, no produce cambios y no revisa los contratos de las aristas. La comprobación corresponde a `python desk/drawer/plans/workspace-documental/context_review.py status`; no se deben aprobar Pxx, satisfacer gates ni alterar estados por inferencia.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** nodo PK06 y sus hijos WS31/WS43 en `dag.yaml`; guía de revisión; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `borradores/manual.md` como contexto suministrado.  
**Cambios previstos:** ninguno; PK06 solo agrupa revisiones.  
**Dependencias:** WS31 requiere `G_HUMAN_MANUAL` y depende de WS30, WS10 y WS43; WS43 requiere `G_HUMAN_MANUAL`, `G_PRODUCT`, `G_WRITE_CONTRACT` y depende de WS17 y WS30. Las revisiones de ambos hijos y sus `disposition.md` condicionan PK06.  
**Validaciones futuras:** ejecutar `context_review.py status` desde la raíz de `deskops`; confirmar que los hashes de input y contrato de cada hijo coinciden con los actuales; verificar `disposition.md` en el intento correspondiente; admitir bloqueo solo si es externo, está registrado por la sesión de coordinación con responsable y dependencia.

## FUTURO
La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos externos. Los revisores de WS31 y WS43 producen sus `disposition.md`. Un humano resuelve las Pxx y los gates aplicables. Ningún resultado de PK06 autoriza ejecución, publicación ni cambio de estado por sí mismo.
