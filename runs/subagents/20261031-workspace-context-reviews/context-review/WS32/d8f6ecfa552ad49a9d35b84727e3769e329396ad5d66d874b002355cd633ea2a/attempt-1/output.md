## REFORMULACION

**Propósito:** unificar la identidad de intento y el cierre de Scion sin crear un segundo pipeline: el intento no es el slug, `dispatch intent` y `dispatch confirmed` son hechos separados, y manifiesto, RunDoc y cierre deben ser consistentes e idempotentes sobre el intento correcto.

**Resultado:** nodo agregado no ejecutable; su resultado son las salidas de WS32.1 (separar identidad de intento y dispatch) y WS32.2 (idempotencia de manifiesto y cierre). Se cumple cuando ambos hijos cumplen su aceptación.

**Repo dueño:** `deskops`. **Límites:** depende de WS05 y WS12; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; promoción no autorizada; prohíbe duplicar pipeline o implementación ya reconciliada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas previstas:** nodo WS32 en `dag.yaml`, guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`. No se ejecutan comandos.
- **Cambios previstos:** ninguno; esta revisión no edita repos ni promueve el nodo.
- **Dependencias:** WS05 (inventario Scion) y WS12 (contrato de operaciones); hijos WS32.1/WS32.2 como componentes de la aceptación agregada. Gates: G_CLOSEOUT satisfecho; G_SCION no verificado, producido por WS44; G_WRITE_CONTRACT pendiente y evaluado por delta.
- **Validaciones futuras:** comprobar aceptación de WS32.1 y WS32.2; recibos por delta de G_WRITE_CONTRACT; verificar G_SCION mediante el probe de WS44; al promover, aplicar la matriz WS06 sin duplicar tareas.

## FUTURO

- WS44 ejecuta el probe real de Scion y designa operador; hasta entonces G_SCION sigue sin verificar.
- WS12 produce el contrato técnico por operación/delta aplicable a WS32.
- Los implementadores de WS32.1/WS32.2 aportan evidencia de sus aceptaciones.
- Una persona decide la promoción y WS06 integra el delta en el ticket receptor vigente.
- El estado de gates pendientes no es defecto de este nodo.
