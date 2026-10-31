REFORMULACION
Propósito: convertir los user-flows en un encargo de planificación comprobable. Resultado: `borradores/user-flows.md` con, por cada UF, entrada/salida, operación, error, nodo del DAG y gate humano. Repo dueño: `deskops`. Límites: no implementar; no prometer funciones fuera de `alcance.md`; operación ausente se registra como hueco, no se inventa; UF08 es solo lectura y el envío interdesk queda fuera del baseline; no se sustituyen decisiones Pxx.

AMBIGUEDADES
1. «cubrir manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado»: no asigna UF a «cambios» ni a «modo degradado». Obliga a inventar si «cambios» es WS29/impacto, UF08 o edición, y en qué UF se documenta el modo degradado.
2. «ack local disponible según contrato»: no nombra el contrato ni su productor; WS12 (`contratos/operaciones.md`) depende de WS08. Obliga a inventar el contrato o a dar por disponible una operación no verificada, contra la regla de marcar hueco.
3. «Mapear UF a operaciones de WS02/03/04» frente a «Las operaciones vienen de auditoria/{deskops,infraestructura,ui}.md»: no fija si la autoridad es el nodo o el archivo de auditoría. Obliga a decidir qué operación citar cuando solo una fuente la contiene.

DRY-RUN
- Lecturas: guía, brief, alcance, decisiones, cobertura, validacion-humana, borrador user-flows, nodo WS08, contratos vecinos y gates.
- Cambios previstos: solo `borradores/user-flows.md`; completar las seis columnas por UF y marcar huecos.
- Dependencias: G_PRODUCT vía WS07; auditorías vía WS06/WS07; operaciones de WS02–04; gates de validacion-humana; matriz de cobertura.
- Validaciones futuras: aceptación del nodo (cada UF completa, sin promesas fuera de alcance); consumo por WS11/12; gates humanos WS16/30/37/39; preflight de TaskDoc. Nada ejecutado.

FUTURO
WS07 registra G_PRODUCT, `source_mode` y responsables. WS11/12 consumen el mapeo. WS16/30/37/39 ejecutan gates humanos. WS40 produce el corpus. WS43 publica. El TaskDoc de promoción fija archivos, pills y evidencia. El humano decide P01/P04/P07/P08.
