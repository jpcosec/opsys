## REFORMULACION

**Propósito:** definir el encargo de planificación de WS15.2, orientación para un proyecto sin desk dentro de UF10.  
**Resultado:** una implementación en graph_ui que muestre orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`, sin mutar nada ni inicializar por GET; tras un init externo, refrescar debe mostrar el desk real.  
**Repo:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/orientation/` y `tests/`.  
**Límites:** solo lectura; rutas según contrato WS11; no inicializar desde GET; `G_UI_READ` es gate por delta; no se autoriza promoción ni implementación.

## AMBIGUEDADES

Ninguna. El nodo concreta resultado, repo, límites y aceptación; las rutas dependen de un contrato con productor nombrado (WS11) y el gate pendiente es intencional.

## DRY-RUN

**Lecturas:** nodo WS15.2 y fuentes suministradas (guía, brief, alcance, decisiones, cobertura, reconciliación); aristas vecinas solo como contexto, sin revisarlas.  
**Cambios previstos:** ninguno por este revisor. La implementación futura se limitaría a orientación y pruebas en graph_ui.  
**Dependencias:** WS13 y, transitivamente, WS11/WS02–WS10; `G_UI_READ` por delta.  
**Validaciones futuras:** abrir proyecto sin desk sin mutación; comprobar orientación, ruta absoluta y comando; ejecutar init fuera de la UI; refrescar y verificar que aparece el desk real; no confundir con errores de WS15.1.

## FUTURO

WS11 produce el contrato de rutas de lectura. El receptor humano designado en P01 emite el acta de `G_UI_READ` para este delta concreto. La promoción/TaskDoc fijará archivos exactos y pruebas detalladas. WS16 y el corpus WS40 validarán el recorrido. La ejecución del init externo corresponde a CLI o persona, fuera de la UI.
