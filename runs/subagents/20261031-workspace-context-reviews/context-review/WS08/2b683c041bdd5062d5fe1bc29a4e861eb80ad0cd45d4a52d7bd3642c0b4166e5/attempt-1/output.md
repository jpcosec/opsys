## REFORMULACION
**Propósito:** convertir los user-flows en criterios observables, mapeando cada UF a operaciones reales de WS02/03/04.  
**Resultado:** `borradores/user-flows.md` precisado con entrada/salida, operación, error, nodo y gate humano por UF.  
**Repo:** `deskops`.  
**Límites:** solo planificación; no implementar, ejecutar ni habilitar Scion; no inventar operaciones ausentes; cubrir UF01–UF10 sin prometer funciones fuera de alcance.

## AMBIGUEDADES
1. **“cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado”**: “manual” no corresponde a ninguna UF ni a un resultado definido en la aceptación; obliga a inventar si significa un flujo, un capítulo del manual o pasos concretos.
2. **“modo degradado (UF07, fallo de backend/dependencia)”**: no se especifica si el modo degradado es un flujo propio, una fila adicional o una condición de error dentro de UF07; obliga a decidir su representación y aceptación observable.
3. **“cambios (UF07/WS29)”**: “cambios” puede aludir a la superficie Changes, a modificaciones del documento o a un UF diferenciado; obliga a inventar qué operación y nodo cubren ese término.

## DRY-RUN
**Lecturas previstas:** `borradores/user-flows.md`, `cobertura.md`, `validacion-humana.md`, `decisiones.md`, auditorías `deskops/infraestructura/ui` y nodos WS02–WS04 vía WS06/WS07.  
**Cambios previstos:** reescribir las secciones UF01–UF10 añadiendo operación, error, nodo DAG y gate humano; marcar huecos donde falte operación.  
**Dependencias:** decisiones de WS07 y auditorías transitivas de WS06; G_PRODUCT satisfecho.  
**Validaciones futuras:** revisar que cada UF tenga los cinco campos, que todas las operaciones citadas existan en auditorías y que los gates coincidan con WS16/30/37/39; WS29 solo como prueba técnica propia.

## FUTURO
WS09 consumirá el mapeo UF→renderización; WS11/WS12 usarán las operaciones y huecos declarados. Los gates humanos WS16/30/37/39 decidirán aceptación; la promoción de WS08 requiere TaskDoc con archivos, pills y evidencia, y autorización humana.
