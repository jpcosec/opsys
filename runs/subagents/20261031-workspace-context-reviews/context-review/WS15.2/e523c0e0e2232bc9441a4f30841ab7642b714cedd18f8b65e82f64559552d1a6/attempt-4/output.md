REFORMULACION
- Propósito: cubrir UF10 en un proyecto sin desk mostrando orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`; nunca inicializar por GET. Tras un init externo real, refrescar la lectura.
- Resultado: delta de UI en `graph_ui` bajo `frontends/mindmap/views/workspace/orientation/`, con tests y rutas de lectura según el contrato WS11.
- Repo dueño: `graph_ui`.
- Límites: no mutar nada al abrir; no inicializar desde la UI ni por GET; el init ocurre fuera; integración como delta o ticket existente, sin duplicar en paralelo; promoción no autorizada.
- Dependencias: WS13 y gate `G_UI_READ` (resuelto por WS11, transitivo).
- Aceptación: dos escenarios comprobables: apertura sin desk con orientación/destino y sin mutación; tras init externo, refresco muestra el desk real.

AMBIGUEDADES
ninguna.

DRY-RUN
- Lecturas previstas: nodo WS15.2, guía, brief, alcance, decisiones, cobertura, reconciliación y bloques de dag.yaml suministrados. Sin herramientas ni ejecución.
- Cambios previstos: solo vista de orientación y tests dentro del `output_scope`; ninguna escritura de inicialización ni mutación del proyecto.
- Dependencias: WS13 debe entregar lectura de workspace; WS11 produce el contrato de rutas y `G_UI_READ`; la matriz WS06 llega transitivamente.
- Validaciones futuras: fixture de proyecto sin desk; comprobar orientación, destino y ausencia de mutaciones; ejecutar `deskops init` fuera de la UI y verificar que el refresco muestra el desk real. No se valida aquí.

FUTURO
- WS11 produce el contrato de rutas de lectura y resuelve `G_UI_READ`; el responsable de `graph_ui` debe aceptar el delta.
- La promoción exige TaskDoc, archivos/pills/evidencia y preflight, y sigue sin autorización.
- WS16 valida la entrega L; WS40 aporta el corpus de prueba. No son ambigüedades de este nodo.
