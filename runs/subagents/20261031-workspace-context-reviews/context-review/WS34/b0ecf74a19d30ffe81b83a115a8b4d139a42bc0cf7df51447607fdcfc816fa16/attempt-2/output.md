## REFORMULACION
**Propósito:** revisar WS34 como encargo de planificación: adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.  
**Resultado:** WS34 es `aggregate` no ejecutable; su aceptación se cumple cuando WS34.1 y WS34.2 cumplen la suya. No produce entregable propio.  
**Repo:** `deskops`.  
**Límites:** no ejecutar dispatch/reply ni mutaciones; no revisar bloques edge; no inventar permisos Scion, aprobación de implementación/API ni contratos. WS12 y WS33 son dependencias nombradas.

## AMBIGUEDADES
Ninguna. El nodo es un agregado que no se ejecuta y delega el contenido operativo en WS34.1/WS34.2; repo, dependencias, gates y aceptación por hijos están definidos. La autoridad del coordinador remite al contrato WS12, y las reglas comunes ya indican detenerse si falta contrato, dato o permiso.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` de WS34, WS34.1, WS34.2, WS12 y WS33; gates `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`; reglas de `alcance.md`.  
**Cambios previstos:** ninguno; WS34 no ejecuta ni modifica archivos.  
**Dependencias:** WS33, WS12, WS34.1 y WS34.2; gates externos pendientes.  
**Validaciones futuras:** comprobar aceptación de ambos hijos, contrato WS12 por delta y evidencia de gates; no hay validación propia adicional para el agregado.

## FUTURO
WS12 debe producir el contrato técnico de operaciones/escritura y autoridad del coordinador. WS33 debe producir referencias y decisión humana. WS34.1/WS34.2 deben demostrar dispatch/respuesta autorizados, identidad de intento y timeout/errores según sus aceptaciones. WS44 debe aportar `G_SCION`; una persona debe registrar `G_EXEC` y los recibos por delta de `G_WRITE_CONTRACT`. La recepción técnica se verifica por nodo/efecto, no por aceptación conjunta.
