REFORMULACION
Propósito: encargar en graph_ui una vista read-only de diff Git e historial junto a una TaskDoc. Resultado: secciones por repo alcanzado por `TaskDoc.files`, con diff real e historial acotado a `TaskDoc.references`/`TaskDoc.files`, o working tree→HEAD si no hay commits, mostrando repo root explícito. Repo: graph_ui, salida `frontends/mindmap/views/workspace/diff/` y `tests/`; rutas de lectura según WS11. Límites: no escribir/revertir; no mostrar integridad del store (WS29); asociación a intento en WS35; ruta/repo no resoluble queda no disponible; depende WS13/WS12 y `G_UI_READ` per-delta.

AMBIGUEDADES
1. «ordenados por fecha de commit» no fija ascendente ni descendente; obligaría a inventar el orden visible del historial.
2. «sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD» solo cubre cero commits; si hay commits resolubles pero ninguno toca `TaskDoc.files` —o `files` está vacío—, no define si se muestra historial vacío, se cae a working tree o se advierte; obligaría a inventar el resultado.
3. «commits de TaskDoc.references resolubles» no define qué hacer con referencias no resolubles (omitir, advertir o bloquear la sección); obligaría a inventar su tratamiento.

DRY-RUN
Lecturas previstas: contrato WS11 (repo/rutas), contrato WS12 (campos/lectura TaskDoc), piezas de WS13 y recibo `G_UI_READ`. Cambios previstos: vista diff/historial y pruebas en graph_ui. Dependencias: WS13/WS12 y, transitivas, WS11. Validaciones futuras: prueba con repo Git temporal/TaskDoc fixture, diff acotado a `files`, una sección por repo, sin escrituras, y verificación del recibo `G_UI_READ`.

FUTURO
WS35 añade asociación a intento; WS29 cubre integridad del store; WS11/WS12 producen contratos; el receptor P01 emite acta `G_UI_READ` por delta; la promoción/TaskDoc fija archivos, textos y pruebas.
