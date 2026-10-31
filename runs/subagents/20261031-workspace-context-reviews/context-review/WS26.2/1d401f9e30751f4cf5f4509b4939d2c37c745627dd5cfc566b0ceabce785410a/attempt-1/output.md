## REFORMULACION
Propósito: enrutar explícitamente una tarea al `BoardDoc` y mostrar una “capa lista”. Resultado: representación en `frontends/mindmap/views/workspace/routing/` que añade la tarea mediante operación pública y muestra su estado listo. Repo dueño: `graph_ui`. Límites: solo endpoints autorizados por WS12; no ejecutar tareas, no avanzar estados ni confundir enrutar con ejecutar; promoción sujeta a contrato autorizado.

## AMBIGUEDADES
1. «representación de capa lista por dependencias/no solapamiento» frente a una aceptación que solo exige «Tras enrutar, `deskops show board` muestra la tarea». Falta criterio comprobable de la capa lista; obligaría a inventar su verificación y prueba.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc» no define qué ocurre con `files` vacíos o ausentes, ni si el solapamiento es por ruta exacta, prefijo o directorio. Obligaría a inventar la regla.
3. «promoción solo cuando el contrato resuelve commits previos por canal autorizado» y «el canal de promoción respeta commits previos y estado real» no aclaran si WS26.2 implementa promoción o solo prepara handoff, ni cómo se comprueba «estado real». Obligaría a inventar alcance y evidencia.
4. «dependencias pendientes» remite al «ritual de fase», pero no se aporta qué estados cuentan como pendientes ni cómo mapearlos desde deskops. Obligaría a inventar esa semántica.

## DRY-RUN
Lecturas previstas: nodo WS26.2, contratos vecinos WS12/WS22/WS26.1, gates y guías. Cambios previstos: vista de enrutamiento, integración con Board, cálculo/visualización de capa lista y tests. Dependencias: contrato WS12, Board de WS22, autoría de WS26.1 y gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Validaciones futuras: `deskops show board`, distinción visual solicitada y pruebas de capa lista. Sin ejecución.

## FUTURO
WS12 produce whitelist, canal y efectos de promoción; WS22 la representación del Board; WS26.1 la tarea autorada; WS16 la aprobación humana de lectura. El responsable humano designado resuelve los gates y Pxx aplicables.
