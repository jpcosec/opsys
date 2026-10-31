REFORMULACION
Propósito: implementar en el workspace la edición de campos reutilizando editores y API, con revisión CAS del documento y conflicto visible sin perder texto local; los campos protegidos por workflow quedan fuera de este canal. Resultado: un delta de UI en `graph_ui` sobre el ticket draft de edición, con pruebas. Repo dueño: `graph_ui`. Límites: mutación solo en desk y modo manual exclusivo; otros modos, read-only. Depende de WS12 y WS16, y de `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. No reviso los nodos vecinos.

AMBIGUEDADES
1. Cita: «endpoints autorizados por el contrato WS12» dentro de `output_scope`. Al figurar como parte del alcance de salida, no queda claro si el nodo solo consume endpoints ya autorizados o también puede modificar su código; esto obligaría a inventar si el cambio cruza a otro repo y dónde termina el límite de `graph_ui`.

DRY-RUN
Lecturas previstas: `task_file`; contrato WS12 —whitelist, CAS, endpoints, policy y campos workflow—; acta de `G_HUMAN_READ`; matriz WS06 vía WS11/12; ticket draft y Board de `graph_ui`.
Cambios previstos, sin ejecutar: componentes/adaptadores en `frontends/mindmap/views/workspace/fields/`, llamadas a endpoints autorizados y pruebas en `tests/`. No se prevé tocar backend no autorizado.
Dependencias: WS12 produce contrato y gates de escritura; WS16 produce `G_HUMAN_READ`; WS06 llega transitivamente.
Validaciones futuras: guardar/recargar persiste el dato; escritura obsoleta se rechaza conservando texto local; campos protegidos no editables; modos no manuales permanecen read-only; no duplicar el ticket existente.

FUTURO
WS12 debe fijar contrato, whitelist, unidad de revisión, endpoints y aceptación `G_UI_WRITE`; WS16 aporta el acta humana; el humano resuelve P03; el TaskDoc de promoción fija archivos, textos y casos de prueba; el responsable de `graph_ui` acepta el delta. Nada de esto se ejecuta aquí.
