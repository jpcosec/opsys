REFORMULACION
Propósito: vincular mensajes y resultados a un intento existente, con deduplicación y procedencia, en el backend documental. Resultado: adaptador en `runtime/`, modelos/reportes y tests que importan referencias Hub/proyecto/conversación/mensaje/intento y resultados; lo no resoluble se registra como hueco. Repo: `deskops` (`deskops:repository_root/`). Límites: backend documental, independiente de editor UI; no tocar tablas Scion; no duplicar; no atribuir una conversación completa a un intento; promoción no autorizada. Depende de WS32 y G_SCION.

AMBIGUEDADES
1. «una importación repetida (mismo Hub/proyecto y conversación, con checkpoint)». No se define qué es el checkpoint ni quién lo emite. Obligaría a inventar cómo se simula o reanuda y qué evidencia demuestra la idempotencia; la aceptación deja de ser comprobable sin esa decisión.
2. «Los resultados se identifican por intento y por el identificador que exponga la fuente ... con la misma regla de deduplicación y procedencia». La clave explícita es «Hub + proyecto + id de mensaje»; para resultados no se fija una clave equivalente. Obligaría a inventar si la deduplicación usa Hub+proyecto+intento+id de fuente u otra combinación, y cómo resolver colisiones.

DRY-RUN
Lecturas previstas: nodo WS33.1, aristas WS32/WS33/WS33.2, gates, guía, brief, alcance, decisiones, cobertura, reconciliación y `task_file` cuando exista. Cambios previstos: adaptador en `runtime/`, modelos/reportes y tests en `deskops`; sin UI ni tablas Scion. Dependencias: WS32 para identidad/cierre; G_SCION vía WS44; identificación de resultados vía WS05/WS44. Validaciones futuras: importación repetida con checkpoint, no duplicación de mensajes/resultados, no atribución de conversación completa a un intento y no escritura en tablas Scion. Sin ejecutar nada.

FUTURO
WS44 ejecuta el probe real y produce G_SCION; WS05 inventaría la fuente; WS32 fija identidad de intento, manifiesto y cierre; WS07 designa al operador Scion. El TaskDoc de promoción fijará archivos, escenarios y textos de prueba. El humano resuelve las Pxx y gates aplicables. Nada de esto es ambigüedad del nodo.
