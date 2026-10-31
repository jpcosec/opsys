REFORMULACION
- **Propósito:** revisar WS39 como encargo de planificación: integrar inspección y edición de modelos existentes Schema/editar clases desde documento/contexto.
- **Resultado:** nodo de implementación en `graph_ui` que usa `draft/validate/promote` de sldb, con alcance en `shell/dialogs.js`, `views/models/`, `tests/` y acta humana en `runs/subagents/workspace-documental-acceptance/modelos/`.
- **Repo dueño:** `graph_ui`.
- **Límites:** no reimplementar modelos; no habilitar `promover` si falta API/autoridad; extensión posterior al lector básico; sujeto a WS12, WS16 y gates `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
- **Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS39 y contratos vecinos WS12/WS16 y gates. Sin herramientas ni ejecución.
- **Cambios previstos:** ninguno en esta revisión. Si se ejecutara, cambios solo dentro de `output_scope`, con pruebas y acta.
- **Dependencias:** contrato/whitelist de WS12 y aceptación del delta en `graph_ui`; `G_HUMAN_READ` producido por WS16. Si falta contrato, aplica la regla común: detenerse y registrar hueco.
- **Validaciones futuras:** UF09 sobre store temporal real; comprobar efectos/errores declarados por WS12; no habilitar promover sin API/autoridad; acta humana con participante fijado por P08; `G_HUMAN_MODEL` antes de publicar el capítulo 15 del manual de WS31.

FUTURO
- WS12 debe producir el contrato y aceptar el delta de escritura; WS16 debe producir `G_HUMAN_READ`.
- El solicitante/P08 debe fijar el participante humano; una persona real realiza la prueba y produce `G_HUMAN_MODEL`.
- WS31 publica el manual; la promoción y el TaskDoc siguen no autorizados.
