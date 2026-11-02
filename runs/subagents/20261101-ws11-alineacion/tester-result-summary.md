## Separación de fuentes

- **LECTURA PROPIA:** abrí completos `navegacion.md`, `review-source.md` (alineación), `patch.diff`, `review-source.md` y `review-source-2.md` de corrección, `task-ws15-1.md`, el bloque WS13.1/WS15.1 de `dag.yaml`, y el tester anterior. No ejecuté nada; no declaro comportamiento en runtime.
- **DATO DEL SUPERVISOR (no verificado por mí):** `tester-facts.log`: HEAD deskops `21004def`, graph_ui `134a665`, sldb `77bd6d00`, sha256 de `navegacion.md`, «Generated table/task files/diagram spec match dag.yaml», stale medido WS13/WS15/WS15.1. No calculé hashes ni ejecuté git/build.

## Parte 1 — Los cuatro puntos

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| 1. Serialización como ausencia del parámetro | review-source §1 | `navegacion.md:89` («viaja como **ausencia del parámetro de alias**») | PASS |
| 1. Sin excepción `?alias=local`; sigue E-MD1 | review-source §1 | `navegacion.md:89` («No existe `?alias=local`… sigue dando E-MD1 (8.5), sin excepción»); `navegacion.md:316` (E-MD1) | PASS |
| 1. ¿Contradice 3.2, 5.1, 5.3 u 8.5? | contrato | `navegacion.md:89`; `navegacion.md:146` (5.1, ausencia = desk del proceso); `navegacion.md:169-170` (5.3, clave con alias); `navegacion.md:316` (E-MD1). Sin contradicción: 5.2 paso 3a sigue siendo sintaxis de texto | PASS |
| 1. URL e historia conocen la equivalencia | review-source §1 | `navegacion.md:89` («URL e historia tratan la ausencia…»); `navegacion.md:146` | PASS |
| 1. `local:` en texto y componente `b` | review-source §1 | `navegacion.md:89` («si ese documento pertenece al alias externo `b`, el componente… es `b`»); `navegacion.md:153-162` (5.2, paso 3a y ejemplos) | PASS |
| 1. Alias configurado es el canónico | review-source §1 | `navegacion.md:89` («se usa su alias, que es el canónico»); `navegacion.md:93` | PASS |
| 1. Ninguna fuente nueva de permisos | review-source §1 | `navegacion.md:90-95` (solo configuración confiable del operador; registry no es autorización automática); `navegacion.md:89` no añade fuente | PASS |
| 2. Mismo par `(root.resolve(), store.resolve())` | review-source §2 | `navegacion.md:93` (literal) | PASS |
| 2. Sinónimos fuera del baseline | review-source §2 | `navegacion.md:93` («los sinónimos del mismo desk no están en el baseline») | PASS |
| 2. Validación de WS41, sin modelo ni nodo, sin valores | review-source §2 | `navegacion.md:93` («Validación (WS41)», «sin modelo ni nodo nuevos»); `navegacion.md:92` (valores los pone el operador) | PASS |
| 3. Actores de preparación en 5.4 | review-source §3 | `navegacion.md:189`: WS40 generador/fixture; Executor del consumidor en pruebas WS13.1/WS41; operador/responsable en uso real | PASS |
| 3. TaskDoc consumidora; UI no migra; sin comando ni productor; hueco/intake | review-source §3 | `navegacion.md:189` (TaskDoc identifica operación/versión/evidencia; UI no migra; no hay productor automático; hueco o intake, sin workaround) | PASS |
| 4. `output_scope` de WS15.1 incluye `shell/api.js` | review-source §4 | `dag.yaml:1061-1063`; `task-ws15-1.md:21`; `navegacion.md:264` | PASS |
| 4. Solo cambia eso; `depends_on`, `requires` y aceptación intactos | review-source §4 | `patch.diff` hunk `@@ -1058,8 +1058,10 @@` solo sustituye `output_scope`; `dag.yaml:1055-1058` (`depends_on: WS13`, `requires: G_UI_READ`), `dag.yaml:1066-1073` (acceptance) sin cambios; `task-ws15-1.md:3-8` sin cambios | PASS |
| 4. §7.3 lo dice; WS13.1 solo consume; sin dependencia nueva | review-source §4 | `navegacion.md:264` («WS13.1 consume ese resultado y no lo implementa… no crea una dependencia»); `dag.yaml:1061` no cambia `depends_on`/`requires` | PASS |

## Parte 2 — No regresión

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| `patch.diff` no toca otras superficies | patch | Solo 3 archivos: `navegacion.md` (3 hunks), `dag.yaml` (1 hunk), `task-ws15-1.md` (1 hunk) | PASS |
| A: C1-C3 navegación, C4 tarjeta pasiva | review-source corrección A | `navegacion.md:201-204` intactas | PASS |
| A: 6.1 dominio futuro y H-03/H-03b/H-04/H-05b | A | `navegacion.md:218-225`; `navegacion.md:364-365` intactos | PASS |
| B: 5.2 orden, `local:` una vez, tabla de ejemplos | review-source-2 §1 | `navegacion.md:153-162` sin cambios en el diff | PASS |
| C: 5.4 obligación de lectura sin mutaciones | review-source corrección C | `navegacion.md:187` intacto; la frase nueva `:189` añade actores, no altera (a)(b)(c) | PASS |
| D: 7.3 `request()` descarta status; delta WS15.1 | review-source corrección D | `navegacion.md:262` intacto; `:264` solo precisa `api.js`, `error.body`, compatibilidad y consumo de WS13.1. Es el cambio autorizado por el punto 4, no una regresión de D | PASS |
| D: 7.5 E1-E3/E7 | D | `navegacion.md:270-283` intactos | PASS |
| 8.5 E-MD1 no aplica al literal 3c | review-source-2 §3 | `navegacion.md:316` intacto y coherente con `:162` (E5) | PASS |
| Sección 10: authored/derivado/manifiesto WS40 | review-source corrección E | `navegacion.md:337-349` intacta; regla 5 `:348-349` mantiene manifiesto como derivado | PASS |
| H-05b tres capacidades distintas | corrección A | `navegacion.md:365` intacto | PASS |
| H-11 fuera de las cinco clases, sin modelo/nodo | review-source-2 §4 | `navegacion.md:371` intacto | PASS |
| H-14 lectura sin mutaciones y dueños | corrección C | `navegacion.md:373` intacto; `:189` lo desarrolla sin contradecirlo | PASS |
| H-16 composición graph_ui/WS41, no ampliar sldb | corrección B | `navegacion.md:374` intacto | PASS |
| C5b sin modelo obligatorio ni API lista | review-source-2 §2 | `navegacion.md:207` intacto | PASS |
| Sigue en borrador y «sin acta registrada» | contrato | `navegacion.md:3` («Estado: borrador… No está revisado»); `navegacion.md:397-410` («sin acta registrada» en todas las filas); `navegacion.md:416`, `:420` | PASS |

## Qué no pude verificar

- Los hashes, commits y `stale` de `tester-facts.log`: son dato del Supervisor, no los recalculé.
- Que la tabla o el diagrama generados coincidan con `dag.yaml`: no ejecuté el generador.
- Comportamiento runtime de `?alias=local`, `doc_status`, `open_store` o `request()`: solo leí contrato y diff.
- Que `surface` reconstruya el texto íntegro: el contrato mantiene la reserva y no lo afirma.
- Actas o aceptaciones fuera de las búsquedas declaradas en el contrato.

RESULTADO: PASS
