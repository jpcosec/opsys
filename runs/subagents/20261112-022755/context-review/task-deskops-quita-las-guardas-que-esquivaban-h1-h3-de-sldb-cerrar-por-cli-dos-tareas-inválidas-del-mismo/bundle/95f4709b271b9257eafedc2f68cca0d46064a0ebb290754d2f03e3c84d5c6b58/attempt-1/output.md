## REFORMULACION

**Propósito.** Quitar de deskops las tres guardas añadidas mientras sldb abortaba stores check ante el primer documento inválido (H1) y re-extraía el modelo entero en cada escritura (H2/H3), una vez que la corrección de sldb está en main.

**Resultado.** En `deskops/services/closure.py`, retire, supersede y resolved-by dejan de bloquearse por otra tarea inválida del mismo modelo; en `deskops/cli/commands/desk.py`, `update --apply` deja de saltarse las reparaciones cuando stores check entrega informe pese a documentos inválidos; informe y doctor nombran los inválidos por `store/doc-invalid` sin duplicar el listado por frontmatter; tests nuevos (caché fría y caliente) y reescritos los que fijaban el rechazo por H2; operator-manual (estados heredados) y CHANGELOG.

**Repo.** deskops, suite desde /dev/shm, contra un clon de sldb origin/main ya corregido.

**Límites.** Fuera: tabla de migración de estados heredados y su escritura por frontmatter, listado de inválidos del doctor (ver ambigüedad 1), y todo cambio en sldb.

## AMBIGUEDADES

1. Scope: "Fuera: … el listado de tareas inválidas del doctor" frente a g3: "el informe de desk update y el doctor listan los documentos inválidos por el hallazgo store/doc-invalid de sldb además del listado por frontmatter que ya existe". Obliga a inventar si `doctor_findings.py` se modifica o no.
2. g1: "y las dos funciones si quedan sin uso". No nombra cuáles (¿`_other_invalid_tasks`, `_blocked_by_invalid_tasks`?) ni el criterio de "sin uso"; obliga a inventar el alcance del borrado.
3. g2: "sin informe y sin documentos inválidos que lo expliquen". No define cómo se decide que un fallo "lo explican" documentos inválidos.
4. Validación: "variable de entorno SLDB_SRC si la tarea de SLDB_SRC ya entró, o la ruta hermana en la copia". No fija valor, ruta ni comprobación de que ese sldb trae la corrección.
5. g3: "sin duplicarlos". No dice la clave de deduplicación (ruta, nombre, ambos) ni el orden de las líneas.
6. g4: "siempre con caché frío además del caliente". No define cómo se fuerza la caché fría (¿`XDG_CACHE_HOME`, `.sldb_cache/`?).

## DRY-RUN

**Lecturas:** `closure.py` (guardas y textos H2), `desk.py` (rama `store_check_error` y salto de reparaciones), `doctor_findings.py` (`invalid_task_findings`, notas), `tests/`, `docs/operator-manual.md` (secciones "Desk scaffold…" y "Closeout"), `CHANGELOG.md`; y en sldb, el hallazgo `store/doc-invalid` y la forma del informe de stores check.

**Cambios previstos:** g1 borrar llamadas (y funciones si quedan huérfanas); g2 eliminar el salto conservando el error real; g3 añadir el hallazgo al informe/doctor según se resuelva la ambigüedad 1; g4 reescribir tests de rechazo como casos (a) y añadir (a)/(b) con caché fría; g5 manual y CHANGELOG.

**Dependencias:** sldb main con H1-H3 y `store/doc-invalid`; `SLDB_SRC` o ruta hermana.

**Validaciones futuras:** tests por archivo, suite completa de a un archivo desde /dev/shm contra el sldb corregido, caché fría y caliente.

## FUTURO

No es ambigüedad: la entrada de la corrección de sldb en main la confirma otro nodo; los 4 pasos del CI los corre el coordinador; la baja del ítem de drawer 75e33dab y la decisión sobre si el doctor entra en alcance corresponden al humano.
