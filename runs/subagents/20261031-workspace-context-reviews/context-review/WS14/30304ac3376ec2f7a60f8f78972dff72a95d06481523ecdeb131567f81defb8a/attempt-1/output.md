## REFORMULACION

WS14 es un nodo de implementación en `graph_ui`: integrar búsqueda navegable en el workspace usando exclusivamente `sldb find` o su ruta en `sldb serve`, sin parser propio. El resultado esperado es buscar por texto/campos —semántica solo si la API real la ofrece—, abrir resultados con identidad y ruta de origen, conservar consulta y foco al volver, y distinguir sin resultados, error de backend y búsqueda degradada. Límites: depende de WS13 y G_UI_READ; no cargar el grafo completo por tecla; archivos y pruebas finas quedan al TaskDoc.

## AMBIGUEDADES

ninguna

## DRY-RUN

Nodo delivery, no agregado. Lecturas: nodo WS14, contrato WS11, auditoría WS03, salidas de WS13.1/13.2/13.3, recibo per-delta G_UI_READ y código de `views/workspace`. Cambios previstos: módulo/UI de búsqueda en `views/workspace` y `source`, consumo de la ruta pública de búsqueda, apertura de resultados mediante la navegación de WS13, estados diferenciados y pruebas en `tests/`. Sin ejecutar nada.

Dependencias: WS13 terminado, WS11/WS03 disponibles y G_UI_READ aceptado para este delta. Si falta contrato, API o permiso, detenerse y registrar el hueco con repo dueño, sin crear sustituto. Validación futura: pruebas de peticiones —teclear no dispara carga completa del grafo—, recorrido de teclado buscar-abrir-volver con consulta y foco conservados, y tres estados distintos; store temporal real o corpus WS40. El TaskDoc fija archivos, textos y casos.

## FUTURO

WS16 validará con humano y medirá apertura/búsqueda/arranque. El receptor P01 produce el acta G_UI_READ por delta. WS11/WS03 deben entregar contrato y auditoría; WS13 sus capacidades. La promoción y el TaskDoc los autoriza un humano; este nodo no los crea.
