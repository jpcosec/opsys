## REFORMULACION
**Propósito:** inventariar el trabajo actual de graph_ui y reconciliarlo con los nodos del plan que tocan ese repo, incluyendo sesiones y solapamientos.  
**Resultado:** `auditoria/ui.md` con tareas externas (path, estado observado, hash SHA256 y alcance), solapamientos, reconciliación del SPEC externo y encargo aportado.  
**Repo dueño:** deskops; lectura de `../UIs/graph_ui` y del SPEC externo indicado.  
**Límites:** no cambiar tareas ni sesiones; no ejecutar; el hash es SHA256 del archivo de tarea.

## AMBIGUEDADES
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui». La aceptación enumera tareas externas, solapamientos, SPEC y encargo, pero no exige demostrar el mapeo de cada nodo ni la identificación de sesiones que pide el scope. Obligaría a inventar cómo evidenciar la completitud de ese mapeo.
2. «tarea o entrada del Board de graph_ui, o commit que ya lo implementa». No define qué registrar cuando un nodo toca graph_ui pero no tiene tarea, entrada de Board ni commit correspondiente. Obligaría a inventar si se anota una ausencia, con qué formato, o se omite.
3. «o commit que ya lo implementa». No fija rango de historial ni criterio para decidir que un commit implementa el nodo. Obligaría a inventar hasta dónde revisar y qué cuenta como implementación.

## DRY-RUN
**Lecturas previstas:** `dag.yaml`, brief, alcance, decisiones, reconciliación, Board/tareas/código de graph_ui, estado git y paneles herdr, `SPEC.md` externo y encargo aportado si existe.  
**Cambios previstos:** crear `auditoria/ui.md` en deskops; ningún cambio en graph_ui.  
**Dependencias:** WS01 produce brief/glosario; graph_ui se lee sin modificar.  
**Validaciones futuras:** cada tarea externa con path/estado/hash/alcance; solapamientos por misma tarea o archivos reclamados; SPEC con path y hash; ausencia de escrituras en graph_ui.

## FUTURO
WS06 consumirá `auditoria/ui.md` para la matriz de correspondencia. WS11/12 obtendrán aceptación específica por delta. La promoción y autorización de ejecución quedan a decisión humana; este nodo no las concede.
