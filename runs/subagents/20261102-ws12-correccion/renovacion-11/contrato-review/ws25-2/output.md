REFORMULACION

WS25.2 (graph_ui, delivery) debe entregar una captura interna en la UI del workspace con destino explícito —candidato de drawer o protoátomo— sin crear tarea implícita. Resultado: captura que persiste tras recargar, muestra origen (ruta o mensaje) y controla colisiones, con los permisos del contrato. Repo: graph_ui (`frontends/mindmap/views/workspace/capture/`, endpoints autorizados, `tests/`). Límites: depende de WS12 (contrato), WS46 (capacidad probada) y WS48 (admisión); gates `G_WRITE_CONTRACT`, `G_UI_WRITE`, `G_HUMAN_READ`; no crea API ni modelo, no muta el desk real y no se cumple declarando «no disponible».

AMBIGUEDADES

1. «endpoints autorizados por el contrato WS12»: el contrato no enumera endpoints de captura; HO-01 los deja al delta. Obliga a inventar qué ruta usa la captura.
2. «Permisos del contrato aplicados»: no concreta cuáles de §9.5 ni cómo. Obliga a elegir controles.
3. «se controla según el contrato»: el contrato compara opciones A–E sin aprobar ninguna y remite el canal a WS46. Obliga a fijar el mecanismo de colisión antes de que exista.
4. «Origen = referencia tipada … con representación fijada por el contrato WS12»: el contrato la llama «propuesta del contrato, sin prueba» y deja abierto un campo tipado si root lo prefiere. Obliga a decidir la representación.

DRY-RUN

Un ejecutor futuro leería WS12 (§§3, 4.2, 5.9, 7), el inventario y pruebas de WS46, el módulo de admisión de WS48 y las rutas/captura de graph_ui. Cambios previstos: archivos de captura en `views/workspace/capture/`, cableado al canal que WS46 haya probado y a la admisión de WS48, y tests por destino en `GU/tests/`. Dependencias: sin WS46 probado (origen, no-tarea-activa, colisión) o sin WS48, se detiene; no inventa canal. Gates consumidos antes de habilitar. Validación esperada: persistencia tras recarga, origen visible (ruta y mensaje), ausencia en Board y `list tasks`, colisión rechazada sin sobrescribir, y rechazo de admisión sin F1. No es agregado: es delivery ejecutable.

FUTURO

WS46 entrega inventario y pruebas de captura; WS48 entrega módulo de admisión y formato F1; root evalúa `G_WRITE_CONTRACT`; P01 registra el acta `G_UI_WRITE`; el humano aporta F1 y `G_HUMAN_READ`.
