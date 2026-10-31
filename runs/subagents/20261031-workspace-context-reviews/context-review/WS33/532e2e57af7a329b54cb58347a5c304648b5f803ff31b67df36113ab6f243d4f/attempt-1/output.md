## REFORMULACION
- **Propósito**: agrupar dos entregas de vinculación documental: mensajes/resultados al intento (WS33.1) y registro de decisión humana explícita (WS33.2), con deduplicación y procedencia.
- **Resultado**: agregado no ejecutable; su salida es la de WS33.1 y WS33.2. Cierra cuando ambos hijos cumplen su aceptación; sus dependientes siguen colgando de WS33.
- **Repo dueño**: `deskops`, con `output_base: deskops:repository_root/`.
- **Límites**: backend documental, independiente del editor UI; no tocar tablas Scion; no duplicar transporte. Depende de WS32, WS11 y del gate G_SCION.

## AMBIGUEDADES
Ninguna. La aceptación del agregado es comprobable por la aceptación de sus hijos; el repo y el gate están identificados; el actor de G_SCION se designa en WS07 y lo produce WS44; los detalles de contrato, deduplicación y campos se delegan expresamente a WS33.1/WS33.2 o al TaskDoc. Que G_SCION esté `unverified` es intencional, no un defecto.

## DRY-RUN
- **Lecturas previstas**: nodo WS33 y sus hijos en `dag.yaml`; contrato de identidad de intento de WS32; `contratos/navegacion.md` de WS11; evidencia de G_SCION producida por WS44; designación del operador Scion en WS07; contrato de actor/operación de WS12; inventario de WS05.
- **Cambios previstos**: ninguno propio. No se escriben archivos ni se ejecuta importación; solo se verificaría la evidencia de cierre de WS33.1/WS33.2.
- **Dependencias**: WS32, WS11, WS33.1, WS33.2 y G_SCION. La matriz WS06 llega de forma transitiva por WS11/WS12 según `integration_mode`.
- **Validaciones futuras**: importación repetida sin duplicar mensajes/resultados; conversación completa no atribuida a un intento; mensaje multi-intento o sin intento no vinculado y registrado como hueco; decisión con actor humano, referencia a intento/tarea y resultado aprobar/pedir corrección; `completed` nunca como aprobado; tablas Scion intactas; G_SCION comprobado.

## FUTURO
- WS44, con operador designado en WS07, produce G_SCION; sin probe real el nodo queda bloqueado.
- WS12 fija la operación y el actor humano; si falta, se registra hueco con repo dueño.
- WS05/WS44 aportan el identificador de resultados y el contrato público real.
- La promoción sigue `not_authorized` hasta autorización humana; WS34 y WS35 consumen este agregado.
