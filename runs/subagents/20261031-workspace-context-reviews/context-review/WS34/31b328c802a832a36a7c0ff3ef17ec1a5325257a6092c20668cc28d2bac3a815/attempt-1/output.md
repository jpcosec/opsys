**REFORMULACION**
Propósito: exponer un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: agregado no ejecutable; se cumple cuando WS34.1 y WS34.2 cumplen su aceptación, y los dependientes siguen dependiendo de WS34. Repo dueño: `deskops`. Límites: no shell arbitrario ni duplicar transporte; no enviar mensajes en planificación; mutaciones sujetas a `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT` por delta; promoción `not_authorized`.

**AMBIGUEDADES**
Ninguna. El nodo es agregado no ejecutable y delega el detalle operativo en WS34.1, WS34.2 y el contrato WS12; el umbral de timeout no debe inventarse aquí.

**DRY-RUN**
Lecturas: `dag.yaml#node:WS34`; guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`. Cambios previstos: ninguno en WS34; no se ejecuta nada. Dependencias: WS33, WS12, WS34.1, WS34.2. Gates: `G_EXEC` pendiente/externo; `G_SCION` no verificado, productor WS44; `G_WRITE_CONTRACT` pendiente `per_delta`, productor WS12. Validaciones futuras: aceptación de ambos hijos; política de timeout por delta verificada en `G_WRITE_CONTRACT`; probe Scion de WS44; autorización humana de ejecución; agregación de evidencias.

**FUTURO**
WS34.1 producirá el adaptador de dispatch; WS34.2, el de reply. WS12 fijará en el contrato la política y umbral de timeout aplicables a cada delta. WS44 aportará el probe público de Scion. El humano/designee emitirá la autorización `G_EXEC`. WS36 consumirá solo el adaptador WS34. La promoción, si se autoriza, fijará archivos, pruebas y evidencia en TaskDoc.
