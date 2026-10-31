## REFORMULACION
**Propósito:** inventariar las superficies y operaciones actuales de Deskops antes de planificar cambios. **Resultado:** `auditoria/deskops.md`, con filas que indiquen archivo/código/operación y estado comprobado. **Repo dueño:** `deskops`. **Límites:** nodo de planificación, sin implementación ni promoción autorizada; depende de WS01; su alcance incluye modelos, Markdown no modelado, inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs, firmas públicas, efectos Git y cierre.

## AMBIGUEDADES
1. «Cada fila incluye archivo/código/operación y estado comprobado; no inferir modelo por carpeta.»  
   Obliga a inventar **qué evidencia cuenta como “estado comprobado”**: inspección estática, ejecución de prueba, fuente runtime o ausencia declarada. Sin ese criterio, el ejecutor no sabe cuándo una fila es aceptable.

2. «Modelos y Markdown no modelado» y «no inferir modelo por carpeta».  
   Obliga a inventar **qué entidad cuenta como “modelo”** y **cómo distinguir Markdown modelado de no modelado** sin usar la carpeta como criterio. El nodo no da taxonomía ni fuente de identidad.

3. «firmas públicas, efectos Git y cierre».  
   Obliga a inventar **qué firmas públicas** se inventarían (API, CLI, funciones exportadas, contratos) y **qué operaciones de cierre** entran, dado que “cierre” no se define en el nodo.

## DRY-RUN
- **Lecturas:** node WS02, guía, brief, alcance, decisiones, cobertura y, al ejecutar, código/artefactos del repo `deskops`.
- **Cambios previstos:** producir/actualizar `auditoria/deskops.md`; no tocar código ni promocionar.
- **Dependencias:** WS01 como prerrequisito; WS06 y WS10 consumen después este inventario. Los bloques `edge` no se revisan.
- **Validaciones futuras:** comprobar que cada fila tenga fuente y estado verificable; que no se infiera modelo por carpeta; que el alcance no se amplíe a implementación. No se ejecuta nada.

## FUTURO
WS01 produce el brief/glosario; WS06 y WS10 consumen el inventario; WS07 o el humano resuelven las Pxx y gates; la promoción exige preflight task-only y autorización posterior. Nada de eso es ambigüedad de WS02.
