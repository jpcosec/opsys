REFORMULACION
- **Propósito:** extender la tarea Changes existente para mostrar impacto comprobable del store actual, sin duplicar esa tarea.
- **Resultado:** vista en graph_ui que, ante una mutación real en store temporal, muestra documento afectado, relaciones entrantes/salientes a 1 hop vía API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando y enlazados al comando documentado de reparación; sin reparación automática.
- **Repo:** graph_ui.
- **Límites:** no CST ni árbol Kimun; no bloquea lector/manual básico; pruebas sobre store temporal real; no promete reparación; gate G_UI_READ por delta.
- **Dependencias:** WS15, WS24; contrato de rutas WS11; G_UI_READ.

AMBIGUEDADES
ninguna

DRY-RUN
- **Lecturas previstas:** nodo WS29 y edges de WS15/WS24; referencia externa de la tarea Changes; contrato WS11; salidas de WS24/WS03 sobre API de grafo; documentación de los tres comandos en sus repos dueños; decisiones y reconciliación.
- **Cambios previstos:** vista/integración en `frontends/mindmap/views/workspace/changes/`; rutas de integridad según WS11; tests con store temporal real.
- **Dependencias:** WS15 completado cuando lo estén sus hijos; WS24 con grafo local y API de sldb; WS11 definiendo rutas de integridad; comandos disponibles y documentados; recibo G_UI_READ del delta concreto.
- **Validaciones futuras:** mutación real muestra documento afectado, relaciones a 1 hop en ambos sentidos y hallazgos agrupados por comando; enlaces a la documentación correcta; ausencia de reparación automática; preflight del TaskDoc; contraste de no solapamiento con Changes.

FUTURO
- La promoción/TaskDoc fijará archivos, escenarios, pills y evidencia.
- WS06 decidirá delta sobre ticket existente o tarea atómica sin solapamiento.
- El receptor P01 emitirá el acta G_UI_READ por delta.
- WS11 entregará las rutas de integridad; WS24/WS03, la API de grafo.
- Los repos dueños mantendrán documentados los comandos; si faltan, se detiene y se registra el hueco.
- La aceptación humana de WS29 y su integración en Changes quedan fuera de este nodo.
