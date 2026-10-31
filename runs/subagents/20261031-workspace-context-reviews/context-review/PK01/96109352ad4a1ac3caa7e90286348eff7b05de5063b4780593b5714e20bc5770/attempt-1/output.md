## REFORMULACION

**Propósito:** agrupar la revisión de fundamentos y auditorías (WS01–WS06) para fijar una base factual y una matriz de deltas verificables que evite duplicar código.

**Resultado:** PK01 es verdadero cuando cada hijo directo tiene una revisión vigente —hash de input y contrato actuales, con `disposition.md` en el intento correspondiente— o un bloqueo explícito por causa externa, registrado con responsable. No produce entregable propio ni ejecución.

**Repo dueño:** `deskops`.

**Límites:** agrupación sin ejecución; no autoriza tareas, no añade aristas, no acepta producto ni probes vivos, y no revisa los contratos de sus hijos.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas:** nodo PK01 en `dag.yaml`; guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`. Los bloques edge se leen solo como contexto, no se revisan.
- **Cambios previstos:** ninguno; PK01 no ejecuta ni modifica archivos.
- **Dependencias:** hijos WS01–WS06. WS06 integra evidencias de WS02–WS04; WS05 es independiente y alimenta E.
- **Validaciones futuras:** comprobar con `context_review.py status` que cada hijo tiene revisión vigente y `disposition.md` en el intento con hashes coincidentes; verificar que los bloqueos externos tengan responsable y dependencia registrados. Sin ejecutar.

## FUTURO

Cada hijo produce su `disposition.md` mediante su propio `context_review`. La sesión de coordinación ejecuta `context_review.py status` y registra bloqueos externos con responsable. WS06 produce la matriz en `reconciliacion.md`; WS11/12 obtienen la aceptación por delta del responsable designado en P01; WS44 aporta el probe de G_SCION; WS40 aporta el corpus para validaciones humanas.
