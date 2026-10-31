## REFORMULACION
**Propósito:** implementar en `graph_ui` la edición de campos del workspace consumiendo el contrato de WS12, con revisión esperada y conflicto visible.  
**Resultado:** guardar/recargar persiste el dato real; una escritura obsoleta conserva el texto local y muestra el conflicto; los campos workflow-protected no son editables por este canal; la mutación queda limitada a desk en modo manual exclusivo.  
**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/fields/` y `tests/`, sin cambiar el contrato WS12.  
**Límites:** solo campos, no relaciones ni fuente raw; no se autoriza promoción ni ejecución; no se modifican otros repos ni el Board; si falta una API/contrato, se detiene y se registra el hueco.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas:** nodo WS19.1, guía, brief, alcance, decisiones, cobertura, reconciliación, aristas WS12/WS16/WS19 y gates.  
**Cambios previstos:** componentes de edición de campos, manejo de rechazo por revisión obsoleta y pruebas de guardado/recarga y conflicto.  
**Dependencias:** WS12 aporta whitelist, canal, CAS/locks y `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16 aporta `G_HUMAN_READ`; WS11/WS08 llegan transitivamente.  
**Validaciones futuras:** guardar/recargar contra store real o corpus WS40; escritura obsoleta sin pérdida de texto local; campos protegidos no editables; modo manual exclusivo y modos read-only. No se ejecuta nada.

## FUTURO
WS12 debe cerrar el contrato y la aceptación del delta en `graph_ui`; WS16 debe producir la aprobación humana de lectura; una persona debe decidir P03 —y las demás Pxx aplicables— y autorizar la promoción. El TaskDoc de promoción fijará archivos, textos y escenarios de prueba. WS19.2 cubrirá relaciones dentro del agregado WS19. Si falta el contrato o permiso, aplica la regla común: detenerse, registrar repo dueño y dejar la operación no disponible.
