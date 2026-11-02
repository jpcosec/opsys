## REFORMULACION

Propósito: capturar en graph_ui con destino explícito —candidato en drawer o protoátomo— por canales que autorice WS12, sin crear tarea. Resultado: UF02, captura persistente tras recargar con origen tipado (ruta o mensaje), sin tarea implícita, colisión no sobrescrita y permisos aplicados; cada destino se prueba aparte. Repo: graph_ui (`frontends/mindmap/views/workspace/capture/`, endpoints de WS12, `tests/`). Límites: depende de WS12, WS46 y WS48; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; no crea API ni modelo; no se cumple declarando la captura no disponible.

## AMBIGUEDADES

1. «endpoints autorizados por el contrato WS12»: WS12 §4.2 registra HO-01 («Ninguna ruta de autoría») sin fijar rutas; obligaría a inventar ruta y contrato de error.
2. «representación fijada por el contrato WS12»: WS12 §7.2 la llama «propuesta del contrato, sin prueba» y deja abierta la decisión de campo tipado; obligaría a decidir modelo.
3. «se controla según el contrato»: WS12 §7.3 concluye que «ninguna opción cumple las tres propiedades con prueba real» y lo difiere a WS46; obligaría a elegir la colisión antes de su prueba.
4. «los orígenes ruta y mensaje se registran»: no se define cómo un candidato de drawer toma origen mensaje si `promote` borra la nota; obligaría a inventar el vínculo.

## DRY-RUN

Nodo ejecutable de entrega. Leería WS12 (2, 3, 5.9, 7), el inventario de WS46 y el módulo de WS48, exigiendo ambos probados. Crearía en `frontends/mindmap/views/workspace/capture/` vista y selector de destino, una ruta que invoque el canal autorizado, el envío del origen y el manejo de colisión; consultaría WS48 antes de escribir; añadiría tests en store temporal. Consume WS46 (captura con origen y colisión), WS48 (admisión) y WS12 (whitelist, campos protegidos, representación). Gates: G_WRITE_CONTRACT y G_UI_WRITE por delta con acta P01; G_HUMAN_READ para habilitar. Validación: captura visible tras recargar con origen ruta y mensaje; ausencia en Board y `list tasks`; colisión rechazada. Errores: falta WS46 → detener, no declarar «no disponible»; falta WS48 → lectura/handoff.

## FUTURO

WS46 debe entregar y probar la composición con origen y colisión para ambos destinos; WS48, el punto de admisión; root y P01 deben aceptar G_WRITE_CONTRACT y G_UI_WRITE del delta; la persona usuaria elige el destino y confirma la captura.
