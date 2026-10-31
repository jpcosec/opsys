## REFORMULACION

**Propósito:** revisar PK01 como encargo de planificación. PK01 es una agrupación de revisión de «Fundamentos y auditoría», no una tarea operativa ni un entregable.

**Resultado:** dictamen sobre si PK01 se entiende y si su aceptación es comprobable; no se produce código ni se corrige el plan.

**Repo:** deskops. PK01 es `aggregate` y no declara `owner_repo`; su comprobación se ancla explícitamente a la raíz de deskops mediante `context_review.py status`.

**Límites:** no ejecutar nada; no revisar los bloques `edge` de los vecinos; no tratar los hijos como tareas activas; no resolver propuestas Pxx; no modificar el Board ni el DAG.

## AMBIGUEDADES

Ninguna.

La aceptación define el resultado como estado verificable de las revisiones de los hijos directos, delimita qué cuenta como bloqueo admisible —causa externa, responsable y dependencia registrada en `disposition.md`— y remite a un comando concreto para comprobarlo. No obliga al ejecutor de PK01 a inventar entregable, criterio de aceptación, repo de comprobación, responsable ni límite de alcance.

## DRY-RUN

- **Lecturas previstas:** bloque de PK01 en `dag.yaml`; guía de revisión; contratos de WS01–WS06 aportados como bloques `edge`; `disposition.md` de cada hijo; salida de `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops.
- **Cambios previstos:** ninguno. PK01 no produce archivos ni edita el plan.
- **Dependencias:** las revisiones vigentes de WS01–WS06; WS01 aparece como prerrequisito de los demás hijos. PK01 no añade dependencia operativa propia.
- **Validaciones futuras:** comprobar coincidencia de hash de input y contrato por hijo; confirmar existencia de `disposition.md` en el intento correspondiente; admitir únicamente bloqueos externos con responsable y dependencia registrada.

## FUTURO

Las revisiones de WS01–WS06 y sus `disposition.md` las producen los nodos de revisión de cada hijo. La sesión de coordinación ejecuta `context_review.py status` y registra los bloqueos externos con su responsable. La resolución de esos bloqueos corresponde al actor o repo designado; no es una ambigüedad de PK01.
