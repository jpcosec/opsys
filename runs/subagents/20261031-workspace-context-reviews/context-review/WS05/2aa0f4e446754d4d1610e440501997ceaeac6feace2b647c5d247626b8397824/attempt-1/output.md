## REFORMULACION
Propósito: inventariar la identidad Scion (slug, agente, intento, dispatch, mensaje, conversación) y su API pública (endpoints/SDK documentados o exportados; no tablas ni funciones internas), incluidos roles, scopes y operaciones autorizadas. Resultado: `auditoria/scion.md`, con esos conceptos separados, campos internos no públicos señalados, capabilities que exigen API real y marca de las requeridas por WS32/WS33. Repo dueño: deskops; lee además `../scion`. Límites: solo lectura de código, documentación y configuración sin secretos; sin endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración. WS05 no produce G_SCION; eso es de WS44.

## AMBIGUEDADES
Ninguna. El alcance fija lectura, salida y aceptación; la ausencia de API pública se resuelve señalando el hueco, y las reglas comunes de `alcance.md` cubren la falta de contrato/API.

## DRY-RUN
Lecturas: `dag.yaml` (WS05 y aristas WS32/33/44 como contexto), `brief.md`, `alcance.md`, `decisiones.md`; árbol y documentación de `../scion`; `runtime/templates/RunDoc` y configuración sin secretos en deskops.
Cambios: crear `auditoria/scion.md` bajo `output_base` con: identidades separadas; superficie pública (endpoint/SDK, firma, export); matriz roles/scopes/operaciones; campos internos fuera de API; capabilities que requieren API real; mapa capabilities→WS32/WS33; huecos con repo dueño.
Dependencias: consume brief/glosario de WS01; no consume WS12 ni WS44. Gates: ninguno exigido; G_SCION permanece `unverified`.
Errores: si falta `../scion` o no hay API pública documentada/exportada, registrar el hueco con repo dueño y no inventar interfaz; si no hay tabla interna, declararlo. Sin llamadas de red ni tokens en la salida.
Validación futura: revisar el documento contra la aceptación (separación, campos internos marcados, capabilities WS32/33) y confirmar ausencia de secretos y contactos vivos.

## FUTURO
WS44 ejecuta el probe real y produce G_SCION; WS12 fija el contrato del registro por intento; WS32/WS33 consumen el inventario para identidad y mensajes. La promoción (task-only preflight, archivos/pills) queda a decisión humana; el operador Scion se designa al abordar el ramal E.
