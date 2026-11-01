## REFORMULACION
**Propósito:** convertir los user-flows en un encargo de planificación comprobable: cada UF con entrada/salida, operación real, error, nodo del DAG y gate humano. **Resultado:** `borradores/user-flows.md` actualizado para UF01–UF10, cubriendo manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado. **Repo:** deskops, con `output_scope` en ese archivo. **Límites:** solo redacción/planificación; no implementa ni muta; UF08 es lectura y el envío interdesk queda fuera; UF06 se documenta condicionada a G_SCION/G_EXEC sin habilitarla; una operación ausente se marca hueco, no se inventa.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas:** nodo WS08, guía, brief, alcance, decisiones, cobertura, validacion-humana y `borradores/user-flows.md`; auditorías `auditoria/{deskops,infraestructura,ui}.md` por dependencia transitiva WS06/WS07; G_PRODUCT ya satisfecho.

**Cambios previstos:** en `borradores/user-flows.md`, completar cada UF01–UF10 con entrada/salida, operación citada de auditoría, error o comportamiento degradado, lista completa de nodos y gate humano (WS16/30/37/39 o “ninguno adicional”). UF02: respuesta local y ack pendiente de WS12. UF06: condicionada a G_SCION/G_EXEC. UF07: distinguir diagnóstico de la prueba técnica WS29. UF08: solo lectura. Marcar huecos con productor si falta una operación.

**Dependencias consumidas:** auditorías WS02–WS04 vía WS06/WS07; decisiones P01–P09; cobertura y protocolo humano. Contratos WS11/WS12 aún no se consumen como disponibles.

**Validaciones futuras:** checklist 10/10 UFs; toda operación con fuente; ningún nodo/gate inventado; ninguna promesa fuera de alcance; coherencia con `cobertura.md` y `validacion-humana.md`; huecos con dueño.

**Errores esperados:** auditoría u operación ausente → registrar hueco y no sustituir; contrato WS12 ausente → ack como pendiente; no bloquear el resto del mapeo por ese hueco.

## FUTURO
WS09 usará estos UFs para el catálogo de renderizaciones; WS11/WS12 producirán contratos de navegación y operaciones; WS16/30/37/39 registrarán actas humanas; WS29 aportará su prueba técnica propia; la promoción y cualquier cambio de alcance los decide un humano.
