## REFORMULACION

**Propósito.** PK04 agrupa los entregables que hacen navegable el desk authored y sus representaciones sobre una identidad común.

**Resultado sustantivo.** Entradas e índices authored versionados (WS17), Board como lista/tablero/dependencias (WS22), procedimiento navegable (WS23), conocimiento/grafo local (WS24) y, opcionalmente, ViewDoc/NotationDoc (WS18). El paquete termina cuando sus hijos cumplen y se comprueba la navegación integrada.

**Repo.** `owner_repo: deskops`; las salidas se distribuyen entre deskops, graph_ui y spec2viz.

**Límites.** No hay ejecución propia ni autorización de tareas; no se escribe status desde renderer, no se marcan pasos por lectura y los índices no sustituyen fuentes. WS18 no bloquea WS24 ni el resto del paquete.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Ejecución hipotética por hijos:

1. Con WS09 (catálogo), WS11 (identidad/contrato), WS13 (lector/foco/historia) y WS40 (corpus reproducible) disponibles, WS17 escribe plantillas `ejemplo/nav/`; WS40 regenera el corpus temporal con ellas y produce manifiesto de roots/stores/aliases. WS17 no copia el registry real ni inventarios derivados.
2. WS22 consume WS13+WS09 y renderiza el Board real: lista, tablero por estado y dependencias, abriendo el mismo TaskDoc y pills.
3. WS23 consume WS13+WS09 y muestra RitualDoc/StepDoc/lifecycle sin controles de avance; pasos inertes si no existe campo/API real.
4. WS24 consume WS13+WS09, reutiliza el gráfico y la vista de documento genérica, con backlinks de sldb, tags del payload y vecindad ≤2 hops; el ViewDoc de WS18 solo se conecta tras `G_SPEC_VIEW`.
5. WS18, si se promueve, requiere `G_SPEC_VIEW` per-delta y se prueba en spec2viz/graph_ui sobre store real.

**Transferencias.** WS17 entrega plantillas y corpus regenerado; WS13 entrega lector y foco; WS09 catálogo; WS11 identidad; WS22–24 entregan vistas que comparten selección y links.

**Validación conjunta.** Sobre el corpus WS40: abrir el mismo TaskDoc desde lista/tablero/dependencias, procedimiento y conocimiento; comprobar que los índices resuelven roots/aliases sin duplicar registry; pruebas de no escritura desde renderers; errores por contrato/API/permiso ausente se registran y la operación queda no disponible.

**Gates.** `G_UI_READ` para WS22–24; `G_SPEC_VIEW` solo para WS18.

## FUTURO

La recepción humana (WS16/WS30), la publicación real WS43, el acta `G_SPEC_VIEW` del receptor/P01 y la promoción de TaskDocs en graph_ui/spec2viz corresponden a otros nodos o a decisión humana.
