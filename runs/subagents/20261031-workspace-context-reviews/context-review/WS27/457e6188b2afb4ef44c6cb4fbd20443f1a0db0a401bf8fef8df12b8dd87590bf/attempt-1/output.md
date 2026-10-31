## REFORMULACION
**Propósito:** definir WS27 como nodo agregado que reúne la revisión de cambios y evidencia junto a la TaskDoc.  
**Resultado:** salidas agregadas de WS27.1 (diff Git e historial read-only) y WS27.2 (evidencia declarada/encontrada/verificada), sin ejecución propia.  
**Repo dueño:** `graph_ui`.  
**Límites:** solo lectura; no escribir, revertir ni inferir cierre por commit; aceptación no ejecutable, cumplida cuando sus hijos cumplen la suya; promoción no autorizada; los dependientes siguen dependiendo de WS27.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS27 y contratos vecinos WS13/WS12/WS27.1/WS27.2/WS28/WS35 y gate G_UI_READ.  
**Cambios previstos:** ninguno; WS27 es `aggregate` y no se ejecuta. No se modifica `dag.yaml` ni se promueve tarea.  
**Dependencias:** WS13 y WS12 como prerrequisitos; WS27.1 y WS27.2 como hijos cuyo cumplimiento cierra el agregado.  
**Validaciones futuras:** aceptación de ambos hijos; recibo G_UI_READ por delta según `evaluation=per_delta`; contraste con `reconciliacion.md` antes de cualquier promoción; comprobar que la base citada no se use para inferir cierre.

## FUTURO
- **WS27.1:** produce diff e historial read-only por repo y tarea.
- **WS27.2:** produce la vista de evidencia declarada, encontrada y verificada.
- **WS13:** entrega lector con historia y foco sobre el que se integran ambos.
- **WS12:** fija el contrato de operaciones y la correspondencia de evidencia.
- **Receptor P01:** emite el acta G_UI_READ del delta concreto en el repo receptor.
- **Humano/promoción:** decide la promoción; el TaskDoc fijará archivos, pruebas y textos.
