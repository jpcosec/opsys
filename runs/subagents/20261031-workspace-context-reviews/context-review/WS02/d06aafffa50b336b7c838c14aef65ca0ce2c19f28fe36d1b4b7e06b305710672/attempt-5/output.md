## REFORMULACION
- **Propósito:** inventariar superficies y operaciones de Deskops: modelos y Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas públicas (CLI y `DeskopsOperations`), efectos Git y cierre.
- **Resultado:** `auditoria/deskops.md` con filas que incluyan archivo/código/operación y estado comprobado mediante cita `archivo:línea` o salida de comando de solo lectura; lo no comprobado se marca.
- **Repo dueño:** `deskops`; salida bajo `desk/drawer/plans/workspace-documental/`.
- **Límites:** no inferir modelo por carpeta; promoción `not_authorized`; depende de WS01; sin gates.

## AMBIGUEDADES
1. «Inventariar superficies y operaciones Deskops»: no se define «superficie» ni su unidad. El ejecutor tendría que inventar si cuenta archivos, comandos, modelos, endpoints, componentes UI o filas del desk, con riesgo de exceder el alcance.
2. «Cada fila incluye archivo/código/operación y estado comprobado»: la barra no aclara si exige los tres campos o uno de ellos. Afecta a la aceptación comprobable; el ejecutor inventaría el contrato de fila.
3. «lo no comprobado se marca así»: no hay vocabulario para distinguir ausente, inaccesible o no encontrado. El ejecutor inventaría estados y podría declarar como «no comprobado» algo que simplemente no existe.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md` y, al ejecutar, código/CLI de Deskops; ahora no se ejecuta nada.
- **Cambios previstos:** crear/editar `auditoria/deskops.md`; no tocar código ni Board.
- **Dependencias:** WS01; sin `requires`; promoción no autorizada.
- **Validaciones futuras:** cada fila con `archivo:línea` o salida de solo lectura; marcar lo no comprobado; no inferir modelo por carpeta.

## FUTURO
WS06 y WS10 consumen la auditoría; WS07 designa responsables y el humano decide P01/P02/P04/P07/P09. El TaskDoc de promoción fijará archivos, pills y evidencia; la autorización de promoción es humana. Si falta `sldb models list` o un contrato, se registra el hueco según `alcance.md`, sin sustituirlo.
