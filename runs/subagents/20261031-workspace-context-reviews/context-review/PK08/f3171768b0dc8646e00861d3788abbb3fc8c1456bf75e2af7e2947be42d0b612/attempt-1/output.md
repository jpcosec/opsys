## REFORMULACION
**Propósito:** definir el paquete opcional Scion como delegación posterior con intentos, trazas e intervención humana verificables, sin duplicar el pipeline Scion.  
**Resultado:** paquete integrado donde identidad de intento, manifiesto/RunDoc/cierre, mensajes/resultados/decisiones, adaptador autorizado, UI de trazas, validación real y capítulo de manual son consistentes, idempotentes y trazables.  
**Repo:** `deskops` como dueño del macroencargo; hijos en `deskops` y `graph_ui` según contrato.  
**Límites:** PK08 es agregación sin ejecución propia ni tareas/aristas nuevas; no autoriza dispatch, mensajes, permisos Scion ni aceptación de producto. G_SCION/G_EXEC siguen pendientes; sin acceso real el ramal queda bloqueado. No se revisan bloques edge vecinos ni se ejecuta nada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Ejecución hipotética por hijos:  
1. **WS44**, tras WS05/WS07: lee inventario y autorización; hace probe read-only; produce `auditoria/scion-probe.md` y G_SCION. Sin operador/acceso registrado, se detiene.  
2. **WS32**: recibe WS05, WS12 y G_SCION; WS32.1/32.2 prueban identidad de intento, manifiesto/RunDoc/cierre e idempotencia local sin red; entregan base de intento/cierre.  
3. **WS33**: recibe WS32 y WS11; produce referencias Hub/proyecto/conversación/mensaje/intento/decisión con procedencia y dedup.  
4. **WS34** y **WS35** pueden avanzar en paralelo: WS34 produce adaptador público restringido dispatch/reply con confirmación, timeout y autoridad; WS35 produce lectura UI de tarea-intento-conversación-resultado-decisión.  
5. **WS36**: integra WS34+WS35; UI invoca solo el adaptador y registra decisiones vía WS33.2, mostrando errores por ausencia de API/permisos.  
6. **WS37**: con WS36 y WS30, ejecuta UF06 real y deja acta humana en `runs/subagents/workspace-documental-acceptance/delegacion/`.  
7. **WS38**: con WS37 y WS31, publica capítulo y átomos enlazados.  

Integración/validación futura: correlacionar el mismo intento entre adaptador, UI y acta; comprobar idempotencia, dedup, procedencia, dispatch intent/confirmed y permisos explícitos; usar Hub real en WS34/37, sin mocks; `completed` no equivale a aprobado/cerrado.

## FUTURO
Un humano designa operador/acceso Scion y registra autorización; otro actor resuelve G_EXEC/G_SCION; WS37 produce acta real; WS31 aporta manual básico; los dueños de contratos/API entregan sus salidas. Nada de eso se ejecuta aquí.
