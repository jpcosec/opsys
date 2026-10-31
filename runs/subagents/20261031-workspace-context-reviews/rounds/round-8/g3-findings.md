### WS28 [1]
1. **“endpoints” sin delimitar frente a “No commit/close desde HTTP en baseline”.**  
   Cita: `output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/` y `No commit/close desde HTTP en baseline.`  
   Obliga a inventar qué endpoints puede producir WS28: si son solo de verificación/diagnóstico o si se espera exponer alguna operación de cierre. El alcance prohíbe cerrar por HTTP, pero no define el conjunto permitido.

### WS30 [2]
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no está en `depends_on` ni se aporta su guion. Obligaría a inventar la lista de escenarios, el criterio de conflicto/teclado y sus condiciones de paso, o suponer que `validacion-humana.md` los define, aunque solo menciona conflicto y gates.
2. «el responsable del repo dueño abre tarea en el nodo que lo causó». No aclara si el responsable es `graph_ui` (dueño de WS30) o el `owner_repo` del nodo causante, ni cómo atribuir fallos de corpus/entorno (WS17/WS40). Obligaría a inventar actor y criterio de atribución.

### WS31 [1]
1. **Base de rutas de los insumos.** Cita: «incorporar el índice de borradores/manual.md» y «cada contrato en contratos/». El nodo no fija si `borradores/manual.md` y `contratos/` se resuelven desde el paquete de plan, desde `deskops:repository_root/` o desde otro repo. Obligaría a inventar la ruta base para localizar el índice y los contratos de WS11/WS12, pese a que sus productores sí están nombrados.

### WS42 [4]
1. «validan contra el modelo SLDB registrado en el store de la tarea» — no se identifica qué store («de la tarea» no coincide con «store temporal real»/«corpus WS40» de alcance.md) ni qué registro del modelo. Obliga a inventar la fuente de validación.
2. «una materialización que no valida se muestra como inválida» — no hay criterio de validación definido en las fuentes; el ejecutor tendría que inventar reglas y umbrales.
3. «bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad» — no existe mapa capability→escenario UF03 en las fuentes suministradas; obliga a inventar la correspondencia.
4. «ve el origen y el efecto de la operación antes de ejecutar» — «efecto» no se define (¿diff, lista de cambios, recuento?); obliga a inventar el contenido de la confirmación.

### WS43 [3]
1. «Repos a enlazar = todos los de `deskops list repositories`» frente a «el mapa publicado corresponde a las entradas/índices validados en Taller». Taller/WS40 solo materializa dos desks; no se define cómo representar repos listados sin entrada validada. Obliga a inventar si se omiten, se enlazan sin validar o se replica el ejemplo.
2. «Enlazar repos conocidos por identidad/origen y su entrada existente» no cubre repos sin entrada existente; junto con «Escribir una entrada dentro de otro repo requiere su tarea y acuerdo de alcance», no se sabe si quedan fuera del mapa, se enlazan a su root o se bloquea. Obliga a inventar el criterio.
3. «commit por `deskops closeout commit`» usa un canal de cierre, pero `requires` no incluye G_CLOSEOUT, que cobertura.md asocia a commits de promoción/cierre. No se sabe si el commit de publicación queda autorizado solo con G_WRITE_CONTRACT o requiere ese gate. Obliga a decidir commit o bloqueo.
