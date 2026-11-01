## REFORMULACION

**Propósito:** mantener un registro trazable y reutilizable de las decisiones ya acordadas, sin reabrir preguntas ni fabricar aceptaciones. **Resultado:** `decisiones.md` verificado/actualizado solo ante cambio real, más `baseline_proposal` y `parameters.source_mode` en `dag.yaml` coherentes con P04. **Repo dueño:** deskops. **Límites:** no repetir preguntas resueltas; no inferir aceptación de API/UI ni permisos Scion; P07/P09 son defaults técnicos delegados, no firmas humanas; `source_mode=editable` queda condicionado a G_SOURCE, que produce WS20; no implementa contratos ni sustituye auditorías de WS06.

## AMBIGUEDADES

Ninguna. El encargo identifica resultado, fuentes (`decisiones.md`, `owner-decisions.json`), criterio de actualización y límites. Las frases «actualizar solo por cambio real de decisión» y «nueva decisión explícita con fuente verificable» remiten a una decisión humana futura, no obligan a inventar: si no existe, se conserva lo registrado.

## DRY-RUN

Un ejecutor futuro leería `decisiones.md`, `owner-decisions.json` (respuestas 0–2), `brief.md`, `alcance.md`, `cobertura.md` y los campos de `dag.yaml` citados en `output_scope`. Verificaría, Pxx por Pxx, que constan tipo humano/técnico, actor, fuente y nodos/gates; contrastaría que no se repiten preguntas ni se atribuyen aceptaciones de API/UI/Scion; comprobaría que `baseline_proposal` conserva la base acordada y que `source_mode` sigue condicionado a G_SOURCE. Consumiría WS06 como prerrequisito, sin editar `reconciliacion.md`. Si todo coincide, no habría cambios: el resultado es verificación registrada. Si detecta una decisión nueva explícita y verificable, actualizaría únicamente las filas y campos afectados. Errores esperados: Pxx sin fuente, contradicción entre `decisiones.md` y `owner-decisions.json`, o intento de actualización sin fuente → detenerse y registrar el hueco, sin inventar decisión ni habilitar contratos. Validación: cada Pxx trazable, sin preguntas repetidas, sin aceptación técnica/Scion inferida y con `source_mode` condicionado. No se ejecuta nada.

## FUTURO

La promoción (`promotion: not_authorized`) y el TaskDoc con archivos, pills, átomos y evidencia quedan para otro nodo o decisión humana. WS06 aporta `reconciliacion.md`. WS20 produce G_SOURCE. WS08/09/10/44 consumen G_PRODUCT. Nuevas decisiones humanas con fuente verificable habilitan cambios en el registro; las actas de P08 siguen pendientes.
