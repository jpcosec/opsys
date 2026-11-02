## Separación de fuentes

- **Lectura propia:** TaskDoc, `preflight-disposition.md`, `vistas.md`, `vistas-antes.md`, `result-summary.md`, `comparison-ledger.md`, `dag.yaml` (tramos citados), `manual.md`, `user-flows.md`, las tres auditorías, `validacion-humana.md`, `borradores/vision.md:36`.
- **Dato del Supervisor (`tester-facts.log`), no verificado por mí:** HEAD `d343fbfe`, revisiones al día, tabla/diagrama coinciden con `dag.yaml`, 13 tests pasados, hash de `vistas.md`, 1 revisión de 73 renovada, `dag.yaml` sin líneas fuera de `evidence`/`input_sha256`.
- **No ejecuté nada:** ni tests, ni build, ni validate, ni git.

## Pérdidas y completitud

- **Pérdidas:** comparé por lectura `vistas-antes.md` con las líneas 1-46 de `vistas.md`: título, tablas, reglas, «Ficha de cada vista», «Filas que faltaban» y párrafo final están intactos. PASS.
- **Filas:** las 12 filas de la tabla 1 y las 8 de la tabla 2 tienen ficha. F11, F18 y F19 se separan en a/b. PASS.
- **Campos:** las 23 fichas contienen los 14 campos exigidos. PASS.

## Tabla de comprobación

| Objeto | Fuente | Evidencia real archivo:línea | Resultado |
|---|---|---|---|
| F15: FAQ sí figura en WS40 y WS09 | `dag.yaml` | `dag.yaml:620` (WS09, FAQ), `dag.yaml:2690` (WS40, FAQ Markdown) | PASS; la negación anterior quedó corregida |
| F14: `user-flows.md` no menciona issues | `user-flows.md` | grep de `issue` sin coincidencias relevantes; solo líneas 36-246 no issues | PASS |
| F15: `user-flows.md` no menciona FAQ | `user-flows.md` | grep de `FAQ/faq` sin coincidencias | PASS |
| F18a: `user-flows.md` no menciona specs/notaciones | `user-flows.md` | grep de `spec/Spec/notaci/Notaci` sin coincidencias sustantivas | PASS |
| F18b: `user-flows.md` no menciona ViewDoc | `user-flows.md` | grep de `ViewDoc` sin coincidencias | PASS |
| F14: `desk/issues` ausente y `desk/drawer/issues` vacío | `deskops.md` | `deskops.md:232` | PASS |
| F14: no modelados por visión | `borradores/vision.md` | `vision.md:36` dice «issues Markdown deliberadamente no modelados» | PASS |
| F12: consulta guardada ausente | `infraestructura.md` | `infraestructura.md:121` | PASS; no hay productor claro en `dag.yaml` |
| F11a/F18a/F19a: etiqueta `propuesto` | disposición y fichas | F11a `vistas.md:236` con identidad/renderer/navegación «no definido; productor WS11» (`:228,231,232`); F18a `:372` con renderer/navegación WS11 (`:367-368`); F19a `:406` con identidad WS11 (`:398`) | **FAIL**: la ficha usa contratos WS11 pendientes; por la disposición debería ser `bloqueado` |
| F18a: contrato | `vistas.md` | `:365` dice «Contrato: SpecDoc y NotationDoc registrados»; `:372` dice «sin evidencia completa ni contrato» | **FAIL**: contradicción interna |
| F11b: conversación Scion atribuida a WS44 | `dag.yaml`, `user-flows.md` | `dag.yaml:2837-2849` define WS44 como probe/validación de acceso; `vistas.md:244` le atribuye la conversación; `user-flows.md:154` habla de acceso/contrato Scion, no de conversación | **FAIL**: correspondencia no soportada |
| F14: lista `issue list` en UI | disposición de productores | `vistas.md:299` asigna «productor WS11» a una implementación de lista; WS11 es contrato de navegación (`dag.yaml:681-711`) | **FAIL menor**: debe ser «sin productor en el DAG» con repo dueño |
| F18a: vista Specs | disposición de productores | `vistas.md:367` asigna «productor WS11» al renderer de Specs; ningún nodo del DAG lo produce | **FAIL menor**: falta producto de implementación o «sin productor en el DAG» |
| ViewDoc no es contrato universal | `vistas.md` | `:263`, `:379` | PASS |
| No se crea otro workspace | `vistas.md` | `:61`, `:78`; no aparece «otro workspace» | PASS |
| Code/origen/foco solo con soporte real | `vistas.md` | `:346-355`; `ui.md:55,77`; `dag.yaml:857-859` | PASS |
| Conteos 20/3/0 | `result-summary.md` y fichas | 20 bloqueadas, 3 propuestas, 0 disponibles según etiquetas escritas | PASS aritmético; **no** respecto a la regla por los FAIL anteriores |
| Clases 20/22/14 | `result-summary.md` y fichas | authored 20; derivado 22; preferencia local 14 | PASS |
| Ledger: no afirma haber comprobado contenido de las 365 citas | `comparison-ledger.md` | «no comprobé el contenido de cada línea citada» | PASS; no excede lo declarado |

