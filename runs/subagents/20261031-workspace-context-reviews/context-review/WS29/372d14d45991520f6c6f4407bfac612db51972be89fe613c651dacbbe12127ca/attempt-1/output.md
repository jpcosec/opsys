## REFORMULACION

**Propósito**: definir un delta en `graph_ui` que haga comprobable, en la vista Changes, el impacto de una mutación mediante los hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`.

**Resultado**: una vista que, ante una mutación real en un store temporal, muestre el documento afectado, las relaciones entrantes y salientes a 1 hop según la API de grafo de sldb, y los errores agrupados por comando; con enlaces al comando documentado correspondiente. Reparar no es automático.

**Repo**: `graph_ui`; salidas en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según contrato WS11 y `tests/`.

**Límites**: delta sobre la tarea Changes actual, sin duplicarla; no CST ni árbol Kimun; no reparación automática; no bloquea lector/manual básico. Nodo `candidate`, sin ejecución autorizada; requiere `G_UI_READ`.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas**: nodo WS29 y gates; guía; brief, alcance, decisiones, cobertura y reconciliación; bloques edge WS15/WS24 solo como contratos vecinos.

**Cambios previstos**: implementación en `changes/` y tests; consumo de los tres comandos; enlaces a documentación de sus repos dueños; sin cambios en reparación ni en otras tareas.

**Dependencias**: WS15 (errores y modo degradado), WS24 (grafo/backlinks), `G_UI_READ` producido por WS11; matriz WS06 transitiva; contrato de rutas de integridad de WS11.

**Validaciones futuras**: prueba con store temporal real; documento afectado visible; relaciones a 1 hop; errores agrupados por comando; enlaces correctos; comprobar que no bloquea lector/manual. El TaskDoc de promoción fijará escenario, archivos y textos; preflight task-only.

## FUTURO

WS11 debe producir el acta de `G_UI_READ` con responsable graph_ui identificado, fecha, tarea receptora y no solapamiento. El solicitante humano designa responsables y decide la promoción; hoy está `not_authorized`. El TaskDoc fijará el escenario concreto de mutación y los detalles de prueba. Si falta un contrato o API esperada, la regla común de alcance obliga a detenerse y registrar el hueco, sin crear sustituto.
