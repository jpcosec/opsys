---
id: task-empaquetar-deskops-como-m-dulo-de-pi-subagents
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-empaquetar-deskops-como-m-dulo-de-pi-subagents
current_node: checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-execution-ready
history: []
references:
- desk/drawer/tasks/task-empaquetar-deskops-como-m-dulo-de-pi-subagents.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-execution-ready
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-testing-ready
- checklist-task-empaquetar-deskops-como-m-dulo-de-pi-subagents-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Empaquetar deskops como módulo de pi-subagents

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20260901-154500-suggestion-empaquetar-deskops-como-modulo-pi-subagents.md`.

## Scope

_State what is in scope and what is out of scope._

ID: task-empaquetar-deskops-como-m-dulo-de-pi-subagents
Status: deferred
Priority: medium

## Goal

Triage and resolve the inbox message promoted from `desk/inbox/20260901-154500-suggestion-empaquetar-deskops-como-modulo-pi-subagents.md`.

## Scope

## Contexto

Soy usuario de deskops. Mi workflow es 100% deskops: creo atoms, tareas, avanzo rituals, cierro tareas. No uso supervisores, testers, chains ni nada del ecosistema pi-subagents por encima.

Sin embargo, necesito despachar subagentes para tareas paralelas. Ejemplo real de hoy:
- Mientras un subagente arreglaba la estructura desk/ (doctor, add task, add ritual, bind board, graph build)
- Otro scouteaba /home/jp/AntonIA buscando datos frescos

Eso es paralelismo puro. No es chain, no es supervisor→executor→tester. Es "haz esto, haz esto otro, tráeme los resultados". Pero el tool `subagent()` me fuerza a elegir entre agents que no conozco (deskops-executor, deskops-tester) con lógica de ciclo de vida que no uso.

## El problema real: fricción semántica

`subagent({tasks: [{agent: "worker", task: "..."}, {agent: "scout", task: "..."}]})` funciona. Pero worker no tiene las skills de deskops. No puede correr `deskops add atom`, `deskops add task`, `deskops advance task` porque no conoce el CLI ni la estructura .sldb.

La alternativa es `deskops-executor` pero ese agente tiene su propia idea de cómo trabajar: recupera board, revisa rituals, exige closeout. No quiero eso. Quiero un worker que herede skills de deskops y nada más.

## Necesidad: agente `deskops.worker`

Un agente empaquetado como módulo de pi-subagents (ej. `@pi-subagents/deskops` o registro directo) que:

1. **Skills que carga:**
   - `use-deskops` (comandos CLI, estructura desk/)
   - `deskops-task-lifecycle` (preparación, ejecución aislada, cierre atómico)
   - `deskops-health-and-drift` (diagnóstico y reparación)
   - `deskops-inbox-coordination` (mensajería entre proyectos)
   - `pi-subagents` (para que él mismo pueda sub-delegar si necesita)

2. **Contexto:** `context: fresh` (no hereda nada, parte de cero)

3. **Tools que usa:** bash (para correr deskops CLI), read/write/edit (para editar archivos desk/), subagent (para delegar tareas sub-deskops)

4. **Lo que NO hace:**
   - No implementa ciclo supervisor→executor→tester
   - No exige closeout antes de devolver control
   - No revisa board a menos que la task lo pida explícitamente
   - No interpreta roles de workflow (no es supervisor, no es tester)

5. **Lo que SÍ hace:**
   - Recibe una tarea concreta y bounded: "crea este atom", "avanza esta task", "porta estos datos"
   - Ejecuta comandos deskops directamente
   - Devuelve el resultado sin intentar auto-gestionar el ciclo de vida

## Por qué no usar los agents existentes

| Agente | Problema |
|---|---|
| `deskops-executor` | Tiene ciclo de vida propio (recupera board, revisa rituals, exige closeout). No quiero gobernanza, quiero ejecución directa. |
| `deskops-supervisor` | No soy supervisor, soy el que pide la pega. |
| `deskops-tester` | No necesito tester, necesito ejecutor. |
| `worker` | No tiene skills de deskops. No puede correr `deskops add atom`. |
| `delegate` | No tiene skills de deskops. |
| `scout` | Solo lectura, no muta el desk. |

Ninguno hace lo que necesito: **un worker con skills de deskops que ejecute comandos sin gobernanza heredada**.

## Forma concreta sugerida

```json
{
  "name": "deskops.worker",
  "package": "deskops",
  "systemPrompt": "Eres un worker de deskops. Ejecutas comandos deskops CLI y editas archivos desk/. No tienes ciclo de vida propio, no revisas board a menos que te lo pidan explícitamente. Devuelves el resultado sin intentar closeout.",
  "systemPromptMode": "replace",
  "inheritProjectContext": false,
  "inheritSkills": false,
  "defaultContext": "fresh",
  "tools": {
    "read-write-edit": true,
    "bash": true,
    "subagent": true
  },
  "skills": ["use-deskops", "deskops-task-lifecycle", "deskops-health-and-drift", "pi-subagents"]
}
```

Registrable via `subagent({action: "create", config: {...}})` o instalable como módulo npm tipo `@pi-subagents/deskops`.

## Uso esperado en el día a día

```typescript
// Paralelismo real sin chains ni roles
subagent({
  tasks: [
    {agent: "deskops.worker", task: "Crea atom con title 'foo' y answer 'bar' en /repo --tags system:x topic:y"},
    {agent: "scout", task: "Explora /otro/lado por datos frescos"}
  ],
  concurrency: 2,
  context: "fresh"
})
```

O single:

```typescript
subagent({agent: "deskops.worker", task: "deskops add atom --root . --title 'X' --answer 'Y'"})
```

Sin tener que lidiar con chains, supervisión, ni ciclo de vida ajeno.

## Impacto

- **Nada se rompe**: el resto de agents existentes (deskops-executor, supervisor, tester) siguen funcionando igual. Esto es un worker liviano, no un remplazo.
- **Bajo mantenimiento**: solo necesita mantener las skills actualizadas. El sistema prompt es ~5 líneas.
- **Alta demanda**: cualquier repo con deskops activo (mepu, antonIA, vitali, teva) podría usarlo.

## Source

- `desk/inbox/20260901-154500-suggestion-empaquetar-deskops-como-modulo-pi-subagents.md`

## Done When

- The message is resolved, answered, or promoted into active work.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-empaquetar-deskops-como-m-dulo-de-pi-subagents.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
