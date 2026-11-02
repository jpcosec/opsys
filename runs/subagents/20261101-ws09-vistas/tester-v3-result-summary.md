## Separación de fuentes

- **Lectura propia:** `fix-diff.txt`, `vistas.md` (23 fichas) y tramos de `dag.yaml` (`:681-740` WS11/WS12, `:841-874` WS13.1, `:1652-1685` WS25.1/WS25.2, `:2690-2695` WS40).
- **Dato del Supervisor, no verificado por mí:** `tester-v3-facts.log` (HEAD `d17d5d04`, revisiones al día, 13 tests, hash `d257d300…`, `dag.yaml` sin líneas fuera de `evidence`/`input_sha256`).
- **No ejecuté nada:** ni tests, ni git, ni validate.

## Comprobación

| Objeto | Fuente | Evidencia real archivo:línea | Resultado |
|---|---|---|---|
| Diff solo toca F07 y F15 | `fix-diff.txt` | Dos hunks, ambos en `vistas.md`: línea antigua 160 (F07 renderer) y 313 (F15 renderer) | PASS |
| F07 resuelta | `vistas.md` | `:163`: «Mostrar la nota como documento: contrato de lectura WS11, implementación WS25.1» | PASS |
| F15 resuelta | `vistas.md` | `:316`: «contrato WS11, implementación WS13.1» | PASS |
| Implementación con WS11/WS12 único productor (Renderer) | `vistas.md` | Las 23 líneas `Renderer` asignan nodo DAG o «sin productor»: `:61,78,95,112,129,146,163,180,197,214,231,248,265,282,299,316,333,350,367,384,401,418,435` | PASS |
| Navegación con productor de contrato WS11 | `vistas.md` | `:164,181,198,232,300,317,334,368,385` dicen «no definido; productor WS11»; coincide con WS11 = «Cerrar contrato de navegación e identidad» (`dag.yaml:682`), es contrato, no implementación | PASS (contrato) |
| `Desde UI: productor WS12` | `vistas.md`, `dag.yaml` | p. ej. `:166,183,200,233`; WS12 = «Cerrar contrato de operaciones y escritura» (`dag.yaml:724`), no implementa UI | PASS (contrato) |
| WS25.1 productor razonable de F07 | `dag.yaml` | `:1652-1685`: `kind: implementation`, `owner_repo: graph_ui`, `output_scope: frontends/mindmap/views/workspace/inbox/`, aceptación de ack persistente | PASS |
| WS13.1 productor razonable de F15 | `dag.yaml` | `:841-874`: `kind: implementation`, `owner_repo: graph_ui`, scope lectura de documento/contexto/enlaces; aceptación incluye Markdown sin modelo legible | PASS |
| WS40 produce el FAQ citado | `dag.yaml` | `:2690`: «su FAQ Markdown y documentos de conocimiento…» en el corpus temporal | PASS |
| 23 fichas con `Estado: bloqueado` | `vistas.md` | 23 líneas `:66,83,100,117,134,151,168,185,202,219,236,253,270,287,304,321,338,355,372,389,406,423,440`; todas `bloqueado` | PASS |
| 14 campos por ficha | `vistas.md` | Fichas uniformes: encabezado + 14 viñetas (Propósito…Evidencia), p. ej. F01 `:56-69`, F20 `:430-443`; 23×14 = 322 | PASS |

## Qué no pude verificar

- No ejecuté tests, git, `status`, `validate` ni build; datos del supervisor sin comprobar.
- No abrí código de `graph_ui` ni ejecuté WS13.1/WS25.1; su idoneidad es por metadata del DAG.
- No leí `dag.yaml` completo; solo nodos citados.
- No verifiqué las citas a `deskops.md`, `ui.md`, `infraestructura.md`, `user-flows.md` ni `manual.md`.
- Ambigüedad menor no bloqueante: navegaciones «no definido; productor WS11» no nombran implementador; se leen como hueco de contrato, no como atribución de implementación.

RESULTADO: PASS
