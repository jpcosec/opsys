---
id: feature-semantic-execution-adapter
status: draft
created: 2026-06-17
tags:
- topic:semantic-execution
- topic:agents
- topic:band-ai
- topic:adapter
- topic:proposal
---

# Semantic Execution Adapter

## Propósito

Definir una integración futura entre `deskops` y ejecutores semánticos externos, con Band.ai como primer adaptador posible, sin acoplar el core de `deskops` a Band.ai.

`deskops` conserva la máquina de estados local, las rutinas deterministas, la validación y el cierre. El adaptador externo consume eventos, coordina subagentes limpios y devuelve resultados estructurados que `deskops` debe validar antes de avanzar estado.

## Fuentes

Fuentes externas:

- `http://docs.band.ai/welcome` — conceptos core de identidades temporales y salas de contexto.
- `http://docs.band.ai/api/introduction` — diseño del cliente/adaptador externo.

Fuentes internas:

- `docs/diagrams/process/llm-tasks-vs-automatic-routines.md` — límites entre trabajo semántico delegado y rutinas deterministas locales.
- `docs/diagrams/tasks/task-accumulation-initialization-resolution.md` — ciclo del subagente limpio y revisión de ambigüedad antes de tocar código.
- `docs/diagrams/tasks/task-board-phases.md` — fases y paralelismo entre tareas que no se pisan.
- `desk/rituals/closeout.md` — cierre con validación, limpieza y commit atómico.

## Arquitectura Propuesta

```mermaid
flowchart TB
    subgraph Core ["Deskops Core (Máquina de Estados Local)"]
        direction TB
        State["desk/tasks/Board.md\n(Estado Activo)"]
        CLI["deskops CLI\n(show, advance)"]
        EventSpec["spec/events/semantic_execution.yaml\n(Contrato de Evento)"]
        Hooks["Generic Hook\n(Emite payload JSON)"]

        State -->|Requiere semantica| Hooks
        Hooks -.->|Emite| EventSpec
    end

    subgraph Adapter ["Adaptador Externo (ej. deskops-band)"]
        direction TB
        Listener["Event Listener\n(Lee stdout o Webhook)"]
        Bridge["Band.ai Client"]

        Listener --> Bridge
    end

    subgraph External ["Entorno de Ejecución (Cloud / Local)"]
        direction TB
        Room["Sala Contextual en Band.ai"]
        Worker["Clean Subagent (Efímero)"]
        Sandbox["Workspace Aislado\n(Worktree / Branch)"]

        Bridge -->|Inicia| Room
        Room -->|Asigna| Worker
        Worker -->|Opera en| Sandbox
    end

    Sandbox -->|1. Mutacion de codigo| Sandbox
    Sandbox -->|2. Usa sldb/deskops para workflow| CLI
    Sandbox -->|3. Retorna resultado estructurado| CLI
    CLI -->|Rutinas automaticas| State

    classDef core fill:#0D1117,stroke:#58A6FF,stroke-width:2px,color:#c9d1d9;
    classDef adapter fill:#238636,stroke:#fff,stroke-width:2px,color:#fff;
    classDef ext fill:#4A154B,stroke:#fff,stroke-width:2px,color:#fff;

    class Core,State,CLI,EventSpec,Hooks core;
    class Adapter,Listener,Bridge adapter;
    class External,Room,Worker,Sandbox ext;
```

## Funcionamiento

1. `deskops` llega a una fase que requiere juicio semántico, como revisión de ambigüedad, edición de código o triage de fallos.
2. Un hook genérico local emite un payload JSON definido por `spec/events/semantic_execution.yaml`.
3. Un adaptador externo, por ejemplo `deskops-band`, consume el payload y llama a la API de Band.ai.
4. Band.ai asigna la ejecución a un subagente limpio en una sala contextual.
5. El subagente trabaja en un sandbox aislado, como `git worktree` o rama separada, para evitar colisiones de concurrencia.
6. El subagente usa `deskops` y `sldb` para operaciones workflow/documentales, no ediciones directas sobre `desk/` o `.sldb/` cuando exista CLI propietaria.
7. El adaptador retorna un resultado estructurado.
8. `deskops` retoma control, ejecuta rutinas deterministas locales, valida, y solo entonces permite avanzar estado o cerrar con commit atómico.

## Restricciones

- Band.ai no entra como dependencia del core de `deskops`.
- El contrato debe ser genérico para permitir otros adaptadores.
- Las rutinas deterministas, tests, closeout y commits siguen siendo locales.
- La ejecución paralela requiere aislamiento de worktree/rama y ownership explícito antes de habilitar mutación concurrente.
- El primer slice implementable debería ser contrato de evento local y superficies JSON de lectura, no integración Band.ai directa.
