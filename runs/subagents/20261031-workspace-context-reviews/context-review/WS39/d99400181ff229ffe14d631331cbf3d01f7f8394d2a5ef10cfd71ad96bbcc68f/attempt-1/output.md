## REFORMULACION

**Propósito:** que WS39 integre en `graph_ui` la inspección y edición de modelos ya existentes (Schema/editar clases), haciéndolas navegables desde documento/contexto.

**Resultado:** vistas/diálogos y pruebas que permitan inspeccionar y mutar modelos reutilizando `draft/validate/promote` del dueño, con acta de prueba humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md` y `G_HUMAN_MODEL` aprobado antes de declarar el capítulo disponible.

**Repo:** `graph_ui`.

**Límites:** no reimplementar modelos; no habilitar `promover` si falta API o autoridad; extensión posterior al lector básico; promoción no autorizada.

## AMBIGUEDADES

1. **«usar draft/validate/promote del dueño»** — no se identifica qué repo/API es «el dueño» de esas operaciones ni dónde están documentadas. Obligaría a inventar el actor o el canal concreto.

2. **«UF09 inspección y mutación en store temporal»** — no se define qué store temporal, quién lo provee ni dónde vive; `output_scope` no lo incluye. Obligaría a inventar el entorno de prueba.

3. **«G_HUMAN_MODEL debe pasar antes de marcar capítulo disponible»** — «capítulo» no está definido en las fuentes suministradas. Obligaría a inventar qué unidad se declara disponible y con qué criterio.

4. **«confirmar efectos de contrato y errores»** — no precisa qué efectos ni qué errores se comprueban; aunque WS12 produce el contrato, no se delimita la comprobación esperada. Obligaría a inventar el umbral de aceptación técnica.

5. **Evidencia en `runs/.../acta.md` frente a `output_scope: shell/dialogs.js; views/models/; tests/`** — el acta exigida queda fuera del alcance declarado. Obligaría a decidir si se escribe fuera de `output_scope` o si este debe ampliarse.

## DRY-RUN

**Lecturas:** `dag.yaml` (WS39, gates, aristas WS12/WS16), guía, brief, alcance, decisiones, cobertura. **Cambios previstos:** ninguno; solo revisión. **Dependencias:** WS12 aporta `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS16 aporta `G_HUMAN_READ`; WS39 produce `G_HUMAN_MODEL`. **Validaciones futuras:** prueba humana UF09, acta en `graph_ui`, contrato WS12, preflight task-only antes de promover. No se ejecuta nada.

## FUTURO

WS07 designa participante/actores; WS12 cierra whitelist y aceptación del delta; WS16 produce `G_HUMAN_READ`; el humano decide P08; la promoción de WS39 queda sujeta a autorización y preflight.
