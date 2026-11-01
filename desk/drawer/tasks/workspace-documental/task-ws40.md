---
id: WS40
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS11
- WS08
requires:
- G_UI_READ
---

# Crear generador reproducible del corpus Taller

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

tests/fixtures/workspace_documental/; script de seed; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Versionar un generador en graph_ui que usa el contrato WS11 y los CLI reales de deskops/sldb verificados en WS02/WS03, no servidor fake. Crear dos repos temporales bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas), sus stores y documentos, incluyendo Markdown no modelado, Code local y referencia rota. Parámetro opcional con la ruta de plantillas WS17: WS40 cierra sin ellas, y WS17 regenera con ellas después. Generar instrucciones de instalación/arranque del ejemplo y entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal, su FAQ Markdown y documentos de conocimiento, todos creados dentro del corpus temporal, para que WS16 pruebe una entrada sin esperar índices ricos WS17. Incluir un tercer repo temporal sin desk para UF10 y enlaces authored entre los dos desks con desk para UF08.

## Aceptación

Un comando crea/recrea entorno aislado, hace commits git reales en los repos temporales y nunca toca desk real; imprime un manifiesto JSON con roots, stores, commits y documentos clave. Es productor único de corpus para WS16/30; WS17 solo aporta contenido authored. Entrada mínima y README de arranque reproducibles, manifiesto de ubicación y segundo desk; WS17 enriquece navegación posteriormente.

## Dependencias

Tareas: WS11, WS08. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS40/c26ae332102d9f90b79ef4022bfdafcc064027dbfc9ee7b89a2210e370190cce/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
