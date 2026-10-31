# Handoff: proponer correcciones de una ronda de context review

Repo: /home/jp/proyectos/SLDB_1/deskops. Plan: desk/drawer/plans/workspace-documental/.
Encargo completo: desk/tasks/task-revisar-dag-workspace-con-agentes-baratos.md.

## Qué haces

Recibes un archivo <grupo>-findings.md con las ambigüedades que revisores baratos hallaron en nodos del plan. Para CADA hallazgo decides y escribes una propuesta. El coordinador revisa y aplica; tú no aplicas nada.

Lee: dag.yaml (solo los nodos del grupo y sus vecinos), brief.md, alcance.md, decisiones.md, cobertura.md, context-review-guide.md, y validacion-humana.md, reconciliacion.md o borradores/*.md si el hallazgo los toca. Para verificar un dato puedes leer código en este repo y en ../sldb, ../spec2viz, ../scion, ../UIs/graph_ui, sin modificar nada. Tampoco ejecutes comandos que escriban.

## Regla de decisión

- `corregir`: la duda es real. Propón un cambio mínimo de texto en la fuente.
- `error_reviewer`: solo con CITA textual de una fuente suministrada al reviewer que resuelva la duda, o con argumento verificable de que pide ejecutar trabajo futuro que el nodo delega. Sin cita, corrige.
- `bloqueo`: requiere una decisión humana o externa; nombra responsable y dependencia.

## Límites

- No edites dag.yaml, ni ningún archivo del plan, ni desk/. Escribe SOLO tu archivo de propuestas.
- No resuelvas decisiones Pxx ni des gates por aprobados. No cambies status, gates, ni execution_authorized.
- No inventes APIs: un dato no comprobado se escribe como hipótesis a auditar.
- No añadas alcance excluido en alcance.md. Mantén el español y la concisión del plan.
- Cambios mínimos: no reescribas un nodo si basta una frase. No uses git. No lances agentes.

## Salida

Escribe runs/subagents/20261031-workspace-context-reviews/rounds/round-3/<grupo>-proposals.json: una lista JSON. Cada elemento:

{"node":"WS12","finding":1,"decision":"corregir|error_reviewer|bloqueo","file":"dag.yaml|brief.md|alcance.md|...","target":"WS12.acceptance","old":"texto exacto actual","new":"texto nuevo","reason":"por qué; cita si es error_reviewer; responsable si es bloqueo"}

`target` solo para dag.yaml, con forma <id>.<campo> (scope, acceptance, output_scope, title, depends_on). Para ROOT y PK usa <id>.acceptance. En los demás archivos `old` debe aparecer tal cual y una sola vez. En error_reviewer y bloqueo, `old` y `new` van vacíos. Valida que el JSON parsea. Al terminar responde solo: LISTO <grupo> <número de propuestas>.

## Precisiones de esta ronda (mandan sobre lo anterior)

Objetivo: converger. Un encargo de planificación no tiene que prever cada caso de borde.

- `corregir` SOLO si la duda afecta resultado, repo, actor, una dependencia real, contradicción entre textos o una aceptación que no se puede comprobar en absoluto. Una frase, sin añadir términos nuevos que abran otras dudas.
- `error_reviewer` cuando pide detalle de implementación: casos de borde, formato, umbrales, textos de pantalla, algoritmo exacto. Cita obligatoria, del input de ese nodo: context-review-guide.md ("textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará") o alcance.md ("El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide"; "Si al llegar a un nodo falta un contrato, API, dato o permiso..."; "Una dependencia transitiva cuenta como prerrequisito"). Si es transitiva, nombra la cadena de aristas.
- Solo puedes proponer cambios en dag.yaml, en scope/acceptance/output_scope/depends_on de los nodos. No propongas tocar brief.md, alcance.md, decisiones.md, cobertura.md, validacion-humana.md ni context-review-guide.md.
- Para scope, acceptance y output_scope, `old` es un fragmento en UNA línea tal como queda el texto con espacios normalizados.
- Para depends_on, `new` es la lista completa como array JSON y `old` queda vacío.
