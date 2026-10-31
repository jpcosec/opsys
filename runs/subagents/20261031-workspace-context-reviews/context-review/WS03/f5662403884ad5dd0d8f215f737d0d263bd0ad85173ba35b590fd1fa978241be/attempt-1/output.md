## REFORMULACION

**Propósito:** auditar en solo lectura `sldb/pron/spec2viz` para inventariar persistencia (fuente/payload), control de concurrencia real (CAS por revisión/hash, locks de archivo o DB), referencias documentales, búsquedas expuestas y alcance real de ViewDoc. Kimun es solo referencia.

**Resultado:** un documento en `deskops:desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` que distingue API comprobada mediante lectura citada del estado actual, ausencia y hueco.

**Repo dueño:** deskops, sin cambios interrepo.

**Límites:** solo lectura; no se modifica ningún repo auditado; no se promete consulta guardada ni migración Kimun.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo WS03 y dependencia WS01), `brief.md` para vocabulario documento/nodo/vista/renderer/consulta/foco, `alcance.md` para límites y reglas de ejecución, `decisiones.md` para no inferir aprobaciones Pxx, y código/estado actual de `sldb`, `pron` y `spec2viz` en modo lectura.

**Cambios previstos:** crear únicamente `auditoria/infraestructura.md` bajo `output_base`; ningún cambio en repos auditados ni en el Board.

**Dependencias:** WS01 debe haber fijado brief y glosario autosuficientes. La auditoría no requiere aprobar P01/P02/P04; si falta un contrato o permiso, se registra el hueco con repo dueño y no se crea sustituto.

**Validaciones futuras:** comprobar que la salida es documental y única; que cada API declarada tiene lectura citada; que ausencias y huecos están separados; que no hay cambios interrepo; revisión de aceptación y preflight de promoción según TaskDoc, sin ejecutarlos aquí.

## FUTURO

WS06 consume el inventario para su matriz de correspondencia. WS11/12 registran aceptación por repo receptor. WS07 designa responsables. Un humano decide las Pxx aplicables. La promoción fijará archivos, pills, átomos y evidencia. Si la auditoría revela una API inexistente, WS11/12 deberán registrar el hueco, repo dueño y dependencia nueva.
