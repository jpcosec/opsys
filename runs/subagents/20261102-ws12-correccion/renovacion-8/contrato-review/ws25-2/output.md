## REFORMULACION

Encargo del nodo **WS25.2** (graph_ui): construir la captura interna del workspace con destino elegido explícitamente por la persona —candidato de drawer o protoátomo— usando solo canales que autorice el contrato WS12, sin exigir tarea. Resultado: una captura que persiste tras recargar en el destino elegido, con origen (referencia tipada a ruta o mensaje) y sin crear tarea activa; colisiones no se sobrescriben en silencio; permisos del contrato aplicados; ambos destinos probados por separado. Repo: `graph_ui:repository_root/`, alcance `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: depende de WS12 (contrato), WS46 (capacidad probada de captura con origen) y WS48 (admisión de escritura); no crea API ni modelo por reflejo; no se cumple declarando la captura no disponible; sin G_HUMAN_READ no hay uso real de mutaciones en UI.

## AMBIGUEDADES

1. «cada destino se prueba por separado» / «una captura persiste tras recargar en el destino elegido». No queda claro si la aceptación se satisface con un destino probado o exige los dos; obligaría a inventar el criterio de completitud del nodo.
2. «endpoints autorizados por el contrato WS12». El contrato (§7.3, §4.2) deja el canal a WS46 y no fija una ruta concreta; obligaría a inventar qué endpoint es el autorizado antes de que WS46 lo determine.
3. «origen… con representación fijada por el contrato WS12», cuando el contrato (§7.2) la declara «propuesta, sin prueba». Obligaría a inventar si esa propuesta es normativa.
4. «se controla según el contrato» para colisiones; el contrato describe comportamientos distintos por opción (A–E) sin una regla única. Obligaría a elegir un comportamiento.

## DRY-RUN

Un ejecutor futuro leería: contrato §7, §4.2, §5.9; inventario y pruebas de WS46 (canal de captura con origen, por destino); módulo de admisión de WS48. Planificaría un módulo bajo `frontends/mindmap/views/workspace/capture/` que: (a) valide por el punto de admisión de WS48 antes de escribir; (b) invoque el canal probado por WS46 para drawer y protoátomo; (c) fije el origen con la representación de §7.2; (d) rechace colisiones. Cambios concretos y archivo exacto en el TaskDoc del delta. Dependencias: WS46 y WS48 entregadas; WS12 disponible. Errores esperados: sin WS46 no hay canal probado (bloqueo, no simulación); sin F1/admisión → lectura o handoff. Validación futura: pruebas en store temporal, persistencia tras recargar, origen visible, sin tarea activa (Board y `list tasks`), colisión rechazada, admisión consultada.

## FUTURO

WS46 produce y prueba la captura con origen por destino; WS48 produce el punto de admisión; WS12 permite la evaluación de `G_WRITE_CONTRACT`; P01 registra el acta `G_UI_WRITE` en graph_ui; el humano decide `G_HUMAN_READ`; root evalúa el nodo.
