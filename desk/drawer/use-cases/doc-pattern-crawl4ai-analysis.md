---
id: doc-pattern-crawl4ai-analysis
status: draft
created: 2026-06-14
tags:
- topic:documentation
- topic:doc-pattern
- topic:crawl4ai
- topic:user-guide
---

# Crawl4AI Documentation Pattern Analysis

## Source

- Home: https://docs.crawl4ai.com/
- Quickstart: https://docs.crawl4ai.com/core/quickstart/

## Purpose

Analizar cómo está estructurada la documentación de Crawl4AI para replicar
el patrón en la documentación del ecosistema hum.

---

## 1. Information Architecture (Site Structure)

Crawl4AI organiza su documentación en 6 capas:

```
Home (landing page)
├── Setup & Installation     # Cómo instalar, prerequisites
├── Quick Start              # Tutorial first-use: 9 pasos numerados
├── Core                     # Guías profundas por feature
│   ├── CLI, Simple Crawling, Deep Crawling...
│   └── 16 temas one-concept-per-page
├── Advanced                 # Features avanzados
│   └── 16 temas
├── Extraction               # Estrategias de extracción
│   └── 4 temas
└── API Reference            # Referencia técnica por clase/método
    └── 7 temas
```

Patrón: **progressive disclosure** — de lo general a lo específico,
de lo simple a lo avanzado. Cada página cubre UN concepto.

---

## 2. Quickstart Page Structure (la página analizada)

La página Quickstart sigue esta plantilla:

```
# Getting Started with Crawl4AI

Welcome... In this tutorial you'll:
1. run your first crawl
2. generate Markdown
3. CSS extraction
4. LLM extraction
5. crawl dynamic page

## 1. Introduction
  → bullet list de qué provee la herramienta

## 2. Your First Crawl
  → código mínimo + "What's happening?" annotation

## 3. Basic Configuration
  → código con BrowserConfig + CrawlerRunConfig
  → callout > IMPORTANT

## 4. Generating Markdown Output
  → explica dos outputs (raw_markdown vs fit_markdown)
  → ejemplo con filter + generator
  → Note: con precisión de performance (~50ms)

## 5. CSS-based Extraction
  → LLM schema generation como intro
  → ejemplo básico de schema
  → Why is this helpful? (bullet benefits)
  → Tips (raw://)

## 6. LLM-based Extraction
  → Open-source vs Closed-source options
  → código con Pydantic schema + LLMExtractionStrategy
  → What's happening? annotation

## 7. Adaptive Crawling
  → código + "What's special?" bullet list

## 8. Multi-URL Concurrency
  → streaming mode vs batch mode

## 8 (otro). Dynamic Content
  → JS interaction (click tabs)
  → Key Points (bullet list)

## 9. Next Steps
  → recaps what you learned
  → links to next tutorials
```

---

## 3. Patrones Identificados

### 3.1 Page Template Pattern

```
title + tagline
"what you'll learn" (numbered list)
---
section 1: Introduction (bullet list of capabilities)
section 2..N: cada capability como paso numerado
  → código completo y ejecutable
  → annotation del código ("What's happening?")
  → callouts: IMPORTANT, Note, Tip, New!
  → benefits list ("Why is this helpful?")
  → linking a doc más profunda ("Learn more →")
final section: Next Steps
  → recap de lo aprendido
  → links a donde seguir
```

### 3.2 Code Pattern

- Código **completo** (con imports, `if __name__`, `asyncio.run`)
- Anotaciones inline con `# comment` en el código
- Sección "What's happening?" debajo del código con bullet list
- Sin truncar ni fragmentos

### 3.3 Callout Pattern

| Tipo | Uso | Ejemplo |
|---|---|---|
| `> IMPORTANT` | Comportamiento default que hay que conocer | CacheMode.BYPASS por defecto |
| `> Note` | Performance, detalle técnico menor | PruningContentFilter ~50ms |
| `> Tips` | Atajo o modo alternativo | raw:// para pasar HTML directo |
| `> **New!**` | Feature recién agregada | Schema generation via LLM |

