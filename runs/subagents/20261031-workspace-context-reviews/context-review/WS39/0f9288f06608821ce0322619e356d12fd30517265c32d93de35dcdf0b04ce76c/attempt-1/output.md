## REFORMULACION
**Propósito:** integrar en graph_ui la inspección y edición de modelos Schema/clases ya existentes, accesibles desde documento/contexto, reutilizando `draft/validate/promote` de sldb sin reimplementar modelos.  
**Resultado:** representaciones/diálogos navegables en `shell/dialogs.js` y `views/models/`, pruebas y acta humana en `runs/subagents/workspace-documental-acceptance/modelos/acta.md`.  
**Repo dueño:** `graph_ui`.  
**Límites:** no reimplementar modelos; no habilitar `promote` si falta API/autoridad; mutaciones sujetas a WS12 y a los gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; acta humana antes de publicar disponibilidad.

## AMBIGUEDADES
1. **Alcance de la mutación según `source_mode`.** Cita: «UF09 inspección y mutación en store temporal real de prueba» y «usar draft/validate/promote de sldb». El contrato vecino WS12 indica: «aceptar delta en sldb solo si source_mode=editable». Si `source_mode=read_only`, no queda claro si WS39 puede cerrar solo con inspección o si la aceptación exige mutación y el nodo queda bloqueado. Obligaría a inventar el criterio de cierre en modo lectura.

## DRY-RUN
**Lecturas previstas:** nodo WS39, guía, brief, alcance, decisiones, cobertura y contratos vecinos WS12/WS16.  
**Cambios previstos:** vistas/diálogos de modelos en `graph_ui`; pruebas en store temporal real; acta de prueba humana; sin tocar otros repos.  
**Dependencias:** contrato y whitelist de WS12; recorrido de lectura aprobado en WS16; gates `G_WRITE_CONTRACT`, `G_UI_WRITE`, `G_HUMAN_READ`.  
**Validaciones futuras:** comprobar efectos/errores declarados por WS12; verificar que no se habilita `promote` sin API/autoridad; ejecutar prueba humana y registrar `G_HUMAN_MODEL`. No se ejecuta nada.

## FUTURO
WS12 debe producir la capability exacta de las operaciones de modelos y aceptar el delta de graph_ui; WS16 debe aportar `G_HUMAN_READ`. La persona que fije P08 decidirá el participante del acta. WS31 publicará el capítulo 15 del manual solo tras `G_HUMAN_MODEL`. La promoción del nodo y el TaskDoc fijarán archivos, escenarios y textos concretos.
