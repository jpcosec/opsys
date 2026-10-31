# Revisión independiente: workspace documental de Deskops

**Veredicto corto:** sirve como paquete de intención, pero no como plan ejecutable. La distinción conceptual es buena. Le faltan decisiones de producto y de autoridad, varias aristas están mal y ya compite con otros dos planes vivos.

Marco cada hallazgo con **[V]** (verificado en código o archivos) o **[I]** (inferencia mía).

**Límites de esta revisión:**
- No tengo la "conversación" que citan el README y A2.
- No ejecuté la UI ni revisé el código de Kimun.
- No comprobé si SLDB soporta editar fuente Markdown cruda.
- Dos de mis fuentes están fuera del paquete: tu plan en `~/.claude/plans/1-si-hay-que-logical-lovelace.md` y la memoria del proyecto. Un ejecutor con contexto cero no las vería, y eso ya es un defecto.

## 1. Qué se pretende construir y qué NO está decidido

**Pretende:** un "IDE para el desk" donde una persona entiende y opera un proyecto a través de sus documentos Markdown. Incluye explorador, pestañas y divisiones, búsqueda y panel contextual. Una misma fuente tiene varias representaciones y las acciones pasan por sus autoridades reales: Deskops para workflow, infraestructura documental para lectura y escritura. Debe funcionar completo sin agentes; Scion es un ramal opcional.

**No está decidido:**
- Si la unidad es el documento o el nodo (ver H1).
- En qué UI se construye y qué pasa con la actual.
- Si Kimun entra o no.
- Qué se puede editar como fuente cruda.
- Si el cierre ocurre en la UI.
- Cómo se relacionan las escrituras con git.
- Cómo conviven el humano y el coordinador.
- Cómo se resuelve la navegación entre desks.
- Qué latencia es aceptable.

## 2. Ambigüedades que obligarían a inventar

| # | Dónde | Hallazgo | Consecuencia |
|---|---|---|---|
| H1 | `README` §Reutilización, D1 | [V] D1 "refina" `task-workspace-multiproyeccion…`, pero esa tarea define `/workspace/node` con pestañas Document/Graph/Code de un nodo. No trae explorador, documentos en pestañas ni divisiones. El átomo de graph_ui también habla de "same node". | Son dos productos distintos. Reusar la tarea desvía el modelo mental. |
| H2 | `vision.md` §Unidad, D2, B3 | [V] Se pide edición de fuente Markdown y a la vez "nada de editar status". `status` y `current_node` viven en el frontmatter del mismo archivo, y la UI actual bloquea justo eso. No hay política de escritura por modelo o campo. | Un editor de fuente evade los gates, o el "editar fuente" real queda sin definir. |
| H3 | `D4`, `UF05`, `vision` §Criterios | [V] D4 incluye cierre. `docs/deskops-ui.md` dice que la UI no cierra, no hace commits y no crea tareas, y tu plan vigente mantiene `closeout *` fuera de la UI. La visión promete no conocer comandos internos. | UF05 no se sabe si termina en la UI o en la terminal. G1 no se puede evaluar. |
| H4 | Todo el paquete | [V] Ningún documento trata commit, historial o deshacer. `AGENTS.md` exige commitear la creación en drawer antes de promover y la promoción antes de implementar. | Tras "guardar" o "promover", nadie sabe si la UI commitea. Una promoción desde la UI podría violar el ritual. |
| H5 | `SPEC.md` §1.3 frente a D2/D4 | [V] El coordinador es "único escritor de `desk/`" y `deskops-ui.md` admite que no hay lock compartido con escritores CLI. B3 solo dice "revisión optimista". | Con un coordinador activo, editar desde la UI viola esa regla o choca con él. Lo mismo vale para el ramal "sin agentes" sobre un desk con coordinador. |
| H6 | `README` L7, D2/F1 | [V] Kimun se trata como "ruta de migración" con prerrequisitos condicionales, y ningún nodo decide adoptarla. Tu memoria registra lo contrario: Kimun es solo referencia, nunca respuesta a decisiones de sldb. | El plan hereda de `SPEC.md` una dirección que no consta aprobada. |
| H7 | `dag.yaml` D2/F1 | [V] "verificar M1/M2/C2" usa IDs de Kimun, pero C2 también es nodo de este DAG. | Colisión directa de identificadores. |
| H8 | `vision`, `vistas` | [V] "Vista", "representación", "renderización" y "proyección" se usan sin definir. "Selección" significa foco del usuario y también resultado de consulta. A2 exige vocabulario y el borrador no lo trae. | Justo la confusión que el encargo quería evitar. |
| H9 | `vistas`, B2 | [V] `ViewDoc` solo cubre `nodes`, `relations`, `direction` y `layout`, y solo se evalúa como grafo. No encontré modelo de consulta guardada (búsqueda acotada a nombres de clase en sldb, deskops y spec2viz). | Board como tablero, "consultas guardadas" y "composiciones" no tienen contrato hoy. |
| H10 | Dueños en `dag.yaml` | [I] "infraestructura" y "repos dueños" no nombran a nadie. La tarea de edición dice `pron.Store/sldb`. | Nadie decide. El README dice que las decisiones van "al dueño" sin nombrarlo. |
| H11 | G1, A2, D1 | [V] "latencia" no tiene umbral y A2 se contrasta con "esta conversación", que no existe para un ejecutor. "Sin inventario hardcodeado" choca literalmente con `VIEWS` en `shell/registry.js`. | Aceptaciones no evaluables. |
| H12 | `README` L3 | [I] "La UI anterior es un experimento técnico" no dice cuál. `/workflow/deskops` está entregada y tu plan declara `docs/deskops-ui.md` como contrato para cualquier UI. | No se sabe si D1 extiende, reemplaza o ignora eso. |