## Citas abiertas (mínimo 25, repartidas)

- F01: `ui.md:54-57,69,87`; `deskops.md:101,185-201,195,220`; `infraestructura.md:88,92`; `user-flows.md:13-33,233`.
- F02: `infraestructura.md:30-33,51-56`; `ui.md:55,57,63-64`; `reconciliacion.md:5,15`; `user-flows.md:63,83`.
- F04: `deskops.md:87,98,134,259`; `ui.md:67,77-79`; `decisiones.md:29`.
- F05: `deskops.md:196,200,219,235`; `dag.yaml:1537-1546`; `manual.md:125-129`.
- F07: `deskops.md:38-43,83,189,216`; `ui.md:71`; `dag.yaml:1652`.
- F09: `deskops.md:190,206`; `ui.md:88`; `infraestructura.md:90`.
- F11a: `deskops.md:197,199,221-222`; `user-flows.md:147,214`.
- F11b: `deskops.md:141-142,198`; `ui.md:82-84`; `user-flows.md:145-157`; `dag.yaml:2136,2276,2499,2532,2842`.
- F12: `infraestructura.md:110-115,121`; `ui.md:58,60-61,80`; `user-flows.md:173,181`.
- F14: `deskops.md:48-49,232`; `ui.md:55`; `vision.md:36`.
- F15: `deskops.md:33,188,233`; `dag.yaml:356,620,2690`.
- F18a: `infraestructura.md:35,100,132,134`; `dag.yaml:1225`.
- F18b: `infraestructura.md:149-153`; `ui.md:104-108`; `dag.yaml:1212-1244`.
- F19b: `ui.md:85`; `dag.yaml:2630-2660`; `manual.md:163`.
- F20: `infraestructura.md:60`; `ui.md:77,158`; `dag.yaml:1887`.
- Auditorías: `deskops.md:41,100,188,197,199,232,233`; `infraestructura.md:33,51-57,60,88-94,121,149-153`; `ui.md:55-58,67-71,77-85,87-88,104-108`.
- `user-flows.md`: 13, 30, 44, 47, 49-50, 63, 83, 101, 107, 145, 147, 154, 171, 173, 177, 181, 192, 198, 200, 214, 233.
- `manual.md`: 41-47, 125-129, 163.
- `validacion-humana.md`: secciones de gates y «Qué significa disponible».

## Qué no pude verificar

- No abrí código de `graph_ui`, `sldb`, `spec2viz`, `pron` ni `scion`.
- No ejecuté tests, build, validate, status ni `git diff`.
- No leí el `dag.yaml` completo ni las 365 citas; solo tramos y citas citadas.
- No verifiqué actas humanas: solo comprobé que `validacion-humana.md` y `manual.md` dicen que no constan.

RESULTADO: FAIL
