REFORMULACION

WS19.2 encarga implementar en graph_ui el alta y baja de relaciones permitidas por el contrato WS12, dentro del workspace, usando API real y la precondición de escritura que WS12 fije. Resultado: las relaciones persisten y se confirman tras recargar; una relación no permitida, protegida o con revisión obsoleta se rechaza con error visible; la baja de un RelationDoc elimina el documento autorado y su índice por el canal público de sldb (`/save delete` con `expected`), o se deshabilita y declara si el modo no ofrece ese efecto. Repo dueño: graph_ui, en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados y `tests/`. Límites: no crear semántica de relaciones en el componente; quitar una referencia de campo es otra operación; el desarrollo y las pruebas aisladas de API pueden avanzar, mientras G_HUMAN_READ solo habilita el uso de mutaciones en UI.

AMBIGUEDADES

ninguna

DRY-RUN

Un ejecutor leería el contrato WS12 —whitelist, canal, precondición, errores—, las salidas de WS47 (guarda de contenido no declarado) y WS48 (admisión de escritura), y la operación `/save delete` con `expected` de sldb. Crearía o modificaría el editor de relaciones en `views/workspace/relations/`: alta y baja, consumo del canal autorizado y error visible; añadiría pruebas en `tests/`.

Consumiría G_PAYLOAD_PRECONDITION (WS45), G_WRITE_CONTRACT (WS12), G_UI_WRITE (acta P01 por delta) y G_HUMAN_READ para habilitar el uso, no para desarrollar. Si falta contrato, endpoint o efecto de borrado, se detendría, registraría el hueco con repo dueño y no crearía sustituto; si el modo solo destrackea, deshabilitaría la baja de RelationDoc y lo declararía.

Validaría con store temporal real: persistencia tras recarga; rechazo de relación no permitida o protegida; rechazo por revisión obsoleta; borrado de RelationDoc y de su índice sin reaparición; y prueba separada para quitar una referencia de campo.

FUTURO

WS12 fija la representación de la precondición y las operaciones; WS45 la verifica; WS47 y WS48 producen la guarda y la admisión; el receptor P01 emite el acta por delta; WS16 resuelve G_HUMAN_READ; WS19 cierra cuando cumplen sus hijos; la promoción fija archivos, textos y pruebas exactas.
