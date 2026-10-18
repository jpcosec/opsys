# TaskDoc unknown frontmatter keys

Pre-scan for task-rw-f6-taskdoc-contract-cleanup, run on 2026-10-18.

Discovery rule: `.sldb` directories under `$HOME` with `core/models/TaskDoc.yaml`, excluding whole path segments `.tmp`, `.venv`, `node_modules`, `tools`, `tmp`, and only inside a git work tree.

Stores found: 46. TaskDoc files scanned: 447.

Files below have top-level frontmatter keys outside `TaskDoc.model_fields`; `extra: ignore` drops those keys, so they are exempt from the byte-identical render check and belong to task-rw-f6-migrate-tracking-stores.

| Store | TaskDoc | Unknown keys |
| --- | --- | --- |
| `/home/jp/.cache/uv/git-v0/checkouts/cb8fbf0ea9a76f52/62e7603/.sldb` | `desk/tasks/task-write-end-to-end-deskops-operator-manual.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cb8fbf0ea9a76f52/ad30fa5/.sldb` | `desk/tasks/task-write-end-to-end-deskops-operator-manual.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9bcef63/.sldb` | `desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9bcef63/.sldb` | `desk/tasks/task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9bcef63/.sldb` | `desk/tasks/task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9bcef63/.sldb` | `desk/tasks/task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9dca856/.sldb` | `desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9dca856/.sldb` | `desk/tasks/task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9dca856/.sldb` | `desk/tasks/task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/9dca856/.sldb` | `desk/tasks/task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-define-sldb-addressability-model.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-definir-arquitectura-objetivo-modular-de-sldb.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-design-sldb-ast-query-primitives.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-dise-ar-estrategia-de-extracci-n-y-modularizaci-n.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-ejecutar-refactor-base-del-n-cleo-sldb.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-expand-sldb-composition-modes.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-mapear-arquitectura-real-de-sldb.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-retirar-modulos-sueltos-sin-importadores.md` | `checklists, routine` |
| `/home/jp/.cache/uv/git-v0/checkouts/cc76a327e48ac903/d877dad/.sldb` | `desk/tasks/task-tighten-semantic-export-provenance-contract.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-agentes-y-pipeline-desde-la-kb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-alarmas-runbook-y-rollback.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-backup-y-restore-de-las-tres-bases.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-base-para-produccion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-borrar-scripts-de-migracion-del-formato-viejo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-ci-mas-rapido.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-cliente-gian.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-el-kit-usa-la-consulta-de-uso-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-el-kit-vuelve-a-transcribir-notas-de-voz.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-endurecer-lint-de-las-pruebas-del-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-enganche-antes-y-despues-del-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-estado-de-twilio-por-mensaje.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-etiqueta-solo-en-rasgos-categoricos.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-evals-antes-de-publicar.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-features-de-gian.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-gateway-para-produccion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-identidad-del-store-desde-store-manifest-de-sldb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-kit-de-pruebas-compartido.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-la-cadena-como-etapas-de-turn.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-limpiar-referencias-a-tokens-viejos-de-ci.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-mensajes-a-la-persona-desde-la-configuracion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-modelos-nova-del-panel-en-us-east-2.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-nombre-por-plantilla.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-nombres-de-runtimes-legados-en-pruebas-del-kit.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-oraculo-propio-sin-el-legado.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-orden-entre-replicas-de-s5.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-paquetes-de-entidades.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-plantilla-de-satelite.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-postgres-efimero-sin-unshare-en-ops.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-pr-26-modo-basic-portado-a-dev.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-pr-45-pyme-roles-y-panel.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-pr-6-modo-basic-tipo-build-my-agent.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-prueba-con-llm-real.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-prueba-manual-de-entidades-y-perfil-en-dev.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-pruebas-de-cada-paquete-corren-solas.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-publicada-vs-borrador-en-las-conexiones.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-pyme-como-satelite.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-rasgos-categoricos-y-segmento-desde-la-kb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-releases-por-digest.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-revisar-y-traer-fix-selfix-private-validation.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-s5-con-dos-replicas-y-orden-por-persona.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-secreto-llm-gateway-token-en-dev.md` | `checklists, closeout_evidence_verified, pill_graduation_verified, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-segmento-desde-la-categoria-del-catalogo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-segundo-cliente-sobre-la-plantilla.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-spec-21-entidades-como-paquetes.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-spec-22-enganche-de-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-alta-en-el-panel-y-webhook.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-completo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-media.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-resiliencia-y-replay.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-texto-en-dev.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-tope-y-perfil-por-subcuenta.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-traer-la-spec-1-1-de-operabilidad.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-trazas-a-cloudwatch-sin-pii.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/Chatbot_Infra/.sldb` | `desk/tasks/task-vistas-generadas-por-entidad.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/ChatbotsKnowledgeBases/.sldb` | `desk/tasks/task-triaje-de-ramas-de-la-kb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-dosis-y-fecha-de-aplicacion-como-paquete-de-entidades.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-dpa-y-retencion-de-datos-de-salud.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-imagen-de-psp-desde-el-satelite.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-psp-en-produccion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-revisar-y-traer-politicas-de-seguridad.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-seguridad-clinica.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-tabla-de-casos-clinicos.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/psp_chatbot/.sldb` | `desk/tasks/task-whatsapp-aprobado-por-meta.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-catalogo-de-openai-y-openrouter.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-ci-propio-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-lector-de-uso-en-el-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-linea-base-de-lint-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-notas-de-voz.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-tope-por-tipo-y-pedidos-bloqueados.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/chatbot/shared_llm-gateway/.sldb` | `desk/tasks/task-workflow-check-obligatorio-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-alarmas-runbook-y-rollback.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-backup-y-restore-de-las-tres-bases.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-base-para-produccion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-borrar-scripts-de-migracion-del-formato-viejo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-ci-mas-rapido.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-el-kit-usa-la-consulta-de-uso-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-el-kit-vuelve-a-transcribir-notas-de-voz.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-endurecer-lint-de-las-pruebas-del-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-enganche-antes-y-despues-del-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-estado-de-twilio-por-mensaje.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-etiqueta-solo-en-rasgos-categoricos.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-identidad-del-store-desde-store-manifest-de-sldb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-kit-de-pruebas-compartido.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-limpiar-referencias-a-tokens-viejos-de-ci.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-mensajes-a-la-persona-desde-la-configuracion.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-modelos-nova-del-panel-en-us-east-2.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-nombre-por-plantilla.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-nombres-de-runtimes-legados-en-pruebas-del-kit.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-oraculo-propio-sin-el-legado.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-orden-entre-replicas-de-s5.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-paquetes-de-entidades.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-plantilla-de-satelite.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-postgres-efimero-sin-unshare-en-ops.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-prueba-con-llm-real.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-prueba-manual-de-entidades-y-perfil-en-dev.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-pruebas-de-cada-paquete-corren-solas.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-rasgos-categoricos-y-segmento-desde-la-kb.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-revisar-y-traer-fix-selfix-private-validation.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-s5-con-dos-replicas-y-orden-por-persona.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-secreto-llm-gateway-token-en-dev.md` | `checklists, closeout_evidence_verified, pill_graduation_verified, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-segmento-desde-la-categoria-del-catalogo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-spec-21-entidades-como-paquetes.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-spec-22-enganche-de-turno.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-alta-en-el-panel-y-webhook.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-completo.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-media.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-resiliencia-y-replay.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-telegram-texto-en-dev.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-traer-la-spec-1-1-de-operabilidad.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/Chatbot_Infra/.sldb` | `desk/tasks/task-vistas-generadas-por-entidad.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-catalogo-de-openai-y-openrouter.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-ci-propio-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-lector-de-uso-en-el-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-linea-base-de-lint-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-notas-de-voz.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-tope-por-tipo-y-pedidos-bloqueados.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/grifo/shared_llm-gateway/.sldb` | `desk/tasks/task-workflow-check-obligatorio-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-catalogo-de-openai-y-openrouter.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-ci-propio-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-lector-de-uso-en-el-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-linea-base-de-lint-del-gateway.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-logs-de-llm-gateway-servir-sin-pii.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-notas-de-voz.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-tope-por-tipo-y-pedidos-bloqueados.md` | `checklists, routine` |
| `/home/jp/AntonIA/repos/mepu/mepu_ocs_dev/shared/llm-gateway/.sldb` | `desk/tasks/task-workflow-check-obligatorio-del-gateway.md` | `checklists, routine` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/001-define-graph-ui-data-contract.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/002-define-minimal-editing-surface.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/003-create-real-graph-fixture.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/004-wire-reusable-editor-to-real-fixture.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/005-surface-semantic-signals.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.claude/worktrees/agent-ad84526feda033646/.sldb` | `desk/tasks/006-prove-one-safe-edit-flow.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/001-define-graph-ui-data-contract.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/002-define-minimal-editing-surface.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/003-create-real-graph-fixture.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/004-wire-reusable-editor-to-real-fixture.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/005-surface-semantic-signals.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/UIs/graph_ui/.sldb` | `desk/tasks/006-prove-one-safe-edit-flow.md` | `created, domain, priority` |
| `/home/jp/proyectos/SLDB_1/sldb/.sldb` | `desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md` | `checklists, routine` |
| `/home/jp/proyectos/SLDB_1/sldb/.sldb` | `desk/tasks/task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges.md` | `checklists, routine` |
| `/home/jp/proyectos/SLDB_1/sldb/.sldb` | `desk/tasks/task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion.md` | `checklists, routine` |
| `/home/jp/proyectos/SLDB_1/sldb/.sldb` | `desk/tasks/task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-alinear-repositorios-y-dependencias-base.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-auditar-y-factorizar-los-atoms-existentes-de-la-kb.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-borrar-runtime-legacy-y-reubicar-knowledge-tools-y-source.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-definir-contratos-de-la-oficina-multiagente.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-agente-bibliotecario.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-agente-decisor-y-guardas-de-riesgo.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-agente-estratega-y-propuesta-de-reglas.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-catalogo-de-tools-estadisticas.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-coordinador-determinista-de-la-oficina.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-datasets-autonomos-y-medibles.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-la-oficina-multiagente-sobre-knowledge.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-ledger-runtime-auditable.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-protoagente-materializado-desde-knowledge.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-recuperacion-y-mantenimiento-de-knowledge.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-reglas-y-backtesting-reproducible.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-implementar-ui-auditable-de-la-oficina.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-integrar-la-oficina-y-retirar-el-runtime-heredado.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-modelar-la-biblioteca-operacional-en-sldb.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-refactorizar-el-codigo-de-tools-para-el-runtime-nuevo.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-revisar-y-delimitar-el-runtime-trader-heredado.md` | `checklists, routine` |
| `/home/jp/proyectos/TraderBot/.sldb` | `desk/tasks/task-separar-las-proyecciones-kgdb-de-knowledge-y-deskops.md` | `checklists, closeout_evidence_verified, pill_graduation_verified, routine` |
| `/home/jp/proyectos/legacy/hum-ecosystem/core/code2specyaml/.sldb` | `desk/tasks/task-07-verification-matrix-and-evidence-rules.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/hum-ecosystem/core/code2specyaml/.sldb` | `desk/tasks/task-08-optional-sldb-reconciliation-boundary.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/001-define-audit-io-contract.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/002-define-finding-model.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/003-create-audit-fixture.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/004-implement-orphan-and-redundancy-audits.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/005-emit-machine-readable-findings.md` | `created, domain, priority` |
| `/home/jp/proyectos/legacy/ontology/.sldb` | `desk/tasks/006-prove-consumption-path.md` | `created, domain, priority` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-adopt-real-classification-mapping-from-ods.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-build-minimal-canonical-catalog-fixture.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-build-minimal-category-item-fixture.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-build-minimal-profile-rule-fixture.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-canonicalize-legacy-catalog-into-humble-ready-master-data.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-compose-cotizador-ui-topology-with-humble-views-and-units.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-define-canonical-profile-and-rule-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-define-initialization-profile-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-define-pricing-profile-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-define-rule-definition-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-cotizadorservice-command-catalog.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-cotizadorservice-command-query-catalog.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-cotizadorservice-query-catalog.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-line-override-patch-semantics.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-quote-line-snapshot-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-quote-snapshot-and-line-patch-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-quote-snapshot-header-and-summary-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-service-error-code-taxonomy.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-service-result-and-error-taxonomy.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-freeze-service-success-failure-envelope.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-implement-quotation-domain-engine-on-humble-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-integrate-humble-boundaries-for-local-and-gas-execution.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-map-category-ownership-from-raw-sources.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-map-item-offer-contract-from-raw-sources.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-map-raw-reference-data-to-canonical-category-item-ownership.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-app-signal-payload-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-app-signals-operations-and-transition-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-boundary-serialization-and-versioning-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-catalog-repository-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-command-orchestration-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-cotizadorservice-orchestration-and-snapshot-assembly.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-effective-property-resolution-flow.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-gas-adapter-normalization-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-line-evaluation-pipeline-and-recompute-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-line-pricing-and-line-ruling-outputs.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-lineacotizada-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-local-adapter-normalization-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-local-gas-adapter-normalization-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-local-gas-equivalence-validation-matrix.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-operation-to-service-call-mapping.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-persistence-timing-and-cross-environment-validation.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-persistence-trigger-policy.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-query-orchestration-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quotationstate-aggregate-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quotationstate-and-lineacotizada-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quote-aggregation-and-quote-level-ruling.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quote-and-catalog-repository-contracts.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quote-lifecycle-and-transition-guards.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-quote-repository-contract.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-recompute-propagation-policy.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-rendermodel-and-unit-local-state-boundaries.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-save-vs-finalize-lifecycle-guards.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-snapshot-assembly-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-store-slices-and-write-ownership.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-specify-workflow-stage-transition-rules.md` | `checklists, routine` |
| `/home/jp/proyectos/office/humble/Cotizador/.sldb` | `desk/tasks/task-split-store-snapshot-and-rendermodel-boundaries.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-blockmatrix-desde-el-logicalsystem-ensamblar-el-hipertensor.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-e-r-y-d-i-como-criterio-de-particion-no-como-numero-muerto.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-guardas-de-forma-detectar-w-degenerados-tipo-relacion-universal.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-orden-acyclidad-y-secuencia-lineal-dentro-de-w.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-proyeccion-objeto-sujeto-encadenar-por-termino-medio.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-proyeccion-wigame-y-matrices-a-s-expressions.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/Matrix/.sldb` | `desk/tasks/task-relaciones-axiomas-de-orden-en-relationalgebra.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-add-editorial-validation-language-and-interruption-cues-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-add-editorial-validation-language-and-interruption-cues-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-add-editorial-validation-language-and-interruption-cues-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-add-editorial-validation-language-and-interruption-cues.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-derive-editorial-trace-status-in-graph-payload-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-derive-editorial-trace-status-in-graph-payload-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-derive-editorial-trace-status-in-graph-payload-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-derive-editorial-trace-status-in-graph-payload.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-editorial-browser-shift-from-node-editor-to-argument-trace-ui-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-editorial-browser-shift-from-node-editor-to-argument-trace-ui-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-editorial-browser-shift-from-node-editor-to-argument-trace-ui-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-editorial-browser-shift-from-node-editor-to-argument-trace-ui.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-enforce-paragraph-to-note-to-source-trace-navigation-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-enforce-paragraph-to-note-to-source-trace-navigation-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-enforce-paragraph-to-note-to-source-trace-navigation-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-enforce-paragraph-to-note-to-source-trace-navigation.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-make-the-paragraph-column-an-assertion-surface-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-make-the-paragraph-column-an-assertion-surface-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-make-the-paragraph-column-an-assertion-surface-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-make-the-paragraph-column-an-assertion-surface.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-rebuild-manuscript-pane-as-trace-first-reading-surface-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-rebuild-manuscript-pane-as-trace-first-reading-surface-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-rebuild-manuscript-pane-as-trace-first-reading-surface-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-rebuild-manuscript-pane-as-trace-first-reading-surface.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-notes-as-warrant-and-reasoning-check.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-notes-as-warrant-and-reasoning-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-notes-as-warrant-and-reasoning-test.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-notes-as-warrant-and-reasoning.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-sources-as-evidence-cards-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-sources-as-evidence-cards-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-sources-as-evidence-cards-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-reframe-sources-as-evidence-cards.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-turn-the-sections-column-into-editorial-context-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-turn-the-sections-column-into-editorial-context-readiness-check.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-turn-the-sections-column-into-editorial-context-test.md` | `checklists, resolver_role, subtasks` |
| `/home/jp/proyectos/wittgenstein/Matrix/paper_v2/.sldb` | `desk/tasks/task-paper-v2-turn-the-sections-column-into-editorial-context.md` | `checklists, resolver_role, routine, subtasks` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-canonicalhypertensor-jax-vram-allocation.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-canonicalhypertensor-jit-bitwise-operations.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-implementar-atomfeeder.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-implementar-logicalspace-registry-bi-direccional.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-meelengine-core-api-facade.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-meelengine-fixpoint-deduction-algorithm.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-rulematrixcompiler-si-mask-encoding.md` | `checklists, routine` |
| `/home/jp/proyectos/wittgenstein/matrix-shrdlu-spec/matrix/.sldb` | `desk/tasks/task-rulematrixcompiler-sop-reduction.md` | `checklists, routine` |
| `/home/jp/setup/.sldb` | `desk/tasks/task-centralizar-configuraciones-personales-en-setup.md` | `checklists, routine` |

Unknown-key files: 306.

## Unreadable tracked TaskDocs

These document entries point at files that no longer exist; they have no frontmatter to scan.

| Store | TaskDoc |
| --- | --- |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-013-product-search-contract.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-014-product-extraction-mission.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-017-search-result-normalization.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-018-query-input-pagination.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-019-mission-completion-rules.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-020-block-detection-observe.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-021-hitl-operator-resume-flow.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-022-passive-bootstrap-blocked-portals.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-023-extraction-persistence-products.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-024-comparison-ready-export.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-025-portal-viability-registry.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-026-cli-product-runs.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-028-blocked-portal-recovery-test.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-029-operator-playbook.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-030-end-to-end-smoke-run.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-032-browseros-user-like-hardening.md` |
| `/home/jp/proyectos/legacy/hum-scrapper/.sldb` | `desk/tasks/task-033-visual-hint-rescue-primitives.md` |
