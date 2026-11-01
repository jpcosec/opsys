## REFORMULACION
**Propósito:** definir el encargo de vincular mensajes y resultados de Scion a un intento existente, con deduplicación y procedencia.
**Resultado:** backend documental en `deskops` que registra referencias Hub/proyecto/conversación/mensaje/intento y resultados, sin duplicar ni atribuir conversaciones completas a un intento.
**Repo:** `deskops`; `output_scope: runtime/ (adaptador definido por contrato); modelos/reportes; tests/`.
**Límites:** no tocar tablas Scion; depende de WS32 y de los gates G_SCION/G_WRITE_CONTRACT; solo vincula lo que tenga id de intento existente; lo no resoluble queda como hueco de procedencia.

## AMBIGUEDADES
Ninguna.

El nodo nombra a WS05/WS44 para comprobar identificadores de fuente y a WS12/G_WRITE_CONTRACT para el canal; el caso sin intento resoluble está definido como hueco. La aceptación es comprobable mediante importación repetida y ausencia de duplicados/atribución indebida.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (nodo, arista WS33, gate G_WRITE_CONTRACT), guía, brief, alcance, decisiones, cobertura, reconciliación y referencia externa Scion. Sin ejecutar nada.
**Cambios previstos:** implementar la vinculación en `runtime/` según contrato; modelos/reportes de procedencia; pruebas en `tests/`. No tocar tablas Scion.
**Dependencias:** WS32 produce identidad de intento/RunDoc; G_SCION depende de WS44; G_WRITE_CONTRACT se verifica por delta desde WS12; WS05/WS44 aportan el identificador de fuente. Si falta contrato o API, detenerse y registrar hueco con dueño.
**Validaciones futuras:** importación repetida mismo Hub/proyecto/conversación sin duplicar mensajes ni resultados; mensajes sin intento o con varios quedan como hueco; no atribuir una conversación completa a un intento; conservar procedencia; pruebas con contrato público real y recibo por delta.

## FUTURO
- WS44 ejecuta el probe real de Scion y produce la evidencia de G_SCION.
- WS12 fija el contrato técnico de la operación y el actor.
- WS32 entrega identidad de intento, manifiesto/RunDoc y cierre idempotentes.
- WS05 inventaría la API Scion sin sustituir a WS44.
- Una persona designa al operador Scion al abordar el ramal E.
- WS37 valida con agente real; WS34/37 prueban estados Hub reales bajo G_EXEC.
