REFORMULACION
- **Propósito:** planificar el explorador del lector workspace para documentos modelados del store y Markdown no modelado del desk.
- **Resultado:** explorador que permite abrir ambos tipos sin conocer su ID ni usar índices nuevos; las altas aparecen tras refresco explícito, sin reiniciar servidor ni cambiar código.
- **Repo:** graph_ui.
- **Límites:** solo lectura; salida en `frontends/mindmap/views/workspace/explorer/`, rutas del contrato WS11 y tests; reutilización permitida del catálogo/filtro para modelados; API/seguridad de no modelados según WS11; no duplicar el workspace; depende de WS13.1 y G_UI_READ.

AMBIGUEDADES
Ninguna. Lo no fijado —API/seguridad de no modelados, archivos exactos, textos de pantalla y escenarios de prueba— está delegado expresamente a WS11, al TaskDoc de promoción o a las reglas comunes de alcance.md.

DRY-RUN
- **Lecturas previstas:** nodo y aristas en `dag.yaml`; contrato WS11; aceptación de WS13.1; código de catálogo/filtro (`workspace_routes.py`, `workspace-view.js`, `workspace.mjs`); reconciliación C-08; reglas comunes de `alcance.md`; corpus WS40 si se usa.
- **Cambios previstos:** nuevo explorador dentro del `output_scope`, rutas de lectura según WS11 y pruebas; sin tocar el store ni crear índices.
- **Dependencias:** WS11 debe producir la API/seguridad para no modelados; WS13.1 aporta la lectura; G_UI_READ se recibe por delta. Si falta el contrato, detenerse y registrar el hueco, sin sustituto.
- **Validaciones futuras:** abrir un modelado y un no modelado sin ID; alta en store temporal y en desk visible tras refresco explícito; sin reinicio ni cambio de código; sin índices nuevos.

FUTURO
- WS11 produce el contrato de navegación/identidad y la API/seguridad para no modelados.
- WS13.1 produce la lectura de documento/fuente.
- P01/receptor de graph_ui emite el acta G_UI_READ del delta.
- La promoción fija archivos, textos y escenarios en el TaskDoc.
- La aceptación del delta es una decisión humana; WS40 aporta corpus si aplica.
