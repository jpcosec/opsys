## REFORMULACION
**Propósito:** revisar PK04 como encargo de planificación: agrupación de revisión de navegación y representaciones, sin ejecución propia ni autorización de tareas. **Resultado:** veredicto de comprensión y disposición del nodo agregado. **Repo:** deskops. **Límites:** no evalúa producto, no revisa contratos de los `edge` vecinos, no ejecuta comandos, no añade aristas ni autoriza implementación. PK04 termina cuando sus hijos directos tienen revisión vigente o bloqueo externo con responsable.

## AMBIGUEDADES
Ninguna.

La frase «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada» remite a la integración descrita en el `scope` (WS17 consume WS11/40; WS22/23 consumen WS13/09; WS24 reutiliza vecindad), y `review_completion` fija la condición verificable. No obliga a inventar un criterio nuevo. Las menciones a TaskDoc, selección mínima de ViewDoc, textos y archivos exactos están delegadas explícitamente a promoción o a contratos con productor (WS09/WS11), por lo que no cuentan.

## DRY-RUN
**Lecturas previstas:** guía de revisión; brief, alcance, decisiones y cobertura; definición PK04 y bloques de hijos solo para confirmar dependencias. No se revisan los contratos `edge` como objetos propios.

**Cambios previstos:** ninguno en el plan; solo una `disposition.md` de revisión si el revisor la emite.

**Dependencias:** WS17 requiere WS11/WS40; WS22/WS23/WS24 requieren WS13/WS09; WS18 requiere WS09/WS11 y `G_SPEC_VIEW` por delta. `G_SPEC_VIEW` pendiente es intencional.

**Validaciones futuras, sin ejecutar:** comprobar hashes de input y contrato de cada hijo contra su revisión guardada; ejecutar `context_review.py status` desde deskops; verificar que cada `disposition.md` esté en el intento correspondiente; admitir bloqueo externo solo si registra responsable y dependencia.

## FUTURO
La sesión de coordinación ejecuta `context_review.py`, registra disposiciones y, si procede, bloqueos externos con responsable. El solicitante P01/receptor de spec2viz produce el acta por delta para `G_SPEC_VIEW` al promover WS18; ningún otro nodo sustituye esa recepción. La promoción de cada hijo fija TaskDoc, archivos, pruebas y textos dentro de su aceptación.
