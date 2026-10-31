REFORMULACION
Propósito: registrar una decisión/revisión humana explícita vinculada a una tarea o intento Scion, distinguiendo estados. Resultado: registro con actor y referencia al intento, sin convertir `completed` del agente en aprobación. Repo dueño: `deskops`. Límites: solo `runtime/` (adaptador definido por contrato), modelos/reportes y tests; no UI/editor ni tablas Scion; `promotion: not_authorized`; depende de WS32, WS11, WS33.1 y G_SCION.

AMBIGUEDADES
1. «distinguir completado, validado, aprobado y cerrado» frente a una aceptación que solo exige «Una decisión humana queda registrada con actor y referencia al intento». No define valores, transiciones ni aceptación para validado/cerrado; obliga a inventar el modelo de estados y sus pruebas. Si «cerrado» implica closeout, además faltan G_CLOSEOUT/WS27–28; si es solo etiqueta, debe precisarse.
2. «Revisión humana explícita» frente a «Una decisión humana queda registrada»: no aclara si se persiste una revisión-eventO o una decisión-resultado. Obliga a inventar la entidad y qué cuenta como decisión.
3. «completed del agente nunca se registra como aprobado»: no indica de dónde se obtiene `completed` ni cómo se identifica. Obliga a inventar el origen y mapeo de ese estado.

DRY-RUN
Lecturas previstas: `task-ws33-2.md`, guía/brief/alcance/decisiones, salidas de WS33.1, contrato de WS32 y evidencia de G_SCION. Cambios previstos: modelo/registro de decisiones humanas, adaptador runtime y tests en `deskops`. Dependencias: WS32, WS11, WS33.1; gate G_SCION. Validaciones futuras: actor y referencia al intento presentes; estados distinguibles; ningún `completed` del agente figura como `aprobado`; sin tocar tablas Scion ni UI. No ejecutar.

FUTURO
WS07 designa operador Scion y receptores; WS44 produce G_SCION; WS33.1 entrega referencias/resultados; WS32/WS11 fijan contratos; WS06 y la promoción —archivos exactos, pills, evidencia— quedan a otro nodo o decisión humana. La ejecución no está autorizada.
