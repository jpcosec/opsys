## REFORMULACION

Encargo WS41 (implementation, repo graph_ui): implementar lectura segura entre desks con las rutas de lectura por store que fija el contrato WS11, resolviendo aliases/roots autorizados contra APIs públicas; cada request conserva su proyecto/store sin cambiar `SLDB_STORE` global; leer el segundo desk y volver sin mutaciones cruzadas. Resultado esperado: UF08 sobre los dos stores de WS40 (identidad/origen visibles, enlaces authored entre desks, retorno por historia) y errores visibles para alias no autorizado, path escapado y store ausente. Límites: solo lectura, sin federación por copia, gate `G_UI_READ`, `promotion: not_authorized`, depende de WS13, WS11 y WS40.

## AMBIGUEDADES

1. «configuración confiable suministrada por el operador al arrancar o al seleccionar el despliegue»: no fija soporte, formato ni punto de carga; obligaría a inventar dónde vive y cómo se lee esa configuración.
2. «designa el desk del documento de origen o de la petición actual»: la disyunción no se resuelve cuando difieren; obligaría a inventar cuál prevalece para `local:`.
3. «Leer segundo desk y volver, sin mutaciones cruzadas»: no dice si la migración de `open_store` cuenta como mutación ni qué hacer si la API pública escribe; obligaría a inventar el criterio y el remedio.

## DRY-RUN

No ejecutable hoy: `status: candidate`, `promotion: not_authorized`. Un ejecutor futuro leería contrato (3.2, 5.2, 5.4, 8.5), `workspace_routes.py`, `serve.py`, `sldb_adapter.py`, `doc_ref.py`, `doc_status.py`, `store_links.py`, `identity.py` y el manifiesto WS40. Cambios previstos: registro cerrado alias→(root,store) cargado de configuración externa; resolución por request; ruta de lectura del segundo desk; alias en URL y flujo de vuelta; contención previa a leer; `include_linked=False`; `local:` obligatorio. Pruebas en `tests/` sobre ambos stores. Dependencias: WS11 (texto), WS40 (corpus/manifiesto), WS13 (lector), gate `G_UI_READ`. Validación: UF08, E-MD1..E-MD4 visibles, store ajeno sin cambios tras leer (archivos y versión), ausencia de escritura en desk real.

## FUTURO

WS40 produce corpus, commits, enlaces authored y manifiesto; WS11 fija el contrato del input; WS13.1/13.2 dan lectura y explorador; WS13.3, historia de sesión; el operador suministra aliases reales; P01/root registran el acta `G_UI_READ` y autorizan promoción; si falta capacidad en sldb, intake explícito en el repo dueño antes de cualquier workaround.
