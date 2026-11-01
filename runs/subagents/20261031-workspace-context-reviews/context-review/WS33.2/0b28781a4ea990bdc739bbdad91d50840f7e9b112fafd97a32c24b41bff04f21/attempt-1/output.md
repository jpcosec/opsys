REFORMULACION
- Propósito: registrar una decisión humana explícita —aprobar o pedir corrección— asociada a un intento y, por él, a su tarea.
- Resultado: registro con actor humano, referencia al intento y a la tarea, resultado explícito y texto obligatorio cuando sea “pedir corrección”; “completed” del agente nunca equivale a aprobado.
- Repo: deskops. Salidas previstas: runtime/ según contrato, modelos/reportes y tests/.
- Límites: no escribe “validado” ni “cerrado”; no reporta “completed”; solo usa la operación que fije WS12 y, si falta, registra hueco con dueño. No toca tablas Scion. Es delivery, no agregado.

AMBIGUEDADES
ninguna

DRY-RUN
- Lecturas: contrato WS12 y recibo per_delta de G_WRITE_CONTRACT para WS33.2; salidas de WS32 sobre identidad de intento/RunDoc y vínculo con tarea; salidas de WS33.1 sobre referencias a mensajes/resultados; evidencia de G_SCION producida por WS44; decisiones.md, alcance.md y TaskDoc de promoción.
- Cambios previstos: en deskops, operación/adaptador de registro de decisión; modelo o reporte de decisión; pruebas. Campos mínimos: actor, intento, tarea, resultado aprobar|pedir corrección, texto obligatorio en corrección. “Completed” no admitido como aprobación.
- Dependencias: WS12 define operación, actor, efectos y errores; WS32 aporta identidad del intento y su tarea; WS33.1 aporta vínculos. G_SCION debe estar verificado y G_WRITE_CONTRACT requiere recibo del efecto concreto de WS33.2.
- Errores: si falta contrato, operación, identidad de intento/tarea o G_SCION, detenerse y registrar el hueco con repo dueño; no crear sustituto.
- Validación esperada: pruebas de aprobar, pedir corrección con texto, rechazo sin texto, actor/intento/tarea obligatorios, lectura de vuelta y no asimilación de “completed” a aprobado; sin red ni tablas Scion.

FUTURO
- WS12 produce el contrato y la operación; WS32/WS32.1/WS32.2, la identidad de intento y su tarea; WS33.1, los vínculos de mensajes/resultados; WS44 resuelve G_SCION; WS37 valida con agente real; el receptor P01 emite el acta por delta. WS34–WS36 podrán consumir la decisión registrada.
