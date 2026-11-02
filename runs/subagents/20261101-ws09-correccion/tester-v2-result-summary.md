## Separación de fuentes

- **LECTURA PROPIA**: `fix-diff-11.txt`, `vistas.md` (448 líneas), `review-source.md`, `docs/faq.md`, `auditoria/deskops.md:33,188,232-234`, `dag.yaml:2680-2699`, `renovacion-1/tester-result-summary.md`.
- **DATO DEL SUPERVISOR** (no verificado): HEAD `109bde40`; reviews current; tabla/tareas/spec coinciden; sin código de producto; `13 passed in 1.36s`; SHA `411b5bc7…` de `vistas.md`.

## Tabla

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| Solo cambia el campo Error de F15 | `fix-diff-11.txt` | `fix-diff-11.txt:5` un único hunk `@@ -317,7 +317,7 @@`; `:13` única línea `-`; `:14` única línea `+`, ambas el campo Error | PASS |
| La línea cambiada es el Error de F15 | `vistas.md` | `vistas.md:309` (### F15), `vistas.md:320` = línea Error con el texto nuevo | PASS |
| `deskops.md:188` dice 0 DeskFAQDoc | `auditoria/deskops.md` | `deskops.md:188` «docs en indice local: 0» + «`deskops faq` NO lo usa» | PASS |
| `deskops.md:233` dice `desk/faq` vacío y 0 documentos | `auditoria/deskops.md` | `deskops.md:233` «EXISTE y esta vacio (0 archivos); `DeskFAQDoc` tiene 0 documentos» | PASS |
| `deskops faq` lee `docs/faq.md` | `auditoria/deskops.md` | `deskops.md:33` «Lee docs/faq.md (ruta por defecto)… No usa DeskFAQDoc» | PASS |
| `docs/faq.md` existe y contiene orientación | `docs/faq.md` | `docs/faq.md:12` «# deskops FAQ»; `:16` «first-use orientation layer»; secciones How do I… | PASS |
| WS40 crea un FAQ Markdown en el corpus | `dag.yaml` | `dag.yaml:2689-2691` «entrada mínima … su FAQ Markdown y documentos … dentro del corpus temporal» | PASS |
| Frase nueva se sostiene | `vistas.md` | `vistas.md:320` sin inferir ausencia de orientación desde 0 DeskFAQDoc | PASS |
| F05 ya corregido | `vistas.md` | `vistas.md:133` «no implica ausencia de pasos»; `:125` `steps` = prosa | PASS |
| F16 ya corregido | `vistas.md` | `vistas.md:337` «0 StepDoc solo niega esas instancias» | PASS |
| F14 «sin issues, la lista queda vacía» | `vistas.md`; `auditoria/deskops.md` | `vistas.md:295,303`; `deskops.md:232` «AUSENTE: desk/issues … desk/drawer/issues/ (0 archivos)» | PASS (ver nota) |
| Otros «0 instancias de modelo» | `vistas.md` | `:142` ProtoAtomDoc (0), `:329` StepDoc (0), `:380` ViewDoc (0): solo se declaran como origen, no niegan capacidad | PASS |
| 23 fichas bloqueado | `vistas.md` | 23 líneas `- **Estado**: bloqueado` en `vistas.md:66,83,100,117,134,151,168,185,202,219,236,253,270,287,304,321,338,355,372,389,406,423,440` | PASS |
| 14 campos por ficha | `vistas.md` | `vistas.md:56-69` (F01) 14 campos; `:430-443` (F20) 14 | PASS |
| Nota final sin patrón de negación por conteo | `vistas.md` | `vistas.md:447` «la lectura básica … reutiliza el lector Markdown o modelado» | PASS |

**F14, evaluación:** el listado vacío es salida directa de `issue list` sobre las dos únicas rutas que lee (`deskops.md:49,232`), no una inferencia de capacidad. No niega la existencia de issues ni la lectura genérica. No es el patrón prohibido.

**Nada más en el diff:** el cambio no toca `Estado`, `Origen`, `Evidencia` ni la nota final.

## No pude verificar

- No ejecuté `git diff`, `git status`, build, validate ni suite; el alcance del diff lo tomo solo de `fix-diff-11.txt`.
- No comprobé SHA `411b5bc7…`, HEAD `109bde40` ni «all reviews current» (dato del supervisor).
- No verifiqué que `dag.yaml` no tenga otros cambios fuera de `evidence`/`input_sha256`.
- No conté mecánicamente los 14 campos de las 23 fichas; verifiqué F01 y F20 y el patrón de línea.

RESULTADO: PASS
