## REFORMULACION

**Propósito:** precisar el índice y la convención del manual conceptual, fijar el ejemplo Taller y definir las etiquetas de disponibilidad, sin redactar el manual completo.

**Resultado:** `borradores/manual.md` actualizado con esquema de capítulos (propósito/entradas/salidas), ejemplo fijo y definiciones disponible/propuesto/bloqueado, contrastadas con auditorías WS02–WS04.

**Repo:** `deskops` (`desk/drawer/plans/workspace-documental/borradores/manual.md`).

**Límites:** solo ese archivo; no redacción completa, capturas ni pasos ficticios; ejemplo WS40 descrito como corpus futuro hasta generarse. Depende de WS02 y WS07; `G_PRODUCT` está satisfecho.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** `borradores/manual.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS10 y gates en `dag.yaml`, auditorías WS02–WS04 y `docs/operator-manual.md` como manual CLI reutilizable.

**Cambios previstos:** únicamente `borradores/manual.md`: índice/esquema conceptual, ejemplo fijo `Taller` en `graph_ui:.tmp/workspace-documental-ejemplo/` con productor WS40 y estado futuro, y definiciones de disponibilidad con remisión de pruebas/actas a sus productores.

**Dependencias:** WS02 y WS07 directas; WS03/WS04 transitivas vía WS06/WS07; `G_PRODUCT` satisfecho; WS40 como productor futuro del corpus, no dependencia ejecutable.

**Validaciones futuras:** comprobar que no se introduzcan pasos/capturas ficticios, que las etiquetas se apoyen en auditorías y no en inferencias, y que las remisiones a pruebas/actas queden identificadas para WS16/WS30. Sin ejecución.

## FUTURO

WS31 incorporará el índice al manual publicado y exigirá actas; WS30/WS16 producirán pruebas y actas humanas; WS40 generará el corpus Taller; WS43 aportará el acta de publicación real; el humano resolverá `G_HUMAN_MANUAL` y la aceptación de uso. WS09 consumirá las etiquetas de disponibilidad. Nada de esto se decide ni ejecuta en WS10.
