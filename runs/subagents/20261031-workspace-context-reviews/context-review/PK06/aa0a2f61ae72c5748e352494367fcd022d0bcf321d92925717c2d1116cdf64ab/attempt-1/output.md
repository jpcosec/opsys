REFORMULACION
- Propósito: agrupar la revisión de “Publicación básica”: manual documental (WS31) y navegación del desk real (WS43), después de la validación manual.
- Resultado: PK06 no entrega artefacto; es verdadero solo si cada hijo directo tiene `context_review` vigente —hashes de input y contrato actuales y `disposition.md` en el intento correspondiente— o `blocked` externo con responsable y dependencia registrados.
- Repo: agregado sin `owner_repo` propio; ambos hijos declaran `deskops`.
- Límites: no se ejecuta, no sustituye revisiones hijas, no resuelve Pxx ni gates pendientes; un `pending` por ambigüedad propia del hijo no satisface la aceptación.

AMBIGUEDADES
ninguna.

DRY-RUN
- Lecturas: `dag.yaml` (PK06, WS31, WS43), `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `borradores/manual.md`.
- Cambios previstos: ninguno; esta revisión solo evalúa el encargo.
- Dependencias: entradas `context_review` de WS31/WS43, hashes de input/contrato, `disposition.md` guardadas, sesión de coordinación y `context_review.py status`. Los gates `G_HUMAN_MANUAL`, `G_PRODUCT` y `G_WRITE_CONTRACT` son de los hijos, no de PK06.
- Validaciones futuras: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`; verificar los dos hijos, vigencia por hashes, `disposition.md` correspondiente y, si hay `blocked`, causa externa, responsable y dependencia. No aceptar `pending` por ambigüedad propia.

FUTURO
- La sesión de coordinación ejecuta el script y registra bloqueos; los revisores de WS31/WS43 producen sus `disposition.md`; humanos resuelven Pxx y gates; la ejecución o promoción de WS31/WS43 ocurre fuera de PK06.
