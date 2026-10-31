## REFORMULACION
**Propósito:** encargo de implementación de un adaptador público restringido para dispatch Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.  
**Resultado:** código en `runtime/`, comando `cli/commands/runtime.py` o API, y `tests/`.  
**Repo dueño:** `deskops` (`output_base: deskops:repository_root/`).  
**Límites:** depende de WS33 y WS12; exige G_EXEC, G_SCION y G_WRITE_CONTRACT; no shell arbitrario ni duplicar transporte; no incluye reply (WS34.2); `promotion: not_authorized`; esta revisión no ejecuta.

## AMBIGUEDADES
1. **“con confirmación, identidad de intento, timeout/errores y autoridad del coordinador”** (scope): no se especifica quién confirma ni por qué canal —humano, CLI o coordinador— ni qué autoridad concreta del coordinador debe verificarse. El ejecutor tendría que inventar el actor y el mecanismo; WS12 produce “policy coordinador”, pero el nodo no remite a un contrato concreto.
2. **“agente real demuestra aceptación y fallo”** (acceptance): “fallo” no define escenario ni evidencia exigida —rechazo, timeout, error de transporte—. Sin precisar el caso negativo, la aceptación no es comprobable sin inventar qué fallo demostrar.
3. **“timeout/errores”** (scope): no hay valores, taxonomía ni criterio de aceptación para timeouts/errores; el ejecutor debe inventar umbrales y clases de error.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS34.1, edges WS33/WS12/WS34/WS34.2 y gates.  
**Cambios previstos:** ninguno; es revisión de encargo.  
**Dependencias:** WS33 (agregado de referencias), WS12 (contrato de operaciones/escritura), G_EXEC (humano), G_SCION (WS44), G_WRITE_CONTRACT (WS12).  
**Validaciones futuras:** agente real demuestra dispatch aceptado y fallo; comprobar ausencia de shell arbitrario y de transporte duplicado; verificar identidad de intento, timeout/errores y autoridad del coordinador; la promoción exigirá archivos, pills, evidencia y preflight task-only.

## FUTURO
WS12 debe producir whitelist, canal/actor y política del coordinador; WS33 debe entregar referencias de mensaje/intento/resultado; WS44 debe probar la API pública y producir G_SCION; un humano debe resolver G_EXEC y las Pxx aplicables. La promoción de WS34.1 definirá archivos exactos, pills y evidencia; WS34.2 consumirá este adaptador para reply. Nada de esto se ejecuta aquí.
