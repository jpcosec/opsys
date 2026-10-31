REFORMULACION
Propósito: fijar WS33.1 como encargo de implementación para vincular mensajes y resultados de Scion a un intento existente, con deduplicación y procedencia. Resultado: adaptador backend documental en `deskops` que registra referencias Hub/proyecto/conversación/mensaje/intento y resultados, deduplica según las claves indicadas y deja huecos de procedencia para mensajes no vinculables. Repo dueño: `deskops`. Límites: no editor UI, no tablas Scion, no dispatch/reply; contrato público real, G_SCION, WS32 y la comprobación en WS05/WS44 son prerrequisitos; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: `dag.yaml` (WS33.1, WS32, WS33 y gates), guía, brief, alcance, decisiones, cobertura y reconciliación; los bloques edge se toman como contratos, no se revisan. Cambios previstos: `runtime/` mediante adaptador definido por contrato, modelos/reportes y `tests/`; sin tocar tablas Scion. Dependencias: WS32 aporta identidad/cierre; G_SCION lo produce WS44 y sigue `unverified`; WS05 inventaría el identificador de fuente. Si falta contrato, API, dato o permiso, aplica la regla común: detenerse y registrar el hueco con repo dueño. Validaciones futuras: importación repetida con mismo Hub/proyecto/conversación no duplica mensajes ni resultados ni atribuye una conversación completa a un intento; los mensajes no vinculados quedan como hueco de procedencia; no se tocan tablas Scion. Sin ejecutar nada.

FUTURO
WS05/WS44 deben aportar inventario/probe y contrato público; WS32 fija la identidad de intento; WS33.2 registra la decisión humana; WS34/37 correlacionan estados reales bajo G_EXEC; el responsable humano acepta el delta con acta en el repo dueño. Nada de ello es ambigüedad de este nodo.
