## REFORMULACION
**Propósito:** convertir brief, alcance y decisiones registradas en un paquete de planificación integrado y comprobable para el workspace documental.
**Resultado sustantivo:** DAG con lector temprano, autoría/operación manual, manual publicado, extensiones independientes y ramal Scion condicionado; incluye dependencias, gates, contratos por delta y criterios de aceptación futura.
**Repo dueño:** `deskops`.
**Límites:** no implementa UI/backend ni ejecuta tareas; no migra a Kimun, no despliega infraestructura distribuida, no admite colaboración multiusuario, no hace commits automáticos ni closeout HTTP, no autoriza Scion y no modifica otros repos. Las actas y publicaciones son validaciones futuras, no producto ya entregado.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Ejecución hipotética por hijos, sin ejecutar:
1. **PK01** produce auditorías y matriz de reutilización/deltas; alimenta a PK02.
2. **PK02** consume PK01 y decisiones para fijar UFs, catálogo de vistas, convención manual, identidad/navegación WS11 y whitelist WS12; habilita PK03–PK05 y PK07.
3. **PK03** usa WS11/WS08 para lector, búsqueda, errores, Taller WS40, multidesk WS41 y acta WS16; entrega base a PK04–PK06.
4. **PK04** consume WS11/WS40 y WS13/WS09 para índices y representaciones de Board, procedimiento y conocimiento; alimenta PK05/PK06. ViewDoc queda opcional.
5. **PK05** consume WS12, WS11 y salidas de PK03/PK04 para edición segura, precondición de payload, intake, tareas, revisión/cierre y acta WS30; alimenta PK06/PK07. Respeta el orden parcial WS12→WS19/WS20/WS45→WS21/WS25/WS27/WS28 y luego WS30.
6. **PK06** consume WS17 y WS30 para publicar entradas WS43 y manual WS31.
7. **PK07** corre separado con WS15/WS24 y WS12; prueba Changes/modelos sin bloquear núcleo.
8. **PK08** consume WS05, ejecuta probe WS44 solo con operador/acceso, y produce contratos/UI Scion; cierra con WS37/WS38.

**Integración/validación futura:** WS16 valida lector; WS30 autoría/operación; WS31/WS43 manual y entradas reales; extras con prueba propia; Scion con acta WS37 y publicación WS38. Se comprobarán identidad/origen, APIs públicas, guardas/canales y ausencia de dependencias opcionales sobre núcleo. No se ejecuta nada.

## FUTURO
Los nodos hijos producen contratos, actas humanas, publicaciones y pruebas. El humano acepta deltas y decide el avance de Scion; este revisor no sustituye esos recibos.
