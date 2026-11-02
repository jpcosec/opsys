## REFORMULACION
Propósito: implementar en graph_ui la lectura segura entre desks que fija WS11. Resultado: rutas de lectura que resuelven un conjunto cerrado `alias → (root, store)` suministrado por el operador, conservan desk/store por petición sin tocar `SLDB_STORE`, leen un segundo desk de WS40 y vuelven por la historia sin mutaciones cruzadas. Repo: graph_ui (`frontends/mindmap/source/`, `views/workspace/`, `tests/`). Límites: solo lectura, sin federación por copia, sin ampliar sldb, sin inventar aliases/roots ni valores de configuración; gate `G_UI_READ`; depende de WS11, WS13 y WS40.

## AMBIGUEDADES
1. «La forma JSON sigue la de 7.1 (`{ok:false,error}` + estado HTTP)»: no fija el estado de E-MD1..E-MD4; obliga a inventar 400/403/404/503.
2. «el de la configuración confiable si el operador lo incluyó y, si no, `local`» frente a «`local` … queda fuera del conjunto y el operador no puede redefinirlo»: no aclara si otro alias puede designar el desk del proceso; obliga a inventar esa regla.
3. «El medio de la comprobación es de los consumidores» y «el store … no cambió»: no define qué se compara (archivos, mtime, versión); obliga a inventar el criterio observable.
4. «los stores que se leen están preparados y canónicos fuera del request»: no dice quién ni cuándo los prepara; obliga a inventar el punto (fixture, script de arranque).

## DRY-RUN
Lecturas: WS11 3.2/5.2/8, rutas del lector WS13, generador/manifiesto WS40. Cambios previstos: módulo que traduce alias→(root,store) por petición; parámetro de alias en las rutas de lectura; pasar el directorio a `open_store`; mapear E-MD1..E-MD4; pruebas con dos desks temporales, enlaces authored y tercer repo sin desk. Dependencias: corpus WS40, lector WS13, `G_UI_READ`. Errores: alias no autorizado, ruta escapada y store ausente visibles. Validación futura: UF08, rechazo de roots/paths escapados y comprobar que el store no cambió tras leer. Sin ejecutar.

## FUTURO
El operador aporta la configuración de aliases; WS40 produce corpus y manifiesto; WS13.1/13.3 dan lectura e historia; P01 registra el acta de `G_UI_READ`; si la API pública no sostiene la no-mutación, intake en el repo dueño antes del workaround.
