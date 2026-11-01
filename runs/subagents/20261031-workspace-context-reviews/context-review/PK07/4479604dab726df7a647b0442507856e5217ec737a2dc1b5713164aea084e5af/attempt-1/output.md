## REFORMULACION
PK07 agrupa dos extensiones independientes del workspace: WS29 (Changes e impacto comprobable) y WS39 (inspección/edición de modelos existentes). El propósito es cerrar un paquete con evidencia propia, sin que ninguna sea prerrequisito del lector ni del manual básico. El resultado sustantivo exige ambas salidas: WS29 prueba mutación real, impacto a 1 hop y diagnóstico sin reparación automática; WS39 prueba edición/validación por API y cuenta con aceptación humana propia. El manual debe etiquetar cada extensión según evidencia, sin presumir CST/Kimun. Repo dueño: deskops; hijos en graph_ui. Límites: no ejecuta nada, no añade aristas ni autoriza tareas, y el gate de comprensión no acredita producto entregado.

## AMBIGUEDADES
1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun»: no identifica el nodo/productor del manual ni dónde se registra la etiqueta para WS29; WS39 sí nombra WS31 y su capítulo 15. Obliga a inventar quién actualiza el manual y con qué evidencia concreta para la extensión Changes.

## DRY-RUN
PK07 es un agregado no ejecutable: termina cuando terminan sus hijos. Orden hipotético: WS29 y WS39 pueden avanzar en paralelo, pues no hay arista entre ellos.

WS29 consume de WS15 el modo degradado/errores de lectura y de WS24 la vista de grafo/vecindad; requiere G_UI_READ. Produce la vista Changes/impacto en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según WS11 y tests. Se validaría con un store temporal real: mutación, documento afectado, relaciones entrantes/salientes a 1 hop y enlace al comando de diagnóstico, sin reparación automática.

WS39 consume el contrato WS12 y el panel Context de WS13; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Produce la entrada desde documento activo al Schema/editor existente, pruebas de UF09 y acta en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`. Se validaría con mutación en store temporal, comprobación de efectos/errores del contrato y acta humana antes de publicar el capítulo 15 del manual.

Integración conjunta: ambas salidas viven sobre el lector existente de graph_ui; se validarían sus tests y que el manual etiquete cada extensión con evidencia. Si falta contrato, API o gate, se registra el hueco y no se crea sustituto.

## FUTURO
Quedan fuera de este nodo las salidas de WS15, WS24, WS12 y WS13; la publicación del manual por WS31; la participación humana de P08; las actas y recepciones por delta; y los gates G_UI_READ, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. Nada de esto se ejecuta ni se acepta aquí.
