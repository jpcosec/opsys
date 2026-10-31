REFORMULACION
Propósito: producir plantillas Markdown authored de entradas/índices para el desk ejemplo, no el corpus. Resultado: plantillas versionadas bajo `ejemplo/nav/` del paquete del plan, materializables por WS40. Repo dueño: deskops. Límites: solo fuentes authored; no generar corpus, no copiar inventarios derivados, no escribir repos reales, no duplicar registry; depende de WS11 y WS40.

AMBIGUEDADES
1. Mecanismo de resolución dinámica: «cada plantilla resuelve el root/store de procedencia de los dos desks del manifiesto WS40» frente a «El generador de WS40 acepta estas fuentes y las materializa bajo su root temporal». No se define si las plantillas usan rutas relativas, placeholders o reescritura por WS40; obligaría a inventar el formato de parametrización y quién lo aplica.
2. Cobertura entre dos desks: título/scope «entradas/índices del desk ejemplo» y aceptación «los dos desks del manifiesto WS40». No queda fijado si WS17 debe authorar índices para ambos o solo enlazar desde uno; obligaría a inventar qué plantillas pertenecen a cada desk.
3. Límite de no duplicación: «no duplicar el registry de deskops» y «sin copiar inventarios derivados» no definen qué contenido de índice cuenta como duplicado; obligaría a inventar el borde entre enlace authored y copia de inventario.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS17 y bloques de contrato vecinos WS11/WS40/WS30/WS43, sin revisarlos. Cambios previstos: plantillas Markdown authored en `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`, sin corpus ni repos reales. Dependencias: contrato WS11 y generador/manifiesto WS40. Validaciones futuras: regenerar corpus WS40 con `ejemplo/nav/`, recorrer links Markdown sin UI, comprobar que cada plantilla resuelve roots/stores de los dos desks y que no se duplica registry; WS30 integra en recorrido humano. No se ejecuta.

FUTURO
WS40 materializa las plantillas y produce manifiesto/corpus temporal; WS30 valida aceptación humana; WS43 publica en deskops real. La promoción de WS17 sigue `not_authorized` y requiere decisión/acción humana y TaskDoc.
