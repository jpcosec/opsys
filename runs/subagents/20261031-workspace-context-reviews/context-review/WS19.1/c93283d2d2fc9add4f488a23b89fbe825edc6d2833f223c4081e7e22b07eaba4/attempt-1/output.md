## REFORMULACION
**Propósito:** encargo de implementación para editar campos en `graph_ui` reutilizando editores y API, con conflicto visible y campos workflow-protegidos excluidos; es un delta sobre un ticket draft de edición.  
**Resultado:** mutación de campos cuyo guardado/recarga confirma el dato y que conserva el texto local ante una escritura obsoleta.  
**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).  
**Límites:** solo desk en “modo manual coordinado”; otros modos read-only hasta contrato; workflow-protected no editables por este canal; endpoints sujetos al contrato WS12.  
**Dependencias:** WS12 y WS16; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. **“modo manual coordinado” contradice P03.** WS19.1: *“Mutación restringida a desk en modo manual coordinado; otros modos read-only hasta contrato.”* P03: *“Baseline editable solo en desk en modo manual exclusivo; con coordinador escritor activo, UI read-only/handoff hasta canal autorizado real.”* El ejecutor tendría que inventar si “coordinado” implica coordinador activo y, por tanto, si puede escribir o debe quedar read-only.
2. **“revisión esperada y conflicto visible” no define resultado ni aceptación comprobable.** WS19.1: *“con revisión esperada y conflicto visible”*; la aceptación solo añade *“una escritura obsoleta no pierde texto local”*. No se define si “revisión” es CAS, revisión humana u otra, ni qué hace “visible” al conflicto. El ejecutor tendría que inventar comportamiento y criterio de verificación.

## DRY-RUN
**Lecturas:** input.md, guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.1 y contratos de vecinos WS12/WS16/gates.  
**Cambios previstos:** ninguno; solo revisión, sin ejecución.  
**Dependencias:** WS12 produce contrato/whitelist y G_WRITE_CONTRACT/G_UI_WRITE; WS16 produce G_HUMAN_READ; WS19 es agregado padre; WS19.2 es hermano; WS06 propone correspondencia con ticket.  
**Validaciones futuras:** comprobar aceptación con guardar/recargar y escritura obsoleta; verificar evidencia de gates y `scope_nodes`; confirmar que el modo de mutación coincide con P03.

## FUTURO
WS12 debe emitir contrato, whitelist y gates G_WRITE_CONTRACT/G_UI_WRITE. WS16 debe producir el acta de G_HUMAN_READ. WS06 debe proponer la correspondencia con el ticket draft. La promoción decidirá archivos, pills, átomos y evidencia, y exigirá preflight task-only. El humano debe resolver P03/P04 y designar al responsable de graph_ui (P01). WS19 cerrará cuando lo hagan WS19.1 y WS19.2.
