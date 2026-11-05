## REFORMULACION

ROOT es un **agregado de planificación** de deskops: no se ejecuta, cierra cuando cierran sus hijos. Su propósito es que los gates del ciclo de vida de una tarea sean documentos evaluados por sldb —tipos de tarea con jerarquía, `ReviewDoc` como recibo, `RuleDoc` de activación, efectos en las aristas—, cerrar las vías que saltan gates (`advance --to`, `edit task status`) y sustituir los scripts de revisión en frío por `deskops review`. El resultado es el paquete completo cerrado, con `G_TYPES`, `G_RECEIPTS` y `G_CONSUMER` satisfechos y este último informado a sldb. Repo dueño: deskops. Límites: no reimplementar el evaluador en Python, no escribir en sldb salvo `deskops message send`, no autenticar actores, no convertir la verificación externa de cierre en recibos y no cambiar la autoridad de `closeout commit`.

## AMBIGUEDADES

1. **Orden de los paquetes.** Cita: «El orden entre paquetes lo imponen las aristas depends_on de sus hijos». ROOT no declara `depends_on` entre PC01, PC02 y PC03; solo remite a aristas de hijos que no están en el input revisable. Un ejecutor tendría que inventar la secuencia de paquetes o asumir que puede leer aristas fuera del input.

## DRY-RUN

ROOT no se ejecuta. Hipotéticamente, un ejecutor ordenaría PC01 → PC02 → PC03 según las aristas de los hijos:

- **PC01** lee el estado actual de deskops y produce tipos registrados, el modelo `ReviewDoc` y `deskops review`. Transfiere a PC02 el vocabulario de tipos y recibos, y a PC03 el tipo base para composición.
- **PC02** consume esos tipos/recibos y los nodos GO05–GO09 de sldb; produce `RuleDoc` de activación, efectos y `advance` por `edges_holding`, cierre de las vías de escape, `G_CONSUMER` y rituales actualizados. Transfiere a PC03 el ciclo de vida como grafo.
- **PC03** consume PC01 y PC02; produce `parent_id`, `children`, `task.aggregate`, promoción desde `dag.yaml` y `deskops graph` leyendo sldb. Transfiere a ROOT el estado final verificable.

Validación conjunta: `pytest tests` verde, cierre de cada hijo, comprobación de los tres gates, nota a sldb con el commit de `G_CONSUMER`, `CHANGELOG`/`docs` según la regla común 4 y revisión en frío aceptada por quien opera el desk.

## FUTURO

sldb entrega GO05–GO09 y se cierran los gates `G_SLDB_*`; el dueño confirma los pendientes (`--evidence`, DC7, `task.external`, Scion); quien opera el desk escribe disposiciones y autoriza la promoción; sldb recibe la nota de `G_CONSUMER`.
