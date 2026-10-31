## REFORMULACION

**Propósito:** integrar en `graph_ui` la inspección y edición de modelos ya existentes, haciendo navegables Schema/editar clases desde documento/contexto y usando `draft/validate/promote` de `sldb`, sin reimplementar modelos.

**Resultado:** flujo UF09 de inspección y mutación sobre store temporal real, verificando efectos/errores del contrato WS12; acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`; `G_HUMAN_MODEL` antes de marcar disponible el capítulo 15 del manual de WS31.

**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/` y `output_scope` limitado a `shell/dialogs.js`, `views/models/`, `tests/` y `runs/subagents/workspace-documental-acceptance/modelos/`.

**Límites:** no reimplementar modelos; no habilitar promover si falta API/autoridad; depende de WS12 y WS16 y de los gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; promoción no autorizada.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS39, contratos vecinos WS12/WS16 y gates. No se revisan los bloques edge como nodos.

**Cambios previstos:** solo código/pruebas en `graph_ui` según `output_scope`, más el acta de aceptación en la ruta indicada. Ningún cambio en `deskops` ni en el plan.

**Dependencias:** contrato de operaciones de WS12; validación humana de lectura de WS16; gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; APIs `draft/validate/promote` de `sldb`; participante que fije P08; publicación/manual de WS31.

**Validaciones futuras:** UF09 en store temporal real; efectos y errores declarados por WS12; acta humana con participante y resultado; `G_HUMAN_MODEL` antes de disponibilidad en manual; preflight de promoción con archivos, pills, átomos y evidencia.

## FUTURO

WS12 produce la whitelist/capabilities y acepta el delta de `graph_ui`. WS16 produce el acta de lectura y `G_HUMAN_READ`. El humano fija el participante de P08 y aprueba `G_HUMAN_MODEL`. WS31 publica el capítulo 15 solo tras ese gate. La autorización de promoción corresponde a un humano; este nodo no la ejecuta.
