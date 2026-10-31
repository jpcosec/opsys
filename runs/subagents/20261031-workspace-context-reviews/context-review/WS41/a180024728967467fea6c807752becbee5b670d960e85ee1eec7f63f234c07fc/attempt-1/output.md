## REFORMULACION
**Propósito:** implementar en el workspace la lectura segura de un segundo desk, resolviendo solo aliases/roots autorizados por el contrato WS11 y usando APIs públicas de store, sin alterar el `SLDB_STORE` global ni realizar mutaciones cruzadas.

**Resultado:** un lector capaz de abrir dos stores del corpus WS40, mostrar identidad/origen, seguir enlaces authored entre desks y volver por la historia; con errores visibles ante alias no autorizado, path escapado o store ausente, y rechazo de roots arbitrarios.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`). Salidas previstas en `frontends/mindmap/source/`, rutas de lectura por store según WS11, `views/workspace/` y `tests/`.

**Límites:** no federar copiando contenido; no mutar el segundo desk; no cambiar el store global; no aceptar roots o paths fuera de lo autorizado; no promocionar todavía (`promotion: not_authorized`).

## AMBIGUEDADES
ninguna.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml` (WS41, WS13, WS11, WS40 y gate `G_UI_READ`), guía de revisión, brief, alcance, cobertura y decisiones. Sin ejecutar código ni consulter otras fuentes.
- **Cambios previstos:** capa de resolución de aliases/roots por request; rutas de lectura por store contra APIs públicas definidas por WS11; vistas de identidad/origen; integración con historia de WS13; tests de errores visibles y ausencia de mutación cruzada.
- **Dependencias:** WS13 agregado de lector/historia; WS11 contrato de navegación e identidad; WS40 corpus y manifiesto con dos desks; `G_UI_READ` pendiente, resuelto por WS11. Si falta contrato/API, rige la regla común: detenerse, registrar hueco y dejar la operación no disponible.
- **Validaciones futuras:** TaskDoc/preflight de promoción; aceptación técnica sobre los dos stores de WS40; verificación de error visible para alias no autorizado, path escapado y store ausente; confirmación de que no cambia `SLDB_STORE` ni hay mutaciones; lectura UF08 por WS16 con humano real.

## FUTURO
WS11 produce el contrato de aliases/roots, identidad y la aceptación `G_UI_READ`; WS40 produce el corpus, manifiesto y enlaces entre desks; WS13 aporta lector, foco e historia; WS16 ejecuta la validación humana de UF08. El humano debe resolver P01/P02/P07/P08/P09 y registrar P04; la promoción fijará archivos, pruebas y textos exactos dentro de esta aceptación.