## 3. Defectos del DAG

**Dependencias externas**
1. **Referencias "no disponibles": obsoleto [V].** Las cuatro existen con otro slug, creadas hacia las 00:16–00:17, después del paquete (00:10):
   - `task-workspace-…-grafo-local-…`
   - `task-vista-changes-arbol-de-hashes-…`
   - `task-edicion-contextual-…` y `task-adaptador-…-prueba-integral-…`
   - `task-integracion-…-del-desk.md`

   Tres están en el Board de graph_ui y sin commitear. Hay otra sesión activa ahí.
2. **Tres planes para lo mismo [V].** El Board de graph_ui tiene su "DAG Knowledge Workspace UI" y tu plan vigente tiene E3 (página de tarea, `runtime dispatch`, `CommentDoc`, diff, vendorizar CDN). Este DAG no menciona ese plan. Además E1–E3 se solapan con él y sus IDs chocan.
3. **Gate de E1 invisible [V].** La tarea de closeout sigue `active` en `ritual-testing`, con `closure.py` modificado sin commitear. No es una arista: `validation.txt` solo comprueba que el archivo existe y coloca E1 en la capa 4.

**Aristas**
4. **Faltan A1→A3/A4/A5.** A3 exige nombrar operaciones reales y A4 dueños, pero ambos corren en paralelo con la auditoría. El borrador de user-flows hoy no nombra ninguna operación.
5. **B2 y B3 no son paralelos [I].** La selección compartida y el "mismo origen" de B3 dependen de la identidad de B2. El README además reparte "navegación" de forma distinta al DAG.
6. **C1 duplica a B2 [V].** Ambos clasifican huecos, con 4 y 5 categorías distintas. C1 no aporta un entregable propio y alarga el camino.
7. **C2→D1 sobra [I].** Un shell lector no necesita entradas nuevas; ya existen `desk/README.md`, Board y registro. Bloquea la primera lectura detrás de 6 nodos, cuando el README dice que D1 "no espera".
8. **D2→D4 también es dudosa [V].** `advance` ya funciona, y ack, `message` y `bind` no dependen de un editor.
9. **F1 mezcla cosas [V].** Las referencias rotas son exigidas por UF01, pero llegan después de D2/D3. Se confunde error de lectura con vista Changes. Si la ruta condicional crece, puede bloquear G1 y H1.
10. **E1←B3 sin razón [I].** Un contrato de interacción no gobierna la identidad de intentos.
11. **Deriva y ruido [V].** La tabla del README dice E2←D2; YAML, candidata y README L72 dicen E1, B3. La arista redundante en YAML es B3→E2, junto con A4→C3 y A5→H1.

