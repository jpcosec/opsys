### WS05 [3]
1. «marca qué capabilities requieren WS32 y WS33». El input no incluye alcance ni aceptación de WS33; el ejecutor tendría que inventar qué necesidades tiene WS33 y qué capabilities marcar.
2. «señalar los campos internos que no figuren en la API pública definida en el scope». El scope dice «API pública de Scion (endpoints/SDK documentados o exportados...)», pero no fija versión ni prevalencia entre documentación y SDK exportado; si discrepan o están incompletos, el ejecutor debe inventar el criterio de qué es interfaz pública.
3. «separar slug/agente/intento/dispatch/mensaje/conversación». El glosario suministrado define “intento”, pero no define slug, dispatch ni conversación; si la API no los etiqueta, el ejecutor tendría que inventar sus equivalencias.

### WS07 [3]
1. «output_scope: decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml» frente a «leyendo ... `baseline_proposal` de dag.yaml». El input no define `baseline_proposal` ni aclara si WS07 debe modificarlo o solo leerlo. Obliga a inventar su contenido y si entra en el cierre.
2. «reconsiderar alcance según P04 dentro de las variantes ya declaradas en dag.yaml, sin editar nodos aquí». No se indican las variantes concretas ni dónde registrar esa reconsideración. Obliga a inventar el artefacto y el alcance del ajuste.
3. «registrar qué acceso read-only tiene» el operador Scion frente a «No cerrar sin registro de designación de responsables ... y operador Scion en P01». La aceptación solo exige identidad, no el nivel de acceso que el scope pide registrar. Obliga a inventar si el acceso debe constar y cómo se verifica.

### WS08 [4]
1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano»: UF03/UF04/UF05 agrupan varios pasos con operaciones distintas; obligaría a inventar si se documenta una fila por UF o una por paso.
2. «nodo y gate humano» en singular: `cobertura.md` asigna varios («WS22/26», «WS16 diagnóstico; prueba propia WS29»); obligaría a inventar si se elige uno o se listan todos.
3. «cubrir manual»: no existe UF de manual en `user-flows.md`; obligaría a inventar un flujo nuevo o a reinterpretar UF05.
4. «Nodo = ID del DAG»: no aclara si es el nodo de implementación o el de validación; el campo separado «gate humano» sugiere lo primero, pero no lo fija.

### WS09 [1]
1. «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)».  
   Obliga a decidir si «estado» mide madurez de implementación en la UI o publicación/verificación en el manual. WS10 define las etiquetas para el manual y WS04 aporta disponibilidad actual; sin una regla de precedencia, el ejecutor debe inventar la correspondencia entre ambos ejes y podría producir una aceptación no comprobable.

### WS11 [4]
1. «Un documento Markdown mantiene identidad/ruta/modelo opcional». No se define qué compone la identidad —ruta, ID estable, hash o clave por store— ni cómo se resuelve entre repos. Obligaría a inventar la semántica de identidad que luego WS13.1 debe mostrar y WS41 usar en multidesk.
2. «Resolver cada hueco como instancia/vínculo/consulta/API/renderer». Solo se definen instancia y vínculo; no hay criterio para distinguir consulta, API y renderer. Obligaría a inventar la taxonomía y, con ella, cuándo un hueco genera una dependencia nueva.
3. «si falta API abrir dependencia acotada del repo dueño antes de code». No se fija qué hace “acotada” ni cómo identificar al dueño si la API faltante no pertenece a un repo ya nombrado. Obligaría a inventar alcance y propietario de la dependencia.
4. «Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk». WS41 exige aliases/roots «explícitamente autorizados en contrato WS11», pero no se indica quién autoriza, con qué formato ni qué límites. Obligaría a inventar la política de autorización multidesk.
