## REFORMULACION
**Propósito:** implementar en `graph_ui` lectura segura entre desks, resolviendo aliases/roots autorizados por el contrato WS11 y usando APIs públicas de los stores.  
**Resultado:** lectura de un segundo desk y vuelta por historia, con identidad/origen visibles, errores visibles y sin mutaciones cruzadas.  
**Repo:** `graph_ui` (`frontends/mindmap/source/`, `views/workspace/`, `tests/`).  
**Límites:** solo lectura; no cambiar global `SLDB_STORE`; no aceptar roots/paths arbitrarios; no afirmar federación por copia; no ejecutar promoción.

## AMBIGUEDADES
Ninguna. Las referencias al contrato WS11, corpus WS40 y gate `G_UI_READ` tienen productor nombrado; la falta de contrato/API se cubre con las reglas comunes de `alcance.md`. La aceptación es comprobable mediante UF08 sobre dos stores y casos de error visibles; textos exactos y pruebas quedan al TaskDoc de promoción.

## DRY-RUN
**Lecturas:** nodo WS41; guía; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; contratos vecinos WS11, WS13, WS40, WS16 y gate `G_UI_READ`.  
**Cambios previstos:** solo si se autoriza promoción, implementar rutas de lectura por store, vista/workspace y tests dentro del `output_scope`; sin ejecutar ahora.  
**Dependencias:** WS13 aporta lector, foco, tabs/historia; WS11 define contrato de resolución, aliases/roots y APIs públicas; WS40 aporta corpus con dos desks. `G_UI_READ` está pendiente.  
**Validaciones futuras:** UF08 sobre dos stores de WS40; identidad/origen visibles; navegación entre enlaces authored y vuelta por historia; error visible para alias no autorizado, path escapado y store ausente; sin mutaciones cruzadas. WS16 hará la validación humana.

## FUTURO
WS11 produce contrato y acta `G_UI_READ`; WS40 produce corpus/manifiesto; WS13 entrega lector/historia; WS16 valida con humano. La promoción de WS41 y la designación de responsables dependen de autorización humana/WS07, no de este nodo.
