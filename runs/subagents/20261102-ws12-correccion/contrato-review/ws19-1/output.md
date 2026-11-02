REFORMULACION
WS19.1 «Editar campos con conflicto visible»: entregar en graph_ui la edición de campos de un documento con precondición de payload y conflicto visible. Resultado: delta en `frontends/mindmap/views/workspace/fields/` más tests, consumiendo endpoints del contrato WS12 sin cambiarlo. Repo: graph_ui (`output_base: repository_root`). Límites: depende de WS12, WS47 y WS48; requiere G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT; no edita campos workflow-protegidos; solo desk en modo manual exclusivo; documentos con contenido no declarado no editables hasta WS47; promoción no autorizada.

AMBIGUEDADES
1. «Delta sobre workspace integrado a1b2b22 de edición»: no dice qué árbol/commit es a1b2b22 ni cómo integrarlo; obligaría a inventar la base.
2. «reutilizando editores y API»: no nombra editores ni rutas; obligaría a inventar qué se reutiliza y qué se crea.
3. «endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato»: no aclara si puede añadir la ruta/filtro HO-02 —que WS12 asigna a WS19.1— o solo consumir rutas existentes; obligaría a inventar la frontera.
4. «conflicto visible (mensaje de rechazo con el texto local conservado)»: no fija forma ni código de error (WS12 lo remite a HO-01); obligaría a inventar el contrato de error.
5. «workspace integrado a1b2b22» frente a WS12 §1.2, que excluye `frontends/workspace/` como base: no aclara si es el mismo árbol; obligaría a decidir cuál prevalece.

DRY-RUN
Ejecutor hipotético: leería WS12 §2–4, §6 y §10.2, los productos de WS47/WS48/WS45 y el workspace actual. Cambios previstos: archivos bajo `views/workspace/fields/`, consumo de `/api/save` con `changes[update, expected]`, rechazo de campos protegidos, mensaje de conflicto conservando buffer local, y tests. Dependencias: `expected` (WS45), guarda de contenido (WS47), admisión (WS48); sin ellas no habilita escritura. Errores esperados: 409 por `expected` obsoleto, rechazo de campo protegido, 500 parcial sin reversión. Validación futura: guardar/recargar confirma el dato; escritura obsoleta da 409 sin perder texto; contenido no declarado no editable.

FUTURO
Producen otros nodos: WS47 (guarda), WS48 (admisión), WS45 (G_PAYLOAD_PRECONDITION) y P01 (acta G_UI_WRITE). Decide un humano: G_HUMAN_READ y autorización de promoción; root evalúa G_WRITE_CONTRACT.
