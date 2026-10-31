## REFORMULACION

**Propósito:** revisar si WS34 está bien formulado como encargo de planificación. WS34 es un agregado no ejecutable: expone un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.

**Resultado:** se cumple cuando WS34.1 (dispatch autorizado) y WS34.2 (respuesta autorizada) cumplen su aceptación. Sus dependientes siguen apuntando a WS34.

**Repo dueño:** `deskops`.

**Límites:** solo adaptador público; sin shell arbitrario ni duplicar transporte; sin mandar mensajes durante planificación; autoridad del coordinador según contrato WS12; gates G_EXEC, G_SCION y G_WRITE_CONTRACT pendientes son intencionales.

## AMBIGUEDADES

Ninguna.

WS34 delega el detalle operativo en sus hijos, que ya fijan confirmación, timeout, identidad de intento y aceptación comprobable. Las dependencias futuras (WS12 y WS44) tienen productor nombrado; WS33 aporta el vínculo mensaje/intento/decisión. No hay contradicción con las fuentes suministradas ni límite que permita exceder alcance: “No shell arbitrario ni duplicar transporte” acota el adaptador.

## DRY-RUN

**Lecturas (sin ejecutar):** nodo WS34, contratos vecinos WS33/WS12/WS34.1/WS34.2/WS36, gates, guía, brief, alcance, decisiones y cobertura.

**Cambios previstos:** ninguno; esta revisión no modifica archivos ni promociona el nodo.

**Dependencias:** WS33 (vínculo de mensajes/resultados/decisiones), WS12 (contrato de operaciones y autoridad del coordinador), hijos WS34.1/WS34.2. Gates G_EXEC humano, G_SCION vía WS44, G_WRITE_CONTRACT vía WS12.

**Validaciones futuras:** aceptación de ambos hijos; dispatch aceptado y uno rechazado/vencido; reply vinculado al intento correcto y timeout reportado como fallo; integración WS36 limitada al adaptador WS34.

## FUTURO

- WS12 debe producir la whitelist/capability y autoridad del coordinador.
- WS44 debe producir G_SCION con probe real.
- Un humano debe resolver G_EXEC mediante autorización explícita.
- WS34.1 y WS34.2 ejecutan su aceptación; WS34 solo cierra cuando ambos cierran.
- WS36 consume el adaptador; no se revisa aquí.
- La promoción de WS34 sigue `not_authorized` y requiere preflight y archivos concretos en el TaskDoc.
