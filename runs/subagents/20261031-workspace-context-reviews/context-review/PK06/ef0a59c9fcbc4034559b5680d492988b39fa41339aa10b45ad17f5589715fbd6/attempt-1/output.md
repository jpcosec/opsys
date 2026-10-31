## REFORMULACION

**Propósito:** PK06 es una agrupación de revisión de la publicación básica: manual documental (WS31) y navegación del desk real (WS43). No es una tarea ejecutable ni una dependencia operativa.

**Resultado:** veredicto booleano: verdadera si cada hijo directo tiene revisión vigente sin ambigüedad de su propio encargo, o bloqueo externo con responsable registrado; falsa en caso contrario.

**Repo:** PK06 no declara `owner_repo`; la comprobación se hace desde la raíz de `deskops`, y ambos hijos pertenecen a `deskops`.

**Límites:** no revisa los bloques edge de WS31/WS43, no ejecuta hijos, no sustituye gates `G_*` ni decisiones humanas, y no produce entregables propios.

## AMBIGUEDADES

ninguna.

La aceptación define el criterio y lo delega a `context_review.py status`; no exige al ejecutor inventar hashes, disposiciones ni responsables.

## DRY-RUN

- **Lecturas previstas:** nodo PK06, lista de hijos WS31/WS43, guía de context review y, en su caso, salida de `context_review.py status`. No se ejecuta ahora.
- **Cambios previstos:** ninguno; un aggregate no modifica archivos ni crea entregables.
- **Dependencias:** revisión vigente de WS31 y WS43; coincidencia de hash de input y contrato; `disposition.md` guardada en el intento correspondiente; para bloqueo, responsable y dependencia registrados en esa disposición.
- **Validaciones futuras:** ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`; comprobar que cada hijo cumple revisión vigente; distinguir ambigüedad propia no resuelta (pending/blocked por esa causa) de bloqueo externo con responsable.

## FUTURO

La sesión de coordinación ejecuta `context_review.py status` y registra el resultado. Los revisores de WS31/WS43 producen sus `disposition.md`. Un actor o repo responsable debe resolver cualquier bloqueo externo. La ejecución de WS31/WS43 y los gates `G_HUMAN_MANUAL`, `G_PRODUCT` y `G_WRITE_CONTRACT` quedan fuera de este nodo.
