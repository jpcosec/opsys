### WS17 [3]
1. Mecanismo de resolución dinámica: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» frente a «El generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se define si las plantillas usan rutas relativas, placeholders o reescritura por WS40; obligaría a inventar el formato de parametrización y quién lo aplica.
2. Cobertura entre dos desks: título/scope «entradas/índices del desk ejemplo» y aceptación «los dos desks del manifiesto WS40». No queda fijado si WS17 debe authorar índices para ambos o solo enlazar desde uno; obligaría a inventar qué plantillas pertenecen a cada desk.
3. Límite de no duplicación: «no duplicar el registry de deskops» y «sin copiar inventarios derivados» no definen qué contenido de índice cuenta como duplicado; obligaría a inventar el borde entre enlace authored y copia de inventario.

### WS22 [3]
1. «con las dependencias declaradas en el TaskDoc» / «Las tres representaciones (lista, tablero y dependencias) abren el mismo TaskDoc»: no se define qué debe mostrar la representación de dependencias (aristas, lista, dirección, agrupación) ni qué hacer si el TaskDoc no las declara. Obliga a inventar el resultado y permite aceptar una vista vacía.
2. «no duplicar tareas ni presentar predicado satisfecho como test aprobado»: «predicado» no está definido en las fuentes. Obliga a inventar qué elemento de Board/lifecycle es predicado y cómo comprobar que no se confunde con un test aprobado.
3. «matriz WS06 llega de forma transitiva por WS11/WS12»: WS12 no figura en `depends_on` ni en la cadena visible (WS22→WS13→WS11; WS22→WS09). Obliga a decidir si falta una dependencia o si la matriz no es requisito de este nodo.

### WS24 [3]
1. «Vecindad = hasta 2 hops» y «la vecindad de hasta 2 hops». No indica dirección ni tipos de relación: ¿entrantes, salientes o ambas? Obliga a inventar el criterio de recorrido y qué validar.
2. «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» frente a «La vista muestra la clasificación (tipo y tags)» y «un soporte no modelado (Markdown sin modelo)». No queda definido qué clasificación mostrar sin modelo, ni si los tags provienen del modelo o del documento. Obliga a inventar representación y fuente.
3. «preservar Code local del ticket workspace en draft que identifique el acta WS11» figura en `scope`, pero no en `acceptance`. El ejecutor tendría que inventar cómo preservarlo, cómo verificarlo y qué significa identificar el acta.
