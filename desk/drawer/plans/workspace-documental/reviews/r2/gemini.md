# Revisión Ronda 2 — Workspace Documental (`deskops-workspace-documental` rev. 2)

**Veredicto:** **APTO COMO PLAN** (con 1 corrección puntual de metadatos en `G_WRITE` para evitar circularidad nominal en `WS12`, y 2 ajustes menores no bloqueantes).

---

## 1. Hallazgos de Ronda 1 que quedaron resueltos

1. **Separación de baseline (`sldb/pron` + `Deskops` + `Mindmap`) vs `Kimun`:** Resuelto en [`dag.yaml` (`baseline_proposal`, `external_references`)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/dag.yaml#L6-L103), [`decisiones.md` (`P02`)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/decisiones.md#L8) y [`reconciliacion.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/reconciliacion.md#L3-L12). `Kimun` queda solo como referencia externa sin dependencias ocultas `M1/M2/C2`, y las 3 tareas reales en `../UIs/graph_ui/desk/tasks/` están referenciadas con ruta verificada y hash SHA-256.
2. **Fuente canónica única y coherencia de aristas:** Resuelto. [`build_plan.py`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/build_plan.py) y [`validate_plan.py`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/validate_plan.py) generan y verifican `README.md`, las 39 fichas `task-ws*.md` y `dag.diagram.yaml` desde `dag.yaml`. Se corrigieron las aristas: `WS09 -> WS11 -> WS12` (navegación precede a operaciones), `WS33` depende de `WS32` y `WS11`, el lector básico (`WS13–WS16`) no se bloquea por los índices authored (`WS17`), y la tarea activa de `closeout` es el gate explícito `G_CLOSEOUT` requerido en `WS12`, `WS26`, `WS28` y `WS32`.
3. **Atomización, dueño único y no duplicación de trabajo activo:** Resuelto. Los 39 nodos (`WS01–WS39`) tienen un único `owner_repo` (`deskops`, `graph_ui`, `sldb` o `spec2viz`), tamaño relativo `S/M`, `output_scope` explícito y guarda `overlap_with` + `G_UI` para concertar deltas con `graph_ui` en `WS06` sin duplicar tickets ni modificar su Board.
4. **Edición fuente Markdown vs payload y autoridad de cierre:** Resuelto. Se separan la edición de campos con conflicto (`WS19`), la prueba/implementación de guardado fuente reversible en `sldb` (`WS20` -> `G_SOURCE`) y su integración en UI (`WS21`). El cierre en baseline usa verificación y handoff externo al CLI/coordinador (`WS28`, `P05`), sin `git commit` desde HTTP.
5. **Alcance de `ViewDoc` y superficies antes omitidas:** Resuelto en [`brief.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/brief.md#L19-L28), [`borradores/vision.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/borradores/vision.md#L34-L38), [`borradores/vistas.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/borradores/vistas.md#L33-L46) y [`borradores/user-flows.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/borradores/user-flows.md#L53-L63). `ViewDoc` se acota a proyecciones de grafo portables en `spec2viz` (`WS18`), y se incorporan `CrossroadDoc`, `desk/issues/` no modelados, `DeskFAQDoc`, `StepDoc`, `drift check`, `Schema`/edición de clases (`WS39` / `UF09`) y arranque sin desk (`UF10`).

---

## 2. Gates futuros bien modelados (no son defectos del plan)

Los 10 gates explícitos (`G_PRODUCT`, `G_UI`, `G_CLOSEOUT`, `G_WRITE`, `G_SOURCE`, `G_SCION`, `G_EXEC`, `G_HUMAN_READ`, `G_HUMAN_MANUAL`, `G_HUMAN_DELEGATE`) tienen estado honesto (`pending`/`blocked`/`unverified`), actor responsable y criterio de evidencia verificable que no se satisface por la mera existencia de archivos. Las decisiones `P01–P08` en `decisiones.md` están correctamente marcadas como propuestas pendientes del humano en `WS07`.

---

## 3. Hallazgos pendientes priorizados

### H1 (Importante — Circularidad nominal de metadatos en `G_WRITE` vs `WS12`)
- **Archivo/sección:** [`dag.yaml` (`gates.G_WRITE`, l. 34–39 y `WS12`, l. 301–318)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/dag.yaml#L34-L39), [`decisiones.md` (§Cómo se resuelve un registro, l. 18)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/decisiones.md#L18) y [`build_plan.py` (l. 71)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/build_plan.py#L71).
- **Problema:** `dag.yaml` declara `G_WRITE.resolver: WS07/WS12`, pero al mismo tiempo `WS12` tiene `requires: [G_CLOSEOUT, G_WRITE]` y exige en su aceptación *"G_WRITE y G_CLOSEOUT verificados"*. Si `WS12` es co-productor de `G_WRITE` y a la vez requiere `G_WRITE` para ejecutarse, existe una dependencia circular `WS12 -> G_WRITE -> WS12`. Actualmente `validate_plan.py` no la detecta solo porque `build_plan.py` (l. 71) ignora el campo `resolver` del YAML y hardcodea `producers = {..., 'G_WRITE': 'WS07', ...}`.
- **Corrección precisa:** Elegir una de dos opciones y alinear `dag.yaml`, `decisiones.md` y `build_plan.py`:
  1. Si `G_WRITE` representa la decisión humana de política de escritura (`P03–P06` en `WS07`): cambiar `G_WRITE.resolver` a `WS07` en `dag.yaml` (manteniendo `G_WRITE` en `WS12.requires`).
  2. Si `G_WRITE` representa el contrato técnico cerrado además de `P03–P06` (`WS12`): cambiar `G_WRITE.resolver` a `WS12`, reemplazar `G_WRITE` por `G_PRODUCT` en `WS12.requires`, y apuntar `producers['G_WRITE'] = 'WS12'` en `build_plan.py`.

### H2 (Sugerencia menor — Gate `G_HUMAN_READ` en `WS25` y `WS39`)
- **Archivo/sección:** [`dag.yaml` (`WS19` l. 447–450, `WS25` l. 575–579, `WS39` l. 870–875)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/dag.yaml#L575-L579).
- **Problema:** `WS19`, `WS25` y `WS39` dependen de `WS16` (*Validar con humano lectura y descubrimiento*), cuya aceptación exige que los fallos humanos de lectura bloqueen el paso a mutación/edición. Sin embargo, `WS19` incluye `G_HUMAN_READ` en `requires` mientras que `WS25` y `WS39` solo incluyen `G_UI, G_WRITE`.
- **Corrección precisa:** Añadir `G_HUMAN_READ` a `requires` en `WS25` y `WS39` para que el validador bloquee toda superficie de mutación si el acta humana `G_HUMAN_READ` sigue pendiente.

### H3 (Sugerencia menor — Trazabilidad del corpus temporal entre `WS16` y `WS17`, y rango en `manual.md`)
- **Archivo/sección:** [`validacion-humana.md` (§Ejemplo reproducible, l. 7)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/validacion-humana.md#L7), [`cobertura.md` (`UF10`, l. 14)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/cobertura.md#L14), [`dag.yaml` (`WS16` y `WS17`, l. 386–421)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/dag.yaml#L386-L421) y [`borradores/manual.md` (§17, l. 23)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/borradores/manual.md#L23).
- **Problema:** `validacion-humana.md` indica que el generador/corpus del proyecto Taller (`.tmp/workspace-documental-ejemplo/`) se escribe en `WS16/17`, y `cobertura.md` asocia `UF10` (validado en `WS16`) con `WS17 ejemplo`, pero `WS16` no depende de `WS17` y `WS17` define `output_scope: ejemplo/README.md...`. Además, `borradores/manual.md` §17 aún cita `UF01–UF08` tras haberse añadido `UF09–UF10`.
- **Corrección precisa:** Precisar en `WS16.output_scope` la creación del script/fixture base `.tmp/workspace-documental-ejemplo/` para lectura (dejando en `WS17` solo las entradas/mapas authored evaluados en `WS30`), y actualizar `borradores/manual.md` §17 a `UF01–UF10` (con `UF09` condicionado a `WS39`).
