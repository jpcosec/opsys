## REFORMULACION

**Propósito:** registrar una decisión humana explícita —aprobar o pedir corrección— sobre un intento, con actor humano identificado y vínculo al intento y a su tarea.

**Resultado:** decisión almacenada con actor, referencia al intento/tarea y resultado explícito; “pedir corrección” exige el texto de la corrección. El `completed` del agente no se registra como aprobado.

**Repo dueño:** `deskops`.

**Límites:** este nodo solo escribe la decisión mediante la operación que fije el contrato WS12; si falta, hueco con dueño. No escribe los estados validado/cerrado de deskops ni el completado que reporta Scion. Depende de WS32, WS33.1 y G_SCION.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS33.2 y contratos vecinos WS32/WS33.1/gates.
- **Cambios previstos:** ninguno ejecutado. El nodo contempla adaptador en `runtime/`, modelos/reportes y `tests/`; la promoción fijará archivos exactos.
- **Dependencias:** WS32 aporta identidad y cierre de intento; WS33.1 vincula mensajes/resultados al intento; WS12 debe fijar la operación y la fuente del actor humano; G_SCION está `unverified` y lo resuelve WS44 con operador designado en WS07.
- **Validaciones futuras:** registrar una decisión con actor, intento, tarea y resultado; rechazar “pedir corrección” sin texto; comprobar que `completed` no equivale a aprobado; si falta la operación de WS12, registrar hueco con dueño y no habilitar la escritura; preflight task-only antes de promover.

## FUTURO

WS12 debe publicar la operación y la identificación del actor; WS44/WS07 resuelven G_SCION; WS32 y WS33.1 entregan los vínculos de intento y procedencia; el TaskDoc de promoción fija archivos, escenarios y textos. El agregado WS33 cierra cuando ambos hijos cumplen. Nada de esto se ejecuta ni se decide aquí.
