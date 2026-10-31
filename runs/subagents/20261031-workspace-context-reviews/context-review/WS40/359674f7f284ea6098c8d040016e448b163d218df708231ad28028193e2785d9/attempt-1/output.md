## REFORMULACION
Propósito: encargar un generador reproducible del corpus del desk Taller para pruebas de lectura. Resultado: generador versionado en `graph_ui` que crea un entorno aislado con dos repos/stores, documentos (Markdown no modelado, Code local, referencia rota), instrucciones de arranque y entrada mínima; devuelve un manifiesto. Repo dueño: `graph_ui`; `output_scope`: `tests/fixtures/workspace_documental/`, script de seed y `tests/`. Límites: usar contratos/CLI reales, no servidor fake; no tocar desk real; corpus único para WS16/30; WS17 solo aporta contenido authored.

## AMBIGUEDADES
1. «Aceptar opcionalmente plantillas de navegación WS17.» WS17 depende de WS40 y produce `ejemplo/nav/`. El ejecutor debe inventar si WS40 espera plantillas inexistentes, las ignora o se bloquea; contradice el orden prerrequisito→dependiente.
2. «registra datos/commits/roots». No se define si son commits Git reales en los repos temporales (identidad, mensajes) o metadatos del manifiesto; obliga a inventar el criterio de aceptación.
3. «los paths se devuelven como manifiesto». Falta formato, campos y destino del manifiesto; el ejecutor debe inventar su esquema para que sea comprobable.
4. «entrada mínima ecosistema/proyecto con enlaces al Board/FAQ/conocimiento reales creados». «Reales» puede significar artefactos del corpus temporal o del deskops real; junto con «nunca toca desk real», obliga a decidir el alcance de esos enlaces.

## DRY-RUN
Lecturas previstas: contrato WS11, user-flows WS08, `dag.yaml` y guía. Cambios previstos: script de seed, fixtures bajo `output_scope`, tests, README/instrucciones y manifiesto. Dependencias: WS11/WS08; `G_UI_READ` pendiente, resuelto por WS11. Validaciones futuras: comando que recrea entorno aislado sin tocar desk real, manifiesto de paths, prueba humana WS16, integración WS17/WS30. Sin ejecución.

## FUTURO
`G_UI_READ` lo acepta WS11 con responsable `graph_ui` designado en WS07; la promoción requiere autorización y preflight de tarea; WS16 ejecuta la validación humana; WS17 aporta plantillas authored después de WS40; WS30 integra índices. Nada de esto se decide aquí.
