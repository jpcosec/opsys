## REFORMULACION
**Propósito:** encargo de implementación de un adaptador público restringido para *dispatch* Scion en `deskops`, con confirmación entendida como respuesta de la API de Scion, identidad de intento, timeout/errores y autoridad del coordinador según el contrato WS12.

**Resultado:** adaptador en `runtime/`, comando `cli/commands/runtime.py` o la API que fije WS12, y pruebas en `tests/`. Sin shell arbitrario ni duplicación de transporte.

**Repo dueño:** `deskops`. Depende de WS33 —vínculos de mensajes/resultados/decisiones— y WS12 —contrato de operaciones—. Requiere G_EXEC, G_SCION y G_WRITE_CONTRACT. Estimación M.

**Límites:** no ejecutar en planificación; promoción no autorizada; la aceptación exige agente real con un dispatch aceptado y otro rechazado o vencido por timeout. Los gates pendientes son intencionales.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas:** nodo WS34.1 y gates en `dag.yaml`; guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`. Los bloques de nodos vecinos se leen solo como contexto contractual y no se revisan.

**Cambios previstos:** implementar adaptador de dispatch, comando/API y tests; nada ejecutado.

**Dependencias:** WS33 —incluye WS33.1/WS33.2— y WS12. G_WRITE_CONTRACT se evalúa por delta para WS34.1; G_SCION es producido por WS44 mediante probe real; G_EXEC requiere autorización humana de agente/proyecto/acciones/sesión. Si falta contrato, API o permiso: detenerse, registrar el hueco con repo dueño y no crear sustituto.

**Validaciones futuras:** agente real demuestra dispatch aceptado y otro rechazado o vencido por timeout; confirmación ligada a respuesta de API Scion; identidad de intento; timeout/errores; autoridad WS12; ausencia de shell arbitrario y de transporte duplicado. El TaskDoc de promoción fijará archivos, escenarios y preflight.

## FUTURO
- **WS44:** produce G_SCION con probe real, Hub/endpoint/identidad/capabilities y operador designado.
- **Solicitante/designee:** otorga G_EXEC para el escenario concreto.
- **WS12:** publica el contrato por delta y el recibo de G_WRITE_CONTRACT; si falta API, registra hueco y dueño.
- **Promoción:** otro nodo/humano autoriza TaskDoc, archivos, pills, atoms y evidencia.
- **WS34.2:** consume WS34.1 para el adaptador de respuesta; WS34 cierra como agregado.
- **WS36/WS37 y aceptación de producto:** intervención UI y recepción técnica por delta en repo dueño.
