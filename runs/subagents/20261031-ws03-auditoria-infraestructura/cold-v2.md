## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, auditoría de solo lectura, verificable fila por fila, del estado actual de `sldb`, `pron` y `spec2viz`.

**Alcance:** fuente/payload documental; conflictos y concurrencia —CAS por revisión/hash, locks de archivo/DB— como hipótesis a comprobar; referencias documentales; búsquedas e índices expuestos; notaciones/renderers de `spec2viz`, incluyendo alcance real de ViewDoc: si el modelo existe, dónde, qué lo produce/consume y qué renderers lo aceptan. Una sección por capacidad; filas por repo y mecanismo con columnas capacidad, repo, ubicación, operación expuesta, estado y evidencia.

**Repo/rutas:** lectura en `../sldb`, `../pron`, `../spec2viz`. Kimun no se lee ni entra al universo; solo referencia. Encabezado con fecha, HEAD completo por repo leído y cantidad de rutas sucias; carpeta sin git se declara. Archivo citado sucio lleva SHA-256.

**Límites:** se escribe únicamente el entregable y evidencia en `runs/subagents/20261031-ws03-auditoria-infraestructura/`; sin commits, closeout ni cambios interrepo. Executor escribe; Supervisor valida/commitea/cierra; Tester independiente muestrea. Lo no comprobado se marca «no comprobado» con causa; no se infiere. WS02–04, WS05, WS06 y WS08–12 son tareas futuras asignadas, no lagunas de esta.

## AMBIGUEDADES

1. **Cita:** «estado (comprobado/ausente/hueco)» y «distinguir API comprobada [...], ausencia y hueco». No define qué separa «ausente» de «hueco». Obligaría a inventar el criterio de clasificación, afectando cada fila.
2. **Cita:** «operación expuesta». No aclara si comprende API pública, CLI, HTTP, símbolo interno o cualquier punto de entrada. Obligaría a inventar la unidad auditada.
3. **Cita:** «búsquedas (índices o consultas expuestas)». «Expuestas» no se delimita: ¿endpoint, función invocable, índice declarado? Obligaría a decidir qué cuenta como búsqueda auditables.
4. **Cita:** «Si un archivo citado está sucio, se agrega su SHA-256». «Citado» puede significar todo archivo leído o solo el referenciado en la evidencia. Obligaría a inventar la cobertura de hashes.
5. **Cita:** «cantidad de rutas sucias en git status». No especifica si incluye no rastreados/ignorados ni qué formato contar. Obligaría a fijar un criterio no escrito.
6. **Cita:** «Precisiones comunes. Roles:». El fragmento «Precisiones comunes» queda sin contenido. Obligaría a inventar a qué precisiones remite.

## DRY-RUN

**Fuentes que leería (sin ejecutar):** TaskDoc, `cierre.md`, `brief.md`, `activation.md`, rituales y pills enlazadas; luego, solo lectura, `../sldb`, `../pron`, `../spec2viz`, buscando payload documental, CAS/revisión/hash, locks, referencias, índices/consultas y renderers/ViewDoc.

**Entregable:** `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` con encabezado y matriz; además `commands.log` y `result-summary.md` bajo el run dir.

**Comandos posteriores (no ejecutados):**
- `git -C ../sldb rev-parse HEAD`; análogos para `../pron` y `../spec2viz`.
- `git -C ../sldb status --porcelain | wc -l`; análogos.
- `rg -n "CAS|lock|revision|hash|index|search|ViewDoc|renderer"` en cada repo.
- `sha256sum <archivo-citado-sucio>` si aplica.
- `test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`
- `python desk/drawer/plans/workspace-documental/build_plan.py --check`
- `python desk/drawer/plans/workspace-documental/validate_plan.py --check`
- `python desk/drawer/plans/workspace-documental/context_review.py status`

**Resultado esperado:** documento no vacío, filas con evidencia y estados explícitos; checks en éxito; Tester muestrea filas sin discrepancias. Si falta prueba, la fila dirá «no comprobado» y su causa.
