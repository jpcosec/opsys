REFORMULACION
WS33 es un agregado no ejecutable del plan workspace-documental, en deskops. Agrupa WS33.1 —vincular mensajes y resultados de Scion al intento, con dedup Hub+proyecto+conversación+mensaje / Hub+proyecto+intento+fuente y procedencia— y WS33.2 —registrar decisión humana de aprobar o pedir corrección, ligada al intento y su tarea—. Resultado: ambos hijos aceptados; WS33 sigue siendo dependencia de WS34/WS35. Límites: backend documental, no editor UI, no tablas Scion, no dispatch/reply (WS34) ni despliegue Scion; G_SCION y G_WRITE_CONTRACT pendientes por delta; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
WS33 no se ejecuta: es agregado. Un ejecutor futuro lo cumpliría por hijos, en orden WS33.1 → WS33.2 (arista de dependencia), ambos tras WS32 y con G_SCION/G_WRITE_CONTRACT. WS33.1: leer identidad de intento/RunDoc de WS32 y el contrato de fuente (G_SCION; comprobación en WS05/WS44); crear adaptador en `runtime/`, modelos/reportes y `tests/`; importar mensajes/resultados, deduplicar por Hub+proyecto+conversación+mensaje y Hub+proyecto+intento+fuente, vincular solo a intento existente y dejar hueco de procedencia para no resolubles; no tocar tablas Scion. Transfiere a WS33.2 los vínculos intento↔mensaje/resultado con procedencia. WS33.2 consume esos vínculos y el actor/operación de WS12; escribe decisión con actor, intento, tarea y resultado aprobar/pedir corrección (con texto); `completed` nunca se registra como aprobado. Validación conjunta: reimportación idempotente sin duplicados ni atribución de conversación completa; decisión apunta a intento existente y su tarea; huecos visibles; ninguna tabla Scion modificada; WS34/WS35 pueden leer el resultado. Errores: gate/contrato ausente → detener y registrar hueco con dueño; intento no resoluble → hueco, no invención.

FUTURO
WS12 produce G_WRITE_CONTRACT por delta; WS44 produce G_SCION. WS34 consume WS33 para dispatch/reply; WS35 para la vista de ejecución; WS37 valida con agente real. Un humano/P01 decide la promoción y el TaskDoc; WS06 reconcilia. Nada de ello es ambigüedad de este nodo.
