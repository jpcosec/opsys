## REFORMULACION

**Propósito:** integrar en `graph_ui` la delegación e intervención humanas usando exclusivamente el adaptador público WS34 para dispatch/reply, y registrar decisiones con WS33.2.  
**Resultado:** pantalla que vincula la respuesta al intento, confirma la operación, muestra actor/evidencia y presenta como error la falta de API o permisos, cubierto por test; sin autoaprobación ni simulación.  
**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador WS34 autorizada por WS12, y `tests/`.  
**Límites:** no crear adaptador propio, no aprobar ni simular; gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «revisión con actor/evidencia visible» — no define qué actor (humano, coordinador, agente), qué evidencia ni cómo se comprueba; la aceptación no la recoge. Obliga a inventar el sujeto y el criterio de visibilidad y prueba.
2. «registrar decisiones con WS33.2» — WS33.2 no se describe en el input ni figura en `depends_on`; solo aparece como referencia. Obliga a inventar su contrato o asumir una dependencia no declarada.

## DRY-RUN

**Lecturas:** `dag.yaml` (WS36, WS34, WS35, gates), guía, brief, alcance, decisiones y cobertura.  
**Cambios previstos:** vistas de ejecución en `graph_ui`, ruta fina al adaptador WS34, registro de decisiones vía WS33.2 y tests.  
**Dependencias:** WS34 (dispatch/reply y confirmación), WS35 (lectura intento/mensajes), WS33.2 (decisiones), contrato WS12 y gates.  
**Validaciones futuras:** test de error por API/permisos ausentes; comprobar respuesta ligada al intento y operación confirmada; ausencia de autoaprobación; WS37 validará UF06 real. No se ejecuta nada.

## FUTURO

WS37 valida con agente real; WS44 produce G_SCION; WS12 resuelve G_UI_WRITE y G_WRITE_CONTRACT; el humano resuelve G_EXEC y autoriza la promoción, hoy `not_authorized`; el TaskDoc fijará archivos, textos y escenarios. WS07 designa operador Scion.
