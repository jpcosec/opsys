---
kind: suggestion
sender_project: graph_ui
created_at: 2026-08-28T00:00:00
status: open
---

# Add anti-mock mandate + pre-execution comprehension gate to task-lifecycle

El skill `deskops-task-lifecycle` no exige dos salvaguardas que en la práctica
son críticas para evitar despachos fallidos y falsos-green. Propongo agregar
ambas como MANDATOS del ciclo de vida.

## 1. Mandato anti-mock (global, innegociable)

Mocks, stubs, fake data, placeholders y atajos TODO están absolutamente
prohibidos como entregable final de un Executor. Incluye:

- retornar constantes falsas en vez de cómputo real
- tests que asertan contra literales inline que duplican la respuesta esperada,
  en vez de validar el contrato real / la salida real del generador
- no-ops que fingen funcionar
- datos fabricados simulando una fuente de datos
- lógica real reemplazada por un atajo comentado

Si una dependencia real no está disponible, el Executor debe DETENERSE y
reportar el bloqueo, no taparlo con un mock.

Hoy esto solo aparece disperso en tasks/issues individuales
(`task-anti-pattern-monolithic-api-endpoint-in-sldb-viewer.md`,
`desk/drawer/issues/monolithic-api-anti-pattern.md`), nunca como mandato del
lifecycle. Debería estar en `deskops-task-lifecycle` como anti-patrón prohibido
de primer nivel, y idealmente materializado como pill/atom canónico reutilizable
que todo Executor reciba por defecto.

## 2. Mandato de gate de comprensión pre-ejecución (preflight barato)

Antes de despachar el Executor real, el Supervisor DEBE lanzar un modelo barato
que lea el bundle de contexto cero (TaskDoc + Pills + Atoms) y responda
EXACTAMENTE qué entendió y qué va a hacer, paso a paso.

Si hay cualquier ambigüedad, o el agente barato se equivoca sobre qué hay que
hacer, eso significa que la descripción de la task es deficiente y hay que
corregirla ANTES de gastar un Executor real.

Este gate no existe en ninguna parte del workflow actual. Debería insertarse
como Paso 2.5 (entre Promoción y Despacho del Executor) en
`deskops-task-lifecycle`. Si corresponde, exponer un comando o convención para
el preflight de comprensión.

## Motivación concreta

En `graph_ui` acabo de tener un Executor que falló en seco tras un bundle que
creía completo. Ambas salvaguardas habrían prevenido el gasto: el gate de
comprensión habría detectado el hueco antes de ejecutar, y el mandato anti-mock
habría cerrado la puerta a un cierre falso-green.

## Solicitud

Incorporar ambos mandatos al skill `deskops-task-lifecycle`. Mientras tanto, en
`graph_ui` ya materialicé el anti-mock como pill local
(`pill-guardrail-no-mocks-no-stubs-no-fake-data-in-deliverables`); idealmente
esto debería vivir canónicamente en deskops.
