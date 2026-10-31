## REFORMULACION
**Propósito:** integrar en el workspace la delegación e intervención humanas, invocando solo el adaptador WS34 para dispatch/reply y registrando decisiones con WS33.2. **Resultado:** superficie UI en `graph_ui` que vincula respuesta al intento, confirma la operación y muestra actor humano/evidencia WS33.1/WS33.2; si faltan API/permisos, muestra error; sin autoaprobación ni simulación. **Repo dueño:** `graph_ui`. **Límites:** no implementa el adaptador ni APIs (WS34/WS33), no autoaprueba, no simula; depende de WS34/WS35 y de gates.

## AMBIGUEDADES
1. «Respuesta vinculada al intento y operación confirmada»: no define quién confirma, con qué evidencia ni cómo se comprueba. Obligaría a inventar si la confirmación viene del adaptador, de un acta humana o del test.
2. «revisión con actor/evidencia visible» y «la revisión muestra actor humano»: el glosario define «Revisión / before-image: hash con que una escritura prueba que partió del estado actual». El uso equívoco obligaría a inventar si «revisión» es pantalla, historial o control de escritura.
3. «registrar decisiones con WS33.2»: WS33.2 no figura definido en el nodo ni en `depends_on` (solo WS34/WS35). Aunque las reglas comunes cubren contratos ausentes, no queda claro el canal de registro; obligaría a inventar si es llamada directa o vía WS35/WS34.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS36, aristas WS34/WS35/WS37, gates e instrucción. **Cambios previstos:** código en `graph_ui:frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador WS34 y `tests/`; registro de decisiones con WS33.2; vista de revisión con actor/evidencia. **Dependencias:** WS34, WS35; G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT `per_delta`; contrato WS12; evidencia WS33.1/WS33.2. **Validaciones futuras:** tests de respuesta vinculada, confirmación, actor/evidencia, error por API/permisos ausentes y ausencia de autoaprobación/simulación; WS37 hará validación humana real. Nada ejecutado.

## FUTURO
WS34 produce adaptador, ruta y confirmación; WS33/WS33.1/WS33.2 producen decisión y evidencia; WS12 fija el contrato técnico por delta; el receptor P01 emite el acta G_UI_WRITE por delta; WS44/operador y solicitante resuelven G_SCION/G_EXEC; el TaskDoc de promoción fija archivos, textos y pruebas; WS37 ejecuta la validación humana.
