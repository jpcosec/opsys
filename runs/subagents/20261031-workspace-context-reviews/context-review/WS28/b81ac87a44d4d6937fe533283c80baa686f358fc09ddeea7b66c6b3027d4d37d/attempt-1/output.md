## REFORMULACION

**Propósito:** integrar en graph_ui la verificación de cierre de una tarea y el handoff explícito con evidencia, sin cerrar desde la UI.

**Resultado:** una vista/experiencia en `frontends/mindmap/views/workspace/review/` que ejecuta o consume `deskops closeout verify` por el canal que fije WS12, muestra los faltantes diagnosticados, ofrece handoff a `deskops closeout commit` por CLI en modo manual —o al coordinador si está activo— y refresca el estado desde deskops tras el cierre externo.

**Repo dueño:** `graph_ui`.

**Límites:** no hay commit ni close por HTTP en el baseline; comandos o solicitudes no equivalen a cierre; no se admite terminal embebido genérico. Depende de WS27 y WS12 y requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES

1. «G_HUMAN_READ aplica porque es una acción de escritura del baseline.» El gate G_HUMAN_READ está definido como «Persona aprueba recorrido de lectura», con evidencia de acta de lectura producida por WS16. Aplicarlo a un handoff de cierre obligaría a inventar si el acta de lectura satisface una aprobación de escritura/cierre o si WS28 necesita otra aprobación humana distinta, y cómo conciliar ambas definiciones.

## DRY-RUN

**Lecturas previstas:** nodo WS28, contratos de WS27 y WS12, definiciones de gates, `decisiones.md` (P03/P04), `alcance.md` (UF05 y reglas comunes), `cobertura.md`.

**Cambios previstos:** vistas de diagnóstico de closeout, componentes de handoff con evidencia, cliente del canal definido por WS12, refresco de estado y pruebas en `tests/`.

**Dependencias:** WS27 aporta diff/evidencia; WS12 aporta canal, whitelist y política de coordinador/Git; los cuatro gates deben estar satisfechos.

**Validaciones futuras:** contrato de closeout establecido (G_CLOSEOUT), contrato técnico verificado (G_WRITE_CONTRACT), delta aceptado en graph_ui (G_UI_WRITE), acta humana de lectura (G_HUMAN_READ), prueba con corpus WS40, aceptación manual de UF05 en WS30 y confirmación real mediante `deskops show task` más commit de cierre.

## FUTURO

WS12 produce el contrato/canal y la política concreta; WS16 produce G_HUMAN_READ; un actor externo satisface G_CLOSEOUT y ejecuta el commit; el humano o coordinador realiza el closeout; WS30 valida UF05; WS07 decide P03/P04; el TaskDoc de promoción fija archivos, textos y escenarios.
