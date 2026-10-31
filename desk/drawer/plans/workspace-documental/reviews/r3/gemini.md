# Revisión Ronda 3 — Workspace Documental (`deskops-workspace-documental` rev. 3)

**Veredicto:** **APTO COMO PLAN**

**Bloqueantes:** **Ninguno (0).**

---

## 1. Verificación de resoluciones de Ronda 2

Todos los hallazgos previos y riesgos de ejecución quedaron resueltos de forma verificable en [`dag.yaml` (rev. 3)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/dag.yaml):

1. **Separación sin circularidad entre decisión y contrato de escritura (`H1` resuelto):** `G_WRITE` se desdobló en `G_WRITE_POLICY` (`produced_by: WS07`, requerido por `WS12`) y `G_WRITE_CONTRACT` (`produced_by: WS12`, requerido por las tareas de mutación). Todos los productores de gates están declarados en `dag.yaml` (`produced_by`) y son leídos directamente por [`build_plan.py` (l. 72)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/build_plan.py#L72) y verificados sin ciclos por [`validate_plan.py` (l. 28–36)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/validate_plan.py#L28-L36).
2. **Gates de recepción por repositorio tras contratos:** Se reemplazó el `G_UI` anticipado de `WS06` por `G_UI_READ` y `G_SPEC_VIEW` (producidos al cerrar `WS11`) y `G_UI_WRITE` y `G_SLDB_WRITE` (producidos al cerrar `WS12`), con designación explícita de responsables en `WS07` (`P01`).
3. **Variantes explícitas de edición fuente (`P04` / `source_mode`):** El parámetro `parameters.source_mode` (`pending | editable | read_only`) gobierna formalmente la activación de `WS20` (`enabled_when`) y las variantes de `WS21` (`variants`), exigiendo `WS20` + `G_SOURCE` en modo `editable` y degradando limpiamente a fuente solo lectura en `read_only`.
4. **Cobertura completa de corpus, multidesk, operaciones de conocimiento y publicación real (`H2` y `H3` resueltos):**
   - `G_HUMAN_READ` se exige en todas las tareas de mutación del baseline (`WS19`, `WS25`, `WS26`, `WS28`, `WS39`, `WS42`).
   - `WS40` unifica la generación reproducible del corpus temporal Taller (dos desks) para `WS16` y `WS30`, separando las plantillas authored (`WS17`) de la publicación en el desk real (`WS43`, gobernada por `P09`).
   - `WS41` cubre la lectura segura multidesk (`UF08` en `WS16`) y `WS42` cubre `atoms split/merge` y `proto typing` (`UF03` en `WS30`).
   - [`borradores/manual.md` (§17)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/borradores/manual.md#L23) y [`cobertura.md`](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/cobertura.md) están alineados en `UF01–UF10`.

---

## 2. Sugerencias no bloqueantes

- **Errata tipográfica en prosa generada (`WS42` por `WS39`):** En [`build_plan.py` (l. 61)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/build_plan.py#L61) y su salida [`README.md` (l. 93)](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/README.md#L93) se lee *"WS29 (Changes) y WS42 (Schema) son extensiones con aceptación propia"*; debe decir *"WS39 (Schema)"* (como ya figura correctamente en [`alcance.md` l. 17](file:///home/jp/proyectos/SLDB_1/deskops/desk/drawer/plans/workspace-documental/alcance.md#L17) y en las aristas de `dag.yaml`).
