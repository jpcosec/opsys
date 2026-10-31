## REFORMULACION

**Propósito:** verificar si `sldb` ya permite extraer/validar y guardar un documento raw-source por API pública, con revisión y campos protegidos; si falta, implementarlo.  
**Resultado:** API y pruebas que demuestren guardado reversible, conflicto, recuperación tras fallo y preservación de campos/secciones; al cerrar, `G_SOURCE`.  
**Repo:** `sldb`; alcance de salida en `src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`.  
**Límites:** solo con `source_mode=editable`; no sobrescribir Markdown desde browser; no duplicar si la capacidad existe; depende de WS12 y sus gates.

## AMBIGUEDADES

ninguna. Los campos protegidos, el canal/API, los fallos parciales y la revisión quedan fijados por WS12/`G_WRITE_CONTRACT`; `source_mode` por P04/WS07; archivos y escenarios finos por el TaskDoc de promoción.

## DRY-RUN

**Lecturas previstas:** input y guía; nodo WS20, gates y arista WS12; `decisiones.md` (P04); `alcance.md`; `cobertura.md`; contrato/capacidades producidos por WS12; implementación y tests actuales de `sldb`; TaskDoc de promoción.  
**Cambios previstos:** ninguno durante esta revisión. En ejecución: verificar capacidad existente y, si falta, implementar en las rutas de `output_scope` con tests, sin editar Markdown desde browser ni duplicar código.  
**Dependencias:** WS12, `G_SLDB_WRITE`, `G_WRITE_CONTRACT`, `source_mode=editable`; `G_SOURCE` para cerrar.  
**Validaciones futuras:** API pública; roundtrip guardar-extraer; conflicto/revisión; recuperación tras fallo; campos protegidos; no duplicación. Sin ejecutar.

## FUTURO

P04/WS07 resuelve `source_mode`; WS12 produce contrato, capacidades y aceptación del delta en `sldb`; el TaskDoc de promoción fija archivos, pills y evidencias; el responsable de `sldb` acepta el alcance. Nada de ello se decide en este nodo.
