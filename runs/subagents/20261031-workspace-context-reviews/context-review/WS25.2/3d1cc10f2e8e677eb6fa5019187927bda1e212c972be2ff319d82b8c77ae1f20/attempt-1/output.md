## REFORMULACION
- **Propósito**: permitir captura interna en graph_ui con destino elegido explícitamente por la persona: candidato de drawer o protoátomo, usando solo operaciones autorizadas por el contrato WS12 y sin exigir ni crear tarea.
- **Resultado**: cada captura persiste tras recargar en el destino elegido, conserva un origen tipado —ruta o mensaje— y no genera tarea implícita; ambos orígenes se registran y muestran tras recargar.
- **Repo**: graph_ui; salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.
- **Límites**: cada destino se prueba por separado; los permisos del contrato WS12 se aplican; G_HUMAN_READ habilita el uso de mutaciones en UI, pero no bloquea desarrollo ni pruebas aisladas de API con contratos/gates técnicos.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas previstas**: nodo WS25.2, agregado WS25, contrato vecino WS12, gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT, y fuentes brief/alcance/decisiones/cobertura.
- **Cambios previstos**: implementación de captura en `capture/`, endpoints ya autorizados por WS12 y pruebas en `tests/`; sin tocar otros nodos ni actas.
- **Dependencias**: WS12 como productor del contrato de operaciones; gates indicados como prerrequisitos de uso/aceptación por delta.
- **Validaciones futuras**: persistencia tras recarga para drawer y protoátomo por separado; origen ruta y origen mensaje registrados y visibles; ausencia de tarea implícita; permisos del contrato aplicados. Nada ejecutado.

## FUTURO
- WS12 debe publicar la whitelist/contrato técnico de operaciones, campos, actor, revisión, efectos y errores; si falta una operación, se registra el hueco y no se crea sustituto.
- WS16 produce el acta humana de lectura que habilita el uso de mutaciones en UI.
- El receptor P01 en graph_ui decide la aceptación por delta de G_UI_WRITE; el Executor de deskops solo registra el enlace.
- La promoción fijará archivos exactos, textos de pantalla, escenarios de prueba y preflight, dentro de esta aceptación.
