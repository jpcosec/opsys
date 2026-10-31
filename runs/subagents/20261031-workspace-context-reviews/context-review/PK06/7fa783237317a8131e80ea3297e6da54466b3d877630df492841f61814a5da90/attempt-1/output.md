## REFORMULACION
**Propósito:** revisar PK06 como encargo de planificación: nodo `aggregate` que agrupa la publicación básica (manual y navegación del desk real).
**Resultado:** PK06 es verdadero cuando cada hijo directo (WS31, WS43) tiene revisión `context_review` vigente —hash de input y contrato coincidentes y `disposition.md` guardada— o un bloqueo explícito con responsable y dependencia.
**Repo:** deskops para PK06/WS31/WS43; WS30 depende de graph_ui.
**Límites:** no es dependencia operativa ni se ejecuta; no revisa los bloques edge de vecinos ni decisiones Pxx; no autoriza implementación.

## AMBIGUEDADES
1. «un bloqueo externo con responsable sí la admite»: no se define qué hace «externo» a un bloqueo frente a la ambigüedad propia del hijo. Obligaría a inventar el criterio de clasificación (¿dependencia ajena, causa técnica, actor externo?) para decidir si PK06 admite el bloqueo.
   Cita: «un bloqueo externo con responsable sí la admite».
2. «cuyo hash de input y de contrato coinciden con los actuales»: no se identifica qué artefacto es el «contrato» del hijo ni quién fija su hash actual; el input remite a `dag.yaml` y a la guía, pero no a un contrato separado por hijo. Obligaría a inventar la fuente de hash.
   Cita: «cuyo hash de input y de contrato coinciden con los actuales».

## DRY-RUN
**Lecturas previstas:** guía de revisión, `dag.yaml` (PK06, WS31, WS43 y transitivos WS30, WS17, WS10, WS40, WS11), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`.
**Cambios previstos:** ninguno; esta revisión no escribe.
**Dependencias:** hijos WS31 y WS43; WS31 depende de WS30, WS10, WS43; WS43 de WS17 y WS30; gates `G_HUMAN_MANUAL`, `G_PRODUCT`, `G_WRITE_CONTRACT`.
**Validaciones futuras (sin ejecutar):** `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; coincidencia de hashes; existencia de `disposition.md`; registro de `status=blocked` con responsable y dependencia; revisión de aceptación de WS31/WS43.

## FUTURO
La sesión de coordinación ejecuta `context_review.py` y registra bloqueos; los revisores de WS31/WS43 producen sus `disposition.md`; WS30/WS43 generan actas de validación/publicación; el humano resuelve P08/P09 y P01/P02. Nada de ello es ambigüedad de PK06.