### 3.4 Linking Pattern

- Cada sección termina con un link a la guía profunda: `[Learn more about X →](...)`
- El link está al final del bloque, después del ejemplo
- Lenguaje consistente: "Learn more about [Feature] →"

### 3.5 Tone

- Instructivo pero no seco ("You now have a simple, working crawl!")
- Explica el **para qué** antes del **cómo**
- "What's happening?" desglosa el código sin asumir conocimiento
- "Why is this helpful?" da contexto de valor
- Lenguaje de tutorial, no de referencia

### 3.6 Sidebar Navigation Pattern

- Sidebar con categorías: Core, Advanced, Extraction, API Reference
- Cada categoría despliega una lista plana de temas
- Los temas están ordenados por complejidad creciente
- Quick Start está fuera de las categorías (entry point)

---

## 4. Lo que NO tiene Crawl4AI (y deberíamos considerar)

- No tiene "pill" o "context node" pattern (lo nuestro es más sofisticado)
- No tiene materialización desde atoms (nosotros separamos source → projection)
- No tiene reversible markup (nosotros tenemos ⸢rev•field⸥)

---

## 5. Aplicación a deskops/hum-ecosystem

### 5.1 Propuesta de estructura de docs

Basado en el patrón crawl4ai, propongo esta organización:

```
Home (landing page: README.md general)
├── Setup & Installation       # Cómo instalar sldb + deskops + bootstrap
├── Quick Start (user-guide)   # Tutorial first-use: crear tarea, avanzar, cerrar
├── Core Concepts              # Un concepto por página
│   ├── What is a Desk?
│   ├── Tasks & Boards
│   ├── Pills & Context
│   ├── Rituals & Routines
│   ├── Atoms & Knowledge
│   ├── Primitives (conditions, operators, checklists, edges)
│   └── Spec-driven artifacts
├── Workflow Guide             # Flujos completos paso a paso
│   ├── How to start a task
│   ├── How to execute a task (execution ritual)
│   ├── How to test a task (testing ritual)
│   ├── How to close a task (closeout ritual)
│   └── How to create a pill
├── Advanced                   # Features avanzadas
│   ├── Knowledge Graph
│   ├── Materializers
│   ├── Promotion workflow
│   └── Cross-repo registry
└── Reference                  # Referencia técnica
    ├── CLI Reference (comandos + flags + ejemplos)
    ├── Model Reference (todos los StructuredNLDoc)
    ├── Spec Reference (formato de spec YAML)
    └── API Reference (Python)
```

### 5.2 Template para cada página de docs

```
# <Concept Name>

> <una línea de propósito>

In this guide you'll learn:
1. <qué>
2. <qué>
3. <qué>

## 1. <Section>

<texto explicativo>

<ejemplo completo>

What's happening?
  - <annotation 1>
  - <annotation 2>

> Note: <callout relevante>

[Learn more about <related concept> →](link)

## Recapitulación

<resumen de lo que se cubrió>
<links a siguientes pasos>
```

### 5.3 Callouts que usar

| Tipo | Cuándo |
|---|---|
| `> Note:` | Performance, comportamiento default, edge case |
| `> IMPORTANT:` | Algo que si no sabés rompe el flujo |
| `> Tip:` | Atajo, modo alternativo, best practice |
| `> ⚠️ Failure Mode:` | Lo que puede salir mal (tomado de los rituals) |

---

## 6. Open Questions for Drawer

- ¿Las guías de "Core Concepts" deben ser atoms materializados o docs independientes?
- ¿Cada CLI command debería tener su propio doc tipo "man page"?
- ¿El user-guide (quickstart) debería ser un ritual o un doc?
- ¿Qué hacemos con la doc existente (workflow-policy-reference, how-to-report)? ¿migrar o mantener?
