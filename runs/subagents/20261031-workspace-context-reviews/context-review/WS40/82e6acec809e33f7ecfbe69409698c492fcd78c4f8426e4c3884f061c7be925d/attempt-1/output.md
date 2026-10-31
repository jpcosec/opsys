## REFORMULACION

**Propósito:** versionar en `graph_ui` un generador reproducible del corpus Taller que use el contrato WS11 y los CLI reales de deskops/sldb, sin servidor fake.

**Resultado:** un comando que crea/recrea un entorno aislado con dos repos temporales con desk y un tercero sin desk, stores, documentos Markdown modelados y no modelados, Code local, referencia rota, enlaces authored entre desks, entrada mínima y README de arranque; con commits Git reales y manifiesto JSON.

**Repo:** `graph_ui`; output_scope `tests/fixtures/workspace_documental/`, script de seed y `tests/`.

**Límites:** no toca el desk real; no produce contenido authored de WS17, que solo aporta plantillas opcionales; WS40 cierra sin ellas. Es productor único de corpus para WS16/30.

## AMBIGUEDADES

1. «hace commits git reales en los repos temporales»: no fija identidad, rama ni mensaje de commit; obligaría a inventar configuración Git y política de commits.
2. «imprime un manifiesto JSON con roots, stores, commits y documentos clave»: no enumera qué documentos son «clave»; obligaría a elegir el conjunto exacto del manifiesto.
3. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)» frente a «output_scope: tests/fixtures/workspace_documental/»: no aclara si se versiona el generador, una copia fixture o ambos; obligaría a decidir qué es artefacto y qué es efímero.
4. «Entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal»: no define si el Board se crea mediante CLI ni qué tareas contiene; obligaría a inventar su contenido.

## DRY-RUN

- **Lecturas:** nodo WS40, guía, brief, alcance, decisiones, cobertura; contratos vecinos WS11/WS08 como dependencias, WS16/WS17/WS41 como consumidores.
- **Cambios previstos:** script generador, fixtures y pruebas en `graph_ui`.
- **Dependencias:** contrato WS11; user-flows WS08; `G_UI_READ` pendiente; CLI deskops/sldb verificados en WS02/WS03, transitivos vía WS11; plantillas WS17 opcionales.
- **Validaciones futuras:** ejecutar el comando, comprobar aislamiento y commits, verificar manifiesto, confirmar que no toca desk real; consumo por WS16 y WS30.

Sin ejecución.

## FUTURO

- WS17 aportará plantillas authored y regenerará el corpus.
- WS16 consumirá el manifiesto para validación humana.
- WS30 integrará índices.
- El responsable de `graph_ui` designado en WS07/WS11 deberá aceptar el delta de lectura que representa `G_UI_READ`.
- La promoción fijará archivos, escenarios y textos mediante TaskDoc.
