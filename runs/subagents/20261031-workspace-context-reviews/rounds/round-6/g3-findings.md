### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08»: el `depends_on` de WS30 no incluye WS08 ni se aporta su guion. Obliga a inventar esos escenarios o a asumir que WS08 estará disponible sin dependencia declarada.
2. «abre tarea en el nodo que lo causó»: no hay criterio para atribuir un fallo a un nodo cuando afecta a varios o su causa no es inequívoca. Obliga a inventar la atribución y el destino de la tarea.

### WS42 [2]
1. «con confirmación de la persona usuaria en la UI, que ve el alcance y la procedencia antes de ejecutar». No se define qué compone “alcance” ni de dónde sale “procedencia”; el ejecutor tendría que inventar campos, fuente y criterio de presentación, y la aceptación quedaría no comprobable.
2. «las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea». No se identifica dónde está registrado ese modelo ni qué reglas determinan que una materialización sea válida o inválida; obligaría a inventar registro, versión y criterios de validación.

### WS43 [2]
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» — no define qué hacer si un repo de `deskops list repositories` carece de entrada existente: omitirlo, bloquear la publicación o abrir tarea. Obliga a inventar el resultado para ese repo.
2. «los acuerdos durables aplicados al mapa (Pxx aceptadas y contratos aplicables)» — «contratos aplicables» no fija criterio ni lista; obliga a inventar si comprende solo `navegacion.md`, también `operaciones.md` u otros de `contratos/`.
