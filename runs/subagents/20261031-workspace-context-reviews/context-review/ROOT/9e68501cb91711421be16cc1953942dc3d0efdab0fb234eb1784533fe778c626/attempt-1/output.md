## REFORMULACION
**Propósito:** consolidar el encargo de planificación del workspace documental sobre Mindmap/SLDB/Deskops, sin ejecutar producto.
**Resultado sustantivo:** paquete integrado que reúne auditoría de base y deltas, decisiones/contratos, lector temprano, navegación y representaciones, autoría/operación manual segura, publicación de entradas/manual, extensiones independientes y ramal Scion opcional. ROOT agrupa; no ejecuta.
**Repo:** `deskops`.
**Límites:** no autoriza implementación, APIs, permisos Scion ni aceptación de deltas. Extras y Scion no son prerrequisito del núcleo; no se inventan decisiones ya registradas. La aceptación futura depende de actas humanas y publicación, no de este gate de comprensión.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Ejecución hipotética por hijos, respetando aristas y sin simultanear lo no listo:

1. **PK01** produce auditorías y matriz de deltas con repos dueños; entrega evidencia a PK02.
2. **PK02** reutiliza decisiones, define UFs, vistas, convención manual y contratos de navegación/operaciones; alimenta PK03, PK04, PK05 y contratos de PK07/PK08.
3. **PK03** entrega lector/descubrimiento probado con corpus WS40 y acta WS16; alimenta PK04, PK05 y PK06.
4. **PK04** produce entradas authored y representaciones navegables; ViewDoc queda opcional; alimenta PK05/PK06.
5. **PK05** produce autoría segura, intake/trabajo, evidencia y pruebas WS30; alimenta PK06.
6. **PK06** publica entradas reales y manual versionado desde WS17/WS30/WS10; valida WS43/31.
7. **PK07** ejecuta Changes/Schema tras las lecturas requeridas, con pruebas propias.
8. **PK08** solo tras inventario WS05, acceso/operador y probe WS44 que produzca G_SCION; WS32–36 y acta WS37/38.

**Integración/validación futura:** contrastar identidad/origen compartidos, APIs públicas, guardas/canales, manual trazado y ausencia de dependencias opcionales sobre núcleo; actas WS16/30, publicaciones WS43/31, pruebas propias de PK07 y aceptación Scion WS37/38.

## FUTURO
Producen otros nodos: contratos WS11/WS12, G_SOURCE WS20, actas WS16/WS30, publicaciones WS43/31, prueba WS39 y habilitación Scion WS44/WS37/38. Decide el humano la aceptación por delta y el acceso Scion. No ejecutado aquí.
