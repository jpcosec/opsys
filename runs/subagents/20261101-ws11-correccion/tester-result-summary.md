## Separación de fuentes

- **LECTURA PROPIA:** abrí `patch-4.diff`, `navegacion.md` (§2.2, §3.2, §5.2, §5.3, §8.5), `review-source-2.md` y `renovacion-2/tester-result-summary.md`. No ejecuté nada; no declaro comportamiento en runtime.
- **DATO DEL SUPERVISOR (no verificado):** `tester-v3-facts.log`: HEAD deskops `76b77f5d`, sha256 de `navegacion.md` `b9db651e…c789`.

## Tabla

| Objeto | Fuente | Evidencia real | Resultado |
|---|---|---|---|
| ¿Una sola frase/ítem de §3.2.1? | LECTURA PROPIA | `patch-4.diff`: solo `navegacion.md`, un hunk `@@ -86,7 +86,7 @@`, un `-` y un `+` sobre el ítem 1; contexto ítems 2-4 intacto (`navegacion.md:89`, `:90-99`) | PASS |
| Precisión: el `+` sustituye el ítem 1 y añade dos oraciones al mismo ítem (no toca otros ítems) | LECTURA PROPIA | `navegacion.md:89` | PASS |
| `local` reservado y fuera del conjunto del operador | LECTURA PROPIA | `navegacion.md:92` («reservado en la sintaxis de enlaces, queda fuera del conjunto y el operador no puede redefinirlo»); `:155` (3a, «se reconoce antes que cualquier alias»); `review-source-2.md` punto 2 | PASS |
| `local` designa el desk de la petición de origen | LECTURA PROPIA | `navegacion.md:89` («designa el desk de la petición (5.2, paso 3a)»); `:155` («desk del documento que contiene el enlace… no el desk inicial del proceso si se está viendo otro desk») | PASS |
| Sin configuración no hay lectura cruzada | LECTURA PROPIA | `navegacion.md:97` (E-MD1 para parámetro explícito; enlace de texto 3c; «solo se sirve el desk del proceso»); `:160-167` (fila `[[b:TaskDoc/x]]` sin configuración → literal local, E5) | PASS |
| E-MD1 solo para el parámetro explícito | LECTURA PROPIA | `navegacion.md:315` (8.5, E-MD1 «Parámetro explícito de alias… No aplica al literal… es E5»); `:162` (3c/E5); `review-source-2.md` punto 3 | PASS |
| Clave de sesión sin colisiones | LECTURA PROPIA | `navegacion.md:175` (alias + identidad local, «dos desks con el mismo `Model:name` no colisionen»); `:92-93` (validación de alias único); `:89` (sin configuración `local`, un solo desk servido) | PASS |
| `local` no autoriza salto de store | LECTURA PROPIA | `navegacion.md:156` (envoltorio `local:` fuerza `split_doc_ref`→resto literal; `doc_ref.py:38-39`); `:161-164` (tabla: `local:foo:bar` y `b:local:x` literales, resto no reinterpretado); `:97` | PASS |
| Contradicción con §2.2 / §5.2 / §5.3 / §8.5 | LECTURA PROPIA | Sin contradicción en `navegacion.md:43-52`, `:148-171`, `:173-175`, `:312-318` | PASS |
| Coincidencia con `review-source-2.md` (dos ajustes, cinco resoluciones) | LECTURA PROPIA | `review-source-2.md` punto 1 (local antes de aliases, `local` reservado), 2, 3 (ámbito E-MD1/E5), 5 | PASS |
| HEAD y sha256 del supervisor | DATO DEL SUPERVISOR (no verificado) | `tester-v3-facts.log:1-2` | No verificado |

## Qué no pude verificar

- HEAD `76b77f5d` y sha256 `b9db651e…`: no ejecuté git ni cálculo de hash.
- Comportamiento en runtime de `doc_ref.py`, `doc_status.py`, `open_store` y rutas de graph_ui.
- Que el árbol abierto corresponda exactamente al commit declarado por el supervisor.

RESULTADO: PASS
