# UX stress-tests

This guide is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-cli-should-match-spoken-workflow-language.md`
- `desk/atoms/workflow-model/atom-ease-of-use-requires-progressive-disclosure.md`
- `desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md`

Cada test es un script de interacción CLI que pone al sistema bajo estrés desde la perspectiva del usuario.

## Formato

Cada test tiene:
- **Script**: comandos que ejecuta el usuario en orden
- **Puntos de estrés**: qué observar en cada paso (no solo "funciona", sino "se siente bien")
- **Modos de fracaso**: cómo se rompe la experiencia (no el código)

## Tests

| # | Basado en | Superficie | Énfasis |
|---|---|---|---|
| ST-01 | UC-01 | atoms, graph, faq | Orientación, primera impresión |
| ST-02 | UC-02 | inbox | Captura de baja fricción |
| ST-03 | UC-03 | graph neighbors | Navegabilidad del grafo |
| ST-04 | UC-04 | graph missing | Calidad del grafo |
| ST-05 | UC-05 | add/list/show/advance | Lifecycle de tareas |
| ST-06 | UC-06 | specs | Pipeline spec→artifact |
| ST-07 | UC-07 | drift | Coherencia conocimiento vs código |
| ST-08 | UC-08 | closeout | Quality gate |
| ST-09 | UC-09 | graph reflect | Meta-cognición del sistema |
| ST-10 | UC-10 | materialize | Comunicación externa |
| ST-11 | UC-11 | atoms new/validate | Creación de conocimiento |
| ST-12 | UC-12 | status | Diagnóstico y recuperación |
| ST-13 | UC-13 | repo | Contexto multi-repo |
| ST-14 | UC-14 | atoms split/merge/deprecate | Evolución del conocimiento |
| ST-15 | UC-15 | CLI en CI | Automatización |

## Cómo usar

1. Elegir un test
2. Setup: preparar el estado inicial (corrupto, vacío, etc.)
3. Ejecutar el script manualmente
4. Observar cada punto de estrés
5. Anotar cada modo de fracaso que se materialice
