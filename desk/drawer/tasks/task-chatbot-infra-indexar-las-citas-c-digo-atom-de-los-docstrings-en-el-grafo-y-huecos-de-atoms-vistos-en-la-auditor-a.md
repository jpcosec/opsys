---
id: task-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Chatbot_Infra: indexar las citas código→atom de los docstrings en el grafo (y huecos de atoms vistos en la auditoría)

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261021-235026-suggestion-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a.md`.

## Goal

_Describe the concrete result this task must produce._

Triage and resolve the inbox message promoted from `desk/inbox/20261021-235026-suggestion-chatbot-infra-indexar-las-citas-c-digo-atom-de-los-docstrings-en-el-grafo-y-huecos-de-atoms-vistos-en-la-auditor-a.md`.

## Scope

_State what is in scope and what is out of scope._

_Describe the incoming message with enough evidence to triage._

Desde Chatbot_Infra (heyantonia), 2026-10-21. Convención nueva en los tres repos del workspace (Chatbot_Infra #133 0de7d041, labchile_chatbots #23 06c4822, shared_llm-gateway #20 ff9c8b1): el código cita sus atoms al final del docstring del módulo, en un bloque

    Atoms:
    atom-<id>

(un id por línea, columna 0). En archivos no Python va como comentario '# Atom: <id>' (workflows de GitHub, Dockerfile, .tf, descriptores yaml). Cada repo tiene tests/test_atoms_citados.py: falla si un id citado no existe en desk/atoms y avisa si un atom no lo cita nadie. Hoy los 24 atoms están citados.

Pedido: que deskops indexe esas citas en el grafo de sldb para que 'deskops show atom <id>' y 'deskops graph' muestren qué módulos lo citan (arista code→atom, p.ej. RelationDoc 'cited_by' o 'implements'), y que 'graph missing' / 'doctor' reporten citas rotas y atoms sin cita. Propuesta concreta: un verbo 'deskops atoms citations [--check] [--write]' que escanee **/*.py (bloque 'Atoms:' del docstring de módulo) y '# Atom:' en el resto, con exit 1 por id inexistente y alerta por atom huérfano; así el test de cada repo se reemplaza por un comando del kit. Complementa el CodeAnchorDoc de sldb (52f63690, nota 20261020-141330): el anchor va atom→símbolo con fingerprint; la cita va módulo→atom y es lo que lee quien abre el código. Un 'anchors record' podría sugerirse para cada cita.

Huecos de deskops encontrados en la misma auditoría de atoms:
1. No hay forma de renombrar el id de un atom; el id sale del título y un retitulado rompe citas y tasks.
2. 'atoms merge' no reescribe el campo 'atoms:' de las tasks que apuntaban al atom absorbido (hubo que reapuntar 5 tasks a mano con edit).
3. 'retire' no acepta atoms.
4. 'atoms validate --all' marca todo provenance como no resoluble (falso positivo masivo).
5. No hay verbo para editar desk/contexts/pills.md (en labchile_chatbots sigue diciendo 'psp_chatbot desk routine').
6. Rutas relativas en .sldb/core/store_index.yaml y .sldb/*/RelationDoc.yaml apuntan a ../../proyectos/SLDB_1/deskops/.sldb: al mover el workspace un nivel (repos/chatbot -> repos/legacy/chatbot/chatbot) 'deskops doctor' queda en 'linked store is missing'. Convendría resolver el store de deskops por ruta absoluta o por paquete instalado.
7. 'message send' rechaza un remitente no registrado; para escribir esta nota hubo que registrar Chatbot_Infra en desk/registry de deskops (repo register).

## Implementation Path

_Outline the expected implementation route or affected surface._

To be defined when the task is promoted.

## Validation

_List the checks required before this task can close._

- 

## Done When

_Name the observable condition that makes the task complete._

The message is resolved, answered, or promoted into active work.
