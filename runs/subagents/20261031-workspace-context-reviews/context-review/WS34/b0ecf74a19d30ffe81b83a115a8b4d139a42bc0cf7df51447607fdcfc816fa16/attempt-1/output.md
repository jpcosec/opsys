## REFORMULACION

- **Propósito:** revisar si WS34, tal como está escrito, constituye un encargo de planificación comprensible.
- **Resultado:** dictamen de claridad, sin ejecutar ni promover el nodo.
- **Repo dueño:** `deskops`.
- **Límites:** solo se evalúa WS34; no se revisan los bloques edge de nodos vecinos ni se juzga el producto. WS34 es `aggregate`: no se ejecuta y termina cuando terminan sus hijos.

## AMBIGUEDADES

Ninguna.

WS34 no fija por sí mismo la definición operativa de confirmación, timeout o autoridad del coordinador, pero no obliga a inventar: su aceptación es agregada, sus hijos WS34.1/WS34.2 concretan confirmación, timeout y errores, y WS12 produce el contrato de autoridad. Las citas del alcance común resuelven la falta de contrato: «detenerse, registrar el hueco con repo dueño y no crear sustituto». Los gates pendientes son intencionales.

## DRY-RUN

- **Lecturas realizadas:** guía de revisión, brief, alcance, decisiones, cobertura y definiciones DAG de WS34, WS33, WS12, WS34.1, WS34.2 y gates.
- **Cambios previstos:** ninguno; esta revisión no modifica archivos.
- **Dependencias:** WS33, WS12, WS34.1 y WS34.2. Gates: G_EXEC, G_SCION y G_WRITE_CONTRACT (`per_delta`, incluye WS34).
- **Validaciones futuras, sin ejecutar:**
  - WS34.1: dispatch real aceptado y otro rechazado o vencido, correlacionado con intento WS32.1 y registros WS32.2; confirmación solo con respuesta observada del Hub.
  - WS34.2: respuesta vinculada al intento correcto; timeout reportado como fallo sin confirmación, con umbral del contrato WS12.
  - Sin shell arbitrario ni duplicación de transporte.
  - Cumplimiento agregado cuando ambos hijos cumplan su aceptación.

## FUTURO

- WS12 debe publicar el contrato de operaciones, autoridad del coordinador, errores y umbral de timeout; si falta, se registra hueco y la operación queda no disponible.
- WS33/WS32.1/WS32.2 aportan identidad de intento y registros.
- WS34.1 y WS34.2 producen las salidas agregadas.
- WS44 y el operador designado verifican G_SCION; un humano autoriza G_EXEC.
- La promoción de WS34 requiere TaskDoc, archivos, pills, átomos y preflight, y no está autorizada.
- WS36 consume únicamente el adaptador WS34.