**Orden y granularidad**
12. **La validación humana llega tarde [V].** G1 es la primera y tiene 16 nodos antes. Ruta más larga: A5-B1-B2-C1-C2-D1-D2-F1-G1. Contradice el principio de no aprobar por tests.
13. **Granularidad [V].** Solo D1 y D4 están marcados para atomizar. D2, D3, F1, C2, A1 y E2 también son paquetes; D3 son al menos cuatro renderers.
14. **Falta lo mínimo para ordenar [V].** No hay archivos por nodo, así que "sin solapamiento" no se puede comprobar. No hay estimaciones, que tu `CLAUDE.md` exige. C2 y D* requieren tareas en otros desks, y el plan no dice cómo se promueven ahí.

## 4. Documentos: qué se puede redactar ya

**Ya:**
- `inventario.md` (A1): no necesita ninguna decisión y muchos datos ya están verificables.
- Glosario y distinciones de la visión.
- UF01–UF03 y UF07 como intención, con el mapa a operaciones. `atoms split|merge`, `proto`, `message` y `sldb find` existen [V].
- Índice del manual y capítulos conceptuales, previa captura en átomos.

**Requieren decisión:**
| Documento | Decisión pendiente |
|---|---|
| UF04/UF05 | Cierre en la UI, relación con git |
| UF06 | Reconciliar con E3 de tu plan |
| UF08 | Modelo multi-desk; hoy la UI se configura por proceso con `SLDB_STORE`/`DESKOPS_ROOT` [V] |
| `vistas.md` (fichas) | Unidad documento/nodo, alcance de ViewDoc |
| `contrato-producto`, `-navegacion`, `-interaccion` | Todas las de §2 |
| Manual §15 | No tiene flujo ni nodo |
| "Proyecto de ejemplo" | El README lo da por fijado, pero `manual.md` no nombra ninguno [V] |

## 5. Omisiones de recorridos y superficies

- **Búsqueda:** está en visión, UF03 y G1, pero ningún nodo la implementa. D1 no la lista.
- **Delegar desde la UI:** E3 es solo lectura. Lanzar, responder y decidir de UF06 no tienen nodo, así que G2 no puede pasar.
- **Revisión:** UF05 pide cambios y comparar con el contrato, pero no hay diff de tarea ni comentarios. F1 Changes mide integridad del store, no el diff.
- **UF08:** sin nodo. `message send` existe, pero el contexto multi-store y el envío desde la UI no.
- **UF02:** captura y ack dependen de D4, sin aceptación propia. G1 no enumera qué UF valida (¿UF07 y UF08 entran?).
- **Arranque:** instalar, primer uso, proyecto sin desk. Mindmap depende de esm.sh [V], y el commit `4c1f9da` registró un bloqueo de CDN [V].
- **Filas ausentes en `vistas.md` [V]:** pills, fases, specs y diagramas, issues, código. Los pills sí están en la visión, y `vision.md` admite el código como soporte no Markdown.
- **UF para reparar:** F1 entrega diagnóstico, no las reparaciones que UF07 promete.

## 6. Veredicto y correcciones prioritarias

**No aprobar para promoción.** La validación PASS solo prueba que el grafo es acíclico, no que el producto sea coherente. Mantener como propuesta y hacer esto, en orden:

1. **Reconciliar antes de avanzar.** Una sola línea de producto entre este DAG, el Board de graph_ui y E3 de tu plan. Corregir las cuatro rutas y detener la duplicación con la otra sesión.
2. **Añadir un nodo de decisión del dueño antes de B1.** Debe fijar:
   - documento o nodo como unidad;
   - UI anfitriona;
   - Kimun: propongo excluirlo y escribir contra sldb;
   - cierre fuera de la UI;
   - política de escritura por campo y relación con git;
   - quién escribe cuando hay coordinador.
3. **Recablear.**
   - Añadir A1→A3/A4/A5.
   - Unir B2+C1 y colgar B3 de ellos.
   - Sacar C2 de D1.
   - Modelar closeout como gate real.
   - Partir F1 en errores inline y Changes.
   - Corregir la tabla de E2 y renombrar C2 de Kimun.
4. **Cortar por rebanadas validadas.** Un G0 tras D1 (UF01 solo lectura con búsqueda), y un gate por grupo de UF. Asignar cada UF a un gate, con umbrales de latencia y uso.
5. **Completar la matriz UF→nodo→archivos→operación→dueño→estimación.** Crear los nodos que faltan: búsqueda, diff y revisión, acciones de delegación, multi-desk, arranque y vendorizar CDN. Atomizar D2, D3, F1 y C2.
