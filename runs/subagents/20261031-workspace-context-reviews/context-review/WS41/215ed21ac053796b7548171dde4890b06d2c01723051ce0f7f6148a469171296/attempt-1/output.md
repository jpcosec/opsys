REFORMULACION
Propósito: fijar como encargo ejecutable la lectura segura entre desks en `graph_ui`. Resultado: leer un segundo desk/store mediante aliases/roots autorizados por WS11, mostrar identidad/origen, seguir enlaces authored y volver por la historia; alias no autorizado, path escapado y store ausente deben dar error visible. Repo: `graph_ui` (`frontends/mindmap/source/`, `views/workspace/`, `tests/`). Límites: solo lectura, sin mutaciones cruzadas, sin cambiar el global `SLDB_STORE`, sin afirmar federación por copia; promoción no autorizada. Depende de WS11 (contrato), WS13 (lector/historia), WS40 (corpus/manifiesto) y G_UI_READ por delta.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, nodo WS41, vecinos WS11/WS13/WS40 y gate G_UI_READ.
Cambios previstos: resolución de contexto por store en `graph_ui` usando APIs públicas y el contrato WS11; UI de identidad/origen, navegación de enlaces e historia; estados de error; pruebas con los dos stores del manifiesto WS40.
Dependencias: contrato WS11 con aliases/roots; lector e historia WS13; corpus, manifiesto y enlaces authored WS40; recibo G_UI_READ del delta concreto.
Validaciones futuras: pruebas de lectura cruzada y retorno; rechazo de alias/root/path no autorizado y store ausente; ausencia de mutaciones cruzadas; no alteración del `SLDB_STORE` global; UF08 humano en WS16. Nada se ejecuta ahora.

FUTURO
WS11 produce el contrato de resolución; WS40 produce corpus, manifiesto y enlaces; WS13 entrega historia/foco; P01/receptor emite el acta G_UI_READ por delta; WS16 realiza la validación humana UF08; el TaskDoc de promoción fija archivos, escenarios y textos; la autorización de promoción queda en decisión humana.
