# Concilio y registro de correcciones

Ronda 1: tres sesiones recién abiertas en Herdr recibieron el mismo paquete sin historial de este chat ni conclusiones de pares. Claude leyó además memoria persistente del proyecto: su dictamen no es prueba de aislamiento estricto. Informes disponibles en r1/; el de Gemini conserva captura de terminal porque no se recuperó aún el Markdown completo. Los informes versionados no incluyen pantallas de configuración de credenciales.

## Resolución de hallazgos R1 en revisión 2

| Hallazgo | Corrección |
|---|---|
| Chat invisible como requisito | brief.md autocontenido con extractos del solicitante, glosario y límites de lo acordado |
| Fuentes/tickets ausentes | external_references con rutas actuales/hash; WS04/06 y G_UI reconcilian deltas con Board activo |
| Unidad documento/nodo/vista confusa | brief.md y WS11: documento conserva identidad, nodos no documentales conservan soporte; ViewDoc solo grafo |
| Backend/autoridad decididos por agente | decisiones.md enumera propuestas y actor humano; gates sin aprobación bloquean código |
| Tabla/YAML/candidatas inconsistentes | build_plan.py genera las tres proyecciones y --check detecta divergencia |
| Dependencias externas fuera del DAG | gates dibujados y validados, productores explícitos, estado pendiente no confundido con terminado |
| Escritura fuente evade workflow | WS12/20/21 + G_SOURCE/G_WRITE; campo protegido/roundtrip/conflicto y modo coordinador |
| Git/cierre/promoción indefinidos | propuestas P03–P06; cierre externo y verificación de resultado, no closeout commit HTTP |
| Validación humana demasiado tarde | WS16 lector temprano; WS30 autoría; WS37 delegación; participante/evidencia/protocolo definidos |
| Búsqueda/diff/dispatch/intervención faltantes | WS14/27/34/36 específicos |
| Errores inline mezclados con Changes | WS15 lector; WS29 extensión independiente |
| Manual bloqueado por Scion/Changes | WS31 básico después de uso manual; WS38 delegación posterior |
| Superficies omitidas | issues no modelados, crossroads/namespaces, FAQ/Step, Code, Schema y Specs explícitos; carpetas legacy auditadas por soporte |
| Tareas multi-repo sin dueño | cada nodo tiene un repo responsable; contratos/auditorías pueden leer otros repos pero no modificarlos |
| Desconocido/overreach | alcance.md delimita bootstrap CLI, multi-desk lectura y exclusiones; no reintroduce KGDB retirado ni migra Kimun |

Los seguimientos R2+ son revisiones iterativas del mismo concilio, no nuevas sesiones de contexto cero. No se muestran dictámenes de pares antes de responder. Un acuerdo del concilio no sustituye Pxx, G_UI, G_EXEC ni pruebas humanas futuras.

## Ronda 2 -> revisión 3

Claude y DeepSeek pidieron correcciones locales; Gemini consideró apto el plan sujeto al mismo gate circular y ajustes. Se separaron G_WRITE_POLICY (WS07) y G_WRITE_CONTRACT (WS12); los productores viven ahora en YAML y el grafo de gates no contiene ciclo. G_UI_READ/WRITE, G_SLDB_WRITE y G_SPEC_VIEW se aceptan tras definir el delta, con responsable receptor identificado por humano; WS06 solo propone matriz.

Se añadieron WS40 (productor único de corpus temporal), WS41 (lectura entre desks), WS42 (operaciones de conocimiento) y WS43 (publicación de navegación real después del ejemplo). Explorador y divisiones están explícitos en WS13. UF10, relaciones, split/merge, capa lista y enrutamiento tienen aceptación. Mutaciones requieren gate humano de lectura. Source_mode tiene variantes explícitas: read_only no queda bloqueado por G_SOURCE; editable sí. UF08 queda read-only sin envío cruzado. Fuente, reglas y manual se alinearon con las propuestas y la publicación real.

Se retiró G_CLOSEOUT del contrato genérico de WS12 para no bloquear intake/ack: autoría/cierre/identidad de intentos conservan ese gate externo. Se añadió acta para ejecución Scion y prueba de modelos. La auditoría Scion puede concluir con API no disponible sin marcar su gate satisfecho.

## Ronda 3 -> revisión 4

Gemini y DeepSeek: apto como plan; Claude: dos correcciones locales. Se añadió WS40->WS41. WS44 tiene actor y responsabilidad de probe/reintento Scion; produce G_SCION y WS32 lo exige. Corregida errata WS42/WS39, alcance de aceptación de fixtures/multidesk por receptor, ejemplos con entrada mínima y actas en repo dueño. WS30 ahora nombra explícitamente UF01/índices. El validador tiene --check sin escrituras. source_mode read_only no exige aceptación de escritura sldb. No hubo cambios de alcance de producto ni aprobación de gates humanos.

## Ronda 4 -> revisión 5

Gemini aprobó. Claude detectó que graph_ui ignora runs/acceptance/: actas movidas a runs/subagents/workspace-documental-acceptance/, sin cambiar .gitignore ajeno ni forzar archivos. evidence_ref permite comprobar git check-ignore sobre cada acta. DeepSeek pidió que WS07/P01/G_PRODUCT, y no solo una nota, exijan designar operador Scion: ahora consta en alcance/aceptación/evidencia. WS05 inventaría; solo WS44 produce recibo del probe. Se aclaró ack/respuesta local en UF02.

## Resultado final R5

| Revisor | Veredicto | Bloqueantes residuales |
|---|---|---|
| Claude | APTO COMO PLAN | 0 |
| DeepSeek | APTO COMO PLAN | 0 |
| Gemini | APTO COMO PLAN | 0 |

Dictámenes completos en r5/. Se recogió además la sugerencia de versionar explícitamente las actas, no solo elegir rutas no ignoradas: validacion-humana.md exige commit/blob verificables. No implica que tales actas o aprobaciones existan hoy.

El criterio de parada es convergencia de los tres sobre la aptitud de planificación y validación estructural verde. Las propuestas de producto quedan pendientes en decisiones.md y no hay autorización de implementación. Se conservaron los dictámenes anteriores incluso cuando discrepan, sin convertir mayoría en prueba de código o aprobación humana. La verificación final incluye generación coherente, ausencia de ciclos con productores/variantes, links y rutas de evidencia no ignoradas.
