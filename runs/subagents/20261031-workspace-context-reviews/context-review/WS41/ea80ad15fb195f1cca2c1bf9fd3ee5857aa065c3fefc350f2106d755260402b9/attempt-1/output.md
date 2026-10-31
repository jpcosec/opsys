## REFORMULACION

**Propósito:** implementar lectura segura entre desks en `graph_ui`, resolviendo aliases/roots autorizados por el contrato WS11 mediante APIs públicas de store.

**Resultado:** UF08 sobre dos stores del corpus WS40: identidad/origen visibles, seguimiento de enlaces authored entre desks, retorno por historia y errores visibles ante alias no autorizado, path escapado o store ausente. Sin federación ni copia de contenido.

**Repo dueño:** `graph_ui`, en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** solo lectura; cada request conserva proyecto/store sin alterar `SLDB_STORE` global; sin mutaciones cruzadas; requiere recibo `G_UI_READ` por delta. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

Las referencias a aliases/roots autorizados y APIs públicas remiten a WS11, que el propio nodo nombra como productor; si falta, aplica la regla común de detenerse y registrar el hueco. Los textos exactos de error y la disposición visual quedan delegados al TaskDoc de promoción. El corpus y sus enlaces cruzados son producidos por WS40. La aceptación es comprobable mediante UF08 y casos de rechazo.

## DRY-RUN

**Lecturas previstas:** nodo WS41 y aristas vecinas WS11/WS13/WS40; guía, brief, alcance, decisiones y cobertura.

**Cambios previstos:** implementación de lectura multidesk en `frontends/mindmap/source/` y `views/workspace/`; pruebas en `tests/`; consumo del contrato WS11 y del manifiesto WS40. No se modifican otros repos ni datos de dominio.

**Dependencias:** WS11 (contrato de navegación, identidad y lectura multidesk), WS13 (lector con historia/foco), WS40 (corpus y manifiesto con dos desks y enlaces authored), `G_UI_READ` por delta. Transitivas: WS09/WS08 detrás de WS11.

**Validaciones futuras:** pruebas técnicas sobre los dos stores de WS40; verificación de errores visibles para alias no autorizado, path escapado y store ausente; comprobación de no mutación y de conservación de store por request; UF08 dentro de WS16 con humano real; registro del recibo `G_UI_READ` con actor P01, alcance, efecto y commit verificable.

## FUTURO

- WS11 debe entregar el contrato con aliases/roots y APIs públicas.
- WS40 debe entregar corpus y manifiesto con enlaces entre desks.
- WS13 debe entregar lector, historia y foco.
- P01/receptor de `graph_ui` debe emitir el recibo `G_UI_READ` del delta.
- WS16 ejecuta la validación humana UF08.
- La promoción fijará TaskDoc, archivos exactos, textos y evidencias; no corresponde a este nodo.
